-- Returns -> sample covariance, then a full 3x3 linear system (identity rows for
-- illiquid assets) solved by Cramer's rule to get the ridge-regularized hedge.
WITH lagged AS (
    SELECT
        CAST(asset_1 AS REAL) AS p1,
        CAST(asset_2 AS REAL) AS p2,
        CAST(asset_3 AS REAL) AS p3,
        LAG(CAST(asset_1 AS REAL)) OVER (ORDER BY period) AS q1,
        LAG(CAST(asset_2 AS REAL)) OVER (ORDER BY period) AS q2,
        LAG(CAST(asset_3 AS REAL)) OVER (ORDER BY period) AS q3
    FROM prices
),
rets AS (
    SELECT p1 / q1 - 1.0 AS r1, p2 / q2 - 1.0 AS r2, p3 / q3 - 1.0 AS r3
    FROM lagged
    WHERE q1 IS NOT NULL
),
st AS (
    SELECT COUNT(*) AS n, AVG(r1) AS m1, AVG(r2) AS m2, AVG(r3) AS m3 FROM rets
),
cov AS (
    SELECT
        SUM((r.r1 - s.m1) * (r.r1 - s.m1)) / (s.n - 1) AS c11,
        SUM((r.r1 - s.m1) * (r.r2 - s.m2)) / (s.n - 1) AS c12,
        SUM((r.r1 - s.m1) * (r.r3 - s.m3)) / (s.n - 1) AS c13,
        SUM((r.r2 - s.m2) * (r.r2 - s.m2)) / (s.n - 1) AS c22,
        SUM((r.r2 - s.m2) * (r.r3 - s.m3)) / (s.n - 1) AS c23,
        SUM((r.r3 - s.m3) * (r.r3 - s.m3)) / (s.n - 1) AS c33
    FROM rets r CROSS JOIN st s
),
port AS (
    SELECT
        MAX(CASE WHEN asset_order = 1 THEN CAST(quantity AS REAL) END) AS x1,
        MAX(CASE WHEN asset_order = 2 THEN CAST(quantity AS REAL) END) AS x2,
        MAX(CASE WHEN asset_order = 3 THEN CAST(quantity AS REAL) END) AS x3,
        MAX(CASE WHEN asset_order = 1 THEN (CASE WHEN is_liquid IN (1, '1', 'true', 'TRUE', 'True', 't') THEN 1 ELSE 0 END) END) AS l1,
        MAX(CASE WHEN asset_order = 2 THEN (CASE WHEN is_liquid IN (1, '1', 'true', 'TRUE', 'True', 't') THEN 1 ELSE 0 END) END) AS l2,
        MAX(CASE WHEN asset_order = 3 THEN (CASE WHEN is_liquid IN (1, '1', 'true', 'TRUE', 'True', 't') THEN 1 ELSE 0 END) END) AS l3
    FROM portfolio
),
cfg AS (
    SELECT CAST(ridge AS REAL) AS g FROM parameters LIMIT 1
),
sys AS (
    SELECT
        cov.c11, cov.c12, cov.c13, cov.c22, cov.c23, cov.c33,
        port.x1, port.x2, port.x3,
        CASE WHEN port.l1 = 0 THEN 1.0 ELSE (CASE WHEN port.l1 = 1 THEN cov.c11 + cfg.g ELSE 0.0 END) END AS a11,
        CASE WHEN port.l1 = 0 THEN 0.0 ELSE (CASE WHEN port.l2 = 1 THEN cov.c12 ELSE 0.0 END) END AS a12,
        CASE WHEN port.l1 = 0 THEN 0.0 ELSE (CASE WHEN port.l3 = 1 THEN cov.c13 ELSE 0.0 END) END AS a13,
        CASE WHEN port.l2 = 0 THEN 0.0 ELSE (CASE WHEN port.l1 = 1 THEN cov.c12 ELSE 0.0 END) END AS a21,
        CASE WHEN port.l2 = 0 THEN 1.0 ELSE (CASE WHEN port.l2 = 1 THEN cov.c22 + cfg.g ELSE 0.0 END) END AS a22,
        CASE WHEN port.l2 = 0 THEN 0.0 ELSE (CASE WHEN port.l3 = 1 THEN cov.c23 ELSE 0.0 END) END AS a23,
        CASE WHEN port.l3 = 0 THEN 0.0 ELSE (CASE WHEN port.l1 = 1 THEN cov.c13 ELSE 0.0 END) END AS a31,
        CASE WHEN port.l3 = 0 THEN 0.0 ELSE (CASE WHEN port.l2 = 1 THEN cov.c23 ELSE 0.0 END) END AS a32,
        CASE WHEN port.l3 = 0 THEN 1.0 ELSE (CASE WHEN port.l3 = 1 THEN cov.c33 + cfg.g ELSE 0.0 END) END AS a33,
        CASE WHEN port.l1 = 0 THEN 0.0 ELSE -(cov.c11 * port.x1 + cov.c12 * port.x2 + cov.c13 * port.x3) END AS b1,
        CASE WHEN port.l2 = 0 THEN 0.0 ELSE -(cov.c12 * port.x1 + cov.c22 * port.x2 + cov.c23 * port.x3) END AS b2,
        CASE WHEN port.l3 = 0 THEN 0.0 ELSE -(cov.c13 * port.x1 + cov.c23 * port.x2 + cov.c33 * port.x3) END AS b3
    FROM cov CROSS JOIN port CROSS JOIN cfg
),
sol AS (
    SELECT
        *,
        a11 * (a22 * a33 - a23 * a32) - a12 * (a21 * a33 - a23 * a31) + a13 * (a21 * a32 - a22 * a31) AS det,
        b1 * (a22 * a33 - a23 * a32) - a12 * (b2 * a33 - a23 * b3) + a13 * (b2 * a32 - a22 * b3) AS d1,
        a11 * (b2 * a33 - a23 * b3) - b1 * (a21 * a33 - a23 * a31) + a13 * (a21 * b3 - b2 * a31) AS d2,
        a11 * (a22 * b3 - b2 * a32) - a12 * (a21 * b3 - b2 * a31) + b1 * (a21 * a32 - a22 * a31) AS d3
    FROM sys
),
fin AS (
    SELECT
        d1 / det AS h1, d2 / det AS h2, d3 / det AS h3,
        x1, x2, x3, c11, c12, c13, c22, c23, c33
    FROM sol
)
SELECT
    printf('%.9f', h1) AS asset_1_hedge,
    printf('%.9f', h2) AS asset_2_hedge,
    printf('%.9f', h3) AS asset_3_hedge,
    printf('%.9f',
      (x1 + h1) * (x1 + h1) * c11
      + (x2 + h2) * (x2 + h2) * c22
      + (x3 + h3) * (x3 + h3) * c33
      + 2.0 * (x1 + h1) * (x2 + h2) * c12
      + 2.0 * (x1 + h1) * (x3 + h3) * c13
      + 2.0 * (x2 + h2) * (x3 + h3) * c23) AS residual_variance
FROM fin;
