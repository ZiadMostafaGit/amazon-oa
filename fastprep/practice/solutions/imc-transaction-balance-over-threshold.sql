-- Aggregate transactions per account and join to logins, keeping net balance > 10000.
SELECT l.USERNAME AS USERNAME
FROM LOGIN l
JOIN TRANSACT t ON t.ACCOUNT = l.ACCOUNT
GROUP BY l.ACCOUNT, l.USERNAME
HAVING SUM(t.AMOUNT) > 10000
