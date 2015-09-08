#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

dem_file = '../geodata/092j02_0200_demw.dem'
hillshade_relief = '../geodata/hillshade.tif'
relief = '../geodata/relief.tif'
final_color_relief = '../geodata/final_color_relief.tif'

create_hillshade = 'gdaldem hillshade -co compress=lzw -compute_edges ' + dem_file +  ' ' + hillshade_relief
subprocess.call(create_hillshade, shell=True)
print create_hillshade

cr = 'gdaldem color-relief -co compress=lzw ' + dem_file + ' ramp.txt ' + relief
subprocess.call(cr)
print cr

merge = 'python hsv_merge.py ' + relief + ' ' + hillshade_relief + ' ' + final_color_relief
subprocess.call(merge)
print merge

create_slope = '''gdaldem slope -co compress=lzw ../geodata/092j02_0200_demw.dem ../geodata/slope_w-degrees.tif '''

subprocess.call(create_slope)


# gdaldem hillshade -co compress=lzw -compute_edges -az 315 -alt 60 -z 2 in_relief.asc 315.tif
# gdaldem hillshade -co compress=lzw -compute_edges -az 275 -alt 60 -z 2 in_relief.asc 275.tif
# gdaldem hillshade -co compress=lzw -compute_edges -az 355 -alt 60 -z 2 in_relief.asc 355.tif
# gdaldem hillshade -co compress=lzw -compute_edges -az 135 -alt 60 -z 2 in_relief.asc 135.tif
# gdaldem slope -co compress=lzw in_relief.asc slope.tif
# gdaldem color-relief -co compress=lzw slope.tif rampslope.txt slope_col.tif
# gdaldem color-relief -co compress=lzw in_relief.asc ramp.txt relief_col.tif