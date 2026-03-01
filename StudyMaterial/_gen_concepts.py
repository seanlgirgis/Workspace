"""
Concept notebook generator for Days 4, 5, 6.
Writes 9 .ipynb files — SQL, Python, and Tech notebooks for each day.
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/Workspace/StudyMaterial'


def nb(cells_list):
    """Wrap cells in a valid .ipynb structure."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
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
# DAY 4-B: SQL Query Optimization
# ─────────────────────────────────────────────────────────────────────────────

SQL_QUERY_OPT = [
md('c01', '''# SQL Query Optimization
---

<div style="padding:15px;border-left:8px solid #f093fb;background:#fdf0ff;border-radius:4px;">
<strong>Core Insight:</strong> Query optimization separates analysts from engineers.
Know EXPLAIN output, why indexes matter, and how the planner decides between
nested loop, hash join, and merge join. A single missing index can turn a 0.3-second
query into a 45-second table scan.
</div>

### Why It Matters
Slow queries in production cause SLA breaches. At Citi, a poorly indexed telemetry
query scanned 500M rows — taking 45 seconds. After adding a composite index and
enabling partition pruning: **0.3 seconds**.'''),

md('c02', '''## 🧠 Three Mental Models for Query Optimization

| Model | The Insight |
|-------|------------|
| **The Librarian** | An index is like a book's index — you jump to the page directly instead of reading every page |
| **The Join Planner** | The query planner estimates row counts and chooses: Nested Loop (small tables), Hash Join (large unsorted), Merge Join (pre-sorted) |
| **The Partition Pruner** | Partitioning by date means a query for "last 7 days" only reads 7 of 365 partitions — 98% skip |

**The Golden Rule:** Optimize for cardinality. High-cardinality columns (user_id, timestamp) make
excellent index leading columns. Low-cardinality (status, boolean) do not.'''),

code('c03', '''-- EXPLAIN: Read the query plan before optimizing anything
-- PostgreSQL syntax (similar in most databases)

-- Step 1: Get the raw plan (no execution)
EXPLAIN
SELECT s.server_name, m.metric_value, m.collected_at
FROM fact_monitoring m
JOIN dim_server s ON m.server_id = s.server_id
WHERE m.collected_at >= '2024-01-01'
  AND m.metric_type = 'cpu_pct'
ORDER BY m.collected_at DESC;

-- Step 2: Actually run it and get real timings
EXPLAIN ANALYZE
SELECT s.server_name, m.metric_value, m.collected_at
FROM fact_monitoring m
JOIN dim_server s ON m.server_id = s.server_id
WHERE m.collected_at >= '2024-01-01'
  AND m.metric_type = 'cpu_pct'
ORDER BY m.collected_at DESC;

-- What to look for in the output:
-- "Seq Scan" = reading every row (BAD for large tables)
-- "Index Scan" = using an index (GOOD)
-- "Hash Join" = building a hash table of smaller side (GOOD for large joins)
-- "rows=X" vs "actual rows=Y" -- big mismatch = stale statistics (run ANALYZE)'''),

md('c04', '''## 📊 Index Types and When to Use Them

| Index Type | When to Use | Example |
|-----------|------------|---------|
| **B-Tree (default)** | Range queries, equality, ORDER BY | `WHERE collected_at > '2024-01-01'` |
| **Hash** | Equality only, no range | `WHERE server_id = 42` (exact match) |
| **Composite** | Multi-column WHERE / ORDER BY | `WHERE env = 'prod' AND collected_at > ...` |
| **Covering** | Query only needs indexed columns | Avoid table heap access entirely |
| **Partial** | Filter on a subset of rows | `WHERE status = 'active'` (only index active rows) |

### Composite Index Column Order Rule
Put the **most selective** (highest cardinality) column FIRST.
The leading column is used for range scans; trailing columns narrow within matches.

```sql
-- Good: collected_at is high-cardinality (many distinct timestamps)
CREATE INDEX idx_monitoring_time_env ON fact_monitoring(collected_at, env);

-- Bad: env has 3 values (dev/staging/prod) — low cardinality leading column
CREATE INDEX idx_monitoring_env_time ON fact_monitoring(env, collected_at);
```'''),

code('c05', '''-- Index creation examples

-- Basic index on timestamp column
CREATE INDEX idx_monitoring_collected_at
ON fact_monitoring(collected_at);

-- Composite index: most selective column first
CREATE INDEX idx_monitoring_time_type
ON fact_monitoring(collected_at DESC, metric_type);

-- Covering index: include extra columns to avoid heap access
-- Query only needs these columns — index covers the full query
CREATE INDEX idx_monitoring_covering
ON fact_monitoring(server_id, collected_at DESC)
INCLUDE (metric_value, metric_type);

-- Partial index: only index active servers (assume 80% are decommissioned)
CREATE INDEX idx_server_active
ON dim_server(server_name, env)
WHERE is_active = TRUE;

-- BEFORE: Seq Scan on 500M rows = 45 seconds
-- AFTER:  Index Scan on 2M matching rows = 0.3 seconds

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE tablename = 'fact_monitoring'
ORDER BY idx_scan DESC;'''),

md('c06', '''## 🔗 Join Strategies: How the Planner Decides

### Nested Loop Join
- Best when: inner table is **small** or has an **index** on the join key
- Cost: O(outer_rows × inner_rows) — catastrophic for large tables

### Hash Join
- Best when: one table fits in memory, no useful index
- Cost: O(n + m) — build hash table of smaller side, probe with larger side
- Forces a full scan of both tables

### Merge Join
- Best when: **both sides are pre-sorted** on the join key
- Cost: O(n log n + m log m) — efficient when data already sorted

```sql
-- Force a specific join type for testing (PostgreSQL):
SET enable_hashjoin = OFF;   -- force merge or nested loop
SET enable_mergejoin = OFF;  -- force hash or nested loop

-- Check what plan was chosen:
EXPLAIN ANALYZE
SELECT * FROM fact_monitoring m
JOIN dim_server s ON m.server_id = s.server_id;
```'''),

code('c07', '''-- Query optimization in practice: before and after

-- ══════════════════════════════════════════════
-- SCENARIO: Monthly capacity report for active servers
-- Table: fact_monitoring (500M rows), partitioned by month
-- ══════════════════════════════════════════════

-- BEFORE: 45 seconds, Seq Scan
SELECT
    s.server_name,
    s.environment,
    AVG(m.metric_value) AS avg_cpu,
    MAX(m.metric_value) AS peak_cpu
FROM fact_monitoring m
JOIN dim_server s ON m.server_id = s.server_id
WHERE m.metric_type = 'cpu_pct'
  AND m.collected_at BETWEEN '2024-01-01' AND '2024-01-31'
  AND s.is_active = TRUE
GROUP BY s.server_name, s.environment
HAVING AVG(m.metric_value) > 70
ORDER BY avg_cpu DESC;

-- Optimization steps applied:
-- 1. Add composite index: (collected_at, metric_type, server_id)
-- 2. Add partial index on dim_server where is_active = TRUE
-- 3. Partition fact_monitoring by month → January partition only
-- 4. Add covering index to include metric_value

-- AFTER: 0.3 seconds, Index Scan + Partition Pruning
-- Same query, same result — different execution plan

-- Verify partition pruning happened:
EXPLAIN SELECT * FROM fact_monitoring
WHERE collected_at BETWEEN '2024-01-01' AND '2024-01-31';
-- Look for: "Partitions: fact_monitoring_2024_01"
-- NOT: scanning all partitions'''),

md('c08', '''## 🎤 5 Interview Q&A

**Q1: What does EXPLAIN ANALYZE tell you that EXPLAIN alone doesn\'t?**
EXPLAIN shows the *estimated* plan — what the planner thinks will happen.
EXPLAIN ANALYZE actually *executes* the query and shows real row counts and timings.
The gap between estimated and actual rows reveals stale statistics — fix with `ANALYZE table_name`.

---

**Q2: When would you NOT add an index?**
(1) Tables with < 10K rows — sequential scan is faster than index overhead.
(2) Columns with low cardinality (boolean, 3-value status) — the index doesn\'t narrow the search enough.
(3) Write-heavy tables — every INSERT/UPDATE/DELETE must update all indexes, slowing writes.
(4) Columns never used in WHERE/JOIN/ORDER BY clauses.

---

**Q3: What is a covering index and why does it matter?**
A covering index includes all columns the query needs — so the planner never touches the heap (main table).
Example: `CREATE INDEX idx ON orders(customer_id) INCLUDE (total, created_at)`.
A query selecting only those columns hits the index only — typically 2-5x faster than an index + heap lookup.

---

**Q4: What is partition pruning and when does it help?**
Partition pruning means the query planner skips partitions whose data cannot match the WHERE clause.
If `fact_monitoring` is partitioned by month and you query `WHERE collected_at >= '2024-01-01'`,
the planner reads only January\'s partition — not all 12. Most effective when queries have tight
date range filters, which is common in time-series data.

---

**Q5: What is cardinality and why does it affect index design?**
Cardinality = the number of distinct values in a column.
High cardinality (user_id: millions of distinct values) → index is very selective → each lookup eliminates most rows.
Low cardinality (status: \'active\'/\'inactive\') → index is not selective → the planner may prefer a full scan.
Rule: put high-cardinality columns first in composite indexes.'''),

md('c09', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Sequential Scan (Seq Scan)** | Reading every row in the table from disk — O(n), appropriate only for small tables or when most rows match |
| **Index Scan** | Using a B-tree index to jump to matching rows — O(log n + k) where k is result rows |
| **Hash Join** | Build a hash table of the smaller relation, probe with the larger — O(n+m) |
| **Nested Loop Join** | For each row in the outer table, scan the inner — O(n×m), good only with indexed inner |
| **Merge Join** | Sort both sides, merge — O(n log n + m log m), ideal when data already sorted |
| **Composite Index** | Index on multiple columns — column order matters: most selective first |
| **Covering Index** | Index that includes all columns the query needs — avoids heap access |
| **Partial Index** | Index on a filtered subset of rows — `CREATE INDEX ... WHERE status = \'active\'` |
| **Partition Pruning** | Query planner skips partitions that can\'t match the WHERE clause |
| **Cardinality** | Number of distinct values in a column — high cardinality → selective index |
| **EXPLAIN ANALYZE** | Run the query and show actual execution stats (rows, timing) vs estimated |
| **Statistics** | Row count / distribution estimates the planner uses — updated by `ANALYZE` |'''),

md('c10', '''## 💼 The Citi Narrative

**Context:** Citi APM telemetry database — `fact_monitoring` table with 500M rows,
storing CPU/memory/response time for 6,000 servers at 1-minute intervals.

**The Problem:** Monthly capacity report took 45 seconds. Analysts ran it during business hours.
Every run locked resources and frustrated the team.

**Root Cause (from EXPLAIN ANALYZE):**
- Sequential scan on `fact_monitoring` (500M rows) — no index on `collected_at`
- Hash Join with `dim_server` — 6,000 rows, small enough but still building a hash table
- Estimates wildly off: planner estimated 50K rows, actual was 2M rows → stale statistics

**The Fix — Three Changes:**
1. `CREATE INDEX idx_monitoring_time_type ON fact_monitoring(collected_at DESC, metric_type)` — composite index
2. `ANALYZE fact_monitoring` — refresh statistics so planner estimates correctly
3. Partition table by month — January query only reads January partition (8M rows, not 500M)

**Result:** 45 seconds → 0.3 seconds. The same query. Same data. Same result.
Analysts could now run the report on demand. Dashboard became interactive.

**Interview Line:** *"EXPLAIN ANALYZE told me the planner estimated 50K rows but was scanning 2M.
That mismatch was the first clue — stale statistics. The second clue was Seq Scan on a 500M row table.
Two changes: composite index and ANALYZE. Query went from 45 seconds to 0.3 seconds."*'''),

code('c11', '''# Practice: Write the SQL for these scenarios

# 1. Find the top 10 servers by average CPU over the last 7 days
# (Use window function + GROUP BY)

# 2. Find servers where CPU INCREASED by more than 20 percentage points
# between January 2024 and January 2025
# (Use self-join or LAG)

# 3. Design a composite index for this query:
# SELECT * FROM fact_monitoring
# WHERE server_id = 42 AND collected_at > NOW() - INTERVAL '30 days'
# ORDER BY collected_at DESC;
# Which columns go in the index, and in what order?

# Write your SQL here:
print("Query 1: Top 10 servers by average CPU (last 7 days)")
print("""
SELECT
    s.server_name,
    ROUND(AVG(m.metric_value), 2) AS avg_cpu
FROM fact_monitoring m
JOIN dim_server s ON m.server_id = s.server_id
WHERE m.metric_type = 'cpu_pct'
  AND m.collected_at >= NOW() - INTERVAL '7 days'
GROUP BY s.server_name
ORDER BY avg_cpu DESC
LIMIT 10;
""")

print("Index for Query 3:")
print("CREATE INDEX idx ON fact_monitoring(server_id, collected_at DESC);")
print("Reason: server_id first (equality filter), collected_at second (range + order)")'''),

md('c12', '''## 🎯 Summary

### The Pattern
Optimize queries by understanding the **execution plan**, not guessing.

### The Four Levers
1. **Indexes** — Direct the planner to rows without scanning the table
2. **Statistics** — `ANALYZE` keeps row count estimates accurate
3. **Partitioning** — Prune irrelevant data at the storage level
4. **Join order** — Small table as the probe side of hash joins

### When to Optimize
- Sequential scan on a table with > 100K rows in a production query
- Query planner estimates differ from actual by > 10x (stale stats)
- Query appears in the slow query log
- Report that used to run in < 1s now takes > 5s

### Interview Confidence Checklist
- [ ] Can read EXPLAIN output and identify Seq Scan vs Index Scan
- [ ] Can explain composite index column ordering rule
- [ ] Can describe Hash Join vs Nested Loop vs Merge Join
- [ ] Can name the Citi narrative: 45s → 0.3s via composite index + partition

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 4-C: NumPy & Vectorization
# ─────────────────────────────────────────────────────────────────────────────

NUMPY_VECTORIZATION = [
md('c01', '''# Python — NumPy & Vectorization
---

<div style="padding:15px;border-left:8px solid #f093fb;background:#fdf0ff;border-radius:4px;">
<strong>Core Insight:</strong> NumPy operations run in C. A Python loop over 1M elements
takes ~seconds. NumPy does the same in milliseconds. This is the difference between a
pipeline that finishes in 2 minutes vs 2 hours — without changing the algorithm.
</div>

### Why It Matters for Data Engineering
Capacity analysis often involves large matrices of metrics × timestamps × servers.
At Citi: 1,000 timestamps × 6,000 servers = 6M values processed daily.
Python loop: 180 seconds. NumPy vectorized: 1.2 seconds.'''),

md('c02', '''## 🧠 Mental Models

| Model | The Story |
|-------|-----------|
| **The Factory Floor** | Python loop = one worker doing one task at a time. NumPy = assembly line of specialized C workers doing the same operation on all items simultaneously. |
| **The Recipe** | Broadcasting is like saying "add 1 tablespoon of salt to every bowl" — you don\'t enumerate each bowl, you describe the operation once. |
| **The Type Contract** | NumPy arrays have a fixed dtype. All elements are the same type, stored contiguously in memory. Python lists are pointers to objects scattered in heap. |

**The Rule:** Any time you write `for i in range(len(arr)):` on a NumPy array, ask:
*"Is there a vectorized equivalent?"* Usually yes.'''),

code('c03', '''import numpy as np
import time

# ══════════════════════════════════════
# BENCHMARK: Python loop vs NumPy
# ══════════════════════════════════════

N = 1_000_000  # 1 million elements

# Python loop
data_list = list(range(N))
start = time.perf_counter()
result_loop = [x * 2.5 + 100 for x in data_list]
loop_time = time.perf_counter() - start

# NumPy vectorized
data_arr = np.arange(N, dtype=np.float64)
start = time.perf_counter()
result_np = data_arr * 2.5 + 100
np_time = time.perf_counter() - start

print(f"Python loop:     {loop_time*1000:.1f} ms")
print(f"NumPy vectorized:{np_time*1000:.1f} ms")
print(f"Speedup:         {loop_time/np_time:.0f}x")

# Memory layout
print(f"\nNumPy array dtype: {data_arr.dtype}")
print(f"Memory (bytes):    {data_arr.nbytes:,}")
print(f"Contiguous:        {data_arr.flags['C_CONTIGUOUS']}")'''),

md('c04', '''## 📐 Broadcasting: The Key to Efficient Array Operations

Broadcasting lets NumPy operate on arrays with different shapes without copying data.

**The Rules:**
1. If arrays have different numbers of dimensions, prepend 1s to the smaller shape
2. Dimensions must either match or one of them must be 1
3. Output shape is the max of each dimension

```
Shape (6000, 1000)  — servers × timestamps (2D)
Shape (1000,)       — per-timestamp baseline (1D → broadcast to (1, 1000))
Result: (6000, 1000) — subtract each server\'s reading from the baseline
```

This is the **core operation** for anomaly detection: compare each server\'s
reading to the average across all servers at each timestamp.'''),

code('c05', '''import numpy as np

# ══════════════════════════════════════
# CITI USE CASE: Capacity matrix analysis
# 6,000 servers × 1,000 timestamps = 6M values
# ══════════════════════════════════════

np.random.seed(42)
N_SERVERS = 6000
N_TIMESTAMPS = 1000

# Simulate CPU readings (percent utilization)
cpu_matrix = np.random.normal(loc=45, scale=15, size=(N_SERVERS, N_TIMESTAMPS))
cpu_matrix = np.clip(cpu_matrix, 0, 100)

# ── Vectorized Operations ──────────────────────────────────────────────────

# 1. Per-server statistics (axis=1 = across timestamps)
avg_cpu = cpu_matrix.mean(axis=1)          # shape: (6000,)
peak_cpu = cpu_matrix.max(axis=1)           # shape: (6000,)
p95_cpu = np.percentile(cpu_matrix, 95, axis=1)  # shape: (6000,)

# 2. Servers breaching 80% threshold (vectorized boolean mask)
THRESHOLD = 80.0
breaching_mask = avg_cpu > THRESHOLD        # shape: (6000,), dtype: bool
n_breaching = breaching_mask.sum()
breach_indices = np.where(breaching_mask)[0]

print(f"Servers analyzed:   {N_SERVERS:,}")
print(f"Timestamps:         {N_TIMESTAMPS:,}")
print(f"Total data points:  {cpu_matrix.size:,}")
print(f"Average CPU (fleet):{avg_cpu.mean():.1f}%")
print(f"Servers > 80% avg:  {n_breaching}")

# 3. Broadcasting: normalize each timestamp by fleet average
fleet_avg_per_ts = cpu_matrix.mean(axis=0)  # shape: (1000,) — per-timestamp average
# Subtract fleet average from each server (broadcasting: (6000,1000) - (1000,))
deviation = cpu_matrix - fleet_avg_per_ts   # shape: (6000, 1000)

# Servers consistently ABOVE fleet average (anomalies)
consistently_high = (deviation > 10).mean(axis=1) > 0.5  # True for > 50% of timestamps
print(f"Consistently above fleet average: {consistently_high.sum()}")'''),

code('c06', '''import numpy as np
import time

# ══════════════════════════════════════
# ANTI-PATTERN vs PATTERN
# ══════════════════════════════════════

matrix = np.random.rand(6000, 1000)

# ❌ ANTI-PATTERN: Python loop over NumPy array
start = time.perf_counter()
result_loop = []
for i in range(matrix.shape[0]):
    row_mean = 0
    for j in range(matrix.shape[1]):
        row_mean += matrix[i, j]
    result_loop.append(row_mean / matrix.shape[1])
loop_ms = (time.perf_counter() - start) * 1000

# ✅ PATTERN: Vectorized
start = time.perf_counter()
result_vec = matrix.mean(axis=1)
vec_ms = (time.perf_counter() - start) * 1000

print(f"Loop:      {loop_ms:.0f} ms")
print(f"Vectorized:{vec_ms:.2f} ms")
print(f"Speedup:   {loop_ms/vec_ms:.0f}x")
print(f"Results match: {np.allclose(result_loop, result_vec)}")

# Common vectorized patterns:
print("\nCommon NumPy patterns:")
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

print(f"Cumulative sum:   {np.cumsum(arr)}")             # rolling sum
print(f"Rolling diff:     {np.diff(arr)}")               # day-over-day change
print(f"Percentile 95:    {np.percentile(arr, 95)}")     # SLA threshold
print(f"Boolean where:    {arr[arr > 4]}")               # filter values > 4
print(f"Clip to 0-5:      {np.clip(arr, 0, 5)}")        # cap values'''),

md('c07', '''## 🎤 5 Interview Q&A

**Q1: Why is NumPy so much faster than a Python loop?**
NumPy\'s array operations are implemented in C and Fortran. When you call
`arr * 2.5`, C code iterates over a contiguous block of memory — no Python
interpreter overhead, no object boxing/unboxing, no pointer chasing through
Python\'s heap. The speedup is typically 10-200x for arithmetic operations.

---

**Q2: What is broadcasting and when does it fail?**
Broadcasting is NumPy\'s rule for operating on arrays with different shapes.
Arrays are compatible if their dimensions are equal or one of them is 1 (from
the trailing dimension). It fails with `ValueError: operands could not be broadcast`
when shapes are incompatible — e.g., `(100, 3)` and `(4,)` — 3 ≠ 4 and neither is 1.
Fix by reshaping: `arr.reshape(-1, 1)` adds a trailing dimension of 1.

---

**Q3: When would you use pandas vs NumPy?**
NumPy for pure numeric array math — lowest overhead, maximum speed.
pandas for labeled data with mixed types, SQL-style group/join/pivot, time series
with DatetimeIndex. Rule of thumb: if your operation is "apply this math to every
row" and data is numeric → NumPy. If your operation involves groupby, merge, or
column names → pandas (which uses NumPy internally).

---

**Q4: What is the difference between `.copy()` and a view?**
NumPy operations often return **views** (slices, reshapes) — they share memory
with the original. Modifying a view modifies the original. `arr.copy()` creates
a new allocation. Use `.copy()` when you need to modify a subset without affecting
the source. Check with `arr.base is None` — True means it\'s the owner, not a view.

---

**Q5: What is vectorization in the context of pandas?**
pandas supports vectorized operations through `.apply()` (row-wise Python, slow),
`.map()` (element-wise), and direct column arithmetic (e.g., `df[\'a\'] + df[\'b\']`).
The fastest path is always direct column math — pandas delegates to NumPy.
`.apply()` with a Python lambda is effectively a loop — avoid for performance.'''),

md('c08', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Vectorization** | Applying an operation to an entire array at once in compiled C/Fortran code — no Python interpreter loop |
| **Broadcasting** | NumPy\'s rules for operating on arrays with different (but compatible) shapes without copying data |
| **dtype** | The data type of all elements in a NumPy array — `float64`, `int32`, `bool`, etc. Determines memory per element |
| **Contiguous Memory** | Elements stored in adjacent memory locations — enables SIMD CPU instructions and cache efficiency |
| **View vs Copy** | View shares memory with original; copy is independent. Slices return views; `.copy()` forces a copy |
| **axis** | The dimension along which an operation reduces. `axis=0` = across rows (per column). `axis=1` = across columns (per row) |
| **Boolean Mask** | A bool array used to select elements — `arr[arr > 5]` selects all elements > 5 |
| **np.where** | `np.where(condition, x, y)` — element-wise: x where condition is True, y where False |
| **SIMD** | Single Instruction Multiple Data — CPU feature that applies one instruction to multiple data elements simultaneously |'''),

md('c09', '''## 💼 The Citi Narrative

**Context:** Daily capacity analysis — 6,000 servers × 1,000 timestamps = 6M data points,
run every morning at 06:00 for the infrastructure team.

**The Problem:** Python loop implementation processed the 6M-cell matrix in ~180 seconds.
The daily batch window was 10 minutes. The capacity analysis was the bottleneck.

**The Fix:** Rewrote matrix operations using NumPy:
- Row means: `cpu_matrix.mean(axis=1)` instead of `for server in servers: sum/count`
- Threshold breaches: `(avg_cpu > 80).sum()` instead of `for x in avgs: if x > 80`
- Fleet deviation: broadcasting `cpu_matrix - fleet_avg` instead of nested loops

**Result:** 180 seconds → 1.2 seconds. 150x speedup. Zero algorithm change.
The capacity analysis went from a nightly batch to a real-time interactive query —
analysts could now ask "which servers are trending toward breach?" during standup.

**Interview Line:** *"The algorithm was correct — it was the implementation that was wrong.
Python loops over 6M NumPy elements are essentially calling the Python interpreter
6 million times. Replacing with vectorized operations cut runtime from 180 seconds to 1.2 seconds.
Same math. Different execution model."*'''),

code('c10', '''# Practice: Rewrite these Python loops using NumPy vectorization

import numpy as np

# Setup
np.random.seed(0)
readings = np.random.uniform(20, 95, size=(500, 24))  # 500 servers, 24 hours

# ── PRACTICE 1 ──────────────────────────────────────────────────────────────
# Loop version (SLOW):
daily_avg_loop = []
for i in range(readings.shape[0]):
    total = 0
    for j in range(readings.shape[1]):
        total += readings[i, j]
    daily_avg_loop.append(total / readings.shape[1])

# Write the NumPy version here:
daily_avg_np = None  # your answer

# ── PRACTICE 2 ──────────────────────────────────────────────────────────────
# Find all servers where ANY hourly reading exceeded 90%
# Loop version:
high_alert_loop = []
for i in range(readings.shape[0]):
    for j in range(readings.shape[1]):
        if readings[i, j] > 90:
            high_alert_loop.append(i)
            break

# Write the NumPy version (one line):
high_alert_np = None  # your answer

# ── SOLUTIONS ───────────────────────────────────────────────────────────────
daily_avg_np = readings.mean(axis=1)
high_alert_np = np.where((readings > 90).any(axis=1))[0]

print(f"Practice 1 - Loop vs NumPy match: {np.allclose(daily_avg_loop, daily_avg_np)}")
print(f"Practice 2 - Servers with >90% peak: {len(high_alert_np)}")'''),

md('c11', '''## 🎯 Summary

### The Pattern
**Vectorization** — Replace Python loops with NumPy array operations.
Same algorithm. 10-200x faster.

### The Four Key Operations
| Operation | Python Loop | NumPy Vectorized |
|-----------|-------------|-----------------|
| Per-row mean | `for row in matrix` | `matrix.mean(axis=1)` |
| Filter rows | `for x in arr: if x > T` | `arr[arr > T]` |
| Element-wise math | `for i: arr[i] * 2.5 + 100` | `arr * 2.5 + 100` |
| Row vs baseline | `for i,j: m[i,j] - base[j]` | `matrix - baseline` (broadcast) |

### Interview Confidence Checklist
- [ ] Can explain WHY NumPy is faster (C, contiguous memory, SIMD)
- [ ] Can explain broadcasting with a concrete shape example
- [ ] Can rewrite a Python loop as a vectorized NumPy operation on the spot
- [ ] Can name the Citi narrative: 180s → 1.2s, 6M-cell capacity matrix

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# DAY 4-D: APM & Observability
# ─────────────────────────────────────────────────────────────────────────────

APM_OBSERVABILITY = [
md('c01', '''# Technology — APM & Observability
---

<div style="padding:15px;border-left:8px solid #f093fb;background:#fdf0ff;border-radius:4px;">
<strong>Core Insight:</strong> Observability = three pillars: metrics (WHAT happened),
logs (WHY it happened), traces (WHERE in the stack it happened).
OpenTelemetry unifies all three with a vendor-neutral SDK. You instrument once — you export
to any backend: Prometheus, Datadog, Grafana, Jaeger.
</div>

### Why It Matters for Senior DE Roles
A Senior Data Engineer at Citi is expected to build and monitor production pipelines.
"Monitoring" is not optional — it\'s how you prove your pipeline is running correctly.
APM tools (AppDynamics, Dynatrace, CA APM) are tools you\'ve used; knowing the conceptual
framework puts you ahead of candidates who only know metrics.'''),

md('c02', '''## 🧠 The Three Pillars of Observability

| Pillar | What it answers | Example tools | Example data |
|--------|----------------|---------------|-------------|
| **Metrics** | WHAT is happening (numbers) | Prometheus, Datadog, CloudWatch | CPU=72%, latency_p99=230ms, error_rate=0.1% |
| **Logs** | WHY it happened (events) | ELK Stack, Splunk, CloudWatch Logs | `ERROR 2024-01-15 14:23 job=etl msg="connection timeout after 30s"` |
| **Traces** | WHERE in the stack (flow) | Jaeger, Zipkin, AWS X-Ray | Request → API → DB → Cache → response: 230ms total, DB took 180ms |

### The Golden Signals (Google SRE)
Four signals that cover 90% of production monitoring needs:
1. **Latency** — how long requests take (p50, p95, p99 — not average)
2. **Traffic** — how many requests/events per second
3. **Errors** — rate of failed requests (500s, exceptions)
4. **Saturation** — how "full" your system is (CPU%, memory%, queue depth)'''),

code('c03', '''# OpenTelemetry: instrument a Python pipeline
# pip install opentelemetry-api opentelemetry-sdk

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
import time, logging, json

# ── Setup (do once at startup) ───────────────────────────────────────────────
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer("capacity-pipeline")

meter_provider = MeterProvider()
metrics.set_meter_provider(meter_provider)
meter = metrics.get_meter("capacity-pipeline")

# Create metrics instruments
rows_processed = meter.create_counter(
    "pipeline.rows_processed",
    description="Total rows processed by the ETL pipeline"
)
pipeline_duration = meter.create_histogram(
    "pipeline.duration_seconds",
    description="Time to complete a pipeline run"
)
pipeline_errors = meter.create_counter(
    "pipeline.errors",
    description="Pipeline errors by type"
)

# ── Structured logging ───────────────────────────────────────────────────────
def log_event(level, msg, **kwargs):
    entry = {"timestamp": time.time(), "level": level, "msg": msg, **kwargs}
    print(json.dumps(entry))  # In prod: send to ELK/Splunk/CloudWatch'''),

code('c04', '''# Instrumented ETL pipeline with traces + metrics + structured logs

def extract_monitoring_data(server_id: str, date: str) -> list:
    """Extract with distributed tracing."""
    with tracer.start_as_current_span("extract") as span:
        span.set_attribute("server.id", server_id)
        span.set_attribute("date", date)
        log_event("INFO", "Extracting data", server_id=server_id, date=date)
        # Simulate extraction
        time.sleep(0.1)
        data = [{"ts": i, "cpu": 45.0 + i*0.1} for i in range(1440)]  # 24h of minutely readings
        rows_processed.add(len(data), {"stage": "extract", "server": server_id})
        span.set_attribute("rows.extracted", len(data))
        return data

def transform_data(data: list) -> list:
    """Transform with error handling and metrics."""
    with tracer.start_as_current_span("transform") as span:
        start = time.perf_counter()
        try:
            transformed = [{"ts": row["ts"], "cpu_pct": round(row["cpu"], 2)} for row in data]
            rows_processed.add(len(transformed), {"stage": "transform"})
            return transformed
        except Exception as e:
            pipeline_errors.add(1, {"stage": "transform", "error_type": type(e).__name__})
            span.record_exception(e)
            log_event("ERROR", "Transform failed", error=str(e))
            raise

def run_pipeline(server_id: str, date: str):
    """Full pipeline with end-to-end trace."""
    with tracer.start_as_current_span("pipeline.run") as root_span:
        start = time.perf_counter()
        root_span.set_attribute("server.id", server_id)
        root_span.set_attribute("date", date)
        log_event("INFO", "Pipeline started", server=server_id, date=date)
        try:
            data = extract_monitoring_data(server_id, date)
            transformed = transform_data(data)
            duration = time.perf_counter() - start
            pipeline_duration.record(duration, {"server": server_id})
            log_event("INFO", "Pipeline complete", server=server_id, duration_s=round(duration, 3))
        except Exception as e:
            pipeline_errors.add(1, {"stage": "run", "server": server_id})
            log_event("ERROR", "Pipeline failed", server=server_id, error=str(e))
            raise

# Demo run
run_pipeline("SRV-1042", "2024-01-15")'''),

md('c05', '''## 📊 SLO / SLA / Error Budget

| Term | Definition | Example |
|------|------------|---------|
| **SLA** | Service Level Agreement — contractual guarantee | "99.9% uptime or we pay a penalty" |
| **SLO** | Service Level Objective — internal target | "p99 latency < 500ms for 99.9% of requests" |
| **SLI** | Service Level Indicator — the measurement | "Measured p99 = 312ms over last 30 days" |
| **Error Budget** | How much SLO you can miss | `error_budget = 1 - SLO = 0.1% = 43.8 min/month` |

### The Error Budget Formula
```
SLO = 99.9%  →  Error Budget = 0.1%  =  ~43.8 min/month downtime allowed
SLO = 99.99% →  Error Budget = 0.01% =  ~4.4 min/month
SLO = 99.5%  →  Error Budget = 0.5%  =  ~3.65 hr/month
```

**How to use it:** If you\'ve consumed 80% of your monthly error budget in 2 weeks,
STOP all non-critical deployments. The error budget is your risk quota.

### Trend-Based vs Threshold Alerting
- **Static threshold:** Alert when CPU > 90%. Problem: server at 90% for 6 months = not an emergency.
- **Trend-based:** Alert when CPU jumps from 40% to 85% overnight (deviation from trend).
- Trend-based dramatically reduces false positives — the key insight from the Citi APM redesign.'''),

code('c06', '''import numpy as np

# ══════════════════════════════════════
# TREND-BASED ALERTING — the Citi APM approach
# ══════════════════════════════════════

# 90-day baseline of CPU readings for one server
np.random.seed(42)
days = 90
baseline_cpu = np.random.normal(42, 5, size=days)  # stable ~42% CPU

# Simulate a sudden spike on day 85
current_week = np.concatenate([baseline_cpu[:84], np.array([78, 82, 85, 88, 90, 87, 89])])

# ── Static threshold (old approach) ─────────────────────────────────────────
STATIC_THRESHOLD = 85
static_alerts = current_week > STATIC_THRESHOLD
print(f"Static threshold alerts (> {STATIC_THRESHOLD}%): {static_alerts.sum()} days")

# ── Trend-based alerting (new approach) ─────────────────────────────────────
# Rolling 14-day baseline
window = 14
rolling_baseline = np.array([
    current_week[max(0, i-window):i].mean()
    for i in range(1, len(current_week)+1)
])

# Alert when current reading deviates > 20pp from rolling baseline
DEVIATION_THRESHOLD = 20
deviation = current_week - rolling_baseline
trend_alerts = deviation > DEVIATION_THRESHOLD
print(f"Trend-based alerts (deviation > {DEVIATION_THRESHOLD}pp): {trend_alerts.sum()} days")
print(f"Alert reduction: {static_alerts.sum()} → {trend_alerts.sum()}")

# The spike is caught (days 85-90 deviate sharply from baseline)
# Servers stable at high utilization do NOT alert (no deviation)
print(f"\nDeviations on last 7 days: {deviation[-7:].round(1)}")
print("Days 85-90 flagged:", trend_alerts[-7:])'''),

md('c07', '''## 🎤 5 Interview Q&A

**Q1: What are the three pillars of observability and what does each answer?**
Metrics (WHAT): numbers over time — CPU%, latency_p99, error_rate.
Logs (WHY): structured events with context — what happened at what time with what parameters.
Traces (WHERE): how a request flowed through services — which service took the most time.
You need all three: metrics tell you there\'s a problem, logs tell you why, traces show where.

---

**Q2: What is an SLO and how do you calculate an error budget?**
SLO = Service Level Objective — an internal target for service reliability. Example: 99.9% availability.
Error budget = 1 - SLO = 0.1% = 43.8 minutes of downtime allowed per month.
Error budgets create a risk management framework: if 80% consumed in 2 weeks, stop risky deployments.
They align engineering (ship features) vs ops (maintain stability).

---

**Q3: What is OpenTelemetry and why is it important?**
OpenTelemetry is a CNCF vendor-neutral observability framework. You instrument your code once
with the OTel SDK, then export to any backend: Prometheus, Datadog, Jaeger, AWS X-Ray.
Avoids vendor lock-in. Your instrumentation code doesn\'t change when you switch from
Datadog to Prometheus. At Citi, migrating from CA APM to Dynatrace required zero code
changes to instrumented applications.

---

**Q4: What is the difference between p50, p95, and p99 latency?**
p50 = median — 50% of requests finish in this time or less. p95 = 95% of requests are ≤ this.
p99 = 99% of requests are ≤ this. Average hides outliers — a p99 of 2 seconds means 1% of users
wait > 2 seconds. In a system handling 1,000 requests/second, that\'s 10 users/second experiencing
a 2-second wait. Always monitor percentiles, not averages.

---

**Q5: What\'s the problem with static threshold alerting and how do you fix it?**
Static thresholds fire whenever a metric crosses a fixed line, regardless of normal behavior.
A server that normally runs at 90% CPU is not an emergency — but a static 85% alert fires constantly.
This causes alert fatigue: ops teams start ignoring alerts because false positive rate is too high.
Fix: trend-based alerting. Alert when the reading deviates significantly from its rolling baseline
(e.g., > 20 percentage points from 14-day rolling average). This catches real anomalies while
ignoring stable-but-high systems.'''),

md('c08', '''## 📚 Key Terms

| Term | Definition |
|------|------------|
| **Observability** | The ability to understand a system\'s internal state from its external outputs (metrics, logs, traces) |
| **APM** | Application Performance Management — monitoring tools for application health (CA APM, AppDynamics, Dynatrace) |
| **SLO** | Service Level Objective — internal reliability target (e.g., 99.9% uptime) |
| **SLA** | Service Level Agreement — contractual guarantee to customers |
| **Error Budget** | `1 - SLO` — how much unreliability you\'re allowed; consumed by incidents and deployments |
| **SLI** | Service Level Indicator — the measured metric that determines if you\'re meeting your SLO |
| **OpenTelemetry (OTel)** | Vendor-neutral observability framework — one SDK, any backend |
| **Trace** | End-to-end record of a request\'s journey through services, showing timing per component |
| **Span** | A single unit of work within a trace — one service call or database query |
| **Golden Signals** | Google SRE\'s four key metrics: Latency, Traffic, Errors, Saturation |
| **Alert Fatigue** | When ops teams stop trusting alerts because false positive rate is too high |
| **Trend-Based Alerting** | Alert on deviation from rolling baseline rather than absolute threshold |'''),

md('c09', '''## 💼 The Citi Narrative

**Context:** Citi APM team monitoring 6,000+ endpoints across 50+ applications.
Tools: CA APM (Introscope) → AppDynamics → Dynatrace migration.

**The Problem:** Static threshold alerts — 400+ alerts/day firing. Ops team response rate was
near zero because > 70% were false positives. A server at 90% CPU for 6 months was alerting daily.
Real incidents were buried in noise.

**The Fix — Trend-Based Alerting:**
1. Pulled 90-day baselines from CA APM API into PostgreSQL
2. Computed rolling 14-day average per server per metric
3. Changed alert condition: `current_value - rolling_avg > threshold` instead of `current_value > threshold`
4. Added SQL window functions to compute the baseline continuously

**Result:** Alert volume dropped from 400+/day to ~120/day (70% reduction).
More importantly, real incidents were now caught earlier — a server deviating 30pp from
its baseline at 2am is a real problem, even if the absolute value is only 55%.

**Interview Line:** *"The insight was that the metric\'s absolute value is less informative
than its deviation from its own history. A server at 90% CPU that\'s been there for 6 months
is fine. A server that jumped from 40% to 85% overnight is on fire. We built the trending
model in Python, stored baselines in PostgreSQL, and used SQL window functions to compute
the rolling averages. Alert volume dropped 70% while catching more real incidents."*'''),

code('c10', '''# Practice: Build a simple alert evaluation system

import numpy as np

def evaluate_alerts(current_readings: np.ndarray,
                    historical_baseline: np.ndarray,
                    static_threshold: float = 85.0,
                    deviation_threshold: float = 20.0) -> dict:
    """
    Compare static threshold vs trend-based alerting.

    Args:
        current_readings: Array of current metric values (one per server)
        historical_baseline: Array of 30-day average per server
        static_threshold: Alert if current > this value
        deviation_threshold: Alert if deviation from baseline > this value

    Returns:
        Dict with alert counts and server indices for each method
    """
    # Your implementation here:
    static_alerts = None       # servers where current > static_threshold
    trend_alerts = None        # servers where (current - baseline) > deviation_threshold

    # Solution:
    static_alerts = np.where(current_readings > static_threshold)[0]
    deviations = current_readings - historical_baseline
    trend_alerts = np.where(deviations > deviation_threshold)[0]

    return {
        "static_count": len(static_alerts),
        "trend_count": len(trend_alerts),
        "static_servers": static_alerts,
        "trend_servers": trend_alerts,
        "reduction_pct": round((1 - len(trend_alerts)/max(len(static_alerts),1)) * 100, 1)
    }

# Test it
np.random.seed(42)
n_servers = 6000
baseline = np.random.normal(42, 10, n_servers)  # historical averages
current = baseline + np.random.normal(0, 5, n_servers)  # small noise
# Inject 50 real incidents (big spike)
incident_idx = np.random.choice(n_servers, 50, replace=False)
current[incident_idx] += np.random.uniform(25, 45, 50)

result = evaluate_alerts(current, baseline)
print(f"Static threshold alerts:  {result['static_count']}")
print(f"Trend-based alerts:       {result['trend_count']}")
print(f"Alert reduction:          {result['reduction_pct']}%")
print(f"(Real incidents injected: 50)")'''),

md('c11', '''## 🎯 Summary

### The Pattern
**Observability** — Metrics + Logs + Traces = full system visibility.
**Trend-based alerting** = alert on deviation from baseline, not absolute values.

### The Stack
| Layer | Tool examples | What you learn |
|-------|--------------|----------------|
| Metrics | Prometheus, CloudWatch, Datadog | Dashboards, SLO tracking |
| Logs | ELK, Splunk, CloudWatch Logs | Root cause investigation |
| Traces | Jaeger, AWS X-Ray, Datadog APM | Latency bottleneck identification |
| Framework | OpenTelemetry | Vendor-neutral instrumentation |

### Interview Confidence Checklist
- [ ] Can name the three pillars and what each answers
- [ ] Can explain SLO / SLA / Error Budget and the formula
- [ ] Can explain trend-based vs static threshold alerting
- [ ] Can name the Citi narrative: 70% alert reduction, APM migration
- [ ] Can describe OpenTelemetry\'s value proposition

**"Simplicity and clarity is Gold."** — Sean\'s Study Mantra 🚀''')
]


# ─────────────────────────────────────────────────────────────────────────────
# Write Day 4 concept notebooks
# ─────────────────────────────────────────────────────────────────────────────

write_nb(f'{BASE}/Day4/sql-query-optimization.ipynb', SQL_QUERY_OPT)
write_nb(f'{BASE}/Day4/python-numpy-vectorization.ipynb', NUMPY_VECTORIZATION)
write_nb(f'{BASE}/Day4/apm-observability.ipynb', APM_OBSERVABILITY)

print('\nDay 4 concepts done. Run again with DAY=5 or DAY=6 to continue.')
print('All Day 4 concept notebooks written successfully.')
