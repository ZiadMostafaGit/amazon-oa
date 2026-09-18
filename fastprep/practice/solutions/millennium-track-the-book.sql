SELECT CASE
         WHEN t = CAST(t AS INTEGER) THEN CAST(CAST(t AS INTEGER) AS TEXT)
         ELSE RTRIM(RTRIM(printf('%.6f', t), '0'), '.')
       END AS pnl
FROM (
  SELECT ROUND(COALESCE(SUM(
           CASE WHEN f.client_side = 'BUY'
                THEN f.quantity * f.fill_price - f.quantity * c.mark_price
                ELSE f.quantity * c.mark_price - f.quantity * f.fill_price
           END), 0), 6) AS t
  FROM fills f
  JOIN closing_prices c ON c.asset = f.asset
)
