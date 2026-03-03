-- =============================================================================
-- 03 — ADVANCED WINDOW FUNCTIONS
-- Goal: NTILE, PERCENT_RANK, FIRST/LAST_VALUE, named WINDOW clauses
-- =============================================================================

-- Ex 1. NTILE(4) quartile ranking of servers by average CPU (whole period)
-- Return: server_id, avg_cpu, quartile (1 = highest usage)

-- Ex 2. PERCENT_RANK and CUME_DIST on overall CPU utilization
-- Show how they differ on the same data (telemetry table)

-- Ex 3. Delta from first day of period (baseline comparison)
-- Use FIRST_VALUE(cpu) OVER (PARTITION BY server_id ORDER BY date)
-- Return: server_id, date, cpu, baseline, delta

-- Ex 4. Correct usage of LAST_VALUE
-- Show last value of the entire partition (not current row!)
-- Hint: ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING

-- Ex 5. Named WINDOW clause – DRY rolling stats
-- Define WINDOW w AS (PARTITION BY server_id ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)
-- Compute rolling 3-day avg, min, max using the same window

-- Ex 6. Combine NTILE + rolling average
-- Servers in top quartile (NTILE=1) with their 7-day rolling avg on the last day

-- Ex 7 (challenge). FIRST_VALUE as dynamic baseline per month
-- For each month, show delta from the first day of that month

-- Ex 8 (challenge). Use named window + PERCENT_RANK in one query
-- Rank servers by rolling 7-day max CPU, show percentile
