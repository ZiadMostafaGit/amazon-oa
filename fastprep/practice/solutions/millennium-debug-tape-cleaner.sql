-- Dedupe by timestamp (lowest source_row wins), null out non-positive prices,
-- then forward-fill each asset with the running-count grouping trick.
WITH deduped AS (
    SELECT timestamp,
           CASE WHEN asset_1 > 0 THEN asset_1 END AS a1,
           CASE WHEN asset_2 > 0 THEN asset_2 END AS a2,
           CASE WHEN asset_3 > 0 THEN asset_3 END AS a3,
           ROW_NUMBER() OVER (PARTITION BY timestamp ORDER BY source_row) AS rn
    FROM prices
),
ordered AS (
    SELECT timestamp, a1, a2, a3,
           ROW_NUMBER() OVER (ORDER BY timestamp) - 1 AS row_index,
           COUNT(a1) OVER (ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g1,
           COUNT(a2) OVER (ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g2,
           COUNT(a3) OVER (ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS g3
    FROM deduped
    WHERE rn = 1
)
SELECT row_index,
       timestamp,
       MAX(a1) OVER (PARTITION BY g1) AS asset_1,
       MAX(a2) OVER (PARTITION BY g2) AS asset_2,
       MAX(a3) OVER (PARTITION BY g3) AS asset_3
FROM ordered
ORDER BY row_index
