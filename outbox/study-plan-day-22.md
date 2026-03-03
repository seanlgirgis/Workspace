---
created: 2026-03-02
updated: 2026-03-02
summary: Day 22 — Week 4 opens with weighted graph algorithms (Dijkstra, Bellman-Ford), Recursive CTEs for hierarchical data, asyncio for DE, and Apache Flink fundamentals.
tags: [study-plan, day-22, dijkstra, bellman-ford, recursive-cte, asyncio, flink]
---

# Day 22 — Dijkstra + Bellman-Ford | Recursive CTEs | asyncio | Apache Flink

**Theme:** Week 4 is about the patterns that appear at staff/principal level and in specialized domains like finance. These are differentiators — most candidates don't know them.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is the core LRU Cache data structure? Why two structures?
2. What is `n & (n-1)` and when is it useful?
3. Name the 4 principles of Data Mesh.
4. What is point-in-time correct joining and why does it prevent data leakage?
5. What is the difference between Trino and Athena?
6. What does the `_delta_log` contain and what 3 things does it enable?

---

## A. LeetCode — Weighted Graph Algorithms (70 min)

### Why Weighted Graphs Now

Weeks 1-3 covered unweighted BFS/DFS for connectivity and traversal. Weighted graphs add edge costs — critical for:
- Shortest path in network topology (which route is cheapest/fastest?)
- Dependency ordering with priorities
- Resource allocation problems

Finance relevance: optimal routing of transactions, dependency analysis in compute graphs, circuit breaker analysis.

---

### Dijkstra's Algorithm — Single Source Shortest Path (non-negative weights)

**Mental model:** Greedy. Always explore the cheapest unvisited node next. Use a min-heap as the frontier.

**Time complexity:** O((V + E) log V) with a binary heap.

**Key constraint:** Does NOT work with negative edge weights.

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start):
    """
    graph: adjacency list {node: [(neighbor, weight), ...]}
    Returns: dist dict — shortest distance from start to every node
    """
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]   # (cost, node)

    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]:
            continue   # stale entry — already found shorter path
        for v, weight in graph[u]:
            new_cost = cost + weight
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))

    return dist
```

---

### LC #743: Network Delay Time (Medium)

**Problem:** There are n nodes labeled 1 to n and a list of travel times as directed edges `times[i] = (u, v, w)`. Return the minimum time for all nodes to receive a signal sent from node `k`. If impossible, return -1.

```
Input:  times = [[2,1,1],[2,3,1],[3,4,1]], n=4, k=2
Output: 2
```

```python
def networkDelayTime(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = dijkstra(graph, k)

    # All nodes except those in graph might not be reachable
    # Build dist for all 1..n nodes
    dist = {i: float('inf') for i in range(1, n+1)}
    dist[k] = 0
    heap = [(0, k)]

    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]:
            continue
        for v, w in graph[u]:
            if cost + w < dist[v]:
                dist[v] = cost + w
                heapq.heappush(heap, (dist[v], v))

    max_dist = max(dist.values())
    return max_dist if max_dist < float('inf') else -1
```

---

### LC #787: Cheapest Flights Within K Stops (Medium)

**Problem:** Find the cheapest price from `src` to `dst` with at most `k` stops.

**Why standard Dijkstra fails here:** It finds the globally shortest path, ignoring the stop constraint. You need to track (cost, stops).

```python
def findCheapestPrice(n, flights, src, dst, k):
    # Bellman-Ford variant: relax edges k+1 times (k stops = k+1 edges)
    prices = [float('inf')] * n
    prices[src] = 0

    for i in range(k + 1):
        temp = prices[:]   # snapshot before this round's updates
        for u, v, w in flights:
            if prices[u] == float('inf'):
                continue
            if prices[u] + w < temp[v]:
                temp[v] = prices[u] + w
        prices = temp

    return prices[dst] if prices[dst] < float('inf') else -1
```

**Why copy `prices` to `temp`:** Without the copy, updates in round i could be used in the same round i, effectively allowing more than i hops. The copy enforces "each round = exactly one more edge allowed."

---

### Bellman-Ford Algorithm — Handles Negative Weights

**When to use:** Dijkstra fails with negative edges. Bellman-Ford handles them. Also detects negative cycles.

**Time complexity:** O(V × E) — slower than Dijkstra.

```python
def bellman_ford(edges, n, src):
    """
    edges: list of (u, v, weight)
    n: number of nodes (0 to n-1)
    Returns: dist array, or signals negative cycle
    """
    dist = [float('inf')] * n
    dist[src] = 0

    # Relax all edges V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycles: if any edge still relaxes, cycle exists
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None   # negative cycle detected

    return dist
```

**Intuition:** After V-1 iterations, the shortest path using at most V-1 edges is found (a path in a V-node graph uses at most V-1 edges if no cycles). If a V-th iteration still relaxes an edge, there's a negative cycle.

---

### When to Use Which

| Algorithm | Weights | Complexity | Use Case |
|-----------|---------|-----------|---------|
| BFS | Unweighted | O(V+E) | Shortest path by hop count |
| Dijkstra | Non-negative | O((V+E)logV) | Most shortest-path problems |
| Bellman-Ford | Any (including negative) | O(VE) | Negative weights, detect negative cycles |
| Floyd-Warshall | Any | O(V³) | All-pairs shortest path (small graphs) |

---

## B. SQL — Recursive CTEs for Hierarchical Data (45 min)

### Why Recursive CTEs

Finance is full of hierarchies: org charts, account ownership chains, cost center rollups, security reference data (parent/child asset classes). A recursive CTE walks these hierarchies in pure SQL without application code.

### The Pattern

```sql
WITH RECURSIVE hierarchy AS (
    -- Anchor: starting point (root nodes, or a specific node)
    SELECT
        employee_id,
        manager_id,
        name,
        0 AS level,
        CAST(name AS VARCHAR) AS path
    FROM employees
    WHERE manager_id IS NULL   -- root: no manager

    UNION ALL

    -- Recursive: join current level to next level
    SELECT
        e.employee_id,
        e.manager_id,
        e.name,
        h.level + 1,
        h.path || ' > ' || e.name
    FROM employees e
    JOIN hierarchy h ON e.manager_id = h.employee_id
)
SELECT * FROM hierarchy ORDER BY level, path;
```

**Key rules:**
1. Must have an anchor SELECT (non-recursive)
2. Must have a recursive SELECT joined to the CTE itself
3. Connected with `UNION ALL` (UNION would be very slow — dedup on every iteration)
4. Must terminate: each iteration must produce fewer rows

### Practice Schema — Server Infrastructure Hierarchy

```sql
CREATE TABLE infra_hierarchy AS
SELECT * FROM (VALUES
    ('us-east-1', NULL,        'AWS Region',       1),
    ('az-1a',     'us-east-1', 'Availability Zone',2),
    ('az-1b',     'us-east-1', 'Availability Zone',2),
    ('rack-01',   'az-1a',     'Physical Rack',    3),
    ('rack-02',   'az-1a',     'Physical Rack',    3),
    ('rack-03',   'az-1b',     'Physical Rack',    3),
    ('srv-001',   'rack-01',   'Server',           4),
    ('srv-002',   'rack-01',   'Server',           4),
    ('srv-003',   'rack-02',   'Server',           4),
    ('srv-004',   'rack-03',   'Server',           4)
) AS t(node_id, parent_id, node_type, depth);
```

### Practice Query 1 — Full Hierarchy with Path

```sql
WITH RECURSIVE infra_tree AS (
    SELECT
        node_id,
        parent_id,
        node_type,
        0                           AS depth,
        CAST(node_id AS VARCHAR)    AS full_path
    FROM infra_hierarchy
    WHERE parent_id IS NULL   -- start at root

    UNION ALL

    SELECT
        h.node_id,
        h.parent_id,
        h.node_type,
        t.depth + 1,
        t.full_path || ' / ' || h.node_id
    FROM infra_hierarchy h
    JOIN infra_tree t ON h.parent_id = t.node_id
)
SELECT
    REPEAT('  ', depth) || node_id  AS indented_name,
    node_type,
    depth,
    full_path
FROM infra_tree
ORDER BY full_path;
```

### Practice Query 2 — Count Servers Under Each Zone

```sql
WITH RECURSIVE infra_tree AS (
    SELECT node_id, parent_id, node_type
    FROM infra_hierarchy
    WHERE parent_id IS NULL

    UNION ALL

    SELECT h.node_id, h.parent_id, h.node_type
    FROM infra_hierarchy h
    JOIN infra_tree t ON h.parent_id = t.node_id
),
server_counts AS (
    -- Assign each server to all its ancestors
    SELECT
        t1.node_id AS ancestor,
        t2.node_id AS server
    FROM infra_tree t1
    JOIN infra_tree t2 ON t2.node_id LIKE t1.node_id || '%'  -- simplified
    WHERE t2.node_type = 'Server'
)
SELECT ancestor, COUNT(DISTINCT server) AS server_count
FROM server_counts
GROUP BY ancestor;
```

### Practice Query 3 — Find All Ancestors of a Node

```sql
-- "Which region/zone/rack does srv-003 belong to?"
WITH RECURSIVE ancestors AS (
    SELECT node_id, parent_id, node_type, 0 AS depth
    FROM infra_hierarchy
    WHERE node_id = 'srv-003'   -- start at the leaf

    UNION ALL

    SELECT h.node_id, h.parent_id, h.node_type, a.depth + 1
    FROM infra_hierarchy h
    JOIN ancestors a ON h.node_id = a.parent_id  -- walk UP the tree
)
SELECT node_id, node_type, depth FROM ancestors ORDER BY depth;
```

**Finance use case:** "Which cost center owns this account? Who approved it? What is the regulatory jurisdiction?"

---

## C. Python — asyncio for Data Engineers (30 min)

### Why asyncio in DE

Traditional pipeline: call 100 APIs sequentially → 100 × 200ms = 20 seconds.
asyncio pipeline: call 100 APIs concurrently → ~200ms total (+ overhead).

asyncio is not threading. It's cooperative multitasking on a single thread. No GIL contention. Best for I/O-bound workloads: HTTP APIs, S3 reads, database queries.

### Core Concepts

```python
import asyncio
import aiohttp   # async HTTP client — pip install aiohttp

# async def = a coroutine function
# await = yield control until this I/O completes
# asyncio.gather = run multiple coroutines concurrently

async def fetch_server_metrics(session, server_id):
    url = f"https://api.telemetry.internal/servers/{server_id}/metrics"
    async with session.get(url) as response:
        return await response.json()

async def fetch_all_metrics(server_ids):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_server_metrics(session, sid) for sid in server_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Entry point
async def main():
    server_ids = [f"srv-{i:03d}" for i in range(1, 101)]
    metrics = await fetch_all_metrics(server_ids)
    print(f"Fetched metrics for {len(metrics)} servers")

asyncio.run(main())
```

### Handling Failures Gracefully

```python
async def fetch_with_retry(session, server_id, retries=3):
    for attempt in range(retries):
        try:
            async with session.get(
                f"https://api.telemetry.internal/servers/{server_id}",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                elif resp.status == 429:   # rate limited
                    await asyncio.sleep(2 ** attempt)   # exponential backoff
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                return {"server_id": server_id, "error": "timeout"}
            await asyncio.sleep(1)
```

### Semaphore — Control Concurrency

```python
# Don't hammer the API — limit to 20 concurrent requests
async def fetch_with_semaphore(session, sem, server_id):
    async with sem:   # only 20 coroutines run this block at once
        return await fetch_server_metrics(session, server_id)

async def fetch_all_bounded(server_ids, max_concurrent=20):
    sem = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_semaphore(session, sem, sid) for sid in server_ids]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

### asyncio vs threading vs multiprocessing

| Approach | Best for | Gotcha |
|----------|----------|--------|
| asyncio | High concurrency I/O (100s of API calls) | Requires async-compatible libraries |
| threading | Moderate I/O (10-20 threads) | GIL limits CPU work; race conditions |
| multiprocessing | CPU-bound (transforms, parsing) | High overhead; separate memory space |
| concurrent.futures | Both (abstraction over above two) | Good default for most pipeline tasks |

### Airflow + asyncio

Airflow DAGs themselves are not async. But operators can spawn async workloads:

```python
# In an Airflow PythonOperator:
def fetch_metrics_task(**context):
    server_ids = context["dag_run"].conf.get("server_ids", [])
    results = asyncio.run(fetch_all_bounded(server_ids))
    return results
```

---

## D. Technology — Apache Flink Fundamentals (45 min)

### What Flink Is

Apache Flink is a distributed stateful stream processing framework. The key word is **stateful**: Flink maintains state across events, enabling complex windowed aggregations, CEP (complex event processing), and exactly-once delivery at scale.

**Spark Streaming vs Flink:**
| Dimension | Spark Structured Streaming | Apache Flink |
|-----------|--------------------------|--------------|
| Processing model | Micro-batch (small batches at intervals) | True event-by-event streaming |
| Latency | 100ms–1s (micro-batch interval) | < 10ms possible |
| State management | Limited (stateful ops via watermarks) | Native, first-class stateful operators |
| Exactly-once | Yes (checkpointing) | Yes (checkpointing + Chandy-Lamport) |
| Batch support | Yes (same API) | Yes (DataStream or Table API) |
| Use case | Streaming ETL, aggregations | CEP, real-time ML scoring, low-latency alerts |

### Core Concepts

**Event Time vs Processing Time:**
- **Processing time:** when Flink receives the event. Simple but wrong if events arrive out-of-order.
- **Event time:** the timestamp embedded in the event itself. Correct but requires handling late arrivals.
- **Ingestion time:** when Kafka received the event (middle ground).

```
Event:    [server_id: srv-001, cpu: 82.5, event_time: 09:00:00.123]
                                                           ↑ use this
Processing time: 09:00:01.456  ← when Flink got it (could be delayed)
```

**Watermarks:** Flink's mechanism for handling late events. A watermark at time T means "I believe all events with time ≤ T have arrived. I'll now close windows ending at T."

```
Events arriving:  [09:00:01] [09:00:00] [09:00:05] [09:00:03] [09:00:09]
                                                                 ↑ if watermark max_lateness = 5s
                                                                 watermark = 09:00:04
                                                                 → triggers window ending at 09:00:00
```

**Windows:** How Flink groups events for aggregation.
- **Tumbling window:** fixed, non-overlapping (every 5 minutes)
- **Sliding window:** overlapping (5-min window, slides every 1 min)
- **Session window:** gap-based (window closes after N seconds of inactivity)

### Flink Architecture

```
JobManager (coordinator):
  - Receives job graph
  - Schedules tasks to TaskManagers
  - Manages checkpoints
  - Single point of failure → use HA with ZooKeeper/K8s

TaskManagers (workers):
  - Execute tasks (operators)
  - Maintain state (in-memory + RocksDB backend for large state)
  - Communicate state snapshots to durable storage (S3, HDFS)

Checkpoint:
  - Snapshot of all operator state at a consistent point
  - Stored in S3 or HDFS
  - On failure: restore from last checkpoint → exactly-once
```

### Python Flink API (PyFlink) Sketch

```python
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.datastream.functions import AggregateFunction
from pyflink.common.time import Time
from pyflink.common.watermark_strategy import WatermarkStrategy, Duration

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(4)

# Source: Kafka
kafka_source = FlinkKafkaConsumer(
    topics="server-telemetry",
    deserialization_schema=...,
    properties={"bootstrap.servers": "kafka:9092", "group.id": "flink-capacity"}
)

stream = env.add_source(kafka_source)

# Watermark strategy: allow events up to 10 seconds late
watermarked = stream.assign_timestamps_and_watermarks(
    WatermarkStrategy
        .for_bounded_out_of_orderness(Duration.of_seconds(10))
        .with_timestamp_assigner(lambda event, _: event["event_time_ms"])
)

# Window: 5-minute tumbling, keyed by server_id
result = (watermarked
    .key_by(lambda e: e["server_id"])
    .window(TumblingEventTimeWindows.of(Time.minutes(5)))
    .aggregate(AvgCpuAggregator())
)

# Sink: Kafka or S3
result.add_sink(...)
env.execute("capacity-cpu-5min-agg")
```

### When to Recommend Flink in an Interview

**Use Flink when:**
- Latency requirement < 100ms (Spark micro-batch isn't fast enough)
- Complex stateful aggregations (session analysis, CEP)
- Exactly-once matters AND you need true streaming (not micro-batch)
- Finance: real-time risk calculation, fraud detection, order book aggregation

**Don't use Flink when:**
- Your pipeline is batch (Spark is simpler)
- Latency of 1-5 minutes is fine (Spark Streaming or Kafka Streams)
- Team has no Flink experience (operational complexity is high)

**One-liner for interviews:**
> "Flink is the right choice when you need true streaming with sub-second latency and complex stateful operations. For most capacity planning workloads at our scale, Spark Streaming's micro-batch is sufficient. Flink would be the answer if I needed to detect a CPU spike within 5 seconds of it happening."

---

## Behavioral Anchor — Day 22

> "Tell me about a time you had to work with data from a system you didn't fully understand."

Strong answers cover:
- How you built understanding quickly (documentation, experiments, talking to the source team)
- How you validated your assumptions before building on them
- What you got wrong first and how you corrected it

---

## Day 22 Checklist

- [ ] Coded Dijkstra from scratch using a min-heap
- [ ] Coded LC #743 (Network Delay) and explained the "stale entry" check
- [ ] Coded LC #787 (Cheapest Flights) and explained why the temp copy matters
- [ ] Know when Bellman-Ford is required over Dijkstra
- [ ] Wrote and ran the recursive CTE hierarchy query in DuckDB
- [ ] Can write the "walk UP the tree" (ancestor) recursive query from scratch
- [ ] Wrote an asyncio gather() example with Semaphore control
- [ ] Can explain event time vs processing time in Flink
- [ ] Can explain what a watermark is in one sentence
- [ ] Know when to recommend Flink vs Spark Streaming
