from dict_hash import sha256, dict_hash
from pathlib import Path
import numpy as np
from .utils import create_dict


def test_dict_hash():
    d = create_dict()
    assert dict_hash(d) == dict_hash(d)
    assert sha256(d) == sha256(d)
    Path(sha256(d)).touch()


def test_dict_hash_with_approximation():
    d = create_dict()
    d["this_is_big"] = [np.zeros((10000, 100))]
    assert dict_hash(d, use_approximation=True) == dict_hash(d, use_approximation=True)
    assert sha256(d, use_approximation=True) == sha256(d, use_approximation=True)
    Path(sha256(d)).touch()
