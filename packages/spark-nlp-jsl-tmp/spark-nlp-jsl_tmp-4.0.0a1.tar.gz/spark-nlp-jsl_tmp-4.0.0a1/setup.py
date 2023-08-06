"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path
from util import read_version
import shutil

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

version=read_version.get_version_from_file('VERSION')
public_version=read_version.get_version_from_file('PUBLIC_VERSION')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="spark-nlp-jsl_tmp",  # Required
    version=version, # Required
    description="NLP Text processing library built on top of Apache Spark",  # Required
    long_description=long_description,  # Optional
    url="http://nlp.johnsnowlabs.com",  # Optional
    author="John Snow Labs",  # Optional
    author_email="john@johnsnowlabs.com",
    classifiers=[  # Optional
        "Programming Language :: Python :: 3.6",
    ],
    keywords="NLP spark development",  # Optional
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],

    packages=find_packages(exclude=["test_jsl"]),
    include_package_data=True,  # Needed to install jar file
)
