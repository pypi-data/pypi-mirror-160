from datetime import datetime, timedelta

from dataproc.crawlers.models import (DataPagesTaskModel, DataRoots2TaskModel,
                                      DataRootsTaskModel)
from dataproc.datastore import DataBucket
from iso3166 import countries
from sqlalchemy import delete, select


class DataPagesTask:

    @staticmethod
    def save(session, data,
             bucket: DataBucket):

        _country_code = -1
        if data.get("country"):
            _country_code = int(countries.get(data["country"]).numeric)

        task = DataPagesTaskModel(
            taskid=data["taskid"],
            country_code=_country_code,
            lang=data["lang"],
            bucket_id=bucket.id
        )
        # jdata = ujson.dumps(data)

        r = bucket.write(data["taskid"], data, mode="w")
        session.add(task)

        return r

    @staticmethod
    def get_last(session, delta, hours=True, country_code=None):
        if hours:
            last = datetime.utcnow() - timedelta(hours=delta)
        else:
            last = datetime.utcnow() - timedelta(delta)

        stmt = select(DataPagesTaskModel)
        if country_code:
            stmt = stmt.where(DataPagesTaskModel.country_code == country_code)

        stmt = stmt.where(DataPagesTaskModel.created_at > last.isoformat())
        stmt = stmt.order_by(DataPagesTaskModel.created_at)

        rows = session.execute(stmt).scalars()
        return rows

    @staticmethod
    def delete(session, bucket: DataBucket, taskid):

        stmt = delete(DataPagesTaskModel).where(
            DataPagesTaskModel.taskid == taskid)
        session.execute(stmt)
        bucket.delete(taskid)


class DataRootsTask:

    @staticmethod
    def save(session, data,
             bucket: DataBucket):

        _country_code = -1
        if data.get("country"):
            _country_code = int(countries.get(data["country"]).numeric)
        task = DataRootsTaskModel(
            taskid=data["taskid"],
            country_code=_country_code,
            lang=data["lang"],
            bucket_id=bucket.id
        )
        # jdata = ujson.dumps(data)

        r = bucket.write(data["taskid"], data, mode="w")
        session.add(task)
        return r

    @staticmethod
    def get_last_db(session, delta, hours=True, country_code=None):
        if hours:
            last = datetime.utcnow() - timedelta(hours=delta)
        else:
            last = datetime.utcnow() - timedelta(delta)

        stmt = select(DataRootsTaskModel)
        if country_code:
            stmt = stmt.where(DataRootsTaskModel.country_code == country_code)

        stmt = stmt.where(DataRootsTaskModel.created_at > last.isoformat())
        stmt = stmt.order_by(DataRootsTaskModel.created_at)

        rows = session.execute(stmt).scalars()
        return rows

    @classmethod
    def get_last(cls, session, delta, hours=True, country_code=None):
        rows = cls.get_last_db(session, delta, hours, country_code)
        root_tasks = [r.to_dict() for r in rows]
        roots = []
        for task in root_tasks:
            bucket_root = DataBucket(
                task["bucket"]["id"], task["bucket"]["namespace"], task["bucket"]["datastore"]
            )
            data = bucket_root.read(task["taskid"]).json()
            roots.append(data)
        return roots

    @staticmethod
    def delete(session, bucket: DataBucket, taskid):

        stmt = delete(DataRootsTaskModel).where(
            DataRootsTaskModel.taskid == taskid)
        session.execute(stmt)
        bucket.delete(taskid)


class DataRootsTask2:

    @staticmethod
    def save(session, data,
             bucket: DataBucket, lbl):

        _country_code = -1
        if data.get("country"):
            _country_code = int(countries.get(data["country"]).numeric)
        task = DataRoots2TaskModel(
            taskid=data["taskid"],
            country_code=_country_code,
            label_id=lbl.id,
            lang=data["lang"],
            bucket_id=bucket.id
        )
        # jdata = ujson.dumps(data)

        r = bucket.write(data["taskid"], data, mode="w")
        session.add(task)
        return r

    @staticmethod
    def get_last_db(session, delta, hours=True, country_code=None, label_id=None):
        if hours:
            last = datetime.utcnow() - timedelta(hours=delta)
        else:
            last = datetime.utcnow() - timedelta(delta)

        stmt = select(DataRoots2TaskModel)
        if country_code:
            stmt = stmt.where(DataRoots2TaskModel.country_code == country_code)
        if label_id:
            stmt = stmt.where(DataRoots2TaskModel.label_id == label_id)

        stmt = stmt.where(DataRoots2TaskModel.created_at > last.isoformat())
        stmt = stmt.order_by(DataRoots2TaskModel.created_at)

        rows = session.execute(stmt).scalars()
        return rows

    @classmethod
    def get_last(cls, session, delta, hours=True, country_code=None, label_id=None):
        rows = cls.get_last_db(session, delta, hours, country_code, label_id)
        root_tasks = [r.to_dict() for r in rows]
        roots = []
        for task in root_tasks:
            bucket_root = DataBucket(
                task["bucket"]["id"], task["bucket"]["namespace"], task["bucket"]["datastore"]
            )
            data = bucket_root.read(task["taskid"]).json()
            roots.append(data)
        return roots

    @staticmethod
    def delete(session, bucket: DataBucket, taskid):

        stmt = delete(DataRoots2TaskModel).where(
            DataRoots2TaskModel.taskid == taskid)
        session.execute(stmt)
        bucket.delete(taskid)
