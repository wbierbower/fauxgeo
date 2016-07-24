#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RasterFactory Class Tests.
"""

import unittest
import os
import tempfile

import numpy as np
from numpy import testing
import gdal

from fauxgeo import Affine
from fauxgeo import RasterFactory


def read_array(filepath):
    ds = gdal.Open(filepath)
    band = ds.GetRasterBand(1)
    a = band.ReadAsArray()
    ds = band = None
    return a


class TestRasterFactory(unittest.TestCase):

    def test_uniform(self):
        rf = RasterFactory(4326, np.float32, -9999, (4, 10))
        new = rf.uniform(4)
        test_array = np.ones((4, 10)) * 4
        testing.assert_array_equal(new.create_array(), test_array)

        f = tempfile.NamedTemporaryFile()
        new.to_file(f.name)
        testing.assert_array_equal(read_array(f.name), test_array)


if __name__ == '__main__':
    unittest.main()
