"""
Copyright (c) 2008-2022 synodriver <synodriver@gmail.com>
"""
from cffi import FFI

ffibuilder = FFI()
ffibuilder.cdef(
    """
enum {RANDOM_64BITWORDS_NEEDED_FOR_CLHASH=133,RANDOM_BYTES_NEEDED_FOR_CLHASH=133*8};



/**
 *  random : the random data source (should contain at least
 *  RANDOM_BYTES_NEEDED_FOR_CLHASH random bytes), it should
 *  also be aligned on 16-byte boundaries so that (((uintptr_t) random & 15) == 0)
 *  for performance reasons. This is usually generated once and reused with many
 *  inputs.
 *
 *
 * stringbyte : the input data source, could be anything you want to has
 *
 *
 * length : number of bytes in the string
 */
uint64_t clhash(const void* random, const char * stringbyte,
                const size_t lengthbyte);



/**
 * Convenience method. Will generate a random key from two 64-bit seeds.
 * Caller is responsible to call "free" on the result.
 */
void * get_random_key_for_clhash(uint64_t seed1, uint64_t seed2);

/*free the key*/
void free_key(void *key);
    """
)

source = """
#include "clhash.h"
"""

ffibuilder.set_source(
    "pyclhash.backends.cffi._hash_cffi",
    source,
    sources=["./dep/src/clhash.c"],
    include_dirs=["./dep/include"],
)

if __name__ == "__main__":
    ffibuilder.compile()
