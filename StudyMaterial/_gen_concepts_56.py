"""
Concept notebook generator for Days 5 and 6.
Topics: Analytical SQL, ETL Patterns, Capacity Planning, Schema Design, PySpark, System Design.
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/Workspace/StudyMaterial'


def nb(cells_list):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "cells": cells_list
    }

def md(cell_id, content):
    lines = content.split('\n')
    source = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source}

def code(cell_id, content):
    lines = content.split('\n')
    source = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    return {"cell_type": "code", "id": cell_id, "metadata": {}, "outputs": [], "execution_count": None, "source": source}

def write_nb(path, cells_list):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb(cells_list), f, indent=1, ensure_ascii=False)
    print(f'  Written: {path}')


# ─────────────────────────────────────────────────────────────────────────────
# DAY 5-B: Analytical SQL — YoY Growth, Cohort Analysis, Funnel
# ─────────────────────────────────────────────────────────────────────────────

SQL_ANALYTICAL = [
md('c01', '''# SQL — Analytical SQL: YoY Growth, Cohort Analysis, Funnel
---

<div style="padding:15px;border-left:8px solid #fa709a;background:#fff0f5;border-radius:4px;">
<strong>Core Insight:</strong> Analytical SQL separates analysts from engineers.
YoY, cohort, and funnel queries appear in every data engineering interview.
Master these three patterns and you can answer 80% of business intelligence questions
with SQL alone — no Python required.
</div>

### Why It Matters
At Citi, cohort analysis tracked server cohorts by provisioning quarter:
*"Of servers provisioned in Q1 2024, how many are still active in Q4 2025?"*
The same pattern used for user retention analysis works for infrastructure lifecycle.'''),

md('c02', '''## 🧠 Three Analytical Patterns

| Pattern | Business Question | SQL Technique |
|---------|-----------------|---------------|
| **YoY Growth** | "Revenue this month vs same month last year?" | `LAG(value, 12)` or self-join on `YEAR()` |
| **Cohort Analysis** | "Of users who joined in Jan, how many are still active 3 months later?" | `FIRST_VALUE()` + date arithmetic + GROUP BY cohort |
| **Funnel Analysis** | "How many users completed each step of checkout?" | Conditional aggregation with `COUNT(CASE WHEN...)` |

### The Window Function Toolkit
```sql
-- Running total
SUM(revenue) OVER (ORDER BY date)

-- Row-by-row comparison (YoY needs LAG of 12 months)
LAG(value, 1) OVER (PARTITION BY server_id ORDER BY month)

-- Rank within a group
RANK() OVER (PARTITION BY category ORDER BY value DESC)

-- First value in a group (cohort anchor)
FIRST_VALUE(date) OVER (PARTITION BY user_id ORDER BY date)
```'''),

code('c03', '''-- Pattern 1: Year-over-Year Growth
-- Given: monthly revenue table with (year, month, revenue)
-- Question: Show each month with revenue, prior year revenue, and YoY growth %

-- Setup (simulate with values)
WITH monthly_revenue AS (
    SELECT 2024 AS yr, 1 AS mo, 1200000 AS revenue UNION ALL
    SELECT 2024, 2, 1350000 UNION ALL
    SELECT 2024, 3, 1280000 UNION ALL
    SELECT 2023, 1, 980000 UNION ALL
    SELECT 2023, 2, 1050000 UNION ALL
    SELECT 2023, 3, 1100000
),
-- Method 1: Self-join
yoy_self_join AS (
    SELECT
        curr.yr,
        curr.mo,
        curr.revenue AS curr_revenue,
        prev.revenue AS prev_revenue,
        ROUND((curr.revenue - prev.revenue) * 100.0 / prev.revenue, 1) AS yoy_pct
    FROM monthly_revenue curr
    LEFT JOIN monthly_revenue prev
        ON curr.yr = prev.yr + 1
        AND curr.mo = prev.mo
),
-- Method 2: LAG window function (cleaner)
yoy_lag AS (
    SELECT
        yr, mo, revenue,
        LAG(revenue, 12) OVER (ORDER BY yr, mo) AS prev_year_revenue
    FROM monthly_revenue
)
SELECT
    yr, mo, revenue,
    prev_year_revenue,
    ROUND((revenue - prev_year_revenue) * 100.0 / prev_year_revenue, 1) AS yoy_pct
FROM yoy_lag
WHERE prev_year_revenue IS NOT NULL
ORDER BY yr, mo;'''),

code('c04', '''-- Pattern 2: Cohort Analysis
-- Given: server provisioning data (server_id, provisioned_date, decommissioned_date)
-- Question: For each provisioning cohort (quarter), what % are still active after N quarters?

-- Simulate server lifecycle data
WITH servers AS (
    SELECT 1 AS server_id, DATE('2024-01-15') AS provisioned, NULL AS decommissioned UNION ALL
    SELECT 2, DATE('2024-01-20'), DATE('2024-06-01') UNION ALL
    SELECT 3, DATE('2024-04-10'), NULL UNION ALL
    SELECT 4, DATE('2024-04-15'), DATE('2024-09-01') UNION ALL
    SELECT 5, DATE('2024-07-01'), NULL UNION ALL
    SELECT 6, DATE('2024-07-10'), NULL
),
-- Step 1: Assign each server to a cohort (provisioning quarter)
with_cohort AS (
    SELECT
        server_id,
        provisioned,
        decommissioned,
        -- Cohort = first quarter of provisioning year
        DATE(provisioned, 'start of month', '-' ||
            ((strftime('%m', provisioned) - 1) % 3) || ' months') AS cohort_start
    FROM servers
),
-- Step 2: Count cohort size
cohort_sizes AS (
    SELECT cohort_start, COUNT(*) AS cohort_size
    FROM with_cohort
    GROUP BY cohort_start
),
-- Step 3: Count still active at end of 2024 (no decommission date or decommissioned after)
still_active AS (
    SELECT cohort_start, COUNT(*) AS active_count
    FROM with_cohort
    WHERE decommissioned IS NULL OR decommissioned > DATE('2024-12-31')
    GROUP BY cohort_start
)
SELECT
    cs.cohort_start,
    cs.cohort_size,
    COALESCE(sa.active_count, 0) AS still_active,
    ROUND(COALESCE(sa.active_count, 0) * 100.0 / cs.cohort_size, 0) AS retention_pct
FROM cohort_sizes cs
LEFT JOIN still_active sa ON cs.cohort_start = sa.cohort_start
ORDER BY cs.cohort_start;'''),

code('c05', '''-- Pattern 3: Funnel Analysis
-- Given: user events with (user_id, event_type, event_time)
-- Question: How many users completed each step of: view → add_to_cart → checkout → purchase?

-- Simulate checkout funnel events
WITH events AS (
    SELECT 1 AS user_id, 'view' AS event_type UNION ALL
    SELECT 1, 'add_to_cart' UNION ALL
    SELECT 1, 'checkout' UNION ALL
    SELECT 1, 'purchase' UNION ALL
    SELECT 2, 'view' UNION ALL
    SELECT 2, 'add_to_cart' UNION ALL
    SELECT 3, 'view' UNION ALL
    SELECT 4, 'view' UNION ALL
    SELECT 4, 'add_to_cart' UNION ALL
    SELECT 4, 'checkout'
),
-- Conditional aggregation: count distinct users who completed each step
funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event_type = 'view'        THEN user_id END) AS step1_view,
        COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) AS step2_cart,
        COUNT(DISTINCT CASE WHEN event_type = 'checkout'    THEN user_id END) AS step3_checkout,
        COUNT(DISTINCT CASE WHEN event_type = 'purchase'    THEN user_id END) AS step4_purchase
    FROM events
)
SELECT
    step1_view,
    step2_cart,
    step3_checkout,
    step4_purchase,
    -- Conversion rates between steps
    ROUND(step2_cart * 100.0 / step1_view, 0) AS view_to_cart_pct,
    ROUND(step3_checkout * 100.0 / step2_cart, 0) AS cart_to_checkout_pct,
    ROUND(step4_purchase * 100.0 / step3_checkout, 0) AS checkout_to_purchase_pct,
    ROUND(step4_purchase * 100.0 / step1_view, 0) AS overall_conversion_pct
FROM funnel;'''),

md('c06', '''## 🎤 5 Interview Q&A

**Q1: What is the difference between LAG and LEAD?**
`LAG(col, n)` returns the value from n rows BEFORE the current row (look backward).
`LEAD(col, n)` returns the value from n rows AFTER the current row (look forward).
Both require `OVER (ORDER BY ...)`. Use LAG for YoY comparisons (prior period), use LEAD
for "time until next event" calculations.

---

**Q2: How would you find users who completed step A but never step B?**
Use `COUNT(CASE WHEN event = \'A\' THEN 1 END) > 0` in a HAVING clause,
combined with `COUNT(CASE WHEN event = \'B\' THEN 1 END) = 0`:
```sql
SELECT user_id FROM events
GROUP BY user_id
HAVING SUM(CASE WHEN event = \'view\' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN event = \'purchase\' THEN 1 ELSE 0 END) = 0;
```

---

**Q3: What is the difference between RANK(), DENSE_RANK(), and ROW_NUMBER()?**
All three number rows within a partition. With ties:
- `ROW_NUMBER()` assigns unique sequential numbers (1,2,3,4 — no ties)
- `RANK()` skips numbers after ties (1,2,2,4 — skips 3)
- `DENSE_RANK()` does not skip (1,2,2,3 — compact)
Use RANK for competitions (ties share place but the next rank skips). Use DENSE_RANK for top-N grouping.

---

**Q4: How do you calculate a 7-day rolling average in SQL?**
```sql
AVG(revenue) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```
`ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` defines a 7-row window (6 before + current).
Use `RANGE BETWEEN INTERVAL \'6\' DAY PRECEDING AND CURRENT ROW` for date-based ranges with gaps.

---

**Q5: What is the Citi application of cohort analysis?**
Citi capacity team used cohort analysis on server provisioning data instead of user events.
Cohort = provisioning quarter. Retention = still active (not decommissioned) after N quarters.
The analysis revealed 340 servers provisioned but not decommissioned — a "shadow fleet" costing
in licensing and maintenance. Identifying the cohort that had the worst decommissioning compliance
let the team target the right infrastructure owners for cleanup.'''),

md('c07', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Window Function** | Aggregate function that operates over a sliding window of rows without collapsing the result set |
| **PARTITION BY** | Divides rows into groups for window functions — like GROUP BY but keeps all rows |
| **ORDER BY (in window)** | Defines row order within each partition for LAG, LEAD, RANK, running totals |
| **LAG(col, n)** | Value from n rows before current row — used for period-over-period comparisons |
| **LEAD(col, n)** | Value from n rows after current row — used for time-to-next-event |
| **ROWS BETWEEN** | Explicit window frame — `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` = 7-row window |
| **Cohort** | A group defined by a shared characteristic at a point in time — "users who joined in January" |
| **Funnel** | A sequence of steps where users drop off at each stage — conversion rate per step |
| **YoY** | Year-over-Year — comparing the same period across different years |
| **Conditional Aggregation** | `SUM(CASE WHEN condition THEN value END)` — pivot-style aggregation without actual PIVOT |'''),

md('c08', '''## 💼 The Citi Narrative

**Context:** Citi capacity planning team — server fleet of 6,000 endpoints.
Infrastructure spans 12 teams, servers provisioned across 8 quarters.

**The Problem:** No visibility into "which servers should have been decommissioned but weren\'t."
Licensing costs were based on total server count, including long-inactive servers.

**The Cohort Analysis:** Applied the user retention pattern to server lifecycle:
- Cohort = provisioning quarter (Q1 2024, Q2 2024, etc.)
- "Retention" = still active (not decommissioned) after N quarters
- Expected: most servers decommissioned within 4-6 quarters as applications were retired

**The Finding:** Q1 2023 cohort had 340 servers still "active" after 8 quarters.
Normal decommission rate for this vintage was 85%. These 340 were a shadow fleet —
nobody had officially decommissioned them, but they weren\'t serving production traffic.

**Impact:** Identified $X in licensing cost reduction. Changed decommissioning process to
require a quarterly cohort report. Ownership of old servers now auto-escalated after 6 quarters.

**Interview Line:** *"The pattern came from user retention analysis, but the data was servers.
Cohort = provisioning quarter. Retention = still active. We found 340 servers that should
have been retired — using exactly the same SQL you\'d write for user churn."*'''),

code('c09', '''-- Practice: Write these analytical SQL queries

-- 1. Calculate month-over-month change in server count per environment
-- Table: dim_server(server_id, env, provisioned_date)
-- Expected output: env, month, server_count, prev_month_count, mom_change

-- 2. Find the top 3 servers by CPU for EACH environment
-- Table: fact_monitoring(server_id, env, cpu_pct)
-- Use RANK() or ROW_NUMBER() with PARTITION BY env

-- 3. Calculate 7-day rolling average CPU for server_id = 42
-- Table: daily_avg(server_id, date, avg_cpu)

-- Solutions:

-- 1. MoM change
print("Query 1 — MoM change:")
print("""
WITH monthly_count AS (
    SELECT
        env,
        DATE_TRUNC('month', provisioned_date) AS month,
        COUNT(*) AS server_count
    FROM dim_server
    GROUP BY env, DATE_TRUNC('month', provisioned_date)
)
SELECT
    env, month, server_count,
    LAG(server_count) OVER (PARTITION BY env ORDER BY month) AS prev_count,
    server_count - LAG(server_count) OVER (PARTITION BY env ORDER BY month) AS mom_change
FROM monthly_count
ORDER BY env, month;
""")

-- 2. Top 3 per env
print("Query 2 — Top 3 per environment:")
print("""
SELECT * FROM (
    SELECT
        server_id, env, cpu_pct,
        RANK() OVER (PARTITION BY env ORDER BY cpu_pct DESC) AS rank
    FROM fact_monitoring
) ranked
WHERE rank <= 3;
""")'''),

md('c10', '''## 🎯 Summary

### The Three Patterns
| Pattern | Use case | Key SQL |
|---------|----------|---------|
| **YoY Growth** | Period comparisons | `LAG(value, 12)` or self-join |
| **Cohort Analysis** | Retention / lifecycle | `FIRST_VALUE()` + `GROUP BY cohort` |
| **Funnel** | Conversion rates | `COUNT(CASE WHEN step = X THEN 1 END)` |

### Interview Confidence Checklist
- [ ] Can write YoY using both LAG and self-join (and explain tradeoffs)
- [ ] Can build a cohort table from raw event/provisioning data
- [ ] Can calculate funnel conversion rates with conditional aggregation
- [ ] Can explain RANK vs DENSE_RANK vs ROW_NUMBER
- [ ] Can name the Citi narrative: 340 ghost servers found via cohort analysis

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 5-C: ETL Patterns — argparse, Logging, Pipeline Structure
# ─────────────────────────────────────────────────────────────────────────────

ETL_PATTERNS = [
md('c01', '''# Python — ETL Patterns: argparse, Logging, Pipeline Structure
---

<div style="padding:15px;border-left:8px solid #fa709a;background:#fff0f5;border-radius:4px;">
<strong>Core Insight:</strong> Production ETL pipelines are not scripts — they are programs.
They accept arguments, emit structured logs, handle errors gracefully, and exit with
the right code for orchestrators (Airflow, Kubernetes). Learn this structure once,
apply it to every pipeline you write.
</div>

### The Citi Pattern
The ETL pipeline template came directly from Citi\'s capacity data pipeline —
`--env`, `--date`, `--dry-run` flags, structured JSON logging, `sys.exit(1)` on failure
for Airflow retry detection. The same code ran in dev, staging, and production with zero
code changes — only environment variable differed.'''),

md('c02', '''## 🧠 The Production ETL Checklist

| Concern | The Pattern |
|---------|------------|
| **Arguments** | `argparse` — not hardcoded values. `--env prod`, `--date 2024-01-15`, `--dry-run` |
| **Logging** | Structured JSON logs — not `print()`. Level + timestamp + context in every message |
| **Error Handling** | `try/except` at pipeline level. `sys.exit(1)` on failure → Airflow retries |
| **Idempotency** | Running the pipeline twice for the same `--date` produces the same result |
| **Dry Run** | `--dry-run` flag to validate without writing — essential for testing in prod |
| **Configuration** | Environment variables for secrets. `argparse` for run parameters |

### Why Structured Logs?
`print("Processing complete")` is useless in production.
`{"ts": "2024-01-15T14:23:00Z", "level": "INFO", "job": "capacity-etl", "rows": 14400, "env": "prod"}`
can be queried in CloudWatch Logs, Splunk, or ELK — automatically parsed, alertable, searchable.'''),

code('c03', '''#!/usr/bin/env python3
"""
capacity_etl.py — Production-grade ETL pipeline template
Usage: python capacity_etl.py --env prod --date 2024-01-15 [--dry-run]
"""
import argparse
import json
import logging
import sys
import time
from datetime import date, datetime


# ── Structured logging setup ─────────────────────────────────────────────────

class JSONFormatter(logging.Formatter):
    """Emit logs as JSON lines — compatible with CloudWatch, ELK, Splunk."""
    def __init__(self, job_name: str):
        super().__init__()
        self.job_name = job_name

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "job": self.job_name,
            "msg": record.getMessage(),
        }
        # Add any extra fields passed to the logger
        for key, value in record.__dict__.items():
            if key not in ("msg", "args", "levelname", "levelno", "pathname",
                           "filename", "module", "exc_info", "exc_text",
                           "stack_info", "lineno", "funcName", "created",
                           "msecs", "relativeCreated", "thread", "threadName",
                           "processName", "process", "name", "message"):
                log_data[key] = value
        return json.dumps(log_data)


def setup_logging(job_name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(job_name)
    logger.setLevel(getattr(logging, level))
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter(job_name))
    logger.addHandler(handler)
    logger.propagate = False
    return logger'''),

code('c04', '''# ── Argument parsing ─────────────────────────────────────────────────────────

def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Capacity ETL — extract monitoring data, load to data warehouse",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --env prod --date 2024-01-15
  %(prog)s --env dev --date 2024-01-15 --dry-run
  %(prog)s --env staging --date 2024-01-15 --log-level DEBUG
        """
    )
    parser.add_argument(
        "--env", required=True, choices=["dev", "staging", "prod"],
        help="Target environment"
    )
    parser.add_argument(
        "--date", required=True, type=lambda s: date.fromisoformat(s),
        help="Date to process (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Validate and log without writing any data"
    )
    parser.add_argument(
        "--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )
    return parser.parse_args(argv)


# ── Pipeline stages ──────────────────────────────────────────────────────────

def extract(env: str, run_date: date, logger: logging.Logger) -> list:
    logger.info("Starting extract", extra={"stage": "extract", "env": env, "date": str(run_date)})
    # In production: connect to APM API or S3
    rows = [{"server_id": f"SRV-{i:04d}", "cpu": 45.0 + i*0.01, "date": str(run_date)}
            for i in range(1, 6001)]  # 6000 servers
    logger.info("Extract complete", extra={"stage": "extract", "rows": len(rows)})
    return rows


def transform(rows: list, logger: logging.Logger) -> list:
    logger.info("Starting transform", extra={"stage": "transform", "input_rows": len(rows)})
    transformed = []
    errors = 0
    for row in rows:
        try:
            transformed.append({
                "server_id": row["server_id"],
                "cpu_pct": round(float(row["cpu"]), 2),
                "date": row["date"],
                "alert": row["cpu"] > 80
            })
        except (KeyError, ValueError) as e:
            errors += 1
            logger.warning("Row transform failed", extra={"error": str(e), "row": str(row)[:100]})
    logger.info("Transform complete", extra={
        "stage": "transform", "output_rows": len(transformed), "errors": errors
    })
    return transformed


def load(rows: list, env: str, dry_run: bool, logger: logging.Logger) -> int:
    if dry_run:
        logger.info("DRY RUN: skipping load", extra={"stage": "load", "would_write": len(rows)})
        return len(rows)
    logger.info("Starting load", extra={"stage": "load", "env": env, "rows": len(rows)})
    # In production: write to S3/Redshift/Snowflake
    time.sleep(0.1)  # simulate I/O
    logger.info("Load complete", extra={"stage": "load", "rows_written": len(rows)})
    return len(rows)


# ── Main entrypoint ──────────────────────────────────────────────────────────

def main(argv=None):
    args = parse_args(argv)
    logger = setup_logging("capacity-etl", level=args.log_level)

    logger.info("Pipeline started", extra={
        "env": args.env, "date": str(args.date), "dry_run": args.dry_run
    })
    start = time.perf_counter()

    try:
        rows = extract(args.env, args.date, logger)
        rows = transform(rows, logger)
        written = load(rows, args.env, args.dry_run, logger)
        elapsed = round(time.perf_counter() - start, 2)
        logger.info("Pipeline complete", extra={
            "rows_written": written, "duration_s": elapsed, "env": args.env
        })
        return 0  # success — Airflow reads this exit code

    except Exception as e:
        elapsed = round(time.perf_counter() - start, 2)
        logger.error("Pipeline failed", extra={
            "error": str(e), "error_type": type(e).__name__, "duration_s": elapsed
        })
        return 1  # failure — Airflow will retry


if __name__ == "__main__":
    sys.exit(main())

# Demo run (as if called from command line):
exit_code = main(["--env", "dev", "--date", "2024-01-15", "--dry-run"])
print(f"\\nExit code: {exit_code} (0=success, 1=failure)")'''),

md('c05', '''## 📊 Idempotency — The Critical Property

**Definition:** Running the pipeline multiple times with the same inputs produces the same result.

**Why it matters:** Airflow retries failed tasks. Without idempotency:
- Retry inserts duplicate rows → wrong aggregates
- Retry re-processes data that was already loaded → double-counting

**How to implement:**
```sql
-- Option 1: DELETE + INSERT (for date partitions)
DELETE FROM fact_monitoring WHERE date = :run_date;
INSERT INTO fact_monitoring SELECT ... WHERE date = :run_date;

-- Option 2: UPSERT (INSERT ... ON CONFLICT)
INSERT INTO fact_monitoring (server_id, date, cpu_pct)
VALUES (%(server_id)s, %(date)s, %(cpu_pct)s)
ON CONFLICT (server_id, date)
DO UPDATE SET cpu_pct = EXCLUDED.cpu_pct;

-- Option 3: Overwrite S3 partition
s3://bucket/monitoring/date=2024-01-15/  # overwrite entire partition
```

**The golden rule:** A pipeline that can be safely retried is a pipeline that can be operated.
Every production pipeline must be idempotent.'''),

md('c06', '''## 🎤 5 Interview Q&A

**Q1: Why use `sys.exit(1)` instead of raising an exception?**
Orchestrators like Airflow, Kubernetes, and shell scripts check the process exit code — not Python exceptions.
`sys.exit(1)` signals failure to the OS. `sys.exit(0)` signals success.
If you raise an unhandled exception, the process exits with code 1 anyway, but the error message
may not be in your structured logs. Catching the exception, logging it with full context,
then calling `sys.exit(1)` gives you both the correct exit code and a searchable log entry.

---

**Q2: What is idempotency and how do you achieve it in an ETL pipeline?**
An idempotent pipeline produces the same output when run multiple times with the same input.
Achieve it by partitioning your target table by the processing date and using DELETE+INSERT
or UPSERT on each run. Airflow retries mean pipelines run multiple times — idempotency
ensures duplicates don\'t accumulate.

---

**Q3: Why structured JSON logs instead of print statements?**
JSON logs are machine-parseable. CloudWatch Logs Insights, Splunk, and ELK can parse them
automatically, enabling queries like "show all runs where rows > 10000 and env = prod".
Print statements are strings — you can\'t filter them programmatically without regex.
In a production system with 50 pipelines running daily, structured logs are how you debug
at 3am without SSH access to the server.

---

**Q4: What is a dry-run flag and when do you use it?**
`--dry-run` executes all pipeline logic except the final write operation. It extracts,
transforms, validates — but skips the load step. Use cases: (1) test a new pipeline
against production data without mutating anything; (2) validate a backfill before running
it; (3) debug issues by seeing what WOULD be written. Critical in production environments
where "undo" is not an option.

---

**Q5: What is the difference between `logging.info()` and `print()`?**
`print()` is ephemeral — it goes to stdout with no metadata.
`logging.info()` goes through the logging framework with: timestamp, level, logger name, module,
line number, and any `extra={}` fields you add. The logging framework supports:
handlers (route to file, stdout, CloudWatch), formatters (plain text vs JSON), and levels
(filter debug noise in production with `logging.WARNING`). In production, always use logging.'''),

md('c07', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **ETL** | Extract, Transform, Load — the pattern for moving data from source to destination |
| **ELT** | Extract, Load, Transform — load raw data first, transform in-warehouse (modern data platform approach) |
| **Idempotency** | Running the same operation multiple times produces the same result — critical for retry safety |
| **argparse** | Python standard library for CLI argument parsing — `--flag value`, `--boolean-flag` |
| **Structured Logging** | Logs as JSON/key-value pairs — machine-parseable, filterable in log aggregation tools |
| **Exit Code** | Integer returned by a process: 0=success, non-zero=failure — orchestrators use this for retry logic |
| **Dry Run** | Execute logic without side effects — validates without writing data |
| **Backfill** | Re-running a pipeline for past dates to populate historical data |
| **Orchestrator** | Tool that schedules and monitors pipelines (Airflow, Prefect, Dagster, Kubernetes CronJobs) |
| **Partition** | Organizing data by a key (usually date) so loads can be targeted and overwritten safely |'''),

md('c08', '''## 💼 The Citi Narrative

**Context:** Citi capacity ETL pipeline — extracts APM data for 6,000 servers,
transforms into daily capacity summaries, loads to PostgreSQL for reporting.

**The Problem:** Original script had hardcoded database credentials, printed status to stdout,
and would silently succeed even if 0 rows were written. Airflow marked it as successful
when it shouldn\'t have. Debugging failures required SSH access and grep-ing through logs.

**The Fix — Four Changes:**
1. `argparse`: `--env prod/dev`, `--date 2024-01-15`, `--dry-run` flags
2. JSON logging: every stage logged rows in/out, duration, any errors
3. `sys.exit(1)` on pipeline failure: Airflow retries automatically
4. Idempotent load: `DELETE WHERE date = :run_date` + `INSERT` — safe to retry

**Result:** Same pipeline code ran in dev, staging, and production with zero code changes.
Airflow retry worked correctly. When a source DB was unavailable at 06:00, the pipeline
retried at 06:05, succeeded, and no manual intervention was needed.

**Interview Line:** *"The difference between a script and a pipeline is one of these four things.
A script prints to stdout and exits. A pipeline logs JSON, accepts `--env` and `--date`,
handles errors with the right exit code, and can be retried safely."*'''),

code('c09', '''# Practice: Fix the anti-pattern pipeline below

import sys, time

# ❌ ANTI-PATTERN: Script, not a pipeline
def bad_pipeline():
    env = "prod"                              # hardcoded
    date = "2024-01-15"                       # hardcoded
    print("Starting ETL for", date)           # not structured

    try:
        data = [{"id": i, "val": i*1.5} for i in range(100)]
        print("Got", len(data), "rows")       # not structured
        # load to DB...
        print("Done")                         # no exit code
    except Exception as e:
        print("Error:", e)                    # not structured, no exit

# ✅ YOUR TASK: Rewrite using the patterns from this notebook
# Requirements:
# 1. Accept --env and --date via argparse
# 2. Log each step as JSON with level, msg, stage, rows
# 3. Return exit code 0 on success, 1 on failure
# 4. Support --dry-run flag

# See the full solution in cells c03-c04 above.
# Key test: run with --dry-run and verify no DB writes occur.
# Run with invalid --env and verify argparse rejects it.

print("Anti-pattern identified. See cells c03-c04 for the correct pattern.")
print("Key insight: same 4 changes apply to ANY ETL pipeline you write.")'''),

md('c10', '''## 🎯 Summary

### The Production ETL Template
```
main()
  ├── parse_args()        → argparse: --env, --date, --dry-run
  ├── setup_logging()     → JSON formatter, stdout handler
  ├── try:
  │   ├── extract()       → log rows extracted
  │   ├── transform()     → log rows in/out, errors
  │   └── load()          → skip if --dry-run
  └── except:
      └── log error → sys.exit(1)   ← Airflow retries
```

### Interview Confidence Checklist
- [ ] Can explain why sys.exit(1) matters for orchestrators
- [ ] Can explain idempotency and give a SQL implementation
- [ ] Can write a JSON formatter for Python logging
- [ ] Can describe argparse with --env, --date, --dry-run
- [ ] Can name the Citi narrative: same code in dev/staging/prod with zero changes

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 5-D: Capacity Planning Methodology
# ─────────────────────────────────────────────────────────────────────────────

CAPACITY_PLANNING = [
md('c01', '''# Technology — Capacity Planning Methodology
---

<div style="padding:15px;border-left:8px solid #fa709a;background:#fff0f5;border-radius:4px;">
<strong>Core Insight:</strong> Capacity planning is Sean\'s key differentiator. While most
data engineering candidates know SQL and Python, almost none have experience preventing
capacity outages through data-driven forecasting. This is a direct Citi story —
own it completely.
</div>

### The Four-Step Loop
Sean\'s actual methodology from Citi:
1. **Baseline** — 90-day rolling average from CA APM
2. **Model** — identify the capacity driver (requests/sec, not time)
3. **Forecast** — project the trend, set ceiling at 70% utilization
4. **Alert** — trigger when projected trend line hits the ceiling, not when current reading hits it'''),

md('c02', '''## 🧠 Why Capacity Planning is a Data Engineering Problem

| Step | The Data Engineering Skill |
|------|--------------------------|
| Baseline | Time-series aggregation — rolling averages, percentiles, seasonal decomposition |
| Model | Feature engineering — what DRIVES utilization? (traffic, batch jobs, user growth) |
| Forecast | Linear regression, trend extrapolation, confidence intervals |
| Alert | Threshold logic on the projected value, not current reading |

### The Ceiling Rule
**Never alert at 100%** — by then it\'s too late.
Alert at **70%** on the trend line, giving 6-8 weeks of lead time for procurement.
Server provisioning at Citi took 3-4 weeks (hardware + configuration + security scan).
A 70% ceiling on a linear trend gives 30pp headroom = 3-4 weeks of safe growth at typical rates.

### The Capacity Driver Rule
Don\'t model CPU vs time. Model CPU vs requests/second.
Time is a proxy — the real driver is load.
When a batch job moves from 2am to 11pm, a time-based model fails. A load-based model adapts.'''),

code('c03', '''import numpy as np
import json
from datetime import date, timedelta

# ══════════════════════════════════════
# STEP 1: BASELINE — 90-day rolling average
# ══════════════════════════════════════

np.random.seed(42)

# Simulate 90 days of CPU readings for one server
days = np.arange(90)
# Normal utilization with slight upward trend
baseline_cpu = 35 + 0.15 * days + np.random.normal(0, 3, 90)
dates = [date(2024, 1, 1) + timedelta(days=int(d)) for d in days]

# 90-day statistics
p50 = np.percentile(baseline_cpu, 50)
p95 = np.percentile(baseline_cpu, 95)
rolling_7day = np.array([baseline_cpu[max(0,i-6):i+1].mean() for i in range(90)])

print("=== STEP 1: BASELINE ===")
print(f"90-day p50 CPU: {p50:.1f}%")
print(f"90-day p95 CPU: {p95:.1f}%")
print(f"Current (day 90): {baseline_cpu[-1]:.1f}%")
print(f"7-day rolling avg: {rolling_7day[-1]:.1f}%")
print(f"Trend: +{0.15:.2f}% per day")'''),

code('c04', '''# ══════════════════════════════════════
# STEP 2 & 3: MODEL + FORECAST
# ══════════════════════════════════════

import numpy as np

np.random.seed(42)
days_history = np.arange(90)
baseline_cpu = 35 + 0.15 * days_history + np.random.normal(0, 3, 90)

# Fit a linear trend to the last 30 days (most recent trend matters most)
last_30 = baseline_cpu[-30:]
x = np.arange(30)

# Linear regression: y = mx + b
coeffs = np.polyfit(x, last_30, 1)
slope = coeffs[0]      # percentage points per day
intercept = coeffs[1]  # baseline

print("=== STEP 2: MODEL ===")
print(f"Linear trend: +{slope:.3f}% CPU per day")
print(f"At this rate: +{slope*7:.2f}% per week, +{slope*30:.2f}% per month")

# Project forward 60 days
CEILING = 70.0
future_days = np.arange(60)
projected_cpu = (intercept + 30 * slope) + slope * future_days  # from day 90 forward

# Find when we hit the ceiling
above_ceiling = np.where(projected_cpu >= CEILING)[0]
days_until_breach = above_ceiling[0] if len(above_ceiling) > 0 else None

print("\n=== STEP 3: FORECAST ===")
print(f"Current CPU trend: {slope:.3f}%/day")
print(f"Ceiling:           {CEILING}%")
if days_until_breach is not None:
    print(f"Projected breach:  Day +{days_until_breach} ({days_until_breach} days from today)")
    from datetime import date, timedelta
    breach_date = date(2024, 4, 1) + timedelta(days=int(days_until_breach))
    print(f"Breach date:       {breach_date}")
    print(f"Lead time:         {days_until_breach} days (provisioning takes 21-28 days)")
    print(f"Action needed:     {'NOW — within lead time!' if days_until_breach < 35 else 'Monitor weekly'}")
else:
    print("No breach projected in next 60 days")'''),

code('c05', '''# ══════════════════════════════════════
# STEP 4: ALERT — Proactive, not reactive
# ══════════════════════════════════════

import numpy as np
from datetime import date, timedelta

def capacity_alert(server_id: str, cpu_readings: np.ndarray,
                   ceiling: float = 70.0, lead_days: int = 35) -> dict:
    """
    Evaluate capacity risk for a server.

    Returns:
        alert: bool — should we act now?
        days_until_breach: int or None
        action: str — what to do
    """
    if len(cpu_readings) < 14:
        return {"alert": False, "action": "insufficient_data"}

    # Fit trend to last 14 days
    x = np.arange(len(cpu_readings))
    slope, intercept = np.polyfit(x, cpu_readings, 1)
    current = cpu_readings[-1]

    # Project forward
    days_until_breach = None
    if slope > 0:  # only breaches if trend is upward
        # current_value + slope * n_days = ceiling
        if current < ceiling:
            n = (ceiling - current) / slope
            days_until_breach = int(n)

    alert = (days_until_breach is not None and days_until_breach <= lead_days)
    action = "PROVISION NOW" if alert else ("MONITOR" if days_until_breach else "STABLE")

    return {
        "server_id": server_id,
        "current_cpu": round(float(current), 1),
        "slope_per_day": round(float(slope), 3),
        "days_until_breach": days_until_breach,
        "alert": alert,
        "action": action
    }

# Test on a problem server (fast-growing)
np.random.seed(0)
problem_server = 40 + np.arange(30) * 1.2 + np.random.normal(0, 2, 30)  # +1.2%/day
stable_server  = 55 + np.random.normal(0, 3, 30)  # stable at 55%

print("Problem server:", capacity_alert("SRV-9001", problem_server))
print("Stable server: ", capacity_alert("SRV-9002", stable_server))'''),

md('c06', '''## 📊 Fleet-Wide Capacity Dashboard

The capacity alert runs across all 6,000 servers daily:

```python
# Conceptual: daily capacity scan
alerts = []
for server_id in all_servers:
    readings = fetch_90day_cpu(server_id)
    result = capacity_alert(server_id, readings)
    if result["alert"]:
        alerts.append(result)

# Sort by urgency (fewest days until breach)
alerts.sort(key=lambda x: x["days_until_breach"])

# Report top 20 most urgent
print(f"CAPACITY ALERT REPORT — {date.today()}")
print(f"Servers at risk (breach within 35 days): {len(alerts)}")
for a in alerts[:20]:
    print(f"  {a['server_id']}: {a['days_until_breach']} days | {a['current_cpu']}% CPU | +{a['slope_per_day']}%/day")
```

### The Capacity Report Format (Citi Style)
```
SERVER: SRV-1042 (Production, App: TradingEngine)
Current CPU: 67%
Trend: +0.8% per day (+5.6% per week)
Projected breach (70%): Day +4 = 2024-04-05
Action: PROVISION NOW — lead time is 21 days, breach in 4 days
Owner: Infrastructure Team A (escalation: auto)
```'''),

md('c07', '''## 🎤 5 Interview Q&A

**Q1: What is capacity planning and how is it different from monitoring?**
Monitoring tells you what\'s happening NOW — reactive. Capacity planning tells you what
WILL happen and WHEN — proactive. Monitoring: "CPU is at 85% right now, alert!"
Capacity planning: "CPU is trending at +0.8%/day, will breach 70% in 4 days."
The goal of capacity planning is to never have a monitoring alert fire in production.

---

**Q2: Why 70% ceiling instead of 100%?**
Provisioning hardware takes time — at Citi, 3-4 weeks for hardware + config + security scan.
70% provides ~30 percentage points of headroom. At typical growth rates (+0.8%/day),
30pp = ~37 days of lead time. Setting the ceiling at 90% or 95% only gives 5-12 days —
not enough time to provision before impact.

---

**Q3: Why model against requests/second rather than time?**
Time is a proxy for load — the real driver. When a batch job moves from 2am to 6pm,
a time-based model predicts the wrong utilization for that time slot.
A load-based model (CPU vs requests/sec) adapts: if traffic doubles, the model says
CPU will double. This is more robust to schedule changes, traffic spikes, and application changes.

---

**Q4: How do you handle seasonality in capacity forecasting?**
Simple linear regression ignores day-of-week and time-of-day patterns.
For systems with strong seasonality (business-hours peaks, monthly billing spikes):
(1) Use STL decomposition to separate trend from seasonal patterns.
(2) Model trend separately from seasonal component.
(3) Forecast trend, then add back the seasonal pattern for the target time.
In practice, weekly seasonality (Mon-Fri vs weekend) is often enough to model.

---

**Q5: How do you communicate capacity risk to non-technical stakeholders?**
Translate to business impact: "We will run out of compute capacity for the TradingEngine
on April 5th. This will cause transaction processing delays during peak trading hours.
Provisioning new servers takes 3 weeks and costs $X. We need to order by March 15th."
Avoid: "CPU utilization will exceed the 70th percentile threshold in 4 days."
Use: "The trading engine will slow down in 4 days if we don\'t act by tomorrow."'''),

md('c08', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Capacity Driver** | The metric that best predicts resource utilization — usually load (requests/sec), not time |
| **Utilization Ceiling** | The threshold above which performance degrades — typically 70-80% for CPU/memory |
| **Lead Time** | Time from ordering to delivery — determines how far ahead the forecast must look |
| **Linear Regression** | `y = mx + b` — fit a line to historical data to project future values |
| **Trend** | The long-term direction of a metric (slope of the regression line) |
| **Seasonality** | Repeating patterns by time of day / week / month — separate from trend |
| **STL Decomposition** | Seasonal-Trend decomposition using LOESS — separates trend, seasonal, residual components |
| **p95 / p99** | The 95th/99th percentile — used for capacity sizing (don\'t size for average, size for peak) |
| **Proactive vs Reactive** | Proactive = act before the breach. Reactive = act after the outage. |
| **Provisioning** | Allocating, configuring, and deploying new compute resources |'''),

md('c09', '''## 💼 The Citi Narrative

**Context:** Citi APM infrastructure — 6,000 monitored endpoints, growing application portfolio.
The capacity team was getting paged at 3am when servers hit 100% utilization.

**The Problem:** Monitoring was reactive. No system existed to predict when servers would
breach their utilization ceiling. The team was always in firefighting mode.

**The Four-Step Solution:**
1. **Baseline:** Pulled 90-day CPU data from CA APM API into PostgreSQL via Python ETL
2. **Model:** Linear regression on last 30 days per server, slope = capacity driver
3. **Forecast:** Project trend forward 60 days, compare to 70% ceiling
4. **Alert:** Daily Jira ticket auto-created for any server breaching in < 35 days

**The Result:**
- Caught 3 servers on a collision course with capacity 8 weeks before breach
- Provisioned new hardware before impact — zero downtime
- Alert volume for reactive capacity issues: dropped from 15/month to 0 in the following 12 months

**The Number:** 47 days — the first server flagged was 47 days from breach when the system
caught it. Provisioning took 28 days. Margin: 19 days. Plenty.

**Interview Line:** *"I was tired of getting paged at 3am for something we could have seen
coming 6 weeks earlier. So I built a forecasting model — 90-day baseline, linear trend,
70% ceiling alert. The first time it fired, we had 47 days of lead time. We provisioned
the server, the breach never happened, and I slept through the night it would have paged us."*'''),

code('c10', '''# Practice: Extend the capacity alert function

import numpy as np
from datetime import date, timedelta

def capacity_report(servers_data: dict, ceiling: float = 70.0) -> list:
    """
    Generate a capacity planning report for a fleet of servers.

    Args:
        servers_data: dict of server_id -> array of daily CPU readings (90 days)
        ceiling: utilization ceiling (default 70%)

    Returns:
        List of alert dicts, sorted by urgency (fewest days to breach first)
    """
    # Your implementation:
    # 1. For each server, fit a linear trend to last 30 days
    # 2. Project when it hits the ceiling
    # 3. Return servers breaching within 35 days, sorted by urgency

    alerts = []
    for server_id, readings in servers_data.items():
        readings = np.array(readings)
        last30 = readings[-30:]
        x = np.arange(30)
        slope, intercept = np.polyfit(x, last30, 1)
        current = readings[-1]

        days_to_breach = None
        if slope > 0 and current < ceiling:
            days_to_breach = int((ceiling - current) / slope)

        if days_to_breach is not None and days_to_breach <= 35:
            alerts.append({
                "server_id": server_id,
                "current_cpu": round(float(current), 1),
                "days_to_breach": days_to_breach,
                "breach_date": str(date.today() + timedelta(days=days_to_breach))
            })

    return sorted(alerts, key=lambda x: x["days_to_breach"])

# Test it
np.random.seed(42)
fleet = {
    "SRV-001": 30 + np.arange(90)*0.9 + np.random.normal(0,2,90),   # fast growing
    "SRV-002": 55 + np.random.normal(0,3,90),                         # stable
    "SRV-003": 45 + np.arange(90)*0.4 + np.random.normal(0,2,90),   # slow growing
}
report = capacity_report(fleet)
print(f"Servers at risk: {len(report)}")
for a in report:
    print(f"  {a['server_id']}: breach in {a['days_to_breach']} days ({a['breach_date']})")'''),

md('c11', '''## 🎯 Summary

### The Four-Step Loop
1. **Baseline** → 90-day rolling data, p50/p95 per server
2. **Model** → Linear regression on last 30 days, slope = trend
3. **Forecast** → Project to 70% ceiling, compute days until breach
4. **Alert** → Jira/Slack when breach within 35 days (lead time = 28 days)

### Interview Confidence Checklist
- [ ] Can explain the four-step loop from memory
- [ ] Can explain why 70% ceiling, not 100%
- [ ] Can explain why model load (requests/sec) not time
- [ ] Can write the linear regression + threshold logic in Python
- [ ] Can name the Citi story: 3 servers caught 8 weeks early, zero downtime

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 6-B: SQL Schema Design
# ─────────────────────────────────────────────────────────────────────────────

SQL_SCHEMA_DESIGN = [
md('c01', '''# SQL — Schema Design: Star Schema, Snowflake, SCD Type 2
---

<div style="padding:15px;border-left:8px solid #a18cd1;background:#f5f0ff;border-radius:4px;">
<strong>Core Insight:</strong> Schema design separates data engineers from analysts.
Star = denormalized for speed. Snowflake = normalized for consistency.
SCD Type 2 = the standard for tracking historical changes.
Get these three patterns wrong and your data warehouse is unusable.
</div>

### The Citi Context
Citi\'s capacity analytics warehouse used a star schema. When a server moved teams,
a new SCD Type 2 row was added — preserving who owned the server at incident time.
This changed root cause attribution for 12% of incidents.'''),

md('c02', '''## 🧠 Star vs Snowflake: The Decision

| Schema | Structure | When to use |
|--------|-----------|-------------|
| **Star** | Fact table + flat dimension tables (denormalized) | BI tools, fast queries, analysts write SQL |
| **Snowflake** | Fact table + normalized dimension tables (sub-dimensions) | Data consistency > query speed, ETL pipelines |
| **One Big Table** | Single flat table with all columns | Small datasets, ad-hoc analysis only |

### The Star Schema Pattern
```
fact_monitoring (event_id FK→servers FK→dates FK→metrics, value)
       │
       ├── dim_server (server_id, server_name, env, team, is_active)
       ├── dim_date   (date_id, date, year, quarter, month, day_of_week)
       └── dim_metric (metric_id, metric_type, unit, description)
```

**Why star queries are fast:**
- No joins between dimension tables — only fact → dim
- Dimension tables fit in memory (6,000 servers vs 500M fact rows)
- Query planner knows dimension tables are small → efficient hash joins'''),

code('c03', '''-- Star Schema DDL — Citi capacity analytics warehouse

-- Dimension: Servers (SCD Type 2 — historical tracking)
CREATE TABLE dim_server (
    server_key      SERIAL PRIMARY KEY,          -- surrogate key (never changes)
    server_id       VARCHAR(20) NOT NULL,         -- natural key (SRV-1042)
    server_name     VARCHAR(100) NOT NULL,
    environment     VARCHAR(20) NOT NULL,          -- dev/staging/prod
    team            VARCHAR(50) NOT NULL,
    application     VARCHAR(100),
    data_center     VARCHAR(50),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    -- SCD Type 2 tracking columns
    effective_date  DATE NOT NULL,               -- when this version became active
    expiry_date     DATE,                         -- NULL = current record
    is_current      BOOLEAN NOT NULL DEFAULT TRUE,
    -- Audit columns
    created_at      TIMESTAMP DEFAULT NOW(),
    updated_at      TIMESTAMP DEFAULT NOW()
);

-- Dimension: Dates (pre-populated calendar table)
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,          -- YYYYMMDD as integer (fast join)
    full_date       DATE NOT NULL,
    year            INTEGER NOT NULL,
    quarter         INTEGER NOT NULL,             -- 1-4
    month           INTEGER NOT NULL,             -- 1-12
    month_name      VARCHAR(10) NOT NULL,
    week_of_year    INTEGER NOT NULL,
    day_of_week     INTEGER NOT NULL,             -- 1=Monday, 7=Sunday
    is_weekend      BOOLEAN NOT NULL,
    is_holiday      BOOLEAN NOT NULL DEFAULT FALSE
);

-- Dimension: Metrics
CREATE TABLE dim_metric (
    metric_id       SERIAL PRIMARY KEY,
    metric_type     VARCHAR(50) NOT NULL,         -- cpu_pct, memory_pct, latency_ms
    unit            VARCHAR(20) NOT NULL,
    description     TEXT
);

-- Fact table: Monitoring events
CREATE TABLE fact_monitoring (
    event_id        BIGSERIAL PRIMARY KEY,
    server_key      INTEGER NOT NULL REFERENCES dim_server(server_key),
    date_key        INTEGER NOT NULL REFERENCES dim_date(date_key),
    metric_id       INTEGER NOT NULL REFERENCES dim_metric(metric_id),
    collected_at    TIMESTAMP NOT NULL,
    metric_value    NUMERIC(8,3) NOT NULL,
    -- Partitioned by month for performance
    CONSTRAINT fact_monitoring_collected_at CHECK (collected_at IS NOT NULL)
) PARTITION BY RANGE (collected_at);

-- Monthly partitions
CREATE TABLE fact_monitoring_2024_01 PARTITION OF fact_monitoring
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Indexes
CREATE INDEX idx_fact_server_date ON fact_monitoring(server_key, date_key);
CREATE INDEX idx_fact_metric_date ON fact_monitoring(metric_id, date_key);'''),

code('c04', '''-- SCD Type 2: Handling server team changes
-- When SRV-1042 moves from Team A to Team B on 2024-03-15,
-- we CLOSE the old record and INSERT a new one. History is preserved.

-- Current state: SRV-1042 belongs to Team A (effective 2023-01-01)
SELECT server_id, team, effective_date, expiry_date, is_current
FROM dim_server WHERE server_id = 'SRV-1042';
-- Returns: SRV-1042 | Team A | 2023-01-01 | NULL | TRUE

-- ── SCD Type 2 Update Procedure ──────────────────────────────────────────────
-- Step 1: Close the current record
UPDATE dim_server
SET expiry_date = '2024-03-14',
    is_current  = FALSE,
    updated_at  = NOW()
WHERE server_id  = 'SRV-1042'
  AND is_current = TRUE;

-- Step 2: Insert new version
INSERT INTO dim_server (server_id, server_name, environment, team, effective_date, expiry_date, is_current)
VALUES ('SRV-1042', 'SRV-1042', 'prod', 'Team B', '2024-03-15', NULL, TRUE);

-- ── Now you can query historical ownership ─────────────────────────────────
-- "Which team owned SRV-1042 during the January 2024 incident?"
SELECT s.server_id, s.team, s.effective_date, s.expiry_date
FROM dim_server s
WHERE s.server_id = 'SRV-1042'
  AND s.effective_date <= '2024-01-15'
  AND (s.expiry_date IS NULL OR s.expiry_date >= '2024-01-15');
-- Returns: SRV-1042 | Team A | 2023-01-01 | 2024-03-14

-- Critical insight: without SCD Type 2, a server that moved teams would ALWAYS show
-- the CURRENT team — making historical incident attribution wrong.
PRINT("SCD Type 2 preserves ownership at incident time — critical for post-mortems")'''),

md('c05', '''## 📊 Snowflake Schema: When Normalization Wins

```
fact_monitoring
    └── dim_server (server_key, server_id, location_key, team_key)
            ├── dim_location (location_key, data_center, city, country)
            └── dim_team     (team_key, team_name, department, cost_center)
```

**When to use Snowflake:**
- Location and team data changes frequently and independently
- You need a single source of truth for each entity
- You\'re building ETL pipelines (not analyst-facing BI)

**Trade-off:** Every query now needs 3-4 JOINs instead of 1-2.
For ad-hoc SQL by analysts, this creates friction.

```sql
-- Star query (simpler for analysts):
SELECT s.team, AVG(f.metric_value)
FROM fact_monitoring f
JOIN dim_server s ON f.server_key = s.server_key
GROUP BY s.team;

-- Snowflake query (more joins, more maintenance):
SELECT t.team_name, AVG(f.metric_value)
FROM fact_monitoring f
JOIN dim_server s   ON f.server_key = s.server_key
JOIN dim_team t     ON s.team_key = t.team_key
GROUP BY t.team_name;
```'''),

md('c06', '''## 🎤 5 Interview Q&A

**Q1: What is the difference between a star schema and a snowflake schema?**
Star: fact table + flat (denormalized) dimension tables. All dimension attributes in one table.
Snowflake: dimensions are normalized — hierarchies split into separate tables (dim_server → dim_location → dim_country).
Star is faster for queries (fewer joins), snowflake is more consistent for updates (each entity has one record).
Use star for BI/analytics. Use snowflake when dimension data changes frequently and independently.

---

**Q2: What is SCD Type 2 and when do you need it?**
SCD = Slowly Changing Dimension. Type 2 preserves history by adding new rows.
When an attribute changes (server moves teams, customer changes address), you:
(1) Close the current row by setting `expiry_date` and `is_current = FALSE`
(2) Insert a new row with the new values, `effective_date = today`, `is_current = TRUE`
You need it when you must answer questions like "which team owned this server during the incident?"
— questions that require historical accuracy, not just current state.

---

**Q3: What is a surrogate key and why use it instead of a natural key?**
Natural key = real-world identifier (server_id = \'SRV-1042\').
Surrogate key = system-generated integer (server_key = 4521).
Surrogate keys are used as foreign keys in fact tables because:
(1) They never change — even if the natural key changes (server renamed)
(2) They\'re smaller (integer vs varchar) — faster joins
(3) They support SCD Type 2 — multiple rows for the same server_id get different server_keys

---

**Q4: What is a date dimension table and why not just use the date column?**
A dim_date table pre-computes date attributes: year, quarter, month, day_of_week, is_weekend, is_holiday.
Without it, every query involving "group by quarter" must compute `DATE_TRUNC(\'quarter\', collected_at)`.
With a date dimension: `JOIN dim_date ON date_key = collected_at::DATE` → filter `WHERE quarter = 1`.
Also: you can mark company holidays, fiscal calendar periods, and other business rules once in dim_date
instead of in every query.

---

**Q5: What is a fact table and what should (and shouldn\'t) go in it?**
Fact table: stores events/measurements with foreign keys to dimensions and numeric measures.
✅ IN fact table: event timestamp, surrogate keys to dimensions, numeric measures (cpu_pct, latency_ms, count)
❌ NOT in fact table: descriptive attributes (server_name, team) — those go in dimensions.
This separation enables the star schema\'s core property: add new dimensions without changing the fact table.'''),

md('c07', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Fact Table** | Central table storing events/measurements with numeric measures and foreign keys to dimensions |
| **Dimension Table** | Reference table storing descriptive attributes of entities (servers, dates, metrics) |
| **Star Schema** | Fact table + flat (denormalized) dimension tables — optimized for query speed |
| **Snowflake Schema** | Fact table + normalized dimension hierarchy — optimized for consistency |
| **SCD Type 1** | Overwrite the old value — no history. Simple but lossy. |
| **SCD Type 2** | Add new row with new values, mark old row expired — preserves full history |
| **SCD Type 3** | Add a "previous value" column — limited history (only 1 change tracked) |
| **Surrogate Key** | System-generated integer primary key — never changes, used for foreign keys |
| **Natural Key** | Real-world identifier (server_id, customer_email) — may change |
| **Grain** | The level of detail in a fact table — one row per server per metric per minute |
| **Slowly Changing Dimension** | A dimension whose attributes change infrequently over time |
| **Conformed Dimension** | A dimension shared across multiple fact tables — ensures consistent joins |'''),

md('c08', '''## 💼 The Citi Narrative

**Context:** Citi capacity analytics — needed a data warehouse to support both real-time
alerting and quarterly trend reporting across 6,000 servers.

**The Schema Decision:**
- Star schema chosen over snowflake: analysts write SQL directly, and query simplicity wins
- SCD Type 2 on dim_server: servers moved between teams during organizational restructures (3-4 times/year)
- Partitioned fact table: 500M rows by year-end, needed partition pruning for monthly reports

**The SCD Type 2 Impact:**
Before SCD Type 2: incident post-mortem would show "Team B owns SRV-1042" — but the incident
happened when Team A still owned it. Root cause attribution was wrong for servers that had
changed ownership.

After SCD Type 2: `WHERE effective_date <= incident_date AND (expiry_date IS NULL OR expiry_date >= incident_date)`
correctly identified Team A as the responsible team at incident time.

**Impact:** Changed root cause attribution for 12% of incidents in the first quarter after
implementing SCD Type 2. Infrastructure teams could no longer claim "that server moved to
another team before the incident" — the data now showed the truth.

**Interview Line:** *"We implemented SCD Type 2 because teams argued about who owned a server
during an incident. With the old system, server ownership was current-state only — if a server
moved teams before the post-mortem, the incident would blame the new team. SCD Type 2 let us
ask \'who owned it at 2am on January 15th?\' and get the right answer."*'''),

code('c09', '''-- Practice: Write SCD Type 2 queries

-- Table: dim_server (server_key, server_id, team, effective_date, expiry_date, is_current)
-- Table: fact_monitoring (server_key, collected_at, metric_value)

-- 1. Find the team responsible for all HIGH-CPU incidents in January 2024
-- (servers with metric_value > 90 at any point in January)
-- Use SCD Type 2 to get the team that owned the server DURING the incident

-- 2. Count servers by team as of March 15, 2024
-- (point-in-time query)

-- Solutions:
print("Query 1: Team responsible for January incidents")
print("""
SELECT s.team, COUNT(*) AS high_cpu_events
FROM fact_monitoring f
JOIN dim_server s ON f.server_key = s.server_key
WHERE f.metric_value > 90
  AND f.collected_at BETWEEN '2024-01-01' AND '2024-01-31'
  AND s.effective_date <= f.collected_at::DATE
  AND (s.expiry_date IS NULL OR s.expiry_date >= f.collected_at::DATE)
GROUP BY s.team
ORDER BY high_cpu_events DESC;
""")

print("Query 2: Server count by team on March 15, 2024")
print("""
SELECT team, COUNT(*) AS server_count
FROM dim_server
WHERE effective_date <= '2024-03-15'
  AND (expiry_date IS NULL OR expiry_date >= '2024-03-15')
GROUP BY team
ORDER BY server_count DESC;
""")'''),

md('c10', '''## 🎯 Summary

### The Three Schema Patterns
| Pattern | Use when | Trade-off |
|---------|----------|-----------|
| **Star** | Analysts write SQL, BI tools | Faster queries, some redundancy |
| **Snowflake** | ETL pipelines, consistency critical | More joins, cleaner updates |
| **SCD Type 2** | Historical accuracy required | More rows, more complex queries |

### Interview Confidence Checklist
- [ ] Can draw a star schema with fact + 3 dimensions
- [ ] Can explain SCD Type 2 with the 2-step update (close old, insert new)
- [ ] Can write the point-in-time join query with effective/expiry dates
- [ ] Can explain surrogate vs natural key
- [ ] Can name the Citi narrative: 12% of incidents had wrong attribution before SCD Type 2

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 6-C: PySpark for Data Engineering
# ─────────────────────────────────────────────────────────────────────────────

PYSPARK = [
md('c01', '''# Python — PySpark for Data Engineering
---

<div style="padding:15px;border-left:8px solid #a18cd1;background:#f5f0ff;border-radius:4px;">
<strong>Core Insight:</strong> PySpark is pandas for data that doesn\'t fit in memory.
The critical lesson: Python UDFs are the bottleneck — they serialize data row-by-row
from JVM to Python (10x slower than built-in F. functions).
Replace Python UDFs with F.when().otherwise() chains.
</div>

### The Citi Migration
Citi\'s ETL pipeline migrated from pandas to PySpark when data volume exceeded 50GB/day.
Python UDFs were the bottleneck — serializing row-by-row. Replacing with `F.when().otherwise()`
cut runtime from 45 minutes to 4 minutes for the daily capacity aggregation.'''),

md('c02', '''## 🧠 Mental Models

| Model | The Insight |
|-------|-----------|
| **Lazy Evaluation** | PySpark builds a DAG of transformations. Nothing executes until you call an action (`.count()`, `.write()`). This lets Spark optimize the entire pipeline before running. |
| **The JVM Bridge** | Python UDFs cross the JVM→Python boundary row-by-row — like having 6M individual round-trips. Built-in F. functions run inside the JVM — no serialization. |
| **Immutable DataFrames** | Every transformation returns a NEW DataFrame. The original is unchanged. This enables Spark\'s optimization and parallelism. |

### Transformations vs Actions
```
Transformations (lazy — build the DAG):
  .filter(), .select(), .groupBy(), .join(), .withColumn()

Actions (trigger execution):
  .count(), .collect(), .show(), .write.parquet()
```

**Never call `.collect()` on a large DataFrame** — it brings ALL data to the driver.
Use `.write` to save results, or `.show(20)` to sample.'''),

code('c03', '''# PySpark fundamentals — SparkSession, DataFrame creation
# Note: In Jupyter, SparkSession may already be available as 'spark'

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, DateType
from datetime import date

# Create SparkSession (one per application)
spark = SparkSession.builder \
    .appName("capacity-etl") \
    .config("spark.sql.shuffle.partitions", "200") \
    .getOrCreate()

# Schema definition — always define schema explicitly for production pipelines
monitoring_schema = StructType([
    StructField("server_id",    StringType(),  nullable=False),
    StructField("collected_at", DateType(),    nullable=False),
    StructField("metric_type",  StringType(),  nullable=True),
    StructField("metric_value", DoubleType(),  nullable=True),
    StructField("environment",  StringType(),  nullable=True),
])

# Create DataFrame from data (in prod: read from S3/Hive)
data = [
    ("SRV-001", date(2024, 1, 15), "cpu_pct",    72.5, "prod"),
    ("SRV-001", date(2024, 1, 15), "memory_pct", 55.2, "prod"),
    ("SRV-002", date(2024, 1, 15), "cpu_pct",    91.3, "prod"),
    ("SRV-002", date(2024, 1, 15), "memory_pct", 88.1, "prod"),
    ("SRV-003", date(2024, 1, 15), "cpu_pct",    23.0, "dev"),
]

df = spark.createDataFrame(data, schema=monitoring_schema)
print("Schema:")
df.printSchema()
print("\\nRow count:", df.count())  # action — triggers execution
df.show()'''),

code('c04', '''from pyspark.sql import functions as F

# ══════════════════════════════════════
# CORE OPERATIONS: filter, select, withColumn, groupBy
# ══════════════════════════════════════

# Read monitoring data (in prod: from S3 Parquet)
# df = spark.read.parquet("s3://citi-data/monitoring/date=2024-01-15/")

# ── Transformations (lazy) ────────────────────────────────────────────────────

# Filter to production CPU readings
prod_cpu = df.filter(
    (F.col("environment") == "prod") &
    (F.col("metric_type") == "cpu_pct")
)

# Add alert column using F.when (NOT a Python UDF)
with_alerts = prod_cpu.withColumn(
    "alert_level",
    F.when(F.col("metric_value") >= 90, "CRITICAL")
     .when(F.col("metric_value") >= 75, "WARNING")
     .when(F.col("metric_value") >= 60, "MONITOR")
     .otherwise("OK")
)

# Aggregations
summary = with_alerts.groupBy("server_id", "alert_level") \
    .agg(
        F.avg("metric_value").alias("avg_cpu"),
        F.max("metric_value").alias("peak_cpu"),
        F.count("*").alias("reading_count")
    ) \
    .orderBy(F.col("avg_cpu").desc())

# ── Action: show results ───────────────────────────────────────────────────────
summary.show()

# ── Action: write to Parquet (production output) ───────────────────────────────
# summary.write \
#     .mode("overwrite") \
#     .partitionBy("alert_level") \
#     .parquet("s3://citi-data/capacity-summary/date=2024-01-15/")'''),

code('c05', '''from pyspark.sql import functions as F

# ══════════════════════════════════════
# ❌ ANTI-PATTERN vs ✅ PATTERN: Python UDFs
# ══════════════════════════════════════

# ❌ ANTI-PATTERN: Python UDF — crosses JVM boundary for EVERY row
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

@udf(returnType=StringType())
def classify_cpu_python_udf(cpu_value):
    """This serializes EVERY row to Python and back — 10x slower."""
    if cpu_value is None:
        return "UNKNOWN"
    if cpu_value >= 90:
        return "CRITICAL"
    elif cpu_value >= 75:
        return "WARNING"
    elif cpu_value >= 60:
        return "MONITOR"
    return "OK"

# Slow: 45 minutes for 6M rows (JVM→Python→JVM for each row)
# df.withColumn("alert", classify_cpu_python_udf(F.col("metric_value")))

# ✅ PATTERN: Built-in F.when — stays inside the JVM, runs in C++
fast_classify = df.withColumn(
    "alert",
    F.when(F.col("metric_value").isNull(), "UNKNOWN")
     .when(F.col("metric_value") >= 90, "CRITICAL")
     .when(F.col("metric_value") >= 75, "WARNING")
     .when(F.col("metric_value") >= 60, "MONITOR")
     .otherwise("OK")
)

# Fast: 4 minutes for 6M rows (no serialization overhead)
fast_classify.show()

print("Key Rule: If you can express logic with F.when/F.col/F.expr, NEVER use a Python UDF")
print("Use Python UDFs ONLY for logic that has no equivalent built-in function")'''),

code('c06', '''from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ══════════════════════════════════════
# WINDOW FUNCTIONS in PySpark
# (Same concepts as SQL window functions)
# ══════════════════════════════════════

# Define window: for each server, ordered by date
server_window = Window.partitionBy("server_id").orderBy("collected_at")
server_30day_window = Window.partitionBy("server_id") \
    .orderBy("collected_at") \
    .rowsBetween(-29, 0)  # last 30 rows

# Add window function columns
df_with_windows = df.filter(F.col("metric_type") == "cpu_pct") \
    .withColumn("prev_day_cpu",
        F.lag("metric_value", 1).over(server_window)) \
    .withColumn("rolling_30day_avg",
        F.avg("metric_value").over(server_30day_window)) \
    .withColumn("deviation_from_baseline",
        F.col("metric_value") - F.col("rolling_30day_avg")) \
    .withColumn("rank_in_fleet",
        F.rank().over(Window.orderBy(F.col("metric_value").desc())))

df_with_windows.select(
    "server_id", "collected_at", "metric_value",
    "rolling_30day_avg", "deviation_from_baseline", "rank_in_fleet"
).show()

# ── Joins ───────────────────────────────────────────────────────────────────
# Broadcast join: when one table is small (< 200MB), broadcast to all executors
dim_server_df = spark.createDataFrame(
    [("SRV-001", "Team-Alpha"), ("SRV-002", "Team-Beta"), ("SRV-003", "Team-Dev")],
    ["server_id", "team"]
)

# Broadcast hint avoids shuffle for the small table
joined = df.join(F.broadcast(dim_server_df), on="server_id", how="left")
joined.show()'''),

md('c07', '''## 🎤 5 Interview Q&A

**Q1: What is the difference between a transformation and an action in PySpark?**
Transformations are lazy — they build a DAG but don\'t execute: `.filter()`, `.select()`, `.groupBy()`, `.join()`.
Actions trigger execution and return results: `.count()`, `.collect()`, `.show()`, `.write()`.
Spark\'s optimizer (Catalyst) sees the entire DAG before execution, enabling optimizations like
predicate pushdown (filter before join), projection pruning (only read needed columns), and
broadcast join selection.

---

**Q2: Why are Python UDFs slow in PySpark?**
PySpark runs on the JVM. Python UDFs require serializing each row from JVM memory → Python process,
executing the function, then deserializing the result back to JVM — for EVERY row.
On 6M rows, this is 6M serialization round-trips. Built-in F. functions (F.when, F.col, F.expr)
run natively in the JVM as optimized C++/Scala — no serialization. The speedup is typically 5-20x.
Use Python UDFs only when no built-in equivalent exists.

---

**Q3: What is a broadcast join and when should you use it?**
A broadcast join sends the entire small table to every executor, avoiding a shuffle.
Without a broadcast join, both tables are shuffled by the join key — expensive for large tables.
With `F.broadcast(small_df)`, the small table fits in memory on each executor and the large table
is processed locally. Use when one side is < 200MB (configurable via `spark.sql.autoBroadcastJoinThreshold`).
At Citi: dim_server (6,000 rows) vs fact_monitoring (500M rows) — always broadcast dim_server.

---

**Q4: What is the difference between `.cache()` and `.persist()`?**
Both store a DataFrame in memory for reuse. `.cache()` = `.persist(StorageLevel.MEMORY_AND_DISK)`.
`.persist()` lets you specify the storage level: MEMORY_ONLY (fastest), DISK_ONLY (slowest, largest),
MEMORY_AND_DISK (default — spills to disk if memory is full).
Use `.cache()` when you\'ll reuse a DataFrame multiple times in the same job (e.g., used in two
different branches of a pipeline). Unpersist when done: `df.unpersist()`.

---

**Q5: What is a shuffle and how do you minimize it?**
A shuffle redistributes data across the cluster so that records with the same key end up on the
same executor — required for `groupBy`, `join`, and `orderBy`. Shuffles involve writing data to
disk and transferring over the network — the most expensive Spark operation.
Minimize with: (1) filter early to reduce data before shuffle, (2) use broadcast joins for small tables,
(3) set `spark.sql.shuffle.partitions` to match data size (default 200 is often wrong), (4) avoid
unnecessary `orderBy` — use `sortWithinPartitions` if only local sort is needed.'''),

md('c08', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **RDD** | Resilient Distributed Dataset — original Spark abstraction. Low-level, avoid in favor of DataFrame API |
| **DataFrame** | Distributed table with named columns and schema — the standard PySpark API |
| **Transformation** | Lazy operation that returns a new DataFrame — builds the DAG |
| **Action** | Triggers execution and returns results — count, collect, show, write |
| **DAG** | Directed Acyclic Graph — Spark\'s execution plan, optimized before running |
| **Catalyst Optimizer** | Spark\'s query optimizer — rewrites the DAG for efficiency (predicate pushdown, etc.) |
| **Shuffle** | Redistributing data across executors by key — expensive network + disk operation |
| **Broadcast Join** | Send small table to all executors to avoid shuffle — use when one side < 200MB |
| **Partition** | A chunk of data processed by one executor — default 200 after shuffle |
| **Python UDF** | User-defined function in Python — crosses JVM boundary, 5-20x slower than F. functions |
| **Predicate Pushdown** | Applying filters as early as possible (even in the file reader) — reduces data scanned |
| **Lazy Evaluation** | Transformations are not executed until an action is called — enables optimization |'''),

md('c09', '''## 💼 The Citi Narrative

**Context:** Daily capacity aggregation ETL — processes monitoring data for 6,000 servers,
calculates rolling averages, flags at-risk servers. Data volume: 50GB+ per day.

**The Problem:** Pipeline was taking 45 minutes, blocking the capacity team\'s 07:00 standup.
Performance profiling (Spark UI) showed 90% of time in one stage: the alert classification step.
Root cause: Python UDF for alert level classification.

**The UDF Problem:**
```python
@udf(returnType=StringType())
def classify(cpu):
    if cpu >= 90: return "CRITICAL"
    ...
```
6M rows × 1 serialization round-trip each = the bottleneck.

**The Fix — 2 Lines Changed:**
```python
# Before: Python UDF (45 min)
df.withColumn("alert", classify(F.col("metric_value")))

# After: F.when chain (4 min)
df.withColumn("alert", F.when(F.col("metric_value") >= 90, "CRITICAL").when(...).otherwise("OK"))
```

**Result:** 45 minutes → 4 minutes. No algorithm change. No infrastructure change.
The Spark UI showed the shuffle stage dropped from 40 minutes to 3 minutes.

**Interview Line:** *"The Spark UI showed one red stage taking 40 minutes. It was the UDF.
The function was in Python — Spark was serializing 6M rows from JVM to Python and back.
Replacing it with F.when took 5 minutes to write. The pipeline went from 45 to 4 minutes.
The lesson: check the Spark UI before optimizing anything."*'''),

code('c10', '''# Practice: Rewrite these Python UDFs using F. functions

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, DoubleType

# ── PRACTICE 1: Categorize utilization ────────────────────────────────────────
# ❌ Python UDF (slow):
@udf(returnType=StringType())
def categorize_udf(value):
    if value is None: return None
    if value >= 90: return "CRITICAL"
    if value >= 70: return "HIGH"
    if value >= 50: return "MEDIUM"
    return "LOW"

# ✅ Write the F.when equivalent:
categorize_fwhen = None  # your answer

# ── PRACTICE 2: Apply a 10% headroom adjustment ────────────────────────────────
# ❌ Python UDF (slow):
@udf(returnType=DoubleType())
def add_headroom_udf(value):
    if value is None: return None
    return round(value * 1.10, 2)

# ✅ Write the F.col equivalent (one expression):
add_headroom_fwhen = None  # your answer

# ── Solutions ───────────────────────────────────────────────────────────────
categorize_fwhen = (
    F.when(F.col("metric_value").isNull(), None)
     .when(F.col("metric_value") >= 90, "CRITICAL")
     .when(F.col("metric_value") >= 70, "HIGH")
     .when(F.col("metric_value") >= 50, "MEDIUM")
     .otherwise("LOW")
)

add_headroom_fwhen = F.round(F.col("metric_value") * 1.10, 2)

print("Practice 1 solution: F.when chain (runs in JVM, no serialization)")
print("Practice 2 solution: F.round(F.col(...) * 1.10, 2)")
print("Key: ANY time you write a UDF, ask: can F.when/F.expr/F.col do this?")'''),

md('c11', '''## 🎯 Summary

### The Core Rules
1. **Transformations are lazy** — nothing runs until an action
2. **Never use Python UDFs when F. functions exist** — 5-20x slower
3. **Broadcast small tables** in joins — avoids expensive shuffles
4. **Filter early** — reduce data before groupBy/join operations
5. **Check Spark UI** — before optimizing, find the red stage

### Common Operations Cheatsheet
| Task | PySpark |
|------|---------|
| Filter rows | `.filter(F.col("env") == "prod")` |
| Add column | `.withColumn("alert", F.when(...))` |
| Aggregate | `.groupBy("server").agg(F.avg("cpu"))` |
| Join | `.join(F.broadcast(small_df), on="id")` |
| Window function | `.withColumn("lag", F.lag("cpu").over(w))` |
| Write output | `.write.mode("overwrite").parquet("s3://...")` |

### Interview Confidence Checklist
- [ ] Can explain transformation vs action with examples
- [ ] Can explain why Python UDFs are slow and how to avoid them
- [ ] Can write F.when chain to replace a Python UDF
- [ ] Can explain broadcast join and when to use it
- [ ] Can name the Citi narrative: 45 min → 4 min by removing Python UDF

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 6-D: System Design — Data Platform
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_DESIGN_DATA_PLATFORM = [
md('c01', '''# Technology — System Design: Design a Data Platform
---

<div style="padding:15px;border-left:8px solid #a18cd1;background:#f5f0ff;border-radius:4px;">
<strong>Core Insight:</strong> This is Sean\'s actual Citi architecture. The design exists.
Kafka → Flink/Spark Streaming → S3 Parquet → Glue → Athena → Grafana.
Know every trade-off: Athena (serverless, pay-per-query) vs Redshift (provisioned, fast BI).
Own this design — you built it.
</div>

### The Architecture Overview
```
[APM Agents]
     │  (metrics, logs, traces)
     ▼
 [Kafka]          ← message bus, replay buffer, decoupling
     │
     ├──► [Flink Streaming]   ← real-time alerting (< 30s latency)
     │         │
     │         └──► [Alert DB / PagerDuty]
     │
     └──► [Spark Batch ETL]   ← hourly/daily aggregations
               │
               └──► [S3 Parquet] ← data lake (partitioned by date/env)
                         │
                         └──► [Glue Catalog] ← metadata layer
                                   │
                                   ├──► [Athena]    ← ad-hoc SQL queries
                                   └──► [Grafana]   ← dashboards
```'''),

md('c02', '''## 🏗️ Layer-by-Layer: What Each Component Does

| Layer | Component | Role | Why this choice |
|-------|-----------|------|----------------|
| **Ingestion** | Kafka | Message bus, replay buffer | Decouples producers from consumers; replay on failure |
| **Real-time** | Flink | Stream processing | Sub-second latency; stateful windows for anomaly detection |
| **Batch** | Spark | Large-scale ETL | Process 50GB/day efficiently; familiar to the team |
| **Storage** | S3 Parquet | Data lake | Cheap ($0.023/GB/month), columnar for analytics, durable |
| **Catalog** | AWS Glue | Metadata + schema | Athena and Spark read the same schema — one source of truth |
| **Query** | Athena | Ad-hoc SQL | Serverless, $5/TB scanned, no cluster to manage |
| **BI** | Redshift | Complex reports | Provisioned cluster, faster for repeated BI workloads |
| **Viz** | Grafana | Dashboards | Connects to Athena, Prometheus, Elasticsearch |

### The Two Query Paths
- **Ad-hoc / exploratory:** Athena → pay per query, no setup, slow for complex aggregations
- **Repeated / complex BI:** Redshift → faster, predictable cost, needs cluster management'''),

md('c03', '''## ⚖️ Key Design Trade-offs

### 1. Kafka vs Direct S3 Ingest
| Kafka | Direct S3 |
|-------|-----------|
| Replay capability — reprocess if consumer fails | No replay — data lost if consumer fails |
| Decouples producers (APM agents) from consumers (Spark) | Tight coupling |
| Adds operational complexity (Kafka cluster management) | Simple push to S3 |
| **Choose Kafka** when: consumers can fail and replay is critical | **Choose Direct S3** when: data is already durable and loss is acceptable |

**Citi decision:** Kafka, because APM agents can\'t buffer locally — if the Spark job fails at 2am,
Kafka holds the last 7 days of metrics and Spark replays from the last checkpoint.

### 2. Athena vs Redshift
| Athena | Redshift |
|--------|----------|
| Serverless — no cluster to manage | Provisioned — cluster cost even when idle |
| $5/TB scanned — expensive for repeated large queries | Fixed cost — predictable for heavy BI |
| Slow for complex aggregations across large data | Fast for complex BI queries (columnar + indexes) |
| **Choose Athena** for: ad-hoc exploration, infrequent queries | **Choose Redshift** for: repeated BI dashboards, complex joins |

**Citi decision:** Athena for ad-hoc capacity queries ($5/TB is fine for monthly reports).
Redshift would be overkill — only the capacity team and two analysts use it.

### 3. Lambda vs Kappa Architecture
| Lambda | Kappa |
|--------|-------|
| Two paths: batch + stream processed separately | Single path: stream only, reprocess by replaying |
| Complex: maintain two codebases | Simpler: one codebase |
| Batch is authoritative, stream is approximate | Stream is authoritative |
| **Citi uses Lambda:** batch Spark for historical accuracy, Flink for real-time alerting |'''),

md('c04', '''## 🎤 Interview Framework: "Design a Monitoring Data Platform"

### The 5-Step Answer Structure

**Step 1: Clarify requirements (2 minutes)**
- How many data sources? (6,000 servers → 50GB/day)
- Latency requirements? (real-time alerting < 30s, reports = next-day OK)
- Query patterns? (ad-hoc exploration vs repeated BI dashboards)
- Budget constraints? (serverless preferred for unpredictable workloads)
- Data retention? (90 days hot, 3 years cold → S3 lifecycle policy)

**Step 2: Identify the two query types**
- Real-time: anomaly detection, alerts (stream processing → Flink/Kafka Streams)
- Batch: trend analysis, capacity reports (batch → Spark → S3 → Athena)

**Step 3: Design the ingestion layer**
- APM agents → Kafka (replay buffer)
- Why Kafka: producers and consumers are decoupled; consumers can fail and replay

**Step 4: Design the storage layer**
- S3 Parquet, partitioned by `date=YYYY-MM-DD/env=prod/`
- Partition by date: monthly reports only scan 30 partitions of 365
- Glue Catalog: one schema definition, read by both Athena and Spark

**Step 5: Address scaling and failure modes**
- Kafka retention: 7 days — allows full replay of any week
- S3 lifecycle: 90-day hot (Parquet), then move to Glacier for cold storage
- Failure mode: if Spark job fails → restart from Kafka offset, not from S3
- Cost: Athena $5/TB × estimated monthly scan volume = projected monthly cost'''),

md('c05', '''## 📊 Data Partitioning Strategy

### Why Partitioning Matters
Without partitioning, every Athena query scans the entire dataset.
With date partitioning, a "last 7 days" query scans only 7 of 365 directories.

```
s3://citi-monitoring/
└── date=2024-01-15/
    └── env=prod/
        └── part-00000.parquet   (6,000 servers × 1,440 minutes = 8.6M rows/file)
└── date=2024-01-16/
    └── env=prod/
        └── part-00000.parquet
```

### The Partition Key Decision
| Partition by | Good for | Bad for |
|-------------|----------|---------|
| `date` only | Date range queries | Can\'t filter by env efficiently |
| `date` + `env` | Date + env filters | Too many small partitions if many envs |
| `env` + `date` | Env-first queries | Date queries scan all envs |

**Citi choice:** `date=YYYY-MM-DD/env={dev,staging,prod}/`
- Monthly reports filter by date → partition pruning works
- Env-specific debugging filters by env → second partition helps
- 3 environments = manageable partition count

### File Size Rule
Target: 128MB-512MB per Parquet file. Too small: too many S3 API calls. Too large: can\'t parallelize.
Command: `spark.coalesce(4)` before writing → 4 files per partition.'''),

md('c06', '''## 🎤 5 Interview Q&A

**Q1: Why use Kafka instead of writing directly to S3?**
Kafka provides a replay buffer. If the Spark job fails at 2am, it can restart and read
from its last committed Kafka offset — reprocessing only the missed data.
With direct S3 writes, if the APM agent crashes mid-write, data is lost.
Kafka also decouples producers from consumers: APM agents don\'t need to know about Spark;
they just publish to a topic. New consumers (Flink for real-time alerts) can be added
without changing the agents.

---

**Q2: What is the difference between Athena and Redshift and when do you choose each?**
Athena: serverless, queries S3 directly, pay per TB scanned ($5/TB). No cluster to manage.
Best for: ad-hoc exploration, infrequent queries, teams that can\'t afford idle cluster cost.
Redshift: provisioned cluster, much faster for complex multi-table BI queries, fixed cost.
Best for: daily BI dashboards with complex aggregations, teams running 100+ queries/day.
Rule: if query frequency × cost per query > cluster monthly cost → use Redshift.

---

**Q3: What is the Lambda architecture and what are its trade-offs?**
Lambda has two processing paths: batch (slow, accurate, historical) and stream (fast, approximate, real-time).
Results from both are merged in a serving layer. Trade-off: you maintain two codebases for the same logic.
The Kappa architecture simplifies this by using only streaming — historical reprocessing = replaying Kafka.
Citi uses Lambda because: (1) batch Spark produces authoritative numbers for regulatory reporting,
(2) Flink provides real-time alerts that can be slightly approximate, (3) team had both Spark and
stream processing expertise.

---

**Q4: How do you handle schema evolution in a data lake?**
Schema evolution means adding/removing/changing columns over time.
Parquet supports column addition: new files can have extra columns; old files return NULL for new columns.
Glue Catalog tracks schema versions — Athena reads the current schema and handles nulls for old files.
Dangerous changes: renaming or removing columns breaks backward compatibility.
Strategy: (1) only ADD columns (never remove), (2) version your schema: `v1/`, `v2/`, (3) use
Glue Schema Registry for enforcing Avro/Protobuf schemas at ingestion time.

---

**Q5: How do you optimize Athena query costs?**
Athena charges per TB scanned. Reduce cost with:
(1) Parquet format — columnar, only reads requested columns (vs CSV which reads all columns)
(2) Partition pruning — `WHERE date = \'2024-01-15\'` reads only that day\'s partition
(3) Compression — Parquet + Snappy reduces file size by ~75% vs raw CSV
(4) Partition projection — register partitions in Glue to avoid full metadata scans
(5) SELECT only needed columns — columnar format skips unselected columns entirely
Rule of thumb: same query on Parquet vs CSV = 10-20x cost reduction.'''),

md('c07', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Data Lake** | S3 storage of raw + processed data in open formats (Parquet, ORC) — cheap, scalable |
| **Data Warehouse** | Optimized for SQL analytics — Redshift, Snowflake, BigQuery. Faster for BI, higher cost |
| **Lambda Architecture** | Two-path processing: batch (accurate, slow) + stream (fast, approximate) |
| **Kappa Architecture** | Single stream path — replay Kafka for reprocessing. Simpler, requires fast stream |
| **Kafka Offset** | Position in a Kafka topic partition — consumers commit their offset to resume after failure |
| **Partition Pruning** | Athena/Spark skips S3 directories that don\'t match the WHERE clause partition key |
| **Parquet** | Columnar storage format — reads only needed columns, high compression, fast for analytics |
| **AWS Glue** | Managed ETL service + data catalog (schema registry for S3 data) |
| **Athena** | Serverless SQL on S3 — pay per TB scanned ($5/TB), no cluster management |
| **Redshift** | AWS data warehouse — fast for complex BI, provisioned cluster |
| **Flink** | Stream processing framework — low-latency stateful computation, exactly-once semantics |
| **Schema Evolution** | Adding/changing columns over time — Parquet + Glue handle column additions gracefully |'''),

md('c08', '''## 💼 The Citi Narrative

**Context:** Citi monitoring data was siloed — CA APM for some apps, AppDynamics for others,
no unified platform for cross-application capacity analysis.

**The Problem:** Generating a monthly capacity report required manually extracting data from
4 APM tools, joining in Excel, and building charts. This took 2-3 analysts a full day.

**The Architecture Designed:**
- Kafka: unified ingestion bus — each APM tool\'s agent published to a topic
- Spark Streaming: hourly ETL → S3 Parquet, partitioned by date/env
- Glue Catalog: single schema across all tables
- Athena: ad-hoc capacity queries (SQL, no cluster to maintain)
- Grafana: dashboards reading from Athena via the Athena-Grafana plugin

**Key Trade-off Made:** Chose Athena over Redshift. Volume was ~50GB/day → monthly query
cost = ~$15 (3TB/month × $5/TB). Redshift cluster would cost $180+/month. For 2-3 analysts
running monthly reports, Athena was 10x cheaper.

**Result:**
- Monthly capacity report: 2 hours (from 2 analyst-days)
- Ad-hoc queries: available to anyone with Athena access, no request queue
- New APM tool onboarding: add a Kafka producer → zero changes to the query/dashboard layer

**Interview Line:** *"We replaced 4 separate APM reporting processes with one platform.
The key architectural decision was Kafka for ingestion — it meant we could add or remove
APM tools without touching the downstream pipeline. The capacity report went from 2 days to 2 hours."*'''),

md('c09', '''## 🎯 Summary

### The Architecture (Memorize This)
```
APM Agents → Kafka → Spark/Flink → S3 Parquet → Glue → Athena/Redshift → Grafana
```

### The Five Trade-offs (Always Discuss These)
1. **Kafka vs Direct S3:** Replay capability vs simplicity — choose Kafka when consumers fail
2. **Athena vs Redshift:** Serverless pay-per-query vs provisioned fast BI — use Athena for ad-hoc
3. **Lambda vs Kappa:** Two codebases vs one — Lambda when batch accuracy matters for regulatory data
4. **Date partition vs no partition:** 10-50x cost reduction on Athena — always partition by date
5. **Parquet vs CSV:** 10-20x Athena cost reduction — always use Parquet + Snappy

### The Numbers (Know These)
- S3: $0.023/GB/month
- Athena: $5/TB scanned
- Parquet compression: ~75% vs CSV
- Citi monthly query cost: ~$15 (vs $180+/month for Redshift)
- Report time: 2 hours (down from 2 analyst-days)

### Interview Confidence Checklist
- [ ] Can draw the full architecture from memory (Kafka → S3 → Athena)
- [ ] Can explain Athena vs Redshift trade-off with real numbers
- [ ] Can explain why Kafka instead of direct S3
- [ ] Can explain partition pruning and why it matters for cost
- [ ] Can name the Citi narrative: 4 APM tools → 1 platform, report time 2 days → 2 hours

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# Write all notebooks
# ─────────────────────────────────────────────────────────────────────────────

print("=== Day 5 Concept Notebooks ===")
write_nb(f'{BASE}/Day5/sql-analytical.ipynb', SQL_ANALYTICAL)
write_nb(f'{BASE}/Day5/python-etl-patterns.ipynb', ETL_PATTERNS)
write_nb(f'{BASE}/Day5/capacity-planning.ipynb', CAPACITY_PLANNING)

print("\n=== Day 6 Concept Notebooks ===")
write_nb(f'{BASE}/Day6/sql-schema-design.ipynb', SQL_SCHEMA_DESIGN)
write_nb(f'{BASE}/Day6/python-pyspark.ipynb', PYSPARK)
write_nb(f'{BASE}/Day6/system-design-data-platform.ipynb', SYSTEM_DESIGN_DATA_PLATFORM)

print("\nAll 6 concept notebooks written successfully!")
