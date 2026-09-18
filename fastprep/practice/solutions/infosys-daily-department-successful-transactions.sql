-- Cross join every distinct transaction date with every products department, left join successful rows and count.
SELECT d.transaction_date AS transaction_date,
       p.dept_id AS department_id,
       COUNT(t.status) AS successful_count
FROM (SELECT DISTINCT transaction_date FROM transactions) AS d
CROSS JOIN (SELECT DISTINCT dept_id FROM products) AS p
LEFT JOIN transactions AS t
       ON t.transaction_date = d.transaction_date
      AND t.dept_id = p.dept_id
      AND t.status = 'successful'
GROUP BY d.transaction_date, p.dept_id
ORDER BY d.transaction_date ASC, p.dept_id ASC
