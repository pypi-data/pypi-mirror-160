import asyncio
import json
from dataclasses import dataclass
from typing import Dict, List, Optional

import aiohttp
import pandas as pd
import pyarrow as pa
import pyarrow.plasma as plasma
from dataproc.clients import plasma_lib
from dataproc.conf import Config
from dataproc.crawlers.page import CrawlPageTask
from dataproc.crawlers.parsers.page import Page, page_ml3
from dataproc.crawlers.parsers.url import URL
from dataproc.utils import flatten_list
from dataproc.words.utils import locale
from dataproc.zio.broker import Broker
from dataproc.zio.workers import LocalActorModel
from toolz import partition_all


@dataclass
class CrawlerConfig:
    ns: str
    ds: str
    crawler_service: str
    locale: Optional[str] = None
    user_agent: str = Config.AGENT
    store: bool = False
    strategy: str = "direct"
    http_timeout: int = 30
    plasma_dir: str = Config.PLASMA_DIR
    workers: int = 1
    chunk_size: int = 100


class BatchCrawler:

    def __init__(self, options: CrawlerConfig):
        # self._opts: CrawlPageTask = options
        self.plasma_dir: str = options.plasma_dir
        self._store = options.store
        self._locale = options.locale
        self._strategy = options.strategy
        self._ns = options.ns
        self._ds = options.ds
        self._timeout = aiohttp.ClientTimeout(total=options.http_timeout)
        self.schema = pa.schema({
            "fullurl": pa.string(),
            "url": pa.string(),
            "docid": pa.string(),
            "html": pa.string()
        })
        self.crawler = options.crawler_service

    def create_request(self, url) -> Dict[str, str]:
        req = {
            "url": url,
            "store": self._store,
            "locale": self._locale,
            # "article_data": True,
            "strategy": self._strategy,
            "namespace": self._ns,
            "datastore": self._ds
        }
        return req

    def _to_arrow_table(self, data):

        valid = []
        for ix in range(len(data) - 1):
            if isinstance(data[ix], dict) and data[ix].get("fullurl"):
                valid.append(data[ix])
                # invalid_ix.append(ix)

        df_data = pd.DataFrame(valid)
        table = pa.RecordBatch.from_pandas(df_data, schema=self.schema)
        return table

    async def fetch_one(self, url, session=None):
        req = self.create_request(url)
        async with session.post(self.crawler, json=req) as response:
            data = await response.json()

        return dict(
            fullurl=data["url"]["fullurl"],
            url=data["url"]["url"],
            docid=data["docid"],
            html=data["page"]["html"]
            # text=data["page"]["web"]["text"],
            # article_data=data["article_data"],
            # text=text,
            # title=data["page"]["web"]["title"],
            # h1=data["page"]["web"]["content"]["h1"][0]
            # date=p.page.get_date(),
        )

    async def fetch(self, urls: List[str]):

        plasma_client = plasma.connect(self.plasma_dir)
        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            results = await asyncio.gather(
                *[self.fetch_one(url, session) for url in urls], return_exceptions=True
            )
        #page_sender = Pub("listen-page")
        #page_getter = Sub("rsp-page")
        # page_sender.put(results)
        #final = page_getter.get()
        try:
            rsp = self._to_arrow_table(results)
            id_ = plasma_client.put(rsp)
            return id_
        except KeyError:
            raise TypeError("No results from the crawler. Is it running?")

    async def fetch2(self, urls: List[str]):
        """
        instead of put the data in a plasma store, it will returns the data
        """

        async with aiohttp.ClientSession(timeout=self._timeout) as session:
            results = await asyncio.gather(
                *[self.fetch_one(url, session) for url in urls], return_exceptions=True
            )
        try:
            rsp = self._to_arrow_table(results)
            return rsp
        except KeyError:
            raise TypeError("No results from the crawler. Is it running?")


class BatchPageActor(LocalActorModel):

    def init_shared_state(self, *args, **kwargs):
        from dataproc.words.ml_models import WordActor, create_word_actor
        conf: CrawlerConfig = kwargs["config"]
        locale_opts = locale[conf.locale]
        self.model = create_word_actor(
            Config.BASE_PATH, locale_opts, with_nlp=True, nlp_rank=True)

    def init_process_state(self, *args, **kwargs):
        self.loop = asyncio.get_event_loop()
        # self.plasma_client = plasma_lib.init()
        self.crawler = BatchCrawler(kwargs["config"])

    def exit_process_state(self):
        # self.loop.close()
        # self.plasma_client.close()
        pass

    def execute(self, model, msg: bytes):

        # data = json.loads(msg)
        urls = json.loads(msg)

        # table = client.get(id_)

        table = self.loop.run_until_complete(self.crawler.fetch2(urls))
        dft = table.to_pandas()
        pages = []
        for x in dft.index:
            p = self.apply_ml(model, dft.iloc[x].to_dict())
            if p:
                pages.append(p)
            else:
                print("Failed: ", dft.iloc[x].fullurl)

        # oid = self.plasma_client.put()

        return pages

    @staticmethod
    def apply_ml(words_actor, data):
        docid = data["docid"]
        fu = data["fullurl"]
        try:
            page = Page.from_html_txt(fu, data["html"])
            url = URL.from_str(fu)

            rsp = page_ml3(words_actor, page)
            rsp["docid"] = docid
            rsp["fullurl"] = fu
            rsp["url"] = url.url

            return rsp
        except:
            return None


async def _submit_wrapper(actor, chunks):
    futures = [actor.submit(json.dumps(c).encode()) for c in chunks]
    results_chunk = await asyncio.gather(*futures)

    return results_chunk


def batch_crawl_pages(urls, conf: CrawlerConfig):
    bulks = list(partition_all(conf.chunk_size, urls))
    tasks = list(partition_all(conf.workers, bulks))
    broker = Broker()
    broker.mp_start()
    pa = BatchPageActor(num_cpus=conf.workers)
    proc = pa.mp_start(config=conf)

    pages = []
    loop = asyncio.get_event_loop()
    for ix, chunks in enumerate(tasks):
        #futures = [pa.submit(json.dumps(c).encode()) for c in chunks]
        # results_chunk = await asyncio.gather(*futures)
        results_chunk = loop.run_until_complete(_submit_wrapper(pa, chunks))

        pages.extend(results_chunk)
        print(f"{ix} iteration of {len(tasks)} ended")

    pa.close()
    broker.close()
    proc.join()
    return flatten_list(pages)




def to_pandas(pages, text_columns=["text", "title", "article_data", "desc"]):
    news = pd.DataFrame(pages)
    for c in text_columns:
        news[c] = news[c].astype("string[pyarrow]")
    return news
