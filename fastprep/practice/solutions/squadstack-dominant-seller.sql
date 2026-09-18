-- Per-seller revenue via LEFT JOIN, then keep sellers whose revenue exceeds all others combined.
SELECT seller_id,
       CASE WHEN total_revenue = CAST(total_revenue AS INTEGER)
            THEN CAST(total_revenue AS INTEGER)
            ELSE total_revenue END AS total_revenue
FROM (
    SELECT s.seller_id AS seller_id,
           COALESCE(SUM(o.item_qty * o.item_rate), 0) AS total_revenue
    FROM sellers s
    LEFT JOIN orders o ON o.seller_id = s.seller_id
    GROUP BY s.seller_id
) r
WHERE r.total_revenue * 2 > (
    SELECT COALESCE(SUM(o2.item_qty * o2.item_rate), 0) FROM orders o2
)
ORDER BY r.seller_id ASC
