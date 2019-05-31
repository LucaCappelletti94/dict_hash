from random_dict import random_dict
from dict_hash import sha256
from random import seed, randint
import os

def test_dict_hash():
    seed(0)
    path = sha256(random_dict(randint(0,10), randint(0,10)))
    assert os.path.exists(path)
    os.remove(path)