---
created: 2026-03-02
updated: 2026-03-02
summary: Day 10 — Dynamic Programming (1D) | GROUPING SETS / ROLLUP | Pydantic + Type System | dbt
tags: [study-plan, day-10, leetcode, sql, python, dbt, dynamic-programming]
---

# Study Day 10: Optimization and Data Modeling
**Theme:** DP patterns + Advanced SQL aggregation + Python type safety + dbt for data modeling

---

## Spaced Repetition — Review from Days 1–9
*60 seconds each. Mark Strong / Review / Weak.*

**SR-1 (Day 2):** Named WINDOW clause — what does it give you and when do you use it?
> Define a window spec once with an alias (`WINDOW w AS (...)`), reference it multiple times in SELECT. Avoids repeating the same OVER() clause. Use when you need multiple window functions on the same partition/order.

**SR-2 (Day 5):** Heap — min-heap vs max-heap in Python. How do you get a max-heap?
> Python's `heapq` is a min-heap (smallest element at root). For max-heap: negate all values on push, negate again on pop. Or use a tuple `(-priority, item)` as the heap key.

**SR-3 (Day 8):** What is the BFS "level snapshot" pattern?
> `level_size = len(queue)` before the inner loop. Process exactly `level_size` nodes — they are all in the current level. Children pushed during the loop belong to the next level.

**SR-4 (Day 9):** 3Sum — why sort first and what's the duplicate-skipping rule?
> Sort enables two pointers. Skip: if `nums[i] == nums[i-1]` for the outer loop (same fixed element twice). After finding a triplet, skip equal left/right values before moving pointers.

**SR-5 (Day 9):** Kafka consumer groups — what is the max parallelism rule?
> Max consumers in a group = number of partitions. Extra consumers are idle. To increase parallelism, increase partition count before you need it (irreversible — can't decrease partitions).

**SR-6 (Day 3):** Decorator order — `@timer @log_args def f()` — what is the execution order?
> Decorators apply bottom-up (`log_args` first, then `timer`). Execution is outside-in: `timer.wrapper → log_args.wrapper → f`. Reading top-down = execution order.

---

## A. LeetCode — Dynamic Programming (1D)

> **Discussion opener:** "DP solves problems with overlapping subproblems by storing results instead of recomputing them. The mental model: define what `dp[i]` means, write the recurrence (how dp[i] depends on earlier values), and identify the base case. 1D DP is linear — dp[i] depends on dp[i-1] or dp[i-2]. 2D DP (next level) adds a second dimension like two strings or a capacity."
>
> **Two approaches:**
> - **Top-down (memoization):** Recursive with a cache. Natural to write; may hit recursion limit.
> - **Bottom-up (tabulation):** Iterative, fills dp[] from base case forward. Usually more efficient.

---

### LC #70 — Climbing Stairs [Easy]
**Category:** Dynamic Programming

**Problem:**
You can climb 1 or 2 steps at a time. How many distinct ways to reach step `n`?
`n = 3` → `3` (1+1+1, 1+2, 2+1)

🎯 **Design Checkpoint:** "To reach step n, you came from step n-1 (one step) or step n-2 (two steps). So ways(n) = ways(n-1) + ways(n-2). Sound familiar?"

**Recurrence:** `dp[i] = dp[i-1] + dp[i-2]` (Fibonacci sequence)
**Base cases:** `dp[1] = 1`, `dp[2] = 2`

**Solution 1 — DP Array** O(n) time, O(n) space
```python
def climbStairs(n: int) -> int:
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

**Solution 2 — Space-Optimized** O(n) time, O(1) space
```python
def climbStairs(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```

**Interview Q&A:**
- Q: Is this just Fibonacci? A: Yes — exactly Fibonacci with n=1→1, n=2→2 instead of 0,1. The interview tests whether you can recognize the recurrence quickly.
- Q: When do you optimize from O(n) to O(1) space? A: When dp[i] only depends on the last two values — you only need two variables, not the full array.

---

### LC #198 — House Robber [Medium]
**Category:** Dynamic Programming

**Problem:**
Houses in a line. Can't rob two adjacent houses. Each house has some amount. Maximize total loot.
`nums = [2, 7, 9, 3, 1]` → `12` (rob houses 0, 2, 4: 2+9+1=12)

🎯 **Design Checkpoint:** "For each house: rob it (get nums[i] + best from 2 houses ago) OR skip it (best from 1 house ago). dp[i] = max(dp[i-2] + nums[i], dp[i-1])."

**Recurrence:** `dp[i] = max(dp[i-2] + nums[i], dp[i-1])`
**Base cases:** `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`

**Solution** O(n) time, O(1) space
```python
def rob(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = nums[0], max(nums[0], nums[1])

    for i in range(2, len(nums)):
        curr = max(prev2 + nums[i], prev1)
        prev2, prev1 = prev1, curr

    return prev1

# Test
print(rob([2, 7, 9, 3, 1]))    # 12
print(rob([2, 1, 1, 2]))        # 4
print(rob([1, 2, 3, 1]))        # 4
```

**Interview Q&A:**
- Q: What is the recurrence's intuition? A: At each house, you make a binary choice: rob it (can't use adjacent) or skip it (use the best so far). dp[i] captures the best possible outcome up to house i.
- Q: How would House Robber II work (circular arrangement)? A: Solve twice: once excluding the first house (range 1..n-1), once excluding the last (range 0..n-2). Answer = max of both. This eliminates the adjacency conflict between first and last.

---

### LC #322 — Coin Change [Medium]
**Category:** Dynamic Programming (Unbounded Knapsack)

**Problem:**
Given coin denominations and a target amount, return the minimum number of coins needed. Return -1 if impossible.
`coins = [1, 5, 11]`, `amount = 15` → `3` (5+5+5, not 11+1+1+1+1)

🎯 **Design Checkpoint:** "dp[i] = minimum coins to make amount i. For each amount, try each coin: if coin ≤ amount, dp[i] = min(dp[i], dp[i - coin] + 1)."

**Recurrence:** `dp[i] = min(dp[i - c] + 1 for c in coins if c <= i)`
**Base case:** `dp[0] = 0`, `dp[1..amount] = infinity`

**Solution — Bottom-Up DP** O(amount × coins) time, O(amount) space
```python
def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0    # base case: 0 coins to make amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1

# Test
print(coinChange([1, 5, 11], 15))    # 3
print(coinChange([2], 3))             # -1 (impossible)
print(coinChange([1, 2, 5], 11))     # 3 (5+5+1)
```

**Interview Q&A:**
- Q: Why initialize dp to infinity? A: Impossible states should not propagate. Infinity acts as "not reachable yet."
- Q: Why does greedy fail for coin change? A: Greedy (always take the largest coin) fails: coins=[1,3,4], amount=6 → greedy gives 4+1+1=3 coins; optimal is 3+3=2 coins. DP evaluates all options.
- Q: Real-world application? A: Budget allocation — minimum number of "resource units" to meet a target. Scheduling — minimum number of batches to cover a workload.

---

### LC #300 — Longest Increasing Subsequence [Medium]
**Category:** Dynamic Programming / Binary Search

**Problem:**
Given integer array, return the length of the longest strictly increasing subsequence.
`[10, 9, 2, 5, 3, 7, 101, 18]` → `4` (2, 3, 7, 101 or 2, 5, 7, 101)

🎯 **Design Checkpoint:** "dp[i] = length of LIS ending at index i. For each i, look back at all j < i: if nums[j] < nums[i], dp[i] could extend dp[j]."

**Solution 1 — DP** O(n²) time, O(n) space
```python
def lengthOfLIS(nums: list[int]) -> int:
    dp = [1] * len(nums)    # each element is an LIS of length 1 by itself

    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

**Solution 2 — Binary Search** O(n log n) time, O(n) space
```python
import bisect

def lengthOfLIS(nums: list[int]) -> int:
    tails = []    # tails[i] = smallest tail element of LIS with length i+1

    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)    # extend the LIS
        else:
            tails[pos] = num     # replace (maintain smallest possible tail)

    return len(tails)
```

**Interview Q&A:**
- Q: What does `tails` represent in the binary search solution? A: tails[i] is the smallest possible tail value of all increasing subsequences of length i+1 seen so far. Replacing tails[pos] doesn't change LIS length — it makes future extensions more likely.
- Q: LIS application in data engineering? A: "Version ordering" — find the longest sequence of compatible software versions. Or "signal detection" — longest monotonically increasing CPU trend (sustained growth detection).

---

## B. SQL — GROUPING SETS, ROLLUP, and CUBE

> **Discussion opener:** "GROUPING SETS is the SQL equivalent of UNION ALL-ing multiple GROUP BY queries, but in one pass. ROLLUP and CUBE are shortcuts for common patterns. They appear in analytics dashboards and data warehouse summaries — multiple aggregation levels in one query."

### GROUPING SETS — Multiple Aggregations in One Pass
```sql
-- Without GROUPING SETS: three separate queries joined with UNION ALL
-- With GROUPING SETS: one pass, same result

SELECT
    region,
    tier,
    COUNT(*) AS server_count,
    ROUND(AVG(avg_cpu), 1) AS avg_cpu
FROM servers s
JOIN (
    SELECT server_id, AVG(avg_cpu) AS avg_cpu
    FROM daily_metrics
    GROUP BY server_id
) m ON s.server_id = m.server_id
GROUP BY GROUPING SETS (
    (region, tier),   -- subtotal by region + tier
    (region),         -- subtotal by region only
    ()                -- grand total
)
ORDER BY region NULLS LAST, tier NULLS LAST;

-- NULLs in output = the aggregated dimension.
-- NULL in 'tier' column = aggregated across all tiers.
-- NULL in both = grand total.
```

### ROLLUP — Hierarchical Subtotals
```sql
-- ROLLUP(a, b, c) = GROUPING SETS((a,b,c), (a,b), (a), ())
-- Perfect for hierarchical dimensions: region → tier → server

SELECT
    region,
    tier,
    COUNT(*) AS server_count
FROM servers
GROUP BY ROLLUP(region, tier)
ORDER BY region NULLS LAST, tier NULLS LAST;

-- Result includes:
--   (us-east, gold)     ← leaf level
--   (us-east, silver)
--   (us-east, NULL)     ← region subtotal
--   (us-west, gold)
--   (us-west, NULL)     ← region subtotal
--   (NULL, NULL)        ← grand total
```

### CUBE — All Combinations
```sql
-- CUBE(a, b) = GROUPING SETS((a,b), (a), (b), ())
-- Every possible combination — useful for cross-dimensional analysis

SELECT
    region,
    tier,
    COUNT(*) AS count
FROM servers
GROUP BY CUBE(region, tier);

-- Result: by (region,tier), by region alone, by tier alone, grand total
-- Useful: "show me server count by every combination of dimensions"
```

### GROUPING() Function — Distinguish NULL from Subtotal
```sql
-- Problem: real NULLs in data vs. NULLs from GROUPING SETS
-- GROUPING(col) returns 1 if the row is an aggregate for that column, 0 otherwise

SELECT
    CASE WHEN GROUPING(region) = 1 THEN 'ALL REGIONS' ELSE region END AS region,
    CASE WHEN GROUPING(tier) = 1 THEN 'ALL TIERS'    ELSE tier   END AS tier,
    COUNT(*) AS count
FROM servers
GROUP BY ROLLUP(region, tier)
ORDER BY region, tier NULLS LAST;
```

**Interview Q&A:**
- Q: What is the performance benefit of GROUPING SETS over UNION ALL? A: One table scan instead of N scans. The database optimizer recognizes GROUPING SETS and produces a single aggregation pass. With UNION ALL, each subquery scans the table independently.
- Q: When does ROLLUP make sense? A: Hierarchical dimensions — continent → country → region → city. Financial reports — company → division → department. The hierarchy is the key.
- Q: When does CUBE make sense? A: Cross-dimensional dashboards where you want to slice by every combination. "Show me sales by product × region × quarter, plus all subtotals." Star schema reporting.
- Q: What is the GROUPING() function for? A: Disambiguate between a real NULL in data and a NULL produced by ROLLUP/CUBE aggregation. Without GROUPING(), you can't tell why a cell is NULL.

---

## C. Python — Pydantic, Dataclasses, and the Type System

> **Discussion opener:** "Data pipelines fail because of bad data. Pydantic validates data at the boundary — when data enters your system. Type hints + Pydantic catch schema violations, wrong types, and missing fields at intake, not three steps later when a KeyError crashes production."

### Dataclasses — Structured Data Without Boilerplate
```python
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

@dataclass
class ServerMetric:
    server_id: str
    report_date: date
    avg_cpu: float
    region: str
    tier: str = "silver"           # default value
    alert_threshold: float = 90.0
    tags: list[str] = field(default_factory=list)  # mutable default

    def is_critical(self) -> bool:
        return self.avg_cpu >= self.alert_threshold

    def __post_init__(self):
        """Validation after __init__."""
        if not (0 <= self.avg_cpu <= 100):
            raise ValueError(f"avg_cpu must be 0-100, got {self.avg_cpu}")
        if self.server_id.strip() == "":
            raise ValueError("server_id cannot be empty")

# Usage
m = ServerMetric(
    server_id="srv-01",
    report_date=date(2026, 2, 26),
    avg_cpu=85.3,
    region="us-east",
    tier="gold"
)
print(m.is_critical())    # False
print(m)                  # ServerMetric(server_id='srv-01', ...)
```

### Pydantic — Validation at the Data Boundary
```python
from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional, Literal

class ServerMetricSchema(BaseModel):
    server_id: str = Field(min_length=1, pattern=r"^srv-\d{2}$")
    report_date: date
    avg_cpu: float = Field(ge=0.0, le=100.0)   # >= 0, <= 100
    region: Literal['us-east', 'us-west', 'eu-west']
    tier: Literal['gold', 'silver', 'bronze'] = 'silver'

    @field_validator('server_id')
    @classmethod
    def server_id_uppercase(cls, v: str) -> str:
        return v.lower()   # normalize to lowercase

# Valid data
m = ServerMetricSchema(
    server_id="srv-01",
    report_date="2026-02-26",   # auto-coerces string to date
    avg_cpu=85.3,
    region="us-east",
    tier="gold"
)
print(m.model_dump())

# Invalid data — raises ValidationError
try:
    bad = ServerMetricSchema(
        server_id="",               # fails min_length
        report_date="2026-02-26",
        avg_cpu=150.0,              # fails le=100
        region="eu-north",          # not in Literal
    )
except Exception as e:
    print(f"Validation failed:\n{e}")
```

### Pipeline Boundary Pattern — Validate on Intake
```python
from pydantic import BaseModel, ValidationError
import json

def process_incoming_event(raw_json: str) -> Optional[ServerMetricSchema]:
    """Parse and validate an incoming telemetry event at the pipeline boundary."""
    try:
        data = json.loads(raw_json)
        metric = ServerMetricSchema(**data)
        return metric
    except (json.JSONDecodeError, ValidationError) as e:
        # Log to dead-letter queue, don't crash the pipeline
        print(f"[REJECTED] Invalid event: {e}")
        return None

# Batch intake with validation reporting
def ingest_batch(events: list[str]) -> tuple[list, list]:
    valid, invalid = [], []
    for event in events:
        result = process_incoming_event(event)
        if result:
            valid.append(result)
        else:
            invalid.append(event)
    print(f"Ingested: {len(valid)} valid | {len(invalid)} rejected")
    return valid, invalid
```

**Interview Q&A:**
- Q: Pydantic vs dataclasses — when do you use each? A: Dataclasses: internal data containers where you trust the data source (Python code calling Python code). Pydantic: external data boundaries — API responses, user input, JSON from Kafka, database rows. Pydantic validates and coerces; dataclasses trust.
- Q: What is `field(default_factory=list)` and why is it required? A: Mutable defaults (list, dict) can't be shared across instances. `default_factory` creates a new instance for each object. Using `= []` directly is a Python bug — all instances share the same list.
- Q: What does `model_dump()` do? A: Converts Pydantic model to dict. `model_dump_json()` serializes to JSON string. The inverse of the constructor.
- Q: What is the dead-letter queue pattern? A: Instead of crashing on bad data, route invalid records to a "dead-letter" location (S3 path, separate Kafka topic, DynamoDB table). Allows later inspection and replay without losing valid records.

---

## D. Technology — dbt (Data Build Tool)

> **Discussion opener:** "dbt is to SQL what git is to code. It adds version control, testing, documentation, and lineage to SQL transformations. Instead of untracked SQL scripts running in Redshift or Snowflake, dbt gives you a software engineering workflow for your data models. It's now the standard in modern data engineering — if you haven't used it, you need to know the concepts."

### dbt Mental Model
```
Source data (raw tables in warehouse)
     ↓
  dbt models (SELECT statements in .sql files)
     ↓
  dbt tests (assertions about your data)
     ↓
  Compiled tables/views in the warehouse
     ↓
  Documentation + lineage graph auto-generated
```

### A dbt Model — Just a SELECT Statement
```sql
-- models/staging/stg_server_metrics.sql
-- This becomes a view (or table) in your warehouse automatically

{{ config(materialized='view') }}

SELECT
    server_id,
    report_date::DATE AS report_date,
    avg_cpu::FLOAT AS avg_cpu,
    UPPER(region) AS region,
    LOWER(tier) AS tier
FROM {{ source('raw', 'daily_metrics') }}   -- references raw source table
WHERE avg_cpu IS NOT NULL
  AND report_date >= '2026-01-01'
```

```sql
-- models/marts/server_daily_summary.sql
-- Depends on stg_server_metrics — dbt resolves dependency order automatically

{{ config(materialized='table', partition_by={'field': 'report_date', 'data_type': 'date'}) }}

WITH base AS (
    SELECT * FROM {{ ref('stg_server_metrics') }}   -- ref() links models
),
with_classification AS (
    SELECT
        *,
        CASE
            WHEN avg_cpu >= 90 THEN 'critical'
            WHEN avg_cpu >= 75 THEN 'warning'
            ELSE 'normal'
        END AS cpu_status
    FROM base
)
SELECT
    server_id,
    report_date,
    ROUND(AVG(avg_cpu), 2) AS avg_cpu,
    MAX(avg_cpu) AS peak_cpu,
    MAX(cpu_status) AS worst_status
FROM with_classification
GROUP BY server_id, report_date
```

### dbt Tests — Data Quality as Code
```yaml
# models/schema.yml — defines tests on columns
version: 2

models:
  - name: stg_server_metrics
    columns:
      - name: server_id
        tests:
          - not_null
          - unique           # each server_id+date should be unique
      - name: avg_cpu
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0
              max_value: 100
      - name: region
        tests:
          - accepted_values:
              values: ['us-east', 'us-west', 'eu-west']

  - name: server_daily_summary
    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns: [server_id, report_date]
```

### dbt Key Commands
```bash
dbt run          # compile and run all models (creates tables/views in warehouse)
dbt test         # run all schema tests
dbt docs generate && dbt docs serve    # generate + serve interactive lineage docs
dbt run --select server_daily_summary  # run one specific model
dbt run --select +server_daily_summary # run model + all its upstream dependencies
```

### dbt vs Traditional ETL
```
Traditional SQL scripts    | dbt
---------------------------|------------------------------------------
Run order: manual          | ref() resolves dependency order automatically
Testing: none / ad-hoc     | Built-in schema tests + custom data tests
Documentation: none        | Auto-generated lineage graph + column docs
Versioning: files in S3    | Git repository
Environments: manual       | profiles.yml (dev/staging/prod targets)
```

**Interview Q&A:**
- Q: What is `ref()` in dbt and why is it important? A: `ref('model_name')` links one dbt model to another. dbt uses ref() calls to build a dependency DAG and runs models in the correct order. It also resolves to the correct schema in each environment (dev vs prod).
- Q: What is materialization in dbt? A: How dbt builds the model: `view` (always queries upstream), `table` (full rebuild each run), `incremental` (only processes new rows — most efficient for large tables), `ephemeral` (CTEs, never materialized).
- Q: What are dbt sources? A: `source()` references raw tables that aren't managed by dbt (e.g., loaded by Fivetran, Glue). Sources have freshness tests — dbt can alert if raw data hasn't arrived recently.
- Q: How does dbt handle incremental models? A: On first run: full build. On subsequent runs: filters to new rows using `is_incremental()` macro and merges/inserts. Avoids reprocessing all historical data on every run.
- Q: dbt vs Airflow — what's the relationship? A: dbt transforms data (SQL logic). Airflow orchestrates pipelines (scheduling, triggering, monitoring). They work together: Airflow triggers dbt runs as part of a larger pipeline that includes extraction, loading, and downstream alerting.

---

## Today's Key Interview Talking Points

1. **"DP: define what dp[i] means, write the recurrence, identify base cases. Then optimize space if dp[i] only uses the last 1-2 values."**
2. **"GROUPING SETS = multiple GROUP BYs in one pass. ROLLUP = hierarchical subtotals. CUBE = all combinations."**
3. **"Pydantic validates at the data boundary. Dataclasses structure internal data. Don't confuse them."**
4. **"dbt is software engineering for SQL — git, tests, and lineage for your transformations."**
5. **"`ref()` is dbt's killer feature — dependency resolution and environment awareness in one function call."**
6. **"Incremental models are how dbt handles scale — only process new rows, not full history every run."**

---

## Behavioral Anchor — Citi Story #10

**Topic: Data Quality + Automation**

Practice this story (2 minutes, STAR format):

> *"One of the persistent problems at Citi was data quality in the telemetry pipeline. Agents would report metrics with wrong timestamps — sometimes future-dated by hours due to NTP drift. This would corrupt rolling averages and make dashboards show erratic capacity trends. I built a validation layer that checked timestamp sanity (reject if more than 30 minutes in the future or more than 24 hours old) and server ID validity against our inventory. What I'd do today with dbt: add schema tests on the raw source and custom data tests for timestamp bounds — catch it at the staging layer before it reaches the mart. The dead-letter queue would hold rejects for manual review."*

**Gemini: ask Sean to tell this story unprompted. Time him. Give STAR feedback.**

---

## End of Day 10 — Wrap-Up

Gemini reports:
```
Day 10 Complete.
Topics covered: DP (1D) | GROUPING SETS / ROLLUP | Pydantic + Typing | dbt
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 11: Graphs + EXPLAIN / Query Plans + concurrent.futures + Delta Lake/Iceberg
```
