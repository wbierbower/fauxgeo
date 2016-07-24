#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='fauxgeo',
    version='0.3.0',
    description='programmatically generate geospatial rasters for testing',
    author='Will Bierbower',
    author_email='wbierbower@gmail.com',
    url='https://github.com/wbierbower/fauxgeo',
    packages=find_packages(),
    install_requires=required,
    license="BSD",
    zip_safe=False,
    keywords='fauxgeo',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests'
)
