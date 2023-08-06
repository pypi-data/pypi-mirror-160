import asyncio
from dataclasses import asdict

import httpx
from dataproc.conf import Config
from dataproc.crawlers.indexes import AIOSearch
from dataproc.crawlers.managers.bucket import AIOBucketManager
from dataproc.crawlers.managers.page import AIOPageManager
from dataproc.crawlers.managers.site import AIOSiteManager
from dataproc.crawlers.page import (CrawlPageTask, get_or_crawl_page_async,
                                    transform)
from dataproc.crawlers.root import CrawlRootTask, restore_root_page
from dataproc.crawlers.url_index import (create_url_bucket_async,
                                         find_url_bucket_async)
from dataproc.utils import get_query_param, parse_page_limit
from dataproc.words.parsers import load_stop
from dataproc.workflows.core import NBTask, nb_job_executor
from dataproc.workflows.scheduler import SchedulerExecutor
from iso3166 import countries
from sanic import Blueprint, Sanic
from sanic.response import json
from sanic_ext import openapi

crawlers_bp = Blueprint("crawlers", url_prefix="crawlers")
stopw = load_stop(lang="any")

_URLS_NS = "crawl.urls"


@crawlers_bp.listener("before_server_start")
async def startserver(current_app, loop):
    current_app.ctx.sonic = AIOSearch()

    session = current_app.ctx.db.sessionmaker()

    async with session.begin():
        b = await find_url_bucket_async(session, _URLS_NS)
        if not b:
            b = await create_url_bucket_async(session, Config.RAWSTORE, _URLS_NS)
    current_app.ctx.url_bucket = b
    current_app.ctx.url_index = f"{b.datastore}/{b.namespace}"
    await current_app.ctx.sonic.init_search()


@crawlers_bp.listener("after_server_stop")
async def shutdown(current_app, loop):
    await current_app.ctx.sonic.close()


@crawlers_bp.get("/pages")
@openapi.parameter("page", int, "query")
@openapi.parameter("limit", int, "query")
@openapi.parameter("lang", str, "query")
@openapi.parameter("lastday", int, "query")
async def all_pages_handler(request):
    session = request.ctx.session
    lang = get_query_param(request, "lang", None)
    lastday = get_query_param(request, "lastday", False)
    page, limit = parse_page_limit(request)
    async with session.begin():
        sites_data = await AIOPageManager.list_(
            session, page, limit, lang, lastday)

    return json(sites_data)


@crawlers_bp.get("/pages/<docid>")
@openapi.parameter("docid", str, "path")
async def page_handler(request, docid):
    session = request.ctx.session

    try:
        async with session.begin():
            p = await AIOPageManager.get_fullpage(session, docid)
        return json(asdict(p))
    except IndexError:
        return json(dict(error=f"{docid} not found"), 404)


@crawlers_bp.post("/pages/_crawl")
@openapi.body({"application/json": CrawlPageTask})
async def page_crawler_handler(request):
    """ Crawl simple page
    It will crawl sync the site and store it
    """
    data = CrawlPageTask(**request.json)
    session = request.ctx.session
    async with session.begin():
        rsp = await get_or_crawl_page_async(session, data)

    return json(asdict(rsp))


@crawlers_bp.post("/pages/_crawl2")
@openapi.body({"application/json": CrawlPageTask})
async def page_crawler_handler2(request):
    """ Crawl simple page
    It will crawl sync the site and store it
    """
    data = CrawlPageTask(**request.json)
    session = request.ctx.session
    async with session.begin():
        rsp = await get_or_crawl_page_async(session, data)
    page = transform(rsp.page, stopw, as_dict=True)
    page["created_at"] = rsp.page.created_at

    return json(page)


@crawlers_bp.post("/sites/_run")
@openapi.body({"application/json": CrawlRootTask})
def root_crawler_handler(request):
    """ Crawl root site
    Enqueue a crawl_root_task (register_site). 
    If the site doesn't exist, it will be registered.
    This endpoint requires RQ and dask running.
    """
    crt = CrawlRootTask(**request.json)
    data = asdict(crt)

    current_app = Sanic.get_app("crawler")
    nb_task = NBTask(name="register_site", params=data, timeout=60*5)

    jobid = SchedulerExecutor.jobid()

    job = current_app.ctx.Q.enqueue(nb_job_executor, nb_task, job_id=jobid)
    return json(dict(jobid=job.id), status=202)


@crawlers_bp.get("/sites/<siteid>")
@openapi.parameter("data", bool, "query")
@openapi.parameter("siteid", str, "path")
async def site_handler(request, siteid):
    """ Get Site
    Get site information from the db. If data is sent true, then it will
    get also the data stored in the rawstore. If the site doesn't exist yet, then
    will be raise an error
    """
    session = request.ctx.session

    include_data = get_query_param(request, "data", False)
    root_page_data = None
    try:
        async with session.begin():

            rs = await AIOSiteManager.get_root(session, siteid=siteid)
            if include_data and rs:
                if rs:
                    data = await rs.get()
                    rp = restore_root_page(data)
                    root_page_data = asdict(rp)

        return json(dict(
            fullurl=rs.fullurl,
            url=rs.url,
            siteid=rs.siteid,
            ds=rs.bucket.datastore,
            ns=rs.bucket.namespace,
            label=rs.label.name,
            country=rs.country,
            lang=rs.lang,
            data=root_page_data
        ))
    except IndexError:
        return json(dict(error=f"{siteid} not found"), 404)


@crawlers_bp.get("/sites/labels")
async def all_labels_handler(request):
    """ List buckets registered from the database """

    session = request.ctx.session

    async with session.begin():
        rows = await AIOSiteManager.list_labels(session)
    return json(rows)


@crawlers_bp.get("/sites")
# @openapi.parameter("page", int, "query")
# @openapi.parameter("limit", int, "query")
@openapi.parameter("label", str, "query")
@openapi.parameter("country", str, "query")
@openapi.parameter("lang", str, "query")
async def all_sites_handler(request):
    """ List all sites from db """
    label = get_query_param(request, "label", None)
    country = None
    country_str = get_query_param(request, "country", None)
    if country_str:
        country = countries.get(country_str)

    lang = get_query_param(request, "lang", None)
    session = request.ctx.session
    async with session.begin():
        sites = await AIOSiteManager.list_(session, label, country, lang)

    return json(sites)


async def _get_url(client, bucket_url, docid):
    r = await client.get(f"{bucket_url}/{docid}")
    return r.json()


@crawlers_bp.get("/urls/_search")
@openapi.parameter("q", str, "query")
@openapi.parameter("lt", int, "lt")
async def url_search_handler(request):
    """ Get Site
    Get site information from the db. If data is sent true, then it will
    get also the data stored in the rawstore. If the site doesn't exist yet, then
    will be raise an error
    """
    # session = request.ctx.session

    to_search = get_query_param(request, "q", "")
    limit = get_query_param(request, "lt", 10)
    to_search = to_search.lower()

    current_app = Sanic.get_app("crawler")
    bucket_url = current_app.ctx.url_index
    docs = await current_app.ctx.sonic.query(to_search, bucket=_URLS_NS,
                                             limit=limit)

    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*[_get_url(
            client, bucket_url, d.decode())
            for d in docs])

    return json({"rows": results})
