from .utils import create_dict
from tqdm.auto import trange
from dict_hash import sha256, dict_hash


def test_with_fuzzying():
    for i in trange(1000, desc="Running some fuzzyng tests"):
        d = create_dict(i)
        assert dict_hash(d) == dict_hash(d)
        assert sha256(d) == sha256(d)