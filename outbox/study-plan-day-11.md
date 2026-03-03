---
created: 2026-03-02
updated: 2026-03-02
summary: Day 11 — Graphs (BFS/DFS + Topological Sort) | EXPLAIN + Query Plans | concurrent.futures | Delta Lake / Iceberg
tags: [study-plan, day-11, leetcode, sql, python, delta-lake, iceberg, graphs]
---

# Study Day 11: Networks, Optimization, and Modern Data Formats
**Theme:** Graph algorithms + Query internals + Parallel execution + ACID data lakes

---

## Spaced Repetition — Review from Days 1–10
*60 seconds each. Mark Strong / Review / Weak.*

**SR-1 (Day 1):** CTE vs temp table — when does the temp table win?
> When you need to reference the result set multiple times, or when you need an index on it. CTEs may or may not be materialized (engine-dependent). Temp tables always materialize to disk/memory.

**SR-2 (Day 6):** Why does sorting intervals by start enable the merge algorithm?
> After sorting, any overlapping interval is guaranteed to be adjacent. You only need to check if the next interval's start ≤ current merged end. No need to look ahead.

**SR-3 (Day 9):** Gaps & Islands — what does `date - ROW_NUMBER()` produce for consecutive dates?
> A constant. Dates 2026-02-01, 02-02, 02-03 with RN 1,2,3 give 2026-01-31 each time. Non-consecutive dates produce different constants, forming different groups.

**SR-4 (Day 10):** Coin Change — why does greedy fail and DP succeed?
> Greedy always takes the largest coin, missing combinations that use smaller coins more efficiently. DP evaluates all possibilities via the recurrence `dp[i] = min(dp[i-c] + 1 for each coin c)`.

**SR-5 (Day 10):** dbt `ref()` vs `source()` — when do you use each?
> `ref()`: reference another dbt model (transforms managed by dbt). `source()`: reference a raw table not managed by dbt (loaded externally by Fivetran, Glue, custom loader). Sources have freshness tests.

**SR-6 (Day 8):** What is Airflow `provide_context=True` for?
> Passes the Airflow execution context (ds, run_id, task_instance, etc.) as `**kwargs` to the Python callable. Needed to access `context['ds']` for the execution date or `context['task_instance']` for XCom.

---

## A. LeetCode — Graphs (BFS/DFS + Topological Sort)

> **Discussion opener:** "Graphs extend trees — a node can have any number of neighbors, and there can be cycles. Two traversal algorithms: BFS (queue, shortest path in unweighted graphs) and DFS (recursion or stack, connectivity, cycle detection). Topological sort is the special case for DAGs — ordering nodes so every dependency comes before the node that depends on it. Critical for build systems, task scheduling, and pipeline dependency resolution."

**Graph representations:**
- **Adjacency list:** `{node: [neighbors]}` — standard for sparse graphs
- **Grid as graph:** `[row][col]` — neighbors are up/down/left/right

---

### LC #200 — Number of Islands [Medium]
**Category:** DFS/BFS on a Grid

**Problem:**
Given a grid of '1' (land) and '0' (water), count the number of islands (connected groups of '1').
```
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
→ 3 islands
```

🎯 **Design Checkpoint:** "Every '1' starts a potential island. When you find one, flood-fill (DFS/BFS) to mark all connected '1's as visited. Count how many floods you start."

**Solution — DFS (in-place marking)** O(m×n) time, O(m×n) space (call stack)
```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        # Out of bounds or water or already visited → stop
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'    # mark as visited (in-place)
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)   # flood-fill this island

    return count
```

**Interview Q&A:**
- Q: Why mark visited cells in-place vs a separate `visited` set? A: Memory optimization — avoids O(m×n) extra space for a visited grid. Fine when you can mutate input. In production, use a separate visited set if you can't mutate.
- Q: How would you do this with BFS? A: Replace the recursive DFS with a queue. Push starting cell, then iteratively pop and push all unvisited neighbors.
- Q: Real-world analog? A: Network connectivity — finding isolated network segments. Infrastructure dependency analysis.

---

### LC #207 — Course Schedule [Medium] — Cycle Detection + Topological Sort
**Category:** Graph / Topological Sort

**Problem:**
`numCourses` courses, prerequisites `[ai, bi]` means must take `bi` before `ai`. Can you finish all courses?
`numCourses=2, prerequisites=[[1,0]]` → `true` (take 0 then 1)
`numCourses=2, prerequisites=[[1,0],[0,1]]` → `false` (cycle: need 0 for 1, need 1 for 0)

🎯 **Design Checkpoint:** "Build a directed graph. If there's a cycle, you can't finish. Cycle detection via DFS: node is in-progress → cycle found."

**Solution 1 — DFS with 3-state coloring** O(V+E) time, O(V+E) space
```python
def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    # Build adjacency list
    graph = {i: [] for i in range(numCourses)}
    for course, prereq in prerequisites:
        graph[course].append(prereq)

    # States: 0=unvisited, 1=in-progress (cycle if revisited), 2=done
    state = [0] * numCourses

    def dfs(course):
        if state[course] == 1:  return False   # cycle detected
        if state[course] == 2:  return True    # already processed

        state[course] = 1      # mark in-progress
        for prereq in graph[course]:
            if not dfs(prereq):
                return False
        state[course] = 2      # mark done
        return True

    return all(dfs(c) for c in range(numCourses))
```

**Solution 2 — BFS / Kahn's Algorithm (Topological Sort)** O(V+E) time
```python
from collections import deque

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    in_degree = [0] * numCourses
    graph = {i: [] for i in range(numCourses)}

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    # Start with all courses that have no prerequisites
    queue = deque(c for c in range(numCourses) if in_degree[c] == 0)
    completed = 0

    while queue:
        course = queue.popleft()
        completed += 1
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)

    return completed == numCourses   # if cycle exists, some courses never reach 0 in-degree
```

**Interview Q&A:**
- Q: What is Kahn's algorithm? A: BFS-based topological sort. Start with nodes that have no incoming edges (in-degree 0). Repeatedly remove such nodes and reduce neighbors' in-degrees. If all nodes are processed, no cycle. If not, a cycle prevents some nodes from reaching in-degree 0.
- Q: Where does topological sort appear in data engineering? A: Airflow DAG validation, dbt model dependency resolution, build systems (Makefile targets), schema migration ordering.
- Q: DFS cycle detection vs Kahn's — when to use each? A: DFS: when you need the actual cycle path or when working recursively. Kahn's: when you need the actual topological order of execution. Both detect cycles.

---

### LC #417 — Pacific Atlantic Water Flow [Medium]
**Category:** Multi-Source BFS/DFS

**Problem:**
Given a height matrix, water flows from high to low (or equal). Find cells where water can reach both the Pacific (top/left) and Atlantic (bottom/right) ocean.

🎯 **Design Checkpoint:** "Reverse the problem — instead of simulating water flowing down, flow UP from each ocean. Find cells reachable from both oceans."

**Solution — Multi-Source BFS** O(m×n) time, O(m×n) space
```python
from collections import deque

def pacificAtlantic(heights: list[list[int]]) -> list[list[int]]:
    rows, cols = len(heights), len(heights[0])
    directions = [(0,1),(0,-1),(1,0),(-1,0)]

    def bfs(starts):
        visited = set(starts)
        queue = deque(starts)
        while queue:
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and (nr, nc) not in visited
                        and heights[nr][nc] >= heights[r][c]):  # flow uphill
                    visited.add((nr, nc))
                    queue.append((nr, nc))
        return visited

    # Pacific starts: top row + left col
    pac_starts = [(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)]
    # Atlantic starts: bottom row + right col
    atl_starts = [(r, cols-1) for r in range(rows)] + [(rows-1, c) for c in range(cols)]

    pac_reachable = bfs(pac_starts)
    atl_reachable = bfs(atl_starts)

    return [[r, c] for r in range(rows) for c in range(cols)
            if (r, c) in pac_reachable and (r, c) in atl_reachable]
```

**Interview Q&A:**
- Q: Why reverse the problem? A: Forward simulation (water flowing down from each cell) would be O(m²×n²) — checking every cell as a starting point. Reverse BFS from ocean boundaries is O(m×n) — one pass per ocean.
- Q: What does "multi-source BFS" mean? A: Starting BFS from multiple source nodes simultaneously. All sources are added to the initial queue. The traversal expands from all of them at once. Common in problems where you want "reachable from any of these starting points."

---

### LC #684 — Redundant Connection [Medium] — Union-Find
**Category:** Union-Find (Disjoint Set Union)

**Problem:**
Given a tree with n nodes, one extra edge is added (creating a cycle). Return the redundant edge.
`edges = [[1,2],[1,3],[2,3]]` → `[2,3]`

🎯 **Design Checkpoint:** "Add edges one by one. If both endpoints are already in the same connected component → this edge creates a cycle → it's the redundant edge. Use Union-Find for O(α(n)) component tracking."

**Solution — Union-Find** O(n α(n)) ≈ O(n) time
```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    parent = list(range(len(edges) + 1))   # each node is its own parent initially
    rank = [0] * (len(edges) + 1)

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])   # path compression
        return parent[x]

    def union(x, y) -> bool:
        """Returns False if x and y are already connected (cycle!)."""
        rx, ry = find(x), find(y)
        if rx == ry:
            return False   # same component — this edge is redundant
        # Union by rank
        if rank[rx] < rank[ry]:  rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:  rank[rx] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]

    return []
```

**Interview Q&A:**
- Q: What is Union-Find (Disjoint Set Union)? A: Data structure for tracking connected components. Two operations: `find(x)` returns the root of x's component; `union(x, y)` merges two components. With path compression + union by rank: near O(1) per operation.
- Q: Applications in data engineering? A: Deduplication (finding records that are "the same entity"), connected component analysis in graphs, network topology analysis.

---

## B. SQL — EXPLAIN, Query Plans, and Index Strategy

> **Discussion opener:** "EXPLAIN is how you see what the database is actually doing. Understanding execution plans is what separates an engineer who writes SQL from an engineer who owns SQL in production. At Citi, understanding why a query took 45 seconds (full table scan, no partition pruning) vs 0.3 seconds (partition skip + index) was daily work."

### Reading a Query Plan
```sql
-- DuckDB / PostgreSQL: EXPLAIN ANALYZE gives estimated + actual costs
EXPLAIN ANALYZE
SELECT s.server_id, s.region, AVG(m.avg_cpu) AS avg_cpu
FROM servers s
JOIN daily_metrics m ON s.server_id = m.server_id
WHERE m.report_date >= '2026-02-01'
GROUP BY s.server_id, s.region
ORDER BY avg_cpu DESC;

-- Key terms to know:
-- Seq Scan: full table scan — O(n). Red flag for large tables.
-- Index Scan: using an index — much faster for selective queries.
-- Hash Join: build hash table from smaller table, probe with larger.
-- Merge Join: both sides sorted on join key — efficient for large sorted tables.
-- Nested Loop: O(n×m) — only efficient with small inner side + index.
-- Sort: sorting step — expensive if not on an index.
-- actual rows vs estimated rows: large discrepancy = stale statistics.
```

### Index Strategy
```sql
-- Rule 1: Index columns that appear in WHERE, JOIN ON, and ORDER BY.
CREATE INDEX idx_metrics_date ON daily_metrics(report_date);
CREATE INDEX idx_metrics_server_date ON daily_metrics(server_id, report_date);

-- Rule 2: Composite index column order matters.
-- (server_id, report_date) index helps:
--   WHERE server_id = 'srv-01'                     ✓
--   WHERE server_id = 'srv-01' AND report_date = X ✓
--   WHERE report_date = X                          ✗ (leading column not used)

-- Rule 3: Index doesn't help when you apply a function to the column:
-- BAD:  WHERE EXTRACT('year' FROM report_date) = 2026  -- can't use index
-- GOOD: WHERE report_date BETWEEN '2026-01-01' AND '2026-12-31'  -- uses index

-- Rule 4: Covering index — all needed columns are in the index
CREATE INDEX idx_metrics_covering ON daily_metrics(server_id, report_date, avg_cpu);
-- A query that only needs these 3 columns can be answered from the index alone (no table scan)
```

### Partition Pruning
```sql
-- In partitioned tables (Parquet on S3, Iceberg, BigQuery):
-- Filtering on the partition column = skipping entire partitions

-- Partition: report_date
-- This query scans ONE day of data (partition pruning):
SELECT * FROM daily_metrics WHERE report_date = '2026-02-27';

-- This scans ALL data (no pruning — function applied to partition col):
SELECT * FROM daily_metrics WHERE EXTRACT('month' FROM report_date) = 2;

-- Rule: partition columns must appear as-is in WHERE for pruning to work.
```

### Analyze Slow Queries — The Process
```sql
-- Step 1: EXPLAIN to see the plan without running
EXPLAIN SELECT ...;

-- Step 2: EXPLAIN ANALYZE to see actual execution stats
EXPLAIN ANALYZE SELECT ...;

-- Step 3: Check for:
--   Sequential scans on large tables → add index
--   Row estimate vs actual huge mismatch → ANALYZE table (update stats)
--   Nested loop on large tables → add index or rewrite
--   Sorts on non-indexed columns → add index on ORDER BY col

-- Step 4: ANALYZE after bulk loads to update statistics
ANALYZE daily_metrics;   -- updates pg_stats so the planner has accurate estimates
```

**Interview Q&A:**
- Q: What is a hash join and when does the optimizer choose it? A: Build a hash table from the smaller table, probe it with the larger. O(n+m). The optimizer chooses it when neither table is sorted on the join key and the smaller table fits in memory.
- Q: What is a covering index? A: An index that contains all columns a query needs — the query is answered entirely from the index without touching the table. Eliminates the "heap fetch" step. Dramatically faster for SELECT queries on large tables.
- Q: What causes stale statistics and why does it matter? A: Statistics are updated by `ANALYZE` or `VACUUM ANALYZE`. After large bulk loads, statistics are stale — the planner's row estimates are wrong, leading to bad plan choices (choosing a seq scan when an index would be better). Run ANALYZE after bulk loads.
- Q: Why can't you use an index when you wrap a column in a function? A: The index is built on the raw column values. Applying a function (YEAR(), UPPER(), etc.) produces a derived value that's not in the index. Solution: use a functional index on the expression, or rewrite the predicate to not use a function.

---

## C. Python — concurrent.futures Patterns for Data Pipelines

> **Discussion opener:** "concurrent.futures is the production-grade way to parallelize data work in Python. It unifies threading and multiprocessing under one interface. The patterns you need: parallel file processing, parallel API polling, parallel partition loading."

### ProcessPoolExecutor — Parallel Partition Processing
```python
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd

def process_partition(partition_path: str) -> dict:
    """Process one S3 partition — CPU-bound transformation."""
    df = pd.read_parquet(partition_path)

    return {
        "partition": partition_path,
        "rows": len(df),
        "avg_cpu": float(df['avg_cpu'].mean()),
        "p95_cpu": float(df['avg_cpu'].quantile(0.95)),
        "critical_count": int((df['avg_cpu'] >= 90).sum()),
    }

PARTITIONS = [
    "data/date=2026-02-01/part.parquet",
    "data/date=2026-02-02/part.parquet",
    "data/date=2026-02-03/part.parquet",
    "data/date=2026-02-04/part.parquet",
]

# Sequential
results_seq = [process_partition(p) for p in PARTITIONS]

# Parallel with 4 cores
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(process_partition, p): p for p in PARTITIONS}

    results = []
    for future in as_completed(futures):   # process as each completes
        partition = futures[future]
        try:
            result = future.result()
            results.append(result)
        except Exception as e:
            print(f"[ERROR] Partition {partition}: {e}")

print(f"Processed {len(results)} partitions")
```

### ThreadPoolExecutor — Parallel API Calls
```python
from concurrent.futures import ThreadPoolExecutor
import time

def poll_server_health(server_id: str, timeout: int = 5) -> dict:
    """I/O-bound: poll each server's health API."""
    time.sleep(0.2)   # simulated API latency
    return {"server_id": server_id, "status": "healthy", "latency_ms": 180}

SERVER_IDS = [f"srv-{i:02d}" for i in range(1, 21)]

# Parallel polling — 20 servers concurrently instead of serially
with ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(poll_server_health, SERVER_IDS))

# executor.map preserves ORDER (unlike as_completed which is arrival order)
print(f"Polled {len(results)} servers")
```

### Error Handling and Timeout Pattern
```python
from concurrent.futures import ProcessPoolExecutor, TimeoutError

def process_with_timeout(partition_paths: list[str], timeout_sec: int = 30) -> list:
    results = []
    errors = []

    with ProcessPoolExecutor() as executor:
        future_to_path = {executor.submit(process_partition, p): p for p in partition_paths}

        for future in as_completed(future_to_path, timeout=timeout_sec):
            path = future_to_path[future]
            try:
                result = future.result(timeout=5)   # per-future timeout
                results.append(result)
            except TimeoutError:
                errors.append(f"TIMEOUT: {path}")
            except Exception as e:
                errors.append(f"ERROR {path}: {type(e).__name__}: {e}")

    if errors:
        print(f"[WARNING] {len(errors)} failures:")
        for err in errors:
            print(f"  {err}")

    return results
```

**Interview Q&A:**
- Q: `executor.map()` vs `as_completed()` — what's the difference? A: `map()` preserves input order and blocks until all complete. `as_completed()` yields futures as they finish (out of order) — better when you want to process results immediately or handle partial failures without waiting for all.
- Q: How do you set the number of workers? A: ThreadPoolExecutor: `min(32, os.cpu_count() + 4)` is the Python default. ProcessPoolExecutor: `os.cpu_count()` by default. Tune based on the bottleneck — for I/O, more threads than CPUs is fine. For CPU, match CPU count.
- Q: How do you propagate errors from worker processes? A: `future.result()` re-raises any exception that occurred in the worker. Wrap in try/except to handle gracefully. Unhandled exceptions in workers don't crash the main process — they're stored in the future until `.result()` is called.

---

## D. Technology — Delta Lake and Apache Iceberg

> **Discussion opener:** "Traditional data lakes are immutable append-only files. Delta Lake and Iceberg add ACID transactions, schema evolution, time travel, and efficient upserts to data lakes. They solve the 'lakehouse' problem: you want S3/HDFS storage costs but database-level reliability and correctness."

### The Problem They Solve
```
Traditional Parquet on S3:
- No ACID — two writers can corrupt data
- No deletes or updates — append only (or full rewrite)
- No schema enforcement — silently accepts wrong schemas
- No time travel — can't query yesterday's data
- Slow upserts — must rewrite entire partition for CDC

Delta Lake / Iceberg:
- ACID transactions (serializable isolation)
- Row-level updates and deletes (critical for GDPR erasure requests)
- Schema evolution + enforcement
- Time travel — query data as of any timestamp
- Efficient MERGE for CDC (change data capture)
```

### Delta Lake — Core Concepts
```python
# Delta Lake adds a _delta_log/ directory to your S3 table location
# _delta_log/ contains JSON commit files (transaction log)

# PySpark with Delta Lake
from delta.tables import DeltaTable
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
    .getOrCreate()

# Write as Delta
df.write.format("delta").mode("overwrite").save("s3://bucket/server-metrics/")

# UPSERT (MERGE) — core operation for CDC
delta_table = DeltaTable.forPath(spark, "s3://bucket/server-metrics/")
delta_table.alias("target").merge(
    new_data.alias("source"),
    "target.server_id = source.server_id AND target.report_date = source.report_date"
).whenMatchedUpdateAll() \
 .whenNotMatchedInsertAll() \
 .execute()

# Time travel — query as of timestamp or version
df_yesterday = spark.read.format("delta") \
    .option("timestampAsOf", "2026-02-26") \
    .load("s3://bucket/server-metrics/")

df_v3 = spark.read.format("delta") \
    .option("versionAsOf", 3) \
    .load("s3://bucket/server-metrics/")

# Schema evolution
df_with_new_col.write.format("delta") \
    .option("mergeSchema", "true") \
    .mode("append").save("s3://bucket/server-metrics/")
```

### Delta Lake vs Iceberg — When to Choose
```
Feature             | Delta Lake         | Apache Iceberg
--------------------|--------------------|--------------------------
Origin              | Databricks (2019)  | Netflix (2018), Apache
Best with           | Databricks, Spark  | Spark, Flink, Trino, Athena
AWS integration     | EMR, Glue (with config) | Athena native support
Catalog required    | No (path-based)    | Yes (Glue, Hive, Nessie)
Time travel         | Yes                | Yes
MERGE/upsert        | Yes                | Yes
Schema evolution    | Yes                | Yes (richer spec)
Hidden partitioning | No                 | Yes (automatic partition handling)
```

### The Lakehouse Pattern
```
Sources → S3 (Bronze: raw append-only Parquet)
               ↓ (Glue ETL / Spark / dbt)
          S3 + Delta/Iceberg (Silver: cleaned, ACID, upsertable)
               ↓ (aggregation, business logic)
          S3 + Delta/Iceberg (Gold: business-ready, read-optimized)
               ↓
          Athena / Redshift / DuckDB (query layer)
               ↓
          QuickSight / Jupyter (consumers)
```

**Interview Q&A:**
- Q: What is the Delta transaction log and why is it important? A: A JSON log directory that records every transaction (insert, update, delete, schema change). Enables ACID: readers see a consistent snapshot, writers don't corrupt in-flight reads. Also enables time travel by replaying the log.
- Q: What is `VACUUM` in Delta Lake? A: Removes old Parquet files that are no longer referenced by the current table version. Without vacuuming, old time-travel versions accumulate indefinitely. Run after time-travel retention window passes.
- Q: How would you handle a GDPR "right to be forgotten" request in a data lake? A: With plain Parquet: impossible without rewriting all files. With Delta/Iceberg: `DELETE FROM table WHERE user_id = 'X'` — row-level delete tracked in the transaction log. Then VACUUM to physically remove the data files.
- Q: What is hidden partitioning in Iceberg? A: Iceberg manages partition transforms internally — queries don't need to know the partition scheme. You query by date, Iceberg handles the date-bucket mapping transparently. Avoids the "partition evolution" problem where changing your partition scheme breaks all downstream queries.

---

## Today's Key Interview Talking Points

1. **"For graph problems: BFS = shortest path, DFS = connectivity/cycles, topological sort = dependency ordering."**
2. **"Topological sort appears in real systems: Airflow, dbt, build systems. It's not just an algorithm."**
3. **"EXPLAIN ANALYZE first. A slow query is a plan problem until proven otherwise."**
4. **"Composite index column order matters — leading column must be in your WHERE clause."**
5. **"Delta Lake adds a _delta_log/ to S3 — that log IS the ACID guarantee."**
6. **"Iceberg's hidden partitioning solves partition evolution — query the data, not the partition scheme."**

---

## Behavioral Anchor — Citi Story #11

**Topic: Performance Optimization**

Practice this story (2 minutes, STAR format):

> *"At Citi, our morning capacity report was running for 45 minutes. The query was pulling 6,000 servers × 90 days of telemetry — millions of rows. I ran EXPLAIN and found a sequence scan across the entire metrics table — no partition pruning, no index. The WHERE clause had a YEAR() function wrapped around the date column, which prevented index use. Two changes: remove the function and use a date BETWEEN predicate, and create a composite index on (server_id, collection_date). Query time dropped to 4 seconds. The lesson: when someone says a query is slow, run EXPLAIN before you write any code."*

**Gemini: ask Sean to tell this story unprompted. Time him. Give STAR feedback.**

---

## End of Day 11 — Wrap-Up

Gemini reports:
```
Day 11 Complete.
Topics covered: Graphs + Topo Sort | EXPLAIN + Query Plans | concurrent.futures | Delta/Iceberg
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 12: Greedy + Data Quality SQL + Data Quality Python + AWS Cost Optimization
```
