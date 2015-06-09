#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from shapely.geometry import Point
from shapely.geometry import Polygon

class TestPointPerPolygon(unittest.TestCase):
    def test_inside(self):

        ext = [(0, 0), (0, 2), (2, 2), (2, 0), (0, 0)]
        int = [(1, 1), (1, 1.5), (1.5, 1.5), (1.5, 1)]
        poly_with_hole = Polygon(ext,[int])

        polygon = Polygon([(0, 0), (0, 10), (10, 10),(0, 10)])

        point_on_edge = Point(5, 10)
        point_on_vertex = Point(10, 10)
        point_inside = Point(5, 5)
        point_outside = Point(20,20)
        point_in_hole = Point(1.25, 1.25)

        self.assertTrue(polygon.touches(point_on_vertex))
        self.assertTrue(polygon.touches(point_on_edge))
        self.assertTrue(polygon.contains(point_inside))
        self.assertFalse(polygon.contains(point_outside))
        self.assertTrue(point_in_hole.within(poly_with_hole))

if __name__ == '__main__':
    unittest.main()