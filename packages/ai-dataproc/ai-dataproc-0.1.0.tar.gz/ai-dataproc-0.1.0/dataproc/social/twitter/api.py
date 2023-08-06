from dataclasses import dataclass

import tweepy
from dataproc.conf import Config
from dataproc.utils import flatten_list


@dataclass
class Options:

    consumer_key: str
    consumer_secret: str
    access_token: str
    access_secret: str


class TwitterApi:

    def __init__(self, opts: Options):

        _auth = tweepy.OAuthHandler(opts.consumer_key,
                                    opts.consumer_secret)
        _auth.set_access_token(opts.access_token,
                               opts.access_secret)

        self.api = tweepy.API(_auth)

    @classmethod
    def from_config(cls, conf: Config):
        topts = Options(
            consumer_key=conf.consumer_key,
            consumer_secret=conf.consumer_secret,
            access_token=conf.access_token,
            access_secret=conf.access_secret
        )
        return cls(topts)

    def trends_available(self):
        """
        [
        {'country': 'Japan',
        'countryCode': 'JP',
        'name': 'Okayama',
        'parentid': 23424856,
        'placeType': {'code': 7, 'name': 'Town'},
        'url': 'http://where.yahooapis.com/v1/place/90036018',
        'woeid': 90036018}
        ]
        """
        data = self.api.available_trends()
        return data

    def trends_place(self, woeid: int):
        """ trends by place """
        trends = self.api.get_place_trends(woeid)
        return trends

    def search(self, q: str, lang=None, count=200, tweet_mode="extended"):
        tweets = []
        for t in tweepy.Cursor(self.api.search_tweets,
                               q=q,
                               lang=lang,
                               count=200,
                               tweet_mode=tweet_mode)\
                .items(count):
            tweets.append(t)
        return tweets

    def get_friends(self, user_id=None, screen_name=None, count=200, pages=1,
                    tweet_mode="extended", flatten=True):
        """ Following. It allows etheir user_id or screen_name.
        For each `page` it will gets `count` elements.
        """
        if not user_id and not screen_name:
            raise AttributeError("Please provide user_id or user_name")
        pages = []
        for p in tweepy.Cursor(self.api.get_friends, user_id=user_id, screen_name=screen_name,
                               tweet_mode=tweet_mode,
                               count=count).pages(pages):
            pages.append(p)

        if flatten:
            return flatten_list(pages)
        return pages

    def get_followers(self, user_id=None, screen_name=None, count=200, pages=1,
                      tweet_mode="extended", flatten=True):
        """ Followers
        For each `page` it will gets `count` elements.
        """
        if not user_id and not screen_name:
            raise AttributeError("Please provide user_id or user_name")
        pages = []
        for p in tweepy.Cursor(self.api.get_followers, user_id=user_id, screen_name=screen_name,
                               tweet_mode=tweet_mode,
                               count=count).pages(pages):
            pages.append(p)

        if flatten:
            return flatten_list(pages)
        return pages

    def get_user(self, user_id=None, screen_name=None):
        if not user_id and not screen_name:
            raise AttributeError("Please provide user_id or user_name")

        return self.api.get_user(user_id=user_id, screen_name=screen_name)



def create_client1():
    _auth = tweepy.OAuthHandler(Config.consumer_key,
                                Config.consumer_secret)
    _auth.set_access_token(Config.access_token,
                           Config.access_secret)

    api = tweepy.API(_auth)
    return api


def create_client2():
    client = tweepy.Client(**Config.TWITTER)
    return client
