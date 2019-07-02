import hashlib
from json import dumps
from typing import Dict
import collections
import pandas as pd
import numpy as np

def _convert(data):
    if isinstance(data, str):
        return data
    if isinstance(data, collections.Mapping):
        return dict(map(_convert, data.items()))
    if isinstance(data, pd.DataFrame):
        return data.to_json()
    if isinstance(data, np.ndarray):
        return pd.DataFrame(data).to_json()
    if isinstance(data, collections.Iterable):
        return type(data)(map(_convert, data))
    return data

def _sanitize(d:Dict)->str:
    return dumps(_convert(d))

def dict_hash(d:Dict)->str:
    """Return hash of given dict (may not be equal for every session).
        d:Dict, dictionary of which determine an unique hash.
    """
    return hash(_sanitize(d))

def sha256(d:Dict)->str:
    """Return sha256 of given dict.
        d:Dict, dictionary of which determine an unique hash.
    """
    return hashlib.sha256(_sanitize(d).encode('utf-8')).hexdigest()