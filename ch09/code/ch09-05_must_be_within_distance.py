#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils import shp2_geojson_obj
from utils import create_shply_multigeom
from utils import out_geoj

in_shp_lines = "../geodata/topo_line.shp"
shp1_data = shp2_geojson_obj(in_shp_lines)
shp1_lines = create_shply_multigeom(shp1_data, "MultiLineString")

in_shp_poly = "../geodata/topo_polys.shp"
ply_geojs_obj = shp2_geojson_obj(in_shp_poly)
shply_polys = create_shply_multigeom(ply_geojs_obj, "MultiPolygon")


# nearest point using linear referencing
# with interpolation and project
# pt_interpolate = line.interpolate(line.project(point))

# create point centroids from all polygons
# measure distance from centroid to nearest line segment

def within_tolerance(polygons, lines, tolerance):
    """
    Discover if all polygon centroids are within a distance of a linestring
    data set, if not print out centroids that fall outside tolerance
    :param polygons: list of polygons
    :param lines: list of linestrings
    :param tolerance: value of distance in meters
    :return: list of all points within tolerance
    """

    # create our centroids for each polygon
    list_centroids = [x.centroid for x in polygons]

    # list to store all of our centroids within tolerance
    good_points = []

    for centroid in list_centroids:
        for line in lines:
            # calculate point location on line nearest to centroid
            pt_interpolate = line.interpolate(line.project(centroid))
            # determine distance between 2 cartesian points
            # that are less than the tolerance value in meters
            if centroid.distance(pt_interpolate) > tolerance:
                print "to far  " + str(centroid.distance(pt_interpolate))
            else:
                print "hey your in  " + str(centroid.distance(pt_interpolate))
                good_points.append(centroid)

    if len(good_points) > 1:
        return good_points
    else:
        print "sorry no centroids found within your tolerance of " + str(tolerance)

# run our function to get a list of centroids within tolerance
result_points = within_tolerance(shply_polys, shp1_lines, 20000)

if result_points:
    out_geoj(result_points, '../geodata/centroids_within_tolerance.geojson')
else:
    print "sorry cannot export GeoJSON of Nothing"
