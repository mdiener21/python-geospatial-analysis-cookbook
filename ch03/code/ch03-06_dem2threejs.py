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

#subprocess.call(translate2png.split(), shell=False)
#gdal_translate -scale 0 2470 0 255 -outsize 200 200 -of PNG jotunheimen.tif jotunheimen.png

# gdal_translate -scale 0 2470 0 65535 -ot UInt16 -outsize 200 200 -of ENVI jotunheimen.tif jotunheimen.bin
#gdal_translate -projwin 478036.238528 185166.392009 478494.852057 184768.350079 C:/00_GOMOGI/geodata/ALS_DGM_10m.asc
#gdal_translate -projwin 478036.238528 185166.392009 478494.852057 184768.350079 -of AAIGrid C:/00_GOMOGI/geodata/ALS_DGM_10m.asc C:/Users/Michael/Downloads/ktn_clip-dhm.asc

# clip dem and convert to .tif
# if you want to clip to extents use -te [-te xmin ymin xmax ymax]
# 1. gdalwarp to clip and convert to tif
####subprocess.call(['gdalwarp',"-te", "","","","", temp_vrt, temp_tiff])

#gdalwarp jotunheimen.vrt jotunheimen.tif
#http://www.gdal.org/gdalwarp.html

####print (subprocess.call(["gdalinfo", "-mm", temp_tiff]))

# show new tiff image information
# gdalinfo -mm jotunheimen.tif

####subprocess.call(["gdal_translate", "-ot", "UInt16", "-outsize", "200", "200", "-of", "ENVI", temp_tiff, threejs_webgl_dem])

#gdal_translate -scale 0 2470 0 65535 -ot UInt16 -outsize 200 200 -of ENVI jotunheimen.tif jotunheimen.bin
# http://www.gdal.org/gdal_translate.html

# gdalwarp -te 484500 6818000 486500 6820000 jotunheimen.vrt besseggen.tif
#
# gdal_translate -scale 982 1742 0 255 -of PNG besseggen.tif besseggen.png
#
# gdal_translate -scale 982 1905 0 65535 -ot UInt16 -of ENVI besseggen.tif besseggen.bin
#
# Lastly, I'm creating a tiny heightmap of only 10 x 10 px for testing purposes:
# -of is output format here .png is output
# gdal_translate -scale 982 1905 0 255 -outsize 10 10 -of PNG besseggen.tif besseggen10.png
#-of is ENVI format .bin for threejs
# gdal_translate -scale 982 1905 0 65535 -outsize 10 10 -ot UInt16 -of ENVI besseggen.tif besseggen10.bin