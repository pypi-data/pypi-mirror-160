import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

import Levenshtein as lv
# from dataproc.crawlers.http_client import HTTPError
from dataproc.crawlers.parsers.rss import find_rss_links, rss_parser
from dataproc.crawlers.parsers.sitexml import (get_sitemaps_from_url,
                                               parse_sites_xml)
from dataproc.crawlers.parsers.url import (SOCIALS_COM, URL_REGEX,
                                           url_base_name, url_norm)


@dataclass
class CrawlLink:
    link: str
    source: str
    title: Optional[str] = None
    published: Optional[str] = None
    author: Optional[str] = None

    def __hash__(self):
        return hash(self.link)


def from_robot(url: str, lastmod: int = 1) -> List[CrawlLink]:

    maps = get_sitemaps_from_url(url)
    if maps:
        _links = parse_sites_xml(maps, filter_dt=lastmod)
    else:
        _links = parse_sites_xml([f"{url}/sitemap.xml"], filter_dt=lastmod)

    total = [CrawlLink(link=url_norm(x["fullurl"]), source="xml", published=x["lastmod"])
             for x in _links]

    return total


def from_rss(url) -> List[CrawlLink]:
    final = []
    _rss_links = find_rss_links(url)
    for rl in _rss_links:
        feed = rl.parse()
        for f in feed:
            _norm = url_norm(f.link)
            _link = CrawlLink(
                link=_norm,
                source="rss",
                title=f.title.strip(),
                published=f.published,
                author=f.author
            )
            final.append(_link)

    return final


def from_website_links(links, url: str) -> List[CrawlLink]:

    orig_parsed = urlparse(url)
    _original = url_norm(url)
    base_url = f"{orig_parsed.scheme}://{orig_parsed.netloc}"
    final_links = []
    now = datetime.now().isoformat()
    for l in links:
        if l.internal:
            _url = urlparse(l.href)
            final = l.href
            if _url.netloc == '':
                final = f"{base_url}/{_url.path}"
            _norm = url_norm(final)
            if _norm != _original:
                _link = CrawlLink(link=_norm,
                                source="root",
                                title=l.title.strip(),
                                published=now
                                )
                final_links.append(_link)
    return final_links


def _is_social(base_url, socials):
    # print(_u)
    for s in socials:
        if s in base_url:
            return True
    return False


def _rebuild_social_url(url_tuple):
    return f"https://{''.join(url_tuple[1:])}"


def social_from_html(html: str) -> List[str]:

    urls = re.findall(URL_REGEX, html)
    extracted = set()
    # print(len(urls))
    for u in urls:
        # print(u.split('"')[0])
        # print(u)
        if _is_social(u[1], SOCIALS_COM):
            extracted.add(_rebuild_social_url(u))
    return list(extracted)


def get_social_related(urls_list, origin_url):
    netloc = url_base_name(origin_url).lower()
    final = []
    for u in urls_list:
        to_compare = urlparse(u).path.split("/")[-1]
        if lv.distance(netloc, to_compare.lower()) < 4 \
           or "youtube" in u \
           or "spotify" in u:
            final.append(u)

    return final
