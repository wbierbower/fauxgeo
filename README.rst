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

fauxgeo 0.2.0 requires

* NumPy
* Matplotlib
* GDAL
* affine == 1.0

Installation
------------

.. code::

    pip install fauxgeo

Features
--------

* Raster Class
* RasterFactory Class
* Vector Class
* VectorFactory Class

Usage
-----

The Raster Class

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

    # initialize raster
    raster = Raster.from_array(array, affine, proj, datatype, nodata_val)   
    raster = Raster.from_file('path/to/geotiff')

    raster.uri  # equals '/path/to/geotiff'
    raster.driver  # e.g. 'GTiff'
    raster.dataset

    raster.get_band(1)  # returns 2d numpy masked array
    raster.get_bands()  # returns 3d numpy masked array
    raster.get_nodata()  # returns nodata value
    raster.get_shape()  # returns 2-tuple (rows, cols)
    raster.get_projection()
    raster.get_affine()
    raster.get_bounding_box()
    raster.get_cell_area()

    raster2 = raster1.set_datatype(gdal.GDT_Int32)
    raster2 = raster1.set_nodata(-9999)
    raster2 = raster1.set_datatype_and_nodata(gdal.GDT_Int32, -9999)
    
    # Operations
    raster3 = raster1.align(raster2)
    raster3 = raster1.align_to(raster2)
    assert(raster3.is_aligned(raster2))

    raster4 = raster3 * raster2
    raster4 = raster3 / raster2
    raster4 = raster3 + raster2
    raster4 = raster3 - raster2
    raster4 = raster3 ** raster2

    raster4 = raster3 * 4.5
    raster4 = 4.5 / raster3
    raster4 = raster3 + 4.5
    raster4 = 4.5 - raster3
    raster4 = raster3 ** 4.5

    raster4 = raster3.minimum(raster2)

    # returns base rasters with same nodata and datatype
    zeros_raster = raster3.zeros()  
    ones_raster = raster3.ones()

    raster4 = raster3.clip('/path/to/aoi_shapefile')
    raster4 = raster3.reproject(epsg_code)

    reclass_table = {
        1: 2,
        2: 1
    }
    raster4 = raster3.reclass(reclass_table)

    raster4 = raster3.resize_pixels(pixel_size, resample_method)

    # visualization
    image = raster4.get_grayscale_image()  # returns PIL Image object

    raster.save_raster('/path/to/dst.tif')
    del raster  # cleans up temporary file on object deletion or program exit


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
    test_raster_4 = factory.horizontal_ramp(1, 10)  # interpolated from 1 to 10 across columns
    test_raster_5 = factory.vertical_ramp(1, 10)  # interpolated from 1 to 10 across rows

The Vector Class

.. code:: python

    from shapely.geometry import *

    # set arguments
    shapely_object = Polygon([(0, 0), (0, 1), (1, 1)])
    proj = 4326

    # initialize vector
    vector = Vector.from_shapely(shapely_object, proj)
    vector = Vector.from_file('/path/to/shapefile')

    shapely_object = vector.get_geometry()

    vector.save_vector('/path/to/dst.shp')
    del vector



Tests
-----

.. code::
    
    python setup.py test

Planning
--------

* Add basic visualization functionality
* Raster Operations
    * Reclass
    * Overlay - intersection, union, clip
    * Dissolve
    * Buffer
    * Raster_to_Vector
    * Slope
    * Aspect
