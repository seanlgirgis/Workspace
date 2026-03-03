---
created: 2026-02-28
updated: 2026-02-28
summary: Day 2 — Sliding Window | Advanced Window Functions | Pandas | Apache Spark
tags: [study-plan, day-2, leetcode, sql, python, spark]
---

# Study Day 2: Time Series Patterns
**Theme:** Sliding Window + Advanced SQL Windows + Pandas + Spark Architecture

---

## Spaced Repetition — Review from Day 1
*60 seconds each. No peeking.*

**SR-1:** Two Sum — what data structure and what's the key insight?
> HashMap. Store `complement → index`. One pass: for each number, check if `target - num` is already seen.

**SR-2:** What is a CTE and when does it NOT improve performance?
> Named intermediate result set for readability. Does NOT improve performance — optimizer usually treats it like a subquery. Use temp tables when you need indexes or multiple references.

**SR-3:** Generator vs list comprehension — which do you use for a 10GB file?
> Generator — lazy evaluation, one item at a time. List comp builds everything in memory.

**SR-4:** In AWS, what is Athena pricing based on and how do you reduce cost?
> Per TB scanned. Reduce cost with Parquet (columnar) + S3 partitioning (partition pruning skips irrelevant files).

**SR-5:** Window functions vs GROUP BY — what's the key difference?
> Window functions keep all rows. GROUP BY collapses to one row per group.

---

## A. LeetCode — Sliding Window

> **Discussion opener:** "Sliding window is the pattern for any problem involving a contiguous subarray or substring. Instead of checking every subarray (O(n²)), you maintain a window with two pointers that expand and contract — O(n). This directly maps to time-series analysis: rolling metrics, moving averages, anomaly detection windows."

---

### LC #121 — Best Time to Buy and Sell Stock [Easy]
**Category:** Sliding Window / Two Pointers

**Problem:**
Given array `prices` where `prices[i]` is the price on day i, return maximum profit from one buy + one sell. Return 0 if no profit.
Input: `[7,1,5,3,6,4]` → `5` (buy at 1, sell at 6)

🎯 **Design Checkpoint:** "You need the minimum buy price to the LEFT of each sell day. How do you track that in one pass?"

**Solution 1 — Brute Force** O(n²)
```python
def maxProfit(prices):
    max_p = 0
    for i in range(len(prices)):
        for j in range(i+1, len(prices)):
            max_p = max(max_p, prices[j] - prices[i])
    return max_p
```

**Solution 2 — One Pass** O(n) time, O(1) space
```python
def maxProfit(prices):
    min_price = float('inf')
    max_profit = 0
    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price
    return max_profit
```
*The insight: track the minimum seen so far. At each price, potential profit = current - min.*

**Interview Q&A:**
- Q: Why is this relevant to data engineering? A: Identical pattern to finding max delta in a metric time series — peak CPU above rolling baseline.
- Q: How would you modify this for "best buy and sell twice"? A: LC #123 — requires tracking state for two transactions. DP approach.

---

### LC #3 — Longest Substring Without Repeating Characters [Medium]
**Category:** Sliding Window + HashSet

**Problem:**
Given string `s`, return length of longest substring without repeating characters.
`"abcabcbb"` → `3` ("abc") | `"bbbbb"` → `1` | `"pwwkew"` → `3` ("wke")

🎯 **Design Checkpoint:** "Two pointers: left and right. Right expands. When does left move?"

**Solution — Sliding Window** O(n) time, O(min(n,m)) space where m = charset size
```python
def lengthOfLongestSubstring(s):
    char_index = {}   # char → most recent index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char is in window, move left past its last occurrence
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```
*The insight: when we see a repeat, jump left pointer past the previous occurrence — not just one step.*

**Interview Q&A:**
- Q: Why store the index instead of just using a set? A: So we can jump left directly instead of shrinking one step at a time.
- Q: What's the space complexity? A: O(min(n, m)) where m is the character set size — bounded by the alphabet.

---

### LC #424 — Longest Repeating Character Replacement [Medium]
**Category:** Sliding Window + HashMap

**Problem:**
Given string `s` and integer `k` (replacements allowed), return length of longest substring containing the same letter after at most `k` replacements.
`"AABABBA"`, k=1 → `4` ("AABA" → replace B → "AAAA")

🎯 **Design Checkpoint:** "The window is valid if: (window size - count of most frequent char) ≤ k. Why?"

**Solution — Sliding Window** O(n) time, O(1) space
```python
def characterReplacement(s, k):
    count = {}
    left = 0
    max_count = 0   # max freq of any single char in current window
    result = 0

    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_count = max(max_count, count[s[right]])

        # Characters to replace = window_size - most_frequent_char_count
        while (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1

        result = max(result, right - left + 1)

    return result
```

**Interview Q&A:**
- Q: Why don't we update max_count when we shrink the window? A: We only care about the max count that ever existed — we want the largest valid window, so we never shrink max_count.
- Q: What does this pattern tell you about time series? A: Longest period where a metric stayed within k deviations — anomaly tolerance windows.

---

### LC #239 — Sliding Window Maximum [Hard]
**Category:** Deque (Monotonic Queue)

> **Note:** This is a hard problem directly relevant to capacity planning — rolling maximum CPU/memory over a window.

**Problem:**
Given array `nums` and window size `k`, return array of maximums for each window.
Input: `nums = [1,3,-1,-3,5,3,6,7]`, k=3 → `[3,3,5,5,6,7]`

🎯 **Design Checkpoint:** "You need the max of a sliding window in O(1) per window. What if you maintained a decreasing deque — front always holds the index of the current max?"

**Solution — Monotonic Deque** O(n) time, O(k) space
```python
from collections import deque
def maxSlidingWindow(nums, k):
    dq = deque()   # stores indices, decreasing order of values
    result = []

    for i, num in enumerate(nums):
        # Remove elements outside window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Maintain decreasing order: remove smaller elements from back
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Window is full
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```
*The insight: deque front = current window max. Remove from front when index goes out of window. Remove from back when a larger element enters (those smaller elements can never be the max).*

**Interview Q&A:**
- Q: How is this O(n) if we have inner while loops? A: Each element is added and removed from the deque at most once — amortized O(n) total.
- Q: Real use case? A: Rolling maximum metric over a window — "what was the peak CPU in the last 5 minutes?" At Citi this would be the exact query for capacity alert thresholds.

---

### LC #76 — Minimum Window Substring [Hard]
**Category:** Sliding Window + HashMap

**Problem:**
Given strings `s` and `t`, return minimum window in `s` that contains all chars of `t`.
`s = "ADOBECODEBANC"`, `t = "ABC"` → `"BANC"`

🎯 **Design Checkpoint:** "Expand right until window is valid. Then shrink left as much as possible while still valid."

**Solution** O(n+m) time
```python
from collections import Counter
def minWindow(s, t):
    if not t or not s: return ""
    need = Counter(t)
    have, required = 0, len(need)
    left = 0
    result = ""
    window = {}

    for right, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        if char in need and window[char] == need[char]:
            have += 1

        while have == required:
            # Valid window — try to shrink
            window_size = right - left + 1
            if not result or window_size < len(result):
                result = s[left:right+1]
            # Shrink from left
            left_char = s[left]
            window[left_char] -= 1
            if left_char in need and window[left_char] < need[left_char]:
                have -= 1
            left += 1

    return result
```

**Interview Q&A:**
- Q: What does "have == required" track? A: Number of characters from `t` whose count in the window meets or exceeds what's needed.
- Q: What's the two-pointer general strategy? A: Right expands to find valid window. Left contracts to minimize it. Repeat.

---

## B. SQL — Advanced Window Functions

> **Discussion opener:** "You know the basics. What separates senior candidates is knowing NTILE, PERCENT_RANK, FIRST_VALUE/LAST_VALUE, and named window frames. These show up in business analytics — cohort ranking, percentile scoring, gap detection."

### NTILE — Percentile Buckets
```sql
-- Divide servers into 4 quartiles by CPU utilization
SELECT
    server_id,
    avg_cpu,
    NTILE(4) OVER (ORDER BY avg_cpu DESC) AS quartile
    -- Q1 = top 25%, Q4 = bottom 25%
FROM server_daily_summary;
```

### PERCENT_RANK and CUME_DIST
```sql
SELECT
    server_id,
    avg_cpu,
    ROUND(PERCENT_RANK() OVER (ORDER BY avg_cpu) * 100, 1) AS percentile,
    ROUND(CUME_DIST() OVER (ORDER BY avg_cpu) * 100, 1) AS cumulative_pct
FROM server_daily_summary;
-- PERCENT_RANK: (rank-1)/(total_rows-1)
-- CUME_DIST: rows_leq_current/total_rows
```

### FIRST_VALUE / LAST_VALUE — Baseline comparison
```sql
-- Compare each day's CPU to the first day of the month (baseline)
SELECT
    server_id,
    collection_date,
    avg_cpu,
    FIRST_VALUE(avg_cpu) OVER (
        PARTITION BY server_id, DATE_TRUNC('month', collection_date)
        ORDER BY collection_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS baseline_cpu,
    avg_cpu - FIRST_VALUE(avg_cpu) OVER (
        PARTITION BY server_id, DATE_TRUNC('month', collection_date)
        ORDER BY collection_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS delta_from_baseline
FROM server_daily_summary;
```

### Named Window (WINDOW clause) — DRY SQL
```sql
-- Define the window once, reuse multiple times
SELECT
    server_id,
    collection_date,
    avg_cpu,
    AVG(avg_cpu) OVER w AS rolling_7day_avg,
    MAX(avg_cpu) OVER w AS rolling_7day_max,
    MIN(avg_cpu) OVER w AS rolling_7day_min
FROM server_daily_summary
WINDOW w AS (
    PARTITION BY server_id
    ORDER BY collection_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
);
```

**Interview Q&A:**
- Q: What is NTILE(4) useful for? A: Quartile analysis — "which servers are in the top 25% of CPU usage?" Standard in capacity planning reports.
- Q: PERCENT_RANK vs CUME_DIST — difference? A: PERCENT_RANK is (rank-1)/(n-1). CUME_DIST includes ties differently — (rows ≤ current)/n. CUME_DIST is always > 0; PERCENT_RANK of the first row is always 0.
- Q: Why use the WINDOW clause? A: Avoids repeating the same OVER() clause. DRY principle — one change updates all window calculations.
- Q: LAST_VALUE gotcha? A: Default frame is ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW — so LAST_VALUE gives the current row's value, not the last in the partition. Fix: add `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` or use frame clause explicitly.

---

## C. Python — Pandas for Data Engineering

> **Discussion opener:** "Pandas is the workhorse of Python data engineering. Senior candidates know groupby internals, vectorization vs apply, and when NOT to use pandas (use Spark instead)."

### GroupBy — the most common interview topic
```python
import pandas as pd

df = pd.DataFrame({
    'server_id': ['s1','s1','s2','s2','s3'],
    'region': ['us-east','us-east','us-west','us-west','us-east'],
    'cpu': [70, 85, 60, 95, 45]
})

# Basic groupby
summary = df.groupby('server_id')['cpu'].agg(['mean', 'max', 'min']).reset_index()

# Multiple columns
by_region = df.groupby(['region', 'server_id']).agg(
    avg_cpu=('cpu', 'mean'),
    peak_cpu=('cpu', 'max'),
    count=('cpu', 'count')
).reset_index()

# Transform: add group stat back to original rows (like window function)
df['region_avg_cpu'] = df.groupby('region')['cpu'].transform('mean')
# Now each row has its region's average — PARTITION BY equivalent
```

### Merge (JOIN equivalent)
```python
# Inner, left, right, outer — same as SQL
servers = pd.DataFrame({'server_id': ['s1','s2','s3'], 'tier': ['gold','silver','bronze']})
metrics = pd.DataFrame({'server_id': ['s1','s2','s4'], 'cpu': [70, 85, 90]})

# Left join (keep all servers, fill NaN where no metrics)
result = servers.merge(metrics, on='server_id', how='left')

# Anti-join: servers with NO metrics
no_metrics = servers[~servers['server_id'].isin(metrics['server_id'])]
```

### apply vs vectorization — performance critical
```python
# SLOW: apply with lambda (row by row, Python overhead)
df['cpu_category'] = df['cpu'].apply(lambda x: 'high' if x > 80 else 'normal')

# FAST: vectorized with np.where (C speed)
import numpy as np
df['cpu_category'] = np.where(df['cpu'] > 80, 'high', 'normal')

# FAST: pd.cut for bins
df['cpu_bucket'] = pd.cut(df['cpu'], bins=[0, 50, 80, 100], labels=['low', 'medium', 'high'])
```

**Interview Q&A:**
- Q: What does `groupby().transform()` do vs `groupby().agg()`? A: `agg()` reduces — returns one row per group. `transform()` returns a Series with the same index as the original — like SQL window PARTITION BY.
- Q: When would you use pandas over Spark? A: Dataset fits in memory (rule of thumb: < 1-2GB). Spark has overhead for small data.
- Q: What's the difference between `merge()` and `join()`? A: `merge()` joins on column values. `join()` joins on index. Use `merge()` — it's explicit and safer.
- Q: `apply` vs vectorization — why does it matter? A: `apply` is Python-level iteration — slow on large DataFrames. Vectorized operations use NumPy's C layer — 10-100x faster.

---

## D. Technology — Apache Spark Architecture

> **Discussion opener:** "Spark is the industry standard for distributed data processing. Senior data engineers are expected to know the execution model — not just 'it's fast' but WHY it's fast and what makes it slow."

### The Execution Model
```
Driver Program
    ↓ (creates)
SparkContext / SparkSession
    ↓ (submits)
DAG of Stages
    ↓ (each stage is)
Set of Tasks (one per partition)
    ↓ (run on)
Executors (JVMs on worker nodes)
```

### Key Concepts

**RDD → DataFrame → Dataset**
- RDD: low-level, untyped, verbose. Use only for legacy code.
- DataFrame: optimized by Catalyst optimizer. Use this.
- Dataset: typed DataFrame (Scala/Java). Python doesn't have this.

**Transformations vs Actions**
```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("demo").getOrCreate()

df = spark.read.parquet("s3://bucket/telemetry/")

# Transformations (lazy — nothing runs yet):
filtered = df.filter(df.cpu_utilization > 80)
grouped = filtered.groupBy("server_id").agg({"cpu_utilization": "avg"})

# Action (triggers execution):
grouped.show()   # NOW the DAG runs
grouped.write.parquet("s3://output/high-cpu/")  # another action
```

**Partitions = Parallelism**
```python
# See partition count
print(df.rdd.getNumPartitions())

# Repartition: expensive (full shuffle)
df_rep = df.repartition(100)

# Coalesce: reduce partitions cheaply (no full shuffle)
df_small = df.coalesce(10)

# Partition by column: write one file per value (good for downstream queries)
df.write.partitionBy("year", "month").parquet("s3://output/")
```

**Interview Q&A:**
- Q: What is the Catalyst optimizer? A: Spark's query optimizer — transforms logical plans into optimized physical plans. Same role as a SQL optimizer. It pushes filters down, reorders joins, etc.
- Q: What causes a shuffle? Why is it expensive? A: Any operation requiring data from multiple partitions — groupBy, join, repartition. Shuffle writes data to disk and sends it across the network. It's the #1 Spark performance bottleneck.
- Q: What's the difference between `repartition` and `coalesce`? A: `repartition` does a full shuffle — good for increasing partitions or balancing skewed data. `coalesce` just merges existing partitions locally — good for reducing without shuffling.
- Q: Explain lazy evaluation. A: Transformations build a DAG but don't execute. Only actions trigger execution. This allows Spark to optimize the entire plan before running anything.
- Q: How many partitions should you have? A: Rule of thumb: 2-4 per CPU core. 128MB-256MB per partition is typical. Too few = underutilized cores. Too many = scheduling overhead.

---

## Today's Key Interview Talking Points

1. **"Sliding window converts O(n²) brute force to O(n) by maintaining a window that expands and contracts instead of re-examining every subarray."**
2. **"NTILE and PERCENT_RANK are how you bucket data into percentiles — standard for capacity tier analysis."**
3. **"Pandas `transform()` is the DataFrame equivalent of SQL PARTITION BY — adds a group stat back to every row."**
4. **"Shuffle is Spark's most expensive operation. Design your pipeline to minimize it: partition wisely, filter early, broadcast small tables."**

---

## Behavioral Anchor — Citi Story #2

**Topic: Scale + Performance**
Practice this (2 minutes):

> *"At Citi, processing telemetry for 6,000+ endpoints at daily cadence. The query pattern was rolling 7-day averages using SQL window functions — `AVG(cpu) OVER (PARTITION BY server_id ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`. We fed this into Prophet forecasting models to project 6 months forward. Before window functions, the team was doing this with self-joins, which was significantly slower. Switching to window functions cut query time by roughly 60%."*

---

## End of Day 2 — Wrap-Up

Gemini reports:
```
Day 2 Complete.
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 3: Stack + Complex JOINs + Decorators + Pipeline Architecture
```
