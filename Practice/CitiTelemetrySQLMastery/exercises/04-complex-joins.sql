-- =============================================================================
-- 04 — COMPLEX JOINS (self, anti, cross)
-- Goal: self-joins for deltas & pairs, anti-joins for gaps, cross for completeness
-- =============================================================================

-- Ex 1. Self-join: find server pairs in same region with CPU difference > 20 on same date

-- Ex 2. Self-join for day-over-day delta (alternative to LAG)
-- Join on server_id and date = previous date

-- Ex 3. Anti-join (LEFT JOIN + IS NULL): servers missing data on 2026-01-10

-- Ex 4. Same as Ex 3 but using NOT EXISTS

-- Ex 5. Cross join: generate all server × date combinations for Jan 2026
-- Then LEFT JOIN telemetry to find missing rows (gaps)

-- Ex 6. Gap detection + last seen date
-- For each server, show dates with no data + most recent date with data

-- Ex 7 (challenge). Self-join + window: compare each server's CPU to the average of other servers in same region on same day
