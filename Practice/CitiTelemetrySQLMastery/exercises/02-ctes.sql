-- =============================================================================
-- 02 — COMMON TABLE EXPRESSIONS (CTEs)
-- Goal: master readability, chaining, recursive CTEs, testing intermediate steps
-- =============================================================================

-- Ex 1. Above-average earners using a named CTE
-- Return: name, dept_name, salary, dept_avg, difference
-- Use CTE instead of correlated subquery or inline window

-- Ex 2. Simple multi-step pipeline: raw telemetry → daily average per server
-- CTEs: raw → daily_avg
-- Final: show server_id, date, avg_cpu for srv-01 only

-- Ex 3. 4-step capacity-like pipeline
-- raw → daily_avg → 7d_rolling_max → status ('HIGH' if rolling_max > 85, else 'OK')
-- Return: server_id, date, rolling_max, status

-- Ex 4. Recursive CTE: full organization chart from CEO
-- Columns: name, manager_name, level, path (e.g. "CEO > CTO > Senior DE")
-- Use indentation or numbered levels

-- Ex 5. Find all employees who are managers (have at least one direct report)
-- Use CTE + EXISTS or recursive or GROUP BY

-- Ex 6. Chained CTEs: compute dept_avg_salary, then rank employees within dept
-- Final SELECT: name, dept, salary, dept_avg, dept_rank (using DENSE_RANK)

-- Ex 7. Test any intermediate step in isolation
-- Example: after writing the pipeline in Ex 3, add SELECT * FROM rolling_max LIMIT 10;

-- Ex 8 (challenge). Recursive CTE + window function
-- Show hierarchy level + salary rank within each manager's subtree

-- Ex 9 (challenge). Prevent infinite recursion in org chart
-- Add depth limit (WHERE level < 10) and explain why it's needed
