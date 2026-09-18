-- Left join profiles to relations and aggregate counts with conditional SUM.
SELECT
  p.last_name || ' ' || p.first_name AS full_name,
  p.email AS email,
  COUNT(r.profile_id) AS total_relations,
  COALESCE(SUM(CASE WHEN r.is_approved THEN 1 ELSE 0 END), 0) AS approved_relations,
  COALESCE(SUM(CASE WHEN r.profile_id IS NOT NULL AND NOT r.is_approved THEN 1 ELSE 0 END), 0) AS pending_relations
FROM profiles p
LEFT JOIN relations r ON r.profile_id = p.id
GROUP BY p.id, p.last_name, p.first_name, p.email
ORDER BY full_name ASC, p.email ASC
