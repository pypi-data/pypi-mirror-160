from dataclasses import dataclass
from typing import List, Union

import aiohttp
from dataproc.crawlers.http_client import (Fetch, Response, http_post_async,
                                           make_agent_headers)
from dataproc.crawlers.models import CrawlerBucketModel
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

# from dataproc.crawlers.parsers.html import url_norm

_fetch = Fetch()

_headers_octet = {'Content-Type': 'application/octet-stream'}


def list_remote_ns(url):
    r = _fetch.get(f"{url}/v1/namespace")
    return r.json()


def post_data(ds, ns, key, data, mode="wb"):
    """
    :param ns: namespace
    :param key: key
    :param data: data to sent
    :param mode: like open in python: wb or w or

    """
    if mode == "wb":
        res = _fetch.post(f"{ds}/{ns}/{key}",
                          data=data,
                          headers=_headers_octet)

    elif mode == "w":
        res = _fetch.post(f"{ds}/{ns}/{key}",
                          json=data,
                          )

    else:
        raise AttributeError(f"Mode {mode} is not valid")
    return res


def put_data(ds, ns, key, data, mode="wb"):
    """
    :param ns: namespace
    :param key: key
    :param data: data to sent
    :param mode: like open in python: wb or w or

    """
    if mode == "wb":
        res = _fetch.put(f"{ds}/{ns}/{key}",
                         data=data,
                         headers=_headers_octet)

    elif mode == "w":
        res = _fetch.put(f"{ds}/{ns}/{key}",
                         json=data,
                         )
    else:
        raise AttributeError(f"Mode {mode} is not valid")

    return res


@dataclass
class AIODataBucket:
    id: int
    namespace: str
    datastore: str

    async def put_data(self, key, data, mode) -> Response:

        url = f"{self.datastore}/{self.namespace}/{key}"
        if mode == "wb":
            async with aiohttp.ClientSession() as session:
                async with session.put(url,
                                       headers=_headers_octet,
                                       data=data) as response:
                    content = await response.read()

        elif mode == "w":
            async with aiohttp.ClientSession() as session:
                async with session.put(url,
                                       headers=_headers_octet,
                                       json=data) as response:
                    content = await response.read()

        else:
            raise AttributeError(f"Mode {mode} is not valid")

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def post_data(self, key, data, mode) -> Response:

        url = f"{self.datastore}/{self.namespace}/{key}"
        if mode == "wb":
            async with aiohttp.ClientSession() as session:
                async with session.post(url,
                                        headers=_headers_octet,
                                        data=data) as response:

                    content = await response.read()

        elif mode == "w":
            async with aiohttp.ClientSession() as session:
                async with session.post(url,
                                        headers=_headers_octet,
                                        json=data) as response:
                    content = await response.read()

        else:
            raise AttributeError(f"Mode {mode} is not valid")

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def write(self, key, data, mode, replace=False):
        """
        :param ns: namespace
        :param key: key
        :param data: data to sent
        :param mode: like open in python: wb or w or

        """
        if replace:
            r = await self.put_data(key, data, mode)
        else:
            r = await self.post_data(key, data, mode)

        return r

    async def read(self, key) -> Response:
        url = f"{self.datastore}/{self.namespace}/{key}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def delete(self, key) -> Response:
        url = f"{self.datastore}/{self.namespace}/{key}"

        async with aiohttp.ClientSession() as session:
            async with session.delete(url) as response:
                content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def list_remote_ns(self) -> Response:
        url = f"{self.datastore}/v1/namespace"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def list_data(self, list_=True):
        if list_:
            url = f"{self.datastore}/v1/data/{self.namespace}/_list"
        else:
            url = f"{self.datastore}/v1/data/{self.namespace}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))


async def find_ds_async(session, ds, ns) -> Union[AIODataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = select(CrawlerBucketModel)\
        .filter(CrawlerBucketModel.datastore == ds)\
        .filter(CrawlerBucketModel.namespace == ns)
    r = await session.execute(stmt)
    bucket_db: CrawlerBucketModel = r.scalar()
    if bucket_db:

        return AIODataBucket(id=bucket_db.id,
                             namespace=bucket_db.namespace,
                             datastore=bucket_db.datastore)


async def create_bucket_async(session, ds, ns) -> AIODataBucket:
    headers = make_agent_headers(agent="dataproc")
    r = await http_post_async(f"{ds}/v1/namespace",
                              json={"name": ns},
                              headers=headers)
    if r.status > 201:
        raise IndexError("Bucket Not found, or conn error")

    stmt = insert(CrawlerBucketModel.__table__).values(namespace=ns,
                                                   datastore=ds)
    stmt = stmt.on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()
    bucket = await find_ds_async(session, ds, ns)
    return bucket


@dataclass
class DataBucket:
    id: int
    namespace: str
    datastore: str

    def write(self, key, data, mode="wb", replace=False):
        """
        :param ns: namespace
        :param key: key
        :param data: data to sent
        :param mode: like open in python: wb or w or

        """
        if replace:
            r = put_data(self.datastore, self.namespace, key, data, mode)
        else:
            r = post_data(self.datastore, self.namespace, key, data, mode)

        return r

    def read(self, key):
        res = _fetch.get(f"{self.datastore}/{self.namespace}/{key}")
        return res

    def delete(self, key):
        res = _fetch.delete(f"{self.datastore}/{self.namespace}/{key}")
        return res

    def list_remote_ns(self):
        r = _fetch.get(f"{self.datastore}/v1/namespace")
        return r.json()

    def list_data(self, list_=True):
        if list_:
            r = _fetch.get(f"{self.datastore}/v1/data/{self.namespace}/_list")
        else:
            r = _fetch.get(f"{self.datastore}/v1/data/{self.namespace}")
        return r.json()


class DatastoreManager:

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

    def write(self, ns, key, data, mode="wb", replace=False):
        """
        :param ns: namespace
        :param key: key
        :param data: data to sent
        :param mode: like open in python: wb or w or

        """
        if replace:
            r = put_data(self.url, ns, key, data, mode)
        else:
            r = post_data(self.url, ns, key, data, mode)

        return r

    def read(self, ns, key):
        res = _fetch.get(f"{self.url}/{ns}/{key}")
        return res
