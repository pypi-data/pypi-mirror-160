from typing import List, Union

import aiohttp
import requests
from dataproc.datastore.core import AIODataBucket, DataBucket
from dataproc.http_client import (Fetch, Response, http_post, http_post_async,
                                  make_agent_headers)
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert


def _find_stmt(Model, ds, ns):
    stmt = select(Model)\
        .filter(Model.datastore == ds)\
        .filter(Model.namespace == ns)
    return stmt


def _find_stmt_id(Model, id_):
    stmt = select(Model)\
        .filter(Model.id == id_)
    return stmt


async def find_ds_async(session, Model, ds, ns) -> Union[AIODataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = _find_stmt(Model, ds, ns)
    r = await session.execute(stmt)
    bucket_db = r.scalar()
    if bucket_db:

        return AIODataBucket(id=bucket_db.id,
                             namespace=bucket_db.namespace,
                             datastore=bucket_db.datastore)


async def create_bucket_async(session, Model, ds, ns) -> AIODataBucket:
    headers = make_agent_headers(agent="dataproc")
    r = await http_post_async(f"{ds}/v1/namespace",
                              json={"name": ns},
                              headers=headers)
    if r.status > 201:
        raise IndexError("Bucket Not found, or conn error")

    stmt = insert(Model.__table__).values(namespace=ns,
                                          datastore=ds)
    stmt = stmt.on_conflict_do_nothing()
    await session.execute(stmt)
    await session.commit()
    bucket = await find_ds_async(session, Model, ds, ns)
    return bucket


def find_ds(session, Model, ds, ns) -> Union[DataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = _find_stmt(Model, ds, ns)
    r = session.execute(stmt)
    bucket_db = r.scalar()
    if bucket_db:
        return DataBucket(id=bucket_db.id,
                          namespace=bucket_db.namespace,
                          datastore=bucket_db.datastore)
    return None


def find_ds_by_ns(session, Model, ns) -> Union[DataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = select(Model)\
        .where(Model.namespace == ns)
    r = session.execute(stmt)
    buckets = r.scalars()
    if buckets:
        bucket_db = buckets[0]
        return DataBucket(id=bucket_db.id,
                          namespace=bucket_db.namespace,
                          datastore=bucket_db.datastore)
    return None


async def find_ds_by_ns_async(session, Model, ns) -> Union[AIODataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = select(Model)\
        .where(Model.namespace == ns).limit(1)
    _r = await session.execute(stmt)
    bucket_db = _r.scalar()
    if bucket_db:
        return AIODataBucket(id=bucket_db.id,
                             namespace=bucket_db.namespace,
                             datastore=bucket_db.datastore)
    return None


def find_ds_id(session, Model, id_) -> Union[DataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = _find_stmt_id(Model, id_)
    r = session.execute(stmt)
    bucket_db = r.scalar()
    if bucket_db:
        return DataBucket(id=bucket_db.id,
                          namespace=bucket_db.namespace,
                          datastore=bucket_db.datastore)
    return None


async def find_ds_id_async(session, Model, id_) -> Union[AIODataBucket, None]:
    """
    Find a datastore to return a DataBucket object
    wich allows to write and read data from the store
    """
    stmt = _find_stmt_id(Model, id_)
    r = await session.execute(stmt)
    bucket_db = r.scalar()
    if bucket_db:
        return AIODataBucket(id=bucket_db.id,
                             namespace=bucket_db.namespace,
                             datastore=bucket_db.datastore)
    return None


def create_bucket(session, Model, ds, ns) -> DataBucket:
    headers = make_agent_headers(agent="dataproc")
    r = http_post(f"{ds}/v1/namespace",
                  json={"name": ns},
                  headers=headers)
    if r.status > 201:
        raise IndexError("Bucket Not found, or conn error")

    stmt = insert(Model.__table__).values(namespace=ns,
                                          datastore=ds)
    stmt = stmt.on_conflict_do_nothing()
    session.execute(stmt)
    session.commit()
    bucket = find_ds(session, Model, ds, ns)
    return bucket
