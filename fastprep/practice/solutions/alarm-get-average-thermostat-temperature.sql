SELECT room_name,
       ROUND(AVG(temperature)) AS average_temperature
FROM devices
WHERE device_type = 'Thermostat'
GROUP BY room_name
HAVING COUNT(*) > 2
ORDER BY room_name DESC
