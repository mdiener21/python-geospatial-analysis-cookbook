#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sqrt
import shapefile
from shapely.geometry import asShape, MultiPolygon, MultiPoint, MultiLineString
import json


# calculate the size of our matplotlib output
GM = (sqrt(5) - 1.0) / 2.0
W = 8.0
H = W * GM
SIZE = (W, H)

# colors for matplotlib plots as hex
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


def shp_to_shply_multiply(shapefile_path):
    """
    Convert Polygon Shapefile to Shapely MultiPolygon
    :param shapefile_path: path to a shapefile on disk
    :return: shapely MultiPolygon
    """
    in_ply = shapefile.Reader(shapefile_path)

    # using pyshp reading geometry
    ply_shp = in_ply.shapes()

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

        print "converting to MultiPolygon: "
    else:
        print "one or no features found"
        shply_ply = asShape(ply_shp)
        out_multi_ply = MultiPolygon(shply_ply)

    return out_multi_ply

def shp_2_geojson_file(shapefile_path, out_geojson):
    '''
    Convert Shapefile to GeoJSON
    :param shapefile_path: path to shapefile
    :param out_geojson: path with name of output geojson
    :return:  GeoJSON file
    Example:   shp_2_geojson_file('/home/nice.shp', '/home/out.geojson')
    '''
    # open shapefile
    in_shp = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_shp.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_shp.fields[1:]

    # using list comprehension to create list of field names
    field_names = [field_name[0] for field_name in fc_fields]
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
    in_shp = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_shp.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_shp.fields[1:]

    # using list comprehension to create list of field names
    field_names = [field_name[0] for field_name in fc_fields]
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


def create_valid_shply_poly(in_geom):
    """
    :param in_geom: input valid Shapely geometry objects
    :return: Shapely MultiPolygon cleaned
    """
    list_geom = []
    for g in in_geom:
        # if geometry is NOT valid
        if not g.is_valid:
            print "Oh no invalid geometry"
            # clean polygon with buffer 0 distance trick
            new_buf = g.buffer(0)
            print "now lets make it valid"
            # add new geometry to list
            list_geom.append(new_buf)
        else:
            # add valid geometry to list
            print "yes Valid geom"
            list_geom.append(g)
    # convert new polygons into a new MultiPolygon
    out_new_valid_multi = MultiPolygon(list_geom)
    return out_new_valid_multi

def create_shply_multigeom(in_geojs, geom_type):
    '''

    :param in_geojs: geojson input
    :param geom_type: enter string MultiPolygon, MultiPoint, MultiLineString
    :return: Shapely Geometry
    '''
    shps_list = []
    for feature in in_geojs['features']:
        shape = asShape(feature['geometry'])
        shps_list.append(shape)

    if geom_type == "MultiPolygon":
        new_multi = MultiPolygon(shps_list)
    elif geom_type == "MultiPoint":
        new_multi = MultiPoint(shps_list)
    elif geom_type == "MultiLineString":
        new_multi = MultiLineString(shps_list)
    else:
        print "sorry invalid geom_type only accepted MultiPolygon, MultiPoint, MultiLineString"
    return new_multi

def shp2_shply_geom(shapefile, linetype):
    '''
    Convert Shapefile to Shapely geometries for processing
    :param shapefile: path to shapefile including ending .shp
    :param linetype: MultiPolygon, MultiPoint, MultiLineString
    :return:

    Example usage:
    doit("../geodata/topo_dangles.shp", 'MultiLineString')
    '''

    shp1_data = shp2_geojson_obj(shapefile)
    shply_geom = create_shply_multigeom(shp1_data, linetype)

    return shply_geom
