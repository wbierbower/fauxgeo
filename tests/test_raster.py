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

from fauxgeo.raster import Raster


class Test_Raster(unittest.TestCase):

    def setUp(self):
        self.shape = (3, 4)
        self.array = np.ones(self.shape)
        self.affine = Affine(1, 0, 0, 0, 1, 0)
        self.misaligned_affine = Affine(1, 0, 0, 0, 1, 1)
        self.proj = 4326
        self.datatype = gdal.GDT_Float64
        self.nodata_val = -9999
        t = tempfile.NamedTemporaryFile(mode='w+')
        t_aligned = tempfile.NamedTemporaryFile(mode='w+')
        t_misaligned = tempfile.NamedTemporaryFile(mode='w+')
        t.close()
        t_aligned.close()
        t_misaligned.close()
        self.raster = Raster.from_array(
            t.name, self.array, self.affine, self.proj, self.datatype, self.nodata_val)
        self.aligned_raster = Raster.from_array(
            t_aligned.name, np.zeros(self.shape), self.affine, self.proj, self.datatype, self.nodata_val)
        self.misaligned_raster = Raster.from_array(
            t_misaligned.name, self.array, self.misaligned_affine, self.proj, self.datatype, self.nodata_val)

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

    def test_set_functions(self):
        a = np.ma.masked_equal(np.zeros((self.shape)), 1)
        self.raster.set_band(a)
        np.testing.assert_array_equal(self.raster.get_band(1), a)

    def test_is_aligned(self):
        assert(self.raster.is_aligned(self.aligned_raster) == True)
        assert(self.raster.is_aligned(self.misaligned_raster) == False)

    def test_align(self):
        print self.misaligned_raster
        assert(self.raster.is_aligned(self.misaligned_raster) == False)
        self.raster.align(self.misaligned_raster, "nearest")
        print self.misaligned_raster
        assert(self.raster.is_aligned(self.misaligned_raster) == True)

    def test_clip(self):
        pass

    def test_project(self):
        pass

    def test_reclass(self):
        pass

    def test_overlay(self):
        pass

    def test_copy(self):
        pass

    def test_to_vector(self):
        pass

    def tearDown(self):
        os.remove(self.raster.uri)
        os.remove(self.aligned_raster.uri)
        os.remove(self.misaligned_raster.uri)


if __name__ == '__main__':
    unittest.main()
