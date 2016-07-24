# -*- coding: utf-8 -*-
"""RasterFactory Class"""

import copy
import random
import pprint as pp

import numpy as np
import gdal
import osr

from fauxgeo.affine import Affine

dtype_mapping = {
    None: 0,
    np.uint8: 1,
    np.uint16: 2,
    np.int16: 3,
    np.uint32: 4,
    np.int32: 5,
    np.float32: 6,
    np.float64: 7,
    np.complex64: 10,
    np.complex128: 11
}


class RasterFactory(object):

    """A class to generate rasters."""

    def __init__(self, epsg, datatype, nodata, shape, driver='GTIFF', affine=Affine.identity()):
        """Construct RasterFactory object."""
        self.epsg = epsg
        self.datatype = datatype
        self.nodata = nodata
        self.shape = shape
        self.driver = driver
        self.affine = affine

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return pp.pformat(self.get_metadata()).__str__()

    def get_metadata(self):
        """Return metadata dictionary."""
        meta = {}
        meta['epsg'] = self.epsg
        meta['datatype'] = self.datatype
        meta['nodata'] = self.nodata
        meta['shape'] = self.shape
        meta['driver'] = self.driver
        meta['affine'] = self.affine
        return meta

    def uniform(self, val):
        def func():
            return np.ones(self.shape).astype(self.datatype) * val
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def ramp(self, zero_index, slope=1):
        def func():
            high = self.shape[1] - zero_index
            low = -zero_index
            a = np.arange(low, high) * slope
            a[:zero_index] = 0
            return np.tile(a, (self.shape[0], 1)).astype(self.datatype)
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def saw(self, low, high, period):
        def func():
            a = np.linspace(low, high, period)
            repeat_cols = int(np.ceil(self.shape[1] / period))
            subarray = np.linspace(low, high, period)
            return np.tile(subarray, (self.shape[0], repeat_cols)).astype(
                self.datatype) [:, :self.shape[1]]
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def triangle(self, low, high, period):
        def func():
            repeat_cols = int(np.ceil(self.shape[1] / period))
            if period % 2 == 0:
                subarray_left = np.linspace(low, high, np.ceil(period/2.)+1)
                subarray_right = np.array(list(reversed(subarray_left)))
                subarray = np.append(subarray_left[:-1], subarray_right[:-1])
            else:
                subarray_left = np.linspace(low, high, np.ceil(period/2.))
                subarray_right = np.array(list(reversed(subarray_left)))
                subarray = np.append(subarray_left[:-1], subarray_right)
            return np.tile(subarray, (self.shape[0], repeat_cols)).astype(self.datatype)[:, :self.shape[1]]
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def step(self, low, high, period):
        def func():
            repeat_cols = int(np.ceil(self.shape[1] / period))
            low_subarray = np.ones(int(np.ceil(period/2.))) * low
            if period % 2 == 0:
                high_subarray = np.ones(int(np.ceil(period/2.))) * high
                subarray = np.append(low_subarray, high_subarray)
            else:
                high_subarray = np.ones(int(np.floor(period/2.))) * high
                subarray = np.append(low_subarray, high_subarray)
            return np.tile(subarray, (self.shape[0], repeat_cols)).astype(self.datatype)[:, :self.shape[1]]
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def random(self, *args):
        def func():
            if len(args) == 1 and type(args[0]) ==  list:
                return np.random.choice(args[0], self.shape)
            else:
                a = np.random.rand(*self.shape) * (args[1] - args[0]) + args[0]
                return a.astype(self.datatype)
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def alternate(self, val1, val2):
        def func():
            a = np.ones(self.shape) * val2
            a[::2, ::2] = val1
            a[1::2, 1::2] = val1
            return a
        new = copy.deepcopy(self)
        new.create_array = func
        return new

    def to_file(self, filepath):
        num_bands = 1
        datatype = dtype_mapping[self.datatype]
        driver = gdal.GetDriverByName(self.driver)
        dataset = driver.Create(
            filepath, self.shape[1], self.shape[0], num_bands, datatype)
        dataset.SetGeoTransform((self.affine.to_gdal()))

        band = dataset.GetRasterBand(1)
        band.SetNoDataValue(self.nodata)
        band.WriteArray(self.create_array())
        dataset_srs = osr.SpatialReference()
        dataset_srs.ImportFromEPSG(self.epsg)
        dataset.SetProjection(dataset_srs.ExportToWkt())

        band.FlushCache()
        band = dataset_srs = dataset = driver = None
        return True
