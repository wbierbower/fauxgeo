'''
Raster, TestRaster, and RasterFactory Classes
'''

import tempfile
import os
import gdal
import osr
import numpy as np
from affine import Affine


class Raster(object):
    # any global variables here

    def __init__(self, uri):
        self.exists = False
        self.uri = uri
        self.dataset = None

        if uri is not None:
            if os.path.exists(uri):
                self.exists = True
            else:
                self.exists = False
                # os.makedirs(uri)
                f = open(uri, 'w')
                f.close()
        else:
            # make temporary raster file
            self.exists = False
            self.tmp = True
            tmpfile = tempfile.NamedTemporaryFile(mode='r')
            self.uri = tmpfile.name
            tmpfile.close()

    def __str__(self):
        return "raster at %s" % (self.uri)

    def __del__(self):
        self._close()

    def __exit__(self):
        self._close()

    # Should probably be in TestRaster class
    def _close(self):
        if self.tmp is False:
            os.remove(self.uri)

    def init(self, array, affine, proj, datatype, nodata_val):
        # if self.exists == True:
        #     raise Exception

        if len(array.shape) == 2:
            num_bands = 1
        elif len(array.shape) == 3:
            num_bands = len(array)
        else:
            raise ValueError

        rows = array.shape[0]
        cols = array.shape[1]

        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(self.uri, cols, rows, num_bands, datatype)
        dataset.SetGeoTransform((
            affine.c, affine.a, affine.b, affine.f, affine.d, affine.e))

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

        self.exists = True
        band = None
        dataset_srs = None
        dataset = None
        driver = None

    def init_2(self, array, bot_left_x, bot_left_y, pix_width, proj, datatype, nodata_val):

        if len(array.shape) == 2:
            num_bands = 1
        elif len(array.shape) == 3:
            num_bands = len(array)
        else:
            raise ValueError

        rows = array.shape[0]
        cols = array.shape[1]
        vertical_offset = rows * pix_width

        driver = gdal.GetDriverByName('GTiff')
        dataset = driver.Create(self.uri, cols, rows, num_bands, datatype)
        dataset.SetGeoTransform((
            bot_left_x, pix_width, 0, (bot_left_y + vertical_offset), 0, -(pix_width)))

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

        self.exists = True
        band = None
        dataset_srs = None
        dataset = None
        driver = None

    def get_band(self, band_num):
        a = None
        self._open_dataset()

        if band_num >= 1 and band_num <= self.dataset.RasterCount:
            band = self.dataset.GetRasterBand(band_num)
            a = band.ReadAsArray()
            band = None
        else:
            pass

        self._close_dataset()
        return a

    def get_bands(self):
        self._open_dataset()

        if self.dataset.RasterCount == 0:
            return None

        a = np.zeros((self.dataset.RasterYSize, self.dataset.RasterXSize, self.dataset.RasterCount))
        for num in arange(self.dataset.RasterCount):
            band = self.dataset.GetRasterBand(num+1)
            a[:, :, num] = band.ReadAsArray()

        self._close_dataset()
        return a

    def get_nodata_val(self, band_num):
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

    def _open_dataset(self):
        self.dataset = gdal.Open(self.uri)

    def _close_dataset(self):
        self.dataset = None


class TestRaster(Raster):

    def __init__(self, array, affine, proj, datatype, nodata_val):
        super(TestRaster, self).__init__(None)
        self.init(array, affine, proj, datatype, nodata_val)

    def __del__(self):
        self._close()

    def __exit__(self):
        self._close()

    def _close(self):
        os.remove(self.uri)


class RasterFactory(object):

    def __init__(self, proj, datatype, nodata_val, rows, cols, affine=Affine.identity):
        self.proj = proj
        self.datatype = datatype
        self.nodata_val = nodata_val
        self.rows = rows
        self.cols = cols
        self.affine = affine

    def get_metadata(self):
        meta = {}
        meta['proj'] = self.proj
        meta['datatype'] = self.datatype
        meta['nodata_val'] = self.nodata_val
        meta['rows'] = self.rows
        meta['cols'] = self.cols
        meta['affine'] = self.affine
        return meta

    def _create_raster(self, array, uri):
        if uri is None:
            return TestRaster(array, self.affine, self.proj, self.datatype, self.nodata_val)
        else:
            r = Raster(uri)
            r.init(array, self.affine, self.proj, self.datatype, self.nodata_val)
            return r

    def filled_value(self, val, uri=None):
        a = np.ones((self.rows, self.cols)) * val
        return self._create_raster(a, uri)

    def filled_alternating_values(self, val1, val2, uri=None):
        a = np.ones((self.rows, self.cols)) * val2
        a[::2, ::2] = val1
        a[1::2, 1::2] = val1
        return self._create_raster(a, uri)

    def filled_random(self, uri=None):
        a = np.random.rand(self.rows, self.cols)
        return self._create_raster(a, uri)

    def filled_ramp_across_cols(self, val1, val2, uri=None):
        a = np.zeros((self.rows, self.cols))
        col_vals = np.linspace(val1, val2, self.cols)
        a[:] = col_vals
        return self._create_raster(a, uri)

    def filled_ramp_across_rows(self, val1, val2, uri=None):
        a = np.zeros((self.cols, self.rows))
        row_vals = np.linspace(val1, val2, self.rows)
        a[:] = row_vals
        a = a.T
        return self._create_raster(a, uri)

    # def bell_shape(self, uri=None):
