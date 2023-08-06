from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, List, Union

from dataproc.crawlers.links_extractors import CrawlLink
from dataproc.crawlers.models import (CrawlerBucketModel, SiteLabelModel,
                                      SiteModel)
from dataproc.crawlers.parsers.html import WebSite
from dataproc.crawlers.parsers.rss import find_rss_links
from dataproc.crawlers.parsers.url import (URL, get_country_from_tld,
                                           parse_url2, url2docid,
                                           url_base_name)
from dataproc.datastore import AIODataBucket, DataBucket
from dataproc.datastore.managers import create_bucket, find_ds
from hashes.noncrypto import Hasher
from iso3166 import countries
from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload


def rebuild_url_from_model(model):
    url = "http://"
    if model.secure:
        url = "https://"
    if model.www:
        url = f"{url}www."
    return f"{url}{model.urlnorm}"


@dataclass
class SiteLabel:
    id: int
    name: str

    @staticmethod
    def create(session, name):
        stmt = insert(SiteLabelModel.__table__).values(name=name)
        stmt = stmt.on_conflict_do_nothing()
        # ts = TypeSite(name=name)
        session.execute(stmt)

    @staticmethod
    def listall(session):
        stmt = select(SiteLabelModel)
        result = session.execute(stmt).scalars()
        return [r.to_dict() for r in result]

    @classmethod
    def from_db(cls, session, name: str):
        stmt = select(SiteLabelModel).where(
            SiteLabelModel.name == name).limit(1)
        result = session.execute(stmt).scalar()
        if result:
            return cls(id=result.id, name=result.name)
        return None


@dataclass
class RootPage:
    url: str
    web: WebSite
    html: str
    links: Dict[str, CrawlLink]
    social: List[str]

    @property
    def base_name(self):
        u = parse_url2(self.url)
        return u.domain_base

    @property
    def key(self):
        _url = URL.from_str(self.url)
        return Hasher.xxhash64(_url.url).hexdigest

    def find_og(self, prop):
        for x in self.web.og_tags:
            for p in x.get("properties"):
                if f"og:{prop}" in p[0]:
                    return p[1]
        return None

    def has_rss(self):
        for _, x in self.links.items():
            if x.source == "rss":
                return True
        return False

    def has_sitemap(self):
        for _, x in self.links.items():
            if x.source == "xml":
                return True
        return False


def root_page_to_store(rp: RootPage, key):
    links = [asdict(rp.links[x]) for x in rp.links]
    return dict(fullurl=rp.url,
                key=key,
                social=rp.social,
                links=links,
                html=rp.html
                )


@dataclass
class RootSave:
    fullurl: str
    url: str
    siteid: str
    bucket: DataBucket
    label: SiteLabel
    lang: str
    country: int

    def get(self):
        r = self.bucket.read(key=self.siteid)
        return r.json()

    def delete(self, session):
        SiteManager.delete_root(session, self.siteid)
        r = self.bucket.delete(key=self.siteid)
        return r.json()


@dataclass
class AIORootSave:
    fullurl: str
    url: str
    siteid: str
    bucket: AIODataBucket
    label: SiteLabel
    lang: str
    country: int

    async def get(self):
        r = await self.bucket.read(key=self.siteid)
        return r.json()

    def delete(self, session):
        SiteManager.delete_root(session, self.siteid)
        r = self.bucket.delete(key=self.siteid)
        return r.json()


def _get_site_stmt(siteid=None, url=None):
    stmt = select(SiteModel)\
        .options(selectinload(SiteModel.label))\
        .options(selectinload(SiteModel.bucket))
    if siteid:
        stmt = stmt.where(SiteModel.siteid == siteid)
    elif url:
        _url = URL.from_str(url)
        _key = Hasher.xxhash64(_url.url).hexdigest
        stmt = stmt.where(SiteModel.siteid == _key)
    elif id:
        stmt = stmt.where(SiteModel.id == id)
    else:
        raise AttributeError("id, siteid or url param should be provided")

    return stmt


def _get_country_code(url2, country_code: Union[str, None]) -> Union[int, None]:
    country = None
    try:
        c = countries.get(country_code)
        country = int(c.numeric)
    except KeyError:
        country = None
    except AttributeError:
        country = None
    if not country:
        c = get_country_from_tld(url2.tld)
        if c:
            country = int(c.numeric)
    return country


class AIOSiteManager:

    @staticmethod
    async def get_root(session, id=None, siteid=None, url=None) -> Union[AIORootSave, None]:

        stmt = _get_site_stmt(siteid, url)

        result = await session.execute(stmt)
        row = result.scalar()
        if row:
            lbl = SiteLabel(row.label.id, row.label.name)
            bucket = AIODataBucket(row.bucket.id,
                                   datastore=row.bucket.datastore,
                                   namespace=row.bucket.namespace,
                                   )
            fullurl = rebuild_url_from_model(row)
            return AIORootSave(
                fullurl=fullurl,
                url=row.urlnorm,
                siteid=row.siteid,
                label=lbl,
                bucket=bucket,
                country=row.country,
                lang=row.lang,
            )

        return None

    @staticmethod
    async def list_(session, label_name=None, country=None, lang=None):

        stmt = select(SiteModel).options(
            selectinload(SiteModel.label)).options(
            selectinload(SiteModel.bucket))
        if country:
            stmt = stmt.where(SiteModel.country == country)
        if lang:
            stmt = stmt.where(SiteModel.lang == lang)
        if label_name:
            stmt = stmt.join(SiteModel.label).where(
                SiteLabelModel.name == label_name)

        results = await session.execute(stmt)
        rows = results.scalars().all()
        return [r.to_dict() for r in rows]

    @staticmethod
    def url2docid(url):
        _url = URL.from_str(url)  # urlnorm
        _key = Hasher.xxhash64(_url.url).hexdigest
        return _key

    @staticmethod
    async def list_labels(session, name=None, find=None) -> List[Dict[str, Any]]:
        """
        This will list all the sites types register in the database.
        if name is provided then will try to retrieve the exact match.
        if find is provided then will use a like sql statement

        :param name: exact name
        :param find: word for a like search
        """
        stmt = select(SiteLabelModel)
        if find:
            stmt = stmt.filter(SiteLabelModel.name.like(find))
        elif name:
            stmt = stmt.filter(SiteLabelModel.name == name)
        results = await session.execute(stmt)
        rows = results.scalars()

        return [r.to_dict() for r in rows]


class SiteManager:

    def __init__(self):
        pass

    @staticmethod
    def list_(session, label_name=None, country=None, lang=None):

        stmt = select(SiteModel)
        if country:
            stmt = stmt.where(SiteModel.country == country)
        if lang:
            stmt = stmt.where(SiteModel.lang == lang)
        if label_name:
            stmt = stmt.join(SiteModel.label).where(
                SiteLabelModel.name == label_name)

        rows = session.execute(stmt).scalars().all()
        return [r.to_dict() for r in rows]

    @staticmethod
    def create_label(session, name) -> SiteLabel:
        SiteLabel.create(session, name=name)
        session.flush()
        sl = SiteLabel.from_db(session, name=name)
        return sl

    @staticmethod
    def list_labels(session, name=None, find=None) -> List[SiteLabel]:
        """
        This will list all the sites types register in the database.
        if name is provided then will try to retrieve the exact match.
        if find is provided then will use a like sql statement

        :param name: exact name
        :param find: word for a like search
        """
        stmt = select(SiteLabelModel)
        if find:
            stmt = stmt.filter(SiteLabelModel.name.like(find))
        elif name:
            stmt = stmt.filter(SiteLabelModel.name == name)
        result = session.execute(stmt).scalars()

        return [SiteLabel(id=r.id, name=r.name) for r in result]

    @staticmethod
    def get_label(session, id):
        stmt = select.where(SiteLabelModel.id == id)
        r = session.execute(stmt).first().scalar()

        return SiteLabel(id=r.id, name=r.name)

    @staticmethod
    def get_root(session, id=None, siteid=None, url=None) -> Union[RootSave, None]:

        if siteid:
            stmt = select(SiteModel).where(SiteModel.siteid == siteid)
        elif url:
            _url = URL.from_str(url)
            _key = Hasher.xxhash64(_url.url).hexdigest
            stmt = select(SiteModel).where(SiteModel.siteid == _key)
        elif id:
            stmt = select(SiteModel).where(SiteModel.id == id)
        else:
            raise AttributeError("id, siteid or url param should be provided")

        row = session.execute(stmt).scalar()
        if row:
            lbl = SiteLabel(row.label.id, row.label.name)
            bucket = DataBucket(row.bucket.id,
                                datastore=row.bucket.datastore,
                                namespace=row.bucket.namespace,
                                )

            fullurl = rebuild_url_from_model(row)
            return RootSave(
                fullurl=fullurl,
                url=row.urlnorm,
                siteid=row.siteid,
                label=lbl,
                bucket=bucket,
                lang=row.lang,
                country=row.country
            )

    @staticmethod
    def delete_root(session, siteid):
        # https://docs.sqlalchemy.org/en/14/tutorial/data_update.html
        stmt = delete(SiteModel.__table__).where(
            SiteModel.__table__.c.siteid == siteid)
        session.execute(stmt)

    @staticmethod
    def get_or_create_bucket(session, ds, ns) -> DataBucket:
        bucket = find_ds(session, CrawlerBucketModel,  ds, ns)
        if not bucket:
            bucket = create_bucket(session, CrawlerBucketModel, ds, ns)

        return bucket

    @classmethod
    def save_root(cls, session,
                  rp: RootPage,
                  ds,
                  ns,
                  label,
                  country_code: Union[str, None]) -> RootSave:

        bucket = cls.get_or_create_bucket(session, ds, ns)
        lbl = cls.create_label(session, label)

        _rss = None

        urlkey = url2docid(rp.url)
        _url = urlkey.url
        _key = urlkey.key
        url2 = parse_url2(rp.url)
        # _url = URL.from_str(rp.url)
        # _key = Hasher.xxhash64(_url.url).hexdigest
        data = root_page_to_store(rp, _key)
        r = bucket.write(_key, data, mode="w", replace=True)
        if r.status > 201:
            raise AssertionError(f"{rp.url} failed to write into datastore")

        rss_links = None
        if rp.has_rss():
            _rss = find_rss_links(rp.url)
            rss_links = [x.url for x in _rss]

        country = _get_country_code(url2, country_code)

        stmt = insert(SiteModel.__table__).values(
            siteid=_key,
            urlnorm=_url.url,
            basename=url2.domain_base,
            secure=_url.secure,
            www=_url.www,
            socials=list(rp.social),
            feedurls=rss_links,
            country=country,
            lang=rp.web.html_lang,
            bucket_id=bucket.id,
            label_id=lbl.id,

        )
        # stmt = stmt.on_conflict_do_nothing()
        stmt = stmt.on_conflict_do_update(
            # constraint="crawlers_page_bucket_id_fkey",
            index_elements=["siteid"],
            set_=dict(bucket_id=bucket.id,
                      country=country,
                      lang=rp.web.html_lang,
                      label_id=lbl.id, updated_at=datetime.utcnow())
        )
        session.execute(stmt)
        return RootSave(fullurl=_url.fullurl,
                        url=_url.url,
                        siteid=_key,
                        label=lbl,
                        bucket=bucket,
                        lang=rp.web.html_lang,
                        country=country,
                        )

    @staticmethod
    def url2docid(url):
        _url = URL.from_str(url)  # urlnorm
        _key = Hasher.xxhash64(_url.url).hexdigest
        return _key
