#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shapely.geometry import LineString

# define our simple line
line = LineString([(0.5, 0.5), (2.0, 1.5), (3.0, 0.5)])

# get the coordinates of each vertex in our line
line_original = list(line.coords)
print line_original

# showing how to reverse a linestring
line_reversed = list(line.coords)[::-1]
print line_reversed

# example of the same reversing function on a string for example
hello = 'hello world'
reverse_hello = hello[::-1]
print reverse_hello

# locating the point on a line based on distance from line start
point_on_line = line.interpolate(1.4)
print point_on_line