'''
Raster Class
'''

import os
import tempfile
import shutil

import gdal
import osr
import numpy as np
from affine import Affine
import pygeoprocessing as pygeo


class Raster(object):
    # any global variables here
    def __init__(self, uri, driver):
        self.uri = uri
        self.driver = driver
        self.dataset = None

    @classmethod
    def from_array(self, array, affine, proj, datatype, nodata_val, driver='GTiff'):
        if len(array.shape) is 2:
            num_bands = 1
        elif len(array.shape) is 3:
            num_bands = len(array)
        else:
            raise ValueError

        dataset_uri = pygeo.geoprocessing.temporary_filename()
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

        return Raster(dataset_uri, driver=driver)

    @classmethod
    def from_file(self, uri, driver='GTiff'):
        dataset_uri = pygeo.geoprocessing.temporary_filename()
        if not os.path.isabs(uri):
            uri = os.path.join(os.getcwd(), uri)
        # assert existence
        shutil.copyfile(uri, dataset_uri)
        return Raster(dataset_uri, driver)

    @classmethod
    def from_tempfile(self, uri, driver='GTiff'):
        if not os.path.isabs(uri):
            uri = os.path.join(os.getcwd(), uri)
        return Raster(uri, driver)

    @classmethod
    def simple_affine(self, top_left_x, top_left_y, pix_width, pix_height):
        return Affine(pix_width, 0, top_left_x, 0, -(pix_height), top_left_y)

    def __del__(self):
        self._delete()

    def __exit__(self):
        self._delete()

    def _delete(self):
        os.remove(self.uri)

    def __str__(self):
        return self.uri

    def __len__(self):
        return self.band_count()

    def __mul__(self, raster):
        def mul_closer(nodata):
            def mul(x, y):
                if nodata in [x, y]:
                    return nodata
                return x * y
            return mul
        return self.local_op(raster, mul_closer)

    def __div__(self, raster):
        def div_closer(nodata):
            def div(x, y):
                if nodata in [x, y]:
                    return nodata
                return x / y
            return div
        return self.local_op(raster, div_closer)

    def __add__(self, raster):
        def add_closer(nodata):
            def add(x, y):
                if nodata in [x, y]:
                    return nodata
                return x + y
            return add
        return self.local_op(raster, add_closer)

    def __sub__(self, raster):
        def sub_closer(nodata):
            def sub(x, y):
                if nodata in [x, y]:
                    return nodata
                return x - y
            return sub
        return self.local_op(raster, sub_closer)

    def __pow__(self, raster):
        def pow_closer(nodata):
            def pow(x, y):
                if nodata in [x, y]:
                    return nodata
                return x**y
            return pow
        return self.local_op(raster, pow_closer)

    def __eq__(self, raster):
        if self.is_aligned(raster) and (self.get_shape() == raster.get_shape()):
            return (self.get_bands() == raster.get_bands())
        else:
            return False

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

    def __repr__(self):
        return self.get_bands().__repr__()

    def _repr_png_(self):
        raise NotImplementedError

    def save_raster(self, uri):
        shutil.copyfile(self.uri, uri)

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

    def get_projection(self):
        self._open_dataset()
        RasterSRS = osr.SpatialReference()
        RasterSRS.ImportFromWkt(self.dataset.GetProjectionRef())
        return int(RasterSRS.GetAttrValue("AUTHORITY", 1))

    def get_geotransform(self):
        geotransform = None
        self._open_dataset()

        geotransform = self.dataset.GetGeoTransform()

        self._close_dataset()
        return geotransform

    def get_affine(self):
        geotransform = self.get_geotransform()
        return Affine.from_gdal(*geotransform)

    def get_bbox(self):
        pass

    def set_band(self, masked_array):
        '''Currently works for rasters with only one band'''
        assert(len(masked_array) == self.get_rows())
        assert(len(masked_array[0]) == self.get_cols())
        assert(self.band_count() == 1)

        raise NotImplementedError

    def set_bands(self, array):
        # if self.exists:
        #     self._open_dataset()
        #     band_count = self.dataset.RasterCount
        #     self._close_dataset()

        #     if band_count == 1 and len(array.shape) == 2:
        #         assert(len(array) == self.get_rows)
        #         assert(len(array[0]) == self.get_cols)
        #         self.set_band(1, array)

        #     elif len(array.shape) == 3 and array.shape[0] == band_count:
        #         for band_num in range(band_count):
        #             self.set_band(band_num + 1, array[band_num])
        # else:
        #     raise Exception
        raise NotImplementedError

    def copy(self, uri):
        if not os.path.isabs(uri):
            uri = os.path.join(os.getcwd(), uri)
        shutil.copyfile(self.uri, uri)
        return Raster.from_tempfile(uri)

    def is_aligned(self, raster):
        try:
            this_affine = self.get_affine()
            other_affine = raster.get_affine()
            return (this_affine == other_affine)
        except:
            raise TypeError

    def align(self, raster, resample_method):
        '''Currently aligns other raster to this raster - later: union/intersection
        '''
        assert(self.get_projection() == raster.get_projection())

        def dataset_pixel_op(x, y): return y
        dataset_uri_list = [self.uri, raster.uri]
        dataset_out_uri = pygeo.geoprocessing.temporary_filename()
        datatype_out = pygeo.geoprocessing.get_datatype_from_uri(raster.uri)
        nodata_out = pygeo.geoprocessing.get_nodata_from_uri(raster.uri)
        pixel_size_out = pygeo.geoprocessing.get_cell_size_from_uri(self.uri)
        bounding_box_mode = "dataset"

        pygeo.geoprocessing.vectorize_datasets(
            dataset_uri_list,
            dataset_pixel_op,
            dataset_out_uri,
            datatype_out,
            nodata_out,
            pixel_size_out,
            bounding_box_mode,
            resample_method_list=[resample_method]*2,
            dataset_to_align_index=0,
            dataset_to_bound_index=0,
            assert_datasets_projected=False,
            vectorize_op=False)

        return Raster.from_tempfile(dataset_out_uri)
        # temp_raster = Raster.from_tempfile(dataset_out_uri)
        # temp_raster.copy(raster.uri)
        # os.remove(dataset_out_uri)

    def align_to(self, raster, resample_method):
        '''Currently aligns other raster to this raster - later: union/intersection
        '''
        assert(self.get_projection() == raster.get_projection())

        def dataset_pixel_op(x, y): return y
        dataset_uri_list = [raster.uri, self.uri]
        dataset_out_uri = pygeo.geoprocessing.temporary_filename()
        datatype_out = pygeo.geoprocessing.get_datatype_from_uri(raster.uri)
        nodata_out = pygeo.geoprocessing.get_nodata_from_uri(raster.uri)
        pixel_size_out = pygeo.geoprocessing.get_cell_size_from_uri(self.uri)
        bounding_box_mode = "dataset"

        pygeo.geoprocessing.vectorize_datasets(
            dataset_uri_list,
            dataset_pixel_op,
            dataset_out_uri,
            datatype_out,
            nodata_out,
            pixel_size_out,
            bounding_box_mode,
            resample_method_list=[resample_method]*2,
            dataset_to_align_index=0,
            dataset_to_bound_index=0,
            assert_datasets_projected=False,
            vectorize_op=False)

        return Raster.from_tempfile(dataset_out_uri)

    def clip(self, aoi_uri):
        dataset_out_uri = pygeo.geoprocessing.temporary_filename()
        pygeo.geoprocessing.clip_dataset_uri(
            self.uri, aoi_uri, dataset_out_uri)
        return Raster.from_tempfile(dataset_out_uri)

    def reproject(self, proj, resample_method, pixel_size=None):
        if pixel_size is None:
            pixel_size = self.get_affine().a

        dataset_out_uri = pygeo.geoprocessing.temporary_filename()
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(proj)
        wkt = srs.ExportToWkt()

        pygeo.geoprocessing.reproject_dataset_uri(
            self.uri, pixel_size, wkt, resample_method, dataset_out_uri)

        return Raster.from_tempfile(dataset_out_uri)

    def reclass(self, reclass_table, out_nodata=None):
        if out_nodata is None:
            out_nodata = pygeo.geoprocessing.get_nodata_from_uri(self.uri)

        out_datatype = pygeo.geoprocessing.get_datatype_from_uri(self.uri)
        dataset_out_uri = pygeo.geoprocessing.temporary_filename()

        pygeo.geoprocessing.reclassify_dataset_uri(
            self.uri,
            reclass_table,
            dataset_out_uri,
            out_datatype,
            out_nodata)

        return Raster.from_tempfile(dataset_out_uri)

    def overlay(self, raster):
        raise NotImplementedError

    def to_vector(self):
        raise NotImplementedError

    def local_op(self, raster, pixel_op_closer):
        assert(self.is_aligned(raster))
        assert(self.get_nodata(1) == raster.get_nodata(1))

        nodata = self.get_nodata(1)
        pixel_op = pixel_op_closer(nodata)
        dataset_uri_list = [self.uri, raster.uri]
        dataset_out_uri = pygeo.geoprocessing.temporary_filename()
        datatype_out = pygeo.geoprocessing.get_datatype_from_uri(self.uri)
        nodata_out = pygeo.geoprocessing.get_nodata_from_uri(self.uri)
        pixel_size_out = pygeo.geoprocessing.get_cell_size_from_uri(self.uri)
        bounding_box_mode = "dataset"
        resample_method = "nearest"

        pygeo.geoprocessing.vectorize_datasets(
            dataset_uri_list,
            pixel_op,
            dataset_out_uri,
            datatype_out,
            nodata_out,
            pixel_size_out,
            bounding_box_mode,
            resample_method_list=[resample_method]*2,
            dataset_to_align_index=0,
            dataset_to_bound_index=0,
            assert_datasets_projected=False,
            vectorize_op=True)

        return Raster.from_tempfile(dataset_out_uri)

    def _open_dataset(self):
        self.dataset = gdal.Open(self.uri)

    def _close_dataset(self):
        self.dataset = None
