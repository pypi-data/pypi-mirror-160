#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools


with open('README.md', 'r') as file:
    long_description = file.read()


meta = {}
with open('pytdi/meta.py') as file:
    exec(file.read(), meta)


setuptools.setup(
    name='pytdi',
    version=meta['__version__'],
    author=meta['__author__'],
    author_email=meta['__email__'],
    description="Python implementation of time-delay interferometry algorithms.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.in2p3.fr/LISA/LDPG/wg6_inrep/pytdi',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'packaging',
    ],
    tests_require=['pytest'],
    python_requires='>=3.6',
    license='BSD-3-Clause',
)
