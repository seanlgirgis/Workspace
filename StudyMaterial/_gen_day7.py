"""
Day 7 generator:
  1. day-07-mock-interview.ipynb  — Gemini's interviewer guide (full questions + expected answers)
  2. day-07-prep-cheatsheet.html  — Sean's pre-interview quick reference (all 6 days condensed)
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/Workspace/StudyMaterial/Day7'
os.makedirs(BASE, exist_ok=True)


# ─────────────────────────────────────────────────────────────────────────────
# helpers
# ─────────────────────────────────────────────────────────────────────────────

def nb(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "cells": cells
    }

def md(cid, text):
    lines = text.split('\n')
    src = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    return {"cell_type": "markdown", "id": cid, "metadata": {}, "source": src}

def code(cid, text):
    lines = text.split('\n')
    src = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    return {"cell_type": "code", "id": cid, "metadata": {}, "outputs": [], "execution_count": None, "source": src}

def write_nb(path, cells):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb(cells), f, indent=1, ensure_ascii=False)
    print(f'  Written: {path}')


# ─────────────────────────────────────────────────────────────────────────────
# FILE 1: Interviewer guide notebook
# ─────────────────────────────────────────────────────────────────────────────

INTERVIEW_NB = [

md('c00', '''# Day 7 — Full Mock Interview
## Gemini Interviewer Guide

<div style="padding:15px;border-left:8px solid #e53935;background:#ffebee;border-radius:4px;">
<strong>Gemini: You are the INTERVIEWER today, not the teacher.</strong><br>
Rules: No hints on first attempt. Time every answer strictly. No affirmations ("good!", "exactly!").
Save all feedback for the debrief. Mark Strong / Review / Weak privately as you go.
</div>

---

## Interview Structure

| Round | Topic | Time |
|-------|-------|------|
| Round 1 | Technical Phone Screen (3 coding + 2 SQL) | 30 min |
| Round 2 | System Design | 25 min |
| Round 3 | Technical Deep Dive (Python + Data Engineering) | 20 min |
| Round 4 | Behavioral (3 STAR stories) | 15 min |
| Debrief | Full scorecard + top 3 gaps | 10 min |

**Total: ~100 minutes**

---

**Say this to start:**
> "Welcome. Today is your full mock interview. We'll do four rounds — coding, system design, technical deep dive, and behavioral. I'll time each question strictly. Ready? Let's begin."'''),

md('c01', '''## Round 1: Technical Phone Screen (30 min)

> **Say:** "This is a 30-minute technical screen. I'll ask coding and SQL questions. You'll have time limits. Ready? Let's start."

---

### Coding Q1 — Valid Anagram [Easy] — 4 min

**Read to Sean:**
> "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`. Both strings contain only lowercase letters.
> Input: s = "anagram", t = "nagaram" → true | Input: s = "rat", t = "car" → false.
> You have 4 minutes. Go."

**Start timer. Call time at 4:00 without exception.**

---

**Expected answer** *(do NOT reveal until Sean has answered):*

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
    # One-liner: return Counter(s) == Counter(t)
```

**Complexity:** O(n) time, O(1) space (26 lowercase letters).

**Follow-up** *(ask immediately after answer):*
> "What if the strings contain Unicode characters?"
Expected: Counter/hashmap still works — O(k) space where k = unique chars.

**Score privately: Strong / Review / Weak**

---

### Coding Q2 — Longest Subarray Sum K [Medium] — 7 min

**Read to Sean:**
> "Given array `nums` and integer `k`, find the length of the longest subarray with sum equal to `k`.
> Input: [1, -1, 5, -2, 3], k=3 → 4 (subarray [1,-1,5,-2])
> Input: [-2, -1, 2, 1], k=1 → 2
> You have 7 minutes. Go."

---

**Expected answer:**

```python
def maxSubArrayLen(nums: list[int], k: int) -> int:
    prefix_sum = {0: -1}   # sum → first index where this sum occurred
    total = 0
    max_len = 0

    for i, num in enumerate(nums):
        total += num
        if total - k in prefix_sum:
            max_len = max(max_len, i - prefix_sum[total - k])
        if total not in prefix_sum:     # first occurrence only — maximizes length
            prefix_sum[total] = i

    return max_len
```

**Key insight:** `prefix[j] - prefix[i-1] = k` → store FIRST occurrence to maximize subarray length.

**Follow-up:** "Why only store the first occurrence of each prefix sum?"
Expected: We want the longest subarray — earliest start index gives the longest span to current index.

**Score privately: Strong / Review / Weak**

---

### Coding Q3 — Non-overlapping Intervals [Medium] — 7 min

**Read to Sean:**
> "Find the minimum number of intervals to remove to make the remaining non-overlapping.
> Input: [[1,2],[2,3],[3,4],[1,3]] → Output: 1
> You have 7 minutes. Go."

---

**Expected answer:**

```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda x: x[1])   # sort by end time
    removals = 0
    last_end = float('-inf')

    for start, end in intervals:
        if start >= last_end:
            last_end = end     # no overlap — keep this interval
        else:
            removals += 1      # overlap — remove this interval

    return removals
```

**Follow-up:** "What's the greedy choice and why is it correct?"
Expected: Always keep the interval ending earliest — leaves maximum room for future intervals.

**Score privately: Strong / Review / Weak**'''),

md('c02', '''### SQL Q1 — 7-day Average Filter — 3 min

**Read to Sean:**
> "Table `monitoring_events` has columns `(server_id, event_date, cpu_pct)`.
> Find all servers where the average CPU for the past 7 days exceeded 75%, ordered by average CPU descending.
> You have 3 minutes. Go."

---

**Expected answer:**

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

**Follow-up:** "How do you optimize this for a 500M row table?"
Expected: Partition by event_date (only reads 7 partitions), composite index on (server_id, event_date), pre-aggregated daily summary table for repeated queries.

**Score privately: Strong / Review / Weak**

---

### SQL Q2 — YoY Change Query — 4 min

**Read to Sean:**
> "Same table. For each server, show its current 7-day average CPU AND the average from the same 7-day window one year ago. Include the year-over-year change in percentage points.
> You have 4 minutes. Go."

---

**Expected answer:**

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
    ROUND(c.avg_cpu_now, 2)                                     AS avg_cpu_now,
    ROUND(p.avg_cpu_prior, 2)                                   AS avg_cpu_prior,
    ROUND(c.avg_cpu_now - COALESCE(p.avg_cpu_prior, 0), 2)     AS yoy_change_pp
FROM current_period c
LEFT JOIN prior_period p ON c.server_id = p.server_id
ORDER BY yoy_change_pp DESC;
```

**Follow-up:** "Why LEFT JOIN, not INNER JOIN?"
Expected: New servers didn't exist a year ago — INNER JOIN would silently drop them. LEFT JOIN preserves all current servers.

**Score privately: Strong / Review / Weak**

---

> **End of Round 1. Say:** "Round 1 complete. Take 2 minutes. Then we do system design."'''),

md('c03', '''## Round 2: System Design (25 min)

> **Say:** "Let's do system design. You have 20 minutes to walk me through a design. I'll ask questions as you go. Ready?"

---

**Read this question:**
> "Design a real-time alerting system for a fleet of 10,000 monitored servers.
> Requirements:
> - Detect when a server's CPU exceeds a threshold
> - Alert the on-call engineer within 60 seconds
> - Store all events for historical analysis
> Walk me through the architecture. You have 20 minutes."

---

### Probe Questions (ask one at a time as Sean speaks — don't wait until the end)

**Probe 1** *(after ingestion):*
> "How many messages per second are you expecting? Walk me through the math."
Expected: 10,000 servers × ~10 metrics × 1/60 sec ≈ 1,667 msg/sec. Kafka handles this easily with a single partition set.

**Probe 2** *(after alerting):*
> "What happens if the alerting service goes down? Does the on-call engineer miss a page?"
Expected: Kafka consumer group — another consumer takes over the partition. Alert deduplication with Redis SET (avoid double-paging). PagerDuty itself is HA.

**Probe 3** *(after storage):*
> "An analyst wants to query 3 years of data. How does your storage handle that?"
Expected: S3 tiered — 90 days Standard, older in Glacier Instant Retrieval. Athena + Glue catalog queries both tiers. Partitioned by date + region.

**Probe 4** *(any time):*
> "How do you handle a threshold that fires only after 5 consecutive minutes above 90% — not on a single spike?"
Expected: Stateful stream processing — Flink or Spark Streaming with a tumbling 5-minute window. Or: sliding window aggregation in the Kafka consumer.

**Probe 5** *(near the end):*
> "What's the cost trade-off between Athena and Redshift for historical queries?"
Expected: Athena = $5/TB scanned, serverless, good for ad-hoc. Redshift = provisioned, faster for complex repeated BI. Redshift Spectrum bridges both. Choose by query frequency × cost vs cluster cost.

---

### Model Architecture (probe against this — don't read it)

```
Agents → Kafka (partitioned by server_id)
       ↓
Flink  → stateful 5-min window → alert engine → Redis dedup → PagerDuty/Slack
       ↓
Kinesis Firehose → S3 Parquet (partitioned by date/region)
                 → Glue Catalog → Athena (ad-hoc) + Grafana (dashboards)
```

**Score each probe: Strong / Review / Weak**

> **End Round 2. Say:** "Round 2 complete. Short break. Then technical deep dive."'''),

md('c04', '''## Round 3: Technical Deep Dive (20 min)

> **Say:** "Let's go deeper on Python and data engineering. Verbal answers only — no coding. I'll time each question. Ready?"

---

**Q1 — 60 sec:** "What is the difference between `map`, `filter`, and a list comprehension? When would you use each?"

Expected: `map` applies a function to each element (lazy iterator). `filter` keeps elements where function is True. List comprehension does both in one expression and is more Pythonic. Use comprehension for readability; use `map`/`filter` when chaining with itertools or when lazy evaluation matters for large datasets.

**Score: Strong / Review / Weak**

---

**Q2 — 90 sec:** "Explain the GIL in Python. How does it affect data engineering workloads?"

Expected: Global Interpreter Lock prevents multiple Python threads from executing bytecode simultaneously. For CPU-bound tasks: threads don't give true parallelism — use `multiprocessing` or NumPy/pandas (which release the GIL for C-level ops). For I/O-bound tasks: threading works fine. PySpark avoids this — runs on the JVM.

**Score: Strong / Review / Weak**

---

**Q3 — 90 sec:** "What is the difference between `repartition` and `coalesce` in Spark?"

Expected: `repartition(n)` = full shuffle, evenly redistributes data, can increase OR decrease partition count. `coalesce(n)` = no shuffle, combines adjacent partitions, can only DECREASE. Use `repartition` when data is skewed (before a join). Use `coalesce` before writing to reduce output files (avoids thousands of tiny files in S3).

**Score: Strong / Review / Weak**

---

**Q4 — 2 min:** "Walk me through how you would debug a slow Spark job."

Expected structured answer:
1. Check Spark UI — find the red/slow stage
2. Check shuffle read/write size — large shuffle = expensive join or groupBy
3. Check for data skew — one task much longer than others → salting or broadcast join
4. Check for Python UDFs — replace with built-in F. functions
5. Check `spark.sql.shuffle.partitions` — too many small or too few large partitions
6. Check storage format — CSV vs Parquet (Parquet = columnar, 10x faster reads)

**Score: Strong / Review / Weak**

---

**Q5 — 90 sec:** "What is idempotency and why does it matter in ETL?"

Expected: An idempotent operation produces the same result when run multiple times. In ETL: if a pipeline fails and re-runs, does it insert duplicate data? Solutions: UPSERT (INSERT ON CONFLICT), partition overwrite on S3 (mode "overwrite"), watermark tables to skip processed dates. Required for safe Airflow retries.

**Score: Strong / Review / Weak**

---

**Q6 — 90 sec:** "Explain the difference between SCD Type 1 and SCD Type 2."

Expected: Type 1 = overwrite the existing record (no history). Type 2 = add a new row per change with `effective_date`, `expiry_date`, `is_current`. Type 2 is used when historical accuracy matters — "which team owned this server at the time of this alert?" Type 1 is fine for non-critical attributes (phone numbers, contact email).

**Score: Strong / Review / Weak**

> **End Round 3. Say:** "Round 3 complete. Last round — behavioral. Two minutes each."'''),

md('c05', '''## Round 4: Behavioral (15 min)

> **Say:** "Three behavioral questions. Two minutes each. STAR format — Situation, Task, Action, Result. I'll time you. Ready?"

---

**Q1 — Scale story (2 min):**
> "Tell me about a time you had to handle a significant increase in scale or data volume. How did you approach it?"

*(Sean's story: Citi 6,000 endpoints monitoring. NumPy vectorization — 180s → 1.2s. Or: pandas → PySpark migration.)*

After answer: "Strong" OR "You need more [Situation / Task / Action / Result]. Specifically: ..."

**Score: Strong / Review / Weak**

---

**Q2 — Problem solving (2 min):**
> "Describe a situation where you discovered a significant technical problem. How did you identify it and what did you do?"

*(Sean's story: Alert fatigue — 400 alerts/day, 70% false positives. Redesigned to trend-based alerting using 14-day rolling baseline. OR: data gap detected with anti-join.)*

After answer: give feedback.

**Score: Strong / Review / Weak**

---

**Q3 — Cross-functional (2 min):**
> "Tell me about a time you had to explain a complex technical concept to a non-technical stakeholder."

*(Sean's story: Capacity forecast to management — translating "CPU at 67% with slope +0.8%/day" to "we need servers by March 15th or face downtime during trading hours.")*

After answer: give feedback.

**Score: Strong / Review / Weak**

---

> **Say:** "Round 4 complete. Give me a moment to compile your scorecard."'''),

md('c06', '''## Debrief — Full Scorecard

> **Say:** "Interview complete. Here is your full scorecard."

```
═══════════════════════════════════════════════════════════════
DAY 7 MOCK INTERVIEW SCORECARD
Date: ____________    Gemini reviewer: Antigravity
═══════════════════════════════════════════════════════════════

ROUND 1: PHONE SCREEN
────────────────────────────────────────────────────────────
[ ] Coding Q1 — Valid Anagram                Strong / Review / Weak
[ ] Coding Q2 — Longest Subarray Sum K       Strong / Review / Weak
[ ] Coding Q3 — Non-overlapping Intervals    Strong / Review / Weak
[ ] SQL Q1    — 7-day average filter         Strong / Review / Weak
[ ] SQL Q2    — YoY change query             Strong / Review / Weak

ROUND 2: SYSTEM DESIGN
────────────────────────────────────────────────────────────
[ ] Architecture narration (Kafka→Flink→S3→Athena)  Strong / Review / Weak
[ ] Math: messages/sec calculation                   Strong / Review / Weak
[ ] Fault tolerance (consumer failover, dedup)       Strong / Review / Weak
[ ] Stateful alerting (5-min window)                 Strong / Review / Weak
[ ] Athena vs. Redshift trade-off                    Strong / Review / Weak

ROUND 3: TECHNICAL DEEP DIVE
────────────────────────────────────────────────────────────
[ ] map / filter / comprehension             Strong / Review / Weak
[ ] GIL and parallelism                      Strong / Review / Weak
[ ] repartition vs coalesce                  Strong / Review / Weak
[ ] Debugging a slow Spark job               Strong / Review / Weak
[ ] Idempotency in ETL                       Strong / Review / Weak
[ ] SCD Type 1 vs. Type 2                   Strong / Review / Weak

ROUND 4: BEHAVIORAL
────────────────────────────────────────────────────────────
[ ] Scale story (STAR format)                Strong / Review / Weak
[ ] Problem solving story (STAR format)      Strong / Review / Weak
[ ] Cross-functional story (STAR format)     Strong / Review / Weak

OVERALL
────────────────────────────────────────────────────────────
Strong:  ____    Review:  ____    Weak:  ____

TOP 3 GAPS (fill these in):
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

INTERVIEW READINESS:
[ ] Ready — book the interview
[ ] 1-2 more days — drill the gaps
[ ] Needs significant work — revisit weak areas first
═══════════════════════════════════════════════════════════════
```

---

## Post-Debrief Instructions

1. Tell Sean his top 3 gaps explicitly by name.
2. If any WEAK items: *"These need Claude Code — I'll flag them for reinforcement."*
3. Ask: *"What do you want to capture from this week? I'll add it to the vault."*
4. Update `/log/study-progress.md` with the Day 7 entry.
5. Tell Sean: *"This is your baseline. When you get the interview date, we drill the top gaps every day until then."*

---

**Log entry format for study-progress.md:**
```markdown
## Day 7 — YYYY-MM-DD — Mock Interview
Strong: [list]
Review: [list]
Weak: [list]
Top 3 gaps: [1], [2], [3]
Behavioral: Scale [S/R/W] | Problem [S/R/W] | Cross-functional [S/R/W]
Readiness: [Ready / 1-2 more days / Needs work]
```

---

## Gemini's Closing Message to Sean

> "Seven days done. You covered HashMap, Sliding Window, Stack, Binary Search, Heap, Intervals —
> the core LeetCode patterns. SQL from CTEs to cohort analysis. Python from generators to PySpark.
> And the system design you built at Citi.
>
> The goal was never to memorize — it was to build the reflex to recognize patterns and narrate
> solutions confidently. Check your scorecard. The gaps are the work that's left.
>
> Tell me what you want to drill next."'''),

]

write_nb(f'{BASE}/day-07-mock-interview.ipynb', INTERVIEW_NB)


# ─────────────────────────────────────────────────────────────────────────────
# FILE 2: Pre-interview cheat sheet HTML
# ─────────────────────────────────────────────────────────────────────────────

CHEAT_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Day 7 — Interview Prep Cheat Sheet</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  min-height: 100vh; padding: 30px 20px; color: #e0e0e0;
}
.container { max-width: 1200px; margin: 0 auto; }
h1 { color: white; text-align: center; font-size: 2em; font-weight: 300;
     letter-spacing: -1px; margin-bottom: 6px; }
.subtitle { color: rgba(255,255,255,0.7); text-align: center; margin-bottom: 30px; font-size: 0.95em; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 20px; }
@media(max-width:900px) { .grid,.grid3 { grid-template-columns: 1fr; } }
.card {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px; padding: 20px;
  backdrop-filter: blur(10px);
}
.card h2 { font-size: 1em; font-weight: 600; margin-bottom: 14px;
           text-transform: uppercase; letter-spacing: 1px; }
.card.red h2    { color: #ff6b6b; border-bottom: 2px solid #ff6b6b; padding-bottom: 8px; }
.card.blue h2   { color: #74b9ff; border-bottom: 2px solid #74b9ff; padding-bottom: 8px; }
.card.green h2  { color: #55efc4; border-bottom: 2px solid #55efc4; padding-bottom: 8px; }
.card.yellow h2 { color: #fdcb6e; border-bottom: 2px solid #fdcb6e; padding-bottom: 8px; }
.card.purple h2 { color: #a29bfe; border-bottom: 2px solid #a29bfe; padding-bottom: 8px; }
.card.orange h2 { color: #fd79a8; border-bottom: 2px solid #fd79a8; padding-bottom: 8px; }
.card.teal h2   { color: #81ecec; border-bottom: 2px solid #81ecec; padding-bottom: 8px; }
pre {
  background: rgba(0,0,0,0.4); border-radius: 6px;
  padding: 10px 12px; font-size: 0.78em; line-height: 1.5;
  overflow-x: auto; color: #dfe6e9; margin: 8px 0;
  border-left: 3px solid rgba(255,255,255,0.15);
}
.tip { background: rgba(255,255,255,0.07); border-radius: 5px;
       padding: 8px 10px; margin: 6px 0; font-size: 0.82em;
       line-height: 1.6; color: #dfe6e9; }
.tip strong { color: #fdcb6e; }
.tip .label { font-weight: 700; font-size: 0.75em; text-transform: uppercase;
              letter-spacing: 0.5px; margin-bottom: 3px; display: block; }
.label.red    { color: #ff6b6b; }
.label.blue   { color: #74b9ff; }
.label.green  { color: #55efc4; }
.label.yellow { color: #fdcb6e; }
.label.purple { color: #a29bfe; }
table { width: 100%; border-collapse: collapse; font-size: 0.8em; margin-top: 8px; }
th { color: rgba(255,255,255,0.5); font-weight: 600; text-align: left;
     padding: 5px 8px; font-size: 0.75em; text-transform: uppercase; letter-spacing: 0.5px; }
td { padding: 5px 8px; border-top: 1px solid rgba(255,255,255,0.07); color: #b2bec3; vertical-align: top; }
td strong { color: #dfe6e9; }
.full { grid-column: 1 / -1; }
</style>
</head>
<body>
<div class="container">

<h1>Day 7 — Interview Prep Cheat Sheet</h1>
<p class="subtitle">All 6 days condensed &nbsp;|&nbsp; Read once before the mock interview &nbsp;|&nbsp; Then close it and perform</p>


<!-- ── Row 1: LeetCode Patterns ─────────────────────────────────────────── -->
<div class="grid3">

<div class="card red">
<h2>📊 Pattern Recognition</h2>
<div class="tip"><span class="label red">HashMap / Array</span>Complement lookup, frequency count, prefix sum</div>
<div class="tip"><span class="label blue">Sliding Window</span>Contiguous subarray with a constraint — expand right, shrink left when violated</div>
<div class="tip"><span class="label green">Stack</span>Monotonic stack for "next greater element", matching brackets</div>
<div class="tip"><span class="label yellow">Binary Search</span>Sorted array → halve search space. Template: <code>left <= right</code>, <code>mid = left + (right-left)//2</code></div>
<div class="tip"><span class="label purple">Heap</span>Top K → min-heap of size K. <code>heapq</code> is min-heap. Negate for max.</div>
<div class="tip"><span class="label red">Intervals</span>Sort by start (merge) or by end (greedy remove). Track <code>last_end</code>.</div>
</div>

<div class="card blue">
<h2>⚡ Complexity Cheat</h2>
<table>
<tr><th>Pattern</th><th>Time</th><th>Space</th></tr>
<tr><td><strong>HashMap lookup</strong></td><td>O(1) avg</td><td>O(n)</td></tr>
<tr><td><strong>Sliding window</strong></td><td>O(n)</td><td>O(1)–O(k)</td></tr>
<tr><td><strong>Monotonic stack</strong></td><td>O(n)</td><td>O(n)</td></tr>
<tr><td><strong>Binary search</strong></td><td>O(log n)</td><td>O(1)</td></tr>
<tr><td><strong>Heap push/pop</strong></td><td>O(log k)</td><td>O(k)</td></tr>
<tr><td><strong>Sort</strong></td><td>O(n log n)</td><td>O(1)–O(n)</td></tr>
<tr><td><strong>Prefix sum build</strong></td><td>O(n)</td><td>O(n)</td></tr>
<tr><td><strong>Interval merge</strong></td><td>O(n log n)</td><td>O(n)</td></tr>
</table>
</div>

<div class="card green">
<h2>🐍 Python Gotchas</h2>
<div class="tip"><span class="label green">Binary search midpoint</span><code>mid = left + (right - left) // 2</code> — overflow-safe (matters in C/Java)</div>
<div class="tip"><span class="label green">Heap in Python</span><code>heapq</code> = min-heap. For max-heap: push <code>-val</code>. For tuples: push <code>(priority, val)</code></div>
<div class="tip"><span class="label green">Counter</span><code>from collections import Counter; Counter(s) == Counter(t)</code> — anagram in one line</div>
<div class="tip"><span class="label green">defaultdict</span><code>from collections import defaultdict; d = defaultdict(list)</code> — no KeyError</div>
<div class="tip"><span class="label green">Prefix sum pattern</span><code>prefix = {0: -1}</code> → initialize before loop for edge case (subarray from index 0)</div>
<div class="tip"><span class="label green">Interval sort</span>Sort by start: <code>intervals.sort()</code>. By end: <code>.sort(key=lambda x: x[1])</code></div>
</div>

</div>


<!-- ── Row 2: SQL + System Design ─────────────────────────────────────────── -->
<div class="grid">

<div class="card yellow">
<h2>🗄️ SQL Analytical Patterns</h2>
<div class="tip"><span class="label yellow">YoY Growth</span>
<pre>LAG(revenue, 12) OVER (ORDER BY yr, mo)
-- or self-join on same month, prior year</pre></div>
<div class="tip"><span class="label yellow">7-day Rolling Avg</span>
<pre>AVG(cpu) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)</pre></div>
<div class="tip"><span class="label yellow">Top N per group</span>
<pre>RANK() OVER (PARTITION BY env ORDER BY cpu DESC) AS rk
WHERE rk &lt;= 3</pre></div>
<div class="tip"><span class="label yellow">Funnel / conditional agg</span>
<pre>COUNT(DISTINCT CASE WHEN event = 'view' THEN user_id END) AS views</pre></div>
<div class="tip"><span class="label yellow">SCD Type 2 point-in-time</span>
<pre>WHERE effective_date &lt;= :incident_date
  AND (expiry_date IS NULL OR expiry_date &gt;= :incident_date)</pre></div>
<div class="tip"><span class="label yellow">Optimization</span>Composite index (most selective col first) · Partition pruning · EXPLAIN ANALYZE · ANALYZE for stats</div>
</div>

<div class="card purple">
<h2>🏗️ System Design: Data Platform</h2>
<pre>APM Agents → Kafka → Flink (real-time alert &lt;60s)
                   ↘ Spark ETL → S3 Parquet
                                 → Glue Catalog
                                 → Athena (ad-hoc)
                                 → Grafana</pre>
<div class="tip"><span class="label purple">Kafka vs Direct S3</span>Kafka = replay buffer. If consumer fails → restart from offset. Direct S3 = no replay.</div>
<div class="tip"><span class="label purple">Athena vs Redshift</span>Athena = serverless $5/TB, good for ad-hoc. Redshift = provisioned, faster for repeated BI. Rule: query_freq × cost vs cluster_cost/month</div>
<div class="tip"><span class="label purple">Partitioning</span><code>date=YYYY-MM-DD/env=prod/</code> → monthly queries scan 30 of 365 partitions = 10x cost saving</div>
<div class="tip"><span class="label purple">Messages/sec math</span>10K servers × 10 metrics × 1/60 = ~1,667 msg/sec. Kafka: easy.</div>
<div class="tip"><span class="label purple">Stateful alerting</span>5-min window → Flink tumbling window or Kafka Streams KTable with time-based eviction</div>
<div class="tip"><span class="label purple">Fault tolerance</span>Consumer group → partition rebalance. Redis SET for dedup. PagerDuty HA.</div>
</div>

</div>


<!-- ── Row 3: Python DE + Citi Stories ───────────────────────────────────── -->
<div class="grid">

<div class="card orange">
<h2>⚙️ Python Data Engineering</h2>
<div class="tip"><span class="label red">GIL</span>CPU-bound → multiprocessing (not threads). I/O-bound → threading OK. NumPy releases GIL for C ops. PySpark = JVM (no GIL).</div>
<div class="tip"><span class="label red">map vs comprehension</span>map = lazy iterator. List comp = eager + more readable. Use map only when chaining with itertools or lazy eval matters.</div>
<div class="tip"><span class="label red">repartition vs coalesce</span>repartition(n) = full shuffle, can increase. coalesce(n) = no shuffle, can only decrease. Use coalesce before .write() to reduce S3 file count.</div>
<div class="tip"><span class="label red">PySpark UDF anti-pattern</span>Python UDF = JVM→Python serialization per row = 10x slower. Replace with <code>F.when().otherwise()</code>. Citi: 45 min → 4 min.</div>
<div class="tip"><span class="label red">Debug slow Spark job</span>1) Spark UI → find red stage · 2) shuffle size · 3) data skew · 4) Python UDFs · 5) shuffle.partitions · 6) CSV vs Parquet</div>
<div class="tip"><span class="label red">Idempotency</span>DELETE+INSERT per date partition, or UPSERT (ON CONFLICT), or S3 partition overwrite. Required for Airflow retry safety.</div>
<div class="tip"><span class="label red">ETL template</span>argparse → setup_logging → try: extract/transform/load → except: log + sys.exit(1)</div>
</div>

<div class="card teal">
<h2>💼 Citi Narratives (Own These)</h2>
<div class="tip"><span class="label green">Alert Fatigue → Trend-Based</span>400 alerts/day, 70% false positive. Built 14-day rolling baseline in SQL. Changed to deviation-based alerts. Result: 70% reduction, caught more real incidents.</div>
<div class="tip"><span class="label green">NumPy Vectorization</span>6M-cell capacity matrix (6K servers × 1K timestamps). Python loop: 180s. NumPy: 1.2s. 150x speedup. No algorithm change.</div>
<div class="tip"><span class="label green">Capacity Planning Win</span>4-step loop: baseline 90-day APM → linear trend → 70% ceiling alert → Jira at &lt;35 days. First catch: 47 days lead time. Zero capacity outages in 12 months.</div>
<div class="tip"><span class="label green">PySpark UDF Removal</span>45 min → 4 min. Spark UI showed UDF as red stage. Replaced with F.when chain. Same result, no serialization overhead.</div>
<div class="tip"><span class="label green">SQL Index Fix</span>fact_monitoring 500M rows, 45s query. EXPLAIN ANALYZE: Seq Scan + stale stats. Fix: composite index + ANALYZE + partition pruning. Result: 0.3s.</div>
<div class="tip"><span class="label green">SCD Type 2</span>Servers moved teams during restructures. Incident attribution was wrong. SCD Type 2: point-in-time ownership queries. Fixed 12% of incident attributions.</div>
<div class="tip"><span class="label green">Data Platform</span>4 APM tools → 1 platform. Kafka → Spark → S3 → Glue → Athena. Monthly report: 2 analyst-days → 2 hours.</div>
</div>

</div>


<!-- ── Row 4: STAR format + Interview mindset ─────────────────────────────── -->
<div class="grid">

<div class="card red">
<h2>🌟 STAR Behavioral Framework</h2>
<table>
<tr><th>Element</th><th>What to cover</th><th>Time</th></tr>
<tr><td><strong>Situation</strong></td><td>Context — what was the environment, the team, the scale?</td><td>15s</td></tr>
<tr><td><strong>Task</strong></td><td>Your specific responsibility — what were YOU asked to solve?</td><td>15s</td></tr>
<tr><td><strong>Action</strong></td><td>What YOU specifically did — tools, decisions, trade-offs</td><td>60s</td></tr>
<tr><td><strong>Result</strong></td><td>Quantified outcome — time saved, error reduction, revenue, reliability</td><td>30s</td></tr>
</table>
<div class="tip" style="margin-top:10px;"><strong>Common failure:</strong> Too much Situation, too little Action. The interviewer wants to know what YOU did, not what the team did. Use "I" not "we" for actions.</div>
<div class="tip"><strong>The number rule:</strong> Every story needs at least one number. "Alert volume dropped 70%." "Query time went from 45 seconds to 0.3 seconds." "Zero capacity outages."</div>
</div>

<div class="card blue">
<h2>🧠 Interview Mindset Checklist</h2>
<div class="tip"><strong>Coding:</strong> Say the pattern name FIRST. "This is a prefix sum problem." Then code. Don't code first and explain later.</div>
<div class="tip"><strong>Complexity:</strong> Always state time AND space before the interviewer asks. "O(n) time, O(1) space because we use a fixed-size counter."</div>
<div class="tip"><strong>SQL:</strong> Write the WHERE before the HAVING. Filter early. Use CTEs for readability — not subqueries nested 3 levels deep.</div>
<div class="tip"><strong>System design:</strong> Start with requirements. State them back. "10K servers, 60s alerting SLA, 3 years historical. Is that right?" Then design.</div>
<div class="tip"><strong>When stuck:</strong> Think out loud. "My first instinct is brute force O(n²). I think I can improve this with a hashmap..." Don't go silent.</div>
<div class="tip"><strong>The Citi card:</strong> In EVERY relevant answer, tie back to Citi. "I've actually implemented this — at Citi, the capacity matrix was 6M cells and we used exactly this pattern."</div>
<div class="tip"><strong>Follow-up questions:</strong> They test depth, not tricks. Answer directly. "Yes, you'd use <code>bisect</code> from the standard library — O(log n) lookup in a sorted list."</div>
</div>

</div>

<p style="text-align:center;color:rgba(255,255,255,0.35);font-size:0.8em;margin-top:20px;">
"Simplicity and clarity is Gold." — Sean's Study Mantra &nbsp;|&nbsp; Day 7 Prep Sheet &nbsp;|&nbsp; Generated by Claude Code
</p>

</div>
</body>
</html>'''

html_path = f'{BASE}/day-07-prep-cheatsheet.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(CHEAT_HTML)
print(f'  Written: {html_path}')

print('\nDay 7 complete!')
