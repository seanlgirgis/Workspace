---
created: 2026-03-02
updated: 2026-03-02
summary: Day 8 — Trees & BFS/DFS | SQL CASE WHEN / PIVOT | pytest | Apache Airflow
tags: [study-plan, day-8, leetcode, sql, python, airflow, trees]
---

# Study Day 8: Hierarchical Data Patterns
**Theme:** Binary Trees + SQL Pivoting + Testable Code + Orchestration
**Week 2 begins — build on Week 1 patterns, introduce tree traversal as the new core mental model.**

---

## Spaced Repetition — Review from Days 1–7
*60 seconds each. Mark Strong / Review / Weak.*

**SR-1 (Day 1):** Top K Frequent Elements — what's the O(n) approach and why does it work?
> Bucket sort: use frequency as the array index. Since frequency ≤ len(nums), array size is bounded. Iterate from high to low, collect k elements. O(n) — no comparison sort needed.

**SR-2 (Day 2):** Minimum Window Substring — what's the termination condition for the left pointer?
> Shrink left when the window is valid (contains all required characters with required counts). Track `formed` count to know when the window satisfies all character requirements.

**SR-3 (Day 3):** Daily Temperatures — why is the monotonic stack amortized O(n) despite the while loop?
> Each index is pushed once and popped at most once. Total operations across all iterations ≤ 2n. The while loop's iterations are bounded by total pushes across the entire array.

**SR-4 (Day 5):** How does the two-heap median finder maintain balance?
> max-heap (lower half) + min-heap (upper half). After every push, rebalance: `lo` can have at most 1 more element than `hi`. If off by more, pop from one and push to the other. Median = `lo[0]` if odd count, `(lo[0] + hi[0]) / 2` if even.

**SR-5 (Day 6):** What is a Slowly Changing Dimension (SCD) Type 2?
> Track historical changes by adding new rows instead of updating. Each row gets `valid_from`, `valid_to`, `is_current`. Supports point-in-time queries: "what was the state on date X?"

**SR-6 (Day 6):** SCD Type 1 vs Type 2 — when do you choose each?
> SCD1: overwrite — you only care about current value (low cardinality, no audit need). SCD2: versioned rows — you need history (regulatory, trend analysis, point-in-time correctness).

---

## A. LeetCode — Trees & BFS/DFS

> **Discussion opener:** "Trees are graphs with no cycles and one path between any two nodes. The core split: DFS (recursion or explicit stack — go deep) vs BFS (queue — go wide, level by level). BFS is the answer when you need shortest path or level-by-level processing. DFS is the answer when you need to explore all paths, compute depth, or check properties."

**Tree node definition** (all tree problems use this):
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

### LC #104 — Maximum Depth of Binary Tree [Easy]
**Category:** DFS / BFS

**Problem:**
Given root of a binary tree, return its maximum depth (number of nodes along longest path from root to a leaf).
```
    3
   / \
  9  20
    /  \
   15   7
```
→ max depth = 3

🎯 **Design Checkpoint:** "What does 'depth' mean recursively? The depth of a node = 1 + max(depth of left child, depth of right child)."

**Solution 1 — DFS Recursive** O(n) time, O(h) space (h = height)
```python
def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```
*3 lines. The base case (None → 0) handles leaves naturally.*

**Solution 2 — BFS Iterative** O(n) time, O(w) space (w = max width)
```python
from collections import deque

def maxDepth(root: TreeNode) -> int:
    if not root:
        return 0
    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        for _ in range(len(queue)):   # process entire level
            node = queue.popleft()
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)

    return depth
```

**Interview Q&A:**
- Q: When is BFS better than DFS for depth? A: BFS naturally counts levels — depth is just the number of BFS iterations. For skewed trees, BFS uses O(1) extra space vs DFS's O(n) call stack.
- Q: What is the space complexity of the recursive DFS solution? A: O(h) where h is tree height. Worst case (skewed tree): O(n). Best case (balanced): O(log n).

---

### LC #102 — Binary Tree Level Order Traversal [Medium]
**Category:** BFS (Queue)

**Problem:**
Return the level-order traversal of a binary tree as a list of lists.
```
Input:  [3, 9, 20, null, null, 15, 7]
Output: [[3], [9, 20], [15, 7]]
```

🎯 **Design Checkpoint:** "BFS processes nodes level by level. At each iteration, you know exactly how many nodes are in the current level — it's `len(queue)` at the start of the iteration. Process exactly that many, then increment the level."

**Solution — BFS with level snapshot** O(n) time, O(n) space
```python
from collections import deque

def levelOrder(root: TreeNode) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)     # snapshot: how many nodes at this level
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(level)

    return result
```

**Interview Q&A:**
- Q: What's the key to level-by-level BFS? A: `level_size = len(queue)` before the inner loop. This freezes the count — children added during this level are in the queue but counted separately next iteration.
- Q: Real-world tree traversal in data? A: Directory trees, category hierarchies, org charts, dependency graphs. SQL recursive CTEs solve the same problems.
- Q: BFS vs DFS for level order? A: Always BFS — DFS would require passing depth as a parameter and backtracking to reconstruct levels.

---

### LC #226 — Invert Binary Tree [Easy]
**Category:** DFS / Recursion

**Problem:**
Invert (mirror) a binary tree.
```
Input:      Output:
    4           4
   / \         / \
  2   7       7   2
 / \ / \     / \ / \
1  3 6  9   9  6 3  1
```

🎯 **Design Checkpoint:** "At every node, swap left and right children. Then recurse into both. The order doesn't matter because you swap before recursing."

**Solution — DFS Recursive** O(n) time, O(h) space
```python
def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None

    root.left, root.right = root.right, root.left   # swap
    invertTree(root.left)
    invertTree(root.right)

    return root
```

**Interview Q&A:**
- Q: Can you do this iteratively? A: Yes — BFS or DFS with an explicit stack. Push node, swap its children, push children.
- Q: Why is this asked so frequently? A: Tests recursive thinking. The solution is 4 lines but requires understanding that swapping at every level naturally mirrors the tree.

---

### LC #199 — Binary Tree Right Side View [Medium]
**Category:** BFS / DFS

**Problem:**
Imagine standing to the right of a tree, looking left. Return the values you can see (last node at each level).
```
Input:  [1, 2, 3, null, 5, null, 4]
Output: [1, 3, 4]
```

🎯 **Design Checkpoint:** "The rightmost node at each level is the one visible from the right. BFS level-by-level: take the last element of each level."

**Solution 1 — BFS (natural fit)** O(n) time, O(n) space
```python
from collections import deque

def rightSideView(root: TreeNode) -> list[int]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:       # last node at this level
                result.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)

    return result
```

**Solution 2 — DFS (right-first)** O(n) time, O(h) space
```python
def rightSideView(root: TreeNode) -> list[int]:
    result = []

    def dfs(node, depth):
        if not node:
            return
        if depth == len(result):     # first time we've reached this depth
            result.append(node.val)  # rightmost node (right-first traversal)
        dfs(node.right, depth + 1)   # right first!
        dfs(node.left, depth + 1)

    dfs(root, 0)
    return result
```

**Interview Q&A:**
- Q: When does the DFS solution show the wrong node? A: Never — because we traverse right-first. The first node we encounter at each depth is the rightmost one.
- Q: How would you get the LEFT side view? A: BFS: take the first element per level. DFS: traverse left-first, take the first node encountered at each depth.

---

## B. SQL — CASE WHEN, Conditional Aggregation, and PIVOT

> **Discussion opener:** "PIVOT is one of the most common SQL interview requirements in analytics engineering. Most databases don't have a native PIVOT keyword — you build it with CASE WHEN inside aggregate functions. This is the 'conditional aggregation' pattern."

### Conditional Aggregation — The PIVOT Pattern
```sql
-- Transform row data into columns (pivot)
-- Original data: server_id, metric_type, value (one row per server per metric)
-- Goal: one row per server with cpu, memory, disk as separate columns

SELECT
    server_id,
    MAX(CASE WHEN metric_type = 'cpu'    THEN avg_value END) AS avg_cpu,
    MAX(CASE WHEN metric_type = 'memory' THEN avg_value END) AS avg_memory,
    MAX(CASE WHEN metric_type = 'disk'   THEN avg_value END) AS avg_disk
FROM server_metrics
GROUP BY server_id
ORDER BY server_id;
```
*Why MAX()? Because after WHERE-like filtering via CASE WHEN, only one non-NULL value remains per group — MAX picks it. AVG/MIN/SUM work too for this pattern.*

### Column to Rows — UNPIVOT Pattern
```sql
-- The reverse: transform columns into rows
-- Useful when source data is wide-format and you need long-format for analysis

-- Using UNION ALL (most portable):
SELECT server_id, 'cpu'    AS metric_type, avg_cpu    AS value FROM server_wide
UNION ALL
SELECT server_id, 'memory' AS metric_type, avg_memory AS value FROM server_wide
UNION ALL
SELECT server_id, 'disk'   AS metric_type, avg_disk   AS value FROM server_wide;
```

### Cohort Analysis Pattern
```sql
-- Cohort: group users/servers by their first-seen date
-- Then track behavior over time relative to that cohort date

WITH first_report AS (
    SELECT server_id, MIN(report_date) AS cohort_date
    FROM daily_metrics
    GROUP BY server_id
),
cohort_activity AS (
    SELECT
        m.server_id,
        f.cohort_date,
        m.report_date,
        DATEDIFF('day', f.cohort_date, m.report_date) AS days_since_first
    FROM daily_metrics m
    JOIN first_report f ON m.server_id = f.server_id
)
SELECT
    cohort_date,
    MAX(CASE WHEN days_since_first = 0 THEN 1 ELSE 0 END) AS day_0,
    MAX(CASE WHEN days_since_first = 1 THEN 1 ELSE 0 END) AS day_1,
    MAX(CASE WHEN days_since_first = 7 THEN 1 ELSE 0 END) AS day_7,
    MAX(CASE WHEN days_since_first = 30 THEN 1 ELSE 0 END) AS day_30
FROM cohort_activity
GROUP BY cohort_date;
```

### Running Total with CASE WHEN
```sql
-- Categorize + aggregate in one pass
SELECT
    region,
    COUNT(*) AS total_servers,
    SUM(CASE WHEN tier = 'gold'   THEN 1 ELSE 0 END) AS gold_count,
    SUM(CASE WHEN tier = 'silver' THEN 1 ELSE 0 END) AS silver_count,
    SUM(CASE WHEN tier = 'bronze' THEN 1 ELSE 0 END) AS bronze_count,
    ROUND(100.0 * SUM(CASE WHEN tier = 'gold' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_gold
FROM servers
GROUP BY region
ORDER BY total_servers DESC;
```

**Interview Q&A:**
- Q: Does DuckDB/PostgreSQL have native PIVOT? A: DuckDB has `PIVOT` syntax. PostgreSQL requires CASE WHEN. Snowflake has PIVOT. BigQuery has PIVOT (recently added). Always know the CASE WHEN approach — it's universal.
- Q: What's the difference between `FILTER (WHERE ...)` and `CASE WHEN`? A: `FILTER` is cleaner syntax for conditional aggregation in PostgreSQL/DuckDB: `COUNT(*) FILTER (WHERE tier = 'gold')`. Same result as `SUM(CASE WHEN tier='gold' THEN 1 ELSE 0 END)`.
- Q: How would you pivot when you don't know the column values ahead of time? A: Dynamic pivot — requires either dynamic SQL (stored procedures), application layer logic, or features like DuckDB's `PIVOT` with auto-detection. This is a senior-level distinction.

---

## C. Python — pytest and Writing Testable Pipeline Code

> **Discussion opener:** "Untested pipelines fail silently in production. pytest is the standard. The key pattern for data pipelines: test pure transformation functions in isolation — don't test against live databases or S3. Mock external dependencies with `unittest.mock`."

### Basic pytest Structure
```python
# test_transformations.py
import pytest
from datetime import date

# The function we're testing (in transformations.py)
def compute_cpu_delta(today_cpu: float, yesterday_cpu: float) -> float:
    """Returns day-over-day CPU change, rounded to 2 decimal places."""
    return round(today_cpu - yesterday_cpu, 2)

def classify_server(avg_cpu: float) -> str:
    """Classify server health based on average CPU."""
    if avg_cpu >= 90:   return 'critical'
    if avg_cpu >= 75:   return 'warning'
    if avg_cpu >= 50:   return 'normal'
    return 'idle'

# Tests
class TestCpuDelta:
    def test_positive_delta(self):
        assert compute_cpu_delta(80.5, 72.1) == 8.4

    def test_negative_delta(self):
        assert compute_cpu_delta(65.0, 72.5) == -7.5

    def test_zero_delta(self):
        assert compute_cpu_delta(72.5, 72.5) == 0.0

class TestClassifyServer:
    @pytest.mark.parametrize("cpu, expected", [
        (95.0, 'critical'),
        (90.0, 'critical'),
        (80.0, 'warning'),
        (75.0, 'warning'),
        (60.0, 'normal'),
        (50.0, 'normal'),
        (30.0, 'idle'),
    ])
    def test_classification(self, cpu, expected):
        assert classify_server(cpu) == expected
```

### Fixtures — Shared Test Data
```python
import pytest
import pandas as pd

@pytest.fixture
def sample_metrics_df():
    """Reusable DataFrame fixture for multiple tests."""
    return pd.DataFrame({
        'server_id': ['srv-01', 'srv-02', 'srv-03'],
        'avg_cpu': [85.0, 45.2, 92.1],
        'report_date': ['2026-02-26', '2026-02-26', '2026-02-26']
    })

def test_filter_high_cpu(sample_metrics_df):
    high_cpu = sample_metrics_df[sample_metrics_df['avg_cpu'] >= 80]
    assert len(high_cpu) == 2
    assert set(high_cpu['server_id']) == {'srv-01', 'srv-03'}

def test_mean_cpu(sample_metrics_df):
    mean = sample_metrics_df['avg_cpu'].mean()
    assert abs(mean - 74.1) < 0.01
```

### Mocking External Dependencies
```python
from unittest.mock import patch, MagicMock

# The function that calls S3 (we don't want actual S3 in tests)
def load_metrics_from_s3(bucket: str, key: str) -> pd.DataFrame:
    import boto3
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(obj['Body'])

# Test it without touching S3
@patch('boto3.client')
def test_load_metrics_from_s3(mock_boto3):
    # Setup mock
    import io
    mock_s3 = MagicMock()
    mock_boto3.return_value = mock_s3
    mock_s3.get_object.return_value = {
        'Body': io.BytesIO(b"server_id,avg_cpu\nsrv-01,72.5\nsrv-02,45.2")
    }

    # Call function
    result = load_metrics_from_s3('my-bucket', 'metrics/daily.csv')

    # Assert
    assert len(result) == 2
    assert result['avg_cpu'].iloc[0] == 72.5
    mock_s3.get_object.assert_called_once_with(Bucket='my-bucket', Key='metrics/daily.csv')
```

### Testing Pipeline Steps — The Right Level of Abstraction
```python
# Anti-pattern: testing too big (integration test disguised as unit test)
def test_full_pipeline():
    run_pipeline()   # this hits DB, S3, Spark — slow, fragile, not a unit test

# Better: test each transformation in isolation
def aggregate_by_server(df: pd.DataFrame) -> pd.DataFrame:
    """Pure function — no side effects, easy to test."""
    return (df.groupby('server_id')
              .agg(avg_cpu=('cpu', 'mean'), max_cpu=('cpu', 'max'))
              .reset_index())

def test_aggregate_by_server():
    input_df = pd.DataFrame({
        'server_id': ['srv-01', 'srv-01', 'srv-02'],
        'cpu': [70.0, 80.0, 45.0]
    })
    result = aggregate_by_server(input_df)
    assert result.loc[result['server_id']=='srv-01', 'avg_cpu'].iloc[0] == 75.0
    assert result.loc[result['server_id']=='srv-01', 'max_cpu'].iloc[0] == 80.0
```

**Interview Q&A:**
- Q: What is the difference between unit tests and integration tests? A: Unit tests test one function in isolation, with all dependencies mocked. Integration tests test multiple components working together with real (or near-real) external systems. Unit tests are fast; integration tests catch wiring bugs.
- Q: What is `@pytest.fixture` and why use it? A: A factory that creates shared test resources (DataFrames, DB connections, config objects) and handles teardown. Avoids duplicating setup code across tests.
- Q: How would you test a Spark job? A: Use a local SparkSession in tests (`SparkSession.builder.master("local[1]")`). Test transformation functions with small DataFrames. Keep Spark tests in a separate test suite (they're slow).
- Q: What is parametrize? A: `@pytest.mark.parametrize` runs the same test with multiple input sets — avoids copy-paste tests for different cases.

---

## D. Technology — Apache Airflow

> **Discussion opener:** "Airflow is the de facto standard for data pipeline orchestration. You describe pipelines as DAGs — Directed Acyclic Graphs — in Python code. Airflow handles scheduling, retry, alerting, and dependency management. Every modern data team either uses Airflow or something inspired by it (Prefect, Dagster, Mage)."

### Core Concepts

```
DAG (Directed Acyclic Graph)
├── Task 1: Extract (PythonOperator)
│   └── Task 2: Validate (PythonOperator)  ← depends on Task 1
│       ├── Task 3a: Load to S3 (S3Hook)   ← depends on Task 2
│       └── Task 3b: Send Alert (EmailOp)  ← depends on Task 2
│           └── Task 4: Archive (PythonOp) ← depends on 3a
```

- **DAG:** The workflow definition. Contains tasks + dependencies.
- **Task:** A unit of work. Implemented as Operators.
- **Operator:** The task type — `PythonOperator`, `BashOperator`, `GlueCrawlerOperator`, `S3ToRedshiftOperator`, etc.
- **Schedule:** Cron expression. `@daily` = `0 0 * * *`. `@hourly` = `0 * * * *`.
- **XCom:** Cross-task communication. Tasks can push/pull small values (not DataFrames).

### A Real DAG
```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator

# Default arguments inherited by all tasks
default_args = {
    'owner': 'data-engineering',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': True,
    'email': ['alerts@company.com'],
}

with DAG(
    dag_id='daily_server_metrics',
    schedule_interval='0 6 * * *',      # 6 AM UTC daily
    start_date=datetime(2026, 1, 1),
    catchup=False,                        # don't backfill missed runs
    default_args=default_args,
    tags=['capacity', 'telemetry'],
) as dag:

    def extract_metrics(**context):
        """Pull metrics from APM API. Returns count for validation."""
        ds = context['ds']               # execution date: '2026-02-27'
        # ... fetch from API, write to S3 ...
        return {'rows': 6000, 'date': ds}

    def validate_metrics(**context):
        """Check row count meets minimum threshold."""
        ti = context['task_instance']
        upstream = ti.xcom_pull(task_ids='extract_metrics')
        assert upstream['rows'] >= 5000, f"Row count too low: {upstream['rows']}"

    extract = PythonOperator(
        task_id='extract_metrics',
        python_callable=extract_metrics,
        provide_context=True,
    )

    validate = PythonOperator(
        task_id='validate_metrics',
        python_callable=validate_metrics,
        provide_context=True,
    )

    crawl = GlueCrawlerOperator(
        task_id='update_catalog',
        config={'Name': 'server-metrics-crawler'},
    )

    # Define dependencies with >> (bit-shift operator)
    extract >> validate >> crawl
```

### Airflow Concepts Map
```
Component          | Purpose
-------------------|----------------------------------------------------
Scheduler          | Reads DAG files, triggers tasks on schedule
Worker             | Executes tasks (Celery, Kubernetes, or Sequential)
Webserver          | UI — DAG graph, task logs, history
Metadata DB        | PostgreSQL/MySQL — stores run history, XCom values
Executor           | How tasks run: LocalExecutor, CeleryExecutor, KubernetesExecutor
Connection         | Stored credentials (S3, Glue, Redshift, Slack) — reusable across DAGs
Variable           | Key-value config store — accessible in any DAG
Sensor             | Waits for an external condition (S3FileExists, ExternalTask)
```

**Interview Q&A:**
- Q: What is `catchup=False` and why do you almost always want it? A: Prevents Airflow from backfilling all missed DAG runs since `start_date`. Without it, deploying a DAG with start_date 30 days ago triggers 30 immediate runs. Almost always set False unless you explicitly want backfilling.
- Q: What is an XCom and what's its limitation? A: Cross-task message passing — tasks push values to the metadata DB, downstream tasks pull them. Limitation: only for small values (metadata, row counts, paths). Never pass DataFrames through XCom — they belong in S3/GCS.
- Q: What happens when an Airflow task fails? A: It retries `retries` times with `retry_delay` between attempts. After exhausting retries, task status = FAILED. Downstream tasks that depend on it are marked UPSTREAM_FAILED and don't run.
- Q: How do you pass the execution date to a task? A: Via `context['ds']` (date string) or `context['execution_date']` (datetime). The `{{ ds }}` Jinja template in SQL queries. This is critical for idempotent pipelines — each run processes exactly its own day.
- Q: What is idempotency in an Airflow context? A: Running a DAG multiple times for the same date produces the same result. Achieved by: DELETE then INSERT (not just INSERT), partition overwrite in S3, using execution_date to scope all reads and writes.

---

## Today's Key Interview Talking Points

1. **"BFS is a queue. DFS is a stack (or recursion). The data structure IS the algorithm for tree traversal."**
2. **"Level-by-level BFS: snapshot `len(queue)` before the inner loop — that's your level boundary."**
3. **"PIVOT with CASE WHEN works in every SQL engine. Know it first; learn engine-specific PIVOT syntax second."**
4. **"Test transformation functions in isolation — pure functions are the unit test sweet spot in data engineering."**
5. **"Airflow DAGs are code, not config — you get version control, testing, and code reuse for free."**
6. **"`catchup=False` and idempotent tasks are the two rules that prevent Airflow disasters."**

---

## Behavioral Anchor — Citi Story #8

**Topic: Reliability + Automation**

Practice this story (2 minutes, STAR format):

> *"At Citi we had hundreds of collection jobs running across four APM tools — CA APM, AppDynamics, Dynatrace, BMC TrueSight. The problem: jobs would fail silently. Nobody knew until the next morning when the dashboard showed gaps. I built a validation layer that checked row counts post-collection and compared against the server inventory. If any server's data was missing, it escalated immediately rather than waiting for the next cycle. This reduced mean-time-to-detect collection failures from hours to minutes. What I'd do today: wrap this in an Airflow DAG with a Sensor waiting for S3 files and a validation task that asserts row counts — same logic, operationalized correctly."*

**Gemini: ask Sean to tell this story unprompted. Time him. Give STAR feedback.**

---

## End of Day 8 — Wrap-Up

Gemini reports:
```
Day 8 Complete.
Topics covered: Trees/BFS/DFS | CASE WHEN PIVOT | pytest | Airflow
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 9: Two Pointers + Date/Time SQL + Concurrency + Kafka Deep Dive
```
