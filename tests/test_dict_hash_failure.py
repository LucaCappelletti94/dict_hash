"""Test the dict_hash function for failure cases."""

import pytest
from dict_hash import dict_hash, ALL_AVAILABLE_HASHES


def test_dict_hash_failure():
    """Test to make sure that the hash raises an error for invalid input."""
    with pytest.raises(ValueError):
        dict_hash(0)

    for consistent_hash_function in ALL_AVAILABLE_HASHES:
        with pytest.raises(ValueError):
            consistent_hash_function(0)
