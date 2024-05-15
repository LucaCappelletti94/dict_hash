"""Test to check that the behaviour_on_error parameter works as expected."""

import pytest
from dict_hash import sha256, dict_hash, NotHashableException, NotHashableWarning
from .utils import create_dict, NotHashable, RecursiveObject


def test_behaviour_on_error_ignore():
    """Test that the behaviour_on_error parameter works as expected."""
    d = create_dict()
    d["not_hashable"] = NotHashable()
    assert dict_hash(d, behavior_on_error="ignore") == dict_hash(
        d, behavior_on_error="ignore"
    )
    assert sha256(d, behavior_on_error="ignore") == sha256(
        d, behavior_on_error="ignore"
    )


def test_behaviour_on_error_raise():
    """Test that the behaviour_on_error parameter works as expected."""
    d = create_dict()
    d["not_hashable"] = NotHashable()
    with pytest.raises(NotHashableException):
        dict_hash(d, behavior_on_error="raise")

    with pytest.raises(NotHashableException):
        sha256(d, behavior_on_error="raise")

    # Since behavior_on_error is set by default to "raise",
    # the following should raise an exception.
    with pytest.raises(NotHashableException):
        dict_hash(d)

    with pytest.raises(NotHashableException):
        sha256(d)


def test_behaviour_on_error_warn():
    """Test that the behaviour_on_error parameter works as expected."""
    d = create_dict()
    d["not_hashable"] = NotHashable()
    with pytest.warns(NotHashableWarning):
        dict_hash(d, behavior_on_error="warn")

    with pytest.warns(NotHashableWarning):
        sha256(d, behavior_on_error="warn")


def test_behaviour_on_recursive_error_ignore():
    """Test that the behaviour_on_error parameter works as expected."""
    d = create_dict()
    d["not_hashable"] = RecursiveObject()
    assert dict_hash(d, behavior_on_error="ignore") == dict_hash(
        d, behavior_on_error="ignore"
    )
    assert sha256(d, behavior_on_error="ignore") == sha256(
        d, behavior_on_error="ignore"
    )


def test_behaviour_on_recursive_error_raise():
    """Test that the behaviour_on_error parameter works as expected."""
    d = create_dict()
    d["not_hashable"] = RecursiveObject()
    with pytest.raises(NotHashableException):
        dict_hash(d, behavior_on_error="raise")

    with pytest.raises(NotHashableException):
        sha256(d, behavior_on_error="raise")

    # Since behavior_on_error is set by default to "raise",
    # the following should raise an exception.
    with pytest.raises(NotHashableException):
        dict_hash(d)

    with pytest.raises(NotHashableException):
        sha256(d)


def test_behaviour_on_recursive_error_warn():
    """Test that the behaviour_on_error parameter works as expected."""
    d = create_dict()
    d["not_hashable"] = RecursiveObject()
    with pytest.warns(NotHashableWarning):
        dict_hash(d, behavior_on_error="warn")

    with pytest.warns(NotHashableWarning):
        sha256(d, behavior_on_error="warn")
