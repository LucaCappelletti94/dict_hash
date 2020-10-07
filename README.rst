dict_hash
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Simple python tool to hash dictionaries using both default hash and sha256.
The library comes with full support for hashing Pandas DataFrame objects,
Numba objects and Numpy arrays, but you will need to specify the requirements
when installing the package to avoid bloating the installation process.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install dict_hash[all] # To install everything
    pip install dict_hash[numba] # To install with numba support
    pip install dict_hash[numpy] # To install with numpy support
    pip install dict_hash[pandas] # To install with pandas support


Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

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

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/dict_hash.png
   :target: https://travis-ci.org/LucaCappelletti94/dict_hash
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_dict_hash&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_dict_hash
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_dict_hash&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_dict_hash
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_dict_hash&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_dict_hash
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/dict_hash/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/dict_hash?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/dict-hash.svg
    :target: https://badge.fury.io/py/dict-hash
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/dict-hash
    :target: https://pepy.tech/badge/dict-hash
    :alt: Pypi total project downloads 

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/d2954938378a4e4087ebac09b0e50f9e
    :target: https://www.codacy.com/app/LucaCappelletti94/dict_hash?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/dict_hash&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/15f94bb26de6423d38f9/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/dict_hash/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/15f94bb26de6423d38f9/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/dict_hash/test_coverage
    :alt: Code Climate Coverate
