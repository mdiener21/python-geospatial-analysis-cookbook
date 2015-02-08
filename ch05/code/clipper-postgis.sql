SELECT n As gid, ST_Union(ST_GeometryN(div_geom, n), the_knife) as
the_geom
FROM
(SELECT ST_Difference(sol.the_geom,ST_Buffer(sol.div_line,0.001)) As
div_geom, ST_Buffer(sol.div_line,0.001) As the_knife
FROM
(SELECT foo.the_geom,
ST_Intersection(foo.the_geom,ST_MakeLine(ST_MakePoint(ST_XMin(foo.the_ge
om), ST_YMax(foo.the_geom)), ST_MakePoint(ST_XMAX(foo.the_geom),
ST_YMIN(foo.the_geom)))) as div_line
FROM (SELECT
CAST('0103000000010000000500000080D6741' As geometry) As
the_geom) As foo) As sol) As sol2 CROSS JOIN generate_series(1,30) n
WHERE n <= ST_NumGeometries(sol2.div_geom)