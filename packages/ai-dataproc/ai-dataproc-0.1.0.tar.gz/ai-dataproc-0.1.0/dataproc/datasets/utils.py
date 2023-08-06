import enum
import io
import sys

import pyarrow as pa
import pyarrow.parquet as pq
from webdav4.fsspec import WebdavFileSystem


class SIZE_UNIT(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    """Convert the size from bytes to other units like KB, MB or GB"""
    if unit == SIZE_UNIT.KB:
        return size_in_bytes / 1024
    elif unit == SIZE_UNIT.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == SIZE_UNIT.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def parquet_size(df, unit):
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    values = buffer.getvalue()
    size = sys.getsizeof(values)
    return convert_unit(size, unit)


def sizeof_mb(obj):
    return round(sys.getsizeof(obj) / (1024 * 1024), 2)


def from_pandas2webdav(webdav, fullpath, df):
    t = pa.Table.from_pandas(df)
    write_table_webdav(webdav, fullpath, t)
    return t


def write_table_webdav(webdav, fullpath, table):
    fs = WebdavFileSystem(webdav)
    pq.write_table(table, where=fullpath, filesystem=fs)


# size = convert_unit(sys.getsizeof(values), SIZE_UNIT.MB)
