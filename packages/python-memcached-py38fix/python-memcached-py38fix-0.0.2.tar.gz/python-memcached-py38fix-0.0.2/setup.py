#!/usr/bin/env python

from setuptools import setup  # noqa


setup(
    name="python-memcached-py38fix",
    version="0.0.2",
    description="A fork of python-memcached, but fix python3.8 syntax warning",
    long_description=open("README.md").read(),
    author="knktc",
    author_email="me@knktc.com",
    url="https://github.com/knktc/python-memcached",
    py_modules=["memcache"],
    install_requires=open('requirements.txt').read().split(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Python Software Foundation License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
