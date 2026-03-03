-- =============================================================================
-- 04 — COMPLEX JOINS — SOLUTIONS
-- =============================================================================

-- 1. Self-join: pairs with large CPU gap same day
SELECT 
    a.server_id AS s1,
    b.server_id AS s2,
    a.collection_date,
    a.cpu_utilization AS cpu1,
    b.cpu_utilization AS cpu2,
    ABS(a.cpu_utilization - b.cpu_utilization) AS gap
FROM telemetry a
JOIN telemetry b 
    ON a.collection_date = b.collection_date 
    AND a.server_id < b.server_id
JOIN servers sa ON a.server_id = sa.server_id
JOIN servers sb ON b.server_id = sb.server_id
WHERE sa.region = sb.region
  AND ABS(a.cpu_utilization - b.cpu_utilization) > 20
ORDER BY gap DESC;

-- 3. Anti-join (LEFT + IS NULL)
SELECT 
    s.server_id,
    s.region,
    '2026-01-10' AS missing_date
FROM servers s
LEFT JOIN telemetry t 
    ON s.server_id = t.server_id 
    AND t.collection_date = '2026-01-10'
WHERE t.server_id IS NULL;

-- 5. Cross join → find gaps
WITH all_combos AS (
    SELECT 
        s.server_id,
        d.full_date AS collection_date
    FROM servers s
    CROSS JOIN (SELECT full_date FROM dim_date WHERE year = 2026 AND month = 1) d
)
SELECT 
    ac.server_id,
    ac.collection_date
FROM all_combos ac
LEFT JOIN telemetry t 
    ON ac.server_id = t.server_id 
    AND ac.collection_date = t.collection_date
WHERE t.server_id IS NULL
ORDER BY ac.collection_date, ac.server_id;
