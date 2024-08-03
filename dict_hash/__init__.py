"""Python package for hashing dictionaries and other objects."""

from dict_hash.dict_hash import (
    md5,
    sha256,
    sha1,
    sha224,
    sha384,
    sha512,
    sha3_512,
    shake_128,
    shake_256,
    sha3_384,
    sha3_256,
    sha3_224,
    blake2s,
    blake2b,
    dict_hash,
    NotHashableException,
    NotHashableWarning,
)
from dict_hash.hashable import Hashable
from dict_hash.validate_consistent_hash import validate_consistent_hash

ALL_AVAILABLE_HASHES = [
    md5,
    sha1,
    sha224,
    sha256,
    sha384,
    sha512,
    sha3_224,
    sha3_256,
    sha3_384,
    sha3_512,
    shake_128,
    shake_256,
    blake2s,
    blake2b,
]

__all__ = [
    "md5",
    "sha256",
    "sha1",
    "sha224",
    "sha384",
    "sha512",
    "sha3_512",
    "shake_128",
    "shake_256",
    "sha3_384",
    "sha3_256",
    "sha3_224",
    "blake2s",
    "blake2b",
    "ALL_AVAILABLE_HASHES",
    "dict_hash",
    "Hashable",
    "validate_consistent_hash",
    "NotHashableException",
    "NotHashableWarning",
]
