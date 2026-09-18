-- Correlated scalar subquery: newest eligible valid quote, exact integer-second staleness bound.
SELECT CASE WHEN p = CAST(p AS INTEGER) THEN CAST(p AS INTEGER) ELSE p END AS price
FROM (
    SELECT (
        SELECT CASE
                 WHEN (CAST(strftime('%s', q.query_time) AS INTEGER)
                       - CAST(strftime('%s', pr.timestamp) AS INTEGER))
                      > q.max_staleness_minutes * 60
                 THEN NULL
                 ELSE CASE q.asset
                        WHEN 'Asset_1' THEN pr.Asset_1
                        WHEN 'Asset_2' THEN pr.Asset_2
                        ELSE pr.Asset_3
                      END
               END
        FROM prices pr
        WHERE CAST(strftime('%s', pr.timestamp) AS INTEGER)
              <= CAST(strftime('%s', q.query_time) AS INTEGER)
          AND (CASE q.asset
                 WHEN 'Asset_1' THEN pr.Asset_1
                 WHEN 'Asset_2' THEN pr.Asset_2
                 ELSE pr.Asset_3
               END) IS NOT NULL
          AND (CASE q.asset
                 WHEN 'Asset_1' THEN pr.Asset_1
                 WHEN 'Asset_2' THEN pr.Asset_2
                 ELSE pr.Asset_3
               END) > 0
        ORDER BY CAST(strftime('%s', pr.timestamp) AS INTEGER) DESC
        LIMIT 1
    ) AS p
    FROM query_params q
)
