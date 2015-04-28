#!/usr/bin/env python
# -*- coding: utf-8 -*-
from osgeo import gdal
from numpy import gradient
from numpy import pi
from numpy import arctan
from numpy import arctan2
from numpy import sin
from numpy import cos
from numpy import sqrt
import matplotlib.pyplot as plt
import subprocess


def hillshade(array, azimuth, angle_altitude):
    """
    :param array: input USGS ASCII DEM / CDED .dem
    :param azimuth: sun position
    :param angle_altitude: sun angle
    :return: numpy array
    """

    x, y = gradient(array)
    slope = pi/2. - arctan(sqrt(x*x + y*y))
    aspect = arctan2(-x, y)
    azimuthrad = azimuth * pi / 180.
    altituderad = angle_altitude * pi / 180.


    shaded = sin(altituderad) * sin(slope)\
     + cos(altituderad) * cos(slope)\
     * cos(azimuthrad - aspect)
    # return 255*(shaded + 1)/2
    return aspect

ds = gdal.Open('../geodata/092j02_0200_demw.dem')
arr = ds.ReadAsArray()

hs_array = hillshade(arr, 90, 45)
plt.imshow(hs_array,cmap='Greys')
plt.savefig('../geodata/hillshade_whistler.png')
plt.show()

# gdal command line tool called gdaldem
# link  http://www.gdal.org/gdaldem.html
# usage:
# gdaldem hillshade input_dem output_hillshade
# [-z ZFactor (default=1)] [-s scale* (default=1)]"
# [-az Azimuth (default=315)] [-alt Altitude (default=45)]
# [-alg ZevenbergenThorne] [-combined]
# [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]

create_hillshade = '''gdaldem hillshade -az 315 -alt 45 ../geodata/092j02_0200_demw.dem ../geodata/hillshade.tif'''

subprocess.call(create_hillshade)