from datetime import datetime

from dataproc.datastore.base_model import DatastoreMixin
from db.common import Base, MutableList
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
# from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, JSONB
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class CrawlerBucketModel(Base, SerializerMixin, DatastoreMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = "crawlers_bucket"


class SiteLabelModel(Base, SerializerMixin):
    __tablename__ = 'crawlers_sitelabel'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)

    # sites = relationship("Site", backref="crawlers_typesite")

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)


class SiteModel(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = 'crawlers_site'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    # xxhash
    siteid = Column(String(16), index=True, unique=True)
    # https://www.lanacion.com/ lanacion.com
    urlnorm = Column(String(),
                     nullable=False)
    basename = Column(String(),
                      index=True, nullable=False)
    secure = Column(Boolean, nullable=False, default=True)
    www = Column(Boolean, nullable=False, default=True)
    # hasrss = Column(Boolean, default=False)
    feedurls = Column(MutableList.as_mutable(
        ARRAY(String(length=1024))), nullable=True)
    socials = Column(MutableList.as_mutable(
        ARRAY(String(length=1024))), nullable=True)
    # description = Column(Text, nullable=True)
    country = Column(Integer,
                     index=True, nullable=True)

    lang = Column(String(length=6),
                  index=True, nullable=True)

    bucket_id = Column(BigInteger, ForeignKey(
        'crawlers_bucket.id', ondelete='SET NULL'))
    bucket = relationship("CrawlerBucketModel")

    label_id = Column(Integer, ForeignKey(
        'crawlers_sitelabel.id', ondelete='set null'))
    label = relationship("SiteLabelModel")

    # urls = relationship("URL", backref="crawl_site")

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False, index=True)
    updated_at = Column(DateTime(),
                        default=datetime.utcnow())


class URLModel(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = 'crawlers_url'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    docid = Column(String(16), index=True, unique=True)
    fullurl = Column(String(),
                     nullable=False)
    # text = Column(String(), nullable=False)

    # lang = Column(String(length=6),
    #             index=True, nullable=True)

    # label_id = Column(Integer, ForeignKey(
    #    'crawlers_sitelabel.id', ondelete='set null'))
    # label = relationship("SiteLabelModel")

    bucket_id = Column(BigInteger, ForeignKey(
        'crawlers_bucket.id', ondelete='SET NULL'))
    bucket = relationship("CrawlerBucketModel")

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False, index=True)


class PageModel(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = "crawlers_page"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    docid = Column(String(16), index=True, unique=True)
    siteid = Column(String(16), index=True)
    urlnorm = Column(String)
    www = Column(Boolean)
    secure = Column(Boolean)
    lang = Column(String(length=6),
                  index=True, nullable=True)

    bucket_id = Column(BigInteger, ForeignKey(
        'crawlers_bucket.id', ondelete='SET NULL'))
    bucket = relationship("CrawlerBucketModel")

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False, index=True)
    updated_at = Column(DateTime(),
                        default=datetime.utcnow())


class DataRootsTaskModel(Base, SerializerMixin):
    __tablename__ = 'crawlers_data_roots_task'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    # hash96
    taskid = Column(String(24), index=True, unique=True)
    bucket_id = Column(BigInteger, ForeignKey(
        'crawlers_bucket.id', ondelete='SET NULL'))
    bucket = relationship("CrawlerBucketModel")

    lang = Column(String(length=6), nullable=True)
    country_code = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)


class DataRoots2TaskModel(Base, SerializerMixin):
    __tablename__ = 'crawlers_data_roots2_task'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    # hash96
    taskid = Column(String(24), index=True, unique=True)
    bucket_id = Column(BigInteger, ForeignKey(
        'crawlers_bucket.id', ondelete='SET NULL'))
    bucket = relationship("CrawlerBucketModel")

    lang = Column(String(length=6), nullable=True)
    country_code = Column(Integer, nullable=False, index=True)

    label_id = Column(Integer, ForeignKey(
        'crawlers_sitelabel.id', ondelete='set null'))
    label = relationship("SiteLabelModel")

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)


class DataPagesTaskModel(Base, SerializerMixin):
    __tablename__ = 'crawlers_data_pages_task'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    # hash96
    taskid = Column(String(24), index=True, unique=True)
    bucket_id = Column(BigInteger, ForeignKey(
        'crawlers_bucket.id', ondelete='SET NULL'))
    bucket = relationship("CrawlerBucketModel")

    lang = Column(String(length=6), nullable=True)
    country_code = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)
