#!/usr/bin/env python

import imp
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 6):
    sys.exit("Sorry, Python < 3.6 is not supported")

VERSION = imp.load_source("", "matplotlib_ephys/version.py").__version__

# Read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="matplotlib-ephys",
    version=VERSION,
    description="Electrophysiology plotting functions",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU General Public License",
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    packages=find_packages(),
)
