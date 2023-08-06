# cython: language_level=3
# cython: cdivision=True
from libc.stdint cimport uint64_t


cdef extern from "clhash.h" nogil:
    int RANDOM_64BITWORDS_NEEDED_FOR_CLHASH
    int RANDOM_BYTES_NEEDED_FOR_CLHASH
    uint64_t clhash(void * random, char * stringbyte,
                    size_t lengthbyte)
    void * get_random_key_for_clhash(uint64_t seed1, uint64_t seed2)
    void free_key(void *key)