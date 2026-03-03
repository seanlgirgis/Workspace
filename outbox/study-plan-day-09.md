---
created: 2026-03-02
updated: 2026-03-02
summary: Day 9 — Two Pointers | Date/Time SQL + Gaps & Islands | Python Concurrency | Kafka Deep Dive
tags: [study-plan, day-9, leetcode, sql, python, kafka, concurrency]
---

# Study Day 9: Stream and Sequence Patterns
**Theme:** Two Pointers + Time Series SQL + Concurrent Python + Kafka Architecture

---

## Spaced Repetition — Review from Days 1–8
*60 seconds each. Mark Strong / Review / Weak.*

**SR-1 (Day 1):** Product of Array Except Self — why is it O(1) extra space?
> The result array itself is used for the prefix pass. The suffix is computed with a single variable. No additional arrays needed beyond the output.

**SR-2 (Day 3):** Car Fleet — why sort by position descending, not ascending?
> Cars can only catch up to cars ahead (closer to target). Processing closest-first means when we evaluate each car, we already know the fleet it might join. Ascending order would require lookahead.

**SR-3 (Day 4):** Binary search — what is the invariant you maintain?
> The target, if it exists, is always within `[left, right]`. Every iteration eliminates at least one element. Terminates when left > right (not found) or nums[mid] == target.

**SR-4 (Day 6):** Merge Intervals — after sorting by start, what is the one condition for two intervals to overlap?
> `intervals[i][0] <= merged[-1][1]` — the next interval's start is ≤ the current merged interval's end. If true, extend the end: `merged[-1][1] = max(merged[-1][1], intervals[i][1])`.

**SR-5 (Day 8):** BFS level-order — what is the key trick to separate levels?
> `level_size = len(queue)` before the inner loop. Process exactly `level_size` nodes — they all belong to the current level. Children added during this loop belong to the next level.

**SR-6 (Day 8):** What is Airflow `catchup=False` and why does it matter?
> Prevents backfilling all missed runs since start_date. Without it, deploying a DAG with a past start_date triggers one run per missed schedule interval immediately.

---

## A. LeetCode — Two Pointers

> **Discussion opener:** "Two pointers is the pattern for problems on sorted arrays where you need pairs, triples, or a range. The trick: sorting creates structure. From a sorted array, you can move pointers intelligently — the left pointer moves right when the sum is too small, right pointer moves left when too large. This drops O(n²) brute force to O(n) after the O(n log n) sort. The sliding window IS a two-pointer pattern — the difference is that two pointers usually work from both ends while sliding window works from one end."

---

### LC #167 — Two Sum II (Input Array is Sorted) [Medium]
**Category:** Two Pointers

**Problem:**
Given a **sorted** array `numbers` (1-indexed), find two numbers that add to `target`. Return `[index1, index2]` (1-indexed). Use only O(1) extra space.
`numbers = [2, 7, 11, 15]`, `target = 9` → `[1, 2]`

🎯 **Design Checkpoint:** "The array is sorted. If the sum is too big, which pointer moves? If too small?"

**Solution — Two Pointers** O(n) time, O(1) space
```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1

    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]    # 1-indexed
        elif total < target:
            left += 1    # need bigger sum → move left right
        else:
            right -= 1   # need smaller sum → move right left

    return []   # guaranteed to have solution per problem
```

**Interview Q&A:**
- Q: Why does this work? A: Array is sorted. If sum < target, only option is to increase it → move left right (larger values). If sum > target, decrease it → move right left. We never skip a valid pair.
- Q: Why is this O(n) instead of O(n²)? A: Each pointer moves at most n steps total. No nested loops — every iteration eliminates at least one element from consideration.

---

### LC #15 — 3Sum [Medium]
**Category:** Two Pointers + Sort

**Problem:**
Given array `nums`, return all triplets `[nums[i], nums[j], nums[k]]` where `i != j != k` and `nums[i] + nums[j] + nums[k] == 0`. No duplicate triplets.
`[-1, 0, 1, 2, -1, -4]` → `[[-1,-1,2], [-1,0,1]]`

🎯 **Design Checkpoint:** "Fix one element with a for loop. Then solve Two Sum for the remaining two elements with two pointers. Skip duplicates carefully."

**Solution** O(n²) time, O(1) extra space (sorting is in-place)
```python
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        # Skip duplicate values for the fixed element
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:      # sorted: if nums[i] > 0, no triplet sums to 0
            break

        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicates for left and right
                while left < right and nums[left] == nums[left + 1]:  left += 1
                while left < right and nums[right] == nums[right - 1]: right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result
```

**Interview Q&A:**
- Q: Why sort first? A: Sorting lets us use two pointers (sorted structure) AND skip duplicates easily (equal adjacent values).
- Q: Why O(n²) and not O(n)? A: The outer loop is O(n); the inner two-pointer scan is O(n). So O(n) × O(n) = O(n²). Cannot do better without hashing which increases space.
- Q: What is the "early exit" optimization? A: `if nums[i] > 0: break` — if the smallest remaining element is positive, the sum can only be positive. No valid triplet possible.

---

### LC #11 — Container With Most Water [Medium]
**Category:** Two Pointers (Greedy)

**Problem:**
Given heights `height[]`, find two lines that together with the x-axis form a container holding the most water.
`height = [1,8,6,2,5,4,8,3,7]` → `49`

🎯 **Design Checkpoint:** "Width decreases as pointers move in. The only way to increase area is to find a taller line. So always move the shorter pointer inward."

**Solution — Two Pointers** O(n) time, O(1) space
```python
def maxArea(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        current = min(height[left], height[right]) * width
        max_water = max(max_water, current)

        # Move the shorter side — the taller side can't help with a smaller width
        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1

    return max_water
```

**Interview Q&A:**
- Q: Why move the shorter pointer? A: Area = min(left_height, right_height) × width. When we move inward, width decreases by 1. The only hope of increasing area is finding a taller line. Moving the taller line guarantees we keep or decrease the height — no upside. Moving the shorter line gives a chance to find something taller.
- Q: Is this provably optimal? A: Yes — by induction. If we move the shorter pointer, we've already computed the best area possible for that shorter line at any position (since any position to the right has ≤ width). No valid answer is skipped.

---

### LC #42 — Trapping Rain Water [Hard]
**Category:** Two Pointers (Prefix Max)

**Problem:**
Given heights `height[]`, compute total water trapped after rain.
`height = [0,1,0,2,1,0,1,3,2,1,2,1]` → `6`

🎯 **Design Checkpoint:** "Water at each position = min(max height to the left, max height to the right) - height at position. Two pointers track these maximums in O(1) space."

**Solution — Two Pointers** O(n) time, O(1) space
```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] <= height[right]:
            # Right side is at least as tall — left_max determines water level
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            # Left side is taller — right_max determines water level
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1

    return water
```

**Interview Q&A:**
- Q: Why does the two-pointer approach work? A: When `height[left] <= height[right]`, the right boundary is guaranteed ≥ `left_max`. So water at `left` is exactly `left_max - height[left]`. We don't need to know the actual right max — just that it's ≥ left_max.
- Q: What's the O(n) space solution? A: Precompute `prefix_max` (left max at each index) and `suffix_max` (right max), then iterate once. Two pointers does the same in O(1) space.
- Q: How does this relate to data engineering? A: "Windowed capacity headroom" — for each time period, what is the effective available capacity (bounded by upstream and downstream constraints)?

---

## B. SQL — Date/Time Functions and Gaps & Islands

> **Discussion opener:** "Time-series SQL is what separates data engineers from SQL developers. Gaps & islands is the interview problem that shows you understand how to detect missing data in sequences. At Citi, gap detection on server reporting was daily work."

### Core Date Functions (DuckDB / PostgreSQL)
```sql
-- Current date and arithmetic
SELECT CURRENT_DATE;                                    -- 2026-03-02
SELECT CURRENT_DATE - INTERVAL '7 days';               -- 2026-02-23
SELECT CURRENT_DATE + INTERVAL '1 month';              -- 2026-04-02

-- Date parts
SELECT EXTRACT('year'  FROM report_date) AS yr;
SELECT EXTRACT('month' FROM report_date) AS mo;
SELECT EXTRACT('dow'   FROM report_date) AS day_of_week;  -- 0=Sunday

-- Date truncation (useful for grouping by week/month)
SELECT DATE_TRUNC('week',  report_date) AS week_start;
SELECT DATE_TRUNC('month', report_date) AS month_start;

-- Difference in days
SELECT DATEDIFF('day', '2026-02-01'::DATE, '2026-02-28'::DATE);  -- 27

-- Day of week filtering (weekdays only)
SELECT * FROM daily_metrics
WHERE EXTRACT('dow' FROM report_date) NOT IN (0, 6);  -- exclude Sun/Sat
```

### Gaps & Islands — The Core Pattern
```sql
-- Problem: find consecutive date ranges where each server reported data.
-- "Islands" = consecutive blocks of reporting. "Gaps" = missing dates between islands.

-- Step 1: assign a row number and subtract from date to get a group key.
-- Consecutive dates get the SAME group_key (the "island" identifier).
WITH numbered AS (
    SELECT
        server_id,
        report_date,
        ROW_NUMBER() OVER (PARTITION BY server_id ORDER BY report_date) AS rn,
        report_date - CAST(ROW_NUMBER() OVER (
            PARTITION BY server_id ORDER BY report_date
        ) AS INT) AS island_key     -- dates in same island share this value
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
SELECT
    server_id,
    island_start,
    island_end,
    consecutive_days
FROM islands
ORDER BY server_id, island_start;
```

### Consecutive Days — Simpler Version
```sql
-- Find servers that reported data for 3 or more consecutive days
WITH daily AS (
    SELECT server_id, report_date,
           report_date - CAST(ROW_NUMBER() OVER (
               PARTITION BY server_id ORDER BY report_date
           ) AS INT) AS grp
    FROM daily_metrics
)
SELECT server_id, MIN(report_date) AS streak_start,
       MAX(report_date) AS streak_end,
       COUNT(*) AS streak_length
FROM daily
GROUP BY server_id, grp
HAVING COUNT(*) >= 3
ORDER BY streak_length DESC;
```

### Finding Actual Gaps
```sql
-- Find the gaps between islands — periods where no data was reported
WITH all_dates AS (
    -- Generate all expected dates in range
    SELECT UNNEST(generate_series(
        '2026-02-01'::DATE,
        '2026-02-28'::DATE,
        INTERVAL '1 day'
    ))::DATE AS expected_date
),
reported AS (
    SELECT DISTINCT server_id, report_date FROM daily_metrics
),
cross_product AS (
    SELECT s.server_id, d.expected_date
    FROM (SELECT DISTINCT server_id FROM daily_metrics) s
    CROSS JOIN all_dates d
)
SELECT c.server_id, c.expected_date AS missing_date
FROM cross_product c
LEFT JOIN reported r
    ON c.server_id = r.server_id AND c.expected_date = r.report_date
WHERE r.report_date IS NULL
ORDER BY c.server_id, c.expected_date;
```

**Interview Q&A:**
- Q: Explain the gaps & islands "date minus row number" trick. A: Consecutive dates form an arithmetic sequence where `date[i] - i` is constant. If any date is missing, the sequence breaks, and `date - rn` changes. All dates in the same consecutive block share the same `date - rn` value.
- Q: What is `generate_series()` and where does it work? A: PostgreSQL and DuckDB native function that generates a series of dates or numbers. Snowflake equivalent: `GENERATOR(rowcount=>N)`. BigQuery: unnest a date range. SQL Server: recursive CTE.
- Q: How would you find the longest streak? A: Islands query → MAX(consecutive_days). Tie-break by island_start.

---

## C. Python — Threading, Multiprocessing, and asyncio

> **Discussion opener:** "Python has three concurrency models and they solve different problems. Threading: I/O-bound tasks — waiting for network, disk, API. Multiprocessing: CPU-bound tasks — computation, data processing. asyncio: highly concurrent I/O with many connections — APIs, sockets. The GIL is the key: threading doesn't give you parallelism for CPU work, but it does work for I/O waits."

### The Three Models
```
Model          | Parallelism | Best For           | GIL Impact
---------------|-------------|--------------------|-----------
threading      | Concurrent  | I/O-bound (API)    | GIL blocks CPU work
multiprocessing| Parallel    | CPU-bound (compute)| Separate process each
asyncio        | Concurrent  | Many I/O connects  | Single thread, event loop
```

### Threading — Parallel API Calls
```python
import threading
import time
from concurrent.futures import ThreadPoolExecutor

def fetch_server_status(server_id: str) -> dict:
    """Simulate an API call — I/O bound."""
    time.sleep(0.1)   # network latency simulation
    return {"server_id": server_id, "status": "ok", "cpu": 72.5}

SERVER_IDS = [f"srv-{i:02d}" for i in range(1, 11)]   # 10 servers

# Sequential: 10 × 0.1s = ~1.0s
start = time.perf_counter()
results = [fetch_server_status(sid) for sid in SERVER_IDS]
print(f"Sequential: {time.perf_counter() - start:.2f}s")   # ~1.0s

# ThreadPoolExecutor: concurrent I/O — all 10 run simultaneously
start = time.perf_counter()
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_server_status, SERVER_IDS))
print(f"ThreadPool: {time.perf_counter() - start:.2f}s")   # ~0.1s
print(f"Results: {len(results)} servers polled")
```

### Multiprocessing — Parallel CPU Work
```python
from concurrent.futures import ProcessPoolExecutor
import numpy as np

def compute_rolling_stats(server_data: tuple) -> dict:
    """CPU-bound: compute statistics for a server's time series."""
    server_id, readings = server_data
    arr = np.array(readings)
    return {
        "server_id": server_id,
        "mean": float(arr.mean()),
        "p95": float(np.percentile(arr, 95)),
        "std": float(arr.std()),
    }

# Generate sample data
server_datasets = [
    (f"srv-{i:02d}", list(np.random.uniform(40, 100, 10000)))
    for i in range(1, 9)
]

# Sequential
start = time.perf_counter()
results = [compute_rolling_stats(d) for d in server_datasets]
print(f"Sequential: {time.perf_counter() - start:.3f}s")

# ProcessPoolExecutor — uses multiple CPU cores
start = time.perf_counter()
with ProcessPoolExecutor() as executor:
    results = list(executor.map(compute_rolling_stats, server_datasets))
print(f"ProcessPool: {time.perf_counter() - start:.3f}s")
```

### asyncio — Concurrent I/O with Many Connections
```python
import asyncio
import time

async def async_fetch_metrics(server_id: str) -> dict:
    """Async version — yields control during I/O wait."""
    await asyncio.sleep(0.1)   # simulates network wait
    return {"server_id": server_id, "cpu": 72.5}

async def fetch_all_servers(server_ids: list[str]) -> list[dict]:
    """Run all fetches concurrently."""
    tasks = [async_fetch_metrics(sid) for sid in server_ids]
    return await asyncio.gather(*tasks)    # all run concurrently

# Run the event loop
SERVER_IDS = [f"srv-{i:02d}" for i in range(1, 21)]   # 20 servers
start = time.perf_counter()
results = asyncio.run(fetch_all_servers(SERVER_IDS))
print(f"asyncio ({len(results)} servers): {time.perf_counter() - start:.2f}s")
# ~0.1s for 20 servers (vs 2.0s sequential)
```

**Interview Q&A:**
- Q: What is the GIL and why does it matter? A: Global Interpreter Lock — Python's mutex that allows only one thread to execute Python bytecode at a time. Threading doesn't give parallelism for CPU-bound work. For CPU parallelism: use multiprocessing (separate processes, separate GILs).
- Q: When would you use threading vs multiprocessing in a data pipeline? A: Threading for fetching data from many APIs/databases concurrently (I/O bound). Multiprocessing for data transformation, feature engineering, or stats computation on large DataFrames (CPU bound).
- Q: What is `asyncio.gather()`? A: Runs multiple coroutines concurrently within the same event loop. Returns when all coroutines complete. Equivalent to Promise.all() in JavaScript.
- Q: What is `concurrent.futures` and why prefer it over raw threading/multiprocessing? A: High-level interface that abstracts both ThreadPoolExecutor and ProcessPoolExecutor. Same API, you just swap the class. Cleaner than managing threads manually.

---

## D. Technology — Kafka Deep Dive

> **Discussion opener:** "You mentioned Kafka in Day 3 (Lambda/Kappa). Today we go deep. Kafka is the backbone of real-time data pipelines — at Citi scale, Kafka handles millions of messages/sec. The key mental model: Kafka is a distributed, append-only commit log. Understanding partitions, consumer groups, and offsets is what separates the engineers who have used Kafka from those who have operated it."

### Kafka Architecture
```
Producers                   Kafka Cluster                  Consumers
─────────                   ─────────────                  ─────────
APM agent 1 ──→ Topic: server-metrics
APM agent 2 ──→   Partition 0: [msg1][msg3][msg5]  ──→ Consumer Group A
APM agent 3 ──→   Partition 1: [msg2][msg4][msg6]  ──→   Consumer A1 (reads P0)
APM agent 4 ──→   Partition 2: [msg7][msg8][msg9]  ──→   Consumer A2 (reads P1)
                                                           Consumer A3 (reads P2)

                  (Each partition is an ordered, immutable log)
                  (Consumers track their position with an OFFSET)
```

### Core Concepts — One-Line Definitions
```
Concept          | What it is
-----------------|------------------------------------------------------------
Topic            | Named stream of records — like a table name
Partition        | Ordered, immutable log segment of a topic. Unit of parallelism.
Offset           | Position of a message within a partition. Monotonically increasing.
Consumer Group   | Set of consumers that share topic consumption. Each partition → 1 consumer.
Replication      | Each partition has N replicas on N brokers. One is the leader (handles reads/writes).
Retention        | How long messages are kept (time or size). Default: 7 days.
Producer ACK     | acks=0 (fire-forget), acks=1 (leader only), acks=all (all replicas — safest)
```

### Parallelism Rule
```
Max consumers in a group = number of partitions in the topic.

10 partitions → max 10 consumers in parallel.
If you have 12 consumers, 2 are idle.
If you have 5 consumers, some read 2 partitions.

Scaling strategy: increase partition count BEFORE you need it.
Partitions cannot be reduced. Set them right the first time.
```

### Offset Management — The Source of Data Loss and Duplication
```python
# At-most-once: commit before processing (can lose data)
# consumer.commit() THEN process_message(msg)   # if processing fails, message is skipped

# At-least-once: process then commit (can duplicate)
# process_message(msg) THEN consumer.commit()   # if commit fails, message reprocessed

# Exactly-once: idempotent producer + transactional consumer
# Kafka guarantees + idempotent writes to sink (e.g., upsert by primary key)
```

### Key Guarantees
```
Guarantee         | What it means for you
------------------|--------------------------------------------------
Ordering          | Guaranteed WITHIN a partition only. Use same key → same partition.
At-least-once     | Default consumer behavior. Design sinks to be idempotent.
Exactly-once      | Kafka Streams / Flink with transactions. More complex, more expensive.
Replication       | replication.factor=3 = 3 copies. Can survive 2 broker failures.
```

### Citi Context — 6,000 Endpoints
```
6,000 APM agents → Kafka Topic: telemetry.server.metrics
  Partition count: 12   (one per APM source pool, roughly)
  Replication: 3        (standard for production)
  Retention: 7 days     (allows replay of up to 1 week)
  Message key: server_id (ensures all metrics for one server → same partition → ordered)

Consumer Group A: Flink streaming job (real-time alerts, 5-minute windows)
Consumer Group B: S3 sink connector (Parquet files, 5-minute micro-batches)

Both groups read independently — neither blocks the other.
```

**Interview Q&A:**
- Q: Why is message ordering only guaranteed within a partition? A: Each partition is an independent ordered log. Messages across partitions have no global order. If you need ordering for a specific entity (server_id), use that entity as the message key — Kafka routes all messages with the same key to the same partition.
- Q: What happens when a consumer joins or leaves a consumer group? A: Rebalance — partitions are redistributed among current consumers. During rebalance, consumption pauses. Large consumer groups with frequent changes = frequent pauses. Design for it.
- Q: What is a consumer lag and why does it matter? A: Difference between the latest offset in a partition and the consumer's current offset. High lag = consumer is falling behind. Alert on lag, not just throughput.
- Q: What is log compaction? A: Retention mode where Kafka keeps only the latest message for each key (instead of time-based retention). Useful for event sourcing / CDC — keeps the "current state" for each entity indefinitely.
- Q: Kafka vs Kinesis — when do you use each? A: Kafka: on-prem, self-managed, or MSK (managed Kafka on AWS), open source ecosystem, high throughput. Kinesis: pure AWS, simpler ops, tighter AWS integration (Lambda triggers, Firehose). At Citi: Kafka. At a small AWS-native team: Kinesis.

---

## Today's Key Interview Talking Points

1. **"Two pointers always requires sorted input. The movement rule is: move the pointer that can still improve the result."**
2. **"Gaps & islands: `date - ROW_NUMBER()` is constant for consecutive dates. That's the group key."**
3. **"Threading for I/O, multiprocessing for CPU, asyncio for many concurrent I/O connections."**
4. **"Kafka partition count = maximum consumer parallelism. Set it right — you can't decrease."**
5. **"Consumer lag is the health metric for Kafka — not throughput alone."**
6. **"Message key determines partition — use entity ID as key to guarantee per-entity ordering."**

---

## Behavioral Anchor — Citi Story #9

**Topic: Scale + Parallel Processing**

Practice this story (2 minutes, STAR format):

> *"At Citi we collected telemetry from four APM tools on different schedules — some every 5 minutes, some every 30. The challenge was that the collection jobs were serial — each tool's data had to finish before the next started. Total collection window was over an hour. I proposed parallelizing the collectors: each APM tool gets its own collection process. They run concurrently and write to a shared staging table keyed by source. Collection window dropped from 60+ minutes to about 20 — the longest single-tool collection time. The key insight was that the tools had no dependency on each other, so serial execution was purely accidental coupling."*

**Gemini: ask Sean to tell this story unprompted. Time him. Give STAR feedback.**

---

## End of Day 9 — Wrap-Up

Gemini reports:
```
Day 9 Complete.
Topics covered: Two Pointers | Date/Time SQL + Gaps & Islands | Concurrency | Kafka
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 10: Dynamic Programming + GROUPING SETS/ROLLUP + Pydantic/Typing + dbt
```
