#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

name = 'tensor_algebra_dont_use'

setup(
    name=name,
    author='Dojo_team_1',
    version='0.0.1',
    packages=find_packages(),
    package_dir={name: name},
    include_package_data=True,
    license='MIT',
    description='bla',
    long_description='bla bla',
    install_requires=['sympy>=1.8',
                      'numpy>=1.17.0',
                      ],
    python_requires=">=3.6"
)