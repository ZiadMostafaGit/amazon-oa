-- Dense-rank distinct salaries per department, keep rank 5.
SELECT department_id, salary AS fifth_highest_salary
FROM (
  SELECT DISTINCT department_id,
         salary,
         DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS dr
  FROM employees
)
WHERE dr = 5
ORDER BY department_id ASC;
