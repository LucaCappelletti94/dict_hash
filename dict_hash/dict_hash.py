import hashlib
from json import dumps
from typing import Dict
import pandas as pd
import numpy as np
from .hashable import Hashable


def _convert(data):
    # If given object is of type Hashable
    if isinstance(data, Hashable):
        # we call its method to convert it to an hash
        # that can be further hashed as required.
        return data.consistent_hash()
    # If the given data is a simple object such as a string, an integer
    # or a float we can leave it to be hashed.
    if isinstance(data, (str, int, float)):
        return data
    # If it is a dictionary we need to hash every element of it.
    if isinstance(data, dict):
        return dict(map(_convert, data.items()))
    # A similar behaviour is required for DataFrames.
    if isinstance(data, pd.DataFrame):
        return data.to_dict()
    # And numpy arrays.
    if isinstance(data, np.ndarray):
        return _convert(pd.DataFrame(data))
    # And iterables such as lists and tuples.
    if isinstance(data, (list, tuple)):
        return type(data)(map(_convert, data))

    # Otherwise we need to raise an exception to warn the user.
    raise ValueError("Object of class {} not currently supported.".format(
        data.__class__.__name__
    ))


def _sanitize(d: Dict) -> str:
    return dumps(_convert(d))


def dict_hash(d: Dict) -> str:
    """Return hash of given dict (may not be equal for every session).
        d:Dict, dictionary of which determine an unique hash.
    """
    return hash(_sanitize(d))


def sha256(d: Dict) -> str:
    """Return sha256 of given dict.
        d:Dict, dictionary of which determine an unique hash.
    """
    return hashlib.sha256(_sanitize(d).encode('utf-8')).hexdigest()
