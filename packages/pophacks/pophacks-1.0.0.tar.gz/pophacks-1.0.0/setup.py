from distutils.core import setup
from setuptools import find_packages

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from consts import AUTHOR, AUTHOR_EMAIL, DESCRIPTION, MAINTAINER, MAINTAINER_EMAIL, NAME, VERSION


with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,

    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,

    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,

    url="https://github.com/shreyass-ranganatha/pophacks.git",

    keywords=[
        "hack",
        "popular",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Other Audience",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Utilities"
    ],

    package_dir={
        "pophacks": "."
    },
    packages=[
        "pophacks.monkeytype"
    ],
    py_modules=[
        "pophacks.consts"
    ],
    scripts=[
        "scripts/pophacks"
    ],
    python_requires=">=3.2"
)
