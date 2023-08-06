from dataclasses import dataclass
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

import fsspec
import pyarrow as pa
import pyarrow.parquet as pq
import requests
from dataproc.datasets.models import TableModel
from hashes.generators import Hash96
from sqlalchemy import delete, select
from webdav4.fsspec import WebdavFileSystem


@dataclass
class TableMeta:
    format_: str
    protocol: str
    dataset_id: int
    depends_on: Optional[List[str]] = None


class Table:

    _PROTOCOLS = ["webdav", "fileserver"]
    _FORMATS = ["parquet"]

    def __init__(self, table, meta: TableMeta, tableid: str):
        self.table = table
        self.meta = meta
        self.tableid = tableid

    @staticmethod
    def _tableid():
        return Hash96.time_random_string().id_hex

    @classmethod
    def from_pandas(cls, df, meta: TableMeta, tableid=None):
        if not tableid:
            tableid = cls._tableid()

        if meta.format_ == "parquet":
            t = pa.Table.from_pandas(df)
            return cls(t, meta, tableid)

        raise TypeError("Format not implemented")

    @staticmethod
    def get_one(session, tableid) -> TableModel:
        stmt = select(TableModel).where(TableModel.tableid == tableid)
        result = session.execute(stmt)
        row: TableModel = result.fetchone()[0]
        return row

    @classmethod
    def from_tableid(cls, session, tableid):
        row = cls.get_one(session, tableid)
        if row.protocol == "webdav":
            u = urlparse(row.base_location)
            webdav = f"{u.scheme}://{u.netloc}"
            where = f"{u.path}/{row.tableid}.{row.data_format}"

            tbl = cls.read_webdav(webdav, where)

        elif row.protocol == "fileserver":
            u = urlparse(row.base_location)
            # fileserver = f"{u.scheme}://{u.netloc}"
            where = f"{row.base_location}/{row.tableid}.{row.data_format}"
            tbl = cls.read_fileserver(u.scheme, where)

        meta = TableMeta(
            format_=row.data_format,
            protocol=row.protocol,
            dataset_id=row.dataset_id,
            depends_on=row.depends_on
        )
        return cls(
            tbl, meta, row.tableid
        )

    @classmethod
    def delete(cls, session, tableid):

        row = cls.get_one(session, tableid)
        u = urlparse(row.base_location)
        webdav = f"{u.scheme}://{u.netloc}"
        where = f"{u.path}/{row.tableid}.{row.data_format}"

        fs = WebdavFileSystem(webdav)
        fs.delete(where)

        stmt = delete(TableModel.__table__)\
            .where(TableModel.__table__.c.tableid == tableid)
        session.execute(stmt)

    @staticmethod
    def read_webdav(srv, path):
        fs = WebdavFileSystem(srv)
        tbl = pq.read_table(path, filesystem=fs)
        return tbl

    @staticmethod
    def read_fileserver(scheme, fullpath):
        fs = fsspec.filesystem(scheme)
        tbl = pq.read_table(fullpath, filesystem=fs)
        return tbl

    def write(self, session, remote_path):
        if self.meta.protocol == "webdav":
            base_location = self.write_to_webdav(remote_path)
        elif self.meta.protocol == "fileserver":
            base_location = self.write_to_fileserver(remote_path)

        table = TableModel(
            tableid=self.tableid,
            protocol=self.meta.protocol,
            base_location=base_location,
            data_format=self.meta.format_,
            depends_on=self.meta.depends_on,
            dataset_id=self.meta.dataset_id,
            created_at=datetime.utcnow(),
        )
        session.add(table)

        return self.tableid

    def write_to_webdav(self, remote_path):
        u = urlparse(remote_path)
        webdav = f"{u.scheme}://{u.netloc}"
        where = f"{u.path}/{self.tableid}.{self.meta.format_}"

        fs = WebdavFileSystem(webdav)

        pq.write_table(self.table, where=where, filesystem=fs)

        return f"{webdav}{u.path}"

    def write_to_fileserver(self, remote_path):
        # pq.write_table(self.table, out_buffer)
        u = urlparse(remote_path)
        filesrv = f"{u.scheme}://{u.netloc}"
        where = f"{u.path}/{self.tableid}.{self.meta.format_}"
        out_buffer = BytesIO()
        pq.write_table(self.table, out_buffer)
        requests.put(f"{filesrv}/{where}", data=out_buffer.getvalue())

        return f"{filesrv}{u.path}"

    def write_to_local(self, path, format_="parquet"):
        pass
