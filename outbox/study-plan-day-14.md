---
created: 2026-03-02
updated: 2026-03-02
summary: Day 14 — Full Mock Interview Week 2. Timed, scored, no hints on first attempt. Covers Days 8-13 plus spaced repetition from Days 1-7. Gemini is the interviewer.
tags: [study-plan, day-14, mock-interview, all-topics]
---

# Day 14 — Full Mock Interview Week 2

**Theme:** You are in the interview. No more lecture.

> **Gemini Instructions:** Today is different. You are NOT a teacher. You are an interviewer.
>
> Rules for Day 14:
> - **No hints on first attempt.** If Sean asks for a hint: "I can't help during the interview."
> - **Time every answer strictly.** Start timer when you finish reading the question. Call time without exception.
> - **Do not affirm as you go.** No "good!" or "exactly!" — save all feedback for the end.
> - **After each section:** privately note Strong / Review / Weak. Do not reveal until the full debrief.
> - **At the end:** full scorecard with every question marked. Identify top 3 gaps.
> - **Behavioral:** press for specifics. "What exactly did YOU do?" "What was the impact?"

---

## Interview Structure (Follow This Exactly)

```
Round 1: Technical Phone Screen — Week 2 Patterns    (30 min)
  → 3 coding questions (Easy, Medium, Medium)
  → 2 SQL questions (trend analysis, data quality)
  → Timing: strict

Round 2: System Design — Capacity Planning Platform  (25 min)
  → One open-ended design question
  → Gemini asks follow-up probes

Round 3: Technical Deep Dive — DE Concepts           (20 min)
  → Concurrency, Airflow, Kafka, Delta Lake
  → Architecture trade-offs

Round 4: Behavioral                                  (15 min)
  → 3 STAR stories under time pressure

Debrief                                              (10 min)
  → Full scorecard revealed
  → Top 3 gaps identified
  → Week 3 priorities
```

---

## Round 1: Technical Phone Screen (30 min)

> **Gemini:** Say this exactly: "Welcome back. This is a 30-minute technical screen. Coding, SQL, strict timing. Ready? Let's go."

---

### Coding Question 1 — Easy (5 min)

> **Gemini reads problem, starts timer immediately.**

**Problem:** Given a binary tree, return its maximum depth. A leaf node has no children. Maximum depth is the number of nodes along the longest path from the root to the farthest leaf.

```
Input:  root = [3, 9, 20, null, null, 15, 7]
Output: 3
```

**Gemini scoring — after Sean answers:**
- Full credit: recursive or iterative solution, correct base case (None → 0), correct return
- Partial credit: correct approach but syntax error or off-by-one
- No credit: wrong algorithm

**Answer (Gemini reference — do not reveal until after):**
```python
def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

---

### Coding Question 2 — Medium (10 min)

> **Gemini:** Start timer.

**Problem:** Given an integer array `nums`, find the contiguous subarray that has the largest sum and return that sum. (Kadane's Algorithm)

```
Input:  [-2,1,-3,4,-1,2,1,-5,4]
Output: 6  (subarray [4,-1,2,1])
```

*Note: This is LC #53 — Maximum Subarray. Related to sliding window / DP. Not directly covered in the plan — tests transfer of patterns.*

**Gemini scoring:**
- Full credit: O(n) solution using running sum (Kadane's) or DP
- Partial credit: O(n²) brute force — correct but note the gap
- No credit: incorrect

**Answer (Gemini reference):**
```python
def maxSubArray(nums):
    max_sum = curr_sum = nums[0]
    for num in nums[1:]:
        curr_sum = max(num, curr_sum + num)   # extend or restart
        max_sum = max(max_sum, curr_sum)
    return max_sum
```

> **Gemini follow-up (ask after solution):** "What is the time and space complexity? What does `curr_sum = max(num, curr_sum + num)` represent conceptually?"

---

### Coding Question 3 — Medium (10 min)

> **Gemini:** Start timer.

**Problem:** Given an array of gas station amounts and costs, determine if there is a starting station from which you can complete the circuit. Return the starting station index, or -1 if impossible.

```
Input:  gas = [1,2,3,4,5], cost = [3,4,5,1,2]
Output: 3
```

**Gemini scoring:**
- Full credit: greedy O(n) solution with total_surplus check and reset logic
- Partial credit: brute force O(n²) — correct but slow
- No credit: incorrect

**Answer (Gemini reference):**
```python
def canCompleteCircuit(gas, cost):
    total, curr, start = 0, 0, 0
    for i in range(len(gas)):
        delta = gas[i] - cost[i]
        total += delta
        curr += delta
        if curr < 0:
            start = i + 1
            curr = 0
    return start if total >= 0 else -1
```

---

### SQL Question 1 (5 min)

> **Gemini reads problem, starts timer.**

**Schema:**
```
servers(server_id, region, tier)
daily_metrics(server_id, report_date DATE, avg_cpu FLOAT)
```

**Problem:** Write a SQL query that returns, for each server, the 7-day trailing average CPU utilization as of each day in the dataset. Show: server_id, report_date, avg_cpu (raw), trailing_7day_avg.

**Gemini scoring:**
- Full credit: correct OVER clause with ROWS BETWEEN 6 PRECEDING AND CURRENT ROW and PARTITION BY server_id ORDER BY report_date
- Partial credit: missing PARTITION BY, or wrong frame
- No credit: uses subquery/GROUP BY instead of window function

**Answer (Gemini reference):**
```sql
SELECT
    server_id,
    report_date,
    avg_cpu,
    ROUND(AVG(avg_cpu) OVER (
        PARTITION BY server_id
        ORDER BY report_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ), 2) AS trailing_7day_avg
FROM daily_metrics
ORDER BY server_id, report_date;
```

---

### SQL Question 2 (5 min)

> **Gemini:** Start timer.

**Problem:** Using the same schema, find all servers that have NOT reported any data in the last 2 days (report_date < CURRENT_DATE - 2). Return: server_id, region, tier, last_report_date (NULL if never reported).

**Gemini scoring:**
- Full credit: LEFT JOIN + GROUP BY + HAVING or subquery anti-join
- Partial credit: correct result but uses NOT IN with a subquery (flag the NULL risk)
- No credit: INNER JOIN or wrong filter

**Answer (Gemini reference):**
```sql
SELECT
    s.server_id,
    s.region,
    s.tier,
    MAX(m.report_date) AS last_report_date
FROM servers s
LEFT JOIN daily_metrics m ON s.server_id = m.server_id
GROUP BY s.server_id, s.region, s.tier
HAVING MAX(m.report_date) < CURRENT_DATE - INTERVAL '2 days'
    OR MAX(m.report_date) IS NULL
ORDER BY last_report_date NULLS FIRST;
```

---

## Round 2: System Design (25 min)

> **Gemini:** Say this: "Design a capacity planning platform for 6,000 servers. I'll ask follow-up questions."

**Starting question:** "Walk me through how you would design an end-to-end system that collects server telemetry from 6,000 servers, detects capacity risks automatically, and delivers actionable reports to infrastructure teams."

**Gemini: after 10-12 minutes of Sean talking, probe these areas:**

**Probe 1 — Data Collection:**
"What if the agents go down silently? How does your system detect a missing reporting server vs a server that has low CPU?"

**Probe 2 — Scale:**
"At 6,000 servers reporting every 5 minutes, what is your ingest rate in events/second? How does your architecture handle that?"
*(Expected: 6,000 / 300 sec = 20 events/sec — very manageable. Kafka with 3 partitions is overkill. For 1-minute cadence: 100/sec. Kinesis single shard handles 1,000/sec.)*

**Probe 3 — Forecast Accuracy:**
"A server's CPU spikes every Monday due to batch jobs but is low otherwise. Your linear trend says it's fine. What's wrong with that?"
*(Expected: linear trend misses seasonality. Need Prophet or week-over-week comparison. Or: separate weekday vs weekend baselines.)*

**Probe 4 — Operational:**
"Who sees the capacity report? What does it look like? How do they act on it?"
*(Expected: infrastructure team, management. Traffic light dashboard. Automated tickets or alerts for < 30-day runway. Weekly email digest.)*

**Probe 5 — Cost:**
"How much does this system cost to run on AWS?"
*(Expected: S3 (minimal), Athena (per query, Parquet = cheap), Glue (DPU-hours), Lambda (free tier covers alerts). Estimate: < $50/month for this scale.)*

**Gemini scoring for system design:**
- Full credit: covers collection, storage (S3 Parquet), catalog (Glue), query (Athena/DuckDB), forecasting (linear regression or Prophet), alerting (Airflow or Lambda), reporting
- Partial credit: covers the major pieces but gaps in forecasting or alerting
- No credit: describes monitoring (dashboards) but not capacity planning (forecasting + right-sizing)

---

## Round 3: Technical Deep Dive (20 min)

> **Gemini:** Say this: "I have 8 rapid-fire technical questions. 90 seconds each. Ready?"

**Q1:** "What is the difference between threading and multiprocessing in Python? When do you use each?"
> Threading: concurrent I/O (GIL allows switching during waits). Multiprocessing: parallel CPU (separate processes, separate GILs). Threading for API polling; multiprocessing for data transformation.

**Q2:** "You're designing an Airflow DAG for daily telemetry processing. What would you set for `retries`, `retry_delay`, and `catchup`? Explain each."
> retries=3 (transient failures common in API calls). retry_delay=5min (exponential backoff spirit). catchup=False (avoid backfill cascade on deployment). Email on failure = True.

**Q3:** "Explain consumer groups in Kafka. If a topic has 10 partitions and you add an 11th consumer, what happens?"
> Each partition goes to exactly one consumer in the group. 11th consumer is idle — extra consumers beyond partition count don't help. To increase parallelism: increase partitions first.

**Q4:** "What is Delta Lake's transaction log and what problem does it solve?"
> `_delta_log/` directory of JSON commit files. Records every transaction atomically. Enables ACID (readers see consistent snapshot), time travel (replay log to past state), and row-level deletes (critical for GDPR).

**Q5:** "What is `ref()` in dbt and how does it differ from `source()`?"
> `ref('model')`: references another dbt model — resolves dependency order, environment-aware (dev/prod schema). `source('db', 'table')`: references raw external table not managed by dbt — supports freshness tests.

**Q6:** "A dbt model is marked as `incremental`. What happens on the first run vs subsequent runs?"
> First run: full build of the model. Subsequent runs: `is_incremental()` macro filters to new rows only (based on a watermark column like updated_at). Merged or inserted into the target table. Avoids full historical reprocessing.

**Q7:** "What is the difference between `ROLLUP` and `CUBE` in SQL?"
> ROLLUP(a,b): hierarchical subtotals — (a,b), (a), (). Left-to-right removal. CUBE(a,b): all combinations — (a,b), (a), (b), (). Use ROLLUP for hierarchies (region → tier). Use CUBE for cross-dimensional analysis.

**Q8:** "Name three optimizations that make Athena queries faster and cheaper."
> (1) Parquet/ORC columnar format (scan only needed columns). (2) Snappy/gzip compression (less data scanned). (3) S3 partitioning + WHERE clause on partition column (skip entire partitions). Bonus: LIMIT clause in Athena does NOT reduce scan cost.

---

## Round 4: Behavioral (15 min)

> **Gemini:** Say this: "Three behavioral questions. 2 minutes each. I'll call time."

---

**Behavioral 1 (2 min):** "Tell me about a time you discovered a silent failure in a system — something that was failing but nobody knew."

*What Gemini is listening for:*
- Specific system (not vague)
- What the failure was and why it was silent
- How Sean discovered it
- What he did to fix AND prevent recurrence
- Measurable impact

*Press if vague:* "What exactly was failing? How did you detect it specifically?"

---

**Behavioral 2 (2 min):** "Tell me about a time you had to convince a team to change how they worked. What was the change and how did you do it?"

*What Gemini is listening for:*
- Change had a real cost (people had to do something different)
- Sean's argument — data, not authority
- Pushback and how he handled it
- Result

*Press if surface-level:* "What was the pushback? How did you address it specifically?"

---

**Behavioral 3 (2 min):** "Tell me about the most technically complex problem you solved. Walk me through how you approached it."

*What Gemini is listening for:*
- Problem clarity (not vague "complex problem")
- Structured approach (diagnose → design → test → deploy)
- What made it hard specifically
- Lessons learned

*Press:* "What specifically made it complex? What would you do differently?"

---

## Debrief (10 min)

> **Gemini:** Reveal the full scorecard now.

```
ROUND 1: Technical Screen (Coding + SQL)

Coding Q1 - Max Tree Depth:          [ ] Full [ ] Partial [ ] No credit
  Note: ___

Coding Q2 - Max Subarray (Kadane's): [ ] Full [ ] Partial [ ] No credit
  Note: ___

Coding Q3 - Gas Station:             [ ] Full [ ] Partial [ ] No credit
  Note: ___

SQL Q1 - Trailing 7-day average:     [ ] Full [ ] Partial [ ] No credit
  Note: ___

SQL Q2 - Servers with missing data:  [ ] Full [ ] Partial [ ] No credit
  Note: ___

Round 1 Score: ___ / 5

---

ROUND 2: System Design

Covered data collection:             [ ] Yes [ ] Partial [ ] No
Covered storage + format:            [ ] Yes [ ] Partial [ ] No
Covered forecasting:                 [ ] Yes [ ] Partial [ ] No
Covered alerting / reporting:        [ ] Yes [ ] Partial [ ] No
Handled seasonality probe:           [ ] Yes [ ] Partial [ ] No
Handled data quality (silent gaps):  [ ] Yes [ ] Partial [ ] No

Round 2 Score: ___ / 6 ___

---

ROUND 3: Technical Deep Dive

Q1 - Threading vs multiprocessing:   [ ] Strong [ ] Weak
Q2 - Airflow parameters:             [ ] Strong [ ] Weak
Q3 - Kafka consumer groups:          [ ] Strong [ ] Weak
Q4 - Delta Lake transaction log:     [ ] Strong [ ] Weak
Q5 - dbt ref() vs source():          [ ] Strong [ ] Weak
Q6 - dbt incremental:                [ ] Strong [ ] Weak
Q7 - ROLLUP vs CUBE:                 [ ] Strong [ ] Weak
Q8 - Athena optimizations:           [ ] Strong [ ] Weak

Round 3 Score: ___ / 8

---

ROUND 4: Behavioral

Story 1 (silent failure):            [ ] Strong [ ] Partial [ ] Weak
Story 2 (change management):         [ ] Strong [ ] Partial [ ] Weak
Story 3 (complex problem):           [ ] Strong [ ] Partial [ ] Weak

Round 4 Score: ___ / 3

---

OVERALL: ___ / 22

22-20: Interview-ready
19-16: Strong, minor polish needed
15-11: 1-2 more days of targeted study
10 or below: Return to Week 2 core topics
```

---

## Post-Interview: Top 3 Gap Identification

> **Gemini:** Based on the scorecard, identify Sean's top 3 gaps and write a 1-sentence action for each.

```
Gap 1: ___
Action: ___

Gap 2: ___
Action: ___

Gap 3: ___
Action: ___
```

---

## Week 3 Preview (If Continuing)

**If interview-ready:** Move to mock interviews with real company-specific research.
**If gaps remain:** Targeted re-study of weak areas + another mock.

**Potential Week 3 topics (not yet covered):**
- Union-Find deep dive (LC #200 variant, LC #323)
- Tries / prefix trees (LC #208, #211)
- 2D Dynamic Programming (LC #72 Edit Distance, LC #1143 LCS)
- Advanced Spark — partitioning strategies, Catalyst optimizer, AQE
- Real-time ML feature stores (Feast, Tecton concepts)
- Data mesh architecture
- Apache Flink fundamentals
- Company-specific prep (Citi, Goldman, JPMorgan data engineering interview patterns)

---

## End of Week 2

Gemini final message to Sean:
```
Week 2 complete.

14 days of structured study. You've covered:
  Algorithms: HashMap, Sliding Window, Stack, Binary Search, Heap, Intervals,
              Trees, Two Pointers, DP, Graphs, Greedy, Linked Lists
  SQL: CTEs, Window Functions, JOINs, Optimization, Analytical, Schema Design,
       PIVOT, Date/Time, GROUPING SETS, Data Quality, Trend Analysis
  Python: Generators, Pandas, Decorators, NumPy, PySpark, pytest,
          Concurrency, Pydantic, dbt
  Architecture: AWS Data Platform, Lambda/Kappa, APM, Capacity Planning,
                Airflow, Kafka, Delta Lake/Iceberg, Cost Optimization

Your differentiator is real: 10+ years APM + 6,000-server capacity planning
experience + the ability to name the framework, the tools, and the exact
SQL/Python that operationalizes it. Own that story.

What do you want to build tomorrow?
```
