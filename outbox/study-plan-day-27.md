---
created: 2026-03-02
updated: 2026-03-02
summary: Day 27 — Full Mock Interview Week 4. Finance/Banking DE focus. Hardest technical bar of the 4-week plan. 26-point scorecard. Gemini is the interviewer.
tags: [study-plan, day-27, mock-interview, finance-de, all-topics, week-4]
---

# Day 27 — Full Mock Interview Week 4 (Finance DE Focus)

**Theme:** This is the final mock. It is harder than Weeks 2 and 3. Finance DE interviews are stricter on correctness, governance, and operational thinking.

> **Gemini Instructions:** You are a VP-level interviewer at a Tier 1 financial institution. You are conducting a final-round interview for a Senior Data Engineer role.
>
> Rules for Day 27:
> - **No hints. No warmth.** This is a business interview, not a study session.
> - **Strict timing.** Call time on every question. No extensions.
> - **Press behavioral answers hard.** "What exactly did YOU do?" "What was the specific business impact?"
> - **Finance lens on system design.** Push on auditability, idempotency, regulatory requirements, and operational risk.
> - **After each round:** privately mark Strong / Review / Weak. Do not reveal until debrief.
> - **At the end:** full scorecard, top 3 gaps, final verdict.

---

## Interview Structure

```
Round 1: Coding — Hard Bar                     (35 min)
  → 3 problems: Medium / Hard / SQL
  → Timing strict. No working code = no credit.

Round 2: System Design — Regulatory Grade      (30 min)
  → Complex finance-adjacent design
  → Probes on auditability, SLA, idempotency

Round 3: Finance DE Concepts                   (20 min)
  → 8 questions, 90 seconds each
  → Mix of all 4 weeks + finance-specific

Round 4: Behavioral — Senior Standard          (15 min)
  → 3 stories, 90 seconds each
  → Heavy pressing for specifics

Debrief                                         (10 min)
  → 26-point scorecard
  → Top 3 gaps
  → Final verdict: Interview-Ready or Not
```

---

## Round 1: Coding — Hard Bar (35 min)

> **Gemini:** Say this exactly: "Three questions. First two are coding, last is SQL. Strict timing. Ready?"

---

### Coding Q1 — Medium (10 min): Jump Game II

> **Gemini:** Start timer.

**Problem:** Given an integer array `nums` where `nums[i]` is the maximum jump length from position `i`, return the minimum number of jumps to reach the last index. You can always reach the last index.

```
Input:  [2, 3, 1, 1, 4]
Output: 2   (jump 0→1→4)

Input:  [2, 3, 0, 1, 4]
Output: 2
```

**Gemini scoring:**
- Full credit: O(n) greedy — track `farthest`, `current_end`, `jumps`
- Partial credit: BFS approach (also O(n)) — correct but notes the cleaner greedy
- No credit: O(n²) or incorrect

**Answer (Gemini reference):**
```python
def jump(nums):
    jumps = 0
    current_end = 0   # end of current jump's reachable range
    farthest = 0      # farthest we can reach from any position <= current_end

    for i in range(len(nums) - 1):   # don't need to jump from last position
        farthest = max(farthest, i + nums[i])
        if i == current_end:          # we've exhausted the current jump
            jumps += 1
            current_end = farthest    # extend to farthest reachable
            if current_end >= len(nums) - 1:
                break

    return jumps
```

**Gemini follow-up:** "What is the time complexity? Why don't we iterate over the last index?"

---

### Coding Q2 — Hard (15 min): Serialize and Deserialize Binary Tree

> **Gemini:** Start timer.

**Problem:** Design an algorithm to serialize a binary tree to a string and deserialize that string back to the tree. No specific format required — choose what makes sense.

```
Input:  Tree [1, 2, 3, null, null, 4, 5]
Output: Serialize to string, then deserialize back to the exact same tree.
```

**Gemini scoring:**
- Full credit: BFS or DFS serialization with null markers, correct deserialization with index/queue tracking
- Partial credit: correct approach but edge case fails (empty tree, single node)
- No credit: incorrect or incomplete

**Answer (Gemini reference — BFS approach):**
```python
from collections import deque

class Codec:
    def serialize(self, root):
        if not root:
            return ""
        result = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")
        return ",".join(result)

    def deserialize(self, data):
        if not data:
            return None
        vals = data.split(",")
        root = TreeNode(int(vals[0]))
        queue = deque([root])
        i = 1
        while queue and i < len(vals):
            node = queue.popleft()
            if vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                queue.append(node.left)
            i += 1
            if i < len(vals) and vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1
        return root
```

**Gemini follow-up:** "Why did you choose BFS over DFS? What are the trade-offs?"

---

### SQL Q3 — Finance-Grade (10 min)

> **Gemini:** Start timer.

**Schema:**
```
positions(trade_id VARCHAR, asset_id VARCHAR, position_date DATE, quantity FLOAT, book_id VARCHAR)
reference_prices(asset_id VARCHAR, price_date DATE, close_price FLOAT)
```

**Problem:** Calculate mark-to-market P&L per book per day. P&L = today's market value minus yesterday's market value. Market value = quantity × close_price. Return: book_id, position_date, market_value, prior_day_value, daily_pnl. Only include days where both today and yesterday have prices.

**Gemini scoring:**
- Full credit: correct window function or self-join for prior day, correct aggregation (SUM not AVG), handles NULL when prior day missing
- Partial credit: correct logic but misses the NULL filter or gets aggregation wrong
- No credit: wrong join or wrong P&L calculation

**Answer (Gemini reference):**
```sql
WITH position_value AS (
    SELECT
        p.book_id,
        p.position_date,
        SUM(p.quantity * r.close_price)     AS market_value
    FROM positions p
    JOIN reference_prices r
        ON p.asset_id = r.asset_id
       AND p.position_date = r.price_date
    GROUP BY p.book_id, p.position_date
),
with_prior AS (
    SELECT
        book_id,
        position_date,
        market_value,
        LAG(market_value) OVER (
            PARTITION BY book_id
            ORDER BY position_date
        )                                   AS prior_day_value
    FROM position_value
)
SELECT
    book_id,
    position_date,
    ROUND(market_value, 2)                  AS market_value,
    ROUND(prior_day_value, 2)               AS prior_day_value,
    ROUND(market_value - prior_day_value, 2) AS daily_pnl
FROM with_prior
WHERE prior_day_value IS NOT NULL
ORDER BY book_id, position_date;
```

---

## Round 2: System Design — Regulatory Reporting Platform (30 min)

> **Gemini:** Say this: "Design a regulatory reporting platform that captures end-of-day positions across all trading books, calculates risk metrics, and submits a report to the regulator by 6am. The system must support audit queries going back 7 years. Walk me through your design."

**After 10-12 minutes, probe:**

**Probe 1 — Auditability:**
"A regulator asks: what was the net position in book XYZ for asset ABC on March 15th 2024? How do you answer that with your design?"
*(Expected: immutable audit store — S3 with versioning, Delta Lake time travel, or dedicated audit tables. Every submission archived with timestamp and version. Direct query of historical snapshot.)*

**Probe 2 — Idempotency:**
"Your pipeline fails at 3am and restarts. How do you ensure you don't double-count any positions in the report?"
*(Expected: idempotent writes — UPSERT with trade_id + date as key, or delete-partition + reload. Checkpoint table tracks processed batch IDs. Reconcile totals before submitting.)*

**Probe 3 — Late Data:**
"Market data provider delivers prices 45 minutes late. Your pipeline starts at midnight using yesterday's prices but tonight's is incomplete. What do you do?"
*(Expected: two-pass design: pre-run with stale prices flagged, re-run when prices arrive. Or: SLA with provider. Alert if data not received by T+30min. Fallback: use prior close with a flag in the report.)*

**Probe 4 — Lineage:**
"A number in the regulatory report is questioned. How do you trace it back to the source trade?"
*(Expected: field-level lineage — every output number traceable to: pipeline version, source trade ID, reference price used, transformation applied. OpenMetadata or custom lineage table. Each report row has a checksum and source reference.)*

**Probe 5 — SLA Breach:**
"It's 5:30am. The report isn't complete. What do you do?"
*(Expected: pre-established escalation runbook. Operations manager paged at 5am if not 90% complete. Manual override option: partial report submission with flagged incomplete books. Regulator has a notification protocol for late submissions. Post-mortem required.)*

**Gemini scoring:**
- Full credit: covers ingest, position aggregation, audit store, lineage, SLA handling, fail-safe reporting
- Partial credit: covers technical design but misses regulatory/compliance dimensions
- No credit: describes a generic ETL pipeline without finance-specific considerations

---

## Round 3: Finance DE Concepts — 8 Questions (20 min)

> **Gemini:** "8 questions. 90 seconds each. Start now."

**Q1:** "What is exactly-once semantics in stream processing and how does Flink achieve it?"
> Exactly-once means each event is processed exactly once — no loss, no duplicates. Flink uses distributed snapshots (Chandy-Lamport algorithm) stored in S3. On failure, restore from the last checkpoint: all state is reset to that point, all sources replay from their saved offsets. Combined with idempotent sinks, this gives end-to-end exactly-once.

**Q2:** "What is a Snowflake Stream and how would you use it in a daily positions pipeline?"
> A Snowflake Stream is a CDC tracker on a table — it captures INSERT/UPDATE/DELETE since the stream was last consumed. In a positions pipeline: stream on the positions table captures intraday trades as they're booked. A Task runs every 5 minutes, reads the stream, and updates an aggregated positions summary. At EOD: final Task run produces the regulatory snapshot.

**Q3:** "Why is `ROW_NUMBER()` safer than `RANK()` for deduplication?"
> `RANK()` assigns the same rank to ties — two rows with the same value both get rank 1, so `WHERE rank = 1` would keep both duplicates. `ROW_NUMBER()` always assigns a unique sequential number regardless of ties — `WHERE rn = 1` always picks exactly one row. For deduplication where ties are broken arbitrarily, ROW_NUMBER is correct.

**Q4:** "In Python asyncio, why is a Semaphore important when calling external APIs?"
> Without a Semaphore, `asyncio.gather()` with 1000 coroutines launches 1000 concurrent connections simultaneously — overwhelming the API (rate limit / connection pool exhaustion). A Semaphore(20) limits to 20 concurrent active coroutines. The other 980 wait. Total throughput stays high while respecting the API's limits. In finance: crucial for market data APIs with strict rate limits.

**Q5:** "What is the difference between Apache Beam and Apache Flink?"
> Beam is a programming model / abstraction layer. Flink is an execution engine. You write Beam code and choose a runner: Flink, Dataflow (GCP), Spark, or Local. Flink native has more advanced stateful operations and lower latency than Beam-on-Flink. Beam trades some performance for portability. If you're locked to GCP, use Beam + Dataflow. If you control the runtime and need maximum performance, use Flink native.

**Q6:** "A recursive CTE in PostgreSQL terminates with `UNION ALL`. What happens if you accidentally create a cycle in the graph data?"
> Infinite loop — the query never terminates. PostgreSQL will exhaust memory or hit a query timeout. Prevention: (1) add a depth counter and terminate at `WHERE depth < MAX_DEPTH`. (2) Cycle detection: accumulate the path as an array and use `NOT (node_id = ANY(path))` as a termination condition. (3) Use graph databases or dedicated graph algorithms for truly cyclic graphs.

**Q7:** "What is ClickHouse's MergeTree and why is the `ORDER BY` key critical?"
> MergeTree stores data in sorted order by the `ORDER BY` key. Queries that filter on the sort key use sparse indexing — they skip entire 8192-row granules, not individual rows. This makes range queries on the sort key 100-1000x faster than a full scan. Critical: if you query by `server_id` and `report_date` frequently, your sort key should start with those columns. Wrong ORDER BY = full table scans even on indexed queries.

**Q8:** "Explain BCBS 239 in one minute to a non-technical colleague."
> "It's a rule from bank regulators that says: banks must be able to pull any piece of risk data, fully explained, quickly and accurately. The data can't just be correct — it has to be traceable. If the regulator asks 'where did this number come from?' you have to be able to answer, step by step, all the way back to the original trade. It also means data quality is non-negotiable for risk data — no estimates, no stale numbers, no missing values. For us in data engineering, it means every pipeline that feeds risk reports needs full lineage, documented quality controls, and audit logs."

---

## Round 4: Behavioral — Senior Standard (15 min)

> **Gemini:** "Three stories. 90 seconds. I will interrupt if you drift. I will press for specifics."

---

**Behavioral 1 (90 sec):** "Tell me about the most consequential data error you've been responsible for."

*What Gemini is pressing for:*
- Real ownership — not deflection ("the system had a bug")
- Scope of impact — who was affected, what downstream processes
- Response — speed, communication, fix
- Prevention — what changed after

*Press hard:* "What was the downstream impact specifically? How did you discover it was YOUR pipeline? What did you do in the first hour?"

---

**Behavioral 2 (90 sec):** "Tell me about a time you pushed back on a deadline that you believed was unrealistic."

*What Gemini is pressing for:*
- Legitimate technical judgment (not just wanting more time)
- How you framed the argument (data, not emotion)
- The outcome — were you right? Did the team adjust?
- The relationship after

*Press:* "What exactly was your argument? What data did you use? How did the manager respond?"

---

**Behavioral 3 (90 sec):** "What is the most important thing a data engineer can do to build trust with business stakeholders?"

*What Gemini is listening for:*
- Concrete answer, not platitudes ("communicate well")
- Shows understanding of the business perspective
- Supported by a specific example
- Shows maturity: trust is built over time through reliability, not words

*Press:* "Give me a concrete example from your own experience where you built or rebuilt trust."

---

## Debrief (10 min)

> **Gemini:** Reveal the full scorecard now.

```
ROUND 1: Coding

Q1 - Jump Game II:                   [ ] Full [ ] Partial [ ] No credit
  Note: ___

Q2 - Serialize/Deserialize Tree:     [ ] Full [ ] Partial [ ] No credit
  Note: ___

SQL - Mark-to-Market P&L:            [ ] Full [ ] Partial [ ] No credit
  Note: ___

Round 1 Score: ___ / 3

---

ROUND 2: System Design

Covered position aggregation:        [ ] Strong [ ] Partial [ ] Weak
Covered audit store (7-year):        [ ] Yes [ ] Partial [ ] No
Handled idempotency probe:           [ ] Strong [ ] Partial [ ] Weak
Handled late data probe:             [ ] Strong [ ] Partial [ ] Weak
Covered lineage (field-level):       [ ] Yes [ ] Partial [ ] No
Covered SLA breach runbook:          [ ] Yes [ ] Partial [ ] No
Regulatory framing (BCBS, etc.):     [ ] Strong [ ] None

Round 2 Score: ___ / 7

---

ROUND 3: Finance DE Concepts

Q1 - Exactly-once / Flink:           [ ] Strong [ ] Weak
Q2 - Snowflake Streams:              [ ] Strong [ ] Weak
Q3 - ROW_NUMBER vs RANK dedup:       [ ] Strong [ ] Weak
Q4 - asyncio Semaphore:              [ ] Strong [ ] Weak
Q5 - Beam vs Flink:                  [ ] Strong [ ] Weak
Q6 - Recursive CTE cycles:           [ ] Strong [ ] Weak
Q7 - ClickHouse ORDER BY:            [ ] Strong [ ] Weak
Q8 - BCBS 239 plain English:         [ ] Strong [ ] Weak

Round 3 Score: ___ / 8

---

ROUND 4: Behavioral

B1 - Consequential data error:       [ ] Strong [ ] Partial [ ] Weak
B2 - Pushed back on deadline:        [ ] Strong [ ] Partial [ ] Weak
B3 - Building stakeholder trust:     [ ] Strong [ ] Partial [ ] Weak

Round 4 Score: ___ / 3

---

OVERALL WEEK 4 MOCK: ___ / 21

21-19: Finance-ready. Schedule the real interview.
18-15: Strong candidate, one more targeted day.
14-10: 2-3 days of focused work needed.
9 or below: Return to specific week's material.

---

CUMULATIVE SCORE (all 4 mocks):
Week 1 Mock (Day 7):    ___ / 18
Week 2 Mock (Day 14):   ___ / 22
Week 3 Mock (Day 21):   ___ / 23
Week 4 Mock (Day 27):   ___ / 21
TOTAL: ___ / 84
```

---

## Post-Interview: Top 3 Gaps

> **Gemini:** Based on the scorecard AND the pattern across all 4 mock interviews, identify the top 3 persistent gaps.

```
Gap 1 (persistent — seen across N mocks): ___
Action: ___

Gap 2: ___
Action: ___

Gap 3: ___
Action: ___
```

---

## Final Message from Gemini

```
27 days.

You have built something real.

Four weeks of structured study. Four full mock interviews. Coverage
across algorithms, SQL, Python, architecture, system design, behavioral,
finance-specific concepts, and negotiation strategy.

Your differentiator has not changed:
  10+ years APM
  × 6,000-server capacity planning at real scale
  × The ability to name the exact SQL, Python, and architecture
    that operationalizes it
  × The vocabulary to speak to finance DE requirements:
    audit trails, idempotency, lineage, regulatory reporting

Own that story. Stop hedging.

Tomorrow is the final day. It's not more study.
It's clarity on the path forward.
```
