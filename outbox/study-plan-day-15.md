---
created: 2026-03-02
updated: 2026-03-02
summary: Day 15 — Week 3 opens with Backtracking, JSON SQL in DuckDB, Structured Logging & Profiling, and Advanced Spark Optimization.
tags: [study-plan, day-15, backtracking, json-sql, logging, spark-optimization]
---

# Day 15 — Backtracking | JSON SQL | Structured Logging | Advanced Spark Optimization

**Theme:** Go deeper. Week 3 covers patterns and tools that separate senior engineers from mid-level ones.

---

## Spaced Repetition Check-In (15 min)

Before starting new material, answer these from memory:

1. What is the difference between DFS on a graph and DFS on a tree?
2. Write Kadane's Algorithm in 4 lines.
3. What does `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` do in a window function?
4. What is the difference between `ref()` and `source()` in dbt?
5. In Kafka, what happens if you have more consumers than partitions in a consumer group?
6. What are the three things Delta Lake's transaction log enables?

> If any answer takes more than 15 seconds or feels uncertain — flag it for review tonight.

---

## A. LeetCode — Backtracking (60 min)

### Why Backtracking

Backtracking = DFS + undo. You build a candidate solution incrementally. At each step, if the candidate can't lead to a solution, you abandon it (prune) and backtrack. Shows up in:
- Combinatorics: subsets, permutations, combinations
- Constraint satisfaction: N-Queens, Sudoku
- Word search in grids

**Mental model:** "I'm walking a decision tree. At each node I choose. If the path fails, I climb back up and choose differently."

### The Template

```python
def backtrack(path, choices):
    if base_case(path):
        result.append(path[:])   # snapshot — list is mutable
        return
    for choice in choices:
        if not valid(choice, path):
            continue              # prune early
        path.append(choice)
        backtrack(path, remaining_choices(choice))
        path.pop()               # UNDO — this is the "back" in backtrack
```

Key rules:
1. Always `path[:]` or `list(path)` when saving — never save the reference
2. Always `path.pop()` after the recursive call
3. Pruning before the recursive call = massive speedup

---

### Problem 1 — LC #78: Subsets (Medium)

**Problem:** Given an integer array `nums` of unique elements, return all possible subsets (the power set). Include the empty set.

```
Input:  [1, 2, 3]
Output: [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

**Approach — start index prevents duplicates:**
```python
def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])          # every node is a valid subset
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)      # i+1: don't reuse current element
            path.pop()

    backtrack(0, [])
    return result
```

**Complexity:** O(n × 2ⁿ) time, O(n) stack space. There are 2ⁿ subsets; copying each takes O(n).

---

### Problem 2 — LC #39: Combination Sum (Medium)

**Problem:** Given an array of distinct integers `candidates` and a target integer `target`, return all combinations that sum to target. Same element can be used unlimited times.

```
Input:  candidates = [2,3,6,7], target = 7
Output: [[2,2,3], [7]]
```

```python
def combinationSum(candidates, target):
    result = []
    candidates.sort()   # enables early pruning

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break               # sorted: no point continuing
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # i not i+1: reuse allowed
            path.pop()

    backtrack(0, [], target)
    return result
```

---

### Problem 3 — LC #46: Permutations (Medium)

**Problem:** Given an array `nums` of distinct integers, return all permutations.

```
Input:  [1, 2, 3]
Output: [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

```python
def permute(nums):
    result = []

    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()

    backtrack([], nums)
    return result
```

**Complexity:** O(n × n!) — there are n! permutations, each of length n.

---

### Problem 4 — LC #79: Word Search (Medium)

**Problem:** Given an m×n grid of characters and a string `word`, return True if `word` exists in the grid. Letters must be adjacent (horizontal/vertical) and the same cell cannot be used twice.

```
Input:  board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]
        word = "ABCCED"
Output: True
```

```python
def exist(board, word):
    rows, cols = len(board), len(board[0])

    def dfs(r, c, idx):
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if board[r][c] != word[idx]:
            return False

        temp = board[r][c]
        board[r][c] = '#'   # mark visited IN-PLACE

        found = (dfs(r+1,c,idx+1) or dfs(r-1,c,idx+1) or
                 dfs(r,c+1,idx+1) or dfs(r,c-1,idx+1))

        board[r][c] = temp  # UNDO — restore for other paths
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

**Key insight:** In-place marking (`'#'`) avoids a `visited` set. Restore on exit = the "back" in backtrack.

---

### Backtracking Decision Guide

| Problem Type | Include every node? | Reuse elements? | Pattern |
|-------------|---------------------|-----------------|---------|
| Subsets | Yes | No | `start = i+1` |
| Combinations | No (only leaves) | No | `start = i+1` |
| Combination Sum | No (only leaves) | Yes | `start = i` |
| Permutations | No (only leaves) | No | `remaining` list |
| Grid search | No | No | In-place mark + restore |

---

## B. SQL — JSON Functions in DuckDB (45 min)

### Why JSON in DE Interviews

Real telemetry is messy. APIs return nested JSON. Event streams embed JSON blobs. Interviewers test: can you wrangle semi-structured data without loading it into a DataFrame first?

DuckDB is native to the job — it handles JSON natively.

### Schema Setup

```sql
-- Telemetry events with nested JSON payload
CREATE TABLE telemetry_events AS
SELECT * FROM (VALUES
    (1, 'srv-001', '2026-02-26', '{"cpu": 82.5, "mem": 74.1, "disk": {"read_iops": 1200, "write_iops": 800}, "tags": ["production", "web"]}'),
    (2, 'srv-002', '2026-02-26', '{"cpu": 45.2, "mem": 90.3, "disk": {"read_iops": 300, "write_iops": 100}, "tags": ["staging"]}'),
    (3, 'srv-001', '2026-02-27', '{"cpu": 91.0, "mem": 78.4, "disk": {"read_iops": 1500, "write_iops": 950}, "tags": ["production", "web"]}'),
    (4, 'srv-003', '2026-02-27', '{"cpu": 55.0, "mem": 62.0, "disk": {"read_iops": 700, "write_iops": 400}, "tags": ["production", "db"]}')
) AS t(event_id, server_id, report_date, payload);
```

### Core JSON Functions

```sql
-- 1. Extract scalar values
SELECT
    server_id,
    report_date,
    payload->>'cpu'                    AS cpu_util,        -- string
    CAST(payload->>'cpu' AS FLOAT)     AS cpu_float,       -- numeric
    payload->'disk'->>'read_iops'      AS read_iops        -- nested
FROM telemetry_events;

-- 2. Extract nested object
SELECT
    server_id,
    payload->'disk' AS disk_json,
    CAST(payload->'disk'->>'read_iops' AS INTEGER) AS read_iops,
    CAST(payload->'disk'->>'write_iops' AS INTEGER) AS write_iops
FROM telemetry_events;

-- 3. Unnest JSON arrays (CRITICAL — tags is an array)
SELECT
    server_id,
    report_date,
    UNNEST(json_extract(payload, '$.tags')) AS tag
FROM telemetry_events;
-- Returns one row per tag

-- 4. Filter by JSON array membership
SELECT server_id, report_date
FROM telemetry_events
WHERE list_contains(
    json_extract(payload, '$.tags')::VARCHAR[],
    '"production"'
);
```

### Practice Query 1 — Flatten and Aggregate

**Problem:** For each server, compute average CPU and max read IOPS across all days. Output: server_id, avg_cpu, max_read_iops.

```sql
SELECT
    server_id,
    ROUND(AVG(CAST(payload->>'cpu' AS FLOAT)), 2)              AS avg_cpu,
    MAX(CAST(payload->'disk'->>'read_iops' AS INTEGER))        AS max_read_iops
FROM telemetry_events
GROUP BY server_id
ORDER BY avg_cpu DESC;
```

### Practice Query 2 — Tag-Based Rollup

**Problem:** Count distinct servers per environment tag (production, staging, db).

```sql
WITH exploded AS (
    SELECT
        server_id,
        UNNEST(json_extract(payload, '$.tags')) AS raw_tag
    FROM telemetry_events
),
cleaned AS (
    SELECT
        server_id,
        TRIM(REPLACE(raw_tag::VARCHAR, '"', '')) AS tag
    FROM exploded
)
SELECT tag, COUNT(DISTINCT server_id) AS server_count
FROM cleaned
GROUP BY tag
ORDER BY server_count DESC;
```

### Practice Query 3 — High-Risk Servers (CPU > 85 AND write_iops > 700)

```sql
SELECT
    server_id,
    report_date,
    CAST(payload->>'cpu' AS FLOAT)                         AS cpu,
    CAST(payload->'disk'->>'write_iops' AS INTEGER)        AS write_iops
FROM telemetry_events
WHERE CAST(payload->>'cpu' AS FLOAT) > 85
  AND CAST(payload->'disk'->>'write_iops' AS INTEGER) > 700
ORDER BY cpu DESC;
```

### DuckDB JSON Cheat Sheet

| Goal | Syntax |
|------|--------|
| Extract as JSON | `col->'key'` |
| Extract as text | `col->>'key'` |
| Nested extract | `col->'outer'->>'inner'` |
| Cast to numeric | `CAST(col->>'key' AS FLOAT)` |
| Unnest array | `UNNEST(json_extract(col, '$.arr'))` |
| Check array membership | `list_contains(arr::VARCHAR[], '"val"')` |

---

## C. Python — Structured Logging & Profiling (30 min)

### Why This Matters

Production pipelines fail silently. A pipeline that emits unstructured `print()` or bare `logging.info()` is un-debuggable at scale. Structured logs (JSON output) can be queried in CloudWatch, Datadog, ELK. Profiling finds the bottleneck before the SLA breach.

### Structured Logging with `structlog`

```python
import structlog
import logging

# Configure once at startup
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),       # machine-readable output
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

log = structlog.get_logger()

# Usage — bind context, then log events
log = log.bind(pipeline="telemetry_ingest", server_id="srv-001")
log.info("ingestion_started", batch_size=1000)
log.warning("high_cpu_detected", cpu=92.3, threshold=85.0)
log.error("connection_failed", host="db.prod.local", retry=3)
```

**Output (JSON, queryable):**
```json
{"event": "ingestion_started", "pipeline": "telemetry_ingest", "server_id": "srv-001", "batch_size": 1000, "level": "info", "timestamp": "2026-03-02T09:00:00Z"}
```

### Standard Library Logging (baseline — know this too)

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info("Pipeline started")
logger.warning("Memory usage: %.1f%%", 87.3)
logger.error("Failed to write to S3", exc_info=True)   # includes traceback
```

**Log levels — know the semantics:**
| Level | When to use |
|-------|-------------|
| DEBUG | Verbose dev-only detail |
| INFO | Normal operational events |
| WARNING | Something unexpected but recoverable |
| ERROR | Operation failed; pipeline continues |
| CRITICAL | System cannot continue |

### Pipeline Profiling with `cProfile`

```python
import cProfile
import pstats
import io

def profile_pipeline(func, *args, **kwargs):
    """Run func under profiler, return result + print top 10 hotspots."""
    pr = cProfile.Profile()
    pr.enable()
    result = func(*args, **kwargs)
    pr.disable()

    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats(10)
    print(s.getvalue())
    return result

# Use it
def expensive_pipeline(data):
    # ... your pipeline code
    pass

profile_pipeline(expensive_pipeline, my_data)
```

### Line-Level Profiling with `line_profiler`

```python
# Install: pip install line_profiler
# Decorate the function you suspect is slow:

@profile   # added by kernprof at runtime
def transform_telemetry(df):
    df['cpu_norm'] = df['avg_cpu'] / 100.0
    df['risk'] = df['cpu_norm'].apply(lambda x: 'high' if x > 0.85 else 'low')
    return df

# Run: kernprof -l -v script.py
```

### Quick Reference: When to Use What

| Tool | Use case |
|------|----------|
| `structlog` | Production pipelines, CloudWatch/Datadog integration |
| `logging` (stdlib) | Simple scripts, Lambda functions |
| `cProfile` | Find which functions consume total time |
| `line_profiler` | Pin down which lines inside a function are slow |
| `memory_profiler` | Find memory leaks in long-running pipelines |

---

## D. Technology — Advanced Spark Optimization (45 min)

### The Catalyst Optimizer

When you write Spark SQL or use the DataFrame API, Spark doesn't execute it directly. It goes through:

```
Query → Unresolved Logical Plan
      → Resolved Logical Plan (catalog lookups)
      → Optimized Logical Plan (Catalyst rules: predicate pushdown, column pruning)
      → Physical Plans (multiple candidates)
      → Selected Physical Plan (cost-based optimizer picks the best)
      → Code Generation (Tungsten: bytecode)
```

**Key optimization rules Catalyst applies automatically:**
- **Predicate pushdown:** `WHERE` filters applied before joins (filter early, join less data)
- **Column pruning:** Only reads columns referenced in the query
- **Constant folding:** `1 + 1` computed at plan time, not at execution time
- **Join reordering:** (with CBO enabled) smaller tables joined first

**See what Catalyst produces:**
```python
df.explain(extended=True)   # shows all 4 plan stages
```

### Adaptive Query Execution (AQE) — Spark 3.x

AQE re-optimizes at runtime based on actual data statistics, not estimates.

**What AQE fixes:**
1. **Skew joins:** Splits skewed partitions into smaller ones automatically
2. **Dynamic partition coalescing:** Merges small shuffle partitions after a join
3. **Dynamic join strategy switching:** Switches broadcast join on/off based on real size

```python
spark.conf.set("spark.sql.adaptive.enabled", "true")              # default in Spark 3.2+
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### Broadcast Join — When and Why

```python
from pyspark.sql.functions import broadcast

# Small lookup table (< 10 MB default, configurable up to ~200 MB)
region_lookup = spark.table("region_info")   # tiny table

big_df = spark.table("daily_metrics")        # 50 GB

# Without hint: Spark might sort-merge join (expensive shuffle)
# With hint: Spark broadcasts region_lookup to every executor (no shuffle)
result = big_df.join(broadcast(region_lookup), "region_id")
```

**Broadcast threshold:**
```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)  # 50 MB
```

### Shuffle Tuning

Shuffle = the most expensive Spark operation. Data crosses the network between executors.

```python
# Default: 200 partitions after a shuffle (often wrong)
spark.conf.set("spark.sql.shuffle.partitions", "200")

# Rule of thumb: target 100-200 MB per partition
# 50 GB dataset / 200 MB = 250 partitions → set to 256 (power of 2)
spark.conf.set("spark.sql.shuffle.partitions", "256")

# Or use AQE to auto-tune (recommended):
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
```

### Caching Strategy

```python
# Cache only what's reused across multiple actions
from pyspark import StorageLevel

# MEMORY_AND_DISK: spill to disk if RAM full (safer for large datasets)
expensive_df.persist(StorageLevel.MEMORY_AND_DISK)
expensive_df.count()   # trigger the cache (Spark is lazy)

# ... use expensive_df multiple times ...

expensive_df.unpersist()   # release when done — critical in long-running jobs
```

**What NOT to cache:**
- DataFrames used only once
- DataFrames that are re-read from Parquet (Parquet scan is fast)
- Very large DataFrames that will evict other cached data

### Data Skew — Detection and Fix

```python
# Detect skew: look at partition sizes
df.rdd.glom().map(len).collect()   # see element count per partition

# Fix 1: Salting — spread a hot key across N buckets
import pyspark.sql.functions as F

N = 10
df_salted = df.withColumn("salt", (F.rand() * N).cast("int")) \
              .withColumn("key_salted", F.concat(F.col("server_id"), F.lit("_"), F.col("salt")))

# Join on salted key (both sides must be salted)
lookup_exploded = lookup.withColumn("salt", F.explode(F.array([F.lit(i) for i in range(N)]))) \
                        .withColumn("key_salted", F.concat(F.col("server_id"), F.lit("_"), F.col("salt")))

result = df_salted.join(lookup_exploded, "key_salted")

# Fix 2: AQE skew join (Spark 3.x — handles automatically when enabled)
```

### Senior-Level Interview Answers

**Q: "How would you debug a slow Spark job?"**
> First check the Spark UI: look at stage durations, task distribution (skew shows up as one task 100x slower), and GC time. Then: 1) Is there a shuffle? Look at data movement. 2) Is there skew? One partition gets all the data. 3) Are joins broadcasting when they should? Check physical plan with `explain()`. 4) Is the shuffle partition count wrong (default 200)?

**Q: "When would you NOT use Spark?"**
> When DuckDB or Pandas is fast enough. Spark's overhead (cluster startup, serialization, scheduling) is a tax. For files under 10 GB or interactive queries, DuckDB in-process is 10x faster and free. Spark is the right tool when data exceeds single-machine RAM or when distributed compute is already provisioned.

---

## Behavioral Anchor — Day 15

> "Tell me about a time you improved the observability of a system."

Think of a story where you:
- Added logging, monitoring, or alerting to a previously opaque process
- Detected (or could have detected) a problem earlier
- Quantified the improvement (MTTR reduction, faster debugging)

Write a 3-sentence STAR skeleton now:
- **Situation + Task:**
- **Action (specifically what you built):**
- **Result (measured):**

---

## Day 15 Checklist

- [ ] Coded all 4 backtracking problems from scratch (no copy-paste)
- [ ] Ran all 3 JSON SQL practice queries against a real DuckDB instance
- [ ] Can explain `->` vs `->>` in DuckDB JSON extraction
- [ ] Wrote a structlog example from memory
- [ ] Can explain Catalyst optimizer in 3 sentences
- [ ] Can explain what AQE does and why it matters for skew joins
- [ ] Behavioral story drafted
