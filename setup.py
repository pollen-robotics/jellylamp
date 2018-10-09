#!/usr/bin/env python

import imp

from setuptools import setup, find_packages

version = imp.load_source('jellylamp.version', 'jellylamp/version.py')

setup(
    name='jellylamp',
    version=version.version,
    packages=find_packages(),

    install_requires=[
        'pypot',
    ],

    extra_require={
        'tests': [],
    },

    author='Pollen Robotics',
    author_email='contact@pollen-robotics.com',
    description='Python library for controlling the Jelly fish lamp.',
    url='https://github.com/pollen-robotics/jellylamp',
    license='Apache License Version 2.0',
)
