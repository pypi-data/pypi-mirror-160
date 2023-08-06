from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import tweepy
from dataproc.datastore import DataBucket
# from dataproc.social.models import TwitterTrendM
from dataproc.social.models import TweetTrendModel, TweetTrendTask
from dataproc.social.twitter.api import TwitterApi
from dataproc.social.twitter.utils import (extract_media, extract_mentions,
                                           extract_urls)
from hashes.noncrypto import Hasher
from sqlalchemy import delete, select


def _parse_datetime(created_at):
    # date parsing: https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
    dt = datetime.strptime(
        created_at, '%a %b %d %H:%M:%S +0000 %Y')
    return dt


def _resume_tweet(status: tweepy.models.Status, urls, media, mentions):
    td = dict(urls=urls, media=media, mentions=mentions,
              text=status.full_text,
              # hashtags=x["entities"]
              verified=status.user.verified,
              retweets=status.retweet_count,
              likes=status.favorite_count,
              statuses_count=status.user.statuses_count,
              screen_name=status.user.screen_name,
              user_followers=status.user.followers_count,
              created_at=_parse_datetime(
                  status._json["created_at"]).isoformat()
              )
    return td


@dataclass
class SearchResult:
    tweets: List[tweepy.models.Status]
    raw_data: List[Dict[str, Any]]
    text: str
    mentions: List[Dict[str, Any]]
    urls: List[Any]
    medias: List[Any]

    def get_texts(self) -> List[str]:
        return [x["full_text"] for x in self.raw_data]

    @staticmethod
    def parser_dt(dt: str):
        return _parse_datetime(dt)


def search_tweets(twitter: TwitterApi, word,
                  lang="es", mode="extended", items=20) -> SearchResult:
    tweets = []
    raw_data = []
    text = ""
    urls = []
    medias = []
    mentions = []
    for status in tweepy.Cursor(twitter.api.search_tweets,
                                word, lang=lang,
                                tweet_mode=mode).items(items):
        tweets.append(status)
        _mentions = extract_mentions(status)
        _urls = extract_urls(status)
        _media = extract_media(status)
        if _urls:
            for u in _urls:
                urls.append((u, status.retweet_count))

        if _media:
            for m in _media:
                medias.append((m, status.retweet_count))

        if _mentions:
            for m in _mentions:
                mentions.append((m, status.retweet_count))

        text += ". " + status.full_text
        # tweets_data.append(td)
        raw_data.append(status._json)

    medias.sort(key=lambda t: t[1], reverse=True)
    mentions.sort(key=lambda t: t[1], reverse=True)
    urls.sort(key=lambda t: t[1], reverse=True)
    return SearchResult(tweets=tweets, raw_data=raw_data,
                        text=text,
                        mentions=_mentions,
                        urls=urls,
                        medias=medias
                        )


class TrendData:

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


# class Twitter:
#
#    def __init__(self, api: TwitterApi):
#        self.api = api
#
#    def get_trends(self, session, woeid, taskid=None):
#        if not taskid:
#            taskid = TwitterTrend.generate_taskid()
#
#        trends = self.api.trends_place(woeid)
#
#        for ix, t in enumerate(trends[0]["trends"]):
#            """
#            "name": "Bachelet",
#            "url": "http://twitter.com/search?q=Bachelet",
#            "promoted_content": null,
#            "query": "Bachelet",
#            "tweet_volume": 29541
#            """
#            tt = TwitterTrend(
#                name=t.get("name"),
#                ranking=ix + 1,
#                promoted_content=t.get("promoted_content"),
#                query=t.get("query"),
#                volume=t.get("tweet_volume"),
#                woeid=woeid,
#                # place_id=pdata.id,
#                taskid=taskid
#            )
#            session.add(tt)
