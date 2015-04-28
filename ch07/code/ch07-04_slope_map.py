#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

# SLOPE
# - To generate a slope map from any GDAL-supported elevation raster :
# gdaldem slope input_dem output_slope_map"
# [-p use percent slope (default=degrees)] [-s scale* (default=1)]
# [-alg ZevenbergenThorne]
# [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]

create_slope = '''gdaldem slope -co compress=lzw -p ../geodata/092j02_0200_demw.dem ../geodata/slope.tif '''

subprocess.call(create_slope)

# ASPECT
# - To generate an aspect map from any GDAL-supported elevation raster
# Outputs a 32-bit float raster with pixel values from 0-360 indicating azimuth :
# gdaldem aspect input_dem output_aspect_map"
# [-trigonometric] [-zero_for_flat]
# [-alg ZevenbergenThorne]
# [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]

create_aspect = '''gdaldem aspect -co compress=lzw ../geodata/092j02_0200_demw.dem ../geodata/aspect.tif '''

subprocess.call(create_aspect)
