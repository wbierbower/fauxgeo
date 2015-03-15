#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_raster
----------------------------------

Tests for Raster class.
"""

import unittest
import os

import numpy as np
from affine import Affine
import gdal

from fauxgeo import Raster, TestRaster, RasterFactory


class Test_Raster(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 3)
        self.array = np.ones(self.shape)
        self.affine = Affine.identity()
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999

        self.raster = Raster(None)
        self.raster.init(self.array, self.affine, self.proj, self.datatype, self.nodata_val)

    def test_get_functions(self):
        assert(self.raster.get_shape() == self.shape)
        np.testing.assert_array_equal(self.raster.get_band(1), self.array)

    def test_set_functions(self):

        pass

    def tearDown(self):
        os.remove(self.raster.uri)


class Test_TestRaster(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 3)
        self.array = np.ones(self.shape)
        self.affine = Affine.identity()
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999

        self.raster_del = TestRaster(self.array, self.affine, self.proj, self.datatype, self.nodata_val)

    def test_raster_deletion(self):
        uri = self.raster_del.uri
        assert(os.path.exists(uri))
        del self.raster_del
        assert(not os.path.exists(uri))

    def tearDown(self):
        pass


class Test_RasterFactory(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 3)
        self.affine = Affine.identity()
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999

        self.Factory = RasterFactory(
            self.proj,
            self.datatype,
            self.nodata_val,
            self.shape[0],
            self.shape[1],
            affine=self.affine)

    def test_raster_creation(self):
        r = self.Factory.filled_ramp_across_rows(10, 6)
        assert(r.get_band(1)[0, 0] == 10)

    def test_raster_deletion(self):
        r = self.Factory.filled_value(5)
        uri = r.uri
        assert(os.path.exists(uri))
        del r
        assert(not os.path.exists(uri))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
