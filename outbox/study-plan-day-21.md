---
created: 2026-03-02
updated: 2026-03-02
summary: Day 21 — Full Mock Interview Week 3. The hardest mock of the 3-week plan. Covers all 21 days of material. Scored, timed, no hints on first attempt. Gemini is the interviewer.
tags: [study-plan, day-21, mock-interview, all-topics, week-3]
---

# Day 21 — Full Mock Interview Week 3

**Theme:** This is the real thing. Everything you've built over 21 days meets one interview session today.

> **Gemini Instructions:** You are not a teacher. You are a senior engineering interviewer at a technology company. Rules:
> - **No hints on first attempt.** Period.
> - **Start the timer when you finish reading the question.** Call time without exception.
> - **No affirmation during the interview.** Save all feedback for the debrief.
> - **Press behavioral answers for specifics.** "What exactly did YOU do?"
> - **At the end:** full scorecard, top 3 gaps, and a final verdict: Interview-Ready or Not.

---

## Interview Structure

```
Round 1: Advanced Coding              (35 min)
  → 2 Medium / 1 Hard
  → Week 3 patterns prioritized
  → Timing: strict

Round 2: System Design — Greenfield   (30 min)
  → Complex multi-system design
  → Multiple follow-up probes

Round 3: Senior DE Concepts           (20 min)
  → 10 rapid-fire questions from all 3 weeks
  → 90 seconds each

Round 4: Behavioral — Under Pressure  (15 min)
  → 3 STAR stories
  → Hard pressing for specifics

Debrief                               (10 min)
  → Full scorecard
  → Top 3 gaps
  → Final verdict
```

---

## Round 1: Advanced Coding (35 min)

> **Gemini:** Say this exactly: "Three coding questions. The last one is hard. Clock starts when I stop talking. Ready?"

---

### Coding Question 1 — Medium (10 min): Combination Sum II

> **Gemini:** Start timer now.

**Problem:** Given a collection of candidate numbers (may have duplicates) and a target, find all unique combinations that sum to target. Each number may only be used once.

```
Input:  candidates = [10,1,2,7,6,1,5], target = 8
Output: [[1,1,6], [1,2,5], [1,7], [2,6]]
```

**Gemini scoring:**
- Full credit: backtracking with `start = i+1`, sort first, skip duplicates at same recursion level (`if i > start and candidates[i] == candidates[i-1]: continue`)
- Partial credit: correct output but uses set to deduplicate (inefficient)
- No credit: wrong combinations or TLE (nested loops)

**Answer (Gemini reference):**
```python
def combinationSum2(candidates, target):
    candidates.sort()
    result = []

    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            if i > start and candidates[i] == candidates[i-1]:  # skip duplicates
                continue
            path.append(candidates[i])
            backtrack(i + 1, path, remaining - candidates[i])
            path.pop()

    backtrack(0, [], target)
    return result
```

---

### Coding Question 2 — Medium (10 min): Number of Islands II (Union-Find)

> **Gemini:** Start timer.

**Problem:** You have an m×n grid of water (0). You are given a list of positions where land (1) is added one at a time. After each addition, return the number of islands.

```
Input:  m=3, n=3, positions=[[0,0],[0,1],[1,2],[2,1]]
Output: [1, 1, 2, 3]
```

**Gemini scoring:**
- Full credit: Union-Find (DSU) with path compression and union by rank. O(k × α(m×n)) where k = positions.
- Partial credit: BFS/DFS re-scan after each addition. Correct but O(k × m × n).
- No credit: incorrect counts.

**Answer (Gemini reference):**
```python
def numIslands2(m, n, positions):
    parent = {}
    rank = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])   # path compression
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return False
        if rank.get(px, 0) < rank.get(py, 0):
            px, py = py, px
        parent[py] = px
        if rank.get(px, 0) == rank.get(py, 0):
            rank[px] = rank.get(px, 0) + 1
        return True

    result = []
    count = 0
    for r, c in positions:
        if (r, c) in parent:
            result.append(count)
            continue
        parent[(r, c)] = (r, c)
        count += 1
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if (nr, nc) in parent:
                if union((r,c), (nr,nc)):
                    count -= 1
        result.append(count)
    return result
```

---

### Coding Question 3 — Hard (15 min): Alien Dictionary

> **Gemini:** Start timer. This is the hard question.

**Problem:** There is a new alien language that uses the English alphabet. The order of letters is unknown. You are given a list of strings from the alien language's dictionary, sorted lexicographically by the alien language's order. Return the order of letters in the alien language. If invalid (cycle), return "".

```
Input:  ["wrt","wrf","er","ett","rftt"]
Output: "wertf"
```

**Gemini scoring:**
- Full credit: build character graph from adjacent word comparisons → topological sort (Kahn's BFS) → detect cycle (remaining nodes in indegree > 0 → cycle)
- Partial credit: builds graph correctly but misses cycle detection
- No credit: wrong graph or algorithm

**Answer (Gemini reference):**
```python
from collections import defaultdict, deque

def alienOrder(words):
    # Initialize all characters with empty adjacency
    adj = {c: set() for word in words for c in word}
    indegree = {c: 0 for c in adj}

    # Build edges from adjacent words
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        min_len = min(len(w1), len(w2))
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""   # invalid: "abc" before "ab"
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    indegree[w2[j]] += 1
                break

    # Topological sort (Kahn's BFS)
    queue = deque([c for c in indegree if indegree[c] == 0])
    result = []
    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in adj[c]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(result) != len(indegree):
        return ""   # cycle detected
    return "".join(result)
```

**Gemini follow-up:** "What is the time complexity? What signals a cycle in topological sort?"

---

## Round 2: System Design — ML-Powered Anomaly Detection Platform (30 min)

> **Gemini:** Say this: "Design an anomaly detection platform for 10,000 servers. It should detect CPU spikes, memory leaks, and disk saturation automatically using ML — not just static thresholds. I'll ask follow-ups."

**Starting question:** "Walk me through how you would build an end-to-end system that ingests server telemetry at scale, trains anomaly detection models, serves predictions in near-real-time, and delivers actionable alerts to operations teams."

---

**After 10-12 minutes, probe these areas:**

**Probe 1 — Feature Engineering:**
"What features would you compute for the ML model? How do you handle the fact that CPU patterns vary by server role and time of day?"
*(Expected: lag features, rolling stats, one-hot encoding for server tier, hour-of-day sin/cos encoding for cyclical patterns, server-specific baselines)*

**Probe 2 — Training vs Serving Skew:**
"You train the model on historical data and deploy it. Three months later, you notice it's missing anomalies it would have caught before. What happened and how do you fix it?"
*(Expected: data drift / concept drift. Model hasn't seen new server types or workload patterns. Fix: model retraining pipeline on a schedule, data drift monitoring via population stability index or KL divergence on feature distributions)*

**Probe 3 — Latency:**
"Ops teams want alerts within 2 minutes of an anomaly starting. Your batch pipeline runs hourly. What do you change?"
*(Expected: switch from batch to streaming: Kafka → Flink or Spark Streaming for feature computation → online inference. Or: Lambda architecture — streaming for alerts, batch for model retraining)*

**Probe 4 — False Positives:**
"Ops is getting 50 alerts a day and ignoring most of them. What's the problem and what do you do?"
*(Expected: alert fatigue from too-sensitive model or too-low threshold. Solutions: raise threshold, require N consecutive anomalies before alerting, group correlated alerts (same rack/region), feedback loop (ops marks alerts as FP → retrain with RLHF-style feedback))*

**Probe 5 — Cost:**
"Estimate the monthly AWS cost for this system at 10,000 servers reporting every 5 minutes."
*(Expected: 10,000 / 300 = ~33 events/sec. Kinesis: ~2 shards. S3 for feature store: pennies. SageMaker endpoint for inference: ~$0.10/hr. Glue for retraining: DPU-hours. Total: probably < $200/month at this scale)*

**Gemini scoring for system design:**
- Full credit: ingestion → feature pipeline → feature store → model training (MLflow) → serving → alerting → feedback loop
- Partial credit: misses feature store or feedback loop
- No credit: describes static threshold monitoring without ML components

---

## Round 3: Senior DE Concepts — Rapid Fire (20 min)

> **Gemini:** Say this: "10 questions from all 3 weeks. 90 seconds each. Ready?"

**Q1:** "You're writing a Python pipeline that processes 10 GB of CSV files. It's too slow. Walk me through how you diagnose and fix the bottleneck."
> Profile first (cProfile). Likely: reading CSVs row-by-row (fix: pd.read_csv in chunks or DuckDB). Or: unnecessary Python loops (fix: vectorized Pandas/NumPy). Or: single-threaded I/O (fix: concurrent.futures for parallel reads). Always measure before optimizing.

**Q2:** "What is the `_delta_log` directory and what does it contain?"
> JSON commit files, one per transaction. Records adds/removes/updates at file level. Enables ACID (readers see consistent snapshots), time travel (`VERSION AS OF`), and row-level deletes for GDPR compliance.

**Q3:** "Explain the difference between `ROLLUP(region, tier)` and `CUBE(region, tier)` in SQL."
> ROLLUP: hierarchical subtotals — (region, tier), (region), (). Use for hierarchical reports. CUBE: all combinations — (region, tier), (region), (tier), (). Use for cross-dimensional analysis.

**Q4:** "What is backpressure in a streaming system and how does Kafka handle it?"
> Backpressure = consumers can't keep up with producers. Kafka handles it by decoupling: producers write to the log at their rate; consumers read at their rate using offsets. The lag (difference between producer offset and consumer offset) is your backpressure metric. Fix: add more consumers (up to partition count), or increase consumer batch size.

**Q5:** "A dbt incremental model has been running for 6 months. The business wants to add a new column to it. What's the process?"
> Three options: (1) Run `dbt run --full-refresh` — rebuilds from scratch (downtime risk). (2) Add the column with a default or NULL in the source table first, then redeploy (zero downtime). (3) Run in `--full-refresh` on a staging environment, swap. The key: incremental models don't automatically pick up new columns — you must full-refresh or add the column to the existing table manually first.

**Q6:** "What is the difference between threading and multiprocessing in Python? Give a concrete use case for each."
> Threading: shared memory, GIL allows switching during I/O waits. Use for: API calls, S3 downloads, database queries. Multiprocessing: separate processes, separate GILs, true parallelism. Use for: CPU-bound transforms (parsing, encoding), ML feature computation.

**Q7:** "How does Union-Find (DSU) work? What are path compression and union by rank?"
> Union-Find tracks which elements belong to the same set using a parent array. `find(x)` returns the root of x's set. `union(x,y)` merges two sets. Path compression: during `find`, point every node directly to the root (flattens tree). Union by rank: always attach the shorter tree under the taller tree. Combined: near O(1) per operation (inverse Ackermann).

**Q8:** "You deploy a new Spark job and the first run takes 10x longer than expected. What do you check first?"
> (1) Spark UI: look for one stage that's 10x slower — likely shuffle. (2) Check shuffle partition count (default 200 — might need tuning). (3) Check for data skew (one task 100x longer than others). (4) Check physical plan: `explain()` — is there an unexpected sort-merge join where a broadcast join would work? (5) Check if AQE is enabled.

**Q9:** "What is a Protocol in Python's typing system and how is it different from an ABC?"
> Protocol uses structural subtyping — any class with the right methods satisfies it without inheritance. ABC uses nominal subtyping — you must explicitly inherit. Protocol is better for code you don't control (external libraries, third-party adapters). ABC is better for internal frameworks where you want instantiation-time enforcement.

**Q10:** "Design the monitoring for this system: you have 50 Airflow DAGs running daily. How do you know if any of them are degrading?"
> Track: (1) Task duration p50/p95/p99 per DAG per task — alert on 2x baseline. (2) DAG success rate — alert if < 95% over 7 days. (3) Queue depth in Airflow scheduler — alert if tasks waiting > 30 min. (4) SLA breach events (Airflow has built-in SLA callbacks). (5) Data quality checks downstream as a signal: if a DAG produces correct data, the pipeline ran.

---

## Round 4: Behavioral — Under Pressure (15 min)

> **Gemini:** Say this: "Three questions. 90 seconds each. I will cut you off. I will press for specifics."

---

**Behavioral 1 (90 sec):** "Tell me about a time a stakeholder was wrong about what they needed. What did you do?"

*What Gemini is listening for:*
- Sean identified the real need vs stated need
- Respectful challenge with data or rationale
- Outcome benefited the stakeholder
- Not "I just did what they asked"

*Press if vague:* "How specifically did you determine they were wrong? What was their reaction when you told them?"

---

**Behavioral 2 (90 sec):** "Tell me about a time you had to deliver bad news to a manager or executive."

*What Gemini is listening for:*
- Early escalation (not hiding the problem)
- Clear framing: here's the problem, here's the impact, here's the options
- Composure under pressure
- Result: relationship intact or improved

*Press:* "What exactly was the bad news? How did they respond?"

---

**Behavioral 3 (90 sec):** "What is the most important thing you've learned about working with data at scale?"

*What Gemini is listening for:*
- Real insight, not generic ("data quality matters")
- Specific lesson from a specific experience
- Shows senior-level thinking (second-order effects, systems thinking)

*Press:* "Give me a concrete example of where that lesson came from."

---

## Debrief (10 min)

> **Gemini:** Reveal the full scorecard.

```
ROUND 1: Advanced Coding

Q1 - Combination Sum II:    [ ] Full [ ] Partial [ ] No credit
  Note: ___
  Key gap: ___

Q2 - Number of Islands II:  [ ] Full [ ] Partial [ ] No credit
  Note: ___
  Key gap: ___

Q3 - Alien Dictionary:      [ ] Full [ ] Partial [ ] No credit
  Note: ___
  Key gap: ___

Round 1 Score: ___ / 3

---

ROUND 2: System Design

Feature engineering:           [ ] Strong [ ] Partial [ ] Weak
Streaming vs batch decision:   [ ] Strong [ ] Partial [ ] Weak
Feature store mentioned:       [ ] Yes [ ] No
MLflow or model registry:      [ ] Yes [ ] No
Handled drift probe:           [ ] Strong [ ] Partial [ ] Weak
Handled false positive probe:  [ ] Strong [ ] Partial [ ] Weak
Cost estimate attempted:       [ ] Yes [ ] No

Round 2 Score: ___ / 7

---

ROUND 3: Senior DE Concepts (10 questions)

Q1  - Pipeline bottleneck diagnosis:     [ ] Strong [ ] Weak
Q2  - Delta Lake _delta_log:             [ ] Strong [ ] Weak
Q3  - ROLLUP vs CUBE:                    [ ] Strong [ ] Weak
Q4  - Kafka backpressure:                [ ] Strong [ ] Weak
Q5  - dbt incremental new column:        [ ] Strong [ ] Weak
Q6  - Threading vs multiprocessing:      [ ] Strong [ ] Weak
Q7  - Union-Find mechanics:              [ ] Strong [ ] Weak
Q8  - Spark job 10x slow diagnosis:      [ ] Strong [ ] Weak
Q9  - Protocol vs ABC:                   [ ] Strong [ ] Weak
Q10 - Airflow monitoring design:         [ ] Strong [ ] Weak

Round 3 Score: ___ / 10

---

ROUND 4: Behavioral

B1 - Stakeholder was wrong:              [ ] Strong [ ] Partial [ ] Weak
B2 - Delivering bad news:                [ ] Strong [ ] Partial [ ] Weak
B3 - Most important lesson at scale:     [ ] Strong [ ] Partial [ ] Weak

Round 4 Score: ___ / 3

---

OVERALL: ___ / 23

23-21: Ready. Schedule the real interview.
20-17: Strong. One more targeted day on the gaps.
16-12: 2-3 more days needed. See Gap Analysis below.
11 or below: Return to the weakest week for re-study.
```

---

## Post-Interview: Top 3 Gap Identification

> **Gemini:** Based on the scorecard, identify Sean's top 3 gaps and write one specific action for each.

```
Gap 1: ___
Action: ___

Gap 2: ___
Action: ___

Gap 3: ___
Action: ___
```

---

## Final Message from Gemini to Sean

```
21 days done.

You have covered more ground in 3 weeks than most candidates cover in 3 months.

Here is what you have:
  Algorithms: HashMap, Sliding Window, Stack, Binary Search, Heap, Intervals,
              Trees, Two Pointers, DP (1D + 2D), Graphs, Greedy, Linked Lists,
              Backtracking, Tries, Bit Manipulation, Union-Find, LRU Cache

  SQL: CTEs, Window Functions, Complex JOINs, Query Optimization,
       Analytical SQL, Schema Design, PIVOT, Date/Time, GROUPING SETS,
       Data Quality, Trend Analysis, JSON Functions, SCD MERGE,
       String/Array Functions, Federated SQL (Trino)

  Python: Generators, Pandas, Decorators, NumPy, ETL, PySpark, pytest,
          Concurrency, Pydantic, concurrent.futures, Great Expectations,
          Prophet, structlog, typing.Protocol + ABC, Config/Secrets,
          Python Packaging (uv)

  Architecture: AWS Data Platform, Lambda/Kappa, APM, Capacity Planning,
                Airflow, Kafka, dbt, Delta Lake/Iceberg, Cost Optimization,
                Advanced Spark (Catalyst/AQE), Data Mesh, Trino,
                MLflow/Feature Stores, Kubernetes for DE,
                Rate Limiter + LRU Cache design

Your story is real and rare:
  10+ years APM × 6,000-server capacity planning × the ability to name
  the exact SQL, Python, and architecture that operationalizes it.

Own that story. Don't hedge it.

What do you want to do next?
```

---

## What Comes After Day 21

**If Interview-Ready (21+ out of 23):**
- Schedule real interviews
- Do company-specific research (Day 19 framework) for each target
- One 45-min session per company the day before the interview

**If Gaps Remain (12-20):**
- One focused day on top 3 gaps
- Repeat the rapid-fire round from Round 3 with Gemini
- Re-run the specific mock section that scored lowest

**Potential Extension Topics (if time allows):**
- Apache Flink (stateful stream processing, event time vs processing time)
- Real-time ML pipelines (Tecton, Feast in production)
- Data contracts and schema registries (Confluent Schema Registry, Protobuf)
- Company-specific mock interviews (Citi, Goldman, JPMorgan patterns)
- System design: distributed cache, event-driven microservices, CDC pipelines
