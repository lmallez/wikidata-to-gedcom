#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='wikidata-to-gedcom',
    version='0.0.1',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)