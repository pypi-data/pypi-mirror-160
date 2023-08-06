import asyncio
from dataclasses import dataclass

import aiohttp
import ujson
from dataproc.http_client import (Fetch, Response, http_post_async,
                                  make_agent_headers)

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

    async def _get(self, session, id_):
        url = f"{self.datastore}/{self.namespace}/{id_}"
        async with session.get(url) as response:
            data = await response.read()
            return ujson.loads(data)

    async def batch_read(self, ids):
        async with aiohttp.ClientSession() as session:
            futures = await asyncio.gather(*[self._get(session, id_)
                                             for id_ in ids],
                                           return_exceptions=True)
        return futures

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
