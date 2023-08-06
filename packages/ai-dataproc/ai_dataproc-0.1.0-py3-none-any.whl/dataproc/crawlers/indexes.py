import asyncio
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Union
from urllib.parse import urlparse

import dateutil.parser
import redis
from asonic import Client
from asonic.enums import Channel
from dataproc.utils import today_string
from dataproc.words.parsers import DocParser

zk_dt_content = "f:dt:content"
k_entities_country = "f:entities:{}"
k_entities = "f:entities"
k_sections = "f:sections"
k_authors = "f:authors"
k_publishers = "f:publishers"
k_country = "f:c:{}"
# k_month=f"f:dt:{today_string(format_="month")}"
k_month = "f:dt:{}"

k_publisher = "f:p:{}"
k_author = "f:a:{}"
k_entity = "f:e:{}"

k_section = "f:s:{}"
k_label = "f:lb:{}"


@dataclass
class PageIXData:
    key: str
    fullurl: str
    country: str
    publisher: str
    authors: List[str]
    entities: List[str]
    section: str
    created_at: int
    year_month: str


class PageIndexer:

    def __init__(self, redis_client=None, word_parser=None):
        self.word_parser = word_parser or DocParser("any", strip_accents=True)
        self.redis = redis_client or redis.StrictRedis(decode_responses=True)

    @staticmethod
    def url_base(url: str) -> str:
        u = urlparse(url)
        _base = u.netloc.split("www.")
        # print(_base)
        if len(_base) == 2:
            final = _base[1]
        else:
            final = _base[0]

            # final = _base[0].split(".")[0]
        return final

    @staticmethod
    def get_authors_norm(parser, authors):
        _authors = []
        if isinstance(authors, dict):
            # print([authors.get("name")])
            a = authors.get("name")
            if a:
                # parsed = news_actor.words.doc_parser(a)
                _authors.append(a)
        elif isinstance(authors, list):
            for author in authors:
                if isinstance(author, dict):
                    a = author.get("name")
                    if a:
                        _authors.append(a)
                else:
                    parsed = parser.fit_transform(author)
                    _authors.append(".".join(parsed))

        if not _authors:
            return None
        return _authors

    def pageix_from_df_row(self, row) -> PageIXData:
        key = row.docid
        publisher = self.url_base(row.fullurl)
        authors_norm = self.get_authors_norm(self.word_parser, row.authors)
        entities = list(row.tags_augmented)
        section = row.section
        day_month = today_string(format_="month")

        try:
            dt_score = round(dateutil.parser.isoparse(
                row.content_date).timestamp())
        except TypeError:
            dt_score = round(datetime.utcnow().timestamp())

        return PageIXData(
            key=key,
            fullurl=row.fullurl,
            country=row.country,
            publisher=publisher,
            authors=authors_norm,
            entities=entities,
            section=section,
            created_at=dt_score,
            year_month=day_month
        )

    def register(self, page: PageIXData, label: str):
        """
        "f:entities.ar" -> "brasileirao", "lousteau"
        "f:entities" -> "brasileirao", "Lousteau", "Trump"
        "f:sections -> politics, economy, ...
        "f:authors" ->
        "f:publishers" ->
        """

        """
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
        pipe.sadd(k_country.format(page.country), page.key)

        # publisher
        pipe.sadd(k_publisher.format(page.publisher), page.key)
        pipe.sadd(k_publishers, page.publisher)

        # authors
        if page.authors:
            for a in page.authors:
                pipe.sadd(k_authors, a)
                pipe.sadd(k_author.format(a), page.key)

        # entities
        if page.entities:
            for ent in page.entities:
                ent_arr = self.word_parser.fit_transform(ent)
                ent_ = ".".join(ent_arr)
                if ent_:
                    for sub_ent in ent_arr:
                        pipe.sadd(k_entity.format(sub_ent), page.key)

                    pipe.sadd(k_entities, ent_)

        # section
        pipe.sadd(k_section.format(page.section), page.key)

        # time index
        pipe.zadd(zk_dt_content, {page.key: page.created_at})
        pipe.sadd(k_month.format(page.year_month), page.key)

        # label ix
        pipe.sadd(k_label.format(label), page.key)
        pipe.execute()


class AIOSearch():

    _REGEX_W = re.compile("[\W_]+")

    def __init__(self, host="127.0.0.1", port=1491,
                 max_connections=100, password="SecretPassword"):

        self._host = host
        self._port = port
        self._max_connections = max_connections
        self._pass = password
        self.c = None

    def _clean_txt(self, txt):
        return self._REGEX_W.sub(" ", txt)

    def _get_client(self):
        return Client(host=self._host, port=self._port,
                      password=self._pass, max_connections=self._max_connections)

    async def init_ingest(self):
        self.c = self._get_client()
        await self.c.channel(Channel.INGEST)

    async def init_search(self):
        self.c = self._get_client()
        await self.c.channel(Channel.SEARCH)

    async def query(self, txt, bucket, namespace="default", limit=100):
        return await self.c.query(bucket, namespace, self._clean_txt(txt), limit=limit)

    async def put(self, key: str, data: str, bucket, namespace="default"):
        await self.c.push(bucket, namespace, key, self._clean_txt(data))

    async def put_batch(self, data: List[Tuple[str, str]], bucket: str, namespace="default", ):
        # await self.c.channel(Channel.INGEST)
        fails = []
        for txt in data:
            try:
                cleaned = self._clean_txt(txt[1])
                if cleaned:
                    await self.c.push(bucket, namespace, txt[0], cleaned)
            except ConnectionResetError:
                print("sleeping...")
                await asyncio.sleep(2)
                await self.c.push(bucket, namespace, txt[0], cleaned)
            except TypeError:
                fails.append(txt[0])
            except Exception as e:
                print(e)
        return fails

    async def close(self):
        await self.c.quit()
