from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pandas as pd
from dataproc.crawlers.parsers.url import URL, url_base_name
from dataproc.datastore import DataBucket
from dataproc.social.models import TweetTrendModel, TweetTrendTask
from hashes.noncrypto import Hasher
from sqlalchemy import delete, select


class TwitterData:

    def __init__(self, woeid: int,
                 country: str,
                 lang: str,
                 taskid: Optional[str] = None):
        self.woeid = woeid
        self.country = country
        self.taskid: Optional[str] = taskid
        self.lang = lang

    def save_detail(self, session, bucket: DataBucket,
                    ttd: Dict[str, Any]):

        _h = Hasher.xxhash64(ttd["trend_word"]["original"]).hexdigest
        _key = _h + self.taskid
        trend_detail = dict(**ttd)
        trend_detail["taskid"] = self.taskid
        trend_detail["woeid"] = self.woeid
        trend_detail["country"] = self.country

        tweet_model = TweetTrendModel(
            name=ttd["trend_word"]["original"],
            taskid=self.taskid,
            bucket_id=bucket.id
        )
        r = bucket.write(_key, trend_detail, mode="w")
        session.add(tweet_model)
        return r

    def save_general(self, session, bucket: DataBucket, trends_names, data):
        ttt = TweetTrendTask(
            taskid=self.taskid,
            words=trends_names,
            bucket_id=bucket.id,
            lang=self.lang,
            woeid=self.woeid
        )
        r = bucket.write(self.taskid, data, mode="w")
        session.add(ttt)
        return ttt, r

    @staticmethod
    def delete_general(session, bucket: DataBucket, taskid):
        stmt = delete(TweetTrendTask)\
            .where(TweetTrendTask.taskid == taskid)
        session.execute(stmt)

        bucket.delete(taskid)

    @classmethod
    def get_general_trend(cls, session, woeid=None):
        stmt = select(TweetTrendTask)
        if woeid:
            stmt = stmt.where(TweetTrendTask.woeid == woeid)
        stmt = stmt.order_by(TweetTrendTask.created_at)
        rows = session.execute(stmt).scalars()
        return rows

    @classmethod
    def get_general_last(cls, session, delta, hours=True, woeid=None):
        if hours:
            last = datetime.utcnow() - timedelta(hours=delta)
        else:
            last = datetime.utcnow() - timedelta(delta)

        stmt = select(TweetTrendTask)

        if woeid:
            stmt = stmt.where(TweetTrendTask.woeid == woeid)

        stmt = stmt.where(TweetTrendTask.created_at > last.isoformat())
        stmt = stmt.order_by(TweetTrendTask.created_at)

        rows = session.execute(stmt).scalars()
        return rows

    @classmethod
    def get_last_trends(cls, session, delta, hours=True, woeid=None):
        rows = cls.get_general_last(
            session, delta=delta, hours=hours, woeid=woeid)

        tasks = [r.to_dict() for r in rows]

        trends = cls.get_trend_from_bucket(tasks)

        return trends

    @staticmethod
    def get_trend_from_bucket(tasks):
        twitter_data = []
        for task in tasks:
            print(task["taskid"])
            _bucket = DataBucket(
                task["bucket"]["id"],
                task["bucket"]["namespace"],
                task["bucket"]["datastore"],
            )
            data = _bucket.read(task["taskid"]).json()
            twitter_data.append(data)
        return twitter_data


def url_parsed(data):
    parsed = []
    for u in data:
        base = url_base_name(u["url"])
        if base.lower() not in ["twitch", "twitter"]:
            url = URL.from_str(u["url"])
            parsed.append(url.fullurl)
    return parsed


def as_dataframe(tdata) -> pd.DataFrame:
    td = {}
    for x in tdata:
        for j in x["trends_details"]:
            _urls = url_parsed(j["urls"])
            word = j["trend_word"]["original"]
            # print(word)
            _texts = [rt["full_text"] for rt in j["raw_tweets"]]
            _text = ". ".join(_texts)
            _text = _text.replace("RT", "")
            _retweets = [rt["retweet_count"] for rt in j["raw_tweets"]]
            _int = sum(_retweets)
            _td = dict(
                word=j["trend_word"]["original"],
                urls=_urls,
                volume=j["volume"],
                category=j["text_category"],
                interactions=_int,
                fulltext=_text,
            )

            if td.get(word):
                if _urls:
                    td[word]["urls"].append(_urls)
            td[word] = _td

    td_dict = [t for t in td.values()]
    df_tweets = pd.DataFrame(td_dict)
    return df_tweets
