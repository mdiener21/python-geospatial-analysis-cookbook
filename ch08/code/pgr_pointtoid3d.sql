-- Function: public.pgr_pointtoid3d(geometry, double precision, text, integer)

-- DROP FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer);

CREATE OR REPLACE FUNCTION public.pgr_pointtoid3d(point geometry, tolerance double precision, vertname text, srid integer)
  RETURNS bigint AS
$BODY$ 
DECLARE
    rec record; 
    pid bigint; 

BEGIN
    execute 'SELECT ST_3DDistance(the_geom,ST_GeomFromText(st_astext('||quote_literal(point::text)||'),'||srid||')) AS d, id, the_geom
        FROM '||pgr_quote_ident(vertname)||'
        WHERE ST_DWithin(the_geom, ST_GeomFromText(st_astext('||quote_literal(point::text)||'),'||srid||'),'|| tolerance||')
        ORDER BY d
        LIMIT 1' INTO rec ;
    IF rec.id is not null THEN
        pid := rec.id;
    ELSE
        execute 'INSERT INTO '||pgr_quote_ident(vertname)||' (the_geom) VALUES ('||quote_literal(point::text)||')';
        pid := lastval();
    END IF;

    RETURN pid;

END;
$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer)
  OWNER TO postgres;
COMMENT ON FUNCTION public.pgr_pointtoid3d(geometry, double precision, text, integer) IS 'args: point geometry,tolerance,verticesTable,srid - inserts the point into the vertices table using tolerance to determine if its an existing point and returns the id assigned to it';
