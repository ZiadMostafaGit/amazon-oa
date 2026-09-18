SELECT department,
       user_id
  FROM (SELECT department,
               user_id,
               MIN(log_position) OVER (PARTITION BY department) AS dept_first,
               ROW_NUMBER() OVER (PARTITION BY department
                                  ORDER BY last_seen DESC, log_position ASC) AS rn
          FROM activity_logs)
 WHERE rn = 1
 ORDER BY dept_first
