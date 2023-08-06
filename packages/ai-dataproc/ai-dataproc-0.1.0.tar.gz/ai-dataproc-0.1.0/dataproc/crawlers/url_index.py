from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Union

import dateutil.parser
import pandas as pd
import redis
from dataproc.conf import Config
from dataproc.crawlers.models import CrawlerBucketModel, URLModel
from dataproc.crawlers.parsers.url import parse_url2, url2docid
from dataproc.datastore.core import AIODataBucket, DataBucket
from dataproc.datastore.managers import (create_bucket, create_bucket_async,
                                         find_ds_by_ns_async, find_ds_id,
                                         find_ds_id_async)
from dataproc.utils import create_redis_client, today_string
from dataproc.words.parsers import DocParser
from hashes.generators import random_str
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import text

zk_dt_content = "u:dt:url"
k_entities_country = "u:entities:{}"
k_entities = "u:entities"
k_sections = "u:sections"
k_publishers = "u:publishers"
k_country = "u:c:{}"
k_lang = "u:lg:{}"

k_month = "u:dt:{}"
k_publisher = "u:p:{}"
k_entity = "u:e:{}"

k_section = "u:s:{}"
k_label = "u:lb:{}"

indexes = dict(
    country=k_country,
    lang=k_lang,
    month=k_month,
    publisher=k_publisher,
    entity=k_entity,
    section=k_section,
    label=k_label,
)


def get_last_ids(r: redis.Redis, hours=24, zkey=zk_dt_content):
    """
    Get last ids of URLs inserted in redis, by date.
    """
    dt_min = get_dt_min(hours)
    last_day_ids = r.zrangebyscore(zkey, dt_min, "+inf")
    return last_day_ids


def set_tmp_ids(r: redis.Redis, ids: List[str], len_=8):

    tmp_key = f"u.rand:{random_str(len_)}"
    pipe = r.pipeline()
    for id_ in ids:
        pipe.sadd(tmp_key, id_)
    pipe.execute()
    return tmp_key


def get_dt_min(hours):
    return round((datetime.utcnow() - timedelta(hours=hours)).timestamp())


def create_url_bucket(session, ds, ns) -> DataBucket:
    bucket = create_bucket(session, CrawlerBucketModel, ds, ns)
    return bucket


async def create_url_bucket_async(session, ds, ns) -> AIODataBucket:
    bucket = await create_bucket_async(session, CrawlerBucketModel, ds, ns)
    return bucket


async def find_url_bucket_async(session, ns) -> Union[AIODataBucket, None]:
    bucket = await find_ds_by_ns_async(session, CrawlerBucketModel, ns)
    return bucket


def get_url_bucket(session, id_) -> Union[DataBucket, None]:
    b = find_ds_id(session, CrawlerBucketModel, id_)
    return b


async def get_url_bucket_async(session, id_) -> Union[AIODataBucket, None]:
    b = await find_ds_id_async(session, CrawlerBucketModel, id_)
    return b


@dataclass
class URLIXData:
    # pylint: disable=too-many-instance-attributes
    key: str
    fullurl: str
    text: str
    label: str
    label_id: int
    publisher: str
    entities: List[str]
    section: str
    created_at: int
    lang: str
    year_month: str
    text_classify: Optional[str] = None
    country: Optional[str] = None


@dataclass
class URLSQL:
    id: int
    docid: str
    site: str
    fullurl: str
    bucket_id: int
    created_at: str


def _insert_url(url: URLIXData, bucket_id):
    dt = datetime.utcfromtimestamp(url.created_at)
    stmt = insert(URLModel.__table__).values(
        docid=url.key,
        fullurl=url.fullurl,
        # text=url.text,
        # label_id=url.label_id,
        bucket_id=bucket_id,
        # lang=url.lang,
        created_at=dt,

    )
    stmt = stmt.on_conflict_do_nothing()
    return stmt


class URLIndexer:
    """ Index URL using Redis and PostgreSQL """

    def __init__(self, bucket: DataBucket, redis_client=None, word_parser=None):
        self.word_parser = word_parser or DocParser("any", strip_accents=True)
        self.redis = redis_client or create_redis_client(Config.URL_REDIS)
        self.bucket = bucket

    @staticmethod
    def from_df_row(row) -> URLIXData:
        """
        ['link', 'source', 'title', 'published', 'author', 'dt', 'siteid',
       'site_url', 'label', 'bucket_id', 'basename', 'lang', 'country', 'text',
       'link_status', 'title_len', 'text_len', 'final_text', 'final_text_len',
       'lang_pred', 'text_classify', 'section', "entities", "main_lang", "label"],
        """
        url_key = url2docid(row.link)
        key = url_key.key
        publisher = row.basename

        entities = row.entities
        section = row.section
        day_month = today_string(format_="month")
        lang = row.main_lang

        try:
            dt_score = round(dateutil.parser.isoparse(
                row["dt"]).timestamp())
        except TypeError:
            dt_score = round(datetime.utcnow().timestamp())

        return URLIXData(
            key=key,
            text=row.final_text,
            text_classify=row.text_classify,
            fullurl=url_key.url.fullurl,
            label=row.label,
            label_id=int(row.label_id),
            publisher=publisher,
            country=row.country,
            entities=entities,
            section=section,
            created_at=dt_score,
            lang=lang,
            year_month=day_month
        )

    def register(self, session, url: URLIXData):
        """ the registration is execute agains Redis, Postgres and the Raw Store """
        self.register_redis(url)
        self.save_db(session, url)
        self.bucket.write(url.key, asdict(url), mode="w")

    def save_db(self, session, url: URLIXData):
        stmt = _insert_url(url, self.bucket.id)
        session.execute(stmt)

    def register_redis(self, url: URLIXData):
        """
        "f:entities.ar" -> "brasileirao", "lousteau"
        "f:entities" -> "brasileirao", "Lousteau", "Trump"
        "f:sections -> politics, economy, ...
        "f:authors" ->
        "f:publishers" ->

        "f:content" -> (1234,docid), (1222,docid)
        "f:e:brasileirao" -> docid, docid          # entity [MENTION]
        "f:c:AR" -> docid, docid, docid            # country [FROM_PLACE]
        "f:s:economy" -> docid, docid              # section [WITH_TOPIC]
        "f:dt:202112" -> docid, docid, docid          # date    [CREATED_AT]
        "f:a:pagni" -> docid, docid, docid         # author  [CREATED_BY]
        "f:p:lanacion" -> docid, docid, docid      # publisher [PUBLISHED_BY]
        "f:lb:news.ar -> docid
        """

        pipe = self.redis.pipeline()

        # country
        pipe.sadd(k_country.format(url.country), url.key)

        # publisher
        pipe.sadd(k_publisher.format(url.publisher), url.key)
        pipe.sadd(k_publishers, url.publisher)

        # entities
        if url.entities:
            for ent in url.entities:
                ent_arr = self.word_parser.fit_transform(ent)
                ent_ = ".".join(ent_arr)
                if ent_:
                    for sub_ent in ent_arr:
                        pipe.sadd(k_entity.format(sub_ent), url.key)

                    pipe.sadd(k_entities, ent_)

        # section
        pipe.sadd(k_section.format(url.section), url.key)

        # lang
        pipe.sadd(k_lang.format(url.lang), url.key)

        # time index
        pipe.zadd(zk_dt_content, {url.key: url.created_at})
        pipe.sadd(k_month.format(url.year_month), url.key)

        # label ix
        pipe.sadd(k_label.format(url.label), url.key)
        pipe.execute()


class URLQuery:

    def __init__(self, redis_client=None):
        self.redis = redis_client or create_redis_client(Config.URL_REDIS)

    def _sinter(self, rules: Dict[str, List[str]], tmp_key: str):
        """ base on rules, it applies SINTER() method to filter data """

        made = set()
        keys = set()
        for k in rules.keys():
            print(k)
            for x in rules[k]:
                # print("x: ", x)
                for k2 in rules.keys():
                    if k2 != k and k2 not in made or len(rules.keys()) == 1:
                        for j in rules[k2]:
                            print(
                                f"get {indexes[k].format(x)} with {indexes[k2].format(j)}")
                            _keys = self.redis.sinter(indexes[k].format(
                                x), indexes[k2].format(j), tmp_key)
                            keys = keys.union(_keys)

                    made.add(k)
        return keys

    def get_redis(self, query: Dict[str, Any], last_hours=24) -> Set[str]:
        """ It process the query agains redis
        the query is DICT with two main values: include and exclude.

        include=dict(country=["AR", "CL"], section=["politics", "economy"]),
        exclude=dict(entity=["fmi"])

        Each key of include and exclude should match with `indexes`
        """

        last_ids = get_last_ids(self.redis, hours=last_hours)
        tmp_key = set_tmp_ids(self.redis, last_ids)

        includes = self._sinter(query.get("include"), tmp_key)
        excludes = set()
        if query.get("exclude"):
            excludes = self._sinter(query.get("exclude"), tmp_key)
        values = includes - excludes
        self.redis.delete(tmp_key)
        return values

    def get_sql(self, session, values) -> Dict[str, List[URLSQL]]:
        """ the values matched ordered by bucket """
        sql_query = self._make_sql_query(values)
        rows = session.execute(sql_query).all()
        # data = {r[3]: URLSQL(
        #     id=r[0],
        #     docid=r[1],
        #     fullurl=r[2],
        #     site=parse_url2(r[2]).domain_base,
        #     # text=r[3],
        #     bucket_id=r[3],
        #     created_at=r[4].isoformat(),
        # ) for r in rows}

        data: Dict[str, List[URLSQL]] = {}
        for r in rows:
            u = URLSQL(
                id=r[0],
                docid=r[1],
                fullurl=r[2],
                site=parse_url2(r[2]).domain_base,
                # text=r[3],
                bucket_id=r[3],
                created_at=r[4].isoformat(),
            )
            if data.get(r[3]):
                data[r[3]].append(u)
            else:
                data[r[3]] = [u]

        return data

    def get(self, session, query, last_hours=24) -> Union[Dict[str, Any], None]:
        """ get values based on a query ordered by bucket_id """
        ids = self.get_redis(query, last_hours=last_hours)
        if ids:
            data_dict = self.get_sql(session, ids)
            return data_dict
        return None
        

    @staticmethod
    def _make_query_values(values):
        """
        prepare values as in the form of:
        WHERE "Post"."userId" IN (VALUES (201486), (1825186), (998608), ... )
        """
        txt = ""
        for v in values:
            txt += f"('{v}'), "
        txt = txt[:-2]
        return txt

    @classmethod
    def _make_sql_query(cls, values):
        """
        For perfomance reasons in postgresql is recommended the use of VALUES expression
        for queries execution agains list of values.
        https://dba.stackexchange.com/questions/91247/optimizing-a-postgres-query-with-a-large-in
        """
        tbl = URLModel.__tablename__
        q = cls._make_query_values(values)
        return text(f"SELECT * FROM {tbl} WHERE {tbl}.docid IN (VALUES {q})")


async def get_url_data_async(session, data: Dict[str, List[URLSQL]]):
    response = []
    for bucket_id in data.keys():
        bucket = await get_url_bucket_async(session, bucket_id)
        rsp = await bucket.batch_read([u.docid for u in data[bucket_id]])
        response.extend(rsp)
    return response
