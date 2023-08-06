import re
# from dataproc.words.persons import Persons
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from dataproc.crawlers.parsers.url import URL, url_base_name


@dataclass
class URLTweet:
    trend_taskid: str
    trend_name: str
    volume: int
    interactions: int
    category: Dict[str, Any]
    fullurl: str


@dataclass
class MediaTweet:
    trend_taskid: str
    trend_name: str
    tweet_text: str
    volume: int
    interactions: int
    category: Dict[str, Any]
    fullurl: str


def extract_mentions(twt):
    users = []
    for u in twt.entities["user_mentions"]:
        users.append(
            dict(name=u["name"], screen_name=u["screen_name"], id_str=u["id_str"]))
    return users


def extract_urls(twt):
    urls = []
    for u in twt.entities["urls"]:
        urls.append(u["expanded_url"])
    return urls


@dataclass
class Media:
    url: str
    retweet_count: int
    text: str


def extract_media(twt) -> List[Media]:
    media = []
    _media = twt.entities.get("media")
    if _media:
        for u in _media:
            _m = Media(
                url=u["media_url"],
                retweet_count=twt.retweet_count,
                text=twt.full_text
            )
            media.append(_m)
    return media


@dataclass
class TrendWord:
    original: str
    hashtag: bool
    upper_words: bool
    parsed: Optional[str]

    @staticmethod
    def from_original(word):
        tw = trend_parser(word)
        return tw


def trend_parser(word) -> TrendWord:
    parsed = re.findall('[A-Z][^A-Z]*', word)
    hashtag = False
    # parsed = None
    final_parsed = None
    upper_words = False
    if "#" in word:
        hashtag = True

    if len(parsed) > 1 and len(word.split()) < 2:
        _word = ""
        final = []
        for iy, y in enumerate(parsed):
            if len(y) == 1:
                # print(iy)
                # _word += result.pop(iy)
                _word += y
            else:
                final.append(y)
        if _word:
            final.append(_word)
            upper_words = True
        final_parsed = " ".join(final)
    return TrendWord(original=word, hashtag=hashtag, parsed=final_parsed, upper_words=upper_words)


def parse_all_tweets(trends):
    _trends = []
    _promoted = []
    for w in trends:
        tw = trend_parser(w["name"])
        volume = w["tweet_volume"]
        if w["promoted_content"]:
            _promoted.append((tw, volume))
        else:
            _trends.append((tw, volume))
    return _trends, _promoted


def merge_trends(trends, original_limit=10, ordered_limit=10):
    ordered = list(filter(lambda x: bool(x[1]), trends))
    ordered.sort(key=lambda t: t[1], reverse=True)
    s1 = {x[0].original for x in ordered[:ordered_limit]}
    s2 = {x[0].original for x in trends[:original_limit]}
    s3 = s1.union(s2)
    _final = list(filter(lambda x: bool(x[0].original in s3), trends))
    return _final


def extract_data_for_crawl(trends_list, taskid):
    media_data = []
    urls_data = []
    for t in trends_list:
        word = t["trend_word"]["original"]
        volume = t["volume"]
        category = t["text_category"]
        for m in t["media"]:
            interactions = m["retweet_count"]
            mt = MediaTweet(
                trend_taskid=taskid,
                trend_name=word,
                volume=volume,
                interactions=interactions,
                category=category,
                tweet_text=m["text"],
                fullurl=m["url"]
            )
            media_data.append(mt)

        for u in t["urls"]:
            url = URL.from_str(u["url"])
            base = url_base_name(u["url"])
            if base == "bit":
                r = requests.get(url.fullurl)
                url = URL.from_str(r.url)

            interactions = u["retweets"]
            if base not in ["twitter"]:

                ut = URLTweet(trend_taskid=taskid,
                              trend_name=word,
                              volume=volume,
                              interactions=interactions,
                              category=category,
                              fullurl=url.fullurl)
                urls_data.append(ut)
    return urls_data, media_data
