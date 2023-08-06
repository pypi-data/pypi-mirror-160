import re
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import parse_qs, quote, urlparse

from bs4 import BeautifulSoup
from dataproc.crawlers import fetch
# from dataproc.crawlers.parsers.html import parser_html, url_norm
from dataproc.crawlers.parsers import html


@dataclass
class GLink:
    text: str
    base: str
    url: str
    search: str

    def is_google(self):
        if 'google' in self.base:
            return True
        return False

    def is_twitter(self):
        if 'twitter' in self.base:
            return True
        return False

    def without_query(self):
        url = urlparse(self.url)
        return f'{url.scheme}://{url.netloc}{url.path}'

    def to_dict(self):
        return {'text': self.text,
                'base': self.base,
                'url': self.without_query()}


@dataclass
class SearchResponse:
    links: List[str]
    html: str


@dataclass
class TrendSearchResponse:
    trend_word: str
    results: List[str]
    text: str
    section: Optional[str] = None
    section_proba: Optional[str] = None


class Google:
    """ Search on google an return links """

    _G = 'https://www.google.com/search?q='

    _LANGS = dict(es="tbs=lr:lang_1es&lr=lang_es",
                  pt="tbs=lr:lang_1pt&lr=lang_pt")

    def __init__(self, parser="lxml"):
        # self._chrome_srv = chrome_service

        # self.fetch: Fetch = Fetch()
        self._parser = parser

    def _get(self, words: str, lang=None, strategy="axios") -> str:
        """ Scrap using Chrome Service"""

        _quoted = quote(words)

        fullurl = f'{self._G}{_quoted}'
        if lang:
            extra_param = self._LANGS[lang.lower()]
            fullurl = f'{fullurl}&{extra_param}'

        # res = self.fetch.get(f'{self._chrome_srv}{self._G}{words}')
        req = fetch.from_url(fullurl)
        req.strategy = strategy
        res = fetch.get(req)
        # jres = res.json()
        return res.text

    def search(self, words: str, lang=None, strategy="axios") -> List[GLink]:
        """ Make a search in google, and extracts
        the results from there., return a dict of links

        """

        _html = self._get(words, lang, strategy)

        self.soup = BeautifulSoup(_html, self._parser)

        urls = []
        for link in self.soup.findAll(href=True):
            u = urlparse(link["href"])
            possible_url = parse_qs(u.query).get("q")
            print(possible_url)
            if possible_url:
                parsed = urlparse(possible_url[0])
                if parsed.netloc != "" and "google.com" not in parsed.netloc:
                    l = GLink(
                        text=link.text,
                        base=parsed.netloc,
                        url=possible_url[0],
                        search=words
                    )
                    urls.append(l)

        # if filter_g:
        #    urls = list(filter(
        #        # lambda x: True if not x.is_google() else False,
        #        lambda x: bool(x.is_google()),
        #        urls))

        return urls

    @property
    def tmp_soup(self):
        """ will be replaced in each search"""
        return self.soup


class Search:

    _REGEX = '(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+'
    _G = 'https://www.google.com/search?q='

    _LANGS = dict(es="tbs=lr:lang_1es&lr=lang_es",
                  pt="tbs=lr:lang_1pt&lr=lang_pt")
    _BLACKLIST = ["gstatic", "w3.org",  "google.com", "googleapis.com",
                  "googleadservices.com", "ytimg.com",
                  "googleusercontent.com", "schema.org"]

    def __init__(self):
        pass

    def _get(self, words: str, lang=None, strategy="axios") -> str:
        """ Scrap using Chrome Service"""

        _quoted = quote(words)

        fullurl = f'{self._G}{_quoted}'
        if lang:
            extra_param = self._LANGS[lang.lower()]
            fullurl = f'{fullurl}&{extra_param}'

        # res = self.fetch.get(f'{self._chrome_srv}{self._G}{words}')
        req = fetch.from_url(fullurl)
        req.strategy = strategy
        res = fetch.get(req)
        # jres = res.json()
        return res.text

    def _valid_url(self, url):
        parsed = urlparse(url)
        if parsed.scheme != "" and parsed.netloc != "":
            invalid = False
            for u in self._BLACKLIST:
                if u in parsed.netloc:
                    invalid = True
                    break
            if not invalid:
                return url

    def search(self, words, lang=None, norm=False, strategy="axios") -> SearchResponse:

        _html = self._get(words, lang, strategy)
        # breakpoint()
        urls = re.findall(self._REGEX, _html)
        final = set()
        for u in urls:
            url = self._valid_url(u)
            if url:
                ufinal = url
                if norm:
                    ufinal = html.url_norm(url)
                final.add(ufinal)

        return SearchResponse(links=list(final), html=_html)

    def trend(self, word, lang, strategy="axios") -> TrendSearchResponse:
        if lang != "en":
            result = self.search(word, lang, strategy=strategy)
        else:
            result = self.search(word,  strategy=strategy)

        web = html.parse(result.html, "https://www.google.com")

        return TrendSearchResponse(
            trend_word=word,
            results=result.links,
            text=web.text,
            # section=section # deprecated
            # section_proba=section_proba # deprecated
        )


def extract_url(href):
    url = re.findall(r"(((f|ht){1}tps://)[-a-zA-Z0-9@:%_\+.~#?&//=]+)", href)
    if len(url) > 0:
        try:
            return url[0][0]
        except IndexError:
            pass
