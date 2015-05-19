------- list of custom pg types
-- path_result  (new pgr_costresult  used as result from pgr_dijkstra)
CREATE TYPE public.pgr_costresult_idx AS
   (seq integer,
    id1 integer,
    id2 integer,
    cost double precision,
    idx integer);

-- -- path_result_idx
-- CREATE TYPE path_result_idx AS (vertex_id integer, edge_id integer, cost float8, idx integer);

-- -- SnapReturnType
CREATE TYPE public.indrz_snapreturntype AS
   (gid integer,
    dist double precision,
    geo public.geometry,
    source integer,
    target integer,
    location double precision);

-- SnapReturnType2
CREATE TYPE public.indrz_snapreturntype2 AS
   (gid integer,
    dist double precision,
    geo public.geometry,
    location double precision);

-- arbitraryRouteLayer
CREATE TYPE public.indrz_arbitraryroutelayer AS
   (geom public.geometry,
    source integer,
    target integer,
    gid integer,
    layer integer,
    type integer);

-- arbitraryRouteLayer2
CREATE TYPE public.indrz_arbitraryroutelayer2 AS
   (geom1 public.geometry,
    geom2 public.geometry,
    source integer,
    target integer,
    gid integer,
    layer integer,
    type integer,
    direction character varying);