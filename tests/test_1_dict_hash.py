from random_dict import random_dict
from dict_hash import sha256, dict_hash
from random import seed, randint
from pathlib import Path

def test_dict_hash():
    seed(0)
    d = random_dict(randint(0,10), randint(0,10))
    assert dict_hash(d) == dict_hash(d)
    Path(sha256(d)).touch()