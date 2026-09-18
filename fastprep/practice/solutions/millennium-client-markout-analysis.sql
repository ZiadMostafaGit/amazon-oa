-- Aggregate signed desk markout per client and flag a negative unweighted mean.
SELECT client_id,
       COUNT(*) AS trade_count,
       AVG(CASE WHEN side = 'BUY' THEN fill_price - future_mid_price
                ELSE future_mid_price - fill_price END) AS mean_markout,
       CASE WHEN AVG(CASE WHEN side = 'BUY' THEN fill_price - future_mid_price
                          ELSE future_mid_price - fill_price END) < 0
            THEN 'True' ELSE 'False' END AS is_invalid
FROM trades
GROUP BY client_id
ORDER BY client_id ASC
