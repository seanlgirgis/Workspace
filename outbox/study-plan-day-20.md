---
created: 2026-03-02
updated: 2026-03-02
summary: Day 20 — Comprehensive 3-Week Review. Self-assessment across all domains. Targeted drilling on weak areas identified in Day 14 mock interview. No new material.
tags: [study-plan, day-20, review, self-assessment, interview-readiness]
---

# Day 20 — Comprehensive Review & Interview Readiness Assessment

**Theme:** No new material. Today is triage and reinforcement. You find your gaps; you drill them; you go into Day 21 knowing your floor.

> **Rule:** If a topic takes you less than 30 seconds to recall fluently — move on. Spend time only where you stumble.

---

## Part 1 — Master Assessment (All 3 Weeks)

Score each item honestly: **Strong (S)**, **Shaky (K)**, or **Gap (G)**

### LeetCode Patterns

| Pattern | Example Problem | Your Score | Notes |
|---------|----------------|-----------|-------|
| HashMap / Two-Sum | LC #1 | |  |
| Sliding Window | LC #3 Longest Substring | | |
| Stack | LC #20 Valid Parentheses | | |
| Binary Search | LC #704, #153 | | |
| Heap / Top-K | LC #347 Top K Frequent | | |
| Merge Intervals | LC #56 | | |
| BFS on Graph | LC #200 Islands | | |
| DFS on Tree | LC #104 Max Depth | | |
| Two Pointers | LC #167, #15 3Sum | | |
| 1D Dynamic Programming | LC #322 Coin Change | | |
| Topological Sort | LC #207 Course Schedule | | |
| Greedy | LC #134 Gas Station | | |
| Linked List | LC #206 Reverse | | |
| Backtracking | LC #78 Subsets | | |
| 2D DP | LC #1143 LCS | | |
| Tries | LC #208 Implement Trie | | |
| Bit Manipulation | LC #136 Single Number | | |
| LRU Cache | LC #146 | | |

**Red flags (G scores) from above — list here:**
```
1. ___
2. ___
3. ___
```

---

### SQL Topics

| Topic | Can I write it from scratch? | Score | Notes |
|-------|------------------------------|-------|-------|
| CTE (non-recursive) | | | |
| CTE (recursive) | | | |
| Window: RANK/DENSE_RANK/ROW_NUMBER | | | |
| Window: trailing avg (ROWS BETWEEN) | | | |
| Window: LAG/LEAD | | | |
| Complex JOINs (LEFT, anti-join) | | | |
| Query Optimization / EXPLAIN | | | |
| PIVOT with CASE WHEN | | | |
| Date arithmetic + gaps & islands | | | |
| GROUPING SETS / ROLLUP / CUBE | | | |
| Data quality patterns | | | |
| Trend analysis + forecasting SQL | | | |
| JSON extraction (DuckDB) | | | |
| SCD Type 2 MERGE | | | |
| String/array functions | | | |
| Federated SQL (Trino concepts) | | | |

---

### Python

| Topic | Score | Notes |
|-------|-------|-------|
| Generators and `yield` | | |
| Pandas (groupby, merge, pivot, melt) | | |
| Decorators (timing, retry, caching) | | |
| NumPy (vectorized ops, broadcasting) | | |
| ETL with DuckDB | | |
| PySpark (RDD vs DataFrame, transformations vs actions) | | |
| pytest (fixtures, parametrize, monkeypatch) | | |
| Concurrency (threading vs multiprocessing, GIL) | | |
| Pydantic (validators, BaseModel, Settings) | | |
| concurrent.futures (ThreadPoolExecutor, ProcessPoolExecutor) | | |
| Great Expectations | | |
| Prophet / scikit-learn LinearRegression | | |
| structlog / logging | | |
| typing.Protocol + ABC | | |
| Config & Secrets (Pydantic Settings, Secrets Manager) | | |
| Python packaging (uv, pyproject.toml) | | |

---

### Technology / Architecture

| Topic | Score | Notes |
|-------|-------|-------|
| AWS Data Platform (S3 → Glue → Athena) | | |
| Spark architecture (driver, executor, DAG) | | |
| Lambda architecture vs Kappa | | |
| APM concepts and tools | | |
| Capacity planning framework | | |
| System design: capacity planning platform | | |
| Apache Airflow (DAG, operators, XCom, retries) | | |
| Kafka (topics, partitions, consumer groups, offsets) | | |
| dbt (ref, source, incremental, snapshot, tests) | | |
| Delta Lake / Iceberg (ACID, time travel, transaction log) | | |
| AWS Cost Optimization (Parquet, Athena, Glue pricing) | | |
| Advanced Spark (Catalyst, AQE, broadcast, skew) | | |
| Data Mesh (4 principles, data product) | | |
| Trino/Presto (federated SQL, connectors) | | |
| MLflow + Feature Stores | | |
| Kubernetes for DE (Jobs, KubernetesExecutor) | | |

---

## Part 2 — Targeted Drilling by Score

### For Every Gap (G): 20-minute drill

Use the following protocol for each G-scored item:

1. **Read the day's material for that topic** (5 min max — skim the section)
2. **Close the notes** — write the key concept from memory (3 min)
3. **Code or write the SQL** — from scratch, no references (10 min)
4. **Check your work** — run it or compare to the solution (2 min)

---

### For Every Shaky (K): 10-minute drill

1. **Say the concept out loud** — 3 sentences max
2. **Write one concrete example** — code or SQL
3. **Move on** — if you got it, you got it

---

### Gap Priority Order

Work in this order — highest interview frequency first:

**Tier 1 (high frequency, drill first):**
- BFS/DFS on Trees
- Sliding Window
- Dynamic Programming (1D and 2D)
- Window Functions (trailing avg, LAG/LEAD)
- Complex JOINs and anti-joins
- PySpark basics (transformations, actions)
- Airflow DAG concepts

**Tier 2 (medium frequency):**
- Backtracking
- Graphs + Topological Sort
- Greedy Algorithms
- CTEs (recursive)
- dbt (incremental, snapshot)
- Kafka (consumer groups, offsets)
- Delta Lake (transaction log)

**Tier 3 (differentiators):**
- Tries
- Bit Manipulation
- 2D DP
- Federated SQL / Trino
- Catalyst optimizer / AQE
- Data Mesh
- MLflow / Feature Stores

---

## Part 3 — The "Explain It" Test

For these 10 topics, pretend you are explaining to a smart non-engineer (a PM, or your interviewer's manager). Speak it out loud. 60 seconds each.

1. **What is a window function and when would you use one?**
2. **What is the difference between a data lake and a data warehouse?**
3. **What is Delta Lake and why does it matter?**
4. **Why would you use Kafka instead of just writing to S3 directly?**
5. **What is dbt and how does it fit into a data pipeline?**
6. **What is the GIL in Python and when does it matter?**
7. **What is Airflow and how do you make a pipeline retry on failure?**
8. **What is Adaptive Query Execution in Spark?**
9. **What is Data Mesh and when would you not use it?**
10. **What is a feature store and why do DEs need to care about it?**

---

## Part 4 — System Design Speed Round

Answer each in 3 minutes or less, drawing on paper or whiteboard:

**Design 1:** "Design a system that ingests server telemetry from 10,000 servers in real time and alerts if any server's CPU exceeds 90% for 5 consecutive minutes."

**Design 2:** "Design a data platform for a company that wants to analyze their product usage events. 50M events per day. Need dashboards updated within 1 hour."

**Design 3:** "Design a pipeline that builds a training dataset for an ML model that predicts server failures 48 hours in advance."

For each — draw:
```
[ Data Source ] → [ Ingest ] → [ Storage ] → [ Transform ] → [ Serve/Alert ]
```

Then answer:
- What format for storage? (Parquet/Delta/Avro — why?)
- What SLA? (freshness, availability)
- What breaks first at 10x scale?

---

## Part 5 — Behavioral Final Rehearsal

Speak each story out loud. Timer on. 90 seconds target.

| Story | Topic | Timed Score |
|-------|-------|-------------|
| Story 1 | Silent failure | ___s |
| Story 2 | Technical complexity | ___s |
| Story 3 | Change management | ___s |
| Story 4 | Production incident | ___s |
| Story 5 | Cross-functional collaboration | ___s |

**If any story goes over 2 minutes:** cut the setup, expand the result. The result is the point.

**If any story feels hollow:** "What exactly did YOU do?" — press yourself with that question. If the answer is vague, find a different story.

---

## Part 6 — Night-Before Mental Preparation

### What You Know (state it to yourself)

- You have 10+ years of real APM and capacity planning experience
- You have built monitoring systems for 6,000+ servers
- You know the exact tools: CA APM, AppDynamics, Dynatrace, BMC TrueSight
- You can name the SQL, the Python, and the architecture that operationalizes it
- You have 3 weeks of structured study across algorithms, SQL, Python, and DE architecture

### What to Do Tonight

1. No studying after 8pm
2. Review the 3-page "cheat sheet" (see below) — not new material
3. Get 7+ hours of sleep
4. Eat before the interview

### 3-Line Cheat Sheet (Commit to Memory)

```
LeetCode: read → edge cases → brute force → optimize → complexity
SQL: read → what GROUP BY? → what window? → what JOIN type? → run it
System Design: clarify → data flow → bottleneck → trade-offs
```

---

## Day 20 Checklist

- [ ] Completed the full master assessment table (Weeks 1-3)
- [ ] Drilled all G-scored items (20 min each)
- [ ] Drilled all K-scored items (10 min each)
- [ ] Passed the "Explain It" test on all 10 topics
- [ ] Drew at least 2 of the system design speed round diagrams
- [ ] Spoke all 5 behavioral stories out loud — none over 2 minutes
- [ ] Filled in the company research template for tomorrow's mock target
- [ ] Stopped studying by 8pm
