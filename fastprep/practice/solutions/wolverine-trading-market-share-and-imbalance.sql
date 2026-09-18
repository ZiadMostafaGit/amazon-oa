-- Aggregate exchange and participant quantities per product, rank by market-share ratio, report imbalance.
WITH exchange_totals AS (
    SELECT s.product AS product, SUM(m.quantity) AS eq
    FROM market_trades m
    JOIN symbology s ON s.product_id = m.product_id
    GROUP BY s.product
),
participant_totals AS (
    SELECT product AS product,
           SUM(quantity) AS pq,
           SUM(CASE WHEN side = 'B' THEN quantity ELSE -quantity END) AS imbalance
    FROM participant_trades
    GROUP BY product
)
SELECT p.product AS product, p.imbalance AS imbalance
FROM participant_totals p
JOIN exchange_totals e ON e.product = p.product
ORDER BY (p.pq * 1.0) / e.eq DESC, p.product ASC
LIMIT 1
