# cython: language_level=3
# cython: cdivision=True
from cpython.bytes cimport PyBytes_AS_STRING, PyBytes_Check, PyBytes_GET_SIZE
from cpython.pycapsule cimport (PyCapsule_CheckExact, PyCapsule_GetPointer,
                                PyCapsule_New)
from libc.stdint cimport uint8_t, uint64_t

from pyclhash.backends.cython cimport clhash

RANDOM_64BITWORDS_NEEDED_FOR_CLHASH = clhash.RANDOM_64BITWORDS_NEEDED_FOR_CLHASH
RANDOM_BYTES_NEEDED_FOR_CLHASH = clhash.RANDOM_BYTES_NEEDED_FOR_CLHASH

cdef void delkey(object o):
    cdef void* p = PyCapsule_GetPointer(o, NULL)
    # print("delkey", <uint64_t>p)
    clhash.free_key(p)  # origin one does not handle windows condition

cpdef inline object get_random_seed(uint64_t seed1, uint64_t seed2):
    cdef void* p
    with nogil:
        p = clhash.get_random_key_for_clhash(seed1, seed2)
    # print("new", <uint64_t>p)
    if p == NULL:
        raise ValueError("got null")
    return PyCapsule_New(p, NULL, delkey)

cpdef inline uint64_t hash(const uint8_t[::1] data, object seed) except? 0:
    if not PyCapsule_CheckExact(seed) and not PyBytes_Check(seed):
        raise ValueError("invalid seed, should be a capsule or a bytes")
    cdef:
        void * p
        uint64_t ret
    if PyBytes_Check(seed):
        if <int>PyBytes_GET_SIZE(seed) < RANDOM_BYTES_NEEDED_FOR_CLHASH:
            raise ValueError("seed is too short")
        p = <void *>PyBytes_AS_STRING(seed)
    else:
        p = PyCapsule_GetPointer(seed, NULL)
        # print("new", <uint64_t> p)
    with nogil:
        ret = clhash.clhash(p, <char*>&data[0], <size_t>data.shape[0])
    return ret
