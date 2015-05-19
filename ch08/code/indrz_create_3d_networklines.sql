-- if not, go ahead and update
-- make sure tables dont exist

drop table if exists geodata.ch08_e01_networklines_routing;
drop table if exists geodata.ch08_e02_networklines_routing;

-- convert to 3d coordinates with EPSG:3857
SELECT ogc_fid, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(wkb_geometry, 1)),3857)) AS wkb_geometry,
  type_id, cost, length, 0 AS source, 0 AS target
  INTO geodata.ch08_e01_networklines_routing
  FROM geodata.ch08_e01_networklines;

SELECT ogc_fid, ST_Force_3d(ST_Transform(ST_Force_2D(st_geometryN(wkb_geometry, 1)),3857)) AS wkb_geometry,
  type_id, cost, length, 0 AS source, 0 AS target
  INTO geodata.ch08_e02_networklines_routing
  FROM geodata.ch08_e02_networklines;

-- fill the 3rd coordinate according to their floor number
UPDATE geodata.ch08_e01_networklines_routing SET wkb_geometry=ST_Translate(ST_Force_3Dz(wkb_geometry),0,0,1);
UPDATE geodata.ch08_e02_networklines_routing SET wkb_geometry=ST_Translate(ST_Force_3Dz(wkb_geometry),0,0,2);


UPDATE geodata.ch08_e01_networklines_routing SET length =ST_Length(wkb_geometry);
UPDATE geodata.ch08_e02_networklines_routing SET length =ST_Length(wkb_geometry);

-- no cost should be 0 or NULL/empty
UPDATE geodata.ch08_e01_networklines_routing SET cost=1 WHERE cost=0 or cost IS NULL;
UPDATE geodata.ch08_e02_networklines_routing SET cost=1 WHERE cost=0 or cost IS NULL;


-- update unique ids ogc_fid accordingly
UPDATE geodata.ch08_e01_networklines_routing SET ogc_fid=ogc_fid+100000;
UPDATE geodata.ch08_e02_networklines_routing SET ogc_fid=ogc_fid+200000;


-- merge all networkline floors into a single table for routing
DROP TABLE IF EXISTS geodata.networklines_3857;
SELECT * INTO geodata.networklines_3857 FROM
(
(SELECT ogc_fid, wkb_geometry, length, type_id, length*o1.cost as total_cost,
   1 as layer FROM geodata.ch08_e01_networklines_routing o1) UNION
(SELECT ogc_fid, wkb_geometry, length, type_id, length*o2.cost as total_cost,
   2 as layer FROM geodata.ch08_e02_networklines_routing o2))
as foo ORDER BY ogc_fid;

CREATE INDEX wkb_geometry_gist_index
   ON geodata.networklines_3857 USING gist (wkb_geometry);

CREATE INDEX ogc_fid_idx
   ON geodata.networklines_3857 USING btree (ogc_fid ASC NULLS LAST);

CREATE INDEX network_layer_idx
  ON geodata.networklines_3857
  USING hash
  (layer);

-- create populate geometry view with info
SELECT Populate_Geometry_Columns('geodata.networklines_3857'::regclass);

-- update stairs, ramps and elevators to match with the next layer
UPDATE geodata.networklines_3857 SET wkb_geometry=ST_AddPoint(wkb_geometry,
  ST_EndPoint(ST_Translate(wkb_geometry,0,0,1)))
  WHERE type_id=3 OR type_id=5 OR type_id=7;
-- remove the second last point
UPDATE geodata.networklines_3857 SET wkb_geometry=ST_RemovePoint(wkb_geometry,ST_NPoints(wkb_geometry) - 2)
  WHERE type_id=3 OR type_id=5 OR type_id=7;


-- add columns source and target
ALTER TABLE geodata.networklines_3857 add column source integer;
ALTER TABLE geodata.networklines_3857 add column target integer;
ALTER TABLE geodata.networklines_3857 OWNER TO postgres;

-- we dont need the temporary tables any more, delete them
DROP TABLE IF EXISTS geodata.ch08_e01_networklines_routing;
DROP TABLE IF EXISTS geodata.ch08_e02_networklines_routing;

-- remove route nodes vertices table if exists
DROP TABLE IF EXISTS geodata.networklines_3857_vertices_pgr;
-- building routing network vertices (fills source and target columns in those new tables)
SELECT public.pgr_createTopology3d('geodata.networklines_3857', 0.0001, 'wkb_geometry', 'ogc_fid');

