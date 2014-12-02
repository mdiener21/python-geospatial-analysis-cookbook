
# return geometry of shortest path route on a network
query = """SELECT seq, id1 AS node, id2 AS edge, cost, b.the_geom FROM pgr_dijkstra('
                SELECT gid AS id,
                         source::integer,
                         target::integer,
                         length::double precision AS cost
                        FROM ways',
                30, 60, false, false) a LEFT JOIN ways b ON (a.id2 = b.gid);"""
				
# export the route to GeoJSON for visualization
def export_to_geojson(geom):
	"""
	Take in pg geom and convert to GeoJSON
	"""
	geom_pg = geom
	
# now drag and drop the .geojson file to geojson.io to see your line !
	