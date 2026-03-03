-- =============================================================================
-- 05 — ANALYTICAL SQL PATTERNS (YoY, Cohort, Funnel, Rolling)
-- =============================================================================

-- Ex 1. Simulate YoY growth (duplicate 2025 data or use LAG 365 days)
-- Show month, cpu_avg, prev_year_avg, yoy_pct

-- Ex 2. Cohort analysis on servers (provision month → still "active" after 30 days)
-- Note: use hire_date as proxy for "provisioned", assume still active if no "decommission"

-- Ex 3. Funnel analysis on user_events
-- % of users who go view → add_to_cart → checkout → purchase

-- Ex 4. 7-day rolling average CPU per server (last 3 days of data)

-- Ex 5. Month-over-month change in average CPU per region

-- Ex 6. Top-3 highest CPU days per server (use DENSE_RANK)

-- Ex 7 (challenge). Retention-style cohort: % of users who completed purchase within 7 days of first view

-- Ex 8 (challenge). First purchase time per user using window MIN
