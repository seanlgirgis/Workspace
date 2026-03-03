---
created: 2026-03-02
updated: 2026-03-02
summary: Day 13 — Linked Lists | Forecasting SQL + Trend Analysis | Prophet + Linear Regression | Capacity Planning Framework
tags: [study-plan, day-13, leetcode, sql, python, capacity-planning, forecasting]
---

# Study Day 13: Forecasting and the Capacity Planning Differentiator
**Theme:** Linked list patterns + SQL trend analysis + Python forecasting + Capacity planning methodology
**Sean's core differentiator: 10+ years of APM → capacity planning. This day makes it interview-ready.**

---

## Spaced Repetition — Review from Days 1–12
*60 seconds each. Mark Strong / Review / Weak.*

**SR-1 (Day 5):** Four-Step Capacity Planning Loop — name them.
> Baseline → Model (identify driver metric) → Forecast (project to 70% ceiling) → Right-size (provision + set review date). Repeat continuously.

**SR-2 (Day 7 — Mock interview):** What is the error budget for a 99.9% SLO?
> 0.1% = 43.8 minutes per month. Spending the error budget is acceptable; exhausting it early triggers a freeze on new feature deployments.

**SR-3 (Day 8):** pytest `@pytest.mark.parametrize` — what does it do?
> Runs the same test function multiple times with different input sets. Avoids copy-paste test duplication. Each parameter set is a separate test case in the output.

**SR-4 (Day 11):** What is a covering index?
> An index that contains all columns a query needs. The query is answered entirely from the index — no "heap fetch" (no table access needed). Dramatically faster for SELECT-heavy workloads.

**SR-5 (Day 12):** Five dimensions of data quality — name them.
> Completeness, Uniqueness, Validity, Consistency, Freshness. (Some add Accuracy as a sixth — matches ground truth.)

**SR-6 (Day 12):** Greedy vs DP — how do you know which to use?
> Greedy: locally optimal choice = globally optimal. Proof: sorting reveals the order; looking back never helps. DP: optimal substructure with overlapping subproblems. If a greedy choice can be wrong (coin change, knapsack), use DP.

---

## A. LeetCode — Linked Lists

> **Discussion opener:** "Linked lists are less common in data engineering interviews than arrays or trees, but they test pointer manipulation cleanly. The key patterns: fast/slow pointer (detect cycle, find middle), reverse a list, merge sorted lists. In practice, Python deque and the standard library handle most linked-list use cases — but interviewers use LL problems to test whether you can reason about pointer state."

**Linked List node definition:**
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

---

### LC #206 — Reverse Linked List [Easy]
**Category:** Linked List — Pointer Reversal

**Problem:**
Reverse a singly linked list. `1→2→3→4→5` → `5→4→3→2→1`

🎯 **Design Checkpoint:** "Three pointers: prev, curr, next. Save next, point curr to prev, advance both. Repeat."

**Solution 1 — Iterative** O(n) time, O(1) space
```python
def reverseList(head: ListNode) -> ListNode:
    prev = None
    curr = head

    while curr:
        next_node = curr.next    # save next
        curr.next = prev         # reverse the link
        prev = curr              # advance prev
        curr = next_node         # advance curr

    return prev   # prev is now the new head

# State trace for 1→2→3:
# Initially:  prev=None, curr=1
# Iter 1: save 2, curr.next=None, prev=1, curr=2
# Iter 2: save 3, curr.next=1,    prev=2, curr=3
# Iter 3: save None, curr.next=2, prev=3, curr=None
# Return 3 (new head)
```

**Solution 2 — Recursive** O(n) time, O(n) space (call stack)
```python
def reverseList(head: ListNode) -> ListNode:
    if not head or not head.next:
        return head
    new_head = reverseList(head.next)   # reverse rest
    head.next.next = head               # point next node back to head
    head.next = None                     # remove old forward link
    return new_head
```

**Interview Q&A:**
- Q: Why is iterative preferred? A: O(1) space vs O(n) for recursive call stack. With 10,000+ nodes, recursion may cause a stack overflow.

---

### LC #141 — Linked List Cycle Detection [Easy]
**Category:** Fast/Slow Pointers (Floyd's Algorithm)

**Problem:**
Determine if a linked list has a cycle.

🎯 **Design Checkpoint:** "Fast pointer moves 2 steps, slow moves 1. If they meet, there's a cycle. If fast reaches None, no cycle. Like two runners on a circular track — the faster one eventually laps the slower."

**Solution — Floyd's Cycle Detection** O(n) time, O(1) space
```python
def hasCycle(head: ListNode) -> bool:
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow is fast:    # same object in memory
            return True

    return False

# Why is fast: True → O(1) space? No set/visited dict needed.
```

**Interview Q&A:**
- Q: Why does fast moving 2 steps guarantee they meet? A: In a cycle of length L, fast gains 1 step per iteration relative to slow. After at most L iterations inside the cycle, fast catches up to slow.
- Q: HashSet alternative — pros and cons? A: `visited = set(); while node: if node in visited: return True; visited.add(node); node = node.next`. O(n) space but simpler to reason about. Floyd's is O(1) space — always prefer in interviews unless asked about the simpler version.

---

### LC #21 — Merge Two Sorted Lists [Easy]
**Category:** Linked List — Merge

**Problem:**
Merge two sorted linked lists into one sorted linked list.
`1→2→4` + `1→3→4` → `1→1→2→3→4→4`

🎯 **Design Checkpoint:** "Use a dummy head to avoid special-casing the first node. Compare heads of both lists, take the smaller, advance that pointer."

**Solution — Iterative with Dummy** O(m+n) time, O(1) space
```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode(0)   # sentinel — simplifies edge cases
    curr = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next

    curr.next = l1 or l2   # attach remaining list (one is None)

    return dummy.next       # skip the dummy head
```

**Interview Q&A:**
- Q: Why a dummy head? A: Avoids special-casing "first node" — the dummy starts the list so every real node is always attached to something. The return is `dummy.next`.
- Q: Real-world merge: sorted partitions? A: Merging sorted time-series partitions. K-way merge (K sorted lists) uses a min-heap: push first element of each list, pop smallest, push its successor. O(n log k).

---

### LC #19 — Remove Nth Node From End [Medium]
**Category:** Fast/Slow Pointers

**Problem:**
Remove the nth node from the end of a list. Return the head.
`1→2→3→4→5`, `n=2` → `1→2→3→5` (removed 4)

🎯 **Design Checkpoint:** "Two pointers, N apart. When fast reaches end, slow is at the node BEFORE the target. One-pass."

**Solution — Two-Pointer** O(L) time, O(1) space
```python
def removeNthFromEnd(head: ListNode, n: int) -> ListNode:
    dummy = ListNode(0)
    dummy.next = head
    fast = slow = dummy

    # Advance fast by n+1 steps (so slow ends up one before the target)
    for _ in range(n + 1):
        fast = fast.next

    # Move both until fast is None
    while fast:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next   # skip the nth node

    return dummy.next
```

---

## B. SQL — Trend Analysis and Forecasting Patterns

> **Discussion opener:** "SQL can't run Prophet, but it can compute the building blocks of forecasting: trailing averages, growth rates, linear trend slopes. In interviews, 'design a capacity forecast' often means showing you understand the analytical SQL that feeds a forecast — not the ML algorithm itself."

### Trailing Averages — The Baseline
```sql
-- 7-day trailing average CPU per server (foundation of any smoothed trend)
SELECT
    server_id,
    report_date,
    avg_cpu,
    ROUND(
        AVG(avg_cpu) OVER (
            PARTITION BY server_id
            ORDER BY report_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS trailing_7day_avg
FROM daily_metrics
ORDER BY server_id, report_date;
```

### Growth Rate — Period over Period
```sql
-- Week-over-week CPU growth rate per server
WITH weekly AS (
    SELECT
        server_id,
        DATE_TRUNC('week', report_date) AS week_start,
        AVG(avg_cpu) AS weekly_avg_cpu
    FROM daily_metrics
    GROUP BY server_id, DATE_TRUNC('week', report_date)
),
with_lag AS (
    SELECT
        server_id,
        week_start,
        weekly_avg_cpu,
        LAG(weekly_avg_cpu) OVER (
            PARTITION BY server_id ORDER BY week_start
        ) AS prev_week_avg
    FROM weekly
)
SELECT
    server_id,
    week_start,
    ROUND(weekly_avg_cpu, 1) AS this_week,
    ROUND(prev_week_avg, 1) AS last_week,
    ROUND(100.0 * (weekly_avg_cpu - prev_week_avg) / NULLIF(prev_week_avg, 0), 1) AS wow_pct_change
FROM with_lag
WHERE prev_week_avg IS NOT NULL
ORDER BY wow_pct_change DESC;
```

### Linear Trend — Days Until 70% Ceiling
```sql
-- Compute linear regression slope using SQL (manual formula)
-- slope = (n*Σxy - Σx*Σy) / (n*Σx² - (Σx)²)
-- x = day_number, y = avg_cpu

WITH numbered AS (
    SELECT
        server_id,
        report_date,
        avg_cpu,
        ROW_NUMBER() OVER (PARTITION BY server_id ORDER BY report_date) AS day_num
    FROM daily_metrics
),
regression AS (
    SELECT
        server_id,
        COUNT(*) AS n,
        SUM(day_num * avg_cpu) AS sum_xy,
        SUM(day_num) AS sum_x,
        SUM(avg_cpu) AS sum_y,
        SUM(day_num * day_num) AS sum_x2,
        AVG(avg_cpu) AS avg_y,
        MAX(day_num) AS last_day,
        MAX(avg_cpu) AS latest_cpu
    FROM numbered
    GROUP BY server_id
)
SELECT
    server_id,
    ROUND(avg_y, 1) AS current_avg,
    ROUND(
        (n * sum_xy - sum_x * sum_y) / NULLIF((n * sum_x2 - sum_x * sum_x), 0), 4
    ) AS daily_growth_rate,
    ROUND(
        CASE
            WHEN (n * sum_xy - sum_x * sum_y) > 0
            THEN (70.0 - latest_cpu) /
                 NULLIF((n * sum_xy - sum_x * sum_y) / NULLIF((n * sum_x2 - sum_x * sum_x), 0), 0)
            ELSE NULL
        END
    ) AS days_to_70pct_ceiling
FROM regression
ORDER BY days_to_70pct_ceiling NULLS LAST;
```

**Interview Q&A:**
- Q: Why 70% as the capacity ceiling? A: CPU above 70% sustained starts causing queueing delays. Above 85%, response times degrade significantly (Little's Law + M/D/1 queuing). The 70% threshold gives a 6-week buffer window for provisioning decisions. At Citi this was the standard alert threshold.
- Q: What is a capacity "runway"? A: Days (or months) remaining before current usage hits the capacity ceiling. The metric that drives provisioning decisions. Less than 30 days = emergency procurement. 30-90 days = planned order. 90+ days = monitor.
- Q: How do you handle seasonality in trend analysis? A: SQL-level: compute same-week-last-year comparisons (YoY). Python-level: Prophet decomposes trend + seasonality components automatically.

---

## C. Python — Prophet and Linear Regression for Capacity Forecasting

> **Discussion opener:** "This is Sean's differentiator made technical. Most engineers can describe a monitoring dashboard. Few can explain: 'here is how I fit a linear trend to 90 days of CPU data, projected it forward to the 70% ceiling, and gave the team a 6-week runway number.' This is what senior capacity planning engineers do."

### Linear Regression Forecast — scikit-learn
```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta

# Sample: 30 days of CPU data for one server
np.random.seed(42)
dates = pd.date_range('2026-01-01', periods=30, freq='D')
cpu_values = 50 + np.arange(30) * 0.8 + np.random.normal(0, 2, 30)  # trending up

df = pd.DataFrame({'date': dates, 'avg_cpu': cpu_values})
df['day_num'] = (df['date'] - df['date'].min()).dt.days

# Fit linear regression
X = df[['day_num']].values
y = df['avg_cpu'].values

model = LinearRegression()
model.fit(X, y)

slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)

print(f"Slope: {slope:.3f} CPU%/day")
print(f"R²:    {r2:.3f}")
print(f"Intercept: {intercept:.1f}%")

# Forecast: when does this server hit 70% ceiling?
CEILING = 70.0
if slope > 0 and model.predict([[0]])[0] < CEILING:
    days_to_ceiling = (CEILING - intercept) / slope
    ceiling_date = df['date'].min() + timedelta(days=days_to_ceiling)
    print(f"\nProjected to hit {CEILING}% CPU: Day {days_to_ceiling:.0f}")
    print(f"  Estimated date: {ceiling_date.date()}")
else:
    print(f"\nServer not trending toward {CEILING}% ceiling")

# Forecast next 30 days
future_days = np.arange(30, 60).reshape(-1, 1)
future_cpu = model.predict(future_days)
future_dates = [df['date'].max() + timedelta(days=i+1) for i in range(30)]

forecast_df = pd.DataFrame({'date': future_dates, 'predicted_cpu': future_cpu.round(1)})
print(f"\nNext 30-day forecast range: {forecast_df['predicted_cpu'].min():.1f}% - {forecast_df['predicted_cpu'].max():.1f}%")
```

### Prophet — Decomposed Forecasting with Seasonality
```python
# pip install prophet
# Prophet handles: trend + weekly seasonality + annual seasonality + holidays

from prophet import Prophet
import pandas as pd
import numpy as np

# Prophet requires columns: 'ds' (datetime) and 'y' (value)
np.random.seed(42)
dates = pd.date_range('2025-01-01', periods=365, freq='D')
# Simulate: upward trend + weekly seasonality (lower weekends)
trend = np.linspace(40, 65, 365)
weekly = 5 * np.sin(2 * np.pi * np.arange(365) / 7)
noise = np.random.normal(0, 2, 365)
cpu = trend + weekly + noise

df = pd.DataFrame({'ds': dates, 'y': cpu})

# Fit model
model = Prophet(
    interval_width=0.95,           # 95% confidence interval
    changepoint_prior_scale=0.05,  # flexibility of trend changes (lower = smoother)
    weekly_seasonality=True,
    yearly_seasonality=True,
)
model.fit(df)

# Forecast 90 days ahead
future = model.make_future_dataframe(periods=90)
forecast = model.predict(future)

# Extract key numbers
next_90 = forecast[forecast['ds'] > df['ds'].max()][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
peak_forecast = next_90['yhat_upper'].max()
print(f"Peak forecast (95th pct upper bound) in next 90 days: {peak_forecast:.1f}%")

# Days until 70% ceiling (using upper confidence bound for conservative planning)
at_ceiling = next_90[next_90['yhat_upper'] >= 70.0]
if not at_ceiling.empty:
    days_to_ceiling = (at_ceiling.iloc[0]['ds'] - df['ds'].max()).days
    print(f"Upper bound hits 70% ceiling in {days_to_ceiling} days")
    print(f"  Date: {at_ceiling.iloc[0]['ds'].date()}")
else:
    print("Upper bound stays below 70% ceiling for 90 days")

# Components (the insight)
print("\nTrend: upward" if forecast['trend'].iloc[-1] > forecast['trend'].iloc[0] else "Trend: stable/downward")
```

### The Capacity Planning Report — Pulling It Together
```python
def capacity_report(server_metrics_df: pd.DataFrame, ceiling: float = 70.0) -> pd.DataFrame:
    """
    For each server: current CPU, 30-day trend slope, days to ceiling.
    Input: DataFrame with columns server_id, report_date, avg_cpu
    """
    results = []

    for server_id, df in server_metrics_df.groupby('server_id'):
        df = df.sort_values('report_date').copy()
        df['day_num'] = (df['report_date'] - df['report_date'].min()).dt.days

        if len(df) < 7:     # need at least a week of data
            continue

        # Fit trend
        from sklearn.linear_model import LinearRegression
        X = df[['day_num']].values
        y = df['avg_cpu'].values
        model = LinearRegression().fit(X, y)

        slope = model.coef_[0]
        current_cpu = df['avg_cpu'].iloc[-1]
        r2 = model.score(X, y)

        # Days to ceiling
        if slope > 0 and current_cpu < ceiling:
            days = int((ceiling - model.predict([[len(df)]])[0]) / slope)
        else:
            days = None

        results.append({
            'server_id': server_id,
            'current_cpu_pct': round(current_cpu, 1),
            'daily_growth_rate': round(slope, 3),
            'r2': round(r2, 3),
            'days_to_70pct_ceiling': days,
            'status': (
                'CRITICAL' if current_cpu >= 90 else
                'WARNING'  if current_cpu >= 75 else
                'WATCH'    if days is not None and days < 30 else
                'NORMAL'
            )
        })

    return pd.DataFrame(results).sort_values('days_to_70pct_ceiling', na_position='last')

# Run the report
import pandas as pd
import numpy as np

# Generate sample data
np.random.seed(42)
data = []
for i in range(1, 7):
    days = pd.date_range('2026-01-01', periods=60, freq='D')
    slope = np.random.uniform(-0.1, 0.6)
    base = np.random.uniform(40, 75)
    for d, day in enumerate(days):
        data.append({
            'server_id': f'srv-{i:02d}',
            'report_date': day,
            'avg_cpu': base + slope * d + np.random.normal(0, 2)
        })

df = pd.DataFrame(data)
df['report_date'] = pd.to_datetime(df['report_date'])

report = capacity_report(df)
print(report.to_string(index=False))
```

**Interview Q&A:**
- Q: Why use the upper confidence bound for capacity planning, not the point estimate? A: Capacity planning is risk management. Using the upper bound (worst-case scenario) ensures you provision before the 70% ceiling is actually hit, not after. Conservative planning prevents capacity incidents.
- Q: What is the R² value and what does a low R² mean for capacity planning? A: R² measures how well the linear model fits the data. Low R² = high variance, erratic behavior. Don't use a linear forecast for erratic servers — use rolling averages instead, or flag for manual review. Trust the forecast only when R² > 0.6.
- Q: Prophet vs linear regression — when to use each? A: Linear regression: simple, fast, interpretable. Use when the trend is smooth and steady. Prophet: handles seasonality (weekly patterns, holidays), trend changepoints, and missing data gracefully. Use when you have >6 months of data with visible seasonality.

---

## D. Technology — Capacity Planning Framework

> **Discussion opener:** "Capacity planning is not dashboards. It is a repeatable process. Sean knows this better than most interviewers. The framework is: Baseline → Model → Forecast → Right-size. The 10+ years of APM experience at Citi makes every step of this concrete."

### The Four-Step Loop (Revisited and Deepened)
```
STEP 1: BASELINE
  What: Establish current utilization across all resources.
  SQL:  30-day trailing averages, P50/P95/P99 per resource.
  Tool: DuckDB / Athena on historical Parquet data.
  Output: "srv-01 is running at P95 = 87% CPU, P50 = 72% CPU."

STEP 2: MODEL
  What: Identify the demand driver (what causes this metric to grow?).
  Questions to ask:
    - Is growth driven by user/request volume? Data volume? Batch size?
    - Is it seasonal (higher load on weekdays, end-of-month)?
    - Is the trend linear? Exponential? Cyclical?
  Output: "srv-01 CPU grows 0.4%/day, R²=0.85. Driver: transaction volume."

STEP 3: FORECAST
  What: Project the demand driver forward. Apply to capacity model.
  Method: Linear regression for stable trends. Prophet for seasonal.
  Conservative: use upper confidence bound (95th percentile).
  Key question: "Days until 70% ceiling?" (70% = safe operational limit)
  Output: "srv-01 hits 70% ceiling in 45 days. Date: 2026-04-17."

STEP 4: RIGHT-SIZE
  What: Make a provisioning recommendation.
  Vertical: Add CPU/RAM to existing server.
  Horizontal: Add more servers (scale out).
  Cloud: Change instance type (m5.xlarge → m5.2xlarge).
  Timing: Order/provision BEFORE 30-day runway expires.
  Output: "Upgrade srv-01 from 4-core to 8-core by 2026-03-15."

REPEAT: Scheduled re-run (weekly or monthly). New data → new baseline.
```

### Interview Answer: "Walk Me Through How You Would Plan Capacity for 6,000 Servers"

```
1. COLLECT: All 6,000 servers reporting CPU, memory, disk to Kafka → S3 Parquet.
   Partition: by date + environment.

2. BASELINE (SQL/DuckDB): For each server:
   - 30-day P50, P95, P99 CPU utilization
   - Current vs 30-days-ago (growth delta)
   - Flag any already above 70% (immediate attention)

3. PRIORITIZE: Cluster servers by risk:
   - CRITICAL:  Already above 85% → immediate action
   - WARNING:   70-85% → 2-week window
   - WATCH:     Runway < 30 days → plan procurement
   - NORMAL:    Monitor monthly

4. FORECAST (Python): Linear regression on 90-day history per server.
   Daily job: recalculate runway for all servers.
   Outputs: runway_days, projected_ceiling_date, confidence (R²).

5. AUTOMATE REPORTING: Airflow DAG:
   - Daily: run quality checks + update runway numbers
   - Weekly: capacity report email to management (Pareto: top 20 servers by risk)
   - Monthly: infrastructure budget forecast

6. RIGHT-SIZE RECOMMENDATIONS:
   - Generate provisioning tickets for any server < 45 days runway
   - Include: current server spec, recommended spec, cost delta
   - Route to appropriate team (infra, cloud, DBA)

This process ran manually at Citi across 4 APM tools.
In AWS today: same process, Athena + Lambda + QuickSight, fully automated.
```

**Interview Q&A:**
- Q: How do you handle a server that shows erratic CPU (no clear trend)? A: Investigate root cause first — scheduled batch jobs, backup windows, noisy neighbor. If the pattern is irregular, use rolling average + max headroom rather than a linear forecast. Flag for manual review instead of automated provisioning.
- Q: What is a "noisy neighbor" in capacity planning? A: A tenant or application on shared infrastructure using significantly more resources than expected, impacting others. Detection: P99 is much higher than P95 for one server. Resolution: isolate the workload or enforce quotas.
- Q: How do you communicate capacity runway to a non-technical audience? A: Traffic light + number: "🟡 srv-01: 45 days until capacity ceiling." Leadership cares about the deadline and cost, not the regression slope. Present: current status, date of risk, cost to remediate.

---

## Today's Key Interview Talking Points

1. **"Fast/slow pointers (Floyd's) solves cycle detection in O(1) space — the key insight is the mathematical catch-up guarantee."**
2. **"Trailing averages in SQL are the foundation of every monitoring dashboard. 7-day rolling avg = the baseline."**
3. **"Linear regression gives days-to-ceiling: `(70 - current_cpu) / daily_growth_rate`. That's the number executives care about."**
4. **"Prophet adds seasonality decomposition — use it when you have weekly patterns (weekday/weekend CPU variance)."**
5. **"The four steps: Baseline → Model → Forecast → Right-size. This is not a dashboard project. It is a risk management process."**
6. **"Capacity planning differentiator: 'I've done this for 6,000 servers across 4 APM tools. The framework doesn't change — only the data source.'"**

---

## Behavioral Anchor — Citi Story #13

**Topic: Capacity Planning — Core Differentiator Story**

Practice this story (2 minutes, STAR format):

> *"At Citi I owned capacity planning for over 6,000 servers instrumented with CA APM, AppDynamics, Dynatrace, and BMC TrueSight. The challenge: four tools, four schemas, one capacity report. I built a unified collection pipeline that normalized all four to a common schema — server_id, metric, timestamp, value. From that, I ran 90-day linear trend analysis against every server's CPU utilization, calculated days to the 70% capacity ceiling, and produced a weekly prioritized list: the top 20 servers by runway risk. Infrastructure teams used this list to schedule procurement. We went from reactive capacity expansions — where servers hit limits before anyone noticed — to a 6-week proactive window. That's the difference between capacity planning and capacity monitoring."*

**Gemini: ask Sean to tell this story unprompted. Time him. Give STAR feedback.**

---

## Day 13 — Reflection

Before Day 14 mock interview, run through this self-assessment:

```
Rate yourself 1-5 on each:

LeetCode Patterns:
  [ ] HashMap / HashSet (Day 1)
  [ ] Sliding Window (Day 2)
  [ ] Stack / Monotonic Stack (Day 3)
  [ ] Binary Search (Day 4)
  [ ] Heap / Priority Queue (Day 5)
  [ ] Intervals — merge, insert, count (Day 6)
  [ ] Trees — BFS, DFS, level order (Day 8)
  [ ] Two Pointers (Day 9)
  [ ] Dynamic Programming 1D (Day 10)
  [ ] Graphs — BFS, DFS, topological sort (Day 11)
  [ ] Greedy (Day 12)
  [ ] Linked Lists (Day 13)

SQL:
  [ ] CTEs — regular and recursive (Day 1)
  [ ] Window functions — RANK, LAG, LEAD, frames (Day 2)
  [ ] Complex JOINs — self, anti, cross (Day 3)
  [ ] Query optimization + EXPLAIN (Day 4, 11)
  [ ] Analytical SQL — YoY, cohort (Day 5)
  [ ] Schema design — star, snowflake, SCD (Day 6)
  [ ] CASE WHEN + conditional aggregation (Day 8)
  [ ] Date/time functions + gaps & islands (Day 9)
  [ ] GROUPING SETS / ROLLUP / CUBE (Day 10)
  [ ] Data quality SQL patterns (Day 12)
  [ ] Trend analysis + linear regression SQL (Day 13)

System Design:
  [ ] Data lake architecture (S3 + Glue + Athena) (Day 1)
  [ ] Lambda vs Kappa architecture (Day 3)
  [ ] APM + observability design (Day 4)
  [ ] End-to-end data platform system design (Day 6)
  [ ] Airflow DAG design (Day 8)
  [ ] Kafka — partitions, consumer groups, guarantees (Day 9)
  [ ] Delta Lake / Iceberg — ACID data lakes (Day 11)
  [ ] AWS cost optimization (Day 12)
  [ ] Capacity planning framework (Day 13)

Behavioral:
  [ ] Citi scale story (6,000 servers, 4 APM tools) (Day 1)
  [ ] Data quality / silent failure story (Day 8)
  [ ] Parallel processing improvement story (Day 9)
  [ ] Performance optimization (45min → 4sec query) (Day 11)
  [ ] Capacity planning — core differentiator story (Day 13)

Focus your review tonight on anything rated 1-2. Tomorrow is the mock.
```

---

## End of Day 13 — Wrap-Up

Gemini reports:
```
Day 13 Complete.
Topics covered: Linked Lists | Trend SQL | Prophet + Linear Regression | Capacity Planning Framework
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 14: Full Mock Interview Week 2.
No more study. Gemini becomes the interviewer.
```
