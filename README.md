# Dict Hash

[![Pypi project](https://badge.fury.io/py/dict-hash.svg)](https://badge.fury.io/py/dict-hash)
[![License](https://img.shields.io/github/license/LucaCappelletti94/dict_hash)](https://github.com/LucaCappelletti94/dict_hash/blob/master/LICENSE)
[![Pypi total project downloads](https://pepy.tech/badge/dict-hash)](https://pepy.tech/badge/dict-hash)
[![Github Actions](https://github.com/LucaCappelletti94/dict_hash/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/dict_hash/actions/)

Python package to hash dictionaries using both default hash and sha256.
It comes with full support for hashing Pandas & Polars DataFrame/Series objects, Numba objects and Numpy arrays.
It supports both objects from Pandas 1.x and 2.x and Numpy 1.x and 2.x.

Furthermore, the library supports objects that can be recursively hashed.

As we saw this library being used in the wild mostly to create caching libraries and wrappers,
we'd like to point you to our library, [Cache decorator](https://github.com/zommiommy/cache_decorator).

## Why can't I just use the default hash function?

In Python, dictionaries just aren't hashable. This is because they are mutable objects, and as such, they cannot be hashed.
If you were to try and run `hash({})`, you would get a `TypeError` exception.

## How do I install this package?

As usual, just download it using pip:

```shell
pip install dict_hash
```

## Usage examples

The package offers two functions: `sha256` to generate constant sha256 hashes and `dict_hash`, to generate hashes using the native `hash` function.

### Session hash with dict_hash

Obtain a session hash from the given dictionary.

```python
from dict_hash import dict_hash
from random_dict import random_dict
from random import randint

d = random_dict(randint(1, 10), randint(1, 10))
my_hash = dict_hash(d)
```

### Consistent hashes

Obtain a consistent hash from the given dictionary. Supported methods include `md5`, `sha256`, `sha1`, `sha224`, `sha384`, `sha512`, `sha3_512`, `shake_128`, `shake_256`, `sha3_384`, `sha3_256`, `sha3_224`, `blake2s`, `blake2b`, as provided from the `hashlib` library.

For instance, to obtain a sha256 hash from the given dictionary:

```python
from dict_hash import sha256
from random_dict import random_dict
from random import randint

d = random_dict(randint(1, 10), randint(1, 10))
my_hash = sha256(d)
```

The methods `shake_128` and `shake_256` expose the length paramater to specify the length of the hash digest.

```python
from dict_hash import shake_128
from random_dict import random_dict
from random import randint

d = random_dict(randint(1, 10), randint(1, 10))
my_hash = shake_128(d, hash_length=16)
```

### Approximated hash

All of the methods shown offer the `use_approximation` parameter,
which allows you to switch to a more lightweight hashing procedure
where supported, for the various supported objects. This procedure
will randomly subsample the provided objects.

Currently, we support this parameter for NumPy, Polars, and Pandas objects.

```python
from dict_hash import sha256
from random_dict import random_dict
from random import randint

d = random_dict(randint(1, 10), randint(1, 10))
my_hash = sha256(d)

approximated_hash = sha256(d, use_approximation=True)
```

### Behavior on error

If the hashing function encounters an object that it cannot hash,
it will by default raise a `NotHashableException` exception. You
can choose whether this or other options happen by setting the
`behavior_on_error` parameter. You can choose between:

- `raise`: Raise a `NotHashableException` exception.
- `warn`: Print a `NotHashableWarning` and continue hashing, setting the unhashable object to `"Unhashable object"` string.
- `ignore`: Ignore the object and continue hashing, setting the unhashable object to `"Unhashable object"` string.

### Recursive objects

In Python it is possible to have recursive objects, such as a dictionary that contains itself.
When you attempt to hash such an object, the hashing function will raise a `RecursionError` exception,
which you can customize with the `maximal_recursion` parameter, by default equal to `100`. The
`RecursionError` is most commonly then handled as a `NotHashableException`, and as such you can
set the `behavior_on_error` parameter to handle it as you see fit.

### Hashable

When handling complex objects within the dictionaries, you may need to implement
the class Hashable in that object.

Here is an example:

```python
from dict_hash import Hashable, sha256

class MyHashable(Hashable):

    def __init__(self, a: int):
        self._a = a
        self._time = time()

    def consistent_hash(self, use_approximation: bool = False) -> str:
        # The use approximation would be useful when the object is too large,
        # while in this example it may be a bit pointless.
        if use_approximation:
            return sha256({
                "a": self._a
            }, use_approximation=True)
        return sha256({
            "a": self._a
        })
```

## License

This software is distributed under the MIT license.
