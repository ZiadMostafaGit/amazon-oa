-- Label each node by whether it has a parent and whether any row names it as a parent.
SELECT n.id AS id,
       CASE
           WHEN n.pid IS NULL THEN 'Root'
           WHEN EXISTS (SELECT 1 FROM tree_nodes c WHERE c.pid = n.id) THEN 'Inner'
           ELSE 'Leaf'
       END AS node_type
FROM tree_nodes n
ORDER BY n.id ASC;
