import re
from dataclasses import dataclass

from dataproc.crawlers.parsers.url import URL
from hashes.noncrypto import Hasher


@dataclass
class URLParsed:
    url: URL
    docid: str


def rebuild_url(data):
    url = "http://"
    if data["secure"]:
        url = "https://"
    if data["www"]:
        url = f"{url}www."
    return f"{url}{data['urlnorm']}"


def rebuild_url_from_model(model):
    url = "http://"
    if model.secure:
        url = "https://"
    if model.www:
        url = f"{url}www."
    return f"{url}{model.urlnorm}"


def url2docid(url) -> URLParsed:
    _url = URL.from_str(url)  # urlnorm
    _key = Hasher.xxhash64(_url.url).hexdigest
    return URLParsed(url=_url, docid=_key)


url_rex = re.compile(
    r"^https?://"  # http:// or https://
    # domain...
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def valid_url(url):
    if re.match(url_rex, url) is not None:
        return True
    return False


def link_status(row):
    """Verify a url
    0: is ok
    1: invalid title
    2: invalid url

    """
    if valid_url(row.link) and "(" not in row.link:
        # parsed = urlparse(x.link)
        # if parsed.path
        # if row.source != "xml" and row.title:
        try:
            if len(row.title.split()) < 4:
                return 1
        except:
            return 1
        # if row.source != "xml" and not row.title.strip() or not row.title or len(row.title.split()) < 2:
        # print("invalid")
        # print(x.link, x.source)
        # print(x.title)
        #   return 1
    else:
        return 2
    return 0
