from dict_hash import sha256
from .utils import create_dict
import os

def test_dict_hash():
    path = sha256(create_dict())
    assert os.path.exists(path)
    os.remove(path)