"""Module containing the main function of the package."""

import datetime
import hashlib
import inspect
import json
import warnings
from typing import Callable, Dict, List, Any, Tuple
import re
from deflate_dict import deflate

from dict_hash.hashable import Hashable


class NotHashableException(Exception):
    """Exception raised when an object is not hashable."""


class NotHashableWarning(UserWarning):
    """Warning raised when an object is not hashable."""


IGNORED_UNASHABLE_OBJECT_ATTRIBUTES = [
    "_repr_html_",
]


def is_built_in_attribute(obj: Any, attribute_name: str) -> bool:
    """Returns whether attribute is builtin"""
    try:
        attribute = getattr(obj, attribute_name)
        return (attribute.__class__.__module__ in ("__builtin__", "builtins")) or type(
            attribute
        ).__name__ in ("method-wrapper", "builtin_function_or_method")
    except (AttributeError, ValueError):
        return True


def _convert(
    data: Any,
    current_depth: int = 0,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> Any:
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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Hashable object or dictionary.

    Raises
    ------------------
    NotHashableException
        When we have no clue what to do with the provided object yet and we need to raise an error.

    Warns
    ------------------
    NotHashableWarning
        When we have no clue what to do with the provided object yet and we need to warn the user.
    """
    if current_depth > maximal_recursion:
        raise RecursionError(
            (
                f"Recursion depth exceeded {maximal_recursion}. "
                "Please consider increasing the maximal recursion depth "
                "or simplifying the object to hash."
            )
        )

    # If the object is a None.
    if data is None:
        return "None"
    # If given object is of type Hashable
    if isinstance(data, Hashable):
        # we call its method to convert it to an hash
        # that can be further hashed as required.
        try:
            return data.consistent_hash(use_approximation=use_approximation)
        except TypeError:
            # If this Hashable class is using the legacy interface, we call
            # it without any arguments and raise a warning to advise the user
            # that in a future version this will be deprecated.
            warnings.warn(
                (
                    "The method consistent_hash should take an argument "
                    "use_approximation: bool = False. This is needed to "
                    "allow for the approximation of the hash. "
                    "Please update the method to the new interface. "
                    "This will be deprecated in a future version."
                ),
                DeprecationWarning,
            )
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
        import numpy as np  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        pass
    else:
        # If the given object is a numpy integer, we convert it to a python integer.
        if isinstance(
            data,
            (
                np.uint64,
                np.uint32,
                np.uint16,
                np.uint8,
                np.int64,
                np.int32,
                np.int16,
                np.int8,
            ),
        ):
            return int(data)

        # If the given object is a numpy float, we convert it to a python float.
        float_np_types = (np.float64, np.float32, np.float16)

        try:
            float_np_types = (*float_np_types, np.float_)
        except AttributeError:
            pass

        if isinstance(data, float_np_types):
            return float(data)

        # If the given object is a numpy string, we convert it to a python string.
        try:
            string_np_types = (np.str_, np.bytes_)
        except AttributeError:
            string_np_types = (np.str_, np.string_)

        if isinstance(data, string_np_types):
            return str(data)

    # If the given data is a simple object such as a string, an integer
    # or a float we can leave it to be hashed.
    if isinstance(data, (str, int, float)):
        return data

    ############################################
    # Handling hashing of pandas objects       #
    ############################################

    try:
        import pandas as pd  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        pass
    else:
        # A similar behaviour is required for DataFrames.
        if isinstance(data, pd.DataFrame):
            # We store the initial shape of the dataframe, so
            # we can make it part of the hash even if we
            # use the approximation and sample only a part
            # of the dataframe.
            shape = data.shape

            if use_approximation:
                # We take at most the first 50 columns.
                # This is needed because we have encountered DataFrames
                # with millions of columns. Peace to the soul that made them.
                if data.shape[1] > 50:
                    data = data[data.columns[:50]]
                # We sample 50 random lines of the dataframe, as some dataframes
                # can contain millions of samples.
                if data.shape[0] > 50:
                    data = data.sample(n=50, random_state=42)
            return _convert(
                {
                    "hash": _convert(
                        data.to_dict(),
                        current_depth=current_depth + 1,
                        use_approximation=use_approximation,
                        behavior_on_error=behavior_on_error,
                        maximal_recursion=maximal_recursion,
                    ),
                    "shape": shape,
                },
                current_depth=current_depth + 1,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )
        if isinstance(data, pd.Series):
            shape = data.shape

            if use_approximation:
                if data.shape[0] > 50:
                    data = data.sample(n=50, random_state=42)

            return _convert(
                {
                    "hash": _convert(
                        data.to_dict(),
                        current_depth=current_depth + 1,
                        use_approximation=use_approximation,
                        behavior_on_error=behavior_on_error,
                        maximal_recursion=maximal_recursion,
                    ),
                    "name": data.name,
                },
                current_depth=current_depth + 1,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )

    ############################################
    # Handling hashing of Polars objects       #
    ############################################

    try:
        import polars as pl  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        pass
    else:
        # A similar behaviour is required for DataFrames.
        if isinstance(data, pl.DataFrame):
            # We store the initial shape of the dataframe, so
            # we can make it part of the hash even if we
            # use the approximation and sample only a part
            # of the dataframe.
            shape = data.shape

            if use_approximation:
                # We take at most the first 50 columns.
                # This is needed because we have encountered DataFrames
                # with millions of columns. Peace to the soul that made them.
                if data.shape[1] > 50:
                    data = data[data.columns[:50]]
                # We sample 50 random lines of the dataframe, as some dataframes
                # can contain millions of samples.
                if data.shape[0] > 50:
                    data = data.sample(n=50, random_state=42)
            return _convert(
                {
                    "hash": _convert(
                        data.to_dict(),
                        current_depth=current_depth + 1,
                        use_approximation=use_approximation,
                        behavior_on_error=behavior_on_error,
                        maximal_recursion=maximal_recursion,
                    ),
                    "shape": shape,
                },
                current_depth=current_depth + 1,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )
        if isinstance(data, pl.Series):
            shape = data.shape

            if use_approximation:
                if data.shape[0] > 50:
                    data = data.sample(n=50, random_state=42)

            return _convert(
                {
                    "hash": _convert(
                        np.array(data),
                        current_depth=current_depth + 1,
                        use_approximation=use_approximation,
                        behavior_on_error=behavior_on_error,
                        maximal_recursion=maximal_recursion,
                    ),
                    "name": data.name,
                },
                current_depth=current_depth + 1,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )

    ############################################
    # Handling hashing of numpy array objects  #
    ############################################

    try:
        import numpy as np  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        pass
    else:
        # And numpy arrays.
        if isinstance(data, np.ndarray):
            # We store the initial shape of the array, so
            # we can make it part of the hash even if we
            # use the approximation and sample only a part
            # of the array.
            shape = data.shape

            # We reshape the array so it is always 2D,
            # with at most 50 columns.
            if data.ndim == 1:
                data = data.reshape(-1, 1)
            if data.ndim > 2:
                product_of_dimensions = np.prod(data.shape[1:])
                data = data.reshape(-1, product_of_dimensions)

            if use_approximation:
                if data.shape[1] > 50:
                    data = data[:, :50]

                # We sample 100 random lines of the dataframe, as some dataframes
                # can contain millions of samples.
                if data.shape[0] > 50:
                    pnrg = np.random.RandomState(42)  # pylint: disable=no-member
                    data = data[pnrg.randint(data.shape[0], size=50)]

            return _convert(
                {
                    "hash": _convert(
                        data.tolist(),
                        current_depth=current_depth + 1,
                        use_approximation=use_approximation,
                        behavior_on_error=behavior_on_error,
                        maximal_recursion=maximal_recursion,
                    ),
                    "shape": shape,
                },
                current_depth=current_depth + 1,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )

    ############################################
    # Handling hashing of numba array objects  #
    ############################################

    try:
        from numba import typed  # pylint: disable=import-outside-toplevel
    except (ModuleNotFoundError, ImportError):
        pass
    else:
        try:
            # And iterables such as lists and tuples.
            if isinstance(data, typed.List):
                return [
                    _convert(
                        e,
                        current_depth=current_depth + 1,
                        use_approximation=use_approximation,
                        behavior_on_error=behavior_on_error,
                        maximal_recursion=maximal_recursion,
                    )
                    for e in data
                ]
            # If it is a dictionary we need to hash every element of it.
            if isinstance(data, typed.Dict):
                return dict(
                    [
                        _convert(
                            (key, value),
                            current_depth=current_depth + 1,
                            use_approximation=use_approximation,
                            behavior_on_error=behavior_on_error,
                            maximal_recursion=maximal_recursion,
                        )
                        for key, value in data.items()
                    ]
                )
        # In some old numba versions there is no attribute
        # List of Dict in typed.
        except AttributeError:
            pass

    # And iterables such as lists and tuples.
    if isinstance(data, list):
        return [
            _convert(
                e,
                current_depth=current_depth + 1,
                use_approximation=use_approximation,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )
            for e in data
        ]

    # If it is a dictionary we need to hash every element of it.
    if isinstance(data, dict):
        return dict(
            _convert(
                (key, value),
                current_depth=current_depth + 1,
                use_approximation=use_approximation,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )
            for key, value in data.items()
        )

    # And iterables such as lists and tuples.
    if isinstance(data, tuple):
        return tuple(
            _convert(
                e,
                current_depth=current_depth + 1,
                use_approximation=use_approximation,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            )
            for e in data
        )

    if isinstance(data, set):
        return sorted(
            [
                _convert(
                    e,
                    current_depth=current_depth + 1,
                    use_approximation=use_approximation,
                    behavior_on_error=behavior_on_error,
                    maximal_recursion=maximal_recursion,
                )
                for e in data
            ]
        )

    if isinstance(data, re.Pattern):
        return data.pattern

    if isinstance(data, Callable):
        return "".join(inspect.getsourcelines(data)[0])

    ############################################
    # Handling hashing of Ensmallen objects    #
    ############################################

    try:
        from ensmallen import Graph  # pylint: disable=import-outside-toplevel
    except ModuleNotFoundError:
        pass
    else:
        if isinstance(data, Graph):
            return data.hash()

    try:
        return _sanitize(
            {
                key: getattr(data, key)
                for key in dir(data)
                if (
                    key not in IGNORED_UNASHABLE_OBJECT_ATTRIBUTES
                    and not is_built_in_attribute(data, key)
                )
            },
        )
    except (NotHashableException, TypeError, RecursionError):
        pass

    if behavior_on_error == "ignore":
        return "Unhashable object"

    message = (
        f"Object of class {data.__class__.__name__} not currently supported. "
        f"The module of origin of the object is {data.__class__.__module__}. "
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
    )

    if behavior_on_error == "warn":
        warnings.warn(message, NotHashableWarning)
        return "Unhashable object"

    # Otherwise we need to raise an exception to warn the user.
    raise NotHashableException(message)


def _sanitize(
    dictionary: Dict,
    current_depth: int = 0,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return given dictionary as JSON string.

    Parameters
    -------------------
    dictionary: Dict
        Dictionary to be converted to JSON.
    current_depth: int = 0
        Current recursion depth.
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    -------------------
    JSON string representation of given dictionary.

    Raises
    -------------------
    ValueError
        When the given object is not a dictionary.
    ValueError
        When the given value for `behavior_on_error` is not supported.
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".

    Warns
    -------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    if not isinstance(dictionary, (Dict, List)):
        raise ValueError(
            (
                "Given object to hash is not a dictionary nor a List, "
                f"but a {dictionary.__class__.__name__} object, which is not currently supported."
            )
        )
    if not isinstance(behavior_on_error, str) or behavior_on_error not in (
        "raise",
        "warn",
        "ignore",
    ):
        raise ValueError(
            (
                "Given value for `behavior_on_error` is not supported. "
                "Please provide a value in ('raise', 'warn', 'ignore')."
            )
        )
    return json.dumps(
        deflate(
            _convert(
                dictionary,
                current_depth=current_depth,
                use_approximation=use_approximation,
                behavior_on_error=behavior_on_error,
                maximal_recursion=maximal_recursion,
            ),
            leave_tuples=True,
        ),
        sort_keys=True,
    )


def dict_hash(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Session hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return hash(
        _sanitize(
            dictionary,
            use_approximation=use_approximation,
            behavior_on_error=behavior_on_error,
            maximal_recursion=maximal_recursion,
        )
    )


def _basic_hash(
    dictionary: Dict,
    hash_function: Callable[[bytes], Any],
    hexdigest_args: Tuple = (),
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    return hash_function(
        _sanitize(
            dictionary,
            use_approximation=use_approximation,
            behavior_on_error=behavior_on_error,
            maximal_recursion=maximal_recursion,
        ).encode("utf-8")
    ).hexdigest(*hexdigest_args)


def md5(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return md5 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.md5,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha1(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha1 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha1,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha224(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha224 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha224,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha256(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha256,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha384(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha384 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha384,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha512(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha512 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha512,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def blake2b(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return blake2b of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.blake2b,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def blake2s(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return blake2s of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.blake2s,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha3_224(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha3_224 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha3_224,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha3_256(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha3_256 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha3_256,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha3_384(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha3_384 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha3_384,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def sha3_512(
    dictionary: Dict,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return sha3_512 of given dict.

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
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.sha3_512,
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def shake_128(
    dictionary: Dict,
    hash_length: int = 32,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return shake_128 of given dict.

    Parameters
    ------------------
    dictionary: Dict
        Dictionary of which determine an unique hash.
    hash_length: int = 32
        Length of the hash to return.
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.shake_128,
        hexdigest_args=(hash_length,),
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )


def shake_256(
    dictionary: Dict,
    hash_length: int = 32,
    use_approximation: bool = False,
    behavior_on_error: str = "raise",
    maximal_recursion: int = 100,
) -> str:
    """Return shake_256 of given dict.

    Parameters
    ------------------
    dictionary: Dict
        Dictionary of which determine an unique hash.
    hash_length: int = 32
        Length of the hash to return.
    use_approximation: bool = False
        Whether to employ approximations, such as sampling
        random values in pandas dataframe (using a fixed deterministic
        random seed) or lines in a numpy array. This is mainly
        needed when you need to hash frequently big pandas dataframes
        and you do not care about generating a very precise hash
        but a decent one will do the trick.
    behavior_on_error: str = "raise"
        Whether to raise an error when an unhashable object is found
        or to return a string representation of the object. The options
        are "raise", "warn" and "ignore". If "warn" is selected, a warning
        will be issued using the `warnings` module. If "ignore" is selected,
        the object will be ignored and the hash will be computed without it
        without raising any error or warning.
    maximal_recursion: int = 100
        Maximum recursion depth allowed.

    Returns
    ------------------
    Deterministic hash for the given dictionary.

    Raises
    ------------------
    NotHashableException
        When an object is not hashable and `behavior_on_error` is set to "raise".
    ValueError
        When `behavior_on_error` is not a string or is not in ("raise", "warn", "ignore").

    Warns
    ------------------
    NotHashableWarning
        When an object is not hashable and `behavior_on_error` is set to "warn".
    """
    return _basic_hash(
        dictionary,
        hashlib.shake_256,
        hexdigest_args=(hash_length,),
        use_approximation=use_approximation,
        behavior_on_error=behavior_on_error,
        maximal_recursion=maximal_recursion,
    )
