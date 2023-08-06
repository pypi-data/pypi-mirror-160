import asyncio
import json
import time
from typing import List

import cloudpickle
import pandas as pd
from dataproc.clients import plasma_lib
from dataproc.conf import Config
from dataproc.crawlers import aio_fetch
from dataproc.crawlers.managers.page import Page
from dataproc.crawlers.root import CrawlRootTask, crawl_root2
from dataproc.crawlers.utils import rebuild_url, url2docid
from dataproc.utils import set_logger
from dataproc.zio.cluster import LocalCluster


class BatchRoot:
    """ It uses the LocalCluster to scrape root sites """

    def __init__(self, lastmod=1, valid_url=2, label=None, country=None,
                 strategy=Config.DEFAULT_STRATEGY, cluster=None):
        self.cluster = cluster or LocalCluster()
        self._lastmod = lastmod
        self._valid = valid_url
        self._label = label
        self._country = country
        self._strategy = strategy
        self.logger = set_logger(f"{self.__class__}")

    def start(self):
        self.cluster.start_workers(self.scrape_site)

    def close(self):
        self.cluster.close()

    def create_root_task(self, url) -> CrawlRootTask:
        crt = CrawlRootTask(
            url=url,
            lastmod=self._lastmod,
            valid_url=self._valid,
            strategy=self._strategy,
            label=self._label,
            country=self._country,
        )
        return crt

    def scrape_site(self, data):
        jdata = json.loads(data)
        fullurl = rebuild_url(jdata)
        crt = self.create_root_task(fullurl)

        rsp = crawl_root2(crt)
        return rsp.df

    @staticmethod
    def _to_bytes(row):
        bdata = json.dumps(row).encode()
        return bdata

#    @staticmethod
#    def _wrap_response(rsp):
#        obj = cloudpickle.loads(rsp)
#
#        if isinstance(obj, Exception):
#            print(obj)
#        else:
#            return obj

    async def submit_one(self, site):
        r = await self.cluster.submit(self._to_bytes(site))
        return cloudpickle.loads(r)

    async def submit(self, sites):
        futures = [self.cluster.submit(self._to_bytes(row)) for row in sites]
        results = await asyncio.gather(*futures, return_exceptions=True)
        data_and_sites = zip(results, sites)
        df = self._merge_df(data_and_sites)

        return df

    def _merge_df(self, results):
        dataframes = []
        for r, s in results:
            obj = cloudpickle.loads(r)
            if not isinstance(obj, Exception):
                dataframes.append(obj)
            else:
                self.logger.warning("Site %s failed", s.get("urlnorm"))

        df = pd.concat(dataframes)
        return df


class BatchPageHTML:

    def __init__(self, cluster=None, jobs=None):
        self.cluster = cluster or LocalCluster(num_cpus=jobs)
        self.logger = set_logger(f"{self.__class__}")

    def start(self):
        self.cluster.start_workers(self.scrape_chunk)

    def close(self):
        self.cluster.close()

    @staticmethod
    def _to_bytes(data):
        bdata = json.dumps(data).encode()
        return bdata

    def scrape_chunk(self, chunk):
        jdata = json.loads(chunk)
        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        obj_id = loop.run_until_complete(self.proc_chunk(jdata))
        return obj_id

    @staticmethod
    async def fetch(url):
        docid = url2docid(url)
        url = docid.url
        _key = docid.docid

        req = aio_fetch.from_url(url.fullurl)
        rsp = await aio_fetch.get(req)
        html = rsp.text
        page = Page.from_html_txt(url.fullurl, html)
        return _key, page

    async def _wrapper_fetch(self, u):
        try:
            self.logger.debug("Fetching %s", u)
            docid, p = await self.fetch(u)
            return docid, p
        except Exception:
            self.logger.warning("URL %s Failed", u)

    async def proc_chunk(self, chunk):
        import pyarrow as pa

        self.logger.debug("GETTING CHUNK")
        plasma = plasma_lib.init()

        # data = []

        schema = pa.schema(
            [
                ("docid", pa.string()),
                ("url", pa.string()),
                ("title", pa.string()),
                ("base_name", pa.string()),
                ("text", pa.string()),
                ("html", pa.string()),
            ]
        )
        docs = []
        urls = []
        titles = []
        bases = []
        texts = []
        htmls = []
        start = time.time()

        futures = [self._wrapper_fetch(u) for u in chunk]

        results = await asyncio.gather(*futures)
        for r in results:
            if r:
                docs.append(r[0])
                urls.append(r[1].url)
                titles.append(r[1].web.title)
                bases.append(r[1].base_name)
                texts.append(r[1].article_data().text)
                htmls.append(r[1].html)

        table = pa.table([docs, urls, titles, bases,
                         texts, htmls], schema=schema)
        id_ = plasma.put(table)
        plasma.disconnect()

        elapsed = time.time() - start
        self.logger.debug(f"ELAPSED: {round(elapsed, 2)}")
        return id_

    async def submit(self, urls: List[str]):
        rsp = await self.cluster.submit(self._to_bytes(urls))
        return cloudpickle.loads(rsp)
