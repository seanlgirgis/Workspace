-- =============================================================================
-- 01 — WINDOW FUNCTIONS — BASIC
-- Run each block separately in PostgreSQL
-- Goal: master ROW_NUMBER, RANK, DENSE_RANK, LAG/LEAD, rolling aggregates
-- =============================================================================

-- Exercise 1 ── All three ranking functions side-by-side
-- Show name, dept, salary, row_number, rank, dense_rank per department
-- Expected: Alice & Bob both dense_rank=1, rank=1, but row_number different

-- Exercise 2 ── Top-2 earners per department (use DENSE_RANK + CTE)
-- Return name, dept_name, salary, rank — only rank <= 2

-- Exercise 3 ── Day-over-day CPU delta + percentage change
-- Columns: server_id, date, cpu, prev_cpu, delta, pct_change
-- Hint: LAG + (current - prev)/prev * 100

-- Exercise 4 ── Servers with continuous 3-day upward CPU trend
-- (today > yesterday AND yesterday > day-before-yesterday)
-- Return server_id, date, cpu, prev1, prev2

-- Exercise 5 ── 7-day rolling average & running total CPU per server
-- Use ROWS BETWEEN 6 PRECEDING AND CURRENT ROW

-- Exercise 6 ── Employees earning above their department average
-- No subquery — use window AVG() + CTE or inline

-- Exercise 7 ── Salary percentile rank within department (PERCENT_RANK)
-- 0 = lowest, 1 = highest in dept

-- Exercise 8 ── Combine: rank + previous salary in same dept
-- Show name, salary, dept_rank (dense), prev_salary_in_dept (ordered by hire_date)

-- Exercise 9 ── Running total CPU hours per server (cumulative sum)
-- Reset per server, ordered by date

-- Exercise 10 (challenge) ── Detect first time CPU crossed 80% per server
-- Use window + conditional logic or LEAD
