Creating Rasters for Unittests
==============================

.. code::

  import unittest
  from fauxgeo import RasterFactory, Raster
  import pygeoprocessing as pygeo

  class TestIO(unittest.TestCase):

    def setUp(self):
      # arguments for raster factory
      pixel_size = 0.083333
      size = 180/pixel_size
      shape = (size, size*2)
      affine = Affine(pixel_size, 0, -180, 0, -pixel_size, 90)
      proj = 4326
      datatype = gdal.GDT_Int32
      nodata_val = NODATA_INT

      # create raster factory
      self.global_int_factory = RasterFactory(
        proj, datatype, nodata_val, shape[0], shape[1], affine=affine)

    def test(self):
      # create test data
      global_raster = self.global_int_factory.uniform(5)

      # arguments for vectorize_datasets
      dataset_uri_list = [global_raster.uri]
      dataset_out_uri = pygeo.geoprocessing.temporary_filename()
      # ... other inputs ...
      pygeo.geoprocessing.vectorize_datasets(...)

      # validate that output matches expected value
      r = Raster.from_file(dataset_out_uri)
      assert(r[0, 0] == 5)
