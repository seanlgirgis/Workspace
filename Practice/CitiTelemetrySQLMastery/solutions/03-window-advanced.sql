-- =============================================================================
-- 03 — ADVANCED WINDOW FUNCTIONS — SOLUTIONS
-- =============================================================================

-- 1. NTILE quartiles by average CPU
WITH server_avg AS (
    SELECT 
        server_id,
        ROUND(AVG(cpu_utilization), 1) AS avg_cpu
    FROM telemetry
    GROUP BY server_id
)
SELECT 
    server_id,
    avg_cpu,
    NTILE(4) OVER (ORDER BY avg_cpu DESC) AS quartile
FROM server_avg
ORDER BY avg_cpu DESC;

-- 2. PERCENT_RANK vs CUME_DIST
SELECT 
    server_id,
    collection_date,
    cpu_utilization,
    ROUND(PERCENT_RANK() OVER (ORDER BY cpu_utilization)::numeric, 3) AS percent_rank,
    ROUND(CUME_DIST()     OVER (ORDER BY cpu_utilization)::numeric, 3) AS cume_dist
FROM telemetry
ORDER BY cpu_utilization DESC
LIMIT 20;

-- 3. Delta from first day (baseline)
SELECT 
    server_id,
    collection_date,
    cpu_utilization,
    FIRST_VALUE(cpu_utilization) OVER (
        PARTITION BY server_id 
        ORDER BY collection_date
    ) AS first_day_cpu,
    cpu_utilization - FIRST_VALUE(cpu_utilization) OVER (
        PARTITION BY server_id 
        ORDER BY collection_date
    ) AS delta_from_start
FROM telemetry
ORDER BY server_id, collection_date;

-- 4. Correct LAST_VALUE (whole partition)
SELECT 
    server_id,
    collection_date,
    cpu_utilization,
    LAST_VALUE(cpu_utilization) OVER (
        PARTITION BY server_id 
        ORDER BY collection_date
        ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING
    ) AS last_day_cpu
FROM telemetry
ORDER BY server_id, collection_date;

-- 5. Named WINDOW clause example
SELECT 
    server_id,
    collection_date,
    cpu_utilization,
    ROUND(AVG(cpu_utilization) OVER w, 1) AS roll_3d_avg,
    ROUND(MAX(cpu_utilization) OVER w, 1) AS roll_3d_max,
    ROUND(MIN(cpu_utilization) OVER w, 1) AS roll_3d_min
FROM telemetry
WINDOW w AS (
    PARTITION BY server_id 
    ORDER BY collection_date 
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
WHERE server_id = 'srv-01'
ORDER BY collection_date;
