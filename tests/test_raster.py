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
# from affine import Affine
from fauxgeo.affine import Affine
import gdal

from fauxgeo import Raster
from fauxgeo import RasterFactory


class TestRasterGetAndAlign(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.misaligned_affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)
        self.misaligned_factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.misaligned_affine)

    def test_get_functions(self):
        a = self.factory.uniform(1.0)
        assert(a.get_rows() == self.shape[0])
        assert(a.get_cols() == self.shape[1])
        assert(a.get_shape() == self.shape)
        assert(a.get_nodata(1) == self.nodata_val)
        assert(a.get_datatype(1) == self.datatype)
        assert(a.get_geotransform() == self.affine.to_gdal())
        assert(a.get_affine() == self.affine)
        assert(a.get_projection() == 4326)

    def test_is_aligned(self):
        a = self.factory.uniform(1.0)
        b = self.factory.uniform(1.0)
        c = self.misaligned_factory.uniform(1.0)
        assert(a.is_aligned(b) == True)
        assert(a.is_aligned(c) == False)

    def test_align(self):
        a = self.factory.uniform(1.0)
        b = self.misaligned_factory.uniform(1.0)
        assert(a.is_aligned(b) == False)
        c = a.align(b, "nearest")
        assert(a.is_aligned(c) == True)

    def test_align_to(self):
        a = self.misaligned_factory.uniform(1.0)
        b = self.factory.uniform(1.0)
        assert(a.is_aligned(b) == False)
        c = a.align_to(b, "nearest")
        assert(b.is_aligned(c) == True)


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
        assert(b.get_band(1)[0, 0] == 16)


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
        a = self.factory.alternating(1.0, 2.0)
        reclass_dict = {1: 3, 2: 4}
        b = a.reclass(reclass_dict)
        assert(b.get_band(1)[0, 0] == 3)
        assert(b.get_band(1)[0, 1] == 4)


class TestRasterClip(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)


class TestRasterBoundingBox(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_bounding_box(self):
        a = self.factory.alternating(1.0, 2.0)
        assert(a.get_bounding_box() == [0.0, 3.0, 4.0, 0.0])


class TestRasterSetNodataAndDatatype(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_set_nodata(self):
        a = self.factory.alternating(1.0, 2.0)
        b = a.set_nodata(-1)
        assert(b.get_nodata(1) == -1)
        assert(a.uri != b.uri)

    def test_set_datatype(self):
        a = self.factory.alternating(1.0, 2.0)
        b = a.set_datatype(gdal.GDT_Int16)
        assert(b.get_datatype(1) == gdal.GDT_Int16)
        assert(a.uri != b.uri)

    def test_set_nodata_and_datatype(self):
        a = self.factory.alternating(1.0, 2.0)
        b = a.set_datatype_and_nodata(gdal.GDT_Int16, -1)
        assert(b.get_nodata(1) == -1)
        assert(b.get_datatype(1) == gdal.GDT_Int16)
        assert(a.uri != b.uri)


class TestRasterReproject(unittest.TestCase):
    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 3)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_reproject(self):
        # This test needs to be more rigorous
        a = self.factory.alternating(1.0, 2.0)
        b = a.reproject(32631, 'nearest', pixel_size=1000)
        assert(b.get_shape() == (333, 444))


class TestRasterResizePixels(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_resize_pixels(self):
        a = self.factory.alternating(1.0, 2.0)
        b = a.resize_pixels(0.5, 'nearest')
        assert(b.get_shape() == (8, 8))

if __name__ == '__main__':
    unittest.main()
