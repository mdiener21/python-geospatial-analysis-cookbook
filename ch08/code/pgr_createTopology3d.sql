-- Function: public.pgr_createtopology3d(text, double precision, text, text, text, text, text)

-- DROP FUNCTION public.pgr_createtopology3d(text, double precision, text, text, text, text, text);

CREATE OR REPLACE FUNCTION public.pgr_createtopology3d(edge_table text, tolerance double precision, the_geom text DEFAULT 'the_geom'::text, id text DEFAULT 'id'::text, source text DEFAULT 'source'::text, target text DEFAULT 'target'::text, rows_where text DEFAULT 'true'::text)
  RETURNS character varying AS
$BODY$

DECLARE
    points record;
    sridinfo record;
    source_id bigint;
    target_id bigint;
    totcount bigint;
    rowcount bigint;
    srid integer;
    sql text;
    sname text;
    tname text;
    tabname text;
    vname text;
    vertname text;
    gname text;
    idname text;
    sourcename text;
    targetname text;
    notincluded integer;
    i integer;
    naming record;
    flag boolean;
    query text;
    sourcetype  text;
    targettype text;
    debuglevel text;

BEGIN
  raise notice 'PROCESSING:';
  raise notice 'pgr_createTopology3d(''%'',%,''%'',''%'',''%'',''%'',''%'')',edge_table,tolerance,the_geom,id,source,target,rows_where;
  raise notice 'Performing checks, pelase wait .....';
  execute 'show client_min_messages' into debuglevel;


  BEGIN
    RAISE DEBUG 'Cheking % exists',edge_table;
    execute 'select * from pgr_getTableName('||quote_literal(edge_table)||')' into naming;
    sname=naming.sname;
    tname=naming.tname;
    IF sname IS NULL OR tname IS NULL THEN
	RAISE NOTICE '-------> % not found',edge_table;
        RETURN 'FAIL';
    ELSE
	RAISE DEBUG '  -----> OK';
    END IF;

    tabname=sname||'.'||tname;
    vname=tname||'_vertices_pgr';
    vertname= sname||'.'||vname;
    rows_where = ' AND ('||rows_where||')';
  END;

  BEGIN
       raise DEBUG 'Checking id column "%" columns in  % ',id,tabname;
       EXECUTE 'select pgr_getColumnName('||quote_literal(tabname)||','||quote_literal(the_geom)||')' INTO gname;
       EXECUTE 'select pgr_getColumnName('||quote_literal(tabname)||','||quote_literal(id)||')' INTO idname;
       IF idname is NULL then
          raise notice  'ERROR: id column "%"  not found in %',id,tabname;
          RETURN 'FAIL';
       END IF;
       raise DEBUG 'Checking geometry column "%" column  in  % ',the_geom,tabname;
       IF gname is not NULL then
    	  BEGIN
        	raise DEBUG 'Checking the SRID of the geometry "%"', gname;
        	query= 'SELECT ST_SRID(' || quote_ident(gname) || ') as srid '
           		|| ' FROM ' || pgr_quote_ident(tabname)
           		|| ' WHERE ' || quote_ident(gname)
           		|| ' IS NOT NULL LIMIT 1';
                EXECUTE QUERY
           		INTO sridinfo;

        	IF sridinfo IS NULL OR sridinfo.srid IS NULL THEN
            		RAISE NOTICE 'ERROR: Can not determine the srid of the geometry "%" in table %', the_geom,tabname;
            		RETURN 'FAIL';
        	END IF;
        	srid := sridinfo.srid;
        	raise DEBUG '  -----> SRID found %',srid;
        	EXCEPTION WHEN OTHERS THEN
            		RAISE NOTICE 'ERROR: Can not determine the srid of the geometry "%" in table %', the_geom,tabname;
            		RETURN 'FAIL';
    	  END;
        ELSE
                raise notice  'ERROR: Geometry column "%"  not found in %',the_geom,tabname;
                RETURN 'FAIL';
        END IF;
  END;

  BEGIN
       raise DEBUG 'Checking source column "%" and target column "%"  in  % ',source,target,tabname;
       EXECUTE 'select  pgr_getColumnName('||quote_literal(tabname)||','||quote_literal(source)||')' INTO sourcename;
       EXECUTE 'select  pgr_getColumnName('||quote_literal(tabname)||','||quote_literal(target)||')' INTO targetname;
       IF sourcename is not NULL and targetname is not NULL then
                --check that the are integer
                EXECUTE 'select data_type  from information_schema.columns where table_name = '||quote_literal(tname)||
                        ' and table_schema='||quote_literal(sname)||' and column_name='||quote_literal(sourcename) into sourcetype;
                EXECUTE 'select data_type  from information_schema.columns where table_name = '||quote_literal(tname)||
                        ' and table_schema='||quote_literal(sname)||' and column_name='||quote_literal(targetname) into targettype;
                IF sourcetype not in('integer','smallint','bigint')  THEN
          	    raise notice  'ERROR: source column "%" is not of integer type',sourcename;
          	    RETURN 'FAIL';
                END IF;
                IF targettype not in('integer','smallint','bigint')  THEN
          	    raise notice  'ERROR: target column "%" is not of integer type',targetname;
          	    RETURN 'FAIL';
                END IF;
                raise DEBUG  '  ------>OK ';
       END IF;
       IF sourcename is NULL THEN
          	raise notice  'ERROR: source column "%"  not found in %',source,tabname;
          	RETURN 'FAIL';
       END IF;
       IF targetname is NULL THEN
          	raise notice  'ERROR: target column "%"  not found in %',target,tabname;
          	RETURN 'FAIL';
       END IF;
  END;


       IF sourcename=targetname THEN
		raise notice  'ERROR: source and target columns have the same name "%" in %',target,tabname;
                RETURN 'FAIL';
       END IF;
       IF sourcename=idname THEN
		raise notice  'ERROR: source and id columns have the same name "%" in %',target,tabname;
                RETURN 'FAIL';
       END IF;
       IF targetname=idname THEN
		raise notice  'ERROR: target and id columns have the same name "%" in %',target,tabname;
                RETURN 'FAIL';
       END IF;


    BEGIN
      RAISE DEBUG 'Cheking "%" column in % is indexed',idname,tabname;
      if (pgr_isColumnIndexed(tabname,idname)) then
	RAISE DEBUG '  ------>OK';
      else
        RAISE DEBUG ' ------> Adding  index "%_%_idx".',tabname,idname;
        set client_min_messages  to warning;
        execute 'create  index '||pgr_quote_ident(tname||'_'||idname||'_idx')||'
                         on '||pgr_quote_ident(tabname)||' using btree('||quote_ident(idname)||')';
        execute 'set client_min_messages  to '|| debuglevel;
      END IF;
    END;

    BEGIN
      RAISE DEBUG 'Cheking "%" column in % is indexed',sourcename,tabname;
      if (pgr_isColumnIndexed(tabname,sourcename)) then
	RAISE DEBUG '  ------>OK';
      else
        RAISE DEBUG ' ------> Adding  index "%_%_idx".',tabname,sourcename;
        set client_min_messages  to warning;
        execute 'create  index '||pgr_quote_ident(tname||'_'||sourcename||'_idx')||'
                         on '||pgr_quote_ident(tabname)||' using btree('||quote_ident(sourcename)||')';
        execute 'set client_min_messages  to '|| debuglevel;
      END IF;
    END;

    BEGIN
      RAISE DEBUG 'Cheking "%" column in % is indexed',targetname,tabname;
      if (pgr_isColumnIndexed(tabname,targetname)) then
	RAISE DEBUG '  ------>OK';
      else
        RAISE DEBUG ' ------> Adding  index "%_%_idx".',tabname,targetname;
        set client_min_messages  to warning;
        execute 'create  index '||pgr_quote_ident(tname||'_'||targetname||'_idx')||'
                         on '||pgr_quote_ident(tabname)||' using btree('||quote_ident(targetname)||')';
        execute 'set client_min_messages  to ' ||debuglevel;
      END IF;
    END;

    BEGIN
      RAISE DEBUG 'Cheking "%" column in % is indexed',gname,tabname;
      if (pgr_iscolumnindexed(tabname,gname)) then
	RAISE DEBUG '  ------>OK';
      else
        RAISE DEBUG ' ------> Adding unique index "%_%_gidx".',tabname,gname;
        set client_min_messages  to warning;
        execute 'CREATE INDEX '
            || quote_ident(tname || '_' || gname || '_gidx' )
            || ' ON ' || pgr_quote_ident(tabname)
            || ' USING gist (' || quote_ident(gname) || ')';
        execute 'set client_min_messages  to '|| debuglevel;
      END IF;
    END;
       gname=quote_ident(gname);
       idname=quote_ident(idname);
       sourcename=quote_ident(sourcename);
       targetname=quote_ident(targetname);



    BEGIN
       raise DEBUG 'initializing %',vertname;
       execute 'select * from pgr_getTableName('||quote_literal(vertname)||')' into naming;
       IF sname=naming.sname  AND vname=naming.tname  THEN
           execute 'TRUNCATE TABLE '||pgr_quote_ident(vertname)||' RESTART IDENTITY';
           execute 'SELECT DROPGEOMETRYCOLUMN('||quote_literal(sname)||','||quote_literal(vname)||','||quote_literal('the_geom')||')';
       ELSE
           set client_min_messages  to warning;
       	   execute 'CREATE TABLE '||pgr_quote_ident(vertname)||' (id bigserial PRIMARY KEY,cnt integer,chk integer,ein integer,eout integer)';
       END IF;
       execute 'select addGeometryColumn('||quote_literal(sname)||','||quote_literal(vname)||','||
                quote_literal('the_geom')||','|| srid||', '||quote_literal('POINT')||', 3)';
       execute 'CREATE INDEX '||quote_ident(vname||'_the_geom_idx')||' ON '||pgr_quote_ident(vertname)||'  USING GIST (the_geom)';
       execute 'set client_min_messages  to '|| debuglevel;
       raise DEBUG  '  ------>OK';
    END;


  BEGIN
    sql = 'select * from '||pgr_quote_ident(tabname)||' WHERE true'||rows_where ||' limit 1';
    EXECUTE sql into i;
    sql = 'select count(*) from '||pgr_quote_ident(tabname)||' WHERE (' || gname || ' IS NOT NULL AND '||
		idname||' IS NOT NULL)=false '||rows_where;
    EXECUTE SQL  into notincluded;
    EXCEPTION WHEN OTHERS THEN  BEGIN
         RAISE NOTICE 'ERROR: Condition is not correct, please execute the following query to test your condition';
         RAISE NOTICE '%',sql;
         RETURN 'FAIL';
    END;
  END;


    BEGIN
    raise notice 'Creating topology3d, Please wait...';
    execute 'UPDATE ' || pgr_quote_ident(tabname) ||
            ' SET '||sourcename||' = NULL,'||targetname||' = NULL';
    rowcount := 0;
    FOR points IN EXECUTE 'SELECT ' || idname || '::bigint AS id,'
        || ' PGR_StartPoint(' || gname || ') AS source,'
        || ' PGR_EndPoint('   || gname || ') AS target'
        || ' FROM '  || pgr_quote_ident(tabname)
        || ' WHERE ' || gname || ' IS NOT NULL AND ' || idname||' IS NOT NULL '||rows_where
    LOOP

        rowcount := rowcount + 1;
        IF rowcount % 1000 = 0 THEN
            RAISE NOTICE '% edges processed', rowcount;
        END IF;


        source_id := pgr_pointToId3d(points.source, tolerance,vertname,srid);
        target_id := pgr_pointToId3d(points.target, tolerance,vertname,srid);
        BEGIN
        sql := 'UPDATE ' || pgr_quote_ident(tabname) ||
            ' SET '||sourcename||' = '|| source_id::text || ','||targetname||' = ' || target_id::text ||
            ' WHERE ' || idname || ' =  ' || points.id::text;

        IF sql IS NULL THEN
            RAISE NOTICE 'WARNING: UPDATE % SET source = %, target = % WHERE % = % ', tabname, source_id::text, target_id::text, idname,  points.id::text;
        ELSE
            EXECUTE sql;
        END IF;
        EXCEPTION WHEN OTHERS THEN
            RAISE NOTICE '%', SQLERRM;
            RAISE NOTICE '%',sql;
            RETURN 'FAIL';
        end;
    END LOOP;
    raise notice '-------------> TOPOLOGY 3D CREATED FOR  % edges', rowcount;
    RAISE NOTICE 'Rows with NULL geometry or NULL id: %',notincluded;
    Raise notice 'Vertices table for table % is: %',pgr_quote_ident(tabname),pgr_quote_ident(vertname);
    raise notice '----------------------------------------------';
    END;
    RETURN 'OK';

END;


$BODY$
  LANGUAGE plpgsql VOLATILE STRICT
  COST 100;
ALTER FUNCTION public.pgr_createtopology3d(text, double precision, text, text, text, text, text)
  OWNER TO postgres;
COMMENT ON FUNCTION public.pgr_createtopology3d(text, double precision, text, text, text, text, text) IS 'args: edge_table,tolerance, the_geom:=''the_geom'',source:=''source'', target:=''target'',rows_where:=''true'' - fills columns source and target in the geometry table and creates a vertices table for selected rows';
