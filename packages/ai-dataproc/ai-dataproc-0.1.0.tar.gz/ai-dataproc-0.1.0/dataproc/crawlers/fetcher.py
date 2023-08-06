# from dataclasses.http_client import http_post
from dataclasses import dataclass
from typing import Dict

import aiohttp
import requests
import ujson
from dataproc.conf import Config


@dataclass
class FetchRequest:
    url: str
    strategy: str = Config.DEFAULT_STRATEGY
    ts: int = 60  # in secs
    screenshot: bool = False
    autoscroll: bool = False
    user_agent: str = Config.AGENT


@dataclass
class FetchResponse:
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
        except AttributeError:
            return self.content


class HTTPError(Exception):
    """Base class for other exceptions"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Fetch:

    def __init__(self, chrome=Config.CHROME,
                 timeout=180,
                 wrangler=Config.WRANGLER,
                 wrangler_tkn=Config.WRANGLER_TOKEN):
        self.chrome_service = chrome
        self.wrangler = wrangler
        self.wrangler_tkn = wrangler_tkn
        self.axios = f"{self.chrome_service}/v3/axios"
        self.chrome = f"{self.chrome_service}/v3/chrome"
        self.ts = timeout

    @staticmethod
    def from_url(url: str) -> FetchRequest:
        return FetchRequest(url)

    def get(self, req: FetchRequest) -> FetchResponse:
        try:
            rsp = self._get_wrapper(req)
            return rsp
        except requests.exceptions.RequestException as e:
            raise HTTPError("Requests error for url %s" % req.url) from e

    def _get_wrapper(self, req: FetchRequest) -> FetchResponse:
        """ Fetch a page using some strategy. The options are:
        'axios': will go though a digitalocean service but using common request library. 
        'chrome': it will use a chrome instance, simulating a browser.
        'direct': using python
        'wrangler': using cloudflare

        """
        if req.strategy == "axios":
            r = requests.post(self.axios,
                              timeout=self.ts,
                              json=dict(url=req.url,
                                        ts=req.ts,
                                        userAgent=req.user_agent
                                        ))

            _headers = dict(r.headers.items())
            data = ujson.loads(r.content)

            return FetchResponse(
                url=data["fullurl"],
                content=data["content"],
                headers=data["headers"],
                status=data["status"]
            )
        elif req.strategy == "chrome":
            r = requests.post(self.chrome,
                              json=dict(url=req.url,
                                        ts=req.ts,
                                        userAgent=req.user_agent,
                                        screenshot=req.screenshot,
                                        autoscroll=req.autoscroll
                                        ))

            _headers = dict(r.headers.items())
            data = ujson.loads(r.content)

            return FetchResponse(
                url=data["fullurl"],
                content=data["content"],
                headers=data["headers"],
                status=data["status"]
            )

        elif req.strategy == "direct":

            r = requests.get(req.url, timeout=req.ts,
                             headers={"User-Agent": req.user_agent})
            _headers = dict(r.headers.items())

            return FetchResponse(
                url=r.url,
                content=r.content,
                headers=_headers,
                status=r.status_code
            )
        elif req.strategy == "wrangler":

            h = {"Authorization": f"Bearer {self.wrangler_tkn}"}
            r = requests.post(self.wrangler, json={"url": req.url},
                              timeout=req.ts,
                              headers=h
                              )
            data = ujson.loads(r.content)
            return FetchResponse(content=data["html"],
                                 headers=data["headers"],
                                 url=req.url,
                                 status=data["status"])
        else:
            raise TypeError("wrong strategy")


class AIOFetch:

    def __init__(self, chrome=Config.CHROME,
                 wrangler=Config.WRANGLER,
                 wrangler_tkn=Config.WRANGLER_TOKEN):
        self.chrome_service = chrome
        self.wrangler = wrangler
        self.wrangler_tkn = wrangler_tkn
        self.axios = f"{self.chrome_service}/v3/axios"
        self.chrome = f"{self.chrome_service}/v3/chrome"
        self.ts = 60

    @staticmethod
    def from_url(url: str) -> FetchRequest:
        return FetchRequest(url)

    @staticmethod
    async def http_post(url, json=None,
                        timeout=30,
                        headers={}) -> FetchResponse:
        """ Simple http get crawler """
        timeout = aiohttp.client.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=json, headers=headers) as response:
                content = await response.read()
                return FetchResponse(url=str(response.url),
                                     content=content,
                                     status=response.status,
                                     headers=dict(response.headers))

    @staticmethod
    async def http_get(url, timeout=30, headers={}) -> FetchResponse:
        """ Simple http get crawler """
        timeout = aiohttp.client.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers=headers) as response:
                content = await response.read()
                return FetchResponse(url=str(response.url),
                                     content=content,
                                     status=response.status,
                                     headers=dict(response.headers))

    async def get(self, req: FetchRequest) -> FetchResponse:
        """ Fetch a page using some strategy. The options are:
        'axios': will go though a digitalocean service but using common request library. 
        'chrome': it will use a chrome instance, simulating a browser.
        'direct': using python
        'wrangler': using cloudflare

        """
        if req.strategy == "axios":
            r = await self.http_post(self.axios,
                                     timeout=self.ts,
                                     json=dict(url=req.url,
                                               ts=req.ts,
                                               userAgent=req.user_agent
                                               ))

            data = ujson.loads(r.content)

            return FetchResponse(
                url=data["fullurl"],
                content=data["content"],
                headers=data["headers"],
                status=data["status"]
            )
        elif req.strategy == "chrome":
            r = await self.http_post(self.chrome,
                                     timeout=self.ts + 120,
                                     json=dict(url=req.url,
                                               ts=req.ts,
                                               userAgent=req.user_agent,
                                               screenshot=req.screenshot,
                                               autoscroll=req.autoscroll
                                               ))

            data = ujson.loads(r.content)

            return FetchResponse(
                url=data["fullurl"],
                content=data["content"],
                headers=data["headers"],
                status=data["status"]
            )

        elif req.strategy == "direct":
            r = await self.http_get(req.url, timeout=req.ts,
                                    headers={"User-Agent": req.user_agent})

            return FetchResponse(
                url=r.url,
                content=r.content,
                headers=r.headers,
                status=r.status
            )

        elif req.strategy == "wrangler":

            h = {"Authorization": f"Bearer {self.wrangler_tkn}"}
            r = await self.http_post(self.wrangler, json={"url": req.url},
                                     timeout=req.ts,
                                     headers=h
                                     )
            data = ujson.loads(r.content)
            return FetchResponse(content=data["html"],
                                 headers=data["headers"],
                                 url=req.url,
                                 status=data["status"])
        else:
            raise TypeError("wrong strategy")
