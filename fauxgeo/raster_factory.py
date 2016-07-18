"""RasterFactory Class."""

import random

import numpy as np

from fauxgeo.affine import Affine
from fauxgeo.raster import Raster


class RasterFactory(object):

    """A class to generate raster objects."""

    def __init__(self, proj, datatype, nodata_val, rows, cols, affine=Affine.identity()):
        """Construct RasterFactory object."""
        self.proj = proj
        self.datatype = datatype
        self.nodata_val = nodata_val
        self.rows = rows
        self.cols = cols
        self.affine = affine

    def get_metadata(self):
        """Return metadata dictionary."""
        meta = {}
        meta['proj'] = self.proj
        meta['datatype'] = self.datatype
        meta['nodata_val'] = self.nodata_val
        meta['rows'] = self.rows
        meta['cols'] = self.cols
        meta['affine'] = self.affine
        return meta

    def _create_raster(self, array):
        return Raster.from_array(
            array, self.affine, self.proj, self.datatype, self.nodata_val)

    def uniform(self, val):
        """Return raster filled with uniform values."""
        a = np.ones((self.rows, self.cols)) * val
        return self._create_raster(a)

    def alternating(self, val1, val2):
        """Return raster filled with alternating values."""
        a = np.ones((self.rows, self.cols)) * val2
        a[::2, ::2] = val1
        a[1::2, 1::2] = val1
        return self._create_raster(a)

    def random(self):
        """Return raster filled with random values."""
        a = np.random.rand(self.rows, self.cols)
        return self._create_raster(a)

    def random_from_list(self, l):
        a = np.zeros((self.rows, self.cols))
        for i in xrange(len(a)):
            for j in xrange(len(a[0])):
                a[i, j] = random.choice(l)
        return self._create_raster(a)

    def horizontal_ramp(self, val1, val2):
        a = np.zeros((self.rows, self.cols))
        col_vals = np.linspace(val1, val2, self.cols)
        a[:] = col_vals
        return self._create_raster(a)

    def vertical_ramp(self, val1, val2):
        a = np.zeros((self.cols, self.rows))
        row_vals = np.linspace(val1, val2, self.rows)
        a[:] = row_vals
        a = a.T
        return self._create_raster(a)

    @staticmethod
    def create_sample_global_map():
        """Return a simple global map."""
        shape = (360, 180)
        datatype = 5
        nodata_val = -9999
        proj = 4326
        factory = RasterFactory(
            proj, datatype, nodata_val, shape[1], shape[0])
        return factory.uniform(1)

    @staticmethod
    def create_sample_aoi_map(datatype=0):
        """Return a simple global map."""
        shape = (10, 10)
        nodata_val = -9999
        proj = 32618
        factory = RasterFactory(
            proj, datatype, nodata_val, shape[1], shape[0])
        return factory.horizontal_ramp(1, 10)
