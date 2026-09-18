SELECT CASE
         WHEN valid_count = 0 THEN '0.00'
         ELSE printf('%d.%02d',
                     ((20000 * true_count + valid_count) / (2 * valid_count)) / 100,
                     ((20000 * true_count + valid_count) / (2 * valid_count)) % 100)
       END AS success_rate
  FROM (SELECT SUM(CASE WHEN LOWER(TRIM(result_value)) IN ('true', 'false') THEN 1 ELSE 0 END) AS valid_count,
               SUM(CASE WHEN LOWER(TRIM(result_value)) = 'true' THEN 1 ELSE 0 END) AS true_count
          FROM test_results)
