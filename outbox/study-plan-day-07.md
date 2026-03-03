---
created: 2026-02-28
updated: 2026-02-28
summary: Day 7 — Full Mock Interview. Timed, scored, no hints on first attempt. Covers all 6 days of material. LeetCode + SQL + Python + System Design + Behavioral. Gemini tracks every answer.
tags: [study-plan, day-07, mock-interview, all-topics]
---

# Day 7 — Full Mock Interview

**Theme:** No more lecture. Today you are in the interview. Gemini is the interviewer.

> **Gemini Instructions:** Today is different. You are NOT a teacher. You are an interviewer.
>
> Rules for Day 7:
> - **No hints on first attempt.** If Sean asks for a hint: "I can't help during the interview."
> - **Time every answer strictly.** Start timer when you finish reading the question. Call time without exception.
> - **Do not affirm as you go.** No "good!" or "exactly!" — save all feedback for the end.
> - **After each section:** privately note Strong / Review / Weak. Do not reveal until the full debrief.
> - **At the end:** full scorecard with every question marked. Identify top 3 gaps.

---

## Interview Structure (Follow This Exactly)

```
Round 1: Technical Phone Screen Simulation     (30 min)
  → 3 coding questions (Easy, Medium, Medium)
  → 2 SQL questions
  → Timing: strict

Round 2: System Design                         (25 min)
  → One open-ended design question
  → Gemini asks follow-up probes

Round 3: Technical Deep Dive                   (20 min)
  → Python / data engineering concepts
  → Architecture trade-offs

Round 4: Behavioral                            (15 min)
  → 3 STAR stories under time pressure

Debrief                                        (10 min)
  → Full scorecard revealed
  → Top 3 gaps identified
  → Next steps
```

---

## Round 1: Technical Phone Screen (30 min)

> **Gemini:** Say this exactly: "Welcome. This is a 30-minute technical screen. I'll ask coding and SQL questions. You'll have time limits. Ready? Let's start."

---

### Coding Question 1 — Easy (5 min)

> **Gemini reads problem, starts timer immediately.**

**Problem:** Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise. Both strings contain only lowercase letters.

```
Input: s = "anagram", t = "nagaram" → true
Input: s = "rat", t = "car"         → false
```

**Time limit: 4 minutes.** Call time at 4:00.

**Expected answer (do not reveal until after):**

```python
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        count[c] = count.get(c, 0) - 1
        if count[c] < 0:
            return False
    return True
    # Or one-liner: return Counter(s) == Counter(t)
```

**Time complexity:** O(n). **Space:** O(1) (fixed 26 lowercase letters).

**Follow-up (ask immediately after answer):** "What if the strings contain Unicode characters?" *(Answer: Counter/hashmap still works — O(k) space where k = unique characters.)*

---

### Coding Question 2 — Medium (8 min)

**Problem:** You are given an array of integers `nums` and an integer `k`. Find the length of the longest subarray with sum equal to `k`.

```
Input: nums = [1, -1, 5, -2, 3], k = 3
Output: 4   (subarray [1,-1,5,-2])

Input: nums = [-2, -1, 2, 1], k = 1
Output: 2   (subarray [-1,2])
```

**Time limit: 7 minutes.** Call time at 7:00.

**Expected answer (do not reveal until after):**

```python
def maxSubArrayLen(nums: list[int], k: int) -> int:
    prefix_sum = {0: -1}   # sum → first index where this sum occurred
    total = 0
    max_len = 0

    for i, num in enumerate(nums):
        total += num
        if total - k in prefix_sum:
            max_len = max(max_len, i - prefix_sum[total - k])
        if total not in prefix_sum:     # first occurrence only
            prefix_sum[total] = i

    return max_len
```

**Key insight:** We want the longest subarray where `sum(i..j) = k`. That means `prefix[j] - prefix[i-1] = k`, so `prefix[i-1] = prefix[j] - k`. Store the FIRST occurrence of each prefix sum to maximize length.

**Follow-up:** "Why do we only store the first occurrence?" *(Answer: We want the longest subarray — earliest start index gives the longest span to the current index.)*

---

### Coding Question 3 — Medium (8 min)

**Problem:** Find the minimum number of intervals to remove to make the remaining intervals non-overlapping.

```
Input: [[1,2],[2,3],[3,4],[1,3]]
Output: 1
```

**Time limit: 7 minutes.** Call time at 7:00.

**Expected answer (do not reveal until after):**

```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[1])   # sort by end
    removals = 0
    last_end = float('-inf')

    for start, end in intervals:
        if start >= last_end:
            last_end = end
        else:
            removals += 1

    return removals
```

**Follow-up:** "What's the greedy choice here and why is it correct?" *(Answer: Always keep the interval that ends earliest — it leaves the most room for future intervals. Sorting by end time implements this greedy choice.)*

---

### SQL Question 1 (4 min)

**Problem:** Given a `monitoring_events` table with columns `(server_id, event_date, cpu_pct)`, write a query to find all servers where the average CPU usage for the past 7 days exceeded 75%, ordered by average CPU descending.

**Time limit: 3 minutes.**

**Expected answer (do not reveal until after):**

```sql
SELECT
    server_id,
    ROUND(AVG(cpu_pct), 2) AS avg_cpu
FROM monitoring_events
WHERE event_date >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY server_id
HAVING AVG(cpu_pct) > 75
ORDER BY avg_cpu DESC;
```

**Follow-up:** "How would you optimize this query for a table with 500 million rows?" *(Answer: Partition table by event_date — query only reads 7 partitions. Add index on (server_id, event_date). Consider a pre-aggregated daily summary table for repeated queries.)*

---

### SQL Question 2 (4 min)

**Problem:** Using the same table, write a query that returns — for each server — its current average CPU (last 7 days) and the average from the same 7-day window one year ago. Include the year-over-year change in percentage points.

**Time limit: 4 minutes.**

**Expected answer (do not reveal until after):**

```sql
WITH current_period AS (
    SELECT server_id, AVG(cpu_pct) AS avg_cpu_now
    FROM monitoring_events
    WHERE event_date BETWEEN CURRENT_DATE - 7 AND CURRENT_DATE
    GROUP BY server_id
),
prior_period AS (
    SELECT server_id, AVG(cpu_pct) AS avg_cpu_prior
    FROM monitoring_events
    WHERE event_date BETWEEN CURRENT_DATE - 7 - INTERVAL '1 year'
                         AND CURRENT_DATE - INTERVAL '1 year'
    GROUP BY server_id
)
SELECT
    c.server_id,
    ROUND(c.avg_cpu_now, 2)                              AS avg_cpu_now,
    ROUND(p.avg_cpu_prior, 2)                            AS avg_cpu_prior,
    ROUND(c.avg_cpu_now - COALESCE(p.avg_cpu_prior, 0), 2) AS yoy_change_pp
FROM current_period c
LEFT JOIN prior_period p ON c.server_id = p.server_id
ORDER BY yoy_change_pp DESC;
```

**Follow-up:** "Why LEFT JOIN instead of INNER JOIN?" *(Answer: Some servers may not have existed a year ago — LEFT JOIN preserves new servers. INNER JOIN would silently drop them.)*

---

## Round 2: System Design (25 min)

> **Gemini:** Say: "Let's do system design. You have 20 minutes to walk me through a design. I'll ask questions as you go. Ready?"

---

**Design Question:**

> "Design a real-time alerting system for a fleet of 10,000 monitored servers. The system must: detect when a server's CPU exceeds a threshold, alert the on-call engineer within 60 seconds, and store all events for historical analysis. Walk me through the architecture."

**Time limit: 20 minutes total.** Gemini probes during the narration.

**Probe questions (ask these as Sean speaks, one at a time):**

1. *(After Sean mentions data ingestion):* "How many messages per second are you expecting? Walk me through the math."
   - *Expected:* 10,000 servers × ~10 metrics × 1/60 = ~1,667 messages/sec. Not huge — Kafka handles this easily.

2. *(After Sean mentions alerting):* "What happens if the alerting service goes down? Does an on-call engineer miss a page?"
   - *Expected:* Kafka consumer group — another consumer picks up the partition. Alert deduplication with a Redis SET to avoid double-paging. PagerDuty itself is HA.

3. *(After Sean mentions storage):* "An analyst wants to query 3 years of data. How does your storage design handle that?"
   - *Expected:* S3 tiered — recent 90 days in Standard, older in Glacier Instant Retrieval. Athena + Glue catalog queries both tiers. Partitioned by date + region for efficient scanning.

4. "How would you handle a threshold that should fire only after 5 consecutive minutes above 90% — not on a single spike?"
   - *Expected:* Stateful stream processing — Flink or Spark Streaming with a tumbling 5-minute window + COUNT of violations. Or: sliding window aggregation in the Kafka consumer.

5. "What's the cost trade-off between Athena and Redshift for historical queries?"
   - *Expected:* Athena = $5/TB scanned, no provisioning, good for ad-hoc. Redshift = provisioned cost + faster for repeated complex queries. Redshift Spectrum bridges: query S3 via Redshift. Choose based on query frequency and complexity.

---

**Model answer framework (do NOT read — probe against Sean's answer):**

```
Ingestion:  Agents → Kafka (partitioned by server_id)
Streaming:  Flink consumer → stateful 5-min window → alert engine
Alert:      Redis (dedup) → PagerDuty / Slack / Jira
Storage:    Kafka → Kinesis Firehose → S3 (Parquet, partitioned by date/region)
Catalog:    Glue Crawler → Glue Catalog → Athena
Dashboard:  Grafana (real-time, reads Kafka/InfluxDB) + Tableau (historical, reads Athena)
```

---

## Round 3: Technical Deep Dive (20 min)

> **Gemini:** "Let's go deeper on Python and data engineering. I'll ask you questions — give me your best answer. No coding required, just explanation."

---

**Question 1 (60 sec limit):** "What is the difference between `map`, `filter`, and a list comprehension? When would you use each?"

*Expected:* `map` applies a function to each element (lazy, returns iterator). `filter` keeps elements where function returns True. List comprehension does both in one expression and is more Pythonic. Use comprehension for readability; use `map`/`filter` when chaining with `itertools` or when lazy evaluation matters for large datasets.

---

**Question 2 (90 sec limit):** "Explain the GIL in Python. How does it affect data engineering workloads?"

*Expected:* The Global Interpreter Lock prevents multiple Python threads from executing bytecode simultaneously. For CPU-bound tasks (data processing), threads don't give true parallelism — use `multiprocessing` or NumPy/Pandas (which release the GIL for C-level operations). For I/O-bound tasks (API calls, file reads), threading works fine. PySpark avoids this entirely — it runs on the JVM.

---

**Question 3 (90 sec limit):** "What is the difference between `repartition` and `coalesce` in Spark? When would you use each?"

*Expected:* `repartition(n)` = full shuffle, evenly redistributes data, can increase or decrease partition count. `coalesce(n)` = no shuffle, combines adjacent partitions, can only decrease. Use `repartition` when data is skewed or you need even distribution (before a join). Use `coalesce` before writing to reduce the number of output files (avoids thousands of tiny files in S3).

---

**Question 4 (2 min limit):** "Walk me through how you would debug a slow Spark job."

*Expected (structured answer):*
1. Check the Spark UI — look at stage timeline for skew (one task much longer than others)
2. Check shuffle read/write — large shuffle = expensive join or groupBy without partition optimization
3. Check for data skew — one partition has 10x more data → use salting or broadcast the small table
4. Check for Python UDFs — replace with built-in functions
5. Check `shuffle.partitions` — too many small partitions or too few large ones
6. Check storage format — is it reading CSV (slow) instead of Parquet (fast + columnar)?

---

**Question 5 (90 sec limit):** "What is idempotency and why does it matter in ETL?"

*Expected:* An operation is idempotent if running it multiple times has the same result as running it once. In ETL: if a pipeline fails halfway and re-runs, does it load duplicate data? Solutions: UPSERT (INSERT ON CONFLICT UPDATE) for database loads, partition overwrite for S3/Parquet (`mode("overwrite")` on a partition), watermark tables to skip already-processed dates. Idempotency is required for safe retries — Airflow retries failed tasks automatically.

---

**Question 6 (90 sec limit):** "Explain the difference between SCD Type 1 and SCD Type 2."

*Expected:* Type 1 = overwrite the existing record (no history preserved). Type 2 = add a new row for each change, with `valid_from`, `valid_to`, and `is_current` flag. Type 2 is used when historical accuracy matters — e.g., "what team owned this server at the time of this alert?" Type 1 is fine for non-critical attributes like contact phone number.

---

## Round 4: Behavioral (15 min)

> **Gemini:** "Last section. Three behavioral questions. Two minutes each. I'll time you. Ready?"

---

**Question 1 — Scale:**
> "Tell me about a time you had to handle a significant increase in scale or data volume. How did you approach it?"

*(Sean's story: Citi 6,000 endpoints monitoring scale-up. STAR format. 2 min limit.)*

After Sean answers: "Strong" or "You need more [Situation / Task / Action / Result]. Specifically: [what was thin]."

---

**Question 2 — Problem Solving:**
> "Describe a situation where you discovered a significant technical problem. How did you identify it and what did you do?"

*(Sean's story: Data gap detection using anti-joins. Or: alert fatigue problem solved with trend-based alerting. 2 min limit.)*

After Sean answers: give feedback.

---

**Question 3 — Cross-functional:**
> "Tell me about a time you had to explain a complex technical concept to a non-technical stakeholder. What was your approach?"

*(Sean's story: Capacity forecast presented to management — translating 'CPU at 67%' to 'we need servers by [date] or face outage.' 2 min limit.)*

After Sean answers: give feedback.

---

## Debrief — Full Scorecard

> **Gemini:** "Interview complete. Here is your full scorecard."

```
═══════════════════════════════════════════════════════
DAY 7 MOCK INTERVIEW SCORECARD
═══════════════════════════════════════════════════════

ROUND 1: PHONE SCREEN
─────────────────────────────────────────────────────
[ ] Coding Q1 — Valid Anagram          Strong / Review / Weak
[ ] Coding Q2 — Longest Subarray Sum K Strong / Review / Weak
[ ] Coding Q3 — Non-overlapping Intervals Strong / Review / Weak
[ ] SQL Q1 — 7-day average filter      Strong / Review / Weak
[ ] SQL Q2 — YoY change query          Strong / Review / Weak

ROUND 2: SYSTEM DESIGN
─────────────────────────────────────────────────────
[ ] Architecture narration             Strong / Review / Weak
[ ] Math: messages/sec                 Strong / Review / Weak
[ ] Fault tolerance                    Strong / Review / Weak
[ ] Stateful alerting (5-min window)   Strong / Review / Weak
[ ] Athena vs. Redshift trade-off      Strong / Review / Weak

ROUND 3: TECHNICAL DEEP DIVE
─────────────────────────────────────────────────────
[ ] map / filter / comprehension       Strong / Review / Weak
[ ] GIL and parallelism                Strong / Review / Weak
[ ] repartition vs coalesce            Strong / Review / Weak
[ ] Debugging a slow Spark job         Strong / Review / Weak
[ ] Idempotency in ETL                 Strong / Review / Weak
[ ] SCD Type 1 vs. Type 2             Strong / Review / Weak

ROUND 4: BEHAVIORAL
─────────────────────────────────────────────────────
[ ] Scale story (STAR)                 Strong / Review / Weak
[ ] Problem solving story (STAR)       Strong / Review / Weak
[ ] Cross-functional story (STAR)      Strong / Review / Weak

OVERALL
─────────────────────────────────────────────────────
Strong:  [count]
Review:  [count]
Weak:    [count]

TOP 3 GAPS (Gemini fills this in):
1.
2.
3.

INTERVIEW READINESS: [ ] Ready  [ ] 1-2 more days  [ ] Needs significant work
═══════════════════════════════════════════════════════
```

---

## Post-Debrief Instructions for Gemini

**After the scorecard:**

1. Tell Sean his top 3 gaps explicitly.
2. If any WEAK items remain: "These need Claude Code — I'll flag them for reinforcement."
3. Ask: "What do you want to capture from this week? I'll add it to the vault."
4. Update `/log/study-progress.md` with the Day 7 entry.
5. Tell Sean: "This is your baseline. When you get the actual interview date, we drill the top gaps every day until then."

**Log entry format:**

```markdown
## Day 7 — YYYY-MM-DD — Mock Interview
Strong: [list all Strong items]
Review: [list all Review items]
Weak: [list all Weak items]
Top 3 gaps: [1], [2], [3]
Behavioral: [story 1 — Strong/Needs work], [story 2], [story 3]
Interview readiness: [Ready / 1-2 more days / Needs significant work]
```

---

## Week Complete

> **Gemini final message to Sean:**
>
> "Seven days done. You covered HashMap, Sliding Window, Stack, Binary Search, Heap, Intervals — the core LeetCode patterns. SQL from CTEs to cohort analysis. Python from generators to PySpark. And the system design you built at Citi.
>
> The goal was never to memorize — it was to build the reflex to recognize patterns and narrate solutions confidently. Check your scorecard. The gaps are the work that's left.
>
> Tell me what you want to drill next."
