from dict_hash import sha256, dict_hash
from pathlib import Path
from .utils import create_dict

def test_dict_hash():
    d = create_dict()
    assert dict_hash(d) == dict_hash(d)
    Path(sha256(d)).touch()