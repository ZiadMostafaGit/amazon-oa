-- Left join each trade to its optional hedge, treating a NULL or missing hedge PnL as 0
SELECT t.trade_id AS Trade_id
FROM wolve_trades AS t
LEFT JOIN wolve_hedges AS h ON h.trade_id = t.trade_id
WHERE COALESCE(h.hedge_pnl, 0) > t.trade_pnl
