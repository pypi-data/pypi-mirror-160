import logging
import multiprocessing as mp
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import arrow
import cytoolz as toolz
import pandas as pd
from dataproc.conf import Config
# from dataproc.crawlers.http_client import http_get, make_agent_headers
from dataproc.crawlers import fetch, links_extractors
from dataproc.crawlers.fetcher import HTTPError
from dataproc.crawlers.managers.site import RootPage, RootSave, SiteManager
# from dataproc.crawlers.parsers.html import (WebSite, extract_text_from_link,
#                                            parser_html, url_norm)
from dataproc.crawlers.parsers import html, rss
from dataproc.crawlers.parsers import url as url_parser
from dataproc.crawlers.utils import link_status, url2docid
from iso3166 import countries

logger = logging.getLogger(__name__)


@dataclass
class CrawlRootTask:
    # pylint: disable=too-many-instance-attributes
    url: str
    lastmod: int = 1
    valid_url: int = 2
    user_agent: str = Config.AGENT

    store: bool = False
    label: str = "0"
    strategy: str = Config.DEFAULT_STRATEGY
    timeout: int = 30  # secs
    country: Optional[str] = None
    ds: Optional[str] = None
    ns: Optional[str] = None


@dataclass
class CrawlRootResponse:
    root: RootPage
    saved: Union[RootSave, None]
    country: Union[str, None]
    label: Union[str, None]
    _valid_url: Union[int, None]
    _lastmod: int = 1
    _df: Optional[pd.DataFrame] = None

    @property
    def df(self):
        if not isinstance(self._df, pd.DataFrame):
            df = build_df(self.root)
            df["country"] = self.country
            df["label"] = self.label
            mask = create_mask(df, self._valid_url, self._lastmod)
            self._df = df[mask].copy()
        return self._df


def external_links(root):
    links = []
    for x in root.web.links:
        if not x.internal and root.base_name not in x.href:
            links.append(x)
    return links


def to_date_type(dt: datetime) -> str:
    """
    Simple format string, a datetype only includes
    year month and day.
    2021-01-22
    format: now.strftime("%m/%d/%Y
    """
    return dt.strftime("%Y-%m-%d")


def extract_links_from_root(root: RootPage):

    url_parsed = url2docid(root.url)
    siteid = url_parsed.docid
    base_name = root.base_name
    links = []
    for _, v in root.links.items():
        data = asdict(v)
        try:
            _dt = arrow.get(data["published"]).datetime
            data["dt"] = _dt
        except arrow.ParserError:
            data["dt"] = None
        except TypeError:
            data["dt"] = None
        link_parsed = url2docid(data["link"])

        data["docid"] = link_parsed.docid
        data["siteid"] = siteid
        data["site_url"] = url_parsed.url.fullurl
        data["label"] = None
        data["bucket_id"] = None
        data["basename"] = base_name
        # data["orig_url"] = data["link"]
        data["lang"] = root.web.html_lang
        data["country"] = None
        links.append(data)
    return links


def augment_link_text(row):
    try:
        words = url_parser.text_from_link(row.link)
        if pd.isna(row.title):
            return words
        else:
            return row.title.strip()
    except TypeError:
        return ""


def get_link_text(link):
    try:
        words = url_parser.text_from_link(link)
    except:
        words = ""

    return words


def to_pandas(links):
    df = pd.DataFrame(links)
    df.set_index("docid", inplace=True)
    df["dt"] = pd.to_datetime(df["dt"], utc=True)
    df["text"] = df.link.apply(get_link_text)
    df["text"] = df.text.astype("string[pyarrow]")

    text_columns = [
        "link", "source", "title", "author",
        "siteid", "basename", "lang", "text"
    ]
    for c in text_columns:
        df[c] = df[c].astype("string[pyarrow]")

    return df


def validate_links(df):
    """Verify a url
    0: is ok
    1: invalid title
    2: invalid url

    """

    df["link_status"] = df.apply(link_status, axis=1)
    return df


def build_df(root: RootPage) -> pd.DataFrame:
    # pylint: disable=no-member
    df = toolz.pipe(root, extract_links_from_root, to_pandas, validate_links)

    return df


def create_mask(df, valid_url, lastmod):
    """
    valid_url:
        0: is ok
        1: invalid title
        2: invalid url
        3: any url
    """

    from_day = to_date_type(datetime.utcnow() - timedelta(days=lastmod))
    valid_mask = (df.dt > from_day) & (df.link_status < valid_url)
    # print("Valid: ", df[valid_mask].link.count())
    # print("To discard: ", df[~valid_mask].link.count())
    return valid_mask


def crawl_root2(t: CrawlRootTask, session=None) -> CrawlRootResponse:
    """ Main function which will crawl a ROOT site and then parsed it finding:
    social links, rss links, and links in general externals and internals.
    """

    if t.store:
        if not session:
            raise AttributeError("session object is missing")
    root = get_root(t)
    # df = build_df(root)
    # df["country"] = t.country
    # df["label"] = t.label
    # mask = create_mask(df, t.valid_url, t.lastmod)

    country = None
    if not t.country:
        _country = url_parser.get_country_from_url(t.url)
        if _country:
            country = _country.alpha2
    else:
        country = t.country

    saved = None
    if t.store:
        saved = SiteManager.save_root(
            session, root, t.ds, t.ns, t.label, country_code=country)
        if saved.country:
            try:
                alpha2 = countries.get(saved.country).alpha2
                country = alpha2
            except KeyError:
                pass
            except AttributeError:
                pass

    return CrawlRootResponse(
        root,
        country=country,
        label=t.label,
        _lastmod=t.lastmod,
        _valid_url=t.valid_url,
        saved=saved
    )


def get_root(t: CrawlRootTask) -> RootPage:

    url = url_parser.url_norm(t.url)

    # make_agent_headers(t.user_agent)
    req = fetch.from_url(url)
    req.strategy = t.strategy
    req.user_agent = t.user_agent
    r = fetch.get(req)

    web = html.parse(r.text, fullurl=url)
    links = extract_root_links(url, web, lastmod=t.lastmod, timeout=t.timeout)
    _social = links_extractors.social_from_html(r.text)
    try:
        social = links_extractors.get_social_related(_social, url)
    except:
        social = []

    return RootPage(url=url,
                    html=r.text,
                    web=web,
                    links=links,
                    social=social)


def _xml_wrapper(url, lastmod, return_list):

    r = links_extractors.from_robot(url, lastmod)
    return_list.append(r)


def _rss_wrapper(url, return_list):
    try:
        _rss_links = links_extractors.from_rss(url)
        # _rss_links = rss.find_rss_links(url)
        return_list.append(_rss_links)
    except HTTPError:
        logger.warning("RSS HTTPError for site %s", url)
    except ValueError:
        logger.warning("RSS ValueError for site %s", url)


def extract_root_links(url: str, web: html.WebSite, lastmod: int = 1, timeout=30) \
        -> Dict[str, links_extractors.CrawlLink]:
    # links: CrawlLink = []

    manager = mp.Manager()
    return_list: List[Any] = manager.list()
    _robots_links = []

    p = mp.Process(target=_xml_wrapper, args=(url, lastmod, return_list))
    p.start()
    p.join(timeout)

    if p.exitcode == 0:
        _robots_links = return_list[0]
    else:
        logger.warning("sitemap xml timeout for site %s", url)
        p.kill()

    links = {}
    for x in _robots_links:
        links[x.link] = x

    _root_links = links_extractors.from_website_links(web.links, url)
    for x in _root_links:
        if links.get(x.link):
            if links[x.link].published:
                x.published = links[x.link].published
                x.source = links[x.link].source

        links[x.link] = x

    _rss_links = []

    return_list2: List[Any] = manager.list()
    p2 = mp.Process(target=_rss_wrapper, args=(url, return_list2))
    p2.start()
    p2.join(timeout)

    if p2.exitcode == 0 and return_list2:
        _rss_links = return_list2[0]
    elif p2.exitcode != 0:
        logger.warning("RSS timeout for site %s", url)
        p2.kill()
    else:
        logger.warning("Something went wrong with RSS for %s", url)

    for rl in _rss_links:
        links[rl.link] = rl

    return links


def restore_root_page(data) -> RootPage:
    # data = rs.get()
    # dict_keys(['fullurl', 'key', 'social', 'links', 'html'])

    url = url_parser.url_norm(data["fullurl"])

    web = html.parse(data["html"], fullurl=url)
    # links = extract_root_links(web, url, lastmod=t.lastmod)
    links = {l["link"]: links_extractors.CrawlLink(**l) for l in data["links"]}

    return RootPage(url=url,
                    html=data["html"],
                    web=web,
                    links=links,
                    social=data["social"])


def register_site(session, crt: CrawlRootTask, update_site=False) \
        -> Union[CrawlRootResponse, None]:
    r = None
    root_saved = SiteManager.get_root(session, url=crt.url)
    if not root_saved:
        r = crawl_root2(crt, session)
        session.commit()
    elif update_site:
        r = crawl_root2(crt, session)
        session.commit()

    return r
