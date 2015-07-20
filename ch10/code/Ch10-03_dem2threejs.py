#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from jinja2 import Environment, FileSystemLoader


# Create our DEM

# use gdal_translate command to create an image to store elevation values
# -scale from 0 meters to 2625 meters
#     stretch all values to full 16bit  0 to 65535
# -ot is output type = UInt16 unsigned 16bit
# -outsize is 200 x 200 px
# -of is output format ENVI raster image .bin file type
# then our input .tif with elevation
# followed by output file name .bin
subprocess.call("gdal_translate -scale 0 2625 0 65535 "
                "-ot UInt16 -outsize 200 200 -of ENVI "
                "../../ch07/geodata/dem_3857.tif "
                "../geodata/whistler2.bin")


# create our Jinja2 HTML
# create a standard Jinja2 Environment and load all files
# located in the folder templates
env = Environment(loader=FileSystemLoader(["../www/templates"]))

# define which template we want to render
template = env.get_template("base-3d-map.html")

# path and name of input 16bit raster image with our elevation values
dem_3d = "../../geodata/whistler2.bin"

# name and location of the output html file we will generate
out_html = "../www/html/ch10-03_dem3d_map.html"

# dem_file is the variable name we use in our Jinja2 html template file
result = template.render(title="Threejs DEM Viewer", dem_file=dem_3d)

# write out our template to the html file on disk
with open(out_html,mode="w") as f:
    f.write(result)
