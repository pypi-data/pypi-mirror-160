from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from dataproc.datasets.models import DatasetModel, TagModel, TableModel
from hashes.generators import Hash96
from sqlalchemy import select
from sqlalchemy.orm import selectinload


@dataclass
class DatasetMeta:
    name: str
    # format_: str
    tags: Union[List[str], None]
    meta: Union[Dict[str, Any], None]
    datasetid: Optional[str] = None
    country: Optional[str] = None
    lang: Optional[str] = None

@dataclass
class TableMeta:
    location: str
    format_: str
    protocol: str
    datasetid: str
    tableid: Optional[str] = None
    depends_on: Optional[List[str]] = None


def create_dataset(session, dm: DatasetMeta):
    id_ = dm.datasetid or Hash96.time_random_string().id_hex
    dm_db = DatasetModel(
        datasetid=id_,
        name=dm.name,
        meta_desc=dm.meta,
        lang=dm.lang,
        country=dm.country
    )
    if dm.tags:
        for tag_name in dm.tags:
            tag = get_or_create_tag(session, tag_name)
            dm_db.tags.append(tag)

    session.add(dm_db)
    return dm_db


def get_or_create_tag(session, name) -> TagModel:
    stmt = select(TagModel).where(TagModel.name == name)
    tag = session.execute(stmt).scalar()
    if tag:
        return tag
    return create_tag(session, name)


def create_tag(session, name: str) -> TagModel:
    t = TagModel(name=name)
    session.add(
        t
    )
    return t


async def get_tag(session, name: str) -> TagModel:
    stmt = select(TagModel).options(selectinload(TagModel.datasets))\
                           .where(TagModel.name == name)
    result = await session.execute(stmt)
    row = result.scalar()
    return row
