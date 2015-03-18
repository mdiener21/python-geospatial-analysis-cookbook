#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pprint import pprint
import shapefile
from geojson import Feature, FeatureCollection
from shapely.geometry import asShape, MultiPolygon, Polygon, mapping, shape
from shapely.ops import polygonize
from shapely.wkt import dumps
from geojson import FeatureCollection, MultiPolygon
import json
from geojson import loads, Feature, FeatureCollection

shp1 = "../geodata/temp1-ply.shp"
shp2 = "../geodata/temp2-ply.shp"

out_geojson1 = "ol3/data/res_union1.geojson"
out_geojson2 = "ol3/data/res_union2.geojson"
out_wkt = "ol3/data/results_union.js"

# http://gis.stackexchange.com/questions/11987/polygon-overlay-with-shapely
def shapefile_to_geojson(shapefile_path, output_geojson="ol3/data/res_union.geojson"):
    # open shapefile
    in_ply = shapefile.Reader(shapefile_path)
    # get a list of geometry and records
    shp_records = in_ply.shapeRecords()
    # get list of fields excluding first list object
    fc_fields = in_ply.fields[1:]

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
    with open(output_geojson, "w") as oj:
        oj.write(json.dumps({'type': 'FeatureCollection',
                             'features': my_fc_list}))

    geoj_json_obj = json.dumps({'type': 'FeatureCollection',
                                'features': my_fc_list})
    # print geoj_json_obj
    return geoj_json_obj


shp1_dic = json.loads(shapefile_to_geojson(shp1, out_geojson1))
shp2_dic = json.loads(shapefile_to_geojson(shp2, out_geojson2))
#print shp1_dic

shp1_multiply = []
shp2_multiply = []



#
# create shapely geometry objects for fairways
for feature in shp1_dic['features']:
    shape = asShape(feature['geometry'])
    #shp1_multiply.append(shape.boundary)
    shp1_multiply.append(shape)
for fs in shp2_dic['features']:
    s = asShape(fs['geometry'])
    #shp1_multiply.append(s.boundary)
    shp1_multiply.append(s)
# print shp1_multiply
# for f in shp1_multiply:
#     wkb = dumps(f)
# print wkb
from shapely.ops import cascaded_union, unary_union


result = unary_union(shp1_multiply)


def write_wkt(filepath, features):
    with open(filepath, "w") as f:
        # create a js variable called ply_data used in html
        # Shapely dumps geometry out to WKT
        f.write("var ply_data = '" + dumps(features) + "'")

# write to our output js file the new polygon as wkt
write_wkt("ol3/data/res_cascade_union.js", result)



#shp1_plys = MultiPolygon(shp1_multiply)

#print shp1_plys

# list_f3 = []
# shp3_multiply = json.dumps({'type': 'FeatureCollection', 'features': list_f3})

# with open('outfile.geojson', "w") as oj:
# list_f3 = []
# list_f2 = []
# list_f1_prop = []
# list_f1_geom = []
# list_f2_prop = []
# list_f2_geom = []
# int_ply = []
# p = []
#
#
# for f1 in shp1_dic['features']:
#     shape1_id = int(f1['properties']['id'])
#     shape1_geom = asShape(f1['geometry'])
#     shape1_prop = f1['properties']
#     print shape1_prop
#     input_id = "_1"
#     fid1_int = int(f1['properties']['id'])
#     print fid1_int
#     list_f1_prop.append(shape1_prop)
#     list_f1_geom.append(shape1_geom)
#
#     print "line 82"
#
# for f2 in shp2_dic['features']:
#     print "line 85 " + str(f2)
#     shape2_geom = asShape(f2['geometry'])
#     shape2_id = int(f2['properties']['id'])
#     shape2_prop = f2['properties']
#     list_f2_prop.append(shape2_prop)
#     list_f2_geom.append(shape2_geom)
#     props = f2['properties']
    # props_f1 = f1['properties']
    # for k, v in props_f1.iteritems():
    #     props[k + input_id] = v
    # p.append({ 'properties': props,
    #            'geometry': mapping(shape1_geom.intersection(shape2_geom))
    #          })

# oj.write(json.dumps({
#             'type': 'FeatureCollection',
#             'features': p
# }))

# f1_multi = MultiPolygon(list_f1_geom)
# f2_multi = MultiPolygon(list_f2_geom)
# print f2_multi
# print f1_multi
# pprint(f1_multi.intersection(f2_multi))
#outer_bndry = in_ply1.boundary.union(in_ply2.boundary)
#
# shp1_multiply.append(shape1_geom)

def create_shapes(shapefile_path):
    """
    Convert Shapefile Geometry to Shapely MultiPolygon
    :param shapefile_path: path to a shapefile on disk
    :return: shapely MultiPolygon
    """
    in_ply = shapefile.Reader(shapefile_path)

    # using pyshp reading geometry
    # ply_shp = in_ply.shapes()
    ply_shp = in_ply.shapeRecords()
    ply_records = in_ply.records()

    if len(ply_shp) > 1:
        # using python list comprehension syntax
        # shapely asShape to convert to shapely geom
        new_list = [shape(feature) for feature in ply_shp]

        # create new shapely multipolygon
        out_multi_ply = MultiPolygon(new_list)

        # # equivalent to list comprehension syntax
        # new_feature_list = []
        # for feature in features:
        #     temp = asShape(feature)
        #     new_feature_list.append(temp)
        # out_multi_ply = MultiPolygon(new_feature_list)

        print "converting to MultiPolygon: " + str(out_multi_ply)
    else:
        print "one or no features found"
        temp = asShape(ply_shp)
        out_multi_ply = MultiPolygon(temp)

    return out_multi_ply
    # return ply_shp


# access the geometries of each polygon using pyshp
# in_ply_2_shape = create_shapes(shp1)
# in_ply_1_shape = create_shapes(shp2)
# print in_ply_1_shape

def create_union(in_ply1, in_ply2):
    """
    Create union polygon
    :param in_ply1: first input polygon
    :param in_ply2: second input polygon
    :return: shapely polgon
    """
    # union the polygon outer linestrings together
    outer_bndry = in_ply1.boundary.union(in_ply2.boundary)

    # rebuild linestrings into polygons
    output_poly = polygonize(outer_bndry)
    # pprint(list(polygonize(outer_bndry)))
    return output_poly

# result_union = create_union(in_ply_1_shape,in_ply_2_shape)
#pprint(mapping(json.dumps(result_union)))


# p.append({ 'properties': props,
#            'geometry': mapping(shape1_geom.intersection(shape2_geom))
#          })

# # setup matplotlib figure that will display the results
# fig = pyplot.figure(1, figsize=SIZE, dpi=90, facecolor="white")
#
# # add a little more space around subplots
# fig.subplots_adjust(hspace=.5)
#
# ax = fig.add_subplot(111)
#
# # draw each MultiPolygon green
# for poly in result:
#     patch3 = PolygonPatch(poly, fc='green',
#                           alpha=0.5, zorder=2)
#     ax.add_patch(patch3)
#
# ax.set_title('symmetric difference')
#
# # define the area that plot will fit into
# x_range = set_plot_bounds(result, 50)['xrange']
# y_range = set_plot_bounds(result, 50)['yrange']
#
# ax.set_xlim(*x_range)
# ax.set_ylim(*y_range)
# ax.set_aspect(1)
#
# pyplot.show()

