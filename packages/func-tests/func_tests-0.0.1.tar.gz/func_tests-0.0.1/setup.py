#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]


setup(
    author="Andrii Kovalov",
    author_email='andy.kovv@gmail.com',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
    ],
    description="Fast debug tools",
    long_description=readme,
    include_package_data=True,
    keywords='func_tests',
    name='func_tests',
    packages=find_packages(include=['func_test']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='0.0.1',
    zip_safe=False,
)
