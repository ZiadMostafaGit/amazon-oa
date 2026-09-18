-- One COUNT(*)-COUNT(col) per column, unioned and re-ordered by schema position.
SELECT column_name, null_count
FROM (
    SELECT 1 AS ord, 'record_id' AS column_name, COUNT(*) - COUNT(record_id) AS null_count FROM records
    UNION ALL
    SELECT 2, 'name', COUNT(*) - COUNT(name) FROM records
    UNION ALL
    SELECT 3, 'email', COUNT(*) - COUNT(email) FROM records
    UNION ALL
    SELECT 4, 'score', COUNT(*) - COUNT(score) FROM records
)
ORDER BY ord;
