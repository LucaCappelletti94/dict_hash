from dict_hash import sha256, dict_hash
from pathlib import Path
import numpy as np
from .utils import create_dict


def test_dict_hash():
    d = create_dict()
    assert dict_hash(d) == dict_hash(d)
    assert sha256(d) == sha256(d)
    Path(sha256(d)).touch()


def test_dict_hash_without_approximation_1d():
    """Test to make sure that the hash is stable for 1d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((731,), 1)]
    assert dict_hash(d) == dict_hash(d)
    assert sha256(d) == sha256(d)
    Path(sha256(d)).touch()


def test_dict_hash_without_approximation_2d():
    """Test to make sure that the hash is stable for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((873, 100), 2)]
    assert dict_hash(d) == dict_hash(d)
    assert sha256(d) == sha256(d)
    Path(sha256(d)).touch()


def test_dict_hash_without_approximation_3d():
    """Test to make sure that the hash is stable for 3d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1013, 100, 2), 3)]
    assert dict_hash(d) == dict_hash(d)
    assert sha256(d) == sha256(d)
    Path(sha256(d)).touch()


def test_dict_hash_without_approximation_4d():
    """Test to make sure that the hash is stable for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 10, 3, 2), 4)]
    assert dict_hash(d) == dict_hash(d)
    assert sha256(d) == sha256(d)
    Path(sha256(d)).touch()


def test_dict_hash_with_approximation_1d():
    """Test to make sure that the approximation works for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000,), 5)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    assert sha256(d, use_approximation=True) == sha256(d, use_approximation=True)
    Path(sha256(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_2d():
    """Test to make sure that the approximation works for 2d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 100), 6)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    assert sha256(d, use_approximation=True) == sha256(d, use_approximation=True)
    Path(sha256(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_3d():
    """Test to make sure that the approximation works for 3d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 100, 2), 7)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    assert sha256(d, use_approximation=True) == sha256(d, use_approximation=True)
    Path(sha256(d, use_approximation=True)).touch()


def test_dict_hash_with_approximation_4d():
    """Test to make sure that the approximation works for 4d arrays."""
    d = create_dict()
    d["this_is_big"] = [np.full((1000, 10, 3, 2), 8)]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    assert sha256(d, use_approximation=True) == sha256(d, use_approximation=True)
    Path(sha256(d, use_approximation=True)).touch()
