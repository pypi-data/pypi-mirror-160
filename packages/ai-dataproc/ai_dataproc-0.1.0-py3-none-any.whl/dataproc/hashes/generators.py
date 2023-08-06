import binascii
import os
import struct
import sys
import time
from dataclasses import dataclass
import random
import string


def random_str(len_=16):
    """ Simple string generator """
    return ''.join(random.choice(
        string.ascii_uppercase + string.ascii_lowercase + string.digits)
                   for _ in range(len_))



@dataclass
class SiteID:
    id: int
    id_str: str
    id_bytes: bytes


class SiteHash64:
    """
    A random id generator based on instagram and pinteres way
    """

    _modulo = 2**13
    __slots__ = ('__id', '_epoch', '_doc_type')

    def __init__(self, doc_type, custom_epoch, site_id=None):
        """ Initialize a new SiteHash64 id based on ObjectID from mongodb.

        This id will be 64 bits long.

        [ doc_type -> 10 bits, timestamp -> 41 bits, random -> 13 bits ]
        """
        self._epoch = custom_epoch
        # self._doc_type = doc_type

        if site_id is None:
            self.__generate(doc_type)
        elif isinstance(site_id, bytes) and len(site_id) == 8:
            self.__id = site_id
        else:
            raise TypeError("id must be an instance of (bytes)"
                            "not %s" % (type(site_id),))

    def __generate(self, doc_type: int):
        """Generate a new value for SiteHash64
        8 bytes long.

        """

        # 10 bits type of the site
        # doc_type

        # 41 bits timestamp with a custom epoch
        ts = int((time.time() - self._epoch) * 1000)

        # 13 bits a random number
        _rand = int.from_bytes(os.urandom(20), 'big')
        rand = (_rand % (2**13))

        _int_id = (doc_type << 54) | (ts << 13) | (rand << 0)

        site_id = struct.pack(">Q", _int_id)

        self.__id = site_id

    # def generate(self, doc_type) -> SiteID:
    #    _id = self.__generate(doc_type)
    #    return SiteID(_id, str(_id), _id.to_bytes(8, byteorder=sys.byteorder))

    @property
    def binary(self):
        """12-byte binary representation of this ObjectId.
        """
        return self.__id

    @property
    def integer(self):
        return int(str(self), 16)

    @property
    def doc_type(self):
        return self.integer >> 54

    @property
    def generation_time(self):
        # 0x1FFFFFFFFFF == format((2**41) - 1, 'X')
        return (self.integer >> 13) & 0x1FFFFFFFFFF

    def __str__(self):
        """ hexadecimal representation """
        return binascii.hexlify(self.__id).decode()

    def __repr__(self):
        return "SiteHash64('%s')" % (str(self),)

    def __eq__(self, other):
        if isinstance(other, SiteHash64):
            return self.__id == other.binary
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, SiteHash64):
            return self.__id != other.binary
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, SiteHash64):
            return self.__id < other.binary
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, SiteHash64):
            return self.__id <= other.binary
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, SiteHash64):
            return self.__id > other.binary
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, SiteHash64):
            return self.__id >= other.binary
        return NotImplemented

    def __hash__(self):
        return hash(self.__id)


@dataclass
class Hash96:
    id_int: int
    id_hex: str

    @classmethod
    def time_random_string(cls):
        """
        It generates a random string based on a time epoch
        an a random number.
        It's a 96 bit long

        """
        # 41 bits timestamp with a custom epoch
        ts = int(time.time())
        # 55 bits a random number
        num = int.from_bytes(os.urandom(90), 'big') % 2**55
        _int_id = (ts << 55) | (num << 0)
        _bytes = _int_id.to_bytes(12, 'big')
        _bytes_id = binascii.hexlify(_bytes).decode()

        return cls(id_int=_int_id, id_hex=_bytes_id)
