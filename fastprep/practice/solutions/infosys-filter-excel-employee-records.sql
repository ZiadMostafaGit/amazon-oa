-- Case-sensitive filter on department/experience/active flag, projected and ordered by employee_id.
SELECT employee_id, employee_name, years_experience
FROM employees
WHERE department = 'Engineering'
  AND years_experience >= 3
  AND is_active
ORDER BY employee_id ASC;
