#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tempraster
----------------------------------

Tests for TempRaster class.
"""

import unittest
import os
import tempfile

import numpy as np
from affine import Affine
import gdal

from fauxgeo.temp_raster import TempRaster


class Test_TempRaster(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 3)
        self.array = np.ones(self.shape)
        self.affine = Affine.identity()
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999

        self.raster_del = TempRaster.from_array(
            self.array, self.affine, self.proj, self.datatype, self.nodata_val)

    def test_raster_deletion(self):
        uri = self.raster_del.uri
        assert(os.path.exists(uri))
        del self.raster_del
        assert(not os.path.exists(uri))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
