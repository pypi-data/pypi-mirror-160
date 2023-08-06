import logging
from dataclasses import dataclass
from typing import List, Optional

import feedparser
# from dataproc.crawlers.http_client import Fetch
from dataproc.crawlers import fetch
from dataproc.crawlers.fetcher import HTTPError
from dataproc.crawlers.parsers import html
from dateutil.parser import parse as dtparser

# fetch = Fetch()
logger = logging.getLogger(__name__)


@dataclass
class Entry:
    link: str
    title: Optional[str] = None
    published: Optional[str] = None
    author: Optional[str] = None

    def __hash__(self):
        return html.url_norm(self.link)


@dataclass
class RSSLink:
    """URL of the feed and the xml content of it"""
    url: str
    xmlcontent: str

    # def __eq__(self, other):

    @classmethod
    def from_url(cls, url):
        req = fetch.from_url(url)
        r = fetch.get(req)
        obj = cls(url=url, xmlcontent=r.text)
        return obj

    def parse(self) -> List[Entry]:
        feed = feedparser.parse(self.xmlcontent)
        entries = []
        for e in feed["entries"]:
            # print(e.keys())
            title = e.get("title")
            published = e.get("published")
            dt = None
            try:
                _dt = dtparser(published)
                dt = _dt.isoformat()
            except ValueError:
                pass
            except TypeError:
                pass
            try:
                _link = e["link"]
                author = e.get("author")
                _entry = Entry(link=_link, title=title,
                               author=author, published=dt)
                entries.append(_entry)
            except KeyError:
                pass

        return entries


def _find_rss_realated_links(links):
    rss_links = set()
    for l in links:
        if l.internal and "rss" in l.href or "feed" in l.href:
            rss_links.add(l.href)
    return rss_links


def find_rss_links(url) -> List[RSSLink]:
    """ Main method, it will scrap from the url provided looking for links related
    to rss feed. If it found rss links then, it will try to get the feed.
    """
    logger.debug("RSS scrapping for %s", url)
    rss: List[RSSLink] = []
    _urls = set()
    _parsed = set()
    # breakpoint()
    # print(url)
    req = fetch.from_url(url)
    r = fetch.get(req)
    w = html.parse(r.text, url)
    rss_links = _find_rss_realated_links(w.links)
    for x in rss_links:
        if x not in _parsed:
            # print(x)
            req = fetch.from_url(x)
            try:
                possible = fetch.get(req)
                _parsed.add(x)

                if possible.headers.get("Content-Type") and \
                        "xml" in possible.headers["Content-Type"]:
                    if x not in _urls:
                        _urls.add(x)
                        rss.append(RSSLink(url=x, xmlcontent=possible.text))
                else:
                    w2 = html.parse(possible.text, x)
                    rss_links2 = _find_rss_realated_links(w2.links)
                    for y in rss_links2:
                        if y not in _parsed:
                            # print(y)
                            req = fetch.from_url(y)
                            possible2 = fetch.get(req)
                            _parsed.add(y)
                            try:
                                if "xml" in possible2.headers["Content-Type"]:
                                    if y not in _urls:
                                        _urls.add(y)
                                        rss.append(
                                            RSSLink(
                                                url=y, xmlcontent=possible2.text)
                                        )
                            except KeyError:
                                pass
            except HTTPError:
                logger.warning("HTTPError  for %s", x)
    return rss


def rss_parser(link: RSSLink) -> List[Entry]:

    feed = feedparser.parse(link.xmlcontent)
    entries = []
    for e in feed["entries"]:
        # print(e.keys())
        title = e.get("title")
        published = e.get("published")
        try:
            dt = dtparser(published)
        except ValueError:
            dt = None
        except TypeError:
            dt = None
        try:
            _link = e["link"]
            author = e.get("author")
            _entry = Entry(link=_link, title=title,
                           author=author, published=published)
            entries.append(_entry)
        except KeyError:
            pass

    return entries
