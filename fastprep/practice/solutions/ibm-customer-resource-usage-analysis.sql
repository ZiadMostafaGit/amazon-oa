SELECT
    email                                                   AS email,
    printf('%d.%02d', (2 * cpu_cents + n) / (2 * n) / 100,
                      (2 * cpu_cents + n) / (2 * n) % 100)  AS average_cpu_usage,
    printf('%d.%02d', (2 * mem_cents + n) / (2 * n) / 100,
                      (2 * mem_cents + n) / (2 * n) % 100)  AS average_memory_usage,
    printf('%d.%02d', (2 * disk_cents + n) / (2 * n) / 100,
                      (2 * disk_cents + n) / (2 * n) % 100) AS average_disk_usage
FROM (
    SELECT
        c.email                                               AS email,
        COUNT(*)                                              AS n,
        SUM(CAST(ROUND(m.cpu_usage * 100) AS INTEGER))        AS cpu_cents,
        SUM(CAST(ROUND(m.memory_usage * 100) AS INTEGER))     AS mem_cents,
        SUM(CAST(ROUND(m.disk_usage * 100) AS INTEGER))       AS disk_cents
    FROM customers AS c
    JOIN site_metrics AS m ON m.customer_id = c.id
    GROUP BY c.id, c.email
)
WHERE cpu_cents > 5000 * n
   OR mem_cents > 5000 * n
   OR disk_cents > 5000 * n
ORDER BY email ASC
