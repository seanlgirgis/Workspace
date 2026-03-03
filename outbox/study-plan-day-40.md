---
created: 2026-03-02
updated: 2026-03-02
summary: Day 40 — 2D DP review, advanced window functions, and system design drill for a streaming analytics platform.
tags: [study-plan, day-40, week-6, 2d-dp, advanced-windows, system-design-drill]
---

# Day 40 — 2D DP Review + Advanced Windows + System Design Drill

**Theme:** 40 days in. You've been at this long enough to know what your real weaknesses are. Today's system design drill uses that knowledge.

---

## Daily Maintenance (35 min)

**LC — 2D Dynamic Programming (2 problems, timed):**
- LC #62 Unique Paths (6 min — build the grid or use rolling 1D array)
- LC #1143 Longest Common Subsequence (12 min — `dp[i][j] = dp[i-1][j-1]+1` if match, else `max(...)`)

After LCS: write the recurrence in English first, then translate to code.

**SQL — Advanced Window Functions:**
```sql
-- These patterns all come up in finance interviews:

-- 1. Percent of total within group (no subquery needed):
SELECT server_id, region, avg_cpu,
       ROUND(avg_cpu / SUM(avg_cpu) OVER (PARTITION BY region) * 100, 1)
           AS pct_of_region_total
FROM server_snapshot;

-- 2. Running total that resets per partition:
SELECT server_id, report_date, avg_cpu,
       SUM(avg_cpu) OVER (
           PARTITION BY server_id
           ORDER BY report_date
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS cumulative_cpu
FROM daily_metrics;

-- 3. First and last value per partition:
SELECT server_id, report_date, avg_cpu,
       FIRST_VALUE(avg_cpu) OVER (PARTITION BY server_id ORDER BY report_date) AS first_cpu,
       LAST_VALUE(avg_cpu)  OVER (PARTITION BY server_id ORDER BY report_date
                                   ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
                                 ) AS last_cpu
FROM daily_metrics;
```

**Behavioral:** "Describe the system you're most proud of having built. What made it great?"

---

## System Design Drill — Streaming Analytics Platform (40 min)

**Set timer: 15 minutes. Draw this design, then critique it.**

**Prompt:** "Design a streaming platform that ingests 50,000 server metrics per second, detects threshold breaches in < 5 seconds, and stores 2 years of historical data queryable in < 10 seconds."

**Your design should include:**
```
[ Kafka ] → [ Consumer (Flink/Spark Streaming) ] → [ Alert Engine ]
                       ↓                                    ↓
              [ Delta Lake / S3 Parquet ]         [ PagerDuty / Slack ]
                       ↓
              [ ClickHouse (hot layer) ]
                       ↓
              [ Athena / Snowflake (cold layer) ]
```

**After 15 min — answer these probes:**

1. At 50,000 events/sec, how many Kafka partitions do you need?
   *(50,000 / 10,000 per consumer per second = 5 partitions minimum. Use 6 for rebalancing headroom.)*

2. How do you detect a 5-second breach window?
   *(Flink tumbling window of 5 seconds, keyed by server_id. Alert if MAX(cpu) > threshold within window.)*

3. How do you handle a server that goes silent (no events) — is that different from low CPU?
   *(Heartbeat check: if no event received for server_id in last 30 seconds → alert "missing data". Separate from CPU threshold.)*

4. How do you make the historical queries < 10 seconds on 2 years of data?
   *(Parquet columnar + partition by date, ZORDER by server_id. ClickHouse for recent 90 days. S3 + Athena for older data. Pre-aggregated materialized views.)*

---

## Day 40 Checklist

- [ ] LCS solution coded — recurrence written in English before code
- [ ] Unique Paths solved with 1D rolling array (not full grid)
- [ ] All 3 advanced window queries written and tested
- [ ] 15-min system design drawn on paper
- [ ] All 4 probes answered verbally
- [ ] Behavioral story told — specific, quantified, earned
