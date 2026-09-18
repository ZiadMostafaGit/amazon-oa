-- Filter rows against a scalar subquery holding the overall average salary.
SELECT employee_id, employee_name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees)
ORDER BY salary DESC, employee_id ASC;
