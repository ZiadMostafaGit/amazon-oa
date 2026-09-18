-- Centered cross-product matrix, then pivoted Gaussian elimination (window functions) for every regression metric.
WITH
lng(day_id, idx, v) AS (
  SELECT day_id, 0, NYC FROM temperatures
  UNION ALL SELECT day_id, 1, Town1 FROM temperatures
  UNION ALL SELECT day_id, 2, Town2 FROM temperatures
  UNION ALL SELECT day_id, 3, Town3 FROM temperatures
  UNION ALL SELECT day_id, 4, Town4 FROM temperatures
  UNION ALL SELECT day_id, 5, Town5 FROM temperatures
  UNION ALL SELECT day_id, 6, Town6 FROM temperatures
),
names(idx, nm) AS (VALUES (0,'NYC'),(1,'Town1'),(2,'Town2'),(3,'Town3'),(4,'Town4'),(5,'Town5'),(6,'Town6')),
nn AS (SELECT CAST(COUNT(*) AS REAL) AS n FROM temperatures),
stats AS MATERIALIZED (SELECT idx, AVG(v*1.0) AS mu, AVG(v*v*1.0) AS mu2 FROM lng GROUP BY idx),
m0 AS MATERIALIZED (
  SELECT c.i AS i, c.j AS j, c.s - (SELECT n FROM nn)*sa.mu*sb.mu AS v
  FROM (
    SELECT a.idx AS i, b.idx AS j, SUM(a.v*b.v*1.0) AS s
    FROM lng a JOIN lng b ON a.day_id = b.day_id
    GROUP BY a.idx, b.idx
  ) c
  JOIN stats sa ON sa.idx = c.i
  JOIN stats sb ON sb.idx = c.j
),
p1 AS MATERIALIZED (
  SELECT j AS pj FROM (
    SELECT j,
           MAX(CASE WHEN i = 0 THEN v END) AS c,
           MAX(CASE WHEN i = j THEN v END) AS a
    FROM m0 WHERE j <> 0 GROUP BY j
  )
  ORDER BY (c*c)/a DESC, j ASC
  LIMIT 1
),
m1 AS MATERIALIZED (
  SELECT i, j, v - pvi*pvj/pvv AS v FROM (
    SELECT m.i AS i, m.j AS j, m.v AS v, pk.pj AS pj,
           MAX(CASE WHEN m.j = pk.pj THEN m.v END) OVER (PARTITION BY m.i) AS pvi,
           MAX(CASE WHEN m.i = pk.pj THEN m.v END) OVER (PARTITION BY m.j) AS pvj,
           MAX(CASE WHEN m.i = pk.pj AND m.j = pk.pj THEN m.v END) OVER () AS pvv
    FROM m0 m CROSS JOIN p1 pk
  )
  WHERE i <> pj AND j <> pj
),
p2 AS MATERIALIZED (
  SELECT j AS pj FROM (
    SELECT j,
           MAX(CASE WHEN i = 0 THEN v END) AS c,
           MAX(CASE WHEN i = j THEN v END) AS a
    FROM m1 WHERE j <> 0 GROUP BY j
  )
  ORDER BY (c*c)/a DESC, j ASC
  LIMIT 1
),
m2 AS MATERIALIZED (
  SELECT i, j, v - pvi*pvj/pvv AS v FROM (
    SELECT m.i AS i, m.j AS j, m.v AS v, pk.pj AS pj,
           MAX(CASE WHEN m.j = pk.pj THEN m.v END) OVER (PARTITION BY m.i) AS pvi,
           MAX(CASE WHEN m.i = pk.pj THEN m.v END) OVER (PARTITION BY m.j) AS pvj,
           MAX(CASE WHEN m.i = pk.pj AND m.j = pk.pj THEN m.v END) OVER () AS pvv
    FROM m1 m CROSS JOIN p2 pk
  )
  WHERE i <> pj AND j <> pj
),
p3 AS MATERIALIZED (
  SELECT j AS pj FROM (
    SELECT j,
           MAX(CASE WHEN i = 0 THEN v END) AS c,
           MAX(CASE WHEN i = j THEN v END) AS a
    FROM m2 WHERE j <> 0 GROUP BY j
  )
  ORDER BY (c*c)/a DESC, j ASC
  LIMIT 1
),
m3 AS MATERIALIZED (
  SELECT i, j, v - pvi*pvj/pvv AS v FROM (
    SELECT m.i AS i, m.j AS j, m.v AS v, pk.pj AS pj,
           MAX(CASE WHEN m.j = pk.pj THEN m.v END) OVER (PARTITION BY m.i) AS pvi,
           MAX(CASE WHEN m.i = pk.pj THEN m.v END) OVER (PARTITION BY m.j) AS pvj,
           MAX(CASE WHEN m.i = pk.pj AND m.j = pk.pj THEN m.v END) OVER () AS pvv
    FROM m2 m CROSS JOIN p3 pk
  )
  WHERE i <> pj AND j <> pj
),
p4 AS MATERIALIZED (
  SELECT j AS pj FROM (
    SELECT j,
           MAX(CASE WHEN i = 0 THEN v END) AS c,
           MAX(CASE WHEN i = j THEN v END) AS a
    FROM m3 WHERE j <> 0 GROUP BY j
  )
  ORDER BY (c*c)/a DESC, j ASC
  LIMIT 1
),
m4 AS MATERIALIZED (
  SELECT i, j, v - pvi*pvj/pvv AS v FROM (
    SELECT m.i AS i, m.j AS j, m.v AS v, pk.pj AS pj,
           MAX(CASE WHEN m.j = pk.pj THEN m.v END) OVER (PARTITION BY m.i) AS pvi,
           MAX(CASE WHEN m.i = pk.pj THEN m.v END) OVER (PARTITION BY m.j) AS pvj,
           MAX(CASE WHEN m.i = pk.pj AND m.j = pk.pj THEN m.v END) OVER () AS pvv
    FROM m3 m CROSS JOIN p4 pk
  )
  WHERE i <> pj AND j <> pj
),
p5 AS MATERIALIZED (
  SELECT j AS pj FROM (
    SELECT j,
           MAX(CASE WHEN i = 0 THEN v END) AS c,
           MAX(CASE WHEN i = j THEN v END) AS a
    FROM m4 WHERE j <> 0 GROUP BY j
  )
  ORDER BY (c*c)/a DESC, j ASC
  LIMIT 1
),
m5 AS MATERIALIZED (
  SELECT i, j, v - pvi*pvj/pvv AS v FROM (
    SELECT m.i AS i, m.j AS j, m.v AS v, pk.pj AS pj,
           MAX(CASE WHEN m.j = pk.pj THEN m.v END) OVER (PARTITION BY m.i) AS pvi,
           MAX(CASE WHEN m.i = pk.pj THEN m.v END) OVER (PARTITION BY m.j) AS pvj,
           MAX(CASE WHEN m.i = pk.pj AND m.j = pk.pj THEN m.v END) OVER () AS pvv
    FROM m4 m CROSS JOIN p5 pk
  )
  WHERE i <> pj AND j <> pj
),
syy AS (SELECT v AS s FROM m0 WHERE i = 0 AND j = 0),
filt AS (SELECT NYC*1.0 AS v FROM temperatures WHERE Town2 >= 90 AND Town2 <= 100),
fc AS (SELECT COUNT(*) AS c FROM filt),
med AS (
  SELECT COALESCE((SELECT AVG(v) FROM (
      SELECT v FROM filt ORDER BY v
      LIMIT 2 - ((SELECT c FROM fc) % 2)
      OFFSET CASE WHEN (SELECT c FROM fc) = 0 THEN 0 ELSE ((SELECT c FROM fc) - 1) / 2 END
  )), 0.0) AS m
),
maxsd AS (
  SELECT n2.nm AS nm
  FROM stats s JOIN names n2 ON n2.idx = s.idx
  ORDER BY (s.mu2 - s.mu*s.mu) DESC, n2.nm ASC
  LIMIT 1
),
slopesum AS (
  SELECT SUM(ABS(c/a)) AS t FROM (
    SELECT j, MAX(CASE WHEN i = 0 THEN v END) AS c, MAX(CASE WHEN i = j THEN v END) AS a
    FROM m0 WHERE j <> 0 GROUP BY j
  )
),
single AS (
  SELECT n2.nm AS nm, ((SELECT s FROM syy) - (g.c*g.c)/g.a) / (SELECT n FROM nn) AS mse
  FROM (
    SELECT j, MAX(CASE WHEN i = 0 THEN v END) AS c, MAX(CASE WHEN i = j THEN v END) AS a
    FROM m0 WHERE j <> 0 GROUP BY j
  ) g
  JOIN names n2 ON n2.idx = g.j
  ORDER BY mse ASC, nm ASC
  LIMIT 1
),
pairs AS (
  SELECT na.nm || ',' || nb.nm AS nm,
         ((SELECT s FROM syy) -
          (ga.c*ga.c*gb.a - 2*ga.c*gb.c*x.v + gb.c*gb.c*ga.a) / (ga.a*gb.a - x.v*x.v))
         / (SELECT n FROM nn) AS mse
  FROM (
    SELECT j, MAX(CASE WHEN i = 0 THEN v END) AS c, MAX(CASE WHEN i = j THEN v END) AS a
    FROM m0 WHERE j <> 0 GROUP BY j
  ) ga
  JOIN (
    SELECT j, MAX(CASE WHEN i = 0 THEN v END) AS c, MAX(CASE WHEN i = j THEN v END) AS a
    FROM m0 WHERE j <> 0 GROUP BY j
  ) gb ON gb.j > ga.j
  JOIN m0 x ON x.i = ga.j AND x.j = gb.j
  JOIN names na ON na.idx = ga.j
  JOIN names nb ON nb.idx = gb.j
  ORDER BY mse ASC, nm ASC
  LIMIT 1
),
greedy AS (
  SELECT (SELECT nm FROM names WHERE idx = (SELECT pj FROM p1)) || ',' ||
         (SELECT nm FROM names WHERE idx = (SELECT pj FROM p2)) || ',' ||
         (SELECT nm FROM names WHERE idx = (SELECT pj FROM p3)) || ',' ||
         (SELECT nm FROM names WHERE idx = (SELECT pj FROM p4)) || ',' ||
         (SELECT nm FROM names WHERE idx = (SELECT pj FROM p5)) AS nm,
         (SELECT v FROM m5 WHERE i = 0 AND j = 0) / (SELECT n FROM nn) AS mse
)
SELECT metric, towns, value FROM (
  SELECT 1 AS ord, 'max_standard_deviation_place' AS metric, (SELECT nm FROM maxsd) AS towns, NULL AS value
  UNION ALL
  SELECT 2, 'conditional_nyc_median', NULL,
         CAST((SELECT m FROM med) + CASE WHEN (SELECT m FROM med) >= 0 THEN 0.5 ELSE -0.5 END AS INTEGER)
  UNION ALL
  SELECT 3, 'absolute_slope_sum', NULL,
         CAST((SELECT t FROM slopesum) + CASE WHEN (SELECT t FROM slopesum) >= 0 THEN 0.5 ELSE -0.5 END AS INTEGER)
  UNION ALL
  SELECT 4, 'best_single_town', (SELECT nm FROM single), (SELECT mse FROM single)
  UNION ALL
  SELECT 5, 'best_town_pair', (SELECT nm FROM pairs), (SELECT mse FROM pairs)
  UNION ALL
  SELECT 6, 'greedy_five_towns', (SELECT nm FROM greedy), (SELECT mse FROM greedy)
)
ORDER BY ord;
