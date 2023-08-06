from dataclasses import dataclass

from dataproc.crawlers.models import CrawlerBucketModel, PageModel
from dataproc.crawlers.parsers.page import Page
from dataproc.crawlers.parsers.url import url2docid
from dataproc.datastore import AIODataBucket, DataBucket
from dataproc.datastore.managers import create_bucket_async, find_ds_async
from dataproc.utils import today_string
from db.utils import Pagination, get_total, get_total_async, pagination
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload


@dataclass
class PageSave:
    url: str
    docid: str
    bucket: DataBucket

    def get(self):
        r = self.bucket.read(key=self.docid)
        return r.json()


@dataclass
class AIOPageSave:
    url: str
    docid: str
    bucket: AIODataBucket

    async def get(self):
        r = await self.bucket.read(key=self.docid)
        return r.json()


def insert_page_stmt(page: Page, bucket_id, do_nothing=False):
    docid = url2docid(page.url)
    _url = docid.url
    _key = docid.key

    site_root = _url.url.split("/")[0]
    site_docid = url2docid(site_root)
    siteid = site_docid.key
    _lang = None
    if page.web.html_lang:
        _lang = page.web.html_lang[:2]

    stmt = insert(PageModel.__table__).values(
        docid=_key,
        siteid=siteid,
        urlnorm=_url.url,
        www=_url.www,
        secure=_url.secure,
        bucket_id=bucket_id,
        lang=_lang,

    )
    if do_nothing:
        stmt = stmt.on_conflict_do_nothing()
    else:
        stmt = stmt.on_conflict_do_update(
            # constraint="crawlers_page_bucket_id_fkey",
            index_elements=["id"],
            set_=dict(bucket_id=bucket_id)
        )
    # await session.execute(stmt)

    data = {"html": page.html, "fullurl": _url.fullurl}
    return stmt, dict(docid=_key, data=data, url=_url.url)


class AIOPageManager:

    @staticmethod
    async def get_page(session, docid) -> PageModel:
        stmt = select(PageModel).where(PageModel.docid == docid).options(
            selectinload(PageModel.bucket))
        result = await session.execute(stmt)
        urlmodel = result.scalar()
        return urlmodel

    @classmethod
    async def get_fullpage(cls, session, docid) -> Page:
        u = await cls.get_page(session, docid)
        if not u:
            raise IndexError(f"{docid} not found in db")
        bucket = AIODataBucket(id=u.id,
                               datastore=u.bucket.datastore,
                               namespace=u.bucket.namespace)
        rsp = await bucket.read(u.docid)
        data = rsp.json()

        if "error" in data.keys():
            raise IndexError(f"{docid} not found in datastore")
        # fullurl = "http://"
        # if u.secure:
        #   fullurl = "https://"
        # if u.www:
        #     fullurl = f"{fullurl}www."
        # fullurl = f"{fullurl}{u.urlnorm}"
        p = Page.from_html_txt(data["fullurl"], data["html"])
        p.created_at = u.created_at.isoformat()
        return p

    @staticmethod
    async def get_or_create_bucket(session, ds, ns) -> AIODataBucket:
        bucket = await find_ds_async(session,
                                     CrawlerBucketModel,  ds, ns)
        if not bucket:
            bucket = await create_bucket_async(session,
                                               CrawlerBucketModel, ds, ns)

        return bucket

    @classmethod
    async def save(cls, session, page: Page, ds, ns) -> AIOPageSave:

        bucket = await cls.get_or_create_bucket(session, ds, ns)

        stmt, data = insert_page_stmt(page, bucket.id)
        await session.execute(stmt)
        r = await bucket.write(data["docid"], data["data"], mode="w",
                               replace=True
                               )
        if r.status > 201:
            raise AssertionError(f"{page.url} failed to write into datastore")

        return AIOPageSave(url=data["url"], docid=data["docid"], bucket=bucket)

    @staticmethod
    async def list_(session, page=1, limit=100, lang=None, lastday=False):
        total = await get_total_async(session, PageModel)
        page = Pagination(total=total, limit=limit, page=page)
        stmt = select(PageModel).options(
            selectinload(PageModel.bucket))

        slct = stmt.order_by(PageModel.created_at.desc())
        if lang:
            slct = slct.where(PageModel.lang == lang)
        if lastday:
            today = today_string(format_="day")
            slct = slct.where(PageModel.created_at >= today)
        stmt, next_p = pagination(slct, page)
        rsts = await session.execute(stmt)
        results = rsts.scalars()
        return {
            "rows": [r.to_dict() for r in results],
            "next_p": next_p,
            "total": total
        }


class PageManager:

    @staticmethod
    def save(session, page: Page, bucket: DataBucket) -> PageSave:

        stmt, data = insert_page_stmt(page, bucket.id)
        session.execute(stmt)

        r = bucket.write(data["docid"], data["data"], mode="w", replace=True)
        if r.status > 201:
            raise AssertionError(f"{page.url} failed to write into datastore")

        return PageSave(url=data["url"], docid=data["docid"], bucket=bucket)

    @staticmethod
    def list(session, page=1, limit=100, lang=None, lastday=False):
        total = get_total(session, PageModel)
        page = Pagination(total=total, limit=limit, page=page)
        slct = select(PageModel)\
            .order_by(PageModel.created_at.desc())
        if lang:
            slct = slct.where(PageModel.lang == lang)
        if lastday:
            today = today_string(format_="day")
            slct = slct.where(PageModel.created_at >= today)
        stmt, next_p = pagination(slct, page)
        results = session.execute(stmt).scalars()
        return {
            "rows": [r.to_dict() for r in results],
            "next_p": next_p,
            "total": total
        }
