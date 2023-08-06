from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from dataproc.datasets.models import DatasetModel, TableModel, TagModel
from dataproc.datasets.table import Table
from hashes.generators import Hash96
from sqlalchemy import select
from sqlalchemy.orm import selectinload


@dataclass
class TableRef:
    id: int
    tableid: str
    created_at: str


@dataclass
class DatasetMeta:
    name: str
    # format_: str
    tags: Union[List[str], None]
    meta: Union[Dict[str, Any], None]
    id: Union[int, None]
    datasetid: Optional[str] = None
    country: Optional[str] = None
    lang: Optional[str] = None
    tables: Optional[List[TableRef]] = None
    created_at: Optional[str] = None


def create_tag(session, name: str) -> TagModel:
    t = TagModel(name=name)
    session.add(
        t
    )
    return t


class Dataset:

    def __init__(self, dm: DatasetMeta):
        assert isinstance(dm.id, int)
        self.dm = dm

    @staticmethod
    def get_or_create_tag(session, name):
        stmt = select(TagModel).where(TagModel.name == name)
        tag = session.execute(stmt).scalar()
        if tag:
            return tag
        return create_tag(session, name)

    @classmethod
    def from_datasetid(cls, session, datasetid):
        stmt = select(DatasetModel).where(DatasetModel.datasetid == datasetid)
        result = session.execute(stmt).fetchone()
        row = result[0]
        dm = DatasetMeta(
            id=row.id,
            name=row.name,
            tags=[t.name for t in row.tags],
            datasetid=row.datasetid,
            meta=row.meta_desc,
            lang=row.lang,
            country=row.country,
            created_at=row.created_at.isoformat()
        )
        return cls(dm)

    @classmethod
    def from_name(cls, session, name):
        stmt = select(DatasetModel).where(DatasetModel.name == name)
        result = session.execute(stmt).fetchone()
        row = result[0]
        dm = DatasetMeta(
            id=row.id,
            name=row.name,
            tags=[t.name for t in row.tags],
            datasetid=row.datasetid,
            meta=row.meta_desc,
            lang=row.lang,
            country=row.country,
            created_at=row.created_at.isoformat()
        )
        return cls(dm)

    @staticmethod
    def list_(session, include_tables=False,
              filter_tags: Optional[List[str]] = None) -> List[DatasetMeta]:

        stmt = select(DatasetModel)
        if filter_tags:
            stmt = select(DatasetModel)\
                .join(DatasetModel.tags)\
                .where(TagModel.name.in_(filter_tags))

        rows = session.execute(stmt).scalars()

        datasets = []
        for r in rows:
            dm = DatasetMeta(
                id=r.id,
                datasetid=r.datasetid,
                name=r.name,
                tags=[t.name for t in r.tags],
                meta=r.meta_desc,
                country=r.country,
                lang=r.lang,
                created_at=r.created_at.isoformat()
            )
            if include_tables:
                stmt = select(TableModel).where(TableModel.dataset_id == r.id)
                tables_db = session.execute(stmt).scalars()
                tables = []
                for tbl in tables_db:
                    ref = TableRef(
                        id=tbl.id,
                        tableid=tbl.tableid,
                        created_at=tbl.created_at.isoformat())
                    tables.append(ref)
                dm.tables = tables
            datasets.append(dm)
        return datasets

    @staticmethod
    def get_table(session, tableid) -> Table:
        return Table.from_tableid(session, tableid)

    def get_last_tables_ref(self, session, limit=1) -> List[TableRef]:
        stmt = select(TableModel)\
            .where(TableModel.dataset_id == self.dm.id)\
            .order_by(TableModel.created_at.desc())\
            .limit(limit)
        results = session.execute(stmt).scalars()
        tables = []
        for tbl in results:
            ref = TableRef(
                id=tbl.id,
                tableid=tbl.tableid,
                created_at=tbl.created_at.isoformat())
            tables.append(ref)
        return tables


def create_dataset(session, name: str,
                   tags: Union[List[str], None],
                   meta: Union[Dict[str, Any], None],
                   datasetid: Optional[str] = None,
                   country: Optional[str] = None,
                   lang: Optional[str] = None
                   ) -> Dataset:

    id_ = datasetid or Hash96.time_random_string().id_hex
    model = DatasetModel(
        datasetid=id_,
        name=name,
        meta_desc=meta,
        lang=lang,
        country=country
    )
    if tags:
        for tag_name in tags:
            tag = Dataset.get_or_create_tag(session, tag_name)
            model.tags.append(tag)

    session.add(model)
    session.commit()
    dataset = DatasetMeta(
        id=model.id,
        name=name,
        datasetid=id_,
        tags=tags,
        meta=meta,
        lang=lang,
        country=country,
        created_at=model.created_at.isoformat()
    )

    return Dataset(dataset)
