=======
Fauxgeo
=======

.. image:: https://badge.fury.io/py/fauxgeo.png
    :target: http://badge.fury.io/py/fauxgeo

.. image:: https://travis-ci.org/wbierbower/fauxgeo.png?branch=master
        :target: https://travis-ci.org/wbierbower/fauxgeo

.. image:: https://readthedocs.org/projects/fauxgeo/badge/?version=latest
        :target: https://readthedocs.org/projects/fauxgeo/?badge=latest
        :alt: Documentation Status


A python library that generates simple OSGeo-supported rasters and vectors.  The primary purpose for this library is to help test geoprocessing functions.

* Free software: BSD license
* Documentation: https://fauxgeo.readthedocs.org.

Requirements
------------

fauxgeo 0.1.1 requires

* NumPy
* GDAL
* affine == 1.0

Installation
------------

.. code::

	pip install fauxgeo

Features
--------

* Raster Class
* TestRaster Class
* RasterFactory Class


Tests
-----

.. code::
	
	python setup.py test

Planning
--------

* Add basic visualization functionality
* Add Vector, TestVector, and VectorFactory classes

