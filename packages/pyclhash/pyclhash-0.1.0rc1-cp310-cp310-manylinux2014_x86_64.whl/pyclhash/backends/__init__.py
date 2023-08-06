import os
import platform

impl = platform.python_implementation()


def _should_use_cffi() -> bool:
    ev = os.getenv("CLHASH_USE_CFFI")
    if ev is not None:
        return True
    if impl == "CPython":
        return False
    else:
        return True


if not _should_use_cffi():
    from pyclhash.backends.cython import (
        RANDOM_64BITWORDS_NEEDED_FOR_CLHASH,
        RANDOM_BYTES_NEEDED_FOR_CLHASH,
        get_random_seed,
        hash,
    )
else:
    from pyclhash.backends.cffi import (
        RANDOM_64BITWORDS_NEEDED_FOR_CLHASH,
        RANDOM_BYTES_NEEDED_FOR_CLHASH,
        get_random_seed,
        hash,
    )
