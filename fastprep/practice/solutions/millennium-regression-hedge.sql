-- Closed-form 2x2 OLS normal equations on de-meaned returns, scaled by -target_quantity.
WITH agg AS (
  SELECT
    COUNT(*)                                                   AS n,
    AVG(CAST(target_return AS REAL))                           AS my,
    AVG(CAST(hedge_1_return AS REAL))                          AS m1,
    AVG(CAST(hedge_2_return AS REAL))                          AS m2,
    SUM(CAST(hedge_1_return AS REAL) * CAST(hedge_1_return AS REAL)) AS s11,
    SUM(CAST(hedge_1_return AS REAL) * CAST(hedge_2_return AS REAL)) AS s12,
    SUM(CAST(hedge_2_return AS REAL) * CAST(hedge_2_return AS REAL)) AS s22,
    SUM(CAST(hedge_1_return AS REAL) * CAST(target_return AS REAL))  AS s1y,
    SUM(CAST(hedge_2_return AS REAL) * CAST(target_return AS REAL))  AS s2y
  FROM returns
),
cm AS (
  SELECT
    s11 - n * m1 * m1 AS a,
    s12 - n * m1 * m2 AS b,
    s22 - n * m2 * m2 AS c,
    s1y - n * m1 * my AS d,
    s2y - n * m2 * my AS e
  FROM agg
)
SELECT
  -CAST(p.target_quantity AS REAL) * ((cm.c * cm.d - cm.b * cm.e) / (cm.a * cm.c - cm.b * cm.b)) AS hedge_1_quantity,
  -CAST(p.target_quantity AS REAL) * ((cm.a * cm.e - cm.b * cm.d) / (cm.a * cm.c - cm.b * cm.b)) AS hedge_2_quantity
FROM cm, positions p
WHERE p.config_id = 1;
