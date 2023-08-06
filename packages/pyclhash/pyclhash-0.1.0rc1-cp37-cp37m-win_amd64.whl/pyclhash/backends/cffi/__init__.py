"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
from _cffi_backend import _CDataBase

from pyclhash.backends.cffi._hash_cffi import ffi, lib

RANDOM_64BITWORDS_NEEDED_FOR_CLHASH = lib.RANDOM_64BITWORDS_NEEDED_FOR_CLHASH
RANDOM_BYTES_NEEDED_FOR_CLHASH = lib.RANDOM_BYTES_NEEDED_FOR_CLHASH


class Key:
    """simulate pycapsule"""

    def __init__(self, p):
        self.p = p

    def __del__(self):
        lib.free_key(self.p)


def get_random_seed(seed1: int, seed2: int):
    p = lib.get_random_key_for_clhash(seed1, seed2)
    if p == ffi.NULL:
        raise ValueError("got null")
    return Key(p)


def hash(data: bytes, seed: object):
    if isinstance(seed, Key):
        p = seed.p  # void*
    else:
        if len(seed) < RANDOM_BYTES_NEEDED_FOR_CLHASH:
            raise ValueError("seed is too short")
        p = ffi.cast("void*", ffi.from_buffer(seed))

    ret = lib.clhash(p, ffi.from_buffer(data), len(data))
    return ret
