from dataproc.conf import Config
from dataproc.social.twitter.api import TwitterApi


def create_twitter_api() -> TwitterApi:
    return TwitterApi.from_config(Config)


# def driver_init(address=Config.DASK_SCHEDULER, init_new=False):
#     from dask.distributed import Client, get_client
#     if init_new:
#         try:
#             client = get_client()
#         except ValueError:
#             client = Client(address)
#     else:
#         client = Client(address)
# 
#     return client
# 
# 
# async def driver_init_async(address=Config.DASK_SCHEDULER):
#     from dask.distributed import Client, get_client
#     client = await Client(address, asynchronous=True)
# 
#     return client
