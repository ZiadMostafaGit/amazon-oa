-- Per-asset return volatility (sample stddev) and request frequency, min-max
-- normalized across the three assets, blended into the liquidity score.
WITH lagged AS (
    SELECT
        CAST(Asset_1 AS REAL) AS p1,
        CAST(Asset_2 AS REAL) AS p2,
        CAST(Asset_3 AS REAL) AS p3,
        LAG(CAST(Asset_1 AS REAL)) OVER (ORDER BY timestamp) AS b1,
        LAG(CAST(Asset_2 AS REAL)) OVER (ORDER BY timestamp) AS b2,
        LAG(CAST(Asset_3 AS REAL)) OVER (ORDER BY timestamp) AS b3
    FROM prices
),
rets AS (
    SELECT ROUND(p1 / b1 - 1.0, 12) AS r1,
           ROUND(p2 / b2 - 1.0, 12) AS r2,
           ROUND(p3 / b3 - 1.0, 12) AS r3
    FROM lagged WHERE b1 IS NOT NULL
),
mu AS (
    SELECT COUNT(*) AS n, AVG(r1) AS m1, AVG(r2) AS m2, AVG(r3) AS m3 FROM rets
),
sd AS (
    SELECT
        SQRT(SUM((r.r1 - u.m1) * (r.r1 - u.m1)) / (u.n - 1)) AS v1,
        SQRT(SUM((r.r2 - u.m2) * (r.r2 - u.m2)) / (u.n - 1)) AS v2,
        SQRT(SUM((r.r3 - u.m3) * (r.r3 - u.m3)) / (u.n - 1)) AS v3
    FROM rets r CROSS JOIN mu u
),
assets AS (
    SELECT 'Asset_1' AS asset, v1 AS vol FROM sd
    UNION ALL SELECT 'Asset_2', v2 FROM sd
    UNION ALL SELECT 'Asset_3', v3 FROM sd
),
metrics AS (
    SELECT a.asset AS asset, a.vol AS vol,
           CAST((SELECT COUNT(*) FROM requests q WHERE q.asset = a.asset) AS REAL)
             / (SELECT COUNT(*) FROM requests) AS freq
    FROM assets a
),
rng AS (
    SELECT MIN(vol) AS vlo, MAX(vol) AS vhi, MIN(freq) AS flo, MAX(freq) AS fhi
    FROM metrics
),
norm AS (
    SELECT m.asset AS asset,
           CASE WHEN r.vhi - r.vlo = 0 THEN 0.5 ELSE (m.vol - r.vlo) / (r.vhi - r.vlo) END AS nv,
           CASE WHEN r.fhi - r.flo = 0 THEN 0.5 ELSE (m.freq - r.flo) / (r.fhi - r.flo) END AS nf
    FROM metrics m CROSS JOIN rng r
)
SELECT asset AS asset,
       RTRIM(RTRIM(printf('%.6f', 0.1 + 0.9 * (0.5 * (1.0 - nv) + 0.5 * nf)), '0'), '.')
         AS liquidity_score
FROM norm
ORDER BY asset
