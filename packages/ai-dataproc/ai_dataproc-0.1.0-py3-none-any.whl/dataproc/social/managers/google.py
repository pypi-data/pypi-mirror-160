from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from dataproc.crawlers.google import TrendSearchResponse
from dataproc.crawlers.parsers.url import URL
from dataproc.datastore import DataBucket
from dataproc.social.models import GoogleTrendTask
from hashes.noncrypto import Hasher
from iso3166 import countries
from sqlalchemy import select

blacklist = [
    "twitter.com",
    "wikipedia.org",
    "ytimg.com",
    "pedidosya.com",
    "tripadvisor.com",
]


@dataclass
class GData:
    taskid: str
    trends_crawled: List[TrendSearchResponse]
    created_at: str
    lang: str
    country: str


class GoogleData:

    def __init__(self):
        pass

    @staticmethod
    def save_trend_task(session, taskid: str,
                        bucket: DataBucket,
                        words: List[str], data: GData):

        _lang = data.lang
        _country = data.country
        _country_code = int(countries.get(_country).numeric)
        trend = GoogleTrendTask(
            taskid=taskid,
            words=words,
            country_code=_country_code,
            lang=_lang,
            bucket_id=bucket.id
        )
        r = bucket.write(taskid, asdict(data), mode="w")
        session.add(trend)
        return r

    @staticmethod
    def get_last_trends_db(session, delta, hours=True, country_code=None):
        if hours:
            last = datetime.utcnow() - timedelta(hours=delta)
        else:
            last = datetime.utcnow() - timedelta(delta)

        stmt = select(GoogleTrendTask)
        if country_code:
            stmt = stmt.where(GoogleTrendTask.country_code == country_code)

        stmt = stmt.where(GoogleTrendTask.created_at > last.isoformat())
        stmt = stmt.order_by(GoogleTrendTask.created_at)

        rows = session.execute(stmt).scalars()
        return rows

    @classmethod
    def get_last_trends(cls, session, delta, hours=True, country_code=None):
        _rows = cls.get_last_trends_db(session, delta, hours, country_code)
        gtrends = [r.to_dict() for r in _rows]
        gtasks_failed = []
        google_links = []
        for gt in gtrends:
            try:
                links = cls.get_trend_from_bucket(gt)
                google_links.extend(links)
            except AttributeError:
                gtasks_failed.append(gt["taskid"])
            except KeyError:
                gtasks_failed.append(gt["taskid"])
        return google_links, gtasks_failed

    @staticmethod
    def get_trend_from_bucket(gt):
        bucket_g = DataBucket(
            gt["bucket"]["id"], gt["bucket"]["namespace"], gt["bucket"]["datastore"]
        )
        search_result = bucket_g.read(gt["taskid"]).json()
        # print(google_task)
        links = extract_google_data(search_result)
        return links


def _extract_word(data):
    if data.get("trend"):
        return data.get("trend")
    else:
        return data["trend_word"]


def extract_google_data(gtask):
    lang = gtask["lang"]
    country = gtask["country"]
    created_at = gtask["created_at"]
    taskid = gtask["taskid"]
    google_data = []
    for x in gtask["trends_crawled"]:
        word = _extract_word(x)
        section = x["section"]
        section_proba = x["section_proba"]
        for r in x["results"]:
            # _base = url_base_name(r)
            url_ = URL.from_str(r)
            valid = True
            for b in blacklist:
                if b in url_.url:
                    valid = False
                    break
            # if _base not in blacklist:
            _uparsed = urlparse(r)
            if _uparsed.path and valid:
                docid = Hasher.xxhash64(url_.url).hexdigest

                dict_ = dict(
                    word=word,
                    trend_section=section,
                    trend_section_proba=section_proba,
                    url=url_.fullurl,
                    docid=docid,
                    # text=r["text"],
                    lang=lang,
                    country=country,
                    created_at=created_at,
                )
                google_data.append(dict_)
    return google_data
