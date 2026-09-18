-- Keep employees whose salary equals their department's max salary.
SELECT e.department_id, e.employee_id, e.employee_name, e.salary
FROM employees AS e
WHERE e.salary = (
  SELECT MAX(x.salary) FROM employees AS x WHERE x.department_id = e.department_id
)
ORDER BY e.department_id ASC, e.employee_id ASC;
