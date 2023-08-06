from dataclasses import dataclass
from typing import Dict

import aiohttp
import requests
import ujson
from dataproc.conf import Config

_HEADERS = {
    "User-Agent": Config.AGENT
}


class HTTPError(Exception):
    """Base class for other exceptions"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


@dataclass
class Response:
    url: str
    content: bytes
    headers: Dict[str, str]
    status: int

    def json(self):
        return ujson.loads(self.text)

    @property
    def text(self):
        try:
            return self.content.decode("utf-8")
        except UnicodeDecodeError:
            return self.content.decode("latin-1")


class Fetch:
    """ Custom HTTP fetcher """

    def __init__(self, agent=Config.AGENT):
        self.agent = agent

    def _set_headers(self, headers):
        if not headers.get("User-Agent"):
            headers["User-Agent"] = self.agent
        # return headers

    def get(self, *args, **kwargs):
        try:
            self._set_headers(kwargs.get("headers", {}))
            r = requests.get(args[0], *args[1:], **kwargs)
            _headers = dict(r.headers.items())
            resp = Response(content=r.content,
                            headers=_headers,
                            url=r.url,
                            status=r.status_code)

        except requests.exceptions.RequestException as e:
            raise HTTPError("Requests error for url %s" % args[0]) from e

        return resp

    def post(self, *args, **kwargs):
        try:
            self._set_headers(kwargs.get("headers", {}))
            r = requests.post(args[0], *args[1:], **kwargs)
            _headers = dict(r.headers.items())
            resp = Response(content=r.content,
                            url=r.url,
                            headers=_headers,
                            status=r.status_code)

        except requests.exceptions.RequestException as e:
            raise HTTPError("Requests error for url %s" % args[0]) from e

        return resp

    def put(self, *args, **kwargs):
        try:
            self._set_headers(kwargs.get("headers", {}))
            r = requests.put(args[0], *args[1:], **kwargs)
            _headers = dict(r.headers.items())
            resp = Response(content=r.content,
                            url=r.url,
                            headers=_headers,
                            status=r.status_code)

        except requests.exceptions.RequestException as e:
            raise HTTPError("Requests error for url %s" % args[0]) from e

        return resp

    def delete(self, *args, **kwargs):
        try:
            self._set_headers(kwargs.get("headers", {}))
            r = requests.delete(args[0], *args[1:], **kwargs)
            _headers = dict(r.headers.items())
            resp = Response(content=r.content,
                            url=r.url,
                            headers=_headers,
                            status=r.status_code)

        except requests.exceptions.RequestException as e:
            raise HTTPError("Requests error for url %s" % args[0]) from e

        return resp


class AIOFetch:

    def __init__(self, timeout_total=30, agent=None):
        self.timeout = aiohttp.client.ClientTimeout(total=timeout_total)
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        if not agent:
            self._agent = _HEADERS["User-Agent"]
            self.headers = _HEADERS
        else:
            self._agent = agent
            self.headers = {"User-Agent": agent}

    async def post(self, url, json=None, headers=None) -> Response:
        if not headers:
            headers = self.headers
        async with self.session.post(url, json=json, headers=headers) as response:
            content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def post_ctx(self, session, url, json=None, headers=None) -> Response:
        if not headers:
            headers = self.headers
        async with session.post(url, json=json, headers=headers) as response:
            content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def get(self, url, headers=None) -> Response:
        if not headers:
            headers = self.headers
        async with self.session.get(url, headers=headers) as response:
            content = await response.read()

        return Response(url=response.url,
                        content=content,
                        status=response.status,
                        headers=dict(response.headers))

    async def close(self):
        await self.session.close()


def make_agent_headers(agent=Config.AGENT):
    return {"User-Agent": agent}


def http_get(url, timeout_total=30, headers=_HEADERS) -> Response:
    """ Simple http get crawler """
    r = requests.get(url, timeout=timeout_total, headers=headers)
    _headers = dict(r.headers.items())
    resp = Response(content=r.content,
                    headers=_headers,
                    url=r.url,
                    status=r.status_code)

    return resp


async def http_get_async(url, timeout_total=30, headers=_HEADERS) -> Response:
    """ Simple http get crawler """
    timeout = aiohttp.client.ClientTimeout(total=timeout_total)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers) as response:
            content = await response.read()
            return Response(url=response.url,
                            content=content,
                            status=response.status,
                            headers=dict(response.headers))


async def http_post_async(url, json=None,
                          timeout_total=30,
                          headers=_HEADERS) -> Response:
    """ Simple http get crawler """
    timeout = aiohttp.client.ClientTimeout(total=timeout_total)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=json, headers=headers) as response:
            content = await response.read()
            return Response(url=response.url,
                            content=content,
                            status=response.status,
                            headers=dict(response.headers))
