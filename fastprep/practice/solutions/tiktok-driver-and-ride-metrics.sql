-- Three scalar aggregates stacked with UNION ALL over drivers and the four ride partitions, ordered by task.
SELECT insight_type, value
FROM (
    SELECT 1 AS ord,
           'average_driver_rating' AS insight_type,
           (SELECT AVG(rating) FROM drivers) AS value
    UNION ALL
    SELECT 2,
           'percentage_drivers_with_second_language',
           (SELECT 100.0 * SUM(CASE WHEN second_language <> 'no' THEN 1 ELSE 0 END) / COUNT(*) FROM drivers)
    UNION ALL
    SELECT 3,
           'ride_success_rate',
           (SELECT 100.0 * SUM(CASE WHEN status = 'Success' THEN 1 ELSE 0 END) / COUNT(*)
            FROM (
                SELECT status FROM rides_1
                UNION ALL SELECT status FROM rides_2
                UNION ALL SELECT status FROM rides_3
                UNION ALL SELECT status FROM rides_4
            ))
)
ORDER BY ord
