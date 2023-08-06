import logging
import os
from logging import NullHandler


class Config:
    # Services
    SQL = os.getenv("DATAPROC_SQL")
    ASQL = os.getenv("DATAPROC_ASQL")
    FILESERVER = os.getenv("DATAPROC_FILESERVER")

    DISCORD_EVENTS = os.getenv("DISCORD_EVENTS")
    DISCORD_ERRORS = os.getenv("DISCORD_ERRORS")

    RQ_REDIS_HOST = os.getenv("DATAPROC_RQ_HOST", "localhost")
    RQ_REDIS_PORT = os.getenv("DATAPROC_RQ_PORT", "6379")
    RQ_REDIS_DB = os.getenv("DATAPROC_RQ_DB", "1")

    WEB_REDIS = os.getenv("DATAPROC_WEB_REDIS")

    URL_REDIS = os.getenv("DATAPROC_URL_REDIS_HOST",
                          "redis://localhost:6379/0")

    RAWSTORE = os.getenv("DATAPROC_RAWSTORE")
    # INFERENCE_SERVICE = os.getenv("DATAPROC_INFERENCE")
    # DASK_SCHEDULER = os.getenv("DATAPROC_DASK_SCHEDULER")

    CHROME = os.getenv("DATAPROC_CHROME")
    CRAWLER_SERVICE = os.getenv("DATAPROC_CRAWLER")

    WRANGLER = os.getenv("DATAPROC_WRANGLER")
    WRANGLER_TOKEN = os.getenv("DATAPROC_WRANGLER_TOKEN")
    DEFAULT_STRATEGY = os.getenv("DATAPROC_STRATEGY", "direct")

    SONIC = os.getenv("DATAPROC_SONIC_ADDR")
    SONIC_PASS = os.getenv("DATAPROC_SONIC_PASS")

    # MISC
    LOGLEVEL = os.getenv("DATAPROC_LOG", "INFO")
    DEBUG = os.getenv("DATAPROC_DEBUG")
    AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    LOCALE = os.getenv("DATAPROC_LOCALE")

    # Folders
    BASE_PATH = os.getenv("DATAPROC_BASEPATH")
    MODELS_PATH = os.getenv("DATAPROC_MODELS")

    NB_WORKFLOWS = os.getenv("DATAPROC_WORKFLOWS", "workflows/")
    NB_OUTPUT = os.getenv("DATAPROC_NB_OUTPUT", "outputs/")

    PLASMA_DIR = os.getenv("PLASMA_DIR", "/tmp/plasma")
    PLASMA_SIZE = os.getenv("PLASMA_SIZE", "2000000000")  # 2 GB

    # Twitter sensible information
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_secret = os.getenv("ACCESS_SECRET")

    TWITTER = dict(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_SECRET"),
    )

    @classmethod
    def rq2dict(cls):
        return dict(
            host=cls.RQ_REDIS_HOST,
            port=int(cls.RQ_REDIS_PORT),
            db=int(cls.RQ_REDIS_DB),
        )

    @classmethod
    def url_redis2dict(cls):
        url = cls.URL_REDIS.split("redis://")[1]
        h, port_db = url.split(":")
        p, db = port_db.split("/")

        return dict(
            host=h,
            port=p,
            db=db,
        )


# _LOG_LEVEl = os.getenv("DATAPROC_LOG", "INFO")
# _level = getattr(logging, Config.LOGLEVEL)
# logging.basicConfig(format='%(asctime)s %(message)s', level=_level)
# logging.basicConfig(format='%(asctime)s %(message)s')
detailed_format = "[%(asctime)s] - %(name)s %(lineno)d - %(levelname)s - %(message)s"
minimal_format = '%(asctime)s %(message)s'
logging.basicConfig(format=detailed_format)
logging.getLogger(__name__).addHandler(NullHandler())
