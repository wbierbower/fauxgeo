#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

# import multiprocessing

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    "numpy",
    "affine",
    "gdal",
    "shapely",
    "pygeoprocessing",
    "wheel",
    "pyproj",
    "pillow"
]

test_requirements = [
    # TODO: put package test requirements here
    "numpy",
    "affine",
    "gdal",
    "shapely",
    "pygeoprocessing",
    "wheel",
    "pyproj",
    "pillow",
    "nose",
    "coverage"
]

setup(
    name='fauxgeo',
    version='0.2.0',
    description='A python library that generates fake geospatial data',
    long_description=readme + '\n\n' + history,
    author='Will B',
    author_email='wbierbower@gmail.com',
    url='https://github.com/wbierbower/fauxgeo',
    packages=find_packages(),
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='fauxgeo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    extras_require={
        'tests': test_requirements
    }
)
