-- Solution: 01-window-basic

-- 1.
SELECT
    e.name, d.dept_name, e.salary,
    ROW_NUMBER()  OVER (PARTITION BY d.dept_name ORDER BY e.salary DESC) AS rn,
    RANK()        OVER (PARTITION BY d.dept_name ORDER BY e.salary DESC) AS rnk,
    DENSE_RANK()  OVER (PARTITION BY d.dept_name ORDER BY e.salary DESC) AS dense
FROM employees e
JOIN departments d USING (dept_id)
ORDER BY d.dept_name, e.salary DESC;

-- 2.
WITH ranked AS (
    SELECT *,
           DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS r
    FROM employees
)
SELECT e.name, d.dept_name, e.salary, r
FROM ranked r
JOIN departments d USING (dept_id)
WHERE r.r <= 2
ORDER BY d.dept_name, r.r;

-- 3.
SELECT
    server_id, collection_date, cpu_utilization,
    LAG(cpu_utilization) OVER w AS prev_cpu,
    cpu_utilization - LAG(cpu_utilization) OVER w AS delta,
    ROUND(100.0 * (cpu_utilization - LAG(cpu_utilization) OVER w) / NULLIF(LAG(cpu_utilization) OVER w, 0), 1) AS pct_change
FROM telemetry
WINDOW w AS (PARTITION BY server_id ORDER BY collection_date);

-- 4.
WITH lags AS (
    SELECT *,
           LAG(cpu_utilization,1) OVER w AS prev1,
           LAG(cpu_utilization,2) OVER w AS prev2
    FROM telemetry
    WINDOW w AS (PARTITION BY server_id ORDER BY collection_date)
)
SELECT server_id, collection_date, cpu_utilization, prev2, prev1
FROM lags
WHERE cpu_utilization > prev1 AND prev1 > prev2
ORDER BY server_id, collection_date;

-- 5.
SELECT
    server_id, collection_date, cpu_utilization,
    ROUND(AVG(cpu_utilization) OVER (PARTITION BY server_id ORDER BY collection_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW),1) AS roll_avg_7d,
    SUM(cpu_utilization) OVER (PARTITION BY server_id ORDER BY collection_date) AS running_total
FROM telemetry
ORDER BY server_id, collection_date;

-- 6.
WITH dept_avgs AS (
    SELECT
        name, dept_name, salary,
        ROUND(AVG(salary) OVER (PARTITION BY dept_id),0) AS dept_avg
    FROM employees e
    JOIN departments d USING (dept_id)
)
SELECT *, salary - dept_avg AS above_by
FROM dept_avgs
WHERE salary > dept_avg;

-- 7.
SELECT
    name, dept_name, salary,
    ROUND(PERCENT_RANK() OVER (PARTITION BY dept_id ORDER BY salary)::numeric, 2) AS pct_rank
FROM employees e
JOIN departments d USING (dept_id)
ORDER BY dept_name, pct_rank DESC;

-- 8.
SELECT
    name, salary,
    DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS dept_rank,
    LAG(salary) OVER (PARTITION BY dept_id ORDER BY hire_date) AS prev_salary_in_dept
FROM employees e
JOIN departments d USING (dept_id);

-- 9.
SELECT
    server_id, collection_date, cpu_utilization,
    SUM(cpu_utilization) OVER (PARTITION BY server_id ORDER BY collection_date) AS running_total
FROM telemetry
ORDER BY server_id, collection_date;

-- 10.
WITH crossed AS (
    SELECT
        server_id, collection_date, cpu_utilization,
        (cpu_utilization > 80 AND LAG(cpu_utilization, 1, 0.0) OVER (PARTITION BY server_id ORDER BY collection_date) <= 80) AS just_crossed
    FROM telemetry
)
SELECT * FROM crossed WHERE just_crossed = TRUE;
