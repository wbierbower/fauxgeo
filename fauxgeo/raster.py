"""Raster Class."""

import os
import shutil
import logging

import gdal
import osr
import numpy as np
import shapely

from fauxgeo.affine import Affine


class Raster(object):

    """A class for interacting with gdal raster files."""

    def __init__(self, uri, driver, resample_method=None):
        self.uri = uri
        self.driver = driver
        self.dataset = None
        self.resample_method = resample_method

    @staticmethod
    def from_array(array, affine, proj, datatype, nodata_val, resample_method=None, driver='GTiff', filepath=None):
        if len(array.shape) is 2:
            num_bands = 1
        elif len(array.shape) is 3:
            num_bands = len(array)
        else:
            raise ValueError

        if filepath:
            dataset_uri = filepath
        else:
            dataset_uri = geoprocess.temporary_filename()
        rows = array.shape[0]
        cols = array.shape[1]

        driver = gdal.GetDriverByName(driver)
        dataset = driver.Create(dataset_uri, cols, rows, num_bands, datatype)
        dataset.SetGeoTransform((affine.to_gdal()))

        for band_num in range(num_bands):
            band = dataset.GetRasterBand(band_num + 1)  # Get only raster band
            band.SetNoDataValue(nodata_val)
            if num_bands > 1:
                band.WriteArray(array[band_num])
            else:
                band.WriteArray(array)
            dataset_srs = osr.SpatialReference()
            dataset_srs.ImportFromEPSG(proj)
            dataset.SetProjection(dataset_srs.ExportToWkt())
            band.FlushCache()

        band = None
        dataset_srs = None
        dataset = None
        driver = None

        if not filepath:
            return Raster(
                dataset_uri, resample_method=resample_method, driver=driver)

    @staticmethod
    def from_file(uri, resample_method=None, driver='GTiff'):
        dataset_uri = geoprocess.temporary_filename()
        if not os.path.isabs(uri):
            uri = os.path.join(os.getcwd(), uri)
        # assert existence
        shutil.copyfile(uri, dataset_uri)
        return Raster(dataset_uri, driver, resample_method=resample_method)

    @staticmethod
    def from_tempfile(uri, driver='GTiff'):
        if not os.path.isabs(uri):
            uri = os.path.join(os.getcwd(), uri)
        return Raster(uri, driver)

    @staticmethod
    def create_simple_affine(top_left_x, top_left_y, pix_width, pix_height):
        return Affine(pix_width, 0, top_left_x, 0, -(pix_height), top_left_y)

    def _open_dataset(self):
        self.dataset = gdal.Open(self.uri)

    def _close_dataset(self):
        self.dataset = None

    def __del__(self):
        self._delete()

    def __exit__(self):
        self._delete()

    def _delete(self):
        os.remove(self.uri)

    def __str__(self):
        string = '\nRASTER___'
        string += '\nNumber of Bands: ' + str(self.band_count())
        string += '\nBand 1:\n' + self.get_band(1).__repr__()
        string += self.get_affine().__repr__()
        string += '\nNoData for Band 1: ' + str(self.get_nodata(1))
        string += '\nDatatype for Band 1: ' + str(self.get_band(1).dtype)
        string += '\nProjection (EPSG): ' + str(self.get_projection())
        string += '\nuri: ' + self.uri
        string += '\n'
        return string

    def __len__(self):
        return self.band_count()

    def __neg__(self):
        pass

    def __mul__(self, raster):
        pass

    def __rmul__(self, raster):
        pass

    def __div__(self, raster):
        pass

    def __rdiv__(self, raster):
        pass

    def __add__(self, raster):
        pass

    def __radd__(self, raster):
        pass

    def __sub__(self, raster):
        pass

    def __rsub__(self, raster):
        pass

    def __pow__(self, raster):
        pass

    def __rpow__(self, raster):
        pass

    def __mod__(self, raster):
        pass

    def __eq__(self, raster):
        pass

    def minimum(self, raster):
        pass

    def fminimum(self, raster):
        pass

    def __getitem__(self, key):
        arr = self.get_band(1)
        return arr[key]

    def __setitem__(self, key, item):
        arr = self.get_band(1)
        arr[key] = item
        self.set_band(1, arr)

    def getslice(self, a, b, c):
        pass

    def setslice(self, a, b, c):
        pass

    def __iter__(self):
        pass  # iterate over bands?

    def __contains__(self):
        pass  # test numpy raster against all bands?

    def __repr__(self):
        return self.get_bands().__repr__()

    def _repr_png_(self):
        raise NotImplementedError

    def save_raster(self, uri):
        shutil.copyfile(self.uri, uri)

    def get_heatmap_image(self):
        raise NotImplementedError

    def sum(self):
        pass

    def min(self):
        pass

    def max(self):
        pass

    def mean(self):
        pass

    def std(self):
        pass

    def unique(self):
        pass

    def ones(self):
        pass

    def zeros(self):
        pass

    def band_count(self):
        self._open_dataset()
        count = self.dataset.RasterCount
        self._close_dataset()
        return count

    def get_band(self, band_num):
        a = None
        self._open_dataset()

        if band_num >= 1 and band_num <= self.dataset.RasterCount:
            band = self.dataset.GetRasterBand(band_num)
            a = band.ReadAsArray()
            nodata_val = band.GetNoDataValue()
            a = np.ma.masked_equal(a, nodata_val)
            band = None
        else:
            pass

        self._close_dataset()
        return a

    def get_bands(self):
        self._open_dataset()

        if self.dataset.RasterCount == 0:
            return None

        a = np.zeros((
            self.dataset.RasterCount,
            self.dataset.RasterYSize,
            self.dataset.RasterXSize))

        for num in np.arange(self.dataset.RasterCount):
            band = self.dataset.GetRasterBand(num+1)
            b = band.ReadAsArray()
            nodata_val = band.GetNoDataValue()
            b = np.ma.masked_equal(b, nodata_val)
            a[num] = b

        self._close_dataset()
        return a

    def get_resample_method(self):
        if not self.resample_method:
            raise AttributeError(
                'Raster object has no assigned resample_method attribute')
        else:
            return self.resample_method

    def get_nodata(self, band_num):
        nodata_val = None
        self._open_dataset()

        if band_num >= 1 and band_num <= self.dataset.RasterCount:
            band = self.dataset.GetRasterBand(band_num)
            nodata_val = band.GetNoDataValue()

        self._close_dataset()
        return nodata_val

    def get_datatype(self, band_num):
        datatype = None
        self._open_dataset()

        if band_num >= 1 and band_num <= self.dataset.RasterCount:
            band = self.dataset.GetRasterBand(band_num)
            datatype = band.DataType

        self._close_dataset()
        return datatype

    def get_rows(self):
        rows = None
        self._open_dataset()

        rows = self.dataset.RasterYSize

        self._close_dataset()
        return rows

    def get_cols(self):
        cols = None
        self._open_dataset()

        cols = self.dataset.RasterXSize

        self._close_dataset()
        return cols

    def get_shape(self):
        rows = self.get_rows()
        cols = self.get_cols()
        return (rows, cols)

    def get_projection(self):
        self._open_dataset()
        RasterSRS = osr.SpatialReference()
        RasterSRS.ImportFromWkt(self.dataset.GetProjectionRef())
        proj = int(RasterSRS.GetAttrValue("AUTHORITY", 1))
        RasterSRS = None
        self._close_dataset()

        return proj

    def get_projection_wkt(self):
        self._open_dataset()
        wkt = self.dataset.GetProjectionRef()
        self._close_dataset()
        return wkt

    def get_geotransform(self):
        geotransform = None
        self._open_dataset()
        geotransform = self.dataset.GetGeoTransform()
        self._close_dataset()
        return geotransform

    def get_affine(self):
        geotransform = self.get_geotransform()
        return Affine.from_gdal(*geotransform)

    def get_bounding_box(self):
        pass

    def get_aoi(self):
        """May only be suited for non-rotated rasters."""
        bb = self.get_bounding_box()
        u_x = max(bb[0::2])
        l_x = min(bb[0::2])
        u_y = max(bb[1::2])
        l_y = min(bb[1::2])
        return shapely.Polygon([(l_x, l_y), (l_x, u_y), (u_x, u_y), (u_x, l_y)])

    def get_aoi_as_shapefile(self, uri):
        pass

    def get_cell_area(self):
        pass

    def set_band(self, band_num, masked_array):
        pass

    def set_bands(self, array):
        pass

    def set_datatype(self, datatype):
        pass

    def set_nodata(self, nodata_val):
        pass

    def set_datatype_and_nodata(self, datatype, nodata_val):
        pass

    def copy(self, uri=None):
        pass

    def is_aligned(self, raster):
        pass

    def align(self, raster, resample_method):
        pass

    def align_to(self, raster, resample_method):
        pass

    def clip(self, aoi_uri):
        pass

    def reproject(self, proj, resample_method, pixel_size=None):
        pass

    def resize_pixels(self, pixel_size, resample_method):
        pass

    def reclass_masked_values(self, mask_raster, new_value):
        pass

    def sample_from_raster(self, raster):
        pass

    def reclass(self, reclass_table, out_nodata=None, out_datatype=None):
        pass

    def overlay(self, raster):
        pass

    def to_vector(self):
        pass

    def to_binary_raster(self, val):
        pass

    def local_op(self, raster, pixel_op_closure, broadcast=False):
        pass
