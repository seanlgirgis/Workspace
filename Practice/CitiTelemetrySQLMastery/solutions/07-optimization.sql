-- =============================================================================
-- 07 — OPTIMIZATION — SOLUTIONS
-- =============================================================================

-- 1. Before index — expect Seq Scan
EXPLAIN ANALYZE
SELECT * FROM telemetry 
WHERE collection_date = '2026-01-10';

-- 2. Create composite index
CREATE INDEX idx_telemetry_server_date 
ON telemetry (server_id, collection_date);

-- Re-run same query — should now show Index Scan
EXPLAIN ANALYZE
SELECT * FROM telemetry 
WHERE collection_date = '2026-01-10';

-- 3. Range query benefit
EXPLAIN ANALYZE
SELECT server_id, AVG(cpu_utilization)
FROM telemetry
WHERE collection_date >= '2026-01-08'
GROUP BY server_id;
