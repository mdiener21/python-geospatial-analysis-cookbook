from osgeo import ogr
from osgeo import gdal
import sys

#  get raster datasource
open_image = gdal.Open( "INPUT.tif" )
input_band = open_image.GetRasterBand(3)

#  create output datasource
dst_layername = "POLYGONIZED_STUFF"
drv = ogr.GetDriverByName("ESRI Shapefile")

# create output file name
dst_ds = drv.CreateDataSource( dst_layername + ".shp" )
dst_layer = dst_ds.CreateLayer(dst_layername, srs = None )

gdal.Polygonize(input_band, None, dst_layer, -1, [], callback=None)