#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_rasterfactory
----------------------------------

Tests for RasterFactory class.
"""

import unittest
import os
import tempfile

import numpy as np
# from affine import Affine
from fauxgeo.affine import Affine
import gdal

from fauxgeo.raster_factory import RasterFactory


class TestRasterFactory(unittest.TestCase):

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
        r = self.Factory.horizontal_ramp(10, 6)
        assert(r.get_band(1)[0, 0] == 10)

    def test_raster_deletion(self):
        r = self.Factory.uniform(5)
        uri = r.uri
        assert(os.path.exists(uri))
        del r
        assert(not os.path.exists(uri))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
