from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

import dateparser
import pytz
from dataproc.crawlers.links_extractors import social_from_html
from dataproc.crawlers.parsers import authors
from dataproc.crawlers.parsers.article import ArticleData
from dataproc.crawlers.parsers.html import WebSite, parser_html
from dataproc.crawlers.parsers.url import (get_country_from_tld, parse_url2,
                                           url2docid, url_base_name, url_norm)
from dataproc.words import lang


@dataclass
class Page:
    url: str
    web: WebSite
    html: str
    created_at: Optional[str] = None

    # @Timeit
    @classmethod
    def from_html_txt(cls, url, html):
        norm = url_norm(url)
        web = parser_html(html, base_url=norm)
        return cls(url=norm, web=web, html=html)

    @property
    def base_name(self):
        return url_base_name(self.url)

    def social(self):
        return social_from_html(self.html)

    def find_og(self, prop):
        for x in self.web.og_tags:
            for p in x.get("properties"):
                if f"og:{prop}" in p[0]:
                    return p[1]
        return None

    def article_data(self) -> ArticleData:
        """Parse html as it was an article from a news site. """
        return ArticleData.from_html(self.url, self.html)

    def get_date(self, article=None):
        dt = None
        if article:
            if article.publish_date:
                dt = article.publish_date.astimezone(pytz.utc)

        if not dt:
            if self.web.ld_data and self.web.ld_data[0].get("datePublished"):
                dt = dateparser.parse(self.web.ld_data[0].get(
                    "datePublished")).astimezone(pytz.utc)
        return dt


@dataclass
class PageRSP3:
    fullurl: str
    url: str
    docid: str

    domain_base: str
    siteid: str
    country_tld: Optional[str] = None

    meta_img: Optional[str] = None
    meta_desc: Optional[str] = None
    page_h1: Optional[str] = None
    page_h2: Optional[str] = None
    page_article: Optional[str] = None
    page_authors: Optional[List[str]] = None
    page_title: Optional[str] = None
    page_html_lang: Optional[str] = None
    page_date: Optional[str] = None

    ml_lang: Optional[str] = None
    created_at: Optional[str] = None


def get_ld(p, k):
    a = None
    if p.web.ld_data:
        a = p.web.ld_data[0].get(k)
    return a


def get_description(p: Page):
    desc = ""
    from_og = True
    _desc = p.web.find_og_property("desc")

    if not _desc:
        try:
            desc = p.web.content.h2[0]
            from_og = False
        except IndexError:
            desc = ""
            from_og = False
    else:
        desc = _desc
    return desc, from_og


def text_to_predict2(p: Page):
    """ Sometimes article data could be garbage if the site doesn't render
    html well. So instead we are using title and description as a meangfull text.
    """
    # title = p.web.title
    title = p.web.content.h1[0]

    desc, _ = get_description(p)
    text = f"{title}. {desc}"
    return text


def _h1_h2(page):

    h1 = None
    h2 = None
    if isinstance(page.web.content.h1, list):
        try:
            h1 = page.web.content.h1[0]
            h1 = h1.strip()
        except IndexError:
            pass

    if isinstance(page.web.content.h2, list):
        try:
            h2 = page.web.content.h2[0]
            h2 = h2.strip()
        except IndexError:
            pass

    return h1, h2


def _siteid_from_url2(url2):
    _site_url = "http://"
    if url2.secure:
        _site_url = "https://"
    _site_url = f"{_site_url}{url2.netloc}"
    site_id = url2docid(_site_url)

    return site_id.key


def transform(page, stopw, as_dict=False) -> Union[Dict[str, Any], PageRSP3]:
    """ Extracts only what it is needed for ML and Indexing content """
    _doc = url2docid(page.url)
    _key = _doc.key
    _url = _doc.url
    h1, h2 = _h1_h2(page)
    art = page.article_data()
    page_dt = page.get_date(art)
    if page_dt:
        page_dt = page_dt.isoformat()
    url2 = parse_url2(page.url)

    country_tld = get_country_from_tld(url2.tld)
    alpha2 = None
    if country_tld:
        alpha2 = country_tld.alpha2

    meta_og_image = page.find_og("image")
    meta_desc = page.find_og("desc")
    ml_lang = lang.predict_txt(page.web.title)
    authors_ = authors.get_from_ld(page.web.ld_data, stopw)
    siteid = _siteid_from_url2(url2)

    authors_norm = None
    if authors_:
        authors_norm = authors_.authors_norm

    rsp = dict(
        fullurl=_url.fullurl,
        url=_url.url,
        docid=_key,
        domain_base=url2.domain_base,
        siteid=siteid,
        country_tld=alpha2,
        meta_img=meta_og_image,
        meta_desc=meta_desc,
        page_h1=h1,
        page_h2=h2,
        page_article=art.text,
        page_authors=authors_norm,
        page_title=page.web.title,
        page_html_lang=page.web.html_lang,
        page_date=page_dt,
        ml_lang=ml_lang
    )
    if as_dict:
        return rsp
    return PageRSP3(**rsp)
