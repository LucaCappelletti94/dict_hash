from dict_hash import sha256, dict_hash


def test_with_different_keys_order():
    d1 = {
        'tune_best_model': True,
        'target': 'def'
    }

    d2 = {
        'target': 'def',
        'tune_best_model': True
    }

    assert sha256(d1) == sha256(d2)
