from dataclasses import dataclass
from typing import Any, Dict, List, Union

import aiohttp
from dataproc.crawlers.http_client import (Fetch, Response, http_post_async,
                                           make_agent_headers)
from dataproc.crawlers.models import CrawlerBucketModel
from dataproc.datastore.core import AIODataBucket, DataBucket
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

_fetch = Fetch()


class AIOBucketManager:

    @classmethod
    async def list_ns(cls, session) -> List[Dict[str, Any]]:
        stmt = select(CrawlerBucketModel)
        result = await session.execute(stmt)
        rows = result.scalars()
        # return [AIODataBucket(
        #    id=r.id, namespace=r.namespace, datastore=r.datastore)
        #    for r in rows]
        return [r.to_dict() for r in rows]


class BucketManager:

    def __init__(self, url):
        self.url = url

    @staticmethod
    def list_ns_db(session) -> List[DataBucket]:
        stmt = select(CrawlerBucketModel)
        result = session.execute(stmt).scalars()
        return [DataBucket(id=r.id, namespace=r.namespace, datastore=r.datastore)
                for r in result]

    @staticmethod
    def find_ds(session, ds, ns) -> DataBucket:
        """
        Find a datastore to return a DataBucket object
        wich allows to write and read data from the store
        """
        stmt = select(CrawlerBucketModel)\
            .filter(CrawlerBucketModel.datastore == ds)\
            .filter(CrawlerBucketModel.namespace == ns)
        ds: CrawlerBucketModel = session.execute(stmt).scalar()

        return DataBucket(id=ds.id,
                          namespace=ds.namespace,
                          datastore=ds.datastore)

    def get_bucket(self, session, ns) -> DataBucket:
        bucket = self.find_ds(session, self.url, ns)
        return bucket

    def create_ns(self, session, ns: str) -> DataBucket:
        """
        :param ns: namepsace name
        :param ds: datastaore url server
        """
        # url = url_norm(f"{self.url}/v1/namespace")
        r = _fetch.post(f"{self.url}/v1/namespace", json={"name": ns})
        # dt = Datastore(namespace=ns, datastore=self.url)
        if r.status == 200 or r.status == 201:
            stmt = insert(CrawlerBucketModel.__table__).values(namespace=ns,
                                                               datastore=self.url)
            stmt = stmt.on_conflict_do_nothing()
            session.execute(stmt)
            session.commit()
            bucket = self.get_bucket(session, ns)
            return bucket
        else:
            raise TypeError("HTTP request error")

    def create_ns_remote(self, ns):
        r = _fetch.post(f"{self.url}/v1/namespace", json={"name": ns})
        return r

    def list_remote_ns(self):
        r = _fetch.get(f"{self.url}/v1/namespace")
        return r.json()

    def list_remote_data(self, ns, ids_only=True):
        if ids_only:
            r = _fetch.get(f"{self.url}/v1/data/{ns}/_list")
        else:
            r = _fetch.get(f"{self.url}/v1/data/{ns}")
        return r.json()
