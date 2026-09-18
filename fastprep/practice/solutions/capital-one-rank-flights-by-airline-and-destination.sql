-- Window COUNT(*) per airline and per airline+destination drives the multi-key ordering.
SELECT id, destination, departure_time
FROM (
  SELECT
    id,
    aviacompany,
    destination,
    departure_time,
    COUNT(*) OVER (PARTITION BY aviacompany) AS airline_total,
    COUNT(*) OVER (PARTITION BY aviacompany, destination) AS dest_total
  FROM flights
)
ORDER BY
  airline_total DESC,
  aviacompany ASC,
  dest_total DESC,
  destination ASC,
  departure_time ASC,
  id ASC;
