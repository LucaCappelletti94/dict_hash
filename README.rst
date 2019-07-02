dict_hash
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Simple python tool to hash dictionaries using both default hash and sha256.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install dict_hash

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
----------------------------------------------
The package offers two functions: `sha256` to generate constant sha256 hashes and `dict_hash`, to generate hashes using the native `hash` function.

dict_hash
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dict_hash import dict_hash
    from random_dict import random_dict
    from random import randint

    d = random_dict(randint(1, 10), randint(1, 10))
    my_hash = dict_hash(d)


sha256
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from dict_hash import sha256
    from random_dict import random_dict
    from random import randint

    d = random_dict(randint(1, 10), randint(1, 10))
    my_hash = sha256(d)

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

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/d2954938378a4e4087ebac09b0e50f9e
    :target: https://www.codacy.com/app/LucaCappelletti94/dict_hash?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/dict_hash&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/15f94bb26de6423d38f9/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/dict_hash/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/15f94bb26de6423d38f9/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/dict_hash/test_coverage
    :alt: Code Climate Coverate