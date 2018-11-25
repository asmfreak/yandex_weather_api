#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import os
import re

root = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name='yandex_weather_api',
    version="0.0.1",
    url='https://github.com/cdgriffith/Box',
    license='GPLv3',
    author='Pavel Pletenev',
    tests_require=["pytest", "coverage >= 3.6", "tox", "pytest-cov"],
    install_requires=["voluptuous", "python-box", "aiohttp"],
    author_email='cpp.create@gmail.com',
    description='Yandex Weather API python module',
    long_description=long_description,
    py_modules=['aio_yandex_weather'],
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
