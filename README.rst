Dict Hash
=========================================================================================
|pip| |downloads|

Simple python tool to hash dictionaries using both default hash and sha256.
The library comes with full support for hashing Pandas DataFrame objects,
Numba objects and Numpy arrays, but you will need to specify the requirements
when installing the package to avoid bloating the installation process.

Furthermore, the library supports objects that can be recursively hashed.

As we saw this library being used in the wild mostly to create caching libraries and wrappers,
we'd like to point you to our library, `Cache decorator <https://github.com/zommiommy/cache_decorator>`__.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install dict_hash


Usage examples
----------------------------------------------
The package offers two functions: `sha256` to generate constant sha256 hashes and `dict_hash`, to generate hashes using the native `hash` function.

Session hash with dict_hash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Obtain a session hash from the given dictionary.

.. code:: python

    from dict_hash import dict_hash
    from random_dict import random_dict
    from random import randint

    d = random_dict(randint(1, 10), randint(1, 10))
    my_hash = dict_hash(d)


Consistent hash with sha256
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Obtain a consistent hash from the given dictionary.

.. code:: python

    from dict_hash import sha256
    from random_dict import random_dict
    from random import randint

    d = random_dict(randint(1, 10), randint(1, 10))
    my_hash = sha256(d)

Approximated hash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
All of the methods shown offer the `use_approximation` parameter,
which allows you to switch to a more lightweight hashing procedure
where supported, for the various supported objects. This procedure
will randomly subsample the provided objects.

Currently, we support this parameter for NumPy and Pandas objects.

.. code:: python

    from dict_hash import sha256
    from random_dict import random_dict
    from random import randint

    # Even though the DataFrame is very big...
    df = load_a_very_big_dataframe(...)
    # an approximated hash is still very fast!
    my_hash = sha256(
        df,
        use_approximation=True
    )



Hashable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When handling complex objects within the dictionaries, you may need to implement
the class Hashable in that object.

Here is an example:

.. code:: python

    from dict_hash import Hashable, sha256


    class MyHashable(Hashable):

        def __init__(self, a: int):
            self._a = a
            self._time = time()

        def consistent_hash(self) -> str:
            return sha256({
                "a": self._a
            })


.. |pip| image:: https://badge.fury.io/py/dict-hash.svg
    :target: https://badge.fury.io/py/dict-hash
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/dict-hash
    :target: https://pepy.tech/badge/dict-hash
    :alt: Pypi total project downloads
