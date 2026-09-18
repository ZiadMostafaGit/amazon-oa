-- Group by email and keep groups with more than one row.
SELECT email
FROM employees
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email ASC;
