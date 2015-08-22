#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.geometry import asShape
from shapely.ops import polygonize
import json
import os

# define output GeoJSON file
output_result = os.path.realpath("../geodata/ch05-02-geojson.js")

# input GeoJSON features
line_geojs = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"line to clip"},"geometry":{"type":"LineString","coordinates":[[5.767822265625,50.14874640066278],[11.901806640625,50.13466432216696],[4.493408203125,48.821332549646634]]}}]}
poly_geojs = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{"name":"Clipping boundary circle"},"geometry":{"type":"Polygon","coordinates":[[[6.943359374999999,50.45750402042058],[7.734374999999999,51.12421275782688],[8.96484375,51.316880504045876],[10.1513671875,51.34433866059924],[10.8544921875,51.04139389812637],[11.25,50.56928286558243],[11.25,49.89463439573421],[10.810546875,49.296471602658094],[9.6240234375,49.03786794532644],[8.1298828125,49.06666839558117],[7.5146484375,49.38237278700955],[6.8994140625,49.95121990866206],[6.943359374999999,50.45750402042058]]]}}]}

# create shapely geometry from FeatureCollection
# access only the geomety part of GeoJSON
cutting_line = asShape(line_geojs['features'][0]['geometry'])
poly_to_split = asShape(poly_geojs['features'][0]['geometry'])

# convert circle polygon to linestring of circle boundary
bndry_as_line = poly_to_split.boundary

# combine new boundary lines with the input set of lines
result_union_lines = bndry_as_line.union(cutting_line)

# re-create polygons from unioned lines
new_polygons = polygonize(result_union_lines)

# stores the final split up polygons
new_cut_ply = []

# identify which new polygon we want to keep
for poly in new_polygons:
    # check if new poly is inside original otherwise ignore it
    if poly.centroid.within(poly_to_split):
        print ("creating polgon")
        # add only polygons that overlap original for export
        new_cut_ply.append(poly)
    else:
        print ("This polygon is outside of the input features")

# define output GeoJSON dictionary
out_geojson = dict(type='FeatureCollection', features=[])

# generate GeoJSON features
for (index_num, geom) in enumerate(new_cut_ply):
    feature = dict(type='Feature', properties=dict(id=index_num))
    feature['geometry'] = geom.__geo_interface__
    out_geojson['features'].append(feature)

# write out GeoJSON to javascript file
# this file is read in our html and
# displayed as GeoJSON on the leaflet map
# called /html/ch05-02.html
with open(output_result, 'w') as js_file:
    js_file.write('var cut_poly_result = {0}'.format(json.dumps(out_geojson)))
