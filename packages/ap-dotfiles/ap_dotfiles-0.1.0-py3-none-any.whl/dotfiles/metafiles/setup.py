#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# ??????  extends builtin min and max functions.
# Copyright (C) 2021 alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################
"""Setup Module."""

import json

from importlib_metadata import entry_points
from setuptools import find_packages, setup

INFO = json.load(open("./package.json"))

with open("README.md", encoding="UTF-8") as readme:
    long_description = readme.read()

setup(
    name=INFO["name"],
    version=INFO["version"],
    description=INFO["description"],
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=INFO["keywords"],
    author=INFO["author"],
    author_email=INFO["email"],
    url=INFO["url"],
    project_urls={"Source Code": "https://github.com/alexpdev/dotfiles"},
    license=INFO["license"],
    packages=find_packages(exclude=["env"]),
    entry_points={"console_scripts": ["dotfiles = dotfiles:main"]},
    include_package_data=True,
    zip_safe=False,
    test_suite="complete",
)
