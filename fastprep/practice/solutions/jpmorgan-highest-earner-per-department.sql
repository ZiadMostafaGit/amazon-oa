-- Join each employee against the per-department maximum salary to keep every tied top earner.
SELECT e.department_id, e.employee_id, e.employee_name, e.salary
FROM employees AS e
JOIN (
    SELECT department_id, MAX(salary) AS max_salary
    FROM employees
    GROUP BY department_id
) AS m
  ON m.department_id = e.department_id AND e.salary = m.max_salary
ORDER BY e.department_id ASC, e.employee_id ASC;
