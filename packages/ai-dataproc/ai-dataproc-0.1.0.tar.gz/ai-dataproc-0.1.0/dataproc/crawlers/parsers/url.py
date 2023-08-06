import re
from dataclasses import dataclass
from typing import Union
from urllib.parse import urlparse

from hashes.noncrypto import Hasher
from iso3166 import Country, countries

# https://coddingbuddy.com/article/10777844/find-url-with-regex-on-text
URL_REGEX = r"(http|ftp|https):\/\/([\w\-_]+(?:(?:\.[\w\-_]+)+))([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?"

SOCIALS_COM = [
    "facebook.com",
    "instagram.com",
    "t.me",
    "facebook.com",
    "twitter.com",
    "tiktok.com",
    "youtube.com",
    "spotify.com",
    "wikipedia.org",
    "meetup.com",
    "linkedin.com",
    "books.google.com",
    "bit.ly"
]


WORDS_REGEX = re.compile(r'\b[A-Za-z]+\b')


@dataclass
class URL:
    """
    url is without protocol and www netheir
    fullurl: is with https but normalized
    """
    # base_url: str
    url: str
    fullurl: str
    www: bool
    secure: bool

    @classmethod
    def from_str(cls, url):
        _u = urlparse(url)
        # netloc = _u.netloc.strip("/")
        _path = _u.path.strip("/")
        norm = f"{_u.scheme}://{_u.netloc}/{_path}"
        norm = norm.strip("/")

        _url = _u.netloc
        secure = False
        if "https" in _u.scheme:
            secure = True

        www = False
        splited = _u.netloc.split("www.")
        if len(splited) > 1:
            www = True
            _url = splited[1]

        if _path:
            _url = f"{_url}/{_path}"

        return cls(url=_url,
                   fullurl=norm,
                   www=www,
                   secure=secure)

    @property
    def base_name(self):
        return url_base_name(self.fullurl)


@dataclass
class URL2:
    fullurl: str
    url_short: str
    www: bool
    secure: bool
    domain_base: str  # withouth www
    netloc: str  # parsed with urlparsed from python
    path: str
    is_social: bool
    tld: str

    def text(self):
        return text_from_link(self.fullurl)

    def __hash__(self):
        return hash(self.fullurl)


@dataclass
class DocID:
    url: URL
    key: str


def parse_url2(url: str) -> Union[URL2, None]:
    """ Parse a url string to URL. 
    URL_REGEX return a tuple with 3 values:
    (protocol, netloc, path)
    """
    url_regex = re.findall(URL_REGEX, url)

    if url_regex:

        _u = urlparse(url)
        protocol = url_regex[0][0]
        path = url_regex[0][2]
        domain = url_regex[0][1]
        domain_base = domain
        fullurl, url_short = url_norm2(url)

        netloc = _u.netloc
        www = False
        _www = domain.split("www.")
        if len(_www) > 1:
            www = True
            domain_base = _www[1]
            netloc = netloc.split("www.")[1]

        is_social = _is_social(domain_base, SOCIALS_COM)
        is_secure = protocol == "https"
        tld = domain.split(".")[-1]

        return URL2(fullurl=fullurl,
                    url_short=url_short,
                    domain_base=domain_base,
                    netloc=_u.netloc,
                    path=path,
                    is_social=is_social, secure=is_secure, www=www,
                    tld=tld)
    return None


def url_norm(url, trailing=True):
    """
    Strip slashes. 
    """
    _u = urlparse(url)
    # netloc = _u.netloc.strip("/")
    _path = _u.path.strip("/")
    final = f"{_u.scheme}://{_u.netloc}/{_path}"
    if trailing:
        final = final.strip("/")
    return final


def url_norm2(url, trailing=True):
    """
    Strip slashes. 
    """
    _u = urlparse(url)
    # netloc = _u.netloc.strip("/")
    _path = _u.path.strip("/")
    fullurl = f"{_u.scheme}://{_u.netloc}/{_path}"
    url_short = f"{_u.netloc}/{_path}"
    if trailing:
        fullurl = fullurl.strip("/")
        url_short = url_short.strip("/")
    return fullurl, url_short


def url_base_name(url: str) -> str:
    u = urlparse(url)
    _base = u.netloc.split("www.")
    if len(_base) == 2:
        final = _base[1].split(".")[0]
    else:
        final = _base[0].split(".")[0]
    return final


def url2docid(url: Union[str, URL]) -> DocID:
    """ Returns a hash based on a normalized url
    """
    final_url = None
    if isinstance(url, str):
        _url = URL.from_str(url)  # urlnorm
        final_url = _url
        _key = Hasher.xxhash64(_url.url).hexdigest
    elif isinstance(url, URL):
        _key = Hasher.xxhash64(url.url).hexdigest
        final_url = url

    return DocID(url=final_url, key=_key)


def rebuild_url(data):
    url = "http://"
    if data["secure"]:
        url = "https://"
    if data["www"]:
        url = f"{url}www."
    return f"{url}{data['urlnorm']}"


def text_from_link(link: str) -> str:
    """ Gets a link a return a string from the path. 
    It try to keep the last part of the url and give away any extension:
    >> text_from_link("https://www.perfil.com/noticias/politica/morales-y-bullrich-reeditaron-los-reproches-y-profundizaron-las-diferencias-sobre-el-rumbo-de-jxc.phtml")
    >> 'morales y bullrich reeditaron los reproches y profundizaron las diferencias sobre el rumbo de jxc'

    """
    u = urlparse(link)
    _path = u.path.split(".")[0]
    between_path = _path.split("/")
    last_path = between_path[-1]
    # last_path = last_path.split(".html")[0]
    words = re.findall(WORDS_REGEX, last_path)
    return " ".join(words)


def _is_social(base_url, socials):
    # print(_u)
    for s in socials:
        if s in base_url:
            return True
    return False


def get_country_from_tld(tld: str) -> Union[Country, None]:
    c = None
    if tld not in {"io", "ai", "com"}:
        try:
            c = countries.get(tld)
        except KeyError:
            c = None
        if tld == "uk":
            c = countries.get("gb")

    return c


def get_country_from_url(url: str) -> Union[Country, None]:
    u = parse_url2(url)
    c = get_country_from_tld(u.tld)
    return c
