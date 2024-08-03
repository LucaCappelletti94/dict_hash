"""Test suite verifying consistency of hashes"""

from pathlib import Path
import numpy as np
from dict_hash import ALL_AVAILABLE_HASHES, dict_hash
from .utils import create_dict


def test_dict_hash():
    """Test to make sure that the hash is created in a consistent way across runs."""
    d = create_dict()
    assert dict_hash(d) == dict_hash(d)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(d) == consistent_hash_function(d)
        Path(consistent_hash_function(d)).touch()


def test_dict_hash_without_approximation_1d():
    """Test to make sure that the hash is stable for 1d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((731,), 1)]
    assert dict_hash(d) == dict_hash(d)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(d) == consistent_hash_function(d)
        Path(consistent_hash_function(d)).touch()


def test_dict_hash_without_approximation_2d():
    """Test to make sure that the hash is stable for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((873, 10), 2)]
    assert dict_hash(d) == dict_hash(d)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(d) == consistent_hash_function(d)
        Path(consistent_hash_function(d)).touch()


def test_dict_hash_without_approximation_3d():
    """Test to make sure that the hash is stable for 3d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1013, 10, 2), 3)]
    assert dict_hash(d) == dict_hash(d)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(d) == consistent_hash_function(d)
        Path(consistent_hash_function(d)).touch()


def test_dict_hash_without_approximation_4d():
    """Test to make sure that the hash is stable for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 3, 2), 4)]
    assert dict_hash(d) == dict_hash(d)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(d) == consistent_hash_function(d)
        Path(consistent_hash_function(d)).touch()


def test_dict_hash_with_approximation_1d():
    """Test to make sure that the approximation works for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100,), 5)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)

    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(
            d, use_approximation=True
        ) == consistent_hash_function(d, use_approximation=True)
        Path(consistent_hash_function(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_2d():
    """Test to make sure that the approximation works for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10), 6)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(
            d, use_approximation=True
        ) == consistent_hash_function(d, use_approximation=True)
        Path(consistent_hash_function(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_3d():
    """Test to make sure that the approximation works for 3d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 2), 7)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(
            d, use_approximation=True
        ) == consistent_hash_function(d, use_approximation=True)
        Path(consistent_hash_function(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_4d():
    """Test to make sure that the approximation works for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 3, 2), 8)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(
            d, use_approximation=True
        ) == consistent_hash_function(d, use_approximation=True)
        Path(consistent_hash_function(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_4d_with_different_shape():
    """Test to make sure that the approximation works for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 3, 3), 8)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)

    previous = create_dict()
    previous["this_is_big"] = [np.full((100, 10, 3, 2), 8)]

    assert dict_hash(d, use_approximation=True) != dict_hash(
        previous, use_approximation=True
    )

    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        assert consistent_hash_function(
            d, use_approximation=True
        ) == consistent_hash_function(d, use_approximation=True)
        Path(consistent_hash_function(d, use_approximation=True)).touch()
