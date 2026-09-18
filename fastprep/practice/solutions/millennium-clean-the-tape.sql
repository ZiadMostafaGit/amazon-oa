-- Dedupe, null out non-positive values, then forward-fill each asset with a correlated "latest earlier non-null" lookup.
WITH dedup AS (
    SELECT DISTINCT
        timestamp AS ts,
        Asset_1   AS a1,
        Asset_2   AS a2,
        Asset_3   AS a3
    FROM prices
),
clean AS (
    SELECT
        ts,
        CASE WHEN a1 IS NOT NULL AND a1 > 0 THEN a1 END AS a1,
        CASE WHEN a2 IS NOT NULL AND a2 > 0 THEN a2 END AS a2,
        CASE WHEN a3 IS NOT NULL AND a3 > 0 THEN a3 END AS a3
    FROM dedup
),
filled AS (
    SELECT
        c.ts AS ts,
        (SELECT p.a1 FROM clean p WHERE p.a1 IS NOT NULL AND p.ts <= c.ts ORDER BY p.ts DESC LIMIT 1) AS a1,
        (SELECT p.a2 FROM clean p WHERE p.a2 IS NOT NULL AND p.ts <= c.ts ORDER BY p.ts DESC LIMIT 1) AS a2,
        (SELECT p.a3 FROM clean p WHERE p.a3 IS NOT NULL AND p.ts <= c.ts ORDER BY p.ts DESC LIMIT 1) AS a3
    FROM clean c
)
SELECT
    ROW_NUMBER() OVER (ORDER BY ts) - 1 AS row_index,
    ts AS timestamp,
    CASE WHEN a1 = CAST(a1 AS INTEGER) THEN CAST(a1 AS INTEGER) ELSE a1 END AS Asset_1,
    CASE WHEN a2 = CAST(a2 AS INTEGER) THEN CAST(a2 AS INTEGER) ELSE a2 END AS Asset_2,
    CASE WHEN a3 = CAST(a3 AS INTEGER) THEN CAST(a3 AS INTEGER) ELSE a3 END AS Asset_3
FROM filled
ORDER BY ts
