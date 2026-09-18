SELECT COALESCE(
         (SELECT t.transaction_id
            FROM transactions t
           WHERE EXISTS (SELECT 1
                           FROM transactions p
                          WHERE p.transaction_id = t.transaction_id
                            AND p.sequence_no < t.sequence_no
                            AND t.transaction_minute - p.transaction_minute <= 10)
           ORDER BY t.sequence_no
           LIMIT 1),
         'NONE') AS transaction_id
