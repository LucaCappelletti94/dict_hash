"""Tests for the Hashable class."""

from time import time
import pytest
from dict_hash import Hashable, validate_consistent_hash, sha256


class MyHashable(Hashable):
    """A class that implements the consistent_hash method."""

    def __init__(self, a: int):
        self._a = a
        self._time = time()

    def consistent_hash(self, use_approximation: bool = False) -> str:
        if use_approximation:
            return sha256({"a": self._a}, use_approximation=True)
        return sha256({"a": self._a})


class MyDeprecatedHashable(Hashable):
    """A class that implements the consistent_hash method."""

    def __init__(self, a: int):
        self._a = a
        self._time = time()

    def consistent_hash(self) -> str:
        return sha256({"a": self._a})


def test_hashable():
    """Test the Hashable class."""
    with pytest.raises((NotImplementedError, TypeError)):
        Hashable().consistent_hash()

    a = MyHashable(2)
    b = MyHashable(2)
    c = MyHashable(3)
    assert validate_consistent_hash(a, b)
    assert validate_consistent_hash(b, a)
    assert not validate_consistent_hash(a, c)
    assert not validate_consistent_hash(b, c)

    assert sha256({"my_hashable": a}) == sha256({"my_hashable": b})


def test_deprecated_hashable():
    """Test that the deprecated Hashable gets the appropriate warning."""
    with pytest.warns(DeprecationWarning):
        a = MyDeprecatedHashable(2)
        b = MyDeprecatedHashable(2)
        c = MyDeprecatedHashable(3)
        assert validate_consistent_hash(a, b)
        assert validate_consistent_hash(b, a)
        assert not validate_consistent_hash(a, c)
        assert not validate_consistent_hash(b, c)

        assert sha256({"my_hashable": a}) == sha256({"my_hashable": b})
