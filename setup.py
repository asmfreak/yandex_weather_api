#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
yandex_weather_api - Yandex Weather API python module.

Copyright 2018 Pavel Pletenev <cpp.create@gmail.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from setuptools import setup

with open("README.md", "r") as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setup(
    name='yandex_weather_api',
    version="0.2.4",
    url='https://github.com/ASMfreaK/yandex_weather_api',
    license='GPLv3',
    author='Pavel Pletenev',
    tests_require=["pytest", "coverage >= 3.6", "tox", "pytest-cov"],
    install_requires=["voluptuous", "python-box", "aiohttp"],
    author_email='cpp.create@gmail.com',
    description='Yandex Weather API python module',
    long_description=LONG_DESCRIPTION,
    packages=['yandex_weather_api'],
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
