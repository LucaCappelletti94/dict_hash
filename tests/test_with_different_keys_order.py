"""Test that the hash of a dictionary is the same regardless of the order of the keys."""

from dict_hash import ALL_AVAILABLE_HASHES, dict_hash


def test_with_different_keys_order():
    """Test that the hash of a dictionary is the same regardless of the order of the keys."""
    d1 = {"tune_best_model": True, "target": "def"}

    d2 = {"target": "def", "tune_best_model": True}

    for approximation in [True, False]:
        assert dict_hash(d1, use_approximation=approximation) == dict_hash(
            d2, use_approximation=approximation
        )
        for consistent_hash_function in ALL_AVAILABLE_HASHES:
            assert consistent_hash_function(
                d1, use_approximation=approximation
            ) == consistent_hash_function(d2, use_approximation=approximation)
