#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr
from osgeo import gdal

# set pixel size
pixel_size = 1
no_data_value = -9999

# Shapefile input name
# input projection must be in cartesian system in meters
# input wgs 84 or EPSG: 4326 will NOT work!!!
input_shp = r'../geodata/ply_golfcourse-strasslach3857.shp'

# TIF Raster file to be created
output_raster = r'../geodata/ply_golfcourse-strasslach.tif'

# Open the data source get the layer object
# assign extent coordinates
open_shp = ogr.Open(input_shp)
shp_layer = open_shp.GetLayer()
x_min, x_max, y_min, y_max = shp_layer.GetExtent()

# calculate raster resolution
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)

# set the image type for export
image_type = 'GTiff'
driver = gdal.GetDriverByName(image_type)

# create a new raster takes Parameters
# Filename 	the name of the dataset to create. UTF-8 encoded.
# nXSize 	width of created raster in pixels.
# nYSize 	height of created raster in pixels.
# nBands 	number of bands.
# eType 	type of raster.

new_raster = driver.Create(output_raster, x_res, y_res, 1, gdal.GDT_Byte)
new_raster.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))

# get the raster band we want to export too
raster_band = new_raster.GetRasterBand(1)

# assign the no data value to empty cells
raster_band.SetNoDataValue(no_data_value)

# run vector to raster on new raster with input Shapefile
gdal.RasterizeLayer(new_raster, [1], shp_layer, burn_values=[255])