import json
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Union
from urllib.parse import urlparse

import extruct
import ujson
from bs4 import BeautifulSoup
from dataproc.crawlers.parsers.url import URL2, parse_url2

EXTENSIONS_REX = r"(\.jpg|\.ico|\.js|\.css|\.png|\.woff2|\.svg)+"


@dataclass
class Content:
    title: str
    articles: List[str]
    h1: List[str]
    h2: List[str]


@dataclass
class Image:
    alt: str
    src: str


@dataclass
class Link:
    title: str
    href: str
    internal: bool

    def __hash__(self):
        return hash(self.href)


def parse_meta_og(soup: BeautifulSoup,
                  meta=["og:url", "og:image", "og:description", "og:type"]) \
        -> Dict[str, str]:
    tags = {}
    for x in meta:
        tag = soup.find("meta", property=x)
        if tag:
            key = x.split(":")[1]
            tags[key] = tag["content"]
            # tags.append({x.split(":")[1]: tag["content"]})

    return tags


def parse_ld_json(soup: BeautifulSoup) -> Union[Dict[str, Any], None]:
    j = soup.find('script', type='application/ld+json')
    if j:
        text = j.string
        jdata = ujson.loads(text)
        return jdata
    return None


def parse_content(soup: BeautifulSoup) -> Content:

    articles = [x.text for x in soup.findAll("article")]
    try:
        title = soup.title.text
    except AttributeError:
        title = ""
    h1 = [x.text for x in soup.findAll("h1")]
    h2 = [x.text for x in soup.findAll("h2")]

    return Content(title=title, articles=articles, h1=h1, h2=h2)


def parse_images(soup: BeautifulSoup) -> List[Image]:

    images = [Image(alt=x.get("alt", ""),
                    src=x.get("src", ""))
              for x in soup.findAll("img")]
    return images


def is_internal_deprecated(url: str, base_url: str) -> bool:
    u = urlparse(base_url)
    up = urlparse(url)
    if up.netloc != '' and u.netloc != up.netloc:
        return False
    return True


def parse_links_deprecated(soup: BeautifulSoup, base_url: str) -> List[Link]:
    links = set()
    for x in soup.findAll("a"):
        try:
            text = x.text
            href = x["href"]
            internal = is_internal_deprecated(href, base_url)
            links.add(Link(title=text, href=href, internal=internal))
        except KeyError:
            pass
    for x in soup.findAll(href=True):
        text = x.text
        href = x["href"]
        if not ".js" in href:
            internal = is_internal_deprecated(href, base_url)
            links.add(Link(title=text, href=href, internal=internal))

    return list(links)


def _proc_soup_link(s_link, url: URL2) -> Link:
    text = s_link.text
    href = s_link["href"]
    internal = False

    is_a_file = re.findall(EXTENSIONS_REX, href)
    if not is_a_file:
        parsed = urlparse(href)
        if not parsed.netloc:
            protocol = "http"
            if url.secure:
                protocol = "https"
            href = f"{protocol}://{url.netloc}/{parsed.path}"
        if url.domain_base in href:
            internal = True

        return Link(title=text.strip(), href=href.strip(), internal=internal)


def links_from_soup(soup: BeautifulSoup, fullurl: str) -> List[Link]:
    links = set()
    url = parse_url2(fullurl)
    for x in soup.findAll("a"):
        try:
            link = _proc_soup_link(x, url)
            if link:
                links.add(link)
        except KeyError:
            pass
    for x in soup.findAll(href=True):
        try:
            link = _proc_soup_link(x, url)
            if link:
                links.add(link)
        except KeyError:
            pass
    return list(links)


@dataclass
class WebSite:
    content: Content
    html_lang: Union[str, None]
    title: Union[str, None]
    links: List[Link]
    images: List[Image]
    text: str
    og_tags: Union[Dict[str, str], None]
    ld_data: Union[Dict[str, Any], None]

    def find_og_property(self, prop):
        for x in self.og_tags:
            for p in x.get("properties"):
                if f"og:{prop}" in p[0]:
                    return p[1]


def parser_html(html: str, base_url: str) -> WebSite:
    soup = BeautifulSoup(html, 'lxml')
    lang = soup.html.get("lang")
    try:
        title = soup.title.text
    except AttributeError:
        title = None
    content = parse_content(soup)
    links = links_from_soup(soup, base_url)
    images = parse_images(soup)

    data = extruct.extract(html, base_url=base_url,
                           syntaxes=['json-ld', 'opengraph'])

    ld_data = data["json-ld"]
    og_tags = data["opengraph"]

    return WebSite(
        content=content,
        html_lang=lang,
        title=title,
        links=links,
        images=images,
        text=soup.text,
        ld_data=ld_data,
        og_tags=og_tags
    )


def parse(html: str, fullurl: str) -> WebSite:
    """ shortcut """
    soup = BeautifulSoup(html, 'lxml')
    lang = soup.html.get("lang")
    try:
        title = soup.title.text
    except AttributeError:
        title = None
    content = parse_content(soup)
    links = links_from_soup(soup, fullurl)
    images = parse_images(soup)

    try:
        data = extruct.extract(html, base_url=fullurl,
                               syntaxes=['json-ld', 'opengraph'])

        ld_data = data["json-ld"]
        og_tags = data["opengraph"]
    except json.decoder.JSONDecodeError:
        ld_data = None
        og_tags = None

    return WebSite(
        content=content,
        html_lang=lang,
        title=title,
        links=links,
        images=images,
        text=soup.text,
        ld_data=ld_data,
        og_tags=og_tags
    )
