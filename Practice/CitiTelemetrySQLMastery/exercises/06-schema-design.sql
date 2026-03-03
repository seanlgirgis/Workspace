-- =============================================================================
-- 06 — SCHEMA DESIGN (Star, SCD Type 2, Grain)
-- =============================================================================

-- Ex 1. Create a basic star schema fact table
-- fact_cpu_daily (server_key, date_key, avg_cpu) referencing dim_server_scd and dim_date

-- Ex 2. SCD Type 2 update simulation
-- Move srv-01 from Team Alpha to Team Omega on 2026-02-01
-- Close old record, insert new one

-- Ex 3. Point-in-time query: which team owned srv-01 on 2026-01-15?

-- Ex 4. Point-in-time query: which team owned srv-01 on 2026-02-05? (after change)

-- Ex 5. Compare current-state (SCD Type 1 style) vs historical (Type 2) query results

-- Ex 6 (challenge). ETL-style CTE: transform telemetry into star schema fact table
-- Aggregate to daily, join surrogate keys
