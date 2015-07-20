#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from PIL import Image
from jinja2 import Environment, FileSystemLoader


# convert from Canada UTM http://epsg.io/3157/map   to 3857

subprocess.call("gdalwarp -s_srs EPSG:3157 -t_srs EPSG:3857 -overwrite "
                "-te -13664479.091 6446253.250 -13636616.770 6489702.670"
                " ../geodata/canimage_092j02_tif/092j02_1_1.tif ../geodata/whistler_ortho.tif")

subprocess.call("gdal_translate -outsize 200 200 "
                "../geodata/whistler_ortho.tif "
                "../geodata/whistler_ortho_f.tif")

infile = '../geodata/whistler_ortho_f.tif'
drape_texture = '../../geodata/whistler_ortho_f.jpg'
Image.open(infile).save(drape_texture)

env = Environment(loader=FileSystemLoader(["../www/templates"]))
template = env.get_template( "base-3d-map-drape.html")

dem_3d = "../../geodata/whistler2.bin"


out_html = "../www/html/ch10-04_dem3d_map_drape.html"
result = template.render(title="Threejs DEM Drape Viewer", dem_file=dem_3d,
                         texture_map=drape_texture)

with open(out_html,mode="w") as file:
    file.write(result)
