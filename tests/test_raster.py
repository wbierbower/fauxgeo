#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Raster Class Tests.
"""

import unittest
import os
import tempfile

import numpy as np
from numpy import testing
import shapely

from fauxgeo import Affine
from fauxgeo import Raster
from fauxgeo import RasterFactory


class TestRaster(unittest.TestCase):
    def setUp(self):
        pass

    def test_add(self):
        assert(True)


if __name__ == '__main__':
    unittest.main()
