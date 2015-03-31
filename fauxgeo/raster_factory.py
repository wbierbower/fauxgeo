'''
RasterFactory Class
'''

import numpy as np
from affine import Affine

from fauxgeo.raster import Raster
from fauxgeo.temp_raster import TempRaster


class RasterFactory(object):

    def __init__(self, proj, datatype, nodata_val, rows, cols, affine=Affine.identity):
        self.proj = proj
        self.datatype = datatype
        self.nodata_val = nodata_val
        self.rows = rows
        self.cols = cols
        self.affine = affine

    def get_metadata(self):
        meta = {}
        meta['proj'] = self.proj
        meta['datatype'] = self.datatype
        meta['nodata_val'] = self.nodata_val
        meta['rows'] = self.rows
        meta['cols'] = self.cols
        meta['affine'] = self.affine
        return meta

    def _create_raster(self, array, uri):
        if uri is None:
            return TempRaster.from_array(
                array, self.affine, self.proj, self.datatype, self.nodata_val)
        else:
            return Raster.from_file(
                uri, array, self.affine, self.proj, self.datatype, self.nodata_val)

    def uniform(self, val, uri=None):
        a = np.ones((self.rows, self.cols)) * val
        return self._create_raster(a, uri)

    def alternating(self, val1, val2, uri=None):
        a = np.ones((self.rows, self.cols)) * val2
        a[::2, ::2] = val1
        a[1::2, 1::2] = val1
        return self._create_raster(a, uri)

    def random(self, uri=None):
        a = np.random.rand(self.rows, self.cols)
        return self._create_raster(a, uri)

    def horizontal_ramp(self, val1, val2, uri=None):
        a = np.zeros((self.rows, self.cols))
        col_vals = np.linspace(val1, val2, self.cols)
        a[:] = col_vals
        return self._create_raster(a, uri)

    def vertical_ramp(self, val1, val2, uri=None):
        a = np.zeros((self.cols, self.rows))
        row_vals = np.linspace(val1, val2, self.rows)
        a[:] = row_vals
        a = a.T
        return self._create_raster(a, uri)

    # def bell_shape(self, uri=None):
