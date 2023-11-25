"""Test the dict_hash function."""
import os
import numpy as np
from dict_hash import sha256
from .utils import create_dict


def test_dict_hash():
    """Test to make sure that the hash is created."""
    path = sha256(create_dict())
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_without_approximation_1d():
    """Test to make sure that the hash is stable for 1d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((731,), 1)]
    path = sha256(d)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_without_approximation_2d():
    """Test to make sure that the hash is stable for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((873, 100), 2)]
    path = sha256(d)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_without_approximation_3d():
    """Test to make sure that the hash is stable for 3d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1013, 100, 2), 3)]
    path = sha256(d)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_without_approximation_4d():
    """Test to make sure that the hash is stable for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 10, 3, 2), 4)]
    path = sha256(d)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_with_approximation_1d():
    """Test to make sure that the hash is stable for 1d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000,), 5)]
    path = sha256(d, use_approximation=True)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_with_approximation_2d():
    """Test to make sure that the hash is stable for 2d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 100), 6)]
    path = sha256(d, use_approximation=True)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_with_approximation_3d():
    """Test to make sure that the hash is stable for 3d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 100, 2), 7)]
    path = sha256(d, use_approximation=True)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_with_approximation_4d():
    """Test to make sure that the hash is stable for 4d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 10, 3, 2), 8)]
    path = sha256(d, use_approximation=True)
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_with_approximation_4d_with_different_shape():
    """Test to make sure that the hash is stable for 4d arrays with approximations."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 10, 3, 3), 8)]
    path = sha256(d, use_approximation=True)
    assert os.path.exists(path)
    os.remove(path)
