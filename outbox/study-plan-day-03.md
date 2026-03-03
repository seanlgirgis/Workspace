---
created: 2026-02-28
updated: 2026-02-28
summary: Day 3 — Stack & Monotonic Patterns | SQL JOINs | Python Decorators | Pipeline Architecture
tags: [study-plan, day-3, leetcode, sql, python, pipeline]
---

# Study Day 3: Stack, Joins, and Pipeline Thinking
**Theme:** Stack patterns + SQL JOINs + Decorators + Lambda/Kappa Architecture

---

## Spaced Repetition — Review from Days 1-2
*60 seconds each.*

**SR-1:** Product of Array Except Self — what's the key insight? No division allowed.
> Prefix product × suffix product. Two passes — one left-to-right building prefix, one right-to-left multiplying suffix.

**SR-2:** Sliding window — when does the left pointer move?
> When the window becomes invalid (constraint violated). Exact trigger depends on problem: duplicate found, too many replacements used, etc.

**SR-3:** What is a named WINDOW clause in SQL?
> Defines the window once with an alias. Reused in multiple OVER() references — DRY SQL. `WINDOW w AS (PARTITION BY x ORDER BY y ROWS BETWEEN...)`

**SR-4:** What is a Spark shuffle and why is it expensive?
> Data redistribution across nodes — triggered by groupBy, join, repartition. Writes to disk and sends over network. #1 performance bottleneck.

**SR-5:** Pandas `transform()` vs `agg()` — output shape?
> `agg()` reduces to one row per group. `transform()` returns same shape as input — like window PARTITION BY, each row gets the group statistic.

---

## A. LeetCode — Stack

> **Discussion opener:** "Stack problems follow one pattern: use a stack to remember 'unresolved' items while scanning. When you find the trigger that resolves them, pop and process. Monotonic stacks extend this — they maintain sorted order to answer 'what's the next greater/smaller element?' in O(n)."

---

### LC #20 — Valid Parentheses [Easy]
**Category:** Stack

**Problem:**
Given string `s` containing `()[]{}`, return true if it's valid.
Valid: every opener has a matching closer in correct order.
`"()[]{}"` → true | `"(]"` → false | `"([)]"` → false

🎯 **Design Checkpoint:** "When you see an opener, push it. When you see a closer, what do you check?"

**Solution** O(n) time, O(n) space
```python
def isValid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()

    return len(stack) == 0
```
*The insight: push openers. For each closer, the top of stack must be its matching opener.*

**Interview Q&A:**
- Q: Why check `not stack` before `stack[-1]`? A: If stack is empty and we see a closer, it's immediately invalid. Short-circuit before the index.
- Q: Real application? A: Validating nested structures — JSON, XML, nested SQL subqueries, Spark job configs.

---

### LC #155 — Min Stack [Medium]
**Category:** Stack with auxiliary state

**Problem:**
Design a stack that supports push, pop, top, and `getMin()` — all in O(1).

🎯 **Design Checkpoint:** "The challenge: getMin() after popping the current minimum. How do you know what the previous minimum was?"

**Solution — Two stacks** O(1) all operations
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []  # tracks minimum at each state

    def push(self, val):
        self.stack.append(val)
        # Push current minimum: new val or existing min, whichever is smaller
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self):
        self.stack.pop()
        self.min_stack.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.min_stack[-1]
```
*The insight: min_stack[-1] always holds the current minimum. When you pop the main stack, you pop min_stack too — the previous minimum is now exposed.*

**Interview Q&A:**
- Q: What's the space trade-off? A: Double the space — O(n) for both stacks. Worth it for O(1) getMin.
- Q: How would you track the maximum instead? A: Same pattern — max_stack[-1] holds current max.

---

### LC #739 — Daily Temperatures [Medium]
**Category:** Monotonic Stack

**Problem:**
Given array `temperatures`, for each day return how many days until a warmer temperature. If no warmer day exists, return 0.
Input: `[73,74,75,71,69,72,76,73]` → `[1,1,4,2,1,1,0,0]`

🎯 **Design Checkpoint:** "You want 'the next greater element to the right' for each position. A monotonic decreasing stack stores unresolved indices — when do they get resolved?"

**Solution — Monotonic Stack** O(n) time, O(n) space
```python
def dailyTemperatures(temperatures):
    result = [0] * len(temperatures)
    stack = []  # stores indices of unresolved days (decreasing temperature order)

    for i, temp in enumerate(temperatures):
        # Current temp is warmer than stack top → resolve it
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day
        stack.append(i)

    return result
    # Any remaining indices in stack stay 0 (no warmer day found)
```
*The insight: stack holds indices of days "waiting for a warmer day." When a warmer day arrives, pop and calculate the gap.*

**Interview Q&A:**
- Q: Why monotonic decreasing? A: We only push when current temp ≤ stack top. This maintains decreasing order so we always know the top is waiting for something warmer.
- Q: What's amortized O(n)? A: Each index is pushed and popped at most once. Inner while loop's total work across all iterations ≤ n.
- Q: Data engineering application? A: "Next time a metric exceeds its previous peak" — anomaly first-occurrence detection.

---

### LC #853 — Car Fleet [Medium]
**Category:** Stack / Sorting

**Problem:**
`n` cars head to target. Given `position[]` and `speed[]`. Cars that catch up form a fleet (the faster car slows to the slower's speed). Return number of fleets.
`target=12`, `position=[10,8,0,5,3]`, `speed=[2,4,1,1,3]` → `3`

🎯 **Design Checkpoint:** "Sort by position descending. When does a car join the car ahead's fleet?"

**Solution** O(n log n)
```python
def carFleet(target, position, speed):
    # Pair and sort by position descending (closest to target first)
    pairs = sorted(zip(position, speed), reverse=True)
    stack = []  # time to reach target for each fleet

    for pos, spd in pairs:
        time = (target - pos) / spd
        # If this car arrives AFTER the fleet ahead, it's a new fleet
        if not stack or time > stack[-1]:
            stack.append(time)
        # Otherwise it joins the fleet ahead (slower car determines fleet time)

    return len(stack)
```

**Interview Q&A:**
- Q: Why sort descending? A: Process from closest to target outward. A car can only catch up to one ahead of it.
- Q: Why is arrival time the comparison? A: If the car behind arrives before or at the same time as the one ahead, it catches up → same fleet.

---

### LC #84 — Largest Rectangle in Histogram [Hard]
**Category:** Monotonic Stack
**Workbench:** D:\LeetCode\LC_0084.ipynb

> Already in vault at `/code/lc-0084-largest-rectangle-histogram.md`. Run the Q&A only.

**Drill Q&A (no code — from memory):**
- Q: What does the monotonic stack store? A: Pairs of (starting_index, height) — bars waiting to be resolved.
- Q: When do you pop a bar from the stack? A: When the current bar is shorter — it blocks the waiting bar from extending further right.
- Q: What happens to bars still in the stack after the loop? A: They were never blocked on the right — extend to the end of the array. Loop through stack: `area = height × (len(heights) - starting_index)`.
- Q: Time complexity and why? A: O(n) amortized — each bar pushed and popped at most once.

---

## B. SQL — Complex JOINs

> **Discussion opener:** "Most candidates know INNER JOIN. What separates seniors: self-joins, cross joins for combinations, and anti-joins for 'what's missing.' These show up constantly in data quality and gap-detection queries."

### Self Join — compare rows within the same table
```sql
-- Find all pairs of servers in the same region with >20% CPU difference
SELECT
    a.server_id AS server_1,
    b.server_id AS server_2,
    a.region,
    ABS(a.avg_cpu - b.avg_cpu) AS cpu_gap
FROM server_summary a
JOIN server_summary b
    ON a.region = b.region
    AND a.server_id < b.server_id   -- avoid duplicates (a,b) and (b,a)
WHERE ABS(a.avg_cpu - b.avg_cpu) > 20
ORDER BY cpu_gap DESC;
```

### Anti-Join — find missing records
```sql
-- Servers that reported NO data yesterday (data gap detection)

-- Method 1: LEFT JOIN + NULL check
SELECT s.server_id
FROM servers s
LEFT JOIN daily_metrics m
    ON s.server_id = m.server_id
    AND m.report_date = CURRENT_DATE - INTERVAL '1 day'
WHERE m.server_id IS NULL;

-- Method 2: NOT EXISTS (often more readable)
SELECT server_id
FROM servers s
WHERE NOT EXISTS (
    SELECT 1 FROM daily_metrics m
    WHERE m.server_id = s.server_id
    AND m.report_date = CURRENT_DATE - INTERVAL '1 day'
);

-- Method 3: NOT IN (careful with NULLs!)
SELECT server_id FROM servers
WHERE server_id NOT IN (
    SELECT server_id FROM daily_metrics
    WHERE report_date = CURRENT_DATE - INTERVAL '1 day'
    -- If any server_id in subquery is NULL, entire NOT IN returns nothing!
);
```

### Cross Join — generate all combinations
```sql
-- Generate all (server, metric_type) combinations for a dashboard grid
SELECT s.server_id, m.metric_type, 'N/A' AS value
FROM servers s
CROSS JOIN (VALUES ('cpu'), ('memory'), ('disk'), ('network')) AS m(metric_type);
-- Then LEFT JOIN with actual metrics to fill in real values
```

### USING vs ON
```sql
-- USING: when columns have same name in both tables
SELECT * FROM servers JOIN metrics USING (server_id);
-- ON: explicit column mapping (more flexible)
SELECT * FROM servers s JOIN metrics m ON s.id = m.server_id;
```

**Interview Q&A:**
- Q: Why is `NOT IN` with a subquery dangerous? A: If the subquery returns any NULL, the NOT IN condition returns NULL for every row — nothing matches. Always use NOT EXISTS or LEFT JOIN + NULL check.
- Q: Self-join use case in data engineering? A: Year-over-year comparison (join table to itself on year offset), sequential record pairing, hierarchy traversal.
- Q: What's a hash join? A: Build a hash table from the smaller table, probe it with the larger. O(n+m). Most databases choose this over nested loop for large joins.
- Q: What's a broadcast join in Spark? A: Small table replicated to all executors — avoids shuffle. Use when one side is small (< few hundred MB). `broadcast(df_small)` hint in PySpark.

---

## C. Python — Decorators & Context Managers

> **Discussion opener:** "Decorators are functions that wrap other functions — they add behavior without modifying the original code. Context managers ensure cleanup happens. Both are fundamental to production Python pipelines."

### Decorators — timing, logging, retry
```python
import functools
import time
import logging

# Basic decorator structure
def my_decorator(func):
    @functools.wraps(func)  # preserves func.__name__, __doc__
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper

# Timing decorator — useful for pipeline profiling
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logging.info(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

# Retry decorator — resilient data pipeline calls
def retry(max_attempts=3, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logging.warning(f"Attempt {attempt+1} failed: {e}. Retrying...")
                    time.sleep(delay * (2 ** attempt))  # exponential backoff
        return wrapper
    return decorator

@timer
@retry(max_attempts=3, delay=2.0)
def fetch_server_metrics(server_id):
    # API call that might fail transiently
    pass
```

### Context Managers — guaranteed cleanup
```python
# Class-based
class DatabaseConnection:
    def __init__(self, connection_string):
        self.conn_str = connection_string
        self.conn = None

    def __enter__(self):
        self.conn = connect(self.conn_str)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()  # always runs — even if exception
        return False  # don't suppress exceptions

# Generator-based (simpler)
from contextlib import contextmanager

@contextmanager
def managed_spark_session(app_name):
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    try:
        yield spark
    finally:
        spark.stop()  # always stops — even on crash

# Usage
with managed_spark_session("etl-job") as spark:
    df = spark.read.parquet("s3://input/")
    df.write.parquet("s3://output/")
# spark.stop() guaranteed here
```

**Interview Q&A:**
- Q: What does `@functools.wraps` do and why does it matter? A: Preserves the wrapped function's metadata (__name__, __doc__). Without it, all your decorated functions have the name "wrapper" — breaks logging and debugging.
- Q: What are the three arguments to `__exit__`? A: exc_type, exc_val, exc_tb — exception info if one occurred, all None if clean exit. Return True to suppress the exception, False to re-raise.
- Q: When would you use a retry decorator in data engineering? A: API calls to external systems (Datadog, AWS, monitoring endpoints) — transient network errors are common. Use exponential backoff to avoid thundering herd.
- Q: Why use a context manager for a Spark session? A: Guarantees `spark.stop()` runs even if the job crashes — releases cluster resources immediately rather than waiting for timeout.

---

## D. Technology — Pipeline Architecture: Lambda & Kappa

> **Discussion opener:** "Data pipeline architecture boils down to: batch vs streaming vs hybrid. Lambda architecture separates batch (complete, slow) from streaming (fast, approximate) and merges them for a serving layer. Kappa simplifies this by treating everything as a stream."

### Lambda Architecture
```
Source Data
    ↓
    ├── BATCH LAYER (Hadoop/Spark)
    │   Process all historical data
    │   Hours/days latency, complete accuracy
    │   Output: batch views
    │
    └── SPEED LAYER (Kafka/Flink/Kinesis)
        Process recent data in real-time
        Seconds latency, may be approximate
        Output: real-time views
              ↓
        SERVING LAYER (merges both views)
              ↓
        Query (reads from both, speed layer fills recency gap)
```

**Lambda pros/cons:**
- Pro: batch layer is always correct; speed layer gives recency
- Con: maintain TWO codebases for the same logic — drift is a real problem

### Kappa Architecture (simplified Lambda)
```
Source Data → Kafka (append-only log, all history retained)
                ↓
        Stream Processing (Flink/Spark Streaming)
        ONE codebase, process as stream
                ↓
        Serving Layer (Cassandra, DynamoDB, S3)
                ↓
        Query

Reprocessing: replay from Kafka beginning — same code, new version
```

**Kappa pros/cons:**
- Pro: one codebase, simpler operations, reprocessing = replay
- Con: keeping full history in Kafka is expensive; not all stream engines handle complex batch logic well

### Real Example — Telemetry Pipeline at Scale
```
6,000 agents
    → Kafka (10 partitions, 7-day retention)
    → Flink job (sliding window alerts, 5-min aggregates)
    → S3 (raw Parquet, partitioned by date)
    → Glue crawler (auto-update catalog)
    → Athena (ad-hoc SQL for capacity team)
    → Scheduled Glue ETL (daily summaries, Prophet forecasting input)
    → Dashboard (QuickSight)
```

**Interview Q&A:**
- Q: Why would you choose Kappa over Lambda? A: Simpler maintenance — one codebase, one team, easier to reason about. Modern stream processors (Flink) handle batch semantics well enough.
- Q: What is "late data" and how do you handle it? A: Events that arrive after their expected window has closed. Solutions: watermarks (tolerate N minutes of lateness), upsert to the target table, or reprocess from source.
- Q: What is exactly-once semantics? A: Guarantee that each event is processed exactly once — not duplicated, not lost. Hard to achieve; at-least-once + idempotent sinks is a practical alternative.
- Q: How would you design a pipeline for 6,000 endpoints producing 1 metric per second? A: 6,000 events/sec → Kinesis (10 shards) → Lambda or Flink → S3 (5-min micro-batches in Parquet) → Athena. Alert tier: stream directly from Kinesis with threshold rules.

---

## Today's Key Interview Talking Points

1. **"Monotonic stack solves 'next greater element' in O(n) — the key is each element enters and exits the stack at most once."**
2. **"Anti-join with NOT IN is a NULL trap. Always use NOT EXISTS or LEFT JOIN + IS NULL check."**
3. **"Decorators add behavior — timing, logging, retry — without touching the original function. `@functools.wraps` is non-negotiable."**
4. **"Lambda architecture's main weakness: two codebases for the same logic drift apart over time. Kappa solves this with replay."**

---

## Behavioral Anchor — Citi Story #3

**Topic: Reliability / Data Quality**

> *"At Citi, telemetry gaps were a silent killer — if an agent stopped reporting, we wouldn't know for hours. I built a daily SQL check using anti-join pattern: LEFT JOIN the expected server list to actual reports, WHERE report IS NULL. This ran every morning and flagged any server that went dark overnight. We reduced gap detection time from hours to minutes."*

---

## End of Day 3 — Wrap-Up

Gemini reports:
```
Day 3 Complete.
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 4: Binary Search + Query Optimization + NumPy + APM/Observability
```
