-- Approach: join enrollments to students, courses and instructors, filter on the
-- exact course name, and order by student then instructor.
SELECT s.student_name AS student_name,
       i.instructor_name AS instructor_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
JOIN instructors i ON i.instructor_id = c.instructor_id
WHERE c.course_name = 'Database Systems'
ORDER BY s.student_name ASC, i.instructor_name ASC;
