#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vector
----------------------------------

Tests for Vector class.

python -m unittest test_vector
"""

import unittest
import os
import tempfile

import shapely

from fauxgeo import Vector

class TestVectorString(unittest.TestCase):

    def setUp(self):
        pass

    def test__str__(self):
        s = shapely.geometry.polygon.Polygon([(0,0), (0,1), (1,1), (1,0)])
        v = Vector.from_shapely(s, 4326)
        print v


if __name__ == '__main__':
    unittest.main()
