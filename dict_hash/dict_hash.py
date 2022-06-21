import datetime
import hashlib
import inspect
import json
from typing import Callable, Dict, List
import re
from deflate_dict import deflate

from .hashable import Hashable


class NotHashableException(Exception):
    pass


IGNORED_UNASHABLE_OBJECT_ATTRIBUTES = [
    "_repr_html_",
]


def _convert(
    data: object,
    use_approximation: bool = False
) -> object:
    """Returns given data as an hashable object or dictionary.

    Parameters
    ------------------
    data: object
        The data 
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.

    Raises
    ------------------
    NotImplementedError
        When we have no clue what to do with the provided object yet.
    """
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
    # If given object is either a date or datetime object
    if isinstance(data, datetime.date):
        # we convert the object to the string version
        # following the ISO format of the date.
        return data.isoformat()

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
            if use_approximation:
                # We take at most the first 50 columns.
                # This is needed because we have encountered DataFrames
                # with millions of columns. Peace to the soul that made them.
                if data.shape[1] > 50:
                    data = data[data.columns[:50]]
                # We sample 50 random lines of the dataframe, as some dataframes
                # can contain millions of samples.
                if data.shape[0] > 50:
                    data = data.sample(
                        n=50,
                        random_state=42
                    )
            return _convert(
                data.to_dict(),
                use_approximation=use_approximation
            )

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

    ############################################
    # Handling hashing of numpy array objects  #
    ############################################

    try:
        import numpy as np
        import pandas as pd
    except ModuleNotFoundError:
        pass
    else:
        # And numpy arrays.
        if isinstance(data, np.ndarray):
            if use_approximation:
                # We take at most the first 50 columns.
                # This is needed because we have encountered Numpy Arrays
                # with millions of columns. Peace to the soul that made them.
                if len(data.shape) > 1 and data.shape[1] > 50:
                    data = data[:, :50]
                # We sample 100 random lines of the dataframe, as some dataframes
                # can contain millions of samples.
                if data.shape[0] > 50:
                    pnrg = np.random.RandomState(42)
                    data = data[pnrg.randint(data.shape[0], size=50)]

            return _convert(
                pd.DataFrame(data),
                use_approximation=False
            )

    ############################################
    # Handling hashing of numba array objects  #
    ############################################

    try:
        from numba import typed
    except (ModuleNotFoundError, ImportError):
        pass
    else:
        try:
            # And iterables such as lists and tuples.
            if isinstance(data, typed.List):
                return [
                    _convert(
                        e,
                        use_approximation=use_approximation
                    )
                    for e in data
                ]
            # If it is a dictionary we need to hash every element of it.
            if isinstance(data, typed.Dict):
                return dict([
                    _convert(
                        (key, value),
                        use_approximation=use_approximation
                    )
                    for key, value in data.items()
                ])
        # In some old numba versions there is no attribute
        # List of Dict in typed.
        except AttributeError:
            pass

    # And iterables such as lists and tuples.
    if isinstance(data, list):
        return [
            _convert(
                e,
                use_approximation=use_approximation
            )
            for e in data
        ]

    # If it is a dictionary we need to hash every element of it.
    if isinstance(data, dict):
        return dict(
            _convert(
                (key, value),
                use_approximation=use_approximation
            )
            for key, value in data.items()
        )

    # And iterables such as lists and tuples.
    if isinstance(data, tuple):
        return tuple(
            _convert(
                e,
                use_approximation=use_approximation
            )
            for e in data
        )

    if isinstance(data, set):
        return sorted([
            _convert(
                e,
                use_approximation=use_approximation
            )
            for e in data
        ])

    if isinstance(data, re.Pattern):
        return data.pattern

    if isinstance(data, Callable):
        return "".join(
            inspect.getsourcelines(data)[0]
        )

    try:
        return _sanitize({
            key: data.__getattribute__(key)
            for key in dir(data)
            if (
                key not in IGNORED_UNASHABLE_OBJECT_ATTRIBUTES and
                data.__getattribute__(key).__class__.__module__ not in ("__builtin__", "builtins") and
                type(data.__getattribute__(key)).__name__ not in ("method-wrapper", "builtin_function_or_method")
            )
        })
    except NotHashableException:
        pass

    # Otherwise we need to raise an exception to warn the user.
    raise NotHashableException(
        (
            "Object of class {} not currently supported. "
            "You can easily adding support for the object "
            "by extending the `Hashable` abstract class for "
            "your object of interest. "
            "If you believe this object to be of extremely common use, "
            "please do consider opening up an issue and related "
            "pull requested on the `dict_hash` GitHub repository "
            "to add support for this new type of object. "
            "We only consider for the inclusion in the library "
            "either extremely commonly used objects or objects "
            "that impact often our projects."
        ).format(data.__class__.__name__)
    )


def _sanitize(
    dictionary: Dict,
    use_approximation: bool = False
) -> str:
    """Return given dictionary as JSON string.

    Parameters
    -------------------
    dictionary: Dict
        Dictionary to be converted to JSON.
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.

    Raises
    -------------------
    ValueError
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
    return json.dumps(deflate(_convert(
        dictionary,
        use_approximation=use_approximation
    ), leave_tuples=True), sort_keys=True)


def dict_hash(
    dictionary: Dict,
    use_approximation: bool = False
) -> str:
    """Return hash of given dict (may not be equal for every session).

    Parameters
    ------------------
    dictionary: Dict
        Dictionary of which determine an unique hash.
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.

    Returns
    ------------------
    Session hash for the given dictionary.
    """
    return hash(_sanitize(
        dictionary,
        use_approximation=use_approximation
    ))


def sha256(
    dictionary: Dict,
    use_approximation: bool = False
) -> str:
    """Return sha256 of given dict.

    Parameters
    ------------------
    dictionary: Dict
        Dictionary of which determine an unique hash.
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.

    Returns
    ------------------
    Deterministic hash for the given dictionary.
    """
    return hashlib.sha256(
        _sanitize(
            dictionary,
            use_approximation=use_approximation
        ).encode('utf-8')
    ).hexdigest()
