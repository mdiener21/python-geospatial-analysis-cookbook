#!/usr/bin/env python
# -*- coding: utf-8 -*-

from osgeo import ogr
from osgeo import gdal

#  get raster datasource
open_image = gdal.Open( "../geodata/cadaster_borders-2tone-black-white.png" )
input_band = open_image.GetRasterBand(3)

#  create output datasource
output_shp = "../geodata/cadaster_raster"
shp_driver = ogr.GetDriverByName("ESRI Shapefile")

# create output file name
output_shapefile = shp_driver.CreateDataSource( output_shp + ".shp" )
new_shapefile = output_shapefile.CreateLayer(output_shp, srs = None )

gdal.Polygonize(input_band, None, new_shapefile, -1, [], callback=None)
new_shapefile.SyncToDisk()