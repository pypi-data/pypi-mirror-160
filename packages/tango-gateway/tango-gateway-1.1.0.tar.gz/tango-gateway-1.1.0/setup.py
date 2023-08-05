#!/usr/bin/env python3

# Imports
from setuptools import setup


# Read function
def safe_read(fname):
    try:
        return open(fname).read()
    except IOError:
        return ""


# Setup
setup(
    name="tango-gateway",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    packages=["tangogateway"],
    entry_points={"console_scripts": ["tango-gateway = tangogateway:main"]},
    license="GPLv3",
    install_requires=["aiozmq"],
    description="A Tango gateway server",
    long_description=safe_read("README.md"),
    long_description_content_type="text/markdown",
    keywords="Tango",
    author="Vincent Michel",
    author_email="vincent.michel@maxlab.lu.se",
    url="https://gitlab.com/MaxIV/tango-gateway",
)
