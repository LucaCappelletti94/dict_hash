from dict_hash import sha256
from .utils import create_dict
import os
import numpy as np


def test_dict_hash():
    path = sha256(create_dict())
    assert os.path.exists(path)
    os.remove(path)


def test_dict_hash_with_approximation():
    d = create_dict()
    d["this_is_big"] = [np.zeros((10000, 100))]
    path = sha256(d)
    assert os.path.exists(path)
    os.remove(path)
