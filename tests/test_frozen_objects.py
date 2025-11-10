"""Submodule testing hashing of frozendict, frozenset and similar objects."""

from dict_hash import dict_hash


def test_frozenset_hash():
    """Test hashing of frozendict objects."""

    s1 = frozenset(["a", "b", "c"])
    s2 = frozenset(["c", "b", "a"])
    s3 = frozenset(["a", "b", "d"])
    first_dict = {"x": s1, "y": s3}
    second_dict = {"x": s2, "y": s3}
    third_dict = {"x": s3, "y": s1}

    hash1 = dict_hash(first_dict)
    hash2 = dict_hash(second_dict)
    hash3 = dict_hash(third_dict)
    assert hash1 == hash2, "Hashes of identical frozensets should match."
    assert (
        hash1 != hash3
    ), f"Hashes of different frozensets ({first_dict}, {third_dict}) should not match."
