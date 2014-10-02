#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import subprocess
path_base = "c:/00_GOMOGI/geodata/"
# path for book code
# path_base = "../geodata/"
# for windows users
command_gdal_translate = "c:/OSGeo4W/bin/gdal_translate.exe"

command_gdalwarp = "c:/OSGeo4W/bin/gdal_translate.exe"
command_gdalinfo = "c:/OSGeo4W/bin/gdalinfo.exe"

# for linux users
#command_gdal_translate = "gdal_translate"

orig_dem_asc = path_base + "ALS_DGM_10m.asc"
# input arcascii format DEM data
input_dem = path_base + "small_elev.asc"

temp_vrt = path_base + "new_virtual_file.vrt"

temp_tiff = path_base + "temp_image.tif"

threejs_webgl_dem = path_base + "webgl_dem.bin"

new_clip_ktn_dem = path_base + "ktn_clip-dhm5.asc"

final_heightmap = path_base + "final_heightmap.png"

output_envi = path_base + "final_envi.bin"


####subprocess.call(["gdalbuildvrt", temp_vrt, orig_dem_asc])
# gdalbuildvrt jotunheimen.vrt my_elevation.dem

# 5000m x 5000m square
# clip_command = command_gdal_translate + " -projwin 477200 189600 482200 184600 -of AAIGrid " \
#                + orig_dem_asc + " " + new_clip_ktn_dem

# [-projwin ulx uly lrx lry] upper left(ul) x
# 500m x 500m DEM  or 50px x 50px  because DEM pixel is 10m x 10m
clip_command = command_gdal_translate + " -projwin 478000 185200 478500 184700 -of AAIGrid " \
               + orig_dem_asc + " " + new_clip_ktn_dem

#print (clip_command.split())
print ("now executing this command: " + clip_command)
print ("so be patient this could take some time...now clipping...")
#subprocess.call(clip_command.split(), shell=False)

dem2tiff = command_gdalwarp + " " + new_clip_ktn_dem + " "  + temp_tiff
print ("now executing this command: " + dem2tiff)
#subprocess.call(dem2tiff.split(), shell=False)

show_tif_info = command_gdalinfo + " -mm " + temp_tiff
tif_info = subprocess.call(show_tif_info.split(), shell=False)
print type(tif_info)
print "foo"
print tif_info
max_min = re.compile(r'Min/Max=')

if max_min.match(str(max_min)):
    print "yes match"
else:
    print "no match"


translate2png = command_gdal_translate + " -scale 700 851 0 255 -outsize 200 200 -of PNG " + temp_tiff + " " + final_heightmap

####subprocess.call(["gdal_translate", "-ot", "UInt16", "-outsize", "200", "200", "-of", "ENVI", temp_tiff, threejs_webgl_dem])
subprocess.call(['gdalwarp',"-te", "","","","", temp_vrt, temp_tiff])

tif_2_envi = "gdal_translate -scale 700 851 0 65535 -ot UInt16 -outsize 200 200 -of ENVI " + temp_tiff + " " + output_envi
#gdal_translate -scale 0 2470 0 65535 -ot UInt16 -outsize 200 200 -of ENVI jotunheimen.tif jotunheimen.bin
