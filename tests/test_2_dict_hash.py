"""Test the dict_hash function."""

import os
import numpy as np
from dict_hash import ALL_AVAILABLE_HASHES
from .utils import create_dict


def test_dict_hash():
    """Test to make sure that the hash is created."""
    d = create_dict()
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_without_approximation_1d():
    """Test to make sure that the hash is stable for 1d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((731,), 1)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_without_approximation_2d():
    """Test to make sure that the hash is stable for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((873, 10), 2)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_without_approximation_3d():
    """Test to make sure that the hash is stable for 3d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1013, 10, 2), 3)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_without_approximation_4d():
    """Test to make sure that the hash is stable for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 3, 2), 4)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_with_approximation_1d():
    """Test to make sure that the hash is stable for 1d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((100,), 5)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d, use_approximation=True)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_with_approximation_2d():
    """Test to make sure that the hash is stable for 2d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10), 6)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d, use_approximation=True)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_with_approximation_3d():
    """Test to make sure that the hash is stable for 3d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 2), 7)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d, use_approximation=True)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_with_approximation_4d():
    """Test to make sure that the hash is stable for 4d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 3, 2), 8)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d, use_approximation=True)
        assert os.path.exists(path)
        os.remove(path)


def test_dict_hash_with_approximation_4d_with_different_shape():
    """Test to make sure that the hash is stable for 4d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((100, 10, 3, 3), 8)]
    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        path = consistent_hash_function(d, use_approximation=True)
        assert os.path.exists(path)
        os.remove(path)
