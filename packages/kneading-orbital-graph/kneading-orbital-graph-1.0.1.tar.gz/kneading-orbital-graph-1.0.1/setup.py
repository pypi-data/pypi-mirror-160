import os
import os.path
import sys
from setuptools import setup, find_packages
import subprocess

PACKAGE_NAME = 'kneading-orbital-graph'
MINIMUM_PYTHON_VERSION = 3, 6


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {}.{}+ is required.".format(*MINIMUM_PYTHON_VERSION))

check_python_version()
setup(
    name=PACKAGE_NAME,
    version='1.0.1',
    packages=find_packages(exclude=['tests*']),
    license='Apache-2.0',
    classifiers=[
          'License :: OSI Approved :: Apache Software License',
    ],
    install_requires=[
        'networkx',
        'matplotlib',
        'scipy',
    ]
)
