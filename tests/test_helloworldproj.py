#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_fauxgeodata
----------------------------------

Tests for `fauxgeodata` module.
"""

import unittest

from fauxgeodata import fauxgeodata


class TestHelloworldproj(unittest.TestCase):

    def setUp(self):
        pass

    def test_fauxgeodata(self):
        guess = fauxgeodata.fauxgeodata()
        self.assertEqual(guess, "hello world")

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
