import os

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from setuptools import find_packages, setup

from pymatic import __version__


def read(fname):
    """Read the content of the file `fname`."""
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name="pymatic",
    version=__version__,
    description="Fetch Log Analytics alerts and raise them in TheHive",
    author="santal",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
    entry_points={"console_scripts": ["pymatic=pymatic.main:cli"]},
)
