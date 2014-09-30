#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

# input arcascii format DEM data
input_dem = "../geodata/small_elev.asc"
temp_vrt = "../geodata/new_virtual_file.vrt"

temp_tiff = "../geodata/temp_image.tif"

threejs_webgl_dem = "../geodata/webgl_dem.bin"



# url = 'http://www.whatever.com'
# cmd = 'ffplay -vn -nodisp -bufsize 4096 '.split()
# subprocess.call(cmd + [str(url)], shell=False)
#
subprocess.call(["gdalbuildvrt", temp_vrt, input_dem])
# gdalbuildvrt jotunheimen.vrt my_elevation.dem

# clip dem and convert to .tif
# if you want to clip to extents use -te [-te xmin ymin xmax ymax]
subprocess.call(['gdalwarp',temp_vrt, temp_tiff])
#gdalwarp jotunheimen.vrt jotunheimen.tif
#http://www.gdal.org/gdalwarp.html

print (subprocess.call(["gdalinfo", "-mm", temp_tiff]))

# show new tiff image information
# gdalinfo -mm jotunheimen.tif

subprocess.call(["gdal_translate", "-ot", "UInt16", "-outsize", "200", "200", "-of", "ENVI", temp_tiff, threejs_webgl_dem])
#gdal_translate -scale 0 2470 0 65535 -ot UInt16 -outsize 200 200 -of ENVI jotunheimen.tif jotunheimen.bin
# http://www.gdal.org/gdal_translate.html

# gdalwarp -te 484500 6818000 486500 6820000 jotunheimen.vrt besseggen.tif
#
# gdal_translate -scale 982 1742 0 255 -of PNG besseggen.tif besseggen.png
#
# gdal_translate -scale 982 1905 0 65535 -ot UInt16 -of ENVI besseggen.tif besseggen.bin
#
# Lastly, I'm creating a tiny heightmap of only 10 x 10 px for testing purposes:
#
# gdal_translate -scale 982 1905 0 255 -outsize 10 10 -of PNG besseggen.tif besseggen10.png
#
# gdal_translate -scale 982 1905 0 65535 -outsize 10 10 -ot UInt16 -of ENVI besseggen.tif besseggen10.bin