import pytest
from time import time
from dict_hash import Hashable, validate_consistent_hash, sha256, NotHashableException


class MyHashable(Hashable):

    def __init__(self, a: int):
        self._a = a
        self._time = time()

    def consistent_hash(self) -> str:
        return sha256({
            "a": self._a
        })


class NotHashable:

    @property
    def consistent_hash(self) -> str:
        raise NotHashableException()


def test_hashable():
    with pytest.raises(NotImplementedError):
        Hashable().consistent_hash()

    a = MyHashable(2)
    b = MyHashable(2)
    c = MyHashable(3)
    assert validate_consistent_hash(a, b)
    assert validate_consistent_hash(b, a)
    assert not validate_consistent_hash(a, c)
    assert not validate_consistent_hash(b, c)

    assert sha256({
        "my_hashable": a
    }) == sha256({
        "my_hashable": b
    })


def test_not_hashable():
    with pytest.raises(NotHashableException):
        sha256({"a": NotHashable()})