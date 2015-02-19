from shapely.geometry import Point, Polygon, MultiPolygon

# coords = [(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 1), (0, 0)]
# bowtie = Polygon(coords)


a = Point(1, 1).buffer(1.5)
b = Point(2, 1).buffer(1.5)
# poly = Polygon[(0,0), (0,4), (4,4), (4,0)]
print a
# polygons = MultiPolygon([a, b])
# poly.symmetric_differnce(polygons)


