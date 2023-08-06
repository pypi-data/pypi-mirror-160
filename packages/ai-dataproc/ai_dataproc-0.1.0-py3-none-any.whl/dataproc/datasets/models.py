from datetime import datetime

from db.common import Base
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text)
# from sqlalchemy.dialects.postgresql import ARRAY, BYTEA, JSONB
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table
from sqlalchemy_serializer import SerializerMixin

datasets_tags = Table('dataset_tag', Base.metadata,
                      Column('id', BigInteger, primary_key=True),
                      Column('tag_id', ForeignKey('datasets_tag.id')),
                      Column('dataset_id', ForeignKey(
                          'datasets_dataset.id'))
                      )


class TagModel(Base, SerializerMixin):
    __tablename__ = 'datasets_tag'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(), unique=True, nullable=False, index=True)
    # datasets = relationship("DatasetModel",
    #                        secondary=datasets_tags,
    #                        back_populates="tags"
    #                        )


class DatasetModel(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = 'datasets_dataset'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(BigInteger, primary_key=True)
    datasetid = Column(String(24), index=True)
    name = Column(String(), index=True, nullable=False)
    tags = relationship(
        "TagModel", secondary=datasets_tags)
    meta_desc = Column(JSONB())
    lang = Column(String(2), nullable=True)
    country = Column(String(2), nullable=True)
    # code = Column(BigInteger, index=True, unique=True, nullable=False)
    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)


class TableModel(Base, SerializerMixin):
    # pylint: disable=too-few-public-methods
    __tablename__ = 'datasets_table'
    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    tableid = Column(String(24), index=True, unique=True)
    protocol = Column(String(), nullable=False)
    base_location = Column(String(), nullable=False)
    data_format = Column(String(16), nullable=False)
    depends_on = Column(ARRAY(String(length=24)), nullable=True)
    dataset_id = Column(BigInteger, ForeignKey(
        'datasets_dataset.id', ondelete='SET NULL'))
    # dataset = relationship("DatasetModel", backref="tables")
    dataset = relationship("DatasetModel")

    # taskid = Column(String(24), index=True)

    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)
