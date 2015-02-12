#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    "numpy",
    "rasterio",
    "wheel"
]

test_requirements = [
    # TODO: put package test requirements here
    "numpy",
    "rasterio",
    "wheel"
]

setup(
    name='fauxgeodata',
    version='0.1.0',
    description='A python library that generates fake geospatial data',
    long_description=readme + '\n\n' + history,
    author='Will B',
    author_email='wbierbower@gmail.com',
    url='https://github.com/wbierbower/fauxgeodata',
    packages=find_packages(),
    package_dir={'fauxgeodata':
                 'fauxgeodata'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='fauxgeodata',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
