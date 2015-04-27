#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_raster
----------------------------------

Tests for Raster class.
"""

import unittest
import os
import tempfile

import numpy as np
from affine import Affine
import gdal

from fauxgeo import Raster
from fauxgeo import RasterFactory


class TestRasterGetAndAlign(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, 1, 0)
        self.misaligned_affine = Affine(1, 0, 0, 0, 1, 1)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999

        self.raster = Raster.from_array(
            self.array, self.affine, self.proj, self.datatype, self.nodata_val)
        self.aligned_raster = Raster.from_array(
            np.zeros(self.shape), self.affine, self.proj, self.datatype, self.nodata_val)
        self.misaligned_raster = Raster.from_array(
            self.array, self.misaligned_affine, self.proj, self.datatype, self.nodata_val)

    def test_get_functions(self):
        assert(self.raster.get_rows() == self.shape[0])
        assert(self.raster.get_cols() == self.shape[1])
        assert(self.raster.get_shape() == self.shape)
        np.testing.assert_array_equal(self.raster.get_band(1), self.array)
        np.testing.assert_array_equal(
            self.raster.get_bands(), np.array([self.array]))
        assert(self.raster.get_nodata(1) == self.nodata_val)
        assert(self.raster.get_datatype(1) == self.datatype)
        assert(self.raster.get_geotransform() == self.affine.to_gdal())
        assert(self.raster.get_affine() == self.affine)
        assert(self.raster.get_projection() == 4326)

    def test_is_aligned(self):
        assert(self.raster.is_aligned(self.aligned_raster) == True)
        assert(self.raster.is_aligned(self.misaligned_raster) == False)

    def test_align(self):
        assert(self.raster.is_aligned(self.misaligned_raster) == False)
        new_raster = self.raster.align(self.misaligned_raster, "nearest")
        assert(self.raster.is_aligned(new_raster) == True)

    def test_align_to(self):
        assert(self.raster.is_aligned(self.misaligned_raster) == False)
        new_raster = self.misaligned_raster.align_to(self.raster, "nearest")
        assert(self.raster.is_aligned(new_raster) == True)


class TestRasterCopy(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_copy(self):
        a = self.factory.uniform(1)
        b = a.copy()
        assert(a.uri != b.uri)
        assert(a.is_aligned(b))


class TestRasterMath(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_add(self):
        a = self.factory.alternating(1.0, 2.0)
        b = a + a
        assert(b.get_band(1)[0, 0] == 2)

    def test_sub(self):
        a = self.factory.alternating(1.0, 2.0)
        b = a - a
        assert(b.get_band(1)[0, 0] == 0)

    def test_mul(self):
        a = self.factory.alternating(2.0, 3.0)
        b = a * a
        assert(b.get_band(1)[0, 0] == 4)

    def test_div(self):
        a = self.factory.alternating(2.0, 3.0)
        b = a / a
        assert(b.get_band(1)[0, 0] == 1)

    def test_pow(self):
        a = self.factory.alternating(2.0, 3.0)
        b = a ** a
        assert(b.get_band(1)[0, 0] == 4)

    def test_radd(self):
        a = self.factory.alternating(2.0, 3.0)
        b = 4 + a
        assert(b.get_band(1)[0, 0] == 6)

    def test_rsub(self):
        a = self.factory.alternating(2.0, 3.0)
        b = 4 - a
        assert(b.get_band(1)[0, 0] == 2)

    def test_rmul(self):
        a = self.factory.alternating(2.0, 3.0)
        b = 4 * a
        assert(b.get_band(1)[0, 0] == 8)

    def test_rdiv(self):
        a = self.factory.alternating(2.0, 3.0)
        b = 4 / a
        assert(b.get_band(1)[0, 0] == 2)

    def test_rpow(self):
        a = self.factory.alternating(2.0, 3.0)
        b = 4 ** a
        assert(b.get_band(1)[0, 0] == 8)


class TestRasterReclass(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_reclass(self):
        pass


class TestRasterClip(unittest.TestCase):
    pass


class TestRasterBoundingBox(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
