import hashlib
import json
from typing import Dict
import pandas as pd
import numpy as np
from numba import typed
from .hashable import Hashable
from deflate_dict import deflate


def _convert(data):
    """Returns given data as an hashable object or dictionary."""
    # If given object is of type Hashable
    if isinstance(data, Hashable):
        # we call its method to convert it to an hash
        # that can be further hashed as required.
        return data.consistent_hash()
    # If we are handling an instance of fixed-length numpy strings we need to
    # convert them back to a normal python string so that they may be hashed.
    if isinstance(data, bytes):
        return data.decode()
    if isinstance(data, (np.str_, np.string_)):
        return str(data)
    # If the given data is a simple object such as a string, an integer
    # or a float we can leave it to be hashed.
    if isinstance(data, (str, int, float)):
        return data
    # If it is a dictionary we need to hash every element of it.
    if isinstance(data, (dict, typed.Dict)):
        return dict(map(_convert, list(data.items())))
    # A similar behaviour is required for DataFrames.
    if isinstance(data, pd.DataFrame):
        return _convert(data.to_dict())
    # And numpy arrays.
    if isinstance(data, np.ndarray):
        return _convert(pd.DataFrame(data))
    # And iterables such as lists and tuples.
    if isinstance(data, (list, typed.List)):
        return list(map(_convert, data))
    if isinstance(data, tuple):
        return tuple(map(_convert, data))

    # Otherwise we need to raise an exception to warn the user.
    raise ValueError("Object of class {} not currently supported.".format(
        data.__class__.__name__
    ))


def _sanitize(dictionary: Dict) -> str:
    """Return given dictionary as JSON string.

    Parameters
    -------------------
    dictionary: Dict,
        Dictionary to be converted to JSON.

    Raises
    -------------------
    ValueError,
        When the given object is not a dictionary.

    Returns
    -------------------
    JSON string representation of given dictionary.
    """
    if not isinstance(dictionary, Dict):
        raise ValueError("Given object to hash is not a dictionary.")
    return json.dumps(deflate(_convert(dictionary)))


def dict_hash(dictionary: Dict) -> str:
    """Return hash of given dict (may not be equal for every session).

    Parameters
    ------------------
    dictionary: Dict,
        Dictionary of which determine an unique hash.

    Returns
    ------------------
    Session hash for the given dictionary.
    """
    return hash(_sanitize(dictionary))


def sha256(dictionary: Dict) -> str:
    """Return sha256 of given dict.

    Parameters
    ------------------
    dictionary: Dict,
        Dictionary of which determine an unique hash.

    Returns
    ------------------
    Deterministic hash for the given dictionary.
    """
    return hashlib.sha256(_sanitize(dictionary).encode('utf-8')).hexdigest()
