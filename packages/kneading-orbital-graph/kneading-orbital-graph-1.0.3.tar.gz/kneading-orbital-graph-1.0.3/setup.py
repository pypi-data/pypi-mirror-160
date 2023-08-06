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

def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf8') as file:
        return file.read()


check_python_version()

setup(
    name=PACKAGE_NAME,
    version='1.0.3',
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'networkx',
        'matplotlib',
        'scipy',
    ],
    url='https://gitlab.com/dmartinez05/kneading_orbital_graph',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    classifiers=[
          'License :: OSI Approved :: Apache Software License',
    ],
)
