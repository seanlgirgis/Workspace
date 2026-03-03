---
created: 2026-03-02
updated: 2026-03-02
summary: Day 24 — Monotonic Stack (hard problems), Advanced Window Functions (NTILE, PERCENT_RANK, lateral joins), Polars as a Pandas alternative, ClickHouse and real-time analytics.
tags: [study-plan, day-24, monotonic-stack, ntile, percent-rank, lateral-join, polars, clickhouse]
---

# Day 24 — Monotonic Stack | Advanced Window Functions | Polars | ClickHouse

**Theme:** The patterns that appear in performance-critical analytics. Monotonic stack is a hidden LC gem; ClickHouse is replacing Druid in many stacks.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is the time complexity of Dijkstra and when does Bellman-Ford win?
2. In a Recursive CTE, how do you "walk UP" a tree (ancestors)?
3. In asyncio, what is the difference between `asyncio.gather()` and `asyncio.Semaphore`?
4. What does `op: "u"` mean in a Debezium event?
5. What does Snowflake Time Travel let you do, and for how long (Enterprise)?
6. In LC #10 (Regex), what are the two options when the pattern character is `*`?

---

## A. LeetCode — Monotonic Stack (60 min)

### What is a Monotonic Stack?

A monotonic stack maintains elements in either strictly increasing or strictly decreasing order. When a new element violates the order, you pop elements until the order is restored. This gives O(n) time for problems that would naively require O(n²).

**Key insight:** Elements are popped at most once each → total work is O(n) despite nested loops.

**When to use:**
- "Next greater/smaller element"
- "Previous greater/smaller element"
- Largest rectangle / trapped water problems
- Stock price span problems

---

### Problem 1 — LC #739: Daily Temperatures (Medium)

**Problem:** Given a list of daily temperatures, return an array where `answer[i]` = number of days until a warmer temperature. If no warmer day exists, answer[i] = 0.

```
Input:  [73, 74, 75, 71, 69, 72, 76, 73]
Output: [1,  1,  4,  2,  1,  1,  0,  0]
```

```python
def dailyTemperatures(temps):
    result = [0] * len(temps)
    stack = []   # monotonic decreasing stack of indices

    for i, t in enumerate(temps):
        # Pop all days that found their "next warmer day" today
        while stack and temps[stack[-1]] < t:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)

    return result
```

**Trace:** Stack holds indices of days waiting for a warmer day. When a warmer day arrives, pop everything colder.

---

### Problem 2 — LC #84: Largest Rectangle in Histogram (Hard)

**Problem:** Given an array of bar heights, find the largest rectangle you can form using consecutive bars.

```
Input:  [2, 1, 5, 6, 2, 3]
Output: 10  (bars at index 2-3: height=5, width=2)
```

```python
def largestRectangleArea(heights):
    stack = []   # monotonic increasing stack of indices
    max_area = 0
    heights = heights + [0]   # sentinel: force all bars to be popped at end

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            # Width: from current position back to the previous bar in stack
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
```

**Key insight:** When we pop a bar (because a shorter bar arrived), we know:
- The popped bar is the shortest bar in the window
- The window extends right to the current bar (exclusive) and left to the new stack top (exclusive)

---

### Problem 3 — LC #42: Trapping Rain Water (Hard)

**Problem:** Given elevation heights, compute total water trapped.

```
Input:  [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
```

**Two-pointer approach (O(n) time, O(1) space):**
```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water
```

**Monotonic stack approach (also O(n)):**
```python
def trap(height):
    stack = []
    water = 0

    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = stack.pop()
            if not stack:
                break
            left = stack[-1]
            width = i - left - 1
            bound = min(height[left], h) - height[bottom]
            water += width * bound

        stack.append(i)

    return water
```

---

### Problem 4 — LC #901: Online Stock Span (Medium)

**Problem:** Design a class that collects stock prices day by day and returns the span (how many consecutive days before today the price was ≤ today's price).

```
Input:  [100, 80, 60, 70, 60, 75, 85]
Output: [1,   1,  1,  2,  1,  4,  6]
```

```python
class StockSpanner:
    def __init__(self):
        self.stack = []   # (price, span) — monotonic decreasing

    def next(self, price: int) -> int:
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            _, prev_span = self.stack.pop()
            span += prev_span   # absorb the span of popped elements
        self.stack.append((price, span))
        return span
```

**Key trick:** Accumulate spans — when popping elements whose price is ≤ current, add their spans (already pre-computed).

---

### Monotonic Stack Patterns

| Problem type | Stack order | Pop condition |
|-------------|------------|---------------|
| Next greater element | Decreasing | New element > top |
| Next smaller element | Increasing | New element < top |
| Previous greater | Decreasing | Pop to find prev boundary |
| Histogram / trapped water | Increasing | New element < top |

---

## B. SQL — Advanced Window Functions + Lateral Joins (45 min)

### NTILE, PERCENT_RANK, CUME_DIST

These are ranking window functions for distribution analysis — essential for capacity tier assignment and percentile reporting.

```sql
-- Setup: server CPU utilization snapshot
CREATE TABLE server_snapshot AS
SELECT * FROM (VALUES
    ('srv-001', 'us-east-1', 'web',  82.5),
    ('srv-002', 'us-east-1', 'web',  45.2),
    ('srv-003', 'us-east-1', 'db',   91.0),
    ('srv-004', 'us-east-1', 'db',   55.0),
    ('srv-005', 'us-west-2', 'web',  78.3),
    ('srv-006', 'us-west-2', 'cache',30.1),
    ('srv-007', 'us-west-2', 'web',  95.7),
    ('srv-008', 'us-east-1', 'cache',22.4)
) AS t(server_id, region, tier, avg_cpu);
```

```sql
-- Distribution functions
SELECT
    server_id,
    region,
    tier,
    avg_cpu,

    -- NTILE(n): divide rows into n equal buckets (1=lowest, n=highest)
    NTILE(4) OVER (ORDER BY avg_cpu)                    AS cpu_quartile,
    NTILE(4) OVER (PARTITION BY region ORDER BY avg_cpu) AS cpu_quartile_in_region,

    -- PERCENT_RANK: (rank-1)/(total_rows-1) → [0.0, 1.0]
    -- 0.0 = lowest, 1.0 = highest
    ROUND(PERCENT_RANK() OVER (ORDER BY avg_cpu), 3)    AS cpu_pct_rank,

    -- CUME_DIST: what fraction of rows have cpu <= this row's cpu
    -- Always > 0, never > 1
    ROUND(CUME_DIST() OVER (ORDER BY avg_cpu), 3)       AS cpu_cume_dist,

    -- RANK vs DENSE_RANK vs ROW_NUMBER (review)
    RANK()         OVER (ORDER BY avg_cpu DESC)         AS rank_by_cpu,
    DENSE_RANK()   OVER (ORDER BY avg_cpu DESC)         AS dense_rank_by_cpu
FROM server_snapshot
ORDER BY avg_cpu DESC;
```

### Practical Query — Tiered Capacity Risk Report

```sql
-- Assign risk tier based on CPU quartile, then summarize
WITH tiered AS (
    SELECT
        server_id,
        region,
        tier,
        avg_cpu,
        NTILE(4) OVER (ORDER BY avg_cpu DESC) AS risk_quartile
        -- Q1 (quartile=1) = top 25% by CPU = highest risk
    FROM server_snapshot
)
SELECT
    region,
    tier,
    risk_quartile,
    CASE risk_quartile
        WHEN 1 THEN 'Critical'
        WHEN 2 THEN 'High'
        WHEN 3 THEN 'Medium'
        ELSE        'Low'
    END                         AS risk_label,
    COUNT(*)                    AS server_count,
    ROUND(AVG(avg_cpu), 1)      AS avg_cpu,
    MAX(avg_cpu)                AS max_cpu
FROM tiered
GROUP BY region, tier, risk_quartile
ORDER BY risk_quartile, region;
```

### Lateral Joins — Row-by-Row Expansion

A lateral join (also called `CROSS JOIN LATERAL` or just `JOIN LATERAL`) lets a subquery reference columns from the current row. Think of it as "for each row in the left table, run this subquery."

```sql
-- Problem: for each server, get its 3 most recent anomaly events
-- Without lateral: requires window function + filter (doable but verbose)
-- With lateral: cleaner

SELECT
    s.server_id,
    s.region,
    recent.event_date,
    recent.avg_cpu,
    recent.rn
FROM server_snapshot s
CROSS JOIN LATERAL (
    SELECT
        m.report_date AS event_date,
        m.avg_cpu,
        ROW_NUMBER() OVER (ORDER BY m.report_date DESC) AS rn
    FROM daily_metrics m
    WHERE m.server_id = s.server_id   -- references outer query row
      AND m.avg_cpu > 80
) recent
WHERE recent.rn <= 3
ORDER BY s.server_id, recent.rn;
```

**DuckDB `UNNEST` with lateral (array expansion):**
```sql
-- Unnest tags per server and count tag frequency
SELECT
    s.server_id,
    tag_val
FROM server_snapshot s,
LATERAL UNNEST(STRING_SPLIT(s.tier, ',')) AS t(tag_val)
ORDER BY s.server_id;
```

### FILTER Clause (reduce boilerplate vs CASE WHEN)

```sql
-- Compare: CASE WHEN vs FILTER
-- Traditional CASE WHEN pivot:
SELECT
    region,
    COUNT(CASE WHEN avg_cpu > 80 THEN 1 END) AS high_cpu_count,
    COUNT(CASE WHEN avg_cpu <= 80 THEN 1 END) AS normal_cpu_count
FROM server_snapshot
GROUP BY region;

-- Modern FILTER syntax (cleaner):
SELECT
    region,
    COUNT(*) FILTER (WHERE avg_cpu > 80)  AS high_cpu_count,
    COUNT(*) FILTER (WHERE avg_cpu <= 80) AS normal_cpu_count
FROM server_snapshot
GROUP BY region;
```

---

## C. Python — Polars (30 min)

### What is Polars and Why Should DE Know It?

Polars is a DataFrame library written in Rust. It is:
- **10-100x faster than Pandas** for most operations (genuine parallelism, no GIL)
- **Memory efficient** (Apache Arrow columnar format)
- **Lazy evaluation** (like Spark — build query plan, execute once)
- **A real interview differentiator** in 2026 — hiring teams notice when you know it

### Core API Differences from Pandas

```python
import polars as pl

# Read
df = pl.read_parquet("daily_metrics.parquet")
df = pl.scan_parquet("daily_metrics.parquet")   # LAZY — doesn't load yet

# Select columns (method chaining, not df[[cols]])
df.select(["server_id", "avg_cpu", "report_date"])

# Filter (expression-based, not df[df.col > 80])
df.filter(pl.col("avg_cpu") > 80)

# Add column
df.with_columns(
    (pl.col("avg_cpu") / 100).alias("cpu_fraction")
)

# Group by + aggregate
df.group_by("server_id").agg([
    pl.col("avg_cpu").mean().alias("mean_cpu"),
    pl.col("avg_cpu").max().alias("max_cpu"),
    pl.col("report_date").count().alias("days_reported")
])

# Join
df.join(server_dim, on="server_id", how="left")

# Sort
df.sort("avg_cpu", descending=True)
```

### Lazy Evaluation — The Key Polars Feature

```python
# Lazy: build the query plan
query = (
    pl.scan_parquet("daily_metrics/**/*.parquet")   # lazy read
    .filter(pl.col("avg_cpu") > 80)
    .with_columns(
        pl.col("avg_cpu").rolling_mean(window_size=7).over("server_id").alias("cpu_7d")
    )
    .group_by(["server_id", pl.col("report_date").dt.month().alias("month")])
    .agg(pl.col("avg_cpu").mean())
    .sort("avg_cpu", descending=True)
)

# Execute — only now does any I/O or computation happen
result = query.collect()

# Explain the query plan (like Spark's explain())
print(query.explain())
```

**Why lazy matters:** Polars optimizes the plan before executing — predicate pushdown, column pruning, parallel reads. You get Spark-like optimization without Spark's overhead.

### Window Functions in Polars

```python
df = pl.read_parquet("daily_metrics.parquet")

result = df.with_columns([
    # 7-day trailing average per server
    pl.col("avg_cpu")
        .rolling_mean(window_size=7)
        .over("server_id")
        .alias("cpu_7d_avg"),

    # Rank within each region
    pl.col("avg_cpu")
        .rank(descending=True)
        .over("region")
        .alias("cpu_rank_in_region"),

    # Lag (previous day's CPU)
    pl.col("avg_cpu")
        .shift(1)
        .over("server_id")
        .alias("cpu_prev_day"),
])
```

### Polars vs Pandas vs Spark

| Dimension | Pandas | Polars | Spark |
|-----------|--------|--------|-------|
| Size limit | RAM (single machine) | RAM (single machine) | Cluster (TB+) |
| Speed | Baseline | 10-100x faster | Slower start (JVM), faster at scale |
| Parallelism | None (GIL) | Full CPU parallelism | Distributed |
| API | Index-based, mutable | Expression-based, immutable | DataFrame + SQL |
| Best for | < 1GB, quick analysis | 1GB-100GB, fast local processing | 100GB+, distributed ETL |

**Interview answer:**
> "For files that fit in RAM — up to 50-100GB on a memory-optimized instance — Polars is dramatically faster than Pandas and doesn't require Spark cluster overhead. I use Polars for feature engineering in ML pipelines where I need fast iteration. For distributed scale, Spark. For quick analysis of small datasets, Pandas (because everyone knows it)."

---

## D. Technology — ClickHouse and Real-Time Analytics (45 min)

### What is ClickHouse?

ClickHouse is an open-source columnar OLAP database from Yandex. Built for: high-throughput analytical queries, sub-second response, real-time data ingestion.

**Key differentiators:**
- Columnar storage — queries touch only relevant columns
- Vectorized query execution — processes 128+ values at once using SIMD
- Linear scaling — add nodes horizontally
- MergeTree engine — append-only, sorted by sort key, parts merged in background

### When ClickHouse Beats Athena/Snowflake

| Dimension | ClickHouse | Athena | Snowflake |
|-----------|-----------|--------|-----------|
| Query latency | < 100ms at scale | 1-30s (cold) | 1-10s |
| Data freshness | Seconds (real-time insert) | Hours (S3 delay) | Minutes-hours |
| Cost model | Fixed (server) | Per TB scanned | Per credit (warehouse size) |
| Best for | Real-time dashboards, high-QPS analytics | Ad hoc, S3-native | Enterprise warehouse, SQL-heavy |
| Worst for | Complex joins, OLTP | Latency-sensitive apps | Real-time event streams |

### ClickHouse Data Model

```sql
-- MergeTree: the workhorse table engine
CREATE TABLE server_metrics (
    server_id   String,
    region      LowCardinality(String),   -- efficient for low-cardinality strings
    report_date Date,
    avg_cpu     Float32,
    avg_mem     Float32,
    tags        Array(String)
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(report_date)        -- partition by month (S3-like partition pruning)
ORDER BY (server_id, report_date)          -- sort key — critical for range queries
SETTINGS index_granularity = 8192;        -- rows per sparse index mark
```

**ReplacingMergeTree — handle updates (deduplicate on sort key):**
```sql
CREATE TABLE server_current_state (
    server_id   String,
    tier        String,
    region      String,
    updated_at  DateTime
)
ENGINE = ReplacingMergeTree(updated_at)   -- keeps row with latest updated_at
ORDER BY server_id;

-- Upsert: just INSERT (merge happens in background)
INSERT INTO server_current_state VALUES ('srv-001', 'premium', 'us-east-1', now());

-- Query: use FINAL to force dedup at query time
SELECT * FROM server_current_state FINAL;
```

### Real-Time Analytics Pipeline Architecture

```
Kafka (server telemetry events)
  → ClickHouse Kafka Table Engine (direct Kafka consumption — no Flink needed)
  → ClickHouse MergeTree table (metrics stored columnar)
  → Grafana / Superset / custom API (< 100ms queries)
```

**ClickHouse Kafka Engine:**
```sql
-- Source: reads from Kafka automatically
CREATE TABLE kafka_source (
    server_id String,
    avg_cpu   Float32,
    event_ts  DateTime
)
ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'kafka:9092',
    kafka_topic_list = 'server-telemetry',
    kafka_group_name = 'clickhouse-ingest',
    kafka_format = 'JSONEachRow';

-- Materialized view: writes Kafka data to MergeTree automatically
CREATE MATERIALIZED VIEW kafka_to_metrics TO server_metrics AS
SELECT server_id, avg_cpu, event_ts AS report_date
FROM kafka_source;
```

### ClickHouse SQL Extensions

```sql
-- arrayJoin: equivalent to UNNEST
SELECT server_id, arrayJoin(tags) AS tag
FROM server_metrics;

-- quantile: percentile aggregation
SELECT
    region,
    quantile(0.50)(avg_cpu) AS p50_cpu,
    quantile(0.95)(avg_cpu) AS p95_cpu,
    quantile(0.99)(avg_cpu) AS p99_cpu
FROM server_metrics
GROUP BY region;

-- Moving average (native)
SELECT
    server_id,
    report_date,
    avg(avg_cpu) OVER (
        PARTITION BY server_id
        ORDER BY report_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS cpu_7d_avg
FROM server_metrics
ORDER BY server_id, report_date;
```

**Interview framing:**
> "For the capacity planning dashboard where infrastructure teams need to see current utilization across 6,000 servers in under a second, ClickHouse is the right layer. Snowflake or Athena would be the right choice for complex analytical queries run by the data team. I'd use both: real-time operational view in ClickHouse, historical analysis and modeling in Snowflake."

---

## Behavioral Anchor — Day 24

> "Tell me about a time you had to make a build-vs-buy decision."

Strong answers:
- Specific tools and trade-offs evaluated
- Decision criteria (cost, maintenance, features, team skills)
- What you decided and why
- How it played out over time (honest about trade-offs made)

---

## Day 24 Checklist

- [ ] Coded LC #739 (Daily Temperatures) using monotonic stack
- [ ] Coded LC #84 (Largest Rectangle) — understands the sentinel trick
- [ ] Coded LC #901 (Stock Span) — understands span accumulation
- [ ] Ran NTILE, PERCENT_RANK, CUME_DIST queries in DuckDB
- [ ] Wrote a LATERAL join query from scratch
- [ ] Read 5 columns of Polars DataFrame using lazy scan and `.collect()`
- [ ] Can explain the difference between Polars lazy and Pandas eager
- [ ] Can describe ClickHouse MergeTree and what `ORDER BY` does
- [ ] Can describe the Kafka Engine + Materialized View pipeline
- [ ] Know when to recommend ClickHouse vs Snowflake vs Athena
