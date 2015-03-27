'''
Raster Class
'''

import os
import gdal
import osr
import numpy as np
from affine import Affine
from StringIO import StringIO
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import image


class Raster(object):
    # any global variables here
    def __init__(self, uri, driver):
        self.uri = uri
        self.driver = driver
        self.dataset = None

    @classmethod
    def from_array(self, output_uri, array, affine, proj, datatype, nodata_val, driver='GTiff'):
        if len(array.shape) is 2:
            num_bands = 1
        elif len(array.shape) is 3:
            num_bands = len(array)
        else:
            raise ValueError

        rows = array.shape[0]
        cols = array.shape[1]

        driver = gdal.GetDriverByName(driver)
        dataset = driver.Create(output_uri, cols, rows, num_bands, datatype)
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

        return Raster(output_uri, driver=driver)

    @classmethod
    def from_file(self, uri, driver='GTiff'):
        if not os.path.isabs(uri):
            uri = os.path.join(os.getcwd(), uri)
        # assert existence
        return Raster(uri, driver)

    @classmethod
    def simple_affine(self, top_left_x, top_left_y, pix_width, pix_height):
        return Affine(pix_width, 0, top_left_x, 0, -(pix_height), top_left_y)

    def __str__(self):
        return self.uri

    def __len__(self):
        return self.band_count()

    def __eq__(self):
        pass  # false if different shape, element-by-element if same shape

    def __getitem__(self):
        pass  # return numpy slice?  Raster object with sliced numpy array?

    def __setitem__(self):
        pass  # set numpy values to raster

    def __getslice__(self):
        pass

    def __setslice__(self):
        pass

    def __iter__(self):
        pass  # iterate over bands?

    def __contains__(self):
        pass  # test numpy raster against all bands?

    def _figure_data(self, format):
        f = StringIO()
        array = self.get_band(1)
        # fig = plt.figure()
        # ax = plt.subplot(1, 1, 1)
        # plt.savefig(f, bbox_inches='tight', format=format)
        # plt.imsave(f, array, cmap=cm.Greys_r)
        # plt.imshow(array, interpolation="nearest")
        fig = plt.figure()
        ax = fig.add_subplot(111)
        # cax = ax.matshow(array, interpolation='nearest')
        # fig.colorbar(cax)
        plt.savefig(f, bbox_inches='tight', format=format)
        # f.seek(0)
        # return f.read()
        return None

    def _repr_png_(self):
        return self._figure_data('png')

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

    def get_geotransform(self):
        geotransform = None
        self._open_dataset()

        geotransform = self.dataset.GetGeoTransform()

        self._close_dataset()
        return geotransform

    def get_affine(self):
        geotransform = self.get_geotransform()
        return Affine.from_gdal(*geotransform)

    def set_band(self, band_num, array):
        if self.exists:
            assert(len(array) == self.get_rows)
            assert(len(array[0]) == self.get_cols)

            self._open_dataset()

            if band_num >= 1 and band_num <= self.dataset.RasterCount:
                band = self.dataset.GetRasterBand(band_num)
                band.WriteArray(array)
                band.FlushCache()
                band = None

            self._close_dataset()
        else:
            raise Exception

    def set_bands(self, array):
        if self.exists:
            self._open_dataset()
            band_count = self.dataset.RasterCount
            self._close_dataset()

            if band_count == 1 and len(array.shape) == 2:
                assert(len(array) == self.get_rows)
                assert(len(array[0]) == self.get_cols)
                self.set_band(1, array)

            elif len(array.shape) == 3 and array.shape[0] == band_count:
                for band_num in range(band_count):
                    self.set_band(band_num + 1, array[band_num])
        else:
            raise Exception

    def clip(self, aoi):
        raise NotImplementedError

    def reproject(self, proj, resample_method, pixel_size):
        raise NotImplementedError

    def reclass(self, reclass_table):
        raise NotImplementedError

    def overlay(self, raster):
        raise NotImplementedError

    def is_aligned(self, raster):
        raise NotImplementedError

    def align(self, raster, resample_method):
        raise NotImplementedError

    def copy(self, uri):
        raise NotImplementedError

    def to_vector(self):
        raise NotImplementedError

    def _open_dataset(self):
        self.dataset = gdal.Open(self.uri)

    def _close_dataset(self):
        self.dataset = None
