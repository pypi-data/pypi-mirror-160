from __future__ import annotations  # Enable PEP585 for Python3.8

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from dataproc.conf import Config
# from dataproc.crawlers.http_client import (Response, http_get, http_get_async,
#                                           make_agent_headers)
from dataproc.crawlers import aio_fetch, fetch
from dataproc.crawlers.managers.page import AIOPageManager
from dataproc.crawlers.parsers import authors
from dataproc.crawlers.parsers.page import Page, text_to_predict2
from dataproc.crawlers.parsers.url import (URL, get_country_from_tld,
                                           parse_url2, url2docid, url_norm)
from dataproc.utils import Timeit
from dataproc.words import lang

# from dataproc.words.utils import get_locale


@dataclass
class CrawlPageTask:
    url: str
    strategy: str = "axios"
    store: bool = False
    locale: Optional[str] = None
    user_agent: str = Config.AGENT
    predict_lang: bool = False
    article_data: bool = False
    namespace: Optional[str] = None
    datastore: Optional[str] = None


@dataclass
class PageResponse:
    url: URL
    page: Union[Page, None]
    docid: str
    cached: bool
    status: int


@dataclass
class PageRSP3:
    fullurl: str
    url: str
    docid: str

    domain_base: str
    siteid: str
    country_tld: Optional[str] = None

    meta_img: Optional[str] = None
    meta_desc: Optional[str] = None
    page_h1: Optional[str] = None
    page_h2: Optional[str] = None
    page_article: Optional[str] = None
    page_authors: Optional[List[str]] = None
    page_title: Optional[str] = None
    page_html_lang: Optional[str] = None
    page_date: Optional[str] = None

    ml_lang: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class FullPageResponse:
    url: URL
    page: Page
    docid: str
    cached: bool
    lang: str
    # text_predict: str
    article_data: Optional[str] = None
    ns: Optional[str] = None
    ds: Optional[str] = None


@dataclass
class PageMLResponse:
    data: Dict[str, Any]
    page: Page


@Timeit
def crawl_page_sync(t: CrawlPageTask) -> Page:
    """
    Simple Old method
    """
    url = url_norm(t.url)
    req = fetch.from_url(url)
    req.strategy = t.strategy
    req.user_agent = t.user_agent
    # h = make_agent_headers(t.user_agent)
    # r = http_get(url, headers=h)
    r = fetch.get(req)
    p = Page.from_html_txt(url, r.text)

    return p


@Timeit
async def crawl_page_async2(t: CrawlPageTask, timeout=15) -> PageResponse:
    """ timeout in seconds """
    url = url_norm(t.url)
    req = aio_fetch.from_url(url)
    req.strategy = t.strategy
    req.user_agent = t.user_agent
    req.ts = timeout

    rsp = await aio_fetch.get(req)

    p = Page.from_html_txt(url, rsp.text)
    return PageResponse(url=url, page=p, docid="", cached=False, status=rsp.status)


async def crawl_page_async(session, original: str, strategy="axios") -> PageResponse:
    # url = URL.from_str(original)
    # _key = AIOSiteManager.url2docid(original)
    docid = url2docid(original)
    url = docid.url
    _key = docid.key

    cached = True
    status = 304

    try:
        page = await AIOPageManager.get_fullpage(session, _key)
    except IndexError:
        cached = False
        page = None

    if not page:
        req = aio_fetch.from_url(url.fullurl)
        req.strategy = strategy
        # rsp = await http_get_async(url.fullurl)
        rsp = await aio_fetch.get(req)
        status = rsp.status
        html = rsp.text
        page = Page.from_html_txt(url.fullurl, html)

    return PageResponse(url=url, page=page, docid=_key, cached=cached, status=status)


async def get_or_crawl_page_async(session,
                                  cpt: CrawlPageTask) -> FullPageResponse:
    resp = await crawl_page_async(session, cpt.url, cpt.strategy)
    if cpt.predict_lang:
        txt_predict = text_to_predict2(resp.page)
        _lang = lang.predict_txt(txt_predict)
        resp.page.web.html_lang = _lang
    else:
        _lang = resp.page.web.html_lang

    if cpt.store and not resp.cached:
        await AIOPageManager.save(session, resp.page, cpt.datastore, cpt.namespace)
    #article_text = None
    # if cpt.article_data:
    #    try:
    #        article = resp.page.article_data()
    #        article_text = article.text
    #        try:
    #            content_date = resp.page.get_date(article).isoformat()
    #        except:
    #            content_date = None
    #    except:
    #        article_text = None
    #        content_date = None

    return FullPageResponse(
        url=resp.url,
        page=resp.page,
        docid=resp.docid,
        cached=resp.cached,
        lang=_lang,
        # article_data=article_text,
        ns=cpt.namespace,
        ds=cpt.datastore,
    )


def _h1_h2(page):
    try:
        h1 = page.web.content.h1[0]
    except IndexError:
        h1 = None
    except AttributeError:
        h1 = None

    try:
        h2 = page.web.content.h2[0]
    except IndexError:
        h2 = None
    except AttributeError:
        h2 = None

    return h1, h2


def _siteid_from_url2(url2):
    _site_url = "http://"
    if url2.secure:
        _site_url = "https://"
    _site_url = f"{_site_url}{url2.netloc}"
    site_id = url2docid(_site_url)

    return site_id.key


def transform(page: Page, stopw, as_dict=False) -> Union[Dict[str, Any], PageRSP3]:
    """ Extract the most relevant information to apply ML and Index content """
    _doc = url2docid(page.url)
    _key = _doc.key
    _url = _doc.url
    h1, h2 = _h1_h2(page)
    art = page.article_data()
    page_dt = page.get_date(art)
    try:
        page_date = page_dt.isoformat()
    except AttributeError:
        page_date = None
    url2 = parse_url2(page.url)

    country_tld = get_country_from_tld(url2.tld)
    if country_tld:
        country_tld = country_tld.alpha2

    meta_og_image = page.find_og("image")
    meta_desc = page.find_og("desc")
    ml_lang = lang.predict_txt(page.web.title)
    authors_ = authors.get_from_ld(page.web.ld_data, stopw)
    page_authors = None
    if authors_:
        page_authors = authors_.authors_norm
    siteid = _siteid_from_url2(url2)

    rsp = dict(
        fullurl=_url.fullurl,
        url=_url.url,
        docid=_key,
        domain_base=url2.domain_base,
        siteid=siteid,
        country_tld=country_tld,
        meta_img=meta_og_image,
        meta_desc=meta_desc,
        page_h1=h1,
        page_h2=h2,
        page_article=art.text,
        page_authors=page_authors,
        page_title=page.web.title,
        page_html_lang=page.web.html_lang,
        page_date=page_date,
        ml_lang=ml_lang
    )
    if as_dict:
        return rsp
    return PageRSP3(**rsp)
