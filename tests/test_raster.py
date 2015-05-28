#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_raster
----------------------------------

Tests for Raster class.

python -m unittest test_raster
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


class TestRasterReclassMaskedValues(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_reclass_masked_values(self):
        new_value = 20
        masked_raster = self.factory.alternating(0, 1.0)
        raster = self.factory.uniform(np.nan)
        new_raster = raster.reclass_masked_values(masked_raster, new_value)
        assert(new_raster.get_band(1)[0, 0] == new_value)


class TestRasterZeros(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_zeros(self):
        raster = self.factory.alternating(-9999, 2.0)
        zero_raster = raster.zeros()
        assert(zero_raster.get_band(1)[0, 0] == 0)


class TestRasterOnes(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_zeros(self):
        raster = self.factory.alternating(-9999, 2.0)
        ones_raster = raster.ones()
        assert(ones_raster.get_band(1)[0, 0] == 1)


class TestRasterSetBand(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_set_band(self):
        raster = self.factory.alternating(-9999, 2.0)
        new_array = np.ma.ones((4, 4), fill_value=0)
        raster.set_band(1, new_array)
        assert(raster[0][0] == 1)


class TestRasterSetDatatype(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_set_datatype(self):
        raster = self.factory.alternating(-9999, 2.0)
        new_raster = raster.set_datatype(gdal.GDT_Int16)
        assert(new_raster.get_datatype(1) == gdal.GDT_Int16)


class TestRasterSetNoData(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_set_nodata(self):
        raster = self.factory.alternating(-9999, 2.0)
        new_raster = raster.set_nodata(100)
        assert(new_raster.get_nodata(1) == 100)
        assert(new_raster.get_band(1).data[0, 0] == 100.0)


class TestRasterSetDatatypeAndNoData(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_set_nodata(self):
        raster = self.factory.alternating(-9999, 2.0)
        new_raster = raster.set_datatype_and_nodata(gdal.GDT_Int16, 100)
        assert(new_raster.get_datatype(1) == gdal.GDT_Int16)
        assert(new_raster.get_nodata(1) == 100)
        assert(new_raster.get_band(1).data[0, 0] == 100)


class TestRasterStats(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_min(self):
        raster = self.factory.alternating(1.0, 2.0)
        assert(raster.min() == 1.0)

    def test_max(self):
        raster = self.factory.alternating(1.0, 2.0)
        assert(raster.max() == 2.0)

    def test_mean(self):
        raster = self.factory.alternating(1.0, 2.0)
        assert(raster.mean() == 1.5)

    def test_std(self):
        raster = self.factory.uniform(1.0)
        assert(raster.std() == 0.0)

    def test_sum(self):
        raster = self.factory.alternating(1.0, -9999)
        assert(raster.sum() == 8.0)


class TestRasterMinimum(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_minimum(self):
        raster1 = self.factory.alternating(1.0, 2.0)
        raster2 = self.factory.alternating(2.0, -9999)
        min_raster = raster1.minimum(raster2)
        assert(min_raster.get_band(1).data[0, 0] == 1)
        assert(min_raster.get_band(1).data[0, 1] == -9999)

    def test_fminimum(self):
        raster1 = self.factory.alternating(2.0, float('NaN'))
        raster2 = self.factory.alternating(1.0, 2.0)
        min_raster = raster1.fminimum(raster2)
        assert(min_raster.get_band(1).data[0, 0] == 1)
        assert(min_raster.get_band(1).data[0, 1] == 2)


class TestRasterUnique(unittest.TestCase):
    def setUp(self):
        self.shape = (4, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Int16
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_unique(self):
        raster = self.factory.horizontal_ramp(1, 4)
        assert(raster.unique() == [1, 2, 3, 4])


class TestRasterSlice(unittest.TestCase):
    def setUp(self):
        self.shape = (10, 10)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, -1, 4)
        self.proj = 4326
        self.datatype = gdal.GDT_Int16
        self.nodata_val = -9999
        self.factory = RasterFactory(
            self.proj, self.datatype, self.nodata_val, *self.shape, affine=self.affine)

    def test_get_slice(self):
        raster = self.factory.alternating(0, 1)
        a = raster[1:3]
        assert(a[0][0] == 1)

    def test_set_slice(self):
        raster = self.factory.alternating(0, 1)
        raster[1:9:2, 1:9:2] = 2
        assert(raster[1][3] == 2)


if __name__ == '__main__':
    unittest.main()
