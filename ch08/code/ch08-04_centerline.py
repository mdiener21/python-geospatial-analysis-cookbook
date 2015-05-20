#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import shapefile
from shapely.geometry import asShape, mapping
from centerline import Centerline

input_hallways = "../geodata/shp/e01_hallways_small_3857.shp"


def write_geojson(outfilename, indata):
    with open(outfilename, "w") as file_out:
        file_out.write(json.dumps(indata))


def create_shapes(shapefile_path):
    '''
    Create our Polygon
    :param shapefile_path: full path to shapefile
    :return: list of Shapely geometries
    '''
    in_ply = shapefile.Reader(shapefile_path)
    ply_shp = in_ply.shapes()
    print type(ply_shp)

    out_multi_ply = [asShape(feature) for feature in ply_shp]

    print "converting to MultiPolygon: "

    return out_multi_ply

# run our function to create Shapely geometries
shply_ply_halls = create_shapes(input_hallways)


def generate_centerlines(polygon_shps):
    '''
    Create centerlines
    :param polygon_shps: input polygons
    :return: dictionary of linestrings
    '''
    dct_centerlines = {}
    print polygon_shps
    print "i see"

    for i, geom in enumerate(polygon_shps):
        print " now running Centerline creation"
        center_obj = Centerline(geom, 0.5)
        center_line_shply_line = center_obj.create_centerline()
        dct_centerlines[i] = center_line_shply_line

    return dct_centerlines

res_centerlines = generate_centerlines(shply_ply_halls)


def export_center(geojs_file, centerlines):
    '''
    Write output to GeoJSON file
    :param centerlines: input dictionary of linestrings
    :return: write to GeoJSON file
    '''
    with open(geojs_file, 'w') as out:

        for i, key in enumerate(centerlines):
            geom = centerlines[key]
            newline = {'id': key, 'geometry': mapping(geom), 'properties': {'id': key}}

            out.write(json.dumps(newline))

print "now creating centerlines geojson"

outgeojs_file = '../geodata/04_centerline_results_final.geojson'

# write the output GeoJSON file to disk
export_center(outgeojs_file, res_centerlines)

print "FINISHED !  Finally"