---
created: 2026-02-28
updated: 2026-02-28
summary: Day 1 — Arrays & HashMaps | SQL CTEs | Python Generators | AWS Data Platform
tags: [study-plan, day-1, leetcode, sql, python, aws]
---

# Study Day 1: Foundations
**Theme:** HashMaps + CTEs + Generators + AWS Architecture
**Pre-work done:** SQL Window Functions (already studied)

---

## Spaced Repetition — Day 0 Pre-work Review
*Run these before anything new. 60 seconds each.*

**SR-1:** What is the difference between PARTITION BY and GROUP BY?
> GROUP BY collapses rows to one per group. PARTITION BY keeps all rows and adds a calculated column alongside. Window functions never reduce row count.

**SR-2:** You have LAG() and a self-join that achieve the same result. Which do you use and why?
> LAG() — cleaner, more readable, and significantly better performance. A self-join on 6,000 endpoints would be expensive. At Citi I used LAG() to compare server utilization between collection intervals.

**SR-3:** What breaks if you use a window function in a WHERE clause?
> It fails — window functions are evaluated after WHERE. You must wrap in a CTE or subquery first, then filter on the result.

**SR-4:** What is ROWS BETWEEN vs RANGE BETWEEN?
> ROWS = physical rows (predictable). RANGE = logical — includes all rows with same ORDER BY value. Always use ROWS for time series.

---

## A. LeetCode — Arrays & HashMaps

> **Discussion opener:** "HashMap problems appear in nearly every data engineering interview. The pattern is: trade O(n) space for O(1) lookup to drop from O(n²) to O(n) time."

---

### LC #1 — Two Sum [Easy]
**Category:** HashMap

**Problem:**
Given an integer array `nums` and a target, return indices of two numbers that add to target.
Input: `nums = [2, 7, 11, 15]`, `target = 9` → Output: `[0, 1]`
**Constraints:** Exactly one solution. Same element not used twice.

🎯 **Design Checkpoint** *(Gemini: ask before showing solutions)*
> "What's your approach? What does storing the complement give you?"

**Solution 1 — Brute Force** O(n²) time, O(1) space
```python
def twoSum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
```
*Why slow: checks every pair — n*(n-1)/2 comparisons.*

**Solution 2 — HashMap (Optimal)** O(n) time, O(n) space
```python
def twoSum(nums, target):
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
```
*The insight: for each number, check if its complement already exists. One pass.*

**Interview Q&A:**
- Q: Why O(n) space? A: We store up to n elements in the hashmap.
- Q: What if there were multiple valid pairs? A: Modify to collect all pairs, not return on first hit.
- Q: What data structure is `{}` in Python under the hood? A: Hash table — O(1) average lookup.

---

### LC #217 — Contains Duplicate [Easy]
**Category:** HashSet

**Problem:**
Given integer array, return `true` if any value appears at least twice.
Input: `[1,2,3,1]` → `true` | Input: `[1,2,3,4]` → `false`

🎯 **Design Checkpoint:** "What structure lets you check membership in O(1)?"

**Solution 1 — Sort** O(n log n) time
```python
def containsDuplicate(nums):
    nums.sort()
    for i in range(1, len(nums)):
        if nums[i] == nums[i-1]:
            return True
    return False
```

**Solution 2 — HashSet (Optimal)** O(n) time, O(n) space
```python
def containsDuplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
# One-liner: return len(nums) != len(set(nums))
```

**Interview Q&A:**
- Q: When would you prefer the sort approach? A: When memory is constrained — O(1) space vs O(n).
- Q: What's the Python one-liner? A: `return len(nums) != len(set(nums))`

---

### LC #242 — Valid Anagram [Easy]
**Category:** HashMap / Counter

**Problem:**
Given strings `s` and `t`, return `true` if `t` is an anagram of `s`.
`"anagram"`, `"nagaram"` → `true` | `"rat"`, `"car"` → `false`

🎯 **Design Checkpoint:** "Two strings are anagrams if they have the same character frequencies."

**Solution 1 — Sort** O(n log n)
```python
def isAnagram(s, t):
    return sorted(s) == sorted(t)
```

**Solution 2 — Counter (Optimal)** O(n) time, O(1) space (bounded by 26 letters)
```python
from collections import Counter
def isAnagram(s, t):
    return Counter(s) == Counter(t)

# Manual approach:
def isAnagram(s, t):
    if len(s) != len(t): return False
    count = {}
    for c in s: count[c] = count.get(c, 0) + 1
    for c in t:
        if c not in count or count[c] == 0: return False
        count[c] -= 1
    return True
```

**Interview Q&A:**
- Q: What if input contains Unicode? A: Counter still works — keys become unicode chars.
- Q: Why is Counter O(1) space for lowercase letters? A: At most 26 unique keys regardless of input length.

---

### LC #238 — Product of Array Except Self [Medium]
**Category:** Array / Prefix Product

**Problem:**
Given array `nums`, return array where `output[i]` = product of all elements except `nums[i]`.
No division allowed. Must be O(n).
Input: `[1,2,3,4]` → `[24,12,8,6]`

🎯 **Design Checkpoint:** "If you can't divide, how do you get the product of everything except index i? Think: what's to the left × what's to the right."

**Solution — Prefix + Suffix Products** O(n) time, O(1) extra space
```python
def productExceptSelf(nums):
    n = len(nums)
    result = [1] * n

    # Left pass: result[i] = product of everything to the left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Right pass: multiply by product of everything to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result
```
*The insight: result[i] = left_product[i] × right_product[i]. Build each in one pass.*

**Interview Q&A:**
- Q: Why no division? A: nums could contain zero — dividing by zero is undefined.
- Q: If zeros are allowed, how does the approach hold? A: It handles zeros naturally — no special casing needed.
- Q: What's the time complexity? A: O(n) — two passes over the array.

---

### LC #347 — Top K Frequent Elements [Medium]
**Category:** HashMap + Heap (or Bucket Sort)

**Problem:**
Given integer array and k, return the k most frequent elements.
Input: `nums = [1,1,1,2,2,3]`, `k = 2` → `[1, 2]`

🎯 **Design Checkpoint:** "Step 1: count frequencies. Step 2: find top k. What data structure finds top k efficiently?"

**Solution 1 — HashMap + Heap** O(n log k)
```python
from collections import Counter
import heapq
def topKFrequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

**Solution 2 — Bucket Sort (Optimal)** O(n) time
```python
from collections import Counter
def topKFrequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for i in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[i])
        if len(result) >= k:
            return result[:k]
```
*The insight: frequency can't exceed len(nums). Use frequency as array index.*

**Interview Q&A:**
- Q: When would you use the heap approach in production? A: When memory matters — heap is O(k) extra space vs O(n) for buckets.
- Q: How is this relevant in data engineering? A: Top-K queries everywhere — top customers, top error codes, top slow queries.
- Q: What's Counter under the hood? A: Subclass of dict. `Counter(nums)` is O(n).

---

## B. SQL — Common Table Expressions (CTEs)

> **Discussion opener:** "CTEs make complex queries readable by naming intermediate result sets. They're not a performance feature — they're a readability feature. The optimizer often treats them the same as subqueries."

### The Syntax
```sql
WITH cte_name AS (
    SELECT ...
    FROM ...
    WHERE ...
),
second_cte AS (
    SELECT ...
    FROM cte_name  -- reference the first CTE
)
SELECT * FROM second_cte;
```

### Regular CTE — Find employees earning above department average
```sql
WITH dept_averages AS (
    SELECT
        department_id,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    e.name,
    e.salary,
    d.avg_salary,
    e.salary - d.avg_salary AS above_average_by
FROM employees e
JOIN dept_averages d ON e.department_id = d.department_id
WHERE e.salary > d.avg_salary
ORDER BY above_average_by DESC;
```

### Recursive CTE — Walk a hierarchy (manager → reports)
```sql
WITH RECURSIVE org_chart AS (
    -- Base case: start with the CEO (no manager)
    SELECT employee_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- Recursive case: join employees to their manager
    SELECT e.employee_id, e.name, e.manager_id, oc.level + 1
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
)
SELECT * FROM org_chart ORDER BY level, name;
```

### Chained CTEs — Deduplicate then aggregate
```sql
WITH deduped AS (
    SELECT DISTINCT server_id, collection_date, cpu_utilization
    FROM telemetry_raw
    WHERE collection_date >= CURRENT_DATE - INTERVAL '30 days'
),
daily_avg AS (
    SELECT server_id, collection_date, AVG(cpu_utilization) AS avg_cpu
    FROM deduped
    GROUP BY server_id, collection_date
)
SELECT server_id, MAX(avg_cpu) AS peak_30day
FROM daily_avg
GROUP BY server_id
ORDER BY peak_30day DESC;
```

**Interview Q&A:**
- Q: What's the difference between a CTE and a subquery? A: CTEs are named and reusable within the query. Subqueries are inline and can't be referenced more than once. CTEs improve readability significantly for multi-step logic.
- Q: Do CTEs improve performance? A: Not inherently — most optimizers treat them like subqueries. In some databases (PostgreSQL < 12) CTEs were optimization fences. Know your engine.
- Q: When would you use a recursive CTE? A: Hierarchy traversal — org charts, category trees, network topology. At Citi I would have used this to traverse alert escalation chains.
- Q: What's the risk of recursive CTEs? A: Infinite loops if there's a cycle. Always add a depth limit: `WHERE level < 10` or `MAXRECURSION` hint.
- Q: CTE vs temp table — when does temp table win? A: When you need to reference the result many times or need an index on it. Temp tables materialize; CTEs may or may not.

---

## C. Python — Generators & List Comprehensions

> **Discussion opener:** "Generators are lazy — they produce one value at a time instead of building the whole list in memory. For data engineering with millions of rows, this is the difference between crashing and streaming."

### List Comprehensions
```python
# Standard: [expression for item in iterable if condition]
squares = [x**2 for x in range(10) if x % 2 == 0]
# → [0, 4, 16, 36, 64]

# Nested: flatten a 2D list
matrix = [[1,2],[3,4],[5,6]]
flat = [num for row in matrix for num in row]
# → [1, 2, 3, 4, 5, 6]

# Dict comprehension
word_lengths = {word: len(word) for word in ["data", "engineer", "SQL"]}
# → {'data': 4, 'engineer': 8, 'SQL': 3}
```

### Generators — the memory-efficient alternative
```python
# Generator expression (like list comp but with parens)
squares_gen = (x**2 for x in range(10_000_000))  # uses ~200 bytes, not 80MB

# Generator function with yield
def read_large_csv_chunks(filepath, chunk_size=1000):
    """Stream a large file in chunks without loading it all."""
    with open(filepath) as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk  # yield the last partial chunk

# Usage — processes one chunk at a time
for chunk in read_large_csv_chunks("telemetry_data.csv"):
    process(chunk)  # only 1000 rows in memory at a time
```

### itertools — production-grade tools
```python
import itertools

# Chain: combine multiple iterables
servers = ["srv-01", "srv-02"]
databases = ["db-01"]
all_resources = list(itertools.chain(servers, databases))

# Groupby: group consecutive items (sort first!)
from itertools import groupby
data = sorted([("sql", "CTE"), ("sql", "JOIN"), ("py", "pandas")], key=lambda x: x[0])
for topic, items in groupby(data, key=lambda x: x[0]):
    print(topic, list(items))
```

**Interview Q&A:**
- Q: What's the difference between a list comprehension and a generator expression? A: List comp builds the entire list in memory immediately. Generator is lazy — yields one value at a time. Use generators for large datasets.
- Q: When does `yield` pause execution? A: Exactly at the yield statement. The function resumes from that point on the next `next()` call.
- Q: How would you process a 10GB CSV without loading it into memory? A: Use a generator that reads and yields chunks. pandas `read_csv(chunksize=N)` is built on this pattern.
- Q: What's `itertools.chain` useful for in data pipelines? A: Combining results from multiple sources (multiple S3 files, multiple DB queries) into a single iterable without materializing all of them.

---

## D. Technology & Architecture — AWS Data Platform

> **Discussion opener:** "AWS has three services that form the backbone of most modern data lakes: S3 (store), Glue (catalog + transform), Athena (query). You can build a production data platform with no servers."

### The Core Stack
```
Raw Data → S3 (data lake) → Glue Crawler → Glue Data Catalog
                                                      ↓
                                              Athena (SQL query)
                                                      ↓
                                          QuickSight / Jupyter / API
```

### S3 — The Foundation
- Object store, not a file system. Key = full path string.
- **Partitioning is everything:** `s3://bucket/telemetry/year=2026/month=02/day=27/`
- Athena skips entire partitions when your WHERE clause filters on partition keys
- Storage classes: Standard → Standard-IA → Glacier (cost vs access speed tradeoff)

### Glue — Catalog + ETL
```python
# Glue job (PySpark under the hood)
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)

# Read from catalog (defined by crawler)
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="telemetry_db",
    table_name="server_metrics"
)

# Transform and write
output = datasource.filter(f=lambda x: x["cpu_utilization"] > 80)
glueContext.write_dynamic_frame.from_options(
    frame=output,
    connection_type="s3",
    connection_options={"path": "s3://output-bucket/high-cpu/"},
    format="parquet"
)
```

### Athena — Serverless SQL
```sql
-- Query Parquet files in S3 as if they're a table
-- Partition pruning makes this fast even on TBs

SELECT
    server_id,
    AVG(cpu_utilization) as avg_cpu,
    MAX(cpu_utilization) as peak_cpu,
    COUNT(*) as sample_count
FROM telemetry_db.server_metrics
WHERE year = '2026'
  AND month = '02'          -- partition pruning: only scans Feb files
  AND cpu_utilization > 80
GROUP BY server_id
ORDER BY avg_cpu DESC
LIMIT 100;
```

**Interview Q&A:**
- Q: What is a Glue Crawler? A: A job that scans S3 (or RDS, etc.) and automatically infers schema, creates/updates tables in the Glue Data Catalog. You point it at a bucket, it discovers your data.
- Q: What's the difference between Glue and EMR? A: Glue is serverless — no cluster to manage. EMR gives you a full Hadoop/Spark cluster you control. Glue is easier; EMR is more powerful and flexible.
- Q: How does Athena pricing work? A: Pay per TB scanned. Compression + columnar format (Parquet/ORC) reduces cost dramatically. At Citi, using Parquet on Athena would have cut query costs by ~80%.
- Q: What is Lake Formation and when does it matter? A: Fine-grained access control for your data lake — column-level and row-level security on top of S3/Glue/Athena. Matters in regulated industries (finance, healthcare).
- Q: Design a pipeline to ingest server metrics from 6,000 endpoints into S3 for daily reporting. A: Agents push to Kinesis → Lambda batches and writes to S3 (partitioned by date) → Glue crawler updates catalog → Athena for ad-hoc queries → QuickSight for dashboards. CloudWatch for pipeline monitoring.

---

## Today's Key Interview Talking Points

Drop these naturally in interviews:

1. **"HashMap gives O(1) lookup by trading space for time — that's the core of most optimization problems."**
2. **"CTEs are a readability feature first, not a performance feature. Know your optimizer."**
3. **"Generators are the Python equivalent of streaming — essential for large data."**
4. **"S3 partition strategy is your first performance decision in any data lake design."**
5. **"Parquet + Athena = columnar storage + serverless SQL. Pay for what you scan."**

---

## Behavioral Anchor — Citi Story #1

**Topic: Scale**
Practice this story (2 minutes, STAR format):

> *"At Citi I was responsible for collecting telemetry from 6,000+ endpoints. The data volume was significant — we're talking millions of rows of metrics per collection cycle. I used SQL window functions (LAG and rolling AVG) directly against the data warehouse to detect utilization spikes and forecast capacity needs. The key insight was that comparing current vs previous interval with LAG() was far more efficient than self-joins at that scale. We could identify servers trending toward bottleneck 6 months out."*

**Gemini: ask Sean to tell this story unprompted. Time him for 2 minutes. Give STAR feedback.**

---

## End of Day 1 — Wrap-Up

Gemini reports:
```
Day 1 Complete.
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 2: Sliding Window + Advanced Window Functions + Pandas + Spark
```
