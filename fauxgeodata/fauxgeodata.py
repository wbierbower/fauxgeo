# -*- coding: utf-8 -*-
try:
    from osgeo import gdal
    from osgeo import ogr
    from osgeo import osr
except:
    import gdal
    import ogr
    import osr

import numpy as np


def fauxgeodata():
    '''
    About

    Args:
        None

    Returns
        hello_world (string): "hello world"!
    '''
    return "hello world"


def generate_array():
    pass


def generate_geometries():
    pass


def create_raster(filepath, orgX, orgY, pixWidth, pixHeight, array, proj=4326):
    '''
    Creates an arbitrary raster

    Args:
        filepath (string): where to save file
        proj (int): EPSG code
        orgX (float): bottom left x dimension?
        array (np.array): raster values

    Returns:
        None
    '''
    num_bands = 1
    rotX = 0
    rotY = 0

    rows = array.shape[0]
    cols = array.shape[1]

    driver = gdal.GetDriverByName('GTiff')
    raster = driver.Create(filepath, cols, rows, num_bands, gdal.GDT_Byte)
    raster.SetGeoTransform((orgX, pixWidth, rotX, orgY, rotY, pixHeight))

    band = raster.GetRasterBand(1)  # Get only raster band
    band.WriteArray(array)
    raster_srs = osr.SpatialReference()
    raster_srs.ImportFromEPSG(proj)
    raster.SetProjection(raster_srs.ExportToWkt())
    band.FlushCache()


def create_vector(geometries):
    '''
    Creates an arbitrary vector

    Args:
        geometries (list): list of shapely geometries

    Returns:
        None
    '''
    pass
