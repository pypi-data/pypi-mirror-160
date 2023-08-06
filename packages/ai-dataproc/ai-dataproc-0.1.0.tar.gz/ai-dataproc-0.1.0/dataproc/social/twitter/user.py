from dataclasses import dataclass
from typing import Any, Dict, List, Union

import tweepy
from dataproc.social.twitter.api import TwitterApi
from dataproc.words.utils import lang_detect
from iso3166 import countries


@dataclass
class TwitterUser:
    screen_name: str
    followers_count: int
    friends_count: int
    description: str
    urls: Union[List[str], None]
    verified: bool
    image: str
    created_at: str
    location: Union[None, str]
    location_code: Union[None, str]
    lang_predict: Union[None, str]


@dataclass
class TwitterUserResponse:
    data: TwitterUser
    raw: Dict[str, Any]
    user: tweepy.models.User


def get_screen_name(social: List[str]) -> str:
    """Find the screen name from a list of urls """
    tweet_url = list(filter(lambda x: "twitter" in x, social))[0]
    screen_name = tweet_url.split("/")[-1]
    return screen_name


def get_user(t_client: TwitterApi, screen_name=None, user_id=None) -> TwitterUserResponse:
    u = t_client.get_user(screen_name=screen_name, user_id=user_id)
    location = u.location
    try:
        location_code = countries.get(u.location).alpha2
    except KeyError:
        location_code = None
    except AttributeError:
        location_code = None

    try:
        urls = [u["expanded_url"] for u in u.entities["url"]["urls"]]
    except KeyError:
        urls = None
    except AttributeError:
        urls = None
    except NameError:
        urls = None

    raw_data = u._json
    lang = lang_detect(u.description)
    twitter_data = TwitterUser(screen_name=u.screen_name,
                               followers_count=u.followers_count,
                               friends_count=u.friends_count,
                               description=u.description,
                               urls=urls,
                               verified=u.verified,
                               location=location,
                               location_code=location_code,
                               lang_predict=lang,
                               image=u.profile_image_url,
                               created_at=u.created_at.isoformat())

    return TwitterUserResponse(data=twitter_data, raw=u._json, user=u)
