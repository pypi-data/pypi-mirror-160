import binascii
import struct
from typing import Tuple

from hashes.noncrypto import base64_encode


class NewsID:
    """
    A ID of 12 bytes long
    This id is compose by:
    [8 bytes of Site.id][4 bytes of crc32(News.fullurl)]
    """
    __slots__ = ('__id', '_site', '_url')

    def __init__(self, siteid: int, fullurl: int):
        self._site = struct.pack(">q", siteid)  # signed 8 bits long
        self._url = struct.pack(">I", fullurl)  # unsigned 4 bits long
        self._set_id()

    def _set_id(self):
        self.__id = self._site + self._url

    @property
    def idbytes(self) -> bytes:
        return self.__id

    @property
    def idhex(self) -> str:
        return str(self)

    @property
    def idint(self) -> int:
        return int.from_bytes(self.__id, byteorder='big')

    @property
    def base64(self) -> bytes:
        return base64_encode(self.__id)

    @classmethod
    def unpack(cls, newsid: bytes) -> Tuple[int, int]:
        """
        Restore from bytes into siteid and url
        """
        assert len(newsid) == 12
        _siteid = int.from_bytes(newsid[0:8], byteorder='big')
        _url = int.from_bytes(newsid[8:12], byteorder='big')
        return (_siteid, _url)

    def __str__(self):
        return binascii.hexlify(self.__id).decode()

    def __repr__(self):
        return "NewsId('%s')" % (str(self),)
