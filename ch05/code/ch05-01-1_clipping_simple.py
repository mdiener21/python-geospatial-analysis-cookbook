#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from shapely.geometry import asShape

# define output GeoJSON file
res_line_intersect = os.path.realpath("../geodata/ch05-01-geojson.js")

# input GeoJSON features
simple_line = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"line to clip"},"geometry":{"type":"LineString","coordinates":[[5.767822265625,50.14874640066278],[11.901806640625,50.13466432216696],[4.493408203125,48.821332549646634]]}}]}
clip_boundary = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"Clipping boundary circle"},"geometry":{"type":"Polygon","coordinates":[[[6.943359374999999,50.45750402042058],[7.734374999999999,51.12421275782688],[8.96484375,51.316880504045876],[10.1513671875,51.34433866059924],[10.8544921875,51.04139389812637],[11.25,50.56928286558243],[11.25,49.89463439573421],[10.810546875,49.296471602658094],[9.6240234375,49.03786794532644],[8.1298828125,49.06666839558117],[7.5146484375,49.38237278700955],[6.8994140625,49.95121990866206],[6.943359374999999,50.45750402042058]]]}}]}

# create shapely geometry from FeatureCollection
# access only the geomety part of GeoJSON
shape_line = asShape(simple_line['features'][0]['geometry'])
shape_circle = asShape(clip_boundary['features'][0]['geometry'])

# run the intersection
shape_intersect = shape_line.intersection(shape_circle)

# define output GeoJSON dictionary
out_geojson = dict(type='FeatureCollection', features=[])

# generate GeoJSON features
for (index_num, line) in enumerate(shape_intersect):
    feature = dict(type='Feature', properties=dict(id=index_num))
    feature['geometry'] = line.__geo_interface__
    out_geojson['features'].append(feature)

# write out GeoJSON to javascript file
# this file is read in our html and
# displayed as GeoJSON on the leaflet map
# called /html/ch05-01-clipping.html
with open(res_line_intersect, 'w') as js_file:
    js_file.write('var big_circle = {0}'.format(json.dumps(clip_boundary)))
    js_file.write("\n")
    js_file.write('var big_linestring = {0}'.format(json.dumps(simple_line)))
    js_file.write("\n")
    js_file.write('var simple_intersect = {0}'.format(json.dumps(out_geojson)))
