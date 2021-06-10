#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup
except:
    from distutils.core import setup

try:
    with open('README.rst') as readme_file:
        readme = readme_file.read()

    with open('HISTORY.rst') as history_file:
        history = history_file.read()
except IOError:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
        readme = readme_file.read()

    with open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')) as history_file:
        history = history_file.read()

requirements = ['numpy', 'scipy']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Johannes Buchner",
    author_email='johannes.buchner.acad@gmx.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Poisson error bars for low count statistics, detection significances.",
    install_requires=requirements,
    license="MIT",
    long_description=readme + '\n\n' + history,
    keywords='poissonregime',
    name='poissonregime',
    py_modules=['poissonregime'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/JohannesBuchner/poissonregime',
    version='0.1.0',
)
