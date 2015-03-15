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


def create_raster(filepath, orgX, orgY, pixWidth, pixHeight, array, proj=4326, gdal_type=gdal.GDT_Float32, nodata=-9999):
    '''
    Creates an arbitrary raster

    Args:
        filepath (string): where to save file
        orgX (float): x dimension origin coordinate (bottom left untransformed)
        orgY (float): y dimension origin coordinate (bottom left untransformed)
        pixWidth (float): size of each pixel's width (units depend on
            projection)
        pixHeight (float): size of each pixel's height (units depend on
            projection)
        array (np.array): raster values

    Keyword Args:
        proj (int): EPSG code
        gdal_type (GDAL Datatype): a GDAL datatype
        nodata (same as gdal_type): the NODATA value 

    Returns:
        None
    '''
    assert(len(array.shape) == 2)

    num_bands = 1
    rotX = 0
    rotY = 0

    rows = array.shape[0]
    cols = array.shape[1]

    driver = gdal.GetDriverByName('GTiff')
    raster = driver.Create(filepath, cols, rows, num_bands, gdal_type)
    raster.SetGeoTransform((orgX, pixWidth, rotX, orgY, rotY, pixHeight))

    band = raster.GetRasterBand(1)  # Get only raster band
    band.SetNoDataValue(nodata)
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
