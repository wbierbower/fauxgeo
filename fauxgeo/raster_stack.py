"""RasterStack Class."""

import os
import shutil
import logging

try:
    import gdal
    import ogr
    import osr
except ImportError:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr

import numpy as np
from shapely.geometry import Polygon
import shapely
import pygeoprocessing as pygeo

from fauxgeo.vector import Vector
from fauxgeo.affine import Affine

LOGGER = logging.getLogger('RasterStack Class')
logging.basicConfig(format='%(asctime)s %(name)-15s %(levelname)-8s \
    %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %H/%M/%S')


class RasterStack(object):

    """A class for interacting with gdal raster files."""

    def __init__(self, raster_list):
        self.raster_list = raster_list

    def assert_same_projection(self):
        pass

    def align(self):
        pass

    def set_standard_nodata_and_dtype(self):
        pass
