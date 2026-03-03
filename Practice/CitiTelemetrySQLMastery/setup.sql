-- =============================================
-- CITI TELEMETRY SQL MASTERY PROJECT - FULL SETUP (PostgreSQL Version)
-- Run once. Creates everything you need.
-- =============================================

-- 1. Base Tables
CREATE TABLE IF NOT EXISTS departments (
    dept_id   INTEGER PRIMARY KEY,
    dept_name VARCHAR
);
TRUNCATE TABLE departments CASCADE;
INSERT INTO departments VALUES
(1,'Engineering'),(2,'Marketing'),(3,'Finance');

CREATE TABLE IF NOT EXISTS employees (
    emp_id     INTEGER PRIMARY KEY,
    name       VARCHAR,
    dept_id    INTEGER,
    salary     DECIMAL(10,2),
    hire_date  DATE
);
TRUNCATE TABLE employees CASCADE;
INSERT INTO employees VALUES
(1,'Alice',1,120000,'2023-01-15'),(2,'Bob',1,120000,'2023-02-01'),
(3,'Charlie',1,110000,'2024-01-10'),(4,'Diana',1,95000,'2024-03-01'),
(5,'Eve',2,105000,'2023-05-20'),(6,'Frank',2,105000,'2023-06-15'),
(7,'Grace',2,88000,'2024-02-01'),(8,'Henry',3,115000,'2023-04-01'),
(9,'Ivy',3,115000,'2023-07-01'),(10,'Jack',3,92000,'2024-01-15');

CREATE TABLE IF NOT EXISTS employee_hierarchy (
    emp_id     INTEGER,
    manager_id INTEGER
);
TRUNCATE TABLE employee_hierarchy CASCADE;
INSERT INTO employee_hierarchy VALUES
(1,NULL),(2,1),(3,1),(4,2),(5,2),(6,4),(7,5),(8,5),(9,3),(10,3);

CREATE TABLE IF NOT EXISTS servers (
    server_id VARCHAR PRIMARY KEY,
    region    VARCHAR,
    tier      VARCHAR,
    team      VARCHAR
);
TRUNCATE TABLE servers CASCADE;
INSERT INTO servers VALUES
('srv-01','us-east','gold','Team Alpha'),('srv-02','us-east','silver','Team Alpha'),
('srv-03','us-west','gold','Team Beta'),('srv-04','us-west','bronze','Team Beta'),
('srv-05','us-east','silver','Team Gamma'),('srv-06','eu-west','gold','Team Delta');

-- SCD Type 2 Dimension (for schema design exercises)
CREATE TABLE IF NOT EXISTS dim_server_scd (
    server_key     INTEGER PRIMARY KEY,
    server_id      VARCHAR,
    region         VARCHAR,
    tier           VARCHAR,
    team           VARCHAR,
    effective_date DATE,
    expiry_date    DATE,
    is_current     BOOLEAN
);
TRUNCATE TABLE dim_server_scd CASCADE;
-- Initial load (2026-01-01)
INSERT INTO dim_server_scd VALUES
(1,'srv-01','us-east','gold','Team Alpha','2026-01-01',NULL,TRUE),
(2,'srv-02','us-east','silver','Team Alpha','2026-01-01',NULL,TRUE),
(3,'srv-03','us-west','gold','Team Beta','2026-01-01',NULL,TRUE);

-- Telemetry (rich time series - 6 servers × 14 days = 84 rows)
CREATE TABLE IF NOT EXISTS telemetry (
    server_id          VARCHAR,
    collection_date    DATE,
    cpu_utilization    DECIMAL(5,1),
    memory_utilization DECIMAL(5,1)
);
TRUNCATE TABLE telemetry CASCADE;

-- Full telemetry data (compact version - PostgreSQL)
WITH dates AS (
    SELECT d::DATE AS collection_date
    FROM generate_series(DATE '2026-01-01', DATE '2026-01-14', INTERVAL '1 day') AS s(d)
)
INSERT INTO telemetry
SELECT 
    s.server_id,
    d.collection_date,
    ROUND((40 + 50 * sin( (row_number() OVER (PARTITION BY s.server_id ORDER BY d.collection_date) -1) * 0.8 ) + random()*15)::numeric, 1) AS cpu,
    ROUND((50 + 30 * cos( (row_number() OVER (PARTITION BY s.server_id ORDER BY d.collection_date) -1) * 0.5 ) + random()*20)::numeric, 1) AS mem
FROM (VALUES ('srv-01'), ('srv-02'), ('srv-03'), ('srv-04'), ('srv-05'), ('srv-06')) AS s(server_id)
CROSS JOIN dates d;


-- User events for funnel & cohort
CREATE TABLE IF NOT EXISTS user_events (
    event_id   INTEGER,
    user_id    INTEGER,
    event_type VARCHAR,
    event_time TIMESTAMP
);
TRUNCATE TABLE user_events CASCADE;
INSERT INTO user_events VALUES
(1,101,'view','2026-01-05 10:00:00'),(2,101,'add_to_cart','2026-01-05 10:02:00'),
(3,101,'checkout','2026-01-05 10:05:00'),(4,101,'purchase','2026-01-05 10:07:00'),
(5,102,'view','2026-01-05 10:05:00'),(6,102,'add_to_cart','2026-01-05 10:07:20'),
(7,103,'view','2026-01-06 14:30:00'),
(8,104,'view','2026-01-06 15:10:00'),(9,104,'add_to_cart','2026-01-06 15:12:40'),
(10,105,'view','2026-01-07 11:22:00');

-- dim_date (for star schema)
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date AS
SELECT 
    EXTRACT(YEAR FROM d) * 10000 + EXTRACT(MONTH FROM d) * 100 + EXTRACT(DAY FROM d) AS date_key,
    d::DATE AS full_date,
    EXTRACT(YEAR FROM d) AS year,
    EXTRACT(MONTH FROM d) AS month,
    EXTRACT(QUARTER FROM d) AS quarter,
    EXTRACT(ISODOW FROM d) AS day_of_week,
    CASE WHEN EXTRACT(ISODOW FROM d) IN (6,7) THEN TRUE ELSE FALSE END AS is_weekend
FROM generate_series(DATE '2026-01-01', DATE '2026-02-28', INTERVAL '1 day') AS s(d);
