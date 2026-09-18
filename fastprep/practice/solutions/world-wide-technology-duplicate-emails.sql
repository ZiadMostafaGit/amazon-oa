-- Group by email and keep groups whose row count exceeds one.
SELECT email
FROM contacts
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY email ASC;
