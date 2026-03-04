import pandas as pd
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

db_pass = "mysecretpassword"
conn_str = f"postgresql://postgres:{quote_plus(db_pass)}@localhost:5432/practice_db"
engine = create_engine(conn_str)

def run_sql(query, name):
    print(f"\n--- Running: {name} ---")
    try:
        with engine.connect() as conn:
            # For setup_sql (which drops/creates table), we need transaction commit for SQLAlchemy 2.0
            if "CREATE TABLE" in query.upper() or "DROP TABLE" in query.upper():
                conn.execute(text(query))
                conn.commit()
                print("DDL Executed successfully.")
            else:
                result = conn.execute(text(query))
                df = pd.DataFrame(result.mappings())
                print(df.head(2))
    except Exception as e:
        print(f"ERROR:\n{e}")

setup_sql = """
DROP TABLE IF EXISTS daily_metrics;

CREATE TABLE daily_metrics AS 
SELECT * FROM (
    VALUES 
    ('SRV-01', '2026-02-01'::DATE, 100),
    ('SRV-01', '2026-02-02'::DATE, 105),
    ('SRV-01', '2026-02-03'::DATE, 98),
    ('SRV-01', '2026-02-04'::DATE, 102),
    ('SRV-01', '2026-02-06'::DATE, 101),
    ('SRV-01', '2026-02-07'::DATE, 99),
    ('SRV-01', '2026-02-11'::DATE, 110),
    ('SRV-01', '2026-02-12'::DATE, 112),
    ('SRV-01', '2026-02-13'::DATE, 108),
    ('SRV-01', '2026-02-14'::DATE, 109),
    ('SRV-02', '2026-02-01'::DATE, 50),
    ('SRV-02', '2026-02-02'::DATE, 52),
    ('SRV-02', '2026-02-05'::DATE, 55),
    ('SRV-02', '2026-02-06'::DATE, 51)
) AS t(server_id, report_date, cpu_usage);
"""
run_sql(setup_sql, "c03 Setup")

q4 = """
SELECT 
    server_id,
    report_date,
    EXTRACT('dow' FROM report_date) AS day_of_week,
    DATE_TRUNC('week', report_date)::DATE AS week_start,
    DATE_TRUNC('month', report_date)::DATE AS month_start
FROM daily_metrics
WHERE EXTRACT('dow' FROM report_date) NOT IN (0, 6)
ORDER BY server_id, report_date
LIMIT 5;
"""
run_sql(q4, "c04 Pattern 1")

q5 = """
WITH numbered AS (
    SELECT
        server_id,
        report_date,
        ROW_NUMBER() OVER (PARTITION BY server_id ORDER BY report_date) AS rn,
        report_date - CAST(ROW_NUMBER() OVER (
            PARTITION BY server_id ORDER BY report_date
        ) AS INT) AS island_key
    FROM daily_metrics
),
islands AS (
    SELECT
        server_id,
        island_key,
        MIN(report_date) AS island_start,
        MAX(report_date) AS island_end,
        COUNT(*) AS consecutive_days
    FROM numbered
    GROUP BY server_id, island_key
)
SELECT server_id, island_start, island_end, consecutive_days
FROM islands
ORDER BY server_id, island_start;
"""
run_sql(q5, "c05 Gaps and Islands")

q7 = """
WITH all_dates AS (
    SELECT UNNEST(generate_series(
        '2026-02-01'::DATE,
        '2026-02-14'::DATE,
        INTERVAL '1 day'
    ))::DATE AS expected_date
)
SELECT * FROM all_dates LIMIT 2;
"""
run_sql(q7, "c07 Generate Series with UNNEST")

q7b = """
WITH all_dates AS (
    SELECT generate_series(
        '2026-02-01'::DATE,
        '2026-02-14'::DATE,
        INTERVAL '1 day'
    )::DATE AS expected_date
)
SELECT * FROM all_dates LIMIT 2;
"""
run_sql(q7b, "c07 Generate Series WITHOUT UNNEST")
