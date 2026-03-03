-- =============================================================================
-- 06 — SCHEMA DESIGN — SOLUTIONS
-- =============================================================================

-- 2. SCD Type 2 update simulation
-- Step 1: Expire current record
UPDATE dim_server_scd
SET 
    expiry_date = '2026-01-31',
    is_current = FALSE
WHERE server_id = 'srv-01' AND is_current = TRUE;

-- Step 2: Insert new version
INSERT INTO dim_server_scd (
    server_key, server_id, region, tier, team, effective_date, is_current
)
SELECT 
    (SELECT MAX(server_key) + 1 FROM dim_server_scd),
    'srv-01', 'us-east', 'gold', 'Team Omega', '2026-02-01', TRUE;

-- 3. Point-in-time query (before change)
SELECT team
FROM dim_server_scd
WHERE server_id = 'srv-01'
  AND effective_date <= '2026-01-15'
  AND (expiry_date IS NULL OR expiry_date > '2026-01-15');
