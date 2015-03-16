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


Usage
-----

The Raster Class

.. code:: python
	
	raster = Raster('path/to/geotiff')
	raster.uri  # equals '/path/to/geotiff'
	raster.get_band(1)  # returns 2d numpy array
	raster.get_bands()  # returns 3d numpy array
	raster.get_nodata()  # returns nodata value
	raster.shape()  # returns 2-tuple (rows, cols)

The TestRaster Class

.. code:: python

	import numpy as np
	from affine import Affine
	import gdal

	# set arguments
	array = np.ones((3, 3))
	affine = Affine.identity()
	proj = 4326
	datatype = gdal.GDT_Float64
	nodata_val = -9999.0

	# uses tempfile to create temporary file
	test_raster = TestRaster(array, affine, proj, datatype, nodata_val)

	# same functions as Raster class
	raster.get_band(1)  # returns 2d numpy array
	raster.get_bands()  # returns 3d numpy array
	raster.get_nodata()  # returns nodata value
	raster.shape()  # returns 2-tuple (rows, cols)	

	del test_raster  # cleans up temporary file on object deletion or program exit


The RasterFactory Class

.. code:: python

    from affine import Affine
    import gdal

    # set arguments
    shape = (3, 3)
    affine = Affine.identity()
    proj = 4326
    datatype = gdal.GDT_Float64
    nodata_val = -9999

    # initialize factory
    factory = RasterFactory(proj, datatype, nodata_val, shape[0], shape[1], affine=affine)

    # create test rasters
    test_raster_1 = factory.uniform(5)  # returns raster with 1 band filled with 5's
    test_raster_2 = factory.alternating(0, 1)
    test_raster_3 = factory.random()
    test_raster_3 = factory.horizontal_ramp(1, 10)  # interpolated from 1 to 10 across columns

Tests
-----

.. code::
	
	python setup.py test

Planning
--------

* Add basic visualization functionality
* Add Vector, TestVector, and VectorFactory classes
* Add sample/default arguments for Raster classes to simplify raster creation
