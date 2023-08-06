import base64
import sys
from dataclasses import dataclass

import xxhash
from cityhash import CityHash64


def int2bytes(number: int, length: int, byteorder=sys.byteorder) -> bytes:
    """ converts int to bytes"""
    b = number.to_bytes(length, byteorder=byteorder)
    return b


@dataclass
class Digest:
    hexdigest: str
    intdigest: int
    bytesdigest: bytes


class Hasher:

    @staticmethod
    def city64(txt: str) -> Digest:
        """ a wrapper of cityhash """
        _hash = CityHash64(txt)
        _hex = format(_hash, 'x')
        _int = _hash
        _bytes = int2bytes(_hash, 8, byteorder="big")
        return Digest(_hex, _int, _bytes)

    @staticmethod
    def xxhash64(txt: str) -> Digest:
        """ a wrapper of xxhash
        """
        _hash = xxhash.xxh64(txt)
        _int = _hash.intdigest()
        _hex = _hash.hexdigest()
        _bytes = _hash.digest()

        return Digest(_hex, _int, _bytes)


"""
base64's `urlsafe_b64encode` uses '=' as padding.
These are not URL safe when used in URL paramaters.
Functions below work around this to strip/add back in padding.
See:
https://docs.python.org/2/library/base64.html
https://mail.python.org/pipermail/python-bugs-list/2007-February/037195.html
"""


def base64_encode(data: bytes) -> bytes:
    """
    Removes any `=` used as padding from the encoded string.
    """
    encoded = base64.urlsafe_b64encode(data)
    return encoded.rstrip(b"=")


def base64_decode(string: str) -> bytes:
    """
    Adds back in the required padding before decoding.
    """
    padding = 4 - (len(string) % 4)
    string = string + ("=" * padding)
    return base64.urlsafe_b64decode(string)
