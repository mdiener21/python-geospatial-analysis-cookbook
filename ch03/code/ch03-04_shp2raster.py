#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from osgeo import gdal, ogr

# Define pixel_size and NoData value of new raster
pixel_size = 1
NoData_value = -9999

# Filename of input OGR file
input_shp = '/home/mdiener/01_projects/book/geodata/ply_golfcourse-strasslach3857.shp'


# Filename of the raster Tiff that will be created
raster_fn = '/home/mdiener/01_projects/book/geodata/test-foo.tif'

# Open the data source and read in the extent
source_ds = ogr.Open(input_shp)
source_layer = source_ds.GetLayer()
x_min, x_max, y_min, y_max = source_layer.GetExtent()

# Create the destination data source
x_res = int((x_max - x_min) / pixel_size)
y_res = int((y_max - y_min) / pixel_size)
target_ds = gdal.GetDriverByName('GTiff').Create(raster_fn, x_res, y_res, 1, gdal.GDT_Byte)
target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
band = target_ds.GetRasterBand(1)
band.SetNoDataValue(NoData_value)

# Rasterize
gdal.RasterizeLayer(target_ds, [1], source_layer, burn_values=[255])
#gdal.RasterizeLayer(target_ds, [1], source_layer, None, None, [1], ['ALL_TOUCHED=TRUE'])


# one line command line that worked
#gdal_rasterize -burn 255 -l ply_golfcourse-strasslach3857 ply_golfcourse-strasslach3857.shp test.tif
