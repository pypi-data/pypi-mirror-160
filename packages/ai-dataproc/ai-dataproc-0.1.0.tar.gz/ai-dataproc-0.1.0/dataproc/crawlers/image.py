from io import BytesIO

from dataproc.conf import Config
from dataproc.crawlers import aio_fetch, fetch
from dataproc.datastore.core import AIODataBucket, DataBucket
from PIL import Image


async def get_img_async(url_img, strategy=Config.DEFAULT_STRATEGY) -> bytes:

    req = aio_fetch.from_url(url_img)
    req.strategy = strategy

    # print(u_img)
    # async with httpx.AsyncClient(headers={"user-agent": Config.AGENT}) as client:
    #    r = await client.get(u_img)
    r = await aio_fetch.get(req)
    return r.content


def get_img(url_img, strategy=Config.DEFAULT_STRATEGY) -> bytes:

    req = fetch.from_url(url_img)
    req = strategy

    r = fetch.get(req)
    return r.content


def convert_to_webp(img: bytes) -> bytes:
    i = Image.open(BytesIO(img))
    b = BytesIO()
    i.save(b, "webp")
    _bytes = b.getvalue()
    return _bytes


async def get_and_store_img_async(bucket: AIODataBucket,
                                  key: str, url_img: str,
                                  strategy=Config.DEFAULT_STRATEGY):
    if url_img:
        img_bytes = await get_img_async(url_img, strategy=strategy)
        i = convert_to_webp(img_bytes)
        await bucket.put_data(key, i, mode="wb")


def get_and_store_img(bucket: DataBucket, key: str, url_img: str,
                      strategy=Config.DEFAULT_STRATEGY):
    if url_img:
        img_bytes = get_img(url_img, strategy)
        i = convert_to_webp(img_bytes)
        bucket.write(key, i, mode="wb")
