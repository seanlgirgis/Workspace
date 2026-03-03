-- =============================================================================
-- 02 — CTEs — SOLUTIONS
-- =============================================================================

-- 1. Above-average earners using CTE
WITH dept_avg AS (
    SELECT 
        dept_id,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY dept_id
)
SELECT 
    e.name,
    d.dept_name,
    e.salary,
    ROUND(da.avg_salary, 0) AS dept_avg,
    ROUND(e.salary - da.avg_salary, 0) AS above_by
FROM employees e
JOIN departments d USING (dept_id)
JOIN dept_avg da USING (dept_id)
WHERE e.salary > da.avg_salary
ORDER BY d.dept_name, above_by DESC;

-- 2. Simple raw → daily average pipeline
WITH daily AS (
    SELECT 
        server_id,
        collection_date,
        ROUND(AVG(cpu_utilization), 1) AS avg_cpu
    FROM telemetry
    GROUP BY server_id, collection_date
)
SELECT * 
FROM daily 
WHERE server_id = 'srv-01'
ORDER BY collection_date;

-- 3. 4-step pipeline example (raw → daily → rolling → status)
WITH 
raw_filtered AS (
    SELECT * FROM telemetry
    -- could add WHERE collection_date >= '2026-01-01' etc.
),
daily AS (
    SELECT 
        server_id,
        collection_date,
        ROUND(AVG(cpu_utilization), 1) AS avg_cpu
    FROM raw_filtered
    GROUP BY server_id, collection_date
),
rolling AS (
    SELECT 
        *,
        ROUND(MAX(avg_cpu) OVER (
            PARTITION BY server_id 
            ORDER BY collection_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 1) AS roll_max_7d
    FROM daily
)
SELECT 
    server_id,
    collection_date,
    roll_max_7d,
    CASE 
        WHEN roll_max_7d > 85 THEN 'HIGH'
        WHEN roll_max_7d > 70 THEN 'MEDIUM'
        ELSE 'OK'
    END AS status
FROM rolling
WHERE server_id = 'srv-03'
ORDER BY collection_date;


-- 4. Recursive org chart (PostgreSQL compatible)
WITH RECURSIVE org AS (
    -- Anchor: CEO
    SELECT 
        e.emp_id,
        e.name,
        NULL::INTEGER AS manager_id,
        e.name AS path,
        1 AS level
    FROM employees e
    JOIN employee_hierarchy h ON e.emp_id = h.emp_id
    WHERE h.manager_id IS NULL

    UNION ALL

    -- Recursive part
    SELECT 
        e.emp_id,
        e.name,
        h.manager_id,
        org.path || ' → ' || e.name AS path,
        org.level + 1
    FROM employees e
    JOIN employee_hierarchy h ON e.emp_id = h.emp_id
    JOIN org ON h.manager_id = org.emp_id
)
SELECT 
    lpad('', (level-1)*4) || name AS org_tree,
    level,
    path
FROM org
ORDER BY path;


-- 5. Employees who are managers
WITH managers AS (
    SELECT DISTINCT manager_id 
    FROM employee_hierarchy 
    WHERE manager_id IS NOT NULL
)
SELECT e.name, d.dept_name
FROM employees e
JOIN departments d USING (dept_id)
WHERE e.emp_id IN (SELECT manager_id FROM managers)
ORDER BY e.name;

-- 6.
WITH dept_stats AS (
    SELECT dept_id, ROUND(AVG(salary), 2) AS dept_avg FROM employees GROUP BY dept_id
)
SELECT 
    name, dept_id, salary, dept_avg,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank
FROM employees
JOIN dept_stats USING (dept_id);
