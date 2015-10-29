#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_raster_stack
----------------------------------

Tests for RasterStack class.
"""

import unittest
import os
import tempfile

import numpy as np
import gdal

from fauxgeo.affine import Affine
from fauxgeo.raster_factory import RasterFactory
from fauxgeo.raster_stack import RasterStack


class TestRasterStack(unittest.TestCase):

    def setUp(self):
        pass

    def test_assert_same_projection(self):
        proj = 4326
        datatype = gdal.GDT_Float32
        nodata_val = -9999
        rows = 2
        cols = 2
        rf1 = RasterFactory(4326, datatype, nodata_val, rows, cols, affine=Affine.identity())
        rf2 = RasterFactory(4236, datatype, nodata_val, rows, cols, affine=Affine.identity())

        same_proj_stack = RasterStack([rf1.uniform(1), rf1.uniform(1)])
        self.AssertTrue(same_proj_stack.assert_same_projection())
        diff_proj_stack = RasterStack([rf1.uniform(1), rf2.uniform(1)])
        self.AssertFalse(diff_proj_stack.assert_same_projection())

    # def test_align(self):
    #     pass
    #
    # def test_set_standard_nodata_and_dtype(self):
    #     pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
