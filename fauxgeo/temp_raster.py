'''
TempRaster Class
'''

import tempfile
import os
import gdal
import osr

from fauxgeo.raster import Raster


class TempRaster(Raster):

    def __init__(self, uri, driver='GTiff'):
        # make temporary raster file
        super(TempRaster, self).__init__(uri, driver)

    @classmethod
    def from_array(array, affine, proj, datatype, nodata_val, driver='GTiff'):
        if len(array.shape) is 2:
            num_bands = 1
        elif len(array.shape) is 3:
            num_bands = len(array)
        else:
            raise ValueError

        tmpfile = tempfile.NamedTemporaryFile(mode='r')
        uri = tmpfile.name
        tmpfile.close()

        rows = array.shape[0]
        cols = array.shape[1]

        driver = gdal.GetDriverByName(driver)
        dataset = driver.Create(uri, cols, rows, num_bands, datatype)
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

        return Raster(uri, driver=driver)

    @classmethod
    def from_file():
        raise NotImplementedError

    def __del__(self):
        self._delete()

    def __exit__(self):
        self._delete()

    def _delete(self):
        os.remove(self.uri)
