from datetime import datetime

from dataproc.datastore.base_model import DatastoreMixin
from db.common import Base, MutableList
# from hashes.generators import Hash96
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, SmallInteger, String, UniqueConstraint)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


class SocialBucketModel(Base, SerializerMixin, DatastoreMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = "social_bucket"


class TweetTrendModel(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    """ It keeps a register of the tweets related to a trend """
    __tablename__ = 'social_tweet_trend'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    name = Column(String(), index=True, nullable=False)
    # hash96
    taskid = Column(String(24), index=True)
    bucket_id = Column(BigInteger, ForeignKey(
        'social_bucket.id', ondelete='SET NULL'))
    bucket = relationship("SocialBucketModel")
    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)

    __table_args__ = (UniqueConstraint(
        'taskid', 'name', name='_taskid_name_tweet'),)


class TweetTrendTask(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    """ hashtags and words related to a specific moment and woeid"""
    __tablename__ = 'social_tweet_trend_task'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    # hash96
    taskid = Column(String(24), index=True, unique=True)
    words = Column(MutableList.as_mutable(
        ARRAY(String(length=1024))), nullable=True)

    bucket_id = Column(BigInteger, ForeignKey(
        'social_bucket.id', ondelete='SET NULL'))
    bucket = relationship("SocialBucketModel")

    lang = Column(String(length=2), nullable=True)
    woeid = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)


class GoogleTrendTask(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    """ hashtags and words related to a specific moment and woeid"""
    __tablename__ = 'social_google_trend_task'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    # hash96
    taskid = Column(String(24), index=True, unique=True)
    words = Column(MutableList.as_mutable(
        ARRAY(String(length=1024))), nullable=True)

    bucket_id = Column(BigInteger, ForeignKey(
        'social_bucket.id', ondelete='SET NULL'))
    bucket = relationship("SocialBucketModel")

    lang = Column(String(length=2), nullable=True)
    country_code = Column(Integer, nullable=False, index=True)

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)
