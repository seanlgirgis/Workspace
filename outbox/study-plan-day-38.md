---
created: 2026-03-02
updated: 2026-03-02
summary: Day 38 — 1D Dynamic Programming review, Snowflake-specific SQL, and post-screen gap analysis protocol.
tags: [study-plan, day-38, week-6, dynamic-programming, snowflake-sql, gap-analysis]
---

# Day 38 — 1D DP Review + Snowflake SQL + Post-Screen Gap Analysis

**Theme:** Every interview teaches you something. The post-screen protocol turns experience into improvement.

---

## Daily Maintenance (35 min)

**LC — 1D Dynamic Programming (3 problems, timed):**
- LC #70 Climbing Stairs (5 min — Fibonacci DP)
- LC #322 Coin Change (10 min — bottom-up: `dp[i] = min(dp[i - coin] + 1)`)
- LC #300 Longest Increasing Subsequence (12 min — O(n²) DP, O(n log n) with bisect)

After #322: explain the base case (`dp[0] = 0`) and why the array is initialized to `amount + 1`.

**SQL — Snowflake-Specific Patterns:**
```sql
-- If you have Snowflake access, run these. If not, write them knowing the syntax:

-- 1. Time Travel: query daily_metrics as it was 24 hours ago
SELECT * FROM daily_metrics AT (OFFSET => -86400);

-- 2. Stream check: does the server_changes stream have unconsumed data?
SELECT SYSTEM$STREAM_HAS_DATA('server_changes');

-- 3. Create and query a materialized view on server averages
CREATE MATERIALIZED VIEW mv_server_avg AS
SELECT server_id, AVG(avg_cpu) AS lifetime_avg FROM daily_metrics GROUP BY server_id;

-- 4. COPY INTO: load from S3 into Snowflake (syntax only — know the structure)
COPY INTO daily_metrics FROM @my_s3_stage/metrics/
FILE_FORMAT = (TYPE = 'PARQUET');
```

**Behavioral:** "What is the most important data engineering principle you work by?" (60 sec — have a real answer, not "data quality matters")

---

## Post-Screen Gap Analysis Protocol (30 min)

Use this after every technical interview or coding screen. Do not skip it — this is how you improve between interviews.

```
Post-Screen Gap Analysis
━━━━━━━━━━━━━━━━━━━━━━━━
Date: ___  Company: ___

CODING:
  What problems were asked? (reconstruct from memory)
    1. ___  Pattern: ___  My performance: Strong / OK / Weak
    2. ___  Pattern: ___  My performance: Strong / OK / Weak

  Where I got stuck:
    ___

  What I should have done:
    ___

  Study action: go to Day [N] material and redo [specific problem]

SQL:
  What was asked? ___
  My performance: Strong / OK / Weak
  Gap: ___
  Study action: ___

SYSTEM DESIGN (if asked):
  Topic: ___
  Gap: ___
  Study action: ___

BEHAVIORAL (if asked):
  Question: ___
  Gap: ___
  Study action: ___

FOLLOW-UP ACTIONS (do today or tomorrow):
  1. Practice [specific pattern] for 20 min — Day [N]
  2. ___
  3. ___
```

If you haven't had a real technical screen yet — use today to run this analysis on your Day 27 mock interview (the finance mock). Treat it as a real screen.

---

## Application Activities (15 min)

- Check tracker: any companies at 10+ days with no response → mark as "cold" and de-prioritize
- Identify 3 new target companies based on Week 5 research (Citi, Goldman, JPMorgan) — who are their competitors? Who recruits similar profiles?
- Send 2-3 new applications

---

## Day 38 Checklist

- [ ] 3 1D DP problems — Coin Change base case explained
- [ ] All 4 Snowflake SQL patterns written (Time Travel, Stream check, MV, COPY INTO)
- [ ] Behavioral question answered — real, specific principle, under 60 sec
- [ ] Post-screen gap analysis completed (real or mock-based)
- [ ] Follow-up study actions identified and scheduled
- [ ] Application tracker updated
