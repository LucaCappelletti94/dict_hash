"""Setup to install the package."""

import os
import re

# To use a consistent encoding
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def read(*parts):
    with open(os.path.join(here, *parts), "r", encoding="utf-8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("dict_hash", "__version__.py")

test_deps = [
    "pytest",
    "pytest-cov",
    "validate_version_code",
    "random_dict",
    "pytest-readme",
    "netaddr",
]

extras = {"test": test_deps}

setup(
    name="dict_hash",
    version=__version__,
    description="Python package to hash dictionaries using default hash, md5, sha256 and more.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LucaCappelletti94/dict_hash",
    author="Luca Cappelletti",
    author_email="cappelletti.luca94@gmail.com",
    # Choose your license
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    tests_require=test_deps,
    install_requires=[
        "deflate_dict>=1.0.8",
    ],
    extras_require=extras,
)
