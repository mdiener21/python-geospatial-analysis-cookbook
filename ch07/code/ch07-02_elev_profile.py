#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, gdal, os
from gdalconst import GA_ReadOnly
from os.path import realpath
from shapely.geometry import LineString


def get_elevation(x_coord, y_coord, raster, bands, gt):
    """

    :param x_coord:
    :param y_coord:
    :param raster:
    :param bands:
    :param gt:
    :return:
    """
    elevation = []
    xOrigin = gt[0]
    yOrigin = gt[3]
    pixelWidth = gt[1]
    pixelHeight = gt[5]
    px = int((x_coord - xOrigin) / pixelWidth)
    py = int((y_coord - yOrigin) / pixelHeight)
    for j in range(bands):
        band = raster.GetRasterBand(j + 1)
        data = band.ReadAsArray(px, py, 1, 1)
        elevation.append(data[0][0])
    return elevation


line = LineString([(-13659328.8483806, 6450545.73152317), (-13651422.7820022, 6466228.25663444)])

# set directory
in_dem = realpath("../geodata/dem_3857.dem")

# open the image
ds = gdal.Open(in_dem, GA_ReadOnly)

if ds is None:
    print 'Could not open image'
    sys.exit(1)

# get raster bands
bands = ds.RasterCount

# get georeference info
transform = ds.GetGeoTransform()


length_m = line.length

x = []
y = []
z = []
# distance of the topographic profile
distance = []
for currentdistance in range(0, int(length_m), 20):
    # creation of the point on the line
    point = line.interpolate(currentdistance)
    xp, yp = point.x, point.y
    x.append(xp)
    y.append(yp)
    # extraction of the elevation value from the MNT
    z.append(get_elevation(xp, yp, ds, bands, transform)[0])
    distance.append(currentdistance)

print x
print y
print z
print distance
result_profile_x_z = zip(distance,z)

# check if output file exists on disk if yes delete it
if os.path.isfile('output_profile.csv'):
    os.remove('output_profile.csv')

# create new CSV file containing X (distance) and Z value pairs
with open('output_profile.csv', 'a') as outfile:
    # write first row column names into CSV
    outfile.write("distance,elevation" + "\n")
    # loop through each pair and write to CSV
    for x, z in result_profile_x_z:
        outfile.write(str(round(x, 2)) + ',' + str(round(z, 2)) + '\n')
