#!/usr/bin/env python

import os
from pathlib import Path
import pkg_resources
from setuptools import setup, find_namespace_packages
import re

os.environ['PYTHON_EGG_CACHE'] = '.eggs'

with Path("urcv/__init__.py").open() as f:
    version = re.search('__version__\s*=\s*[\'"](.*)[\'"]\n', f.read()).group(1)

with Path("requirements.txt").open() as f:
    install_requires = [
        str(requirement)
        for requirement in pkg_resources.parse_requirements(f)
    ]

setup(
    name="urcv",
    version=version,
    packages=find_namespace_packages(),
    install_requires=install_requires,
    description="",
    author="",
    author_email="",
    url="https://github.com/chriscauley/urcv",
)
