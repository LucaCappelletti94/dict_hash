from .hashable import Hashable


def validate_consistent_hash(first: Hashable, second: Hashable) -> bool:
    """Return boolean validating if given object have consistent hash.

    Parameters
    ----------------------
    first: Hashable,
        First term to be hashed and validated.
    second: Hashable
        Second term to be hashed and validated.

    Returns
    ----------------------
    Boolean representing if the two objects hash consistently.
    """
    return first.consistent_hash() == second.consistent_hash()
