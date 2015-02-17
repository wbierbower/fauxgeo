#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fauxgeodata
----------------------------------

Tests for `fauxgeodata` module.
"""

import unittest
import os

import tempfile
import numpy as np
import rasterio as rio

from fauxgeodata import fauxgeodata


class TestFauxgeodata(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_raster_1(self):
        subdir = tempfile.mkdtemp("subdir")
        filepath = os.path.join(subdir, 'test.tif')
        orgX = 20
        orgY = 20
        pixWidth = 1
        pixHeight = 1
        rasterWidth = 10
        rasterHeight = 20

        array = np.random.randint(10, size=[rasterHeight, rasterWidth])
        fauxgeodata.create_raster(
            filepath,
            orgX,
            orgY,
            pixWidth,
            pixHeight,
            array)

        with rio.open(filepath, 'r') as rast:
            self.assertEqual(rast.width, rasterWidth)
            self.assertEqual(rast.height, rasterHeight)
            self.assertEqual((rasterHeight, rasterWidth), rast.shape)
            # rast.crs
            # rast.affine

    def test_create_raster_2(self):
        subdir = tempfile.mkdtemp("subdir")
        filepath = os.path.join(subdir, 'test.tif')
        orgX = 20
        orgY = 20
        pixWidth = 10000
        pixHeight = 10000
        rasterWidth = 100
        rasterHeight = 800
        proj = 26918

        array = np.random.randint(10, size=[rasterHeight, rasterWidth])
        fauxgeodata.create_raster(
            filepath,
            orgX,
            orgY,
            pixWidth,
            pixHeight,
            array,
            proj=proj)

        with rio.open(filepath, 'r') as rast:
            self.assertEqual(rast.width, rasterWidth)
            self.assertEqual(rast.height, rasterHeight)
            self.assertEqual((rasterHeight, rasterWidth), rast.shape)
            # rast.crs
            # rast.affine

    def test_create_raster_bad_array(self):
        subdir = tempfile.mkdtemp("subdir")
        filepath = os.path.join(subdir, 'test.tif')
        orgX = 20
        orgY = 20
        pixWidth = 10000
        pixHeight = 10000
        rasterWidth = 100
        rasterHeight = 800
        proj = 26918
        ExtraDimension = 2

        array = np.random.randint(
            10, size=[rasterHeight, rasterWidth, ExtraDimension])

        with self.assertRaises(AssertionError):
            fauxgeodata.create_raster(
                filepath,
                orgX,
                orgY,
                pixWidth,
                pixHeight,
                array,
                proj=proj)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
