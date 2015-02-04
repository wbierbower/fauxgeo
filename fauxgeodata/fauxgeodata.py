# -*- coding: utf-8 -*-
try:
	from osgeo import gdal
	from osgeo import ogr
except:
	import gdal
	import ogr

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

def create_raster(array):
	'''
	Creates an arbitrary raster
	
	Args:
		array (np.array): raster values
	
	Returns:
		None
	'''
	pass
	

def create_vector(geometries):
	'''
	Creates an arbitrary vector
	
	Args:
		geometries (list): list of shapely geometries
		
	Returns:
		None
	'''
	pass
