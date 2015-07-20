#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdal2threejs
import subprocess

from jinja2 import Template, Environment, FileSystemLoader


# Create our DEM


subprocess.call("gdal_translate -scale 0 2625 0 65535 -ot UInt16 -outsize 200 200 -of ENVI ../../ch07/geodata/dem_3857.tif ../geodata/whistler.bin")



template = Template('Hello {{ name }}!')
template.render(name='John Doe')

env = Environment(loader=FileSystemLoader(["../www/templates"]))
template = env.get_template( "base-3d-map.html")

dem_3d = "../../geodata/whistler.bin"
out_html = "../www/html/ch10-03_dem3d_map.html"
result = template.render(title="Threejs DEM Viewer", dem_file=dem_3d)

with open(out_html,mode="w") as file:
    file.write(result)
# print result.encode('utf-8')



# dem_file = "../../ch07/geodata/092j02_0200_deme.dem"
dem_file = "../../ch07/geodata/dem_3857.dem"

# gdal2threejs.gdal2threejs(dem_file)

# http://blog.thematicmapping.org/2013/10/textural-terrains-with-threejs.html
# http://blog.thematicmapping.org/2013/10/terrain-building-with-threejs.html
# http://blog.thematicmapping.org/2013/10/terrain-building-with-threejs-part-1.html