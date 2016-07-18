"""Raster Class."""

import os
import shutil
import logging

import numpy as np
import shapely

from fauxgeo.affine import Affine


class Raster(object):

    """A class for interacting with raster files."""

    def __init__(self, uri, driver, resample_method=None):
        self.uri = uri
        self.driver = driver
        self.dataset = None
        self.resample_method = resample_method
