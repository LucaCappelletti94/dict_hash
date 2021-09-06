import hashlib
import inspect
import json
from typing import Dict, List, Callable
from .hashable import Hashable
from deflate_dict import deflate


def _convert(data: object):
    """Returns given data as an hashable object or dictionary."""
    # If the object is a None.
    if data is None:
        return "None"
    # If given object is of type Hashable
    if isinstance(data, Hashable):
        # we call its method to convert it to an hash
        # that can be further hashed as required.
        return data.consistent_hash()
    # If we are handling an instance of fixed-length numpy strings we need to
    # convert them back to a normal python string so that they may be hashed.
    if isinstance(data, bytes):
        return data.decode()

    ############################################
    # Handling hashing of numpy string objects #
    ############################################

    try:
        import numpy as np
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(data, (np.str_, np.string_)):
            return str(data)

    # If the given data is a simple object such as a string, an integer
    # or a float we can leave it to be hashed.
    if isinstance(data, (str, int, float)):
        return data

    ############################################
    # Handling hashing of pandas objects       #
    ############################################

    try:
        import pandas as pd
    except ModuleNotFoundError:
        pass
    else:
        # A similar behaviour is required for DataFrames.
        if isinstance(data, pd.DataFrame):
            return _convert(data.to_dict())

    ############################################
    # Handling hashing of Ensmallen objects    #
    ############################################

    try:
        from ensmallen import Graph
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(data, Graph):
            return data.hash()

    #############################################################
    # Handling hashing of older version of Ensmallen objects    #
    #############################################################

    try:
        from ensmallen_graph import EnsmallenGraph
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(data, EnsmallenGraph):
            return data.hash()

    ############################################
    # Handling hashing of numpy array objects  #
    ############################################

    try:
        import pandas as pd
        import numpy as np
    except ModuleNotFoundError:
        pass
    else:
        # And numpy arrays.
        if isinstance(data, np.ndarray):
            return _convert(pd.DataFrame(data))

    ############################################
    # Handling hashing of numba array objects  #
    ############################################

    try:
        from numba import typed
    except ModuleNotFoundError:
        pass
    else:
        # And iterables such as lists and tuples.
        if isinstance(data, typed.List):
            return list(map(_convert, data))
        # If it is a dictionary we need to hash every element of it.
        if isinstance(data, typed.Dict):
            return dict(map(_convert, list(data.items())))

    # And iterables such as lists and tuples.
    if isinstance(data, list):
        return list(map(_convert, data))
    # If it is a dictionary we need to hash every element of it.
    if isinstance(data, dict):
        return dict(map(_convert, list(data.items())))

    if isinstance(data, tuple):
        return tuple(map(_convert, data))
    if isinstance(data, Callable):
        return "".join(
            inspect.getsourcelines(data)[0]
        )

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
    if not isinstance(dictionary, (Dict, List)):
        raise ValueError((
            "Given object to hash is not a dictionary nor a List, "
            "but a {} object, which is not currently supported."
        ).format(
            dictionary.__class__.__name__
        ))
    return json.dumps(deflate(_convert(dictionary), leave_tuples=True), sort_keys=True)


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
