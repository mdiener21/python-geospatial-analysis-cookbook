#!/usr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt
import shapefile
from shapely.geometry import asShape, MultiPolygon
import json
from shapely.wkt import dumps

# calculate the size of our matplotlib output

GM = (sqrt(5) - 1.0) / 2.0
W = 8.0
H = W * GM
SIZE = (W, H)

# colors for our plots as hex
GRAY = '#B2B3B7'
BLUE = '#6699cc'
YELLOW = '#ffe680'
RED = '#FF1813'
GREEN = '#24CD17'


# functions slightly modified from Sean Gilles http://toblerity.org/shapely/
# used for drawing our results using matplotlib

# matplotlib makers http://matplotlib.org/api/markers_api.html
def plot_coords_line(axis, object, color='#00b700',
                     symbol='o', label="text", mew=1, ms=7):
    """
    mew = marker edge width in points
    ms = marke size in points

    """
    x, y = object.xy
    axis.plot(x, y, symbol, label=label, color=color,
              mew=mew, ms=ms, zorder=1)


def plot_coords_lines(axis, object, color='#999999'):
    for linestring in object:
        x, y = linestring.xy
        axis.plot(x, y, 'o', color=color, zorder=2)


def plot_line(axis, object, color='#00b700', ls='-',
              linewidth=2, c='g'):
    """
    ls is the line style options :[ '-' | '--' | '-.' | ':' | 'steps' | ...]
    """
    x, y = object.xy
    axis.plot(x, y, color=color, linewidth=linewidth, ls=ls, c=c, zorder=1)


def plot_lines(axis, object, color='#00b700'):
    for line in object:
        x, y = line.xy
        axis.plot(x, y, color=color, alpha=0.4, linewidth=1,
                  solid_capstyle='round', zorder=2)


def set_plot_bounds(object, offset=1.0):
    """
    Creates the limits for x and y axis plot

    :param object: input shapely geometry
    :param offset: amount of space around edge of features
    :return: dictionary of x-range and y-range values for
    """
    bounds = object.bounds
    x_min = bounds[0]
    y_min = bounds[1]
    x_max = bounds[2]
    y_max = bounds[3]
    x_range = [x_min - offset, x_max + offset]
    y_range = [y_min - offset, y_max + offset]

    return {'xrange': x_range, 'yrange': y_range}


def create_shapes(shapefile_path):
    """
    Convert Shapefile Geometry to Shapely MultiPolygon
    :param shapefile_path: path to a shapefile on disk
    :return: shapely MultiPolygon
    """
    in_ply = shapefile.Reader(shapefile_path)

    # using pyshp reading geometry
    ply_shp = in_ply.shapes()
    # ply_shp = in_ply.shapeRecords()
    ply_records = in_ply.records()
    ply_fields = in_ply.fields
    # print ply_records
    # print ply_fields

    if len(ply_shp) > 1:
        # using python list comprehension syntax
        # shapely asShape to convert to shapely geom
        ply_list = [asShape(feature) for feature in ply_shp]

        # create new shapely multipolygon
        out_multi_ply = MultiPolygon(ply_list)

        # # equivalent to the 2 lines above without using list comprehension
        # new_feature_list = []
        # for feature in features:
        #     temp = asShape(feature)
        #     new_feature_list.append(temp)
        # out_multi_ply = MultiPolygon(new_feature_list)

        print "converting to MultiPolygon: " + str(out_multi_ply)
    else:
        print "one or no features found"
        shply_ply = asShape(ply_shp)
        out_multi_ply = MultiPolygon(shply_ply)

    return out_multi_ply

def shp_2_geojson_file(shapefile_path, out_geojson):
    # open shapefile
    in_ply = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_ply.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_ply.fields[1:]

    # using list comprehension to create list of field names
    field_names = [field_name[0] for field_name in fc_fields ]
    my_fc_list = []
    # run through each shape geometry and attribute
    for x in shp_records:
        field_attributes = dict(zip(field_names, x.record))
        geom_j = x.shape.__geo_interface__
        my_fc_list.append(dict(type='Feature', geometry=geom_j,
                               properties=field_attributes))

    # write GeoJSON to a file on disk
    with open(out_geojson, "w") as oj:
        oj.write(json.dumps({'type': 'FeatureCollection',
                        'features': my_fc_list}))


def shp2_geojson_obj(shapefile_path):
    # open shapefile
    in_ply = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_ply.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_ply.fields[1:]

    # using list comprehension to create list of field names
    field_names = [field_name[0] for field_name in fc_fields ]
    my_fc_list = []
    # run through each shape geometry and attribute
    for x in shp_records:
        field_attributes = dict(zip(field_names, x.record))
        geom_j = x.shape.__geo_interface__
        my_fc_list.append(dict(type='Feature', geometry=geom_j,
                               properties=field_attributes))

    geoj_json_obj = {'type': 'FeatureCollection',
                    'features': my_fc_list}

    return geoj_json_obj


def out_geoj(list_geom, out_geoj_file):
    out_geojson = dict(type='FeatureCollection', features=[])

    # generate geojson file output
    for (index_num, ply) in enumerate(list_geom):
        feature = dict(type='Feature', properties=dict(id=index_num))
        feature['geometry'] = ply.__geo_interface__
        out_geojson['features'].append(feature)

    # create geojson file on disk
    json.dump(out_geojson, open(out_geoj_file, 'w'))


def write_wkt(filepath, shply_geom):
    """

    :param filepath: output path for new javascript file
    :param shply_geom: shapely geometry features
    :return:
    """
    with open(filepath, "w") as f:
        # create a javascript variable called ply_data used in html
        # Shapely dumps geometry out to WKT
        f.write("var ply_data = '" + dumps(shply_geom) + "'")