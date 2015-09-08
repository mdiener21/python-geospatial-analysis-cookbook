#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, gdal, os
from gdalconst import GA_ReadOnly
from os.path import realpath
from shapely.geometry import LineString


def get_elevation(x_coord, y_coord, raster, bands, geo_trans):
    """
    get the elevation value of each pixel under
    location x, y
    :param x_coord: x coordinate
    :param y_coord: y coordinate
    :param raster: gdal raster open object
    :param bands: number of bands in image
    :param gt: raster limits
    :return: elevation value of raster at point x,y
    """
    elev_list = []
    x_origin = geo_trans[0]
    y_origin = geo_trans[3]
    pix_width = geo_trans[1]
    pix_height = geo_trans[5]
    x_pt = int((x_coord - x_origin) / pix_width)
    y_pt = int((y_coord - y_origin) / pix_height)
    for band_num in range(bands):
        ras_band = raster.GetRasterBand(band_num + 1)
        ras_data = ras_band.ReadAsArray(x_pt, y_pt, 1, 1)
        elev_list.append(ras_data[0][0])
    return elev_list


def write_to_csv(csv_out, profil_x_z):
    # check if output file exists on disk if yes delete it
    if os.path.isfile(csv_out):
        os.remove(csv_out)

    # create new CSV file containing X (distance) and Z value pairs
    with open(csv_out, 'a') as outfile:
        # write first row column names into CSV
        outfile.write("distance,elevation" + "\n")
        # loop through each pair and write to CSV
        for x, z in profil_x_z:
            outfile.write(str(round(x, 2)) + ',' + str(round(z, 2)) + '\n')


if __name__ == '__main__':
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

    # line defining the the profile
    line = LineString([(-13659328.8483806, 6450545.73152317), (-13651422.7820022, 6466228.25663444)])
    # length in meters of profile line
    length_m = line.length

    # lists of coords and elevations
    x = []
    y = []
    z = []
    # distance of the topographic profile
    distance = []
    for curent_dist in range(0, int(length_m), 20):
        # creation of the point on the line
        point = line.interpolate(curent_dist)
        xp, yp = point.x, point.y
        x.append(xp)
        y.append(yp)
        # extraction of the elevation value from the MNT
        z.append(get_elevation(xp, yp, ds, bands, transform)[0])
        distance.append(curent_dist)

    print (x)
    print (y)
    print (z)
    print (distance)

    # combine distance and elevation vales as pairs
    profile_x_z = zip(distance, z)

    csv_file = os.path.realpath('../geodata/output_profile.csv')
    # output final csv data
    write_to_csv(csv_file, profile_x_z)
