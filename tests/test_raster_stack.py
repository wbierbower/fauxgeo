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
        """Setup."""
        proj = 4326
        datatype = gdal.GDT_Float32
        nodata_val = -9999
        rows = 2
        cols = 2
        affine_one = Affine(1.0, 0.0, 3.0, 0.0, -1.0, 3.0)
        affine_offset = Affine(1.0, 0.0, 3.2, 0.0, -1.0, 3.2)
        self.rf1 = RasterFactory(
            4326, datatype, nodata_val, rows, cols, affine=affine_one)
        self.rf2 = RasterFactory(
            32633, datatype, nodata_val, rows, cols, affine=affine_one)
        self.rf3 = RasterFactory(
            32633, datatype, nodata_val, rows, cols, affine=affine_offset)

    def test_assert_same_projection(self):
        """Test assertion function that rasters are in same projection."""
        same_proj_stack = RasterStack(
            [self.rf1.uniform(1), self.rf1.uniform(1)])
        self.assertTrue(same_proj_stack.assert_same_projection())
        diff_proj_stack = RasterStack(
            [self.rf1.uniform(1), self.rf2.uniform(1)])
        self.assertFalse(diff_proj_stack.assert_same_projection())

    def test_assert_aligned(self):
        """Test assertion function that rasters are aligned."""
        same_proj_stack = RasterStack(
            [self.rf1.uniform(1), self.rf1.uniform(1)])
        self.assertTrue(same_proj_stack.assert_same_alignment())
        diff_proj_stack = RasterStack(
            [self.rf2.uniform(1), self.rf3.uniform(1)])
        self.assertFalse(diff_proj_stack.assert_same_alignment())

    def test_assert_resample_methods_assigned(self):
        """Test that resample methods are assigned to each raster in stack."""
        diff_proj_stack = RasterStack(
            [self.rf2.uniform(1), self.rf3.uniform(1)])
        self.assertFalse(diff_proj_stack.assert_resample_methods_assigned())
        for r in diff_proj_stack.raster_list:
            r.resample_method = 'nearest'
        self.assertTrue(diff_proj_stack.assert_resample_methods_assigned())

    def test_align(self):
        """Test align function."""
        diff_proj_stack = RasterStack(
            [self.rf2.uniform(1), self.rf3.uniform(1)])
        for r in diff_proj_stack.raster_list:
            r.resample_method = 'nearest'
        new_stack = diff_proj_stack.align()
        self.assertFalse(diff_proj_stack.assert_same_alignment())
        self.assertTrue(new_stack.assert_same_alignment())
        self.assertTrue(new_stack.raster_list[0][:].all() == 1.0)
        self.assertTrue(new_stack.raster_list[1][:].all() == 1.0)

    def test_set_standard_nodata(self):
        """Test set standard nodata."""
        same_proj_stack = RasterStack(
            [self.rf1.uniform(1), self.rf1.uniform(1)])
        new_stack = same_proj_stack.set_standard_nodata(-9998)
        self.assertTrue(new_stack.raster_list[0].get_nodata(1) == -9998)

    def test_align_and_set_standard_nodata(self):
        diff_proj_stack = RasterStack(
            [self.rf2.uniform(1), self.rf3.uniform(1)])
        for r in diff_proj_stack.raster_list:
            r.resample_method = 'nearest'
        new_stack = diff_proj_stack.align()
        new_stack = new_stack.set_standard_nodata(-9998)
        self.assertTrue(new_stack.assert_same_alignment())
        self.assertTrue(new_stack.raster_list[0].get_nodata(1) == -9998)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
