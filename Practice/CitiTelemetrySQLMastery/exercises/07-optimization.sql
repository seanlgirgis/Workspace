-- =============================================================================
-- 07 — QUERY OPTIMIZATION & EXPLAIN
-- Goal: understand plans, indexes, join strategies
-- =============================================================================

-- Ex 1. Run EXPLAIN on a full table scan query
-- SELECT * FROM telemetry WHERE collection_date = '2026-01-10'

-- Ex 2. Add index on (server_id, collection_date) and re-run EXPLAIN

-- Ex 3. Compare plan before/after index on a range query (last 7 days)

-- Ex 4. Force join order or join type (PostgreSQL: disable seqscan or hashjoin via SET enable_hashjoin=off)

-- Ex 5 (challenge). Optimize the 4-step pipeline from 02-ctes Ex 3
-- Add indexes, check if plan changes from seq scan → index scan
