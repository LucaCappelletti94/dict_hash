from dict_hash import sha256, dict_hash
import pytest


def test_dict_hash_failure():
    with pytest.raises(ValueError):
        dict_hash(0)

    with pytest.raises(ValueError):
        sha256(0)
