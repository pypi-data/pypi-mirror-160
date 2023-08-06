from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_mixin, declared_attr


@declarative_mixin
class DatastoreMixin:
    # pylint: disable=too-few-public-methods

    __mapper_args__ = {"eager_defaults": True}

    id = Column(Integer, primary_key=True)
    namespace = Column(String(length=512), nullable=False)
    datastore = Column(String(length=1024), index=True, nullable=False)
    # code = Column(BigInteger, index=True, unique=True, nullable=False)
    created_at = Column(DateTime(),
                        default=datetime.utcnow(),
                        nullable=False)

    @declared_attr
    def __table_args__(cls):
        return (UniqueConstraint(
            'namespace', 'datastore', name=f"{cls.__tablename__.lower()}_ns_ds"),)
