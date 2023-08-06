import pyarrow.plasma as plasma

from dataproc.conf import Config


def init(plasma_dir=Config.PLASMA_DIR) -> plasma.PlasmaClient:
    client = plasma.connect(plasma_dir)
    return client


def plasmaid2object(id_str: str) -> plasma.ObjectID:
    object_id = plasma.ObjectID(bytes.fromhex(id_str))
    return object_id
