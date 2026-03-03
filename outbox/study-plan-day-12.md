---
created: 2026-03-02
updated: 2026-03-02
summary: Day 12 — Greedy Algorithms | Data Quality SQL | Data Quality Python (Great Expectations) | AWS Cost Optimization
tags: [study-plan, day-12, leetcode, sql, python, aws, data-quality, greedy]
---

# Study Day 12: Efficiency and Quality
**Theme:** Greedy thinking + Data quality at scale + AWS cost control

---

## Spaced Repetition — Review from Days 1–11
*60 seconds each. Mark Strong / Review / Weak.*

**SR-1 (Day 2):** LAST_VALUE default frame — what is the problem and the fix?
> Default frame is `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` — LAST_VALUE returns the current row's value, not the last in the partition. Fix: `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`.

**SR-2 (Day 4):** What is binary search's space complexity and when can it be O(log n)?
> Iterative binary search: O(1) space. Recursive binary search: O(log n) due to call stack. Always prefer iterative for space efficiency.

**SR-3 (Day 9):** asyncio.gather() vs ThreadPoolExecutor — when do you choose each?
> asyncio: when you're already in async code, or need very high concurrency (thousands of connections). ThreadPoolExecutor: when calling synchronous I/O libraries that don't support async. Both are for I/O-bound work.

**SR-4 (Day 10):** House Robber recurrence — state the recurrence and base cases precisely.
> `dp[i] = max(dp[i-2] + nums[i], dp[i-1])`. Base cases: `dp[0] = nums[0]`, `dp[1] = max(nums[0], nums[1])`. Space-optimized: two variables (prev2, prev1).

**SR-5 (Day 11):** Kahn's algorithm — what does the queue contain initially and what happens at the end?
> Initially: all nodes with in-degree 0 (no dependencies). At end: if completed count == numNodes, no cycle. If less, nodes with remaining in-degree > 0 form a cycle.

**SR-6 (Day 11):** Delta Lake vs plain Parquet — what three capabilities does Delta add?
> ACID transactions (no concurrent writes corruption), row-level deletes/updates (GDPR compliance), time travel (query as of version or timestamp).

---

## A. LeetCode — Greedy Algorithms

> **Discussion opener:** "Greedy algorithms make the locally optimal choice at each step without looking back. They work when the locally optimal choice leads to the globally optimal solution — which requires proof (but in interviews, recognizing the pattern and testing against examples is usually enough). Greedy is often O(n) or O(n log n) after sorting. The sorting step is usually the insight: 'if I sort by X, then processing in that order is always safe.'"

---

### LC #55 — Jump Game [Medium]
**Category:** Greedy

**Problem:**
Given array `nums`, each element is your max jump length. Starting at index 0, can you reach the last index?
`[2,3,1,1,4]` → `true` | `[3,2,1,0,4]` → `false`

🎯 **Design Checkpoint:** "Track the farthest index you can reach at any point. If the current index is ever beyond the farthest reach, you're stuck."

**Solution — Greedy (track max reach)** O(n) time, O(1) space
```python
def canJump(nums: list[int]) -> bool:
    max_reach = 0

    for i, jump in enumerate(nums):
        if i > max_reach:
            return False    # current position is unreachable
        max_reach = max(max_reach, i + jump)

    return True

# Test
print(canJump([2,3,1,1,4]))   # True
print(canJump([3,2,1,0,4]))   # False
print(canJump([0]))            # True (already at end)
```

**Interview Q&A:**
- Q: Why greedy works here? A: At each index, we update the global max reachable position. There's never a reason to "save" a big jump — taking the locally optimal reachability at every step gives the global optimum.
- Q: How would you track the actual path? A: Track which index gave the best jump for backtracking. Greedy + path tracking is common in follow-ups.

---

### LC #45 — Jump Game II [Medium]
**Category:** Greedy (Minimum Jumps)

**Problem:**
Same as Jump Game but guarantee you can reach the end. Return the minimum number of jumps.
`[2,3,1,1,4]` → `2` (0→1→4)

🎯 **Design Checkpoint:** "Think in layers (like BFS levels). Within the current jump's reach, find the farthest you can reach in one more jump. When you exhaust the current layer, increment jump count."

**Solution — Greedy (BFS layers)** O(n) time, O(1) space
```python
def jump(nums: list[int]) -> int:
    jumps = 0
    current_end = 0   # farthest reach of current jump layer
    farthest = 0      # farthest reach if we jump from within current layer

    for i in range(len(nums) - 1):   # don't need to jump from last index
        farthest = max(farthest, i + nums[i])

        if i == current_end:          # exhausted current layer → must jump
            jumps += 1
            current_end = farthest

    return jumps

# Test
print(jump([2,3,1,1,4]))    # 2
print(jump([2,3,0,1,4]))    # 2
print(jump([1,2,1,1,1]))    # 3
```

**Interview Q&A:**
- Q: What's the BFS analogy? A: Each jump count = one BFS level. Within the level (between current_end and farthest), we explore all reachable positions. When we cross current_end, we go to the next level (increment jumps).
- Q: What does "greedy" mean here specifically? A: At each layer, we always extend as far as possible — take the best jump in each layer. Never backtrack or reconsider.

---

### LC #134 — Gas Station [Medium]
**Category:** Greedy

**Problem:**
Circular array of gas stations with `gas[i]` and `cost[i]`. Find the starting station to complete the circuit, or -1.
`gas=[1,2,3,4,5]`, `cost=[3,4,5,1,2]` → `3`

🎯 **Design Checkpoint:** "If total gas < total cost, impossible. Otherwise, exactly one valid start exists. Greedily: if tank goes negative, reset and try starting at the next station."

**Solution — Greedy** O(n) time, O(1) space
```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    total_surplus = 0     # tracks overall feasibility
    current_surplus = 0   # current tank level
    start = 0

    for i in range(len(gas)):
        surplus = gas[i] - cost[i]
        total_surplus += surplus
        current_surplus += surplus

        if current_surplus < 0:     # can't reach next station from current start
            start = i + 1           # reset start to next station
            current_surplus = 0     # fresh tank

    return start if total_surplus >= 0 else -1

# Test
print(canCompleteCircuit([1,2,3,4,5], [3,4,5,1,2]))   # 3
print(canCompleteCircuit([2,3,4], [3,4,3]))             # -1
```

**Interview Q&A:**
- Q: Why does resetting the start to i+1 work? A: If the tank goes negative at station i, we can't start at any station between `start` and `i` — they all lose even more gas reaching i. The only candidates are i+1 onwards.
- Q: Why is only one valid start guaranteed if solution exists? A: If total gas ≥ total cost, exactly one valid start exists. The greedy reset finds it in one pass.

---

### LC #846 — Hand of Straights [Medium]
**Category:** Greedy + HashMap

**Problem:**
Given hand of cards and `groupSize`, can you arrange ALL cards into consecutive groups of `groupSize`?
`hand=[1,2,3,6,2,3,4,7,8]`, `groupSize=3` → `true` (1-2-3, 2-3-4, 6-7-8)

🎯 **Design Checkpoint:** "Process smallest card first. For each smallest remaining card, form a consecutive group starting there. If you can't, it's impossible."

**Solution — Greedy + Sorted Map** O(n log n) time
```python
from collections import Counter

def isNStraightHand(hand: list[int], groupSize: int) -> bool:
    if len(hand) % groupSize != 0:
        return False

    count = Counter(hand)

    for card in sorted(count):         # process smallest first
        if count[card] > 0:
            n = count[card]            # need to form n groups starting at this card
            for i in range(groupSize):
                if count[card + i] < n:
                    return False       # not enough cards to form all groups
                count[card + i] -= n

    return True

# Test
print(isNStraightHand([1,2,3,6,2,3,4,7,8], 3))   # True
print(isNStraightHand([1,2,3,4,5], 4))             # False
```

**Interview Q&A:**
- Q: Why sort? A: We must start groups from the smallest available card — otherwise we might "skip" a card that has no smaller complement to complete a group.
- Q: What's the time complexity? A: O(n log n) for sorting + O(n × groupSize) for the inner loop = O(n log n) overall since groupSize is constant.

---

## B. SQL — Data Quality Patterns

> **Discussion opener:** "Data quality is not someone else's job — it's part of the pipeline. The SQL patterns for quality: completeness (NULL checks), uniqueness (duplicate detection), referential integrity (orphaned records), freshness (late data), and validity (values within expected bounds). At Citi scale: automated daily quality reports caught issues before the business saw them."

### Completeness — NULL Detection
```sql
-- Which columns have NULLs, and how many?
SELECT
    COUNT(*) AS total_rows,
    COUNT(server_id) AS non_null_server_id,
    COUNT(*) - COUNT(server_id) AS null_server_id,
    COUNT(avg_cpu) AS non_null_avg_cpu,
    COUNT(*) - COUNT(avg_cpu) AS null_avg_cpu,
    ROUND(100.0 * (COUNT(*) - COUNT(avg_cpu)) / COUNT(*), 2) AS pct_null_cpu
FROM daily_metrics;

-- Alert if null rate exceeds threshold
WITH null_check AS (
    SELECT
        ROUND(100.0 * SUM(CASE WHEN avg_cpu IS NULL THEN 1 ELSE 0 END) / COUNT(*), 2) AS null_pct
    FROM daily_metrics
    WHERE report_date = CURRENT_DATE - INTERVAL '1 day'
)
SELECT
    null_pct,
    CASE WHEN null_pct > 5.0 THEN 'ALERT' ELSE 'OK' END AS status
FROM null_check;
```

### Uniqueness — Duplicate Detection
```sql
-- Find duplicate records (same server + date, multiple rows)
SELECT server_id, report_date, COUNT(*) AS duplicate_count
FROM daily_metrics
GROUP BY server_id, report_date
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;

-- Return the duplicate rows with all columns
WITH dupes AS (
    SELECT server_id, report_date
    FROM daily_metrics
    GROUP BY server_id, report_date
    HAVING COUNT(*) > 1
)
SELECT m.*
FROM daily_metrics m
JOIN dupes d ON m.server_id = d.server_id AND m.report_date = d.report_date
ORDER BY m.server_id, m.report_date;
```

### Referential Integrity — Orphaned Records
```sql
-- Metrics with no matching server in the servers table (orphaned foreign key)
SELECT m.server_id, COUNT(*) AS orphan_row_count
FROM daily_metrics m
LEFT JOIN servers s ON m.server_id = s.server_id
WHERE s.server_id IS NULL
GROUP BY m.server_id;

-- Servers with NO metrics in the last 30 days (stale inventory)
SELECT s.server_id, s.region, MAX(m.report_date) AS last_seen
FROM servers s
LEFT JOIN daily_metrics m ON s.server_id = m.server_id
GROUP BY s.server_id, s.region
HAVING MAX(m.report_date) < CURRENT_DATE - INTERVAL '30 days'
    OR MAX(m.report_date) IS NULL
ORDER BY last_seen NULLS FIRST;
```

### Validity — Values Within Bounds
```sql
-- Values outside valid range (cpu must be 0-100)
SELECT
    server_id,
    report_date,
    avg_cpu,
    CASE
        WHEN avg_cpu < 0   THEN 'BELOW_ZERO'
        WHEN avg_cpu > 100 THEN 'ABOVE_MAX'
        ELSE 'VALID'
    END AS validity_flag
FROM daily_metrics
WHERE avg_cpu < 0 OR avg_cpu > 100;

-- Statistical outliers — beyond 3 standard deviations
WITH stats AS (
    SELECT AVG(avg_cpu) AS mean, STDDEV(avg_cpu) AS sd
    FROM daily_metrics
    WHERE report_date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT m.server_id, m.report_date, m.avg_cpu,
       ROUND((m.avg_cpu - s.mean) / s.sd, 2) AS z_score
FROM daily_metrics m, stats s
WHERE ABS(m.avg_cpu - s.mean) > 3 * s.sd
ORDER BY ABS(m.avg_cpu - s.mean) DESC;
```

### Freshness — Late Data Detection
```sql
-- Which servers haven't reported in the last N hours?
SELECT
    s.server_id,
    s.region,
    MAX(m.report_date) AS last_report,
    CURRENT_DATE - MAX(m.report_date) AS days_since_last_report
FROM servers s
LEFT JOIN daily_metrics m ON s.server_id = m.server_id
GROUP BY s.server_id, s.region
HAVING MAX(m.report_date) < CURRENT_DATE - INTERVAL '1 day'
   OR MAX(m.report_date) IS NULL
ORDER BY days_since_last_report DESC NULLS FIRST;
```

**Interview Q&A:**
- Q: What are the five dimensions of data quality? A: Completeness (no missing required values), Uniqueness (no duplicates), Validity (values within expected domain), Consistency (matches across systems), Freshness (data arrives on time). Some add Accuracy (matches ground truth) as a sixth.
- Q: How would you automate these checks? A: dbt data tests (schema.yml for standard checks, custom SQL tests for complex rules), Great Expectations (Python library for expectations as code), or a scheduled Airflow DAG that runs quality SQL and alerts on failures.

---

## C. Python — Data Quality with Great Expectations

> **Discussion opener:** "Great Expectations (GX) is the standard Python library for data quality. You define 'expectations' about your data — a contract — and run them against new data. Failures go to an alerting pipeline. Think of it as pytest for data."

### Core Concepts
```python
import great_expectations as gx
import pandas as pd

# Sample data
df = pd.DataFrame({
    'server_id': ['srv-01', 'srv-02', 'srv-03', None,    'srv-01'],
    'avg_cpu':   [72.5,     45.2,     110.0,   88.1,     72.5  ],
    'region':    ['us-east','us-west','eu-west','us-east','us-east'],
})

# Create a GX context and validator
context = gx.get_context()
validator = context.sources.pandas_default.read_dataframe(df)

# Define expectations (the "contract" for this dataset)
validator.expect_column_values_to_not_be_null("server_id")
validator.expect_column_values_to_be_between("avg_cpu", min_value=0, max_value=100)
validator.expect_column_values_to_be_in_set("region", ["us-east", "us-west", "eu-west"])
validator.expect_column_pair_values_to_be_unique(["server_id", "report_date"])

# Run validation
results = validator.validate()

print(f"Success: {results['success']}")
for result in results['results']:
    if not result['success']:
        print(f"  FAILED: {result['expectation_config']['type']}")
        print(f"    {result['result']}")
```

### Custom Expectations — Pure SQL/Pandas Pattern (No GX Required)
```python
from dataclasses import dataclass
from typing import Callable
import pandas as pd

@dataclass
class QualityCheck:
    name: str
    check: Callable[[pd.DataFrame], bool]
    threshold: float = 1.0   # 1.0 = must pass 100%; 0.99 = allow 1% failures

def run_quality_suite(df: pd.DataFrame, checks: list[QualityCheck]) -> dict:
    results = {}

    for check in checks:
        try:
            passed = check.check(df)
            results[check.name] = {'passed': passed, 'status': 'OK' if passed else 'FAIL'}
        except Exception as e:
            results[check.name] = {'passed': False, 'status': f'ERROR: {e}'}

    overall = all(r['passed'] for r in results.values())
    return {'overall': overall, 'checks': results}

# Define checks
checks = [
    QualityCheck(
        name="no_null_server_id",
        check=lambda df: df['server_id'].notna().all()
    ),
    QualityCheck(
        name="cpu_in_valid_range",
        check=lambda df: df['avg_cpu'].between(0, 100).all()
    ),
    QualityCheck(
        name="no_duplicate_server_date",
        check=lambda df: not df.duplicated(subset=['server_id', 'report_date']).any()
    ),
    QualityCheck(
        name="valid_regions",
        check=lambda df: df['region'].isin(['us-east', 'us-west', 'eu-west']).all()
    ),
]

# Run against a DataFrame
sample = pd.DataFrame({
    'server_id': ['srv-01', 'srv-02', 'srv-03'],
    'avg_cpu': [72.5, 45.2, 85.1],
    'region': ['us-east', 'us-west', 'eu-west'],
    'report_date': ['2026-02-26', '2026-02-26', '2026-02-26'],
})

result = run_quality_suite(sample, checks)
print(f"Overall: {'PASS' if result['overall'] else 'FAIL'}")
for name, r in result['checks'].items():
    print(f"  {name}: {r['status']}")
```

**Interview Q&A:**
- Q: What is a data contract? A: An explicit agreement between data producers and consumers about the schema, types, value ranges, and freshness guarantees of a dataset. Great Expectations makes this executable code. Violations trigger alerts rather than silent data corruption.
- Q: Where do you place data quality checks in a pipeline? A: (1) At intake (validate raw data before loading). (2) After transformation (validate outputs before publishing). (3) Scheduled (run daily quality reports on the warehouse). The first is most critical — bad data at intake compounds downstream.
- Q: What is a dead-letter queue in data quality context? A: A separate storage location (S3 prefix, Kafka topic, DynamoDB table) for records that failed validation. Allows later inspection, human review, and replay without losing valid records or blocking the pipeline.

---

## D. Technology — AWS Cost Optimization

> **Discussion opener:** "AWS credits expire — you have ~$199 and ~107 days. Cost optimization is also a genuine interview topic for senior engineers. Understanding where money goes and how to reduce it shows production maturity. The two biggest levers: Athena scans less data (format + partitioning), and compute uses Spot instances instead of On-Demand."

### Where AWS Data Costs Come From
```
Service     | Cost Driver              | Optimization
------------|--------------------------|-------------------------------------------
S3          | Storage (GB/month)       | Lifecycle rules: Infrequent Access → Glacier
Athena      | Data scanned ($/TB)      | Parquet + Snappy + partitioning → 80% reduction
Glue ETL    | DPU-hours                | Right-size workers, use smaller DPU type (G.1X vs G.2X)
Glue Crawler| DPU-hours                | Schedule less frequently, scope to changed prefixes
EMR         | EC2 hours                | Spot instances for worker nodes (up to 70% savings)
Lambda      | Invocations + GB-seconds | Keep functions warm, right-size memory
Kinesis     | Shard-hours              | Decommission idle shards
Data Xfer   | GB out of AWS            | Co-locate consumers in same region/AZ
```

### S3 Lifecycle Policies
```json
{
  "Rules": [{
    "ID": "telemetry-lifecycle",
    "Status": "Enabled",
    "Filter": {"Prefix": "telemetry/raw/"},
    "Transitions": [
      {"Days": 30,  "StorageClass": "STANDARD_IA"},
      {"Days": 90,  "StorageClass": "GLACIER"},
      {"Days": 365, "StorageClass": "DEEP_ARCHIVE"}
    ],
    "Expiration": {"Days": 2555}
  }]
}
```

### Athena Cost — The Parquet Effect
```
Same data, different formats:
  CSV (uncompressed): 100 GB → scan 100 GB → $0.50/query
  CSV (gzip):         25 GB  → scan 25 GB  → $0.125/query
  Parquet (Snappy):   15 GB  → scan 15 GB  → $0.075/query
  Parquet + partition filter: 0.5 GB → scan 0.5 GB → $0.0025/query

The partition filter (WHERE report_date = '2026-02-27') skips 99.5% of the data.
Combined: 200× cheaper than uncompressed CSV with full scans.
```

### Spot Instances for EMR
```python
# EMR Cluster with Spot for worker nodes (up to 70% discount)
# boto3 / CloudFormation equivalent config

cluster_config = {
    'Name': 'telemetry-etl-cluster',
    'InstanceGroups': [
        {
            'Name': 'Master',
            'InstanceRole': 'MASTER',
            'InstanceType': 'm5.xlarge',
            'InstanceCount': 1,
            'Market': 'ON_DEMAND'   # Master always On-Demand (avoid interruption)
        },
        {
            'Name': 'Workers',
            'InstanceRole': 'CORE',
            'InstanceType': 'm5.2xlarge',
            'InstanceCount': 4,
            'Market': 'SPOT',       # Workers on Spot — 50-70% savings
            'BidPrice': 'OnDemandPrice'  # don't exceed On-Demand price
        }
    ]
}
# Spot interruption: EMR handles gracefully — checkpoint + migrate work
# Mitigation: use INSTANCE_FLEET with multiple instance types (less likely to all be interrupted)
```

### Reserved Capacity vs Spot vs On-Demand
```
Type          | Discount | Commitment  | Use Case
--------------|----------|-------------|------------------------------------------
On-Demand     | 0%       | None        | Unpredictable, short-lived workloads
Reserved (1yr)| ~30-40%  | 1 year      | Steady-state services (Glue, always-on)
Reserved (3yr)| ~50-60%  | 3 years     | Long-term infrastructure
Spot          | ~60-70%  | None        | Interruptible batch: EMR workers, ECS tasks
Savings Plans | ~20-40%  | 1-3 years   | Flexible: any instance type in region
```

### Cost Monitoring — Practical
```
1. AWS Cost Explorer → breakdown by service, tag, region
2. Billing alerts → set $50, $100, $150 alarms via CloudWatch
3. S3 Storage Lens → analyze storage usage patterns across buckets
4. Athena query history → find expensive queries (high data scanned)
5. Tagging → tag all resources with project, environment, owner
   Every resource should have: Project=capacity-planning, Env=dev/prod

With $199 AWS credits:
  Priority 1: Athena ad-hoc queries (cheap per query with proper format)
  Priority 2: S3 (minimal cost for small data)
  Priority 3: Glue job runs (DPU-hours — run less frequently)
  Priority 4: EMR (expensive — use only when Spark is truly needed)
  → Prefer: DuckDB locally for exploration, Athena for sharing results
```

**Interview Q&A:**
- Q: You have a 500GB Athena table that takes 30 seconds to query. How do you optimize? A: (1) Convert to Parquet with Snappy compression (80% size reduction). (2) Partition by the most-filtered column (usually date). (3) Run MSCK REPAIR TABLE or update Glue catalog. (4) Use columnar predicates — select only needed columns. Expected result: 5-10× faster and 90% cheaper.
- Q: What is S3 Requester Pays? A: A bucket policy that charges the requester (not the bucket owner) for data transfer and requests. Used when exposing a public dataset — the requester pays for their own downloads.
- Q: How would you reduce Glue ETL costs? A: (1) Use G.1X workers for smaller jobs (instead of G.2X). (2) Disable Glue bookmarks if you're processing idempotently with date partitions. (3) Reduce max DPUs — Glue auto-scales but charges for max.

---

## Today's Key Interview Talking Points

1. **"Greedy works when locally optimal choice is globally optimal. Recognize by: sorting reveals the order, and looking back never helps."**
2. **"Data quality: completeness, uniqueness, validity, freshness, referential integrity — cover all five in design discussions."**
3. **"Bad data at intake compounds downstream. Validate at the boundary, route failures to dead-letter, never drop silently."**
4. **"Parquet + partitioning = 200× cheaper Athena queries. This is always the answer to 'how do you reduce Athena costs.'"**
5. **"Spot for workers, On-Demand for masters. Never put a master on Spot — interruption kills the cluster."**

---

## Behavioral Anchor — Citi Story #12

**Topic: Cost Consciousness + Data Quality**

Practice this story (2 minutes, STAR format):

> *"At Citi we ran a quarterly analysis of server capacity utilization for budget planning. The data was stored as CSV in network shares — a 90-day pull took hours. I proposed migrating to a proper column-store with partitioning. The model was simple: convert to Parquet, partition by date, query with an engine that supports predicate pushdown. The result was a 30-day pull going from hours to seconds — the analyst team could run ad-hoc scenarios instead of waiting for nightly batch runs. Lesson: data format is a cost and performance decision, not just a storage decision. In AWS today that's Parquet on S3 with Athena."*

**Gemini: ask Sean to tell this story unprompted. Time him. Give STAR feedback.**

---

## End of Day 12 — Wrap-Up

Gemini reports:
```
Day 12 Complete.
Topics covered: Greedy | Data Quality SQL | Great Expectations | AWS Cost Optimization
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 13: Linked Lists + Forecasting SQL + Prophet/Regression + Capacity Planning Framework
```
