---
created: 2026-03-02
updated: 2026-03-02
summary: Day 46 — Persistent gap drill session 1. Focus on whichever LC pattern and SQL topic most recently failed in a real interview.
tags: [study-plan, day-46, week-7, gap-drill, persistent-gaps]
---

# Day 46 — Persistent Gap Drill 1

**Theme:** Persistent gaps don't close by reading. They close by doing — under pressure, without notes, repeatedly.

---

## Gap Drill Protocol

Identify your top 2 gaps from your post-interview reflections (Days 38/45). If you haven't had a real interview yet, use your Day 28 self-assessment scores.

Fill in before starting:
```
Gap 1 — LC Pattern: ___
  Why it's a gap: ___
  Study plan reference: Day ___

Gap 2 — SQL/Tech Topic: ___
  Why it's a gap: ___
  Study plan reference: Day ___
```

---

## Gap 1 Drill — LC Pattern (50 min)

**Do not look at solutions until after you've attempted each problem.**

Pick 3 problems from your gap pattern (if unsure which, use these defaults):

**Default: Dynamic Programming (most common LC gap)**
- LC #746 Min Cost Climbing Stairs (8 min — DP, two base cases)
- LC #198 House Robber (8 min — `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`)
- LC #213 House Robber II (12 min — circular: solve linear twice, skip first or last)

**Default: Graph BFS (second most common)**
- LC #994 Rotting Oranges (12 min — multi-source BFS, track time and remaining fresh)
- LC #1091 Shortest Path in Binary Matrix (10 min — BFS from [0,0] to [n-1,n-1], 8 directions)
- LC #130 Surrounded Regions (10 min — BFS/DFS from borders, mark safe, flip remaining)

**After each problem:** time check. If you exceeded target time by more than 50% → flag as "needs more reps."

---

## Gap 2 Drill — SQL / Architecture (30 min)

**Pick the topic from your gap and write 3 queries from scratch:**

**Default: Window Functions (most common SQL gap)**
```sql
-- Write from memory, no notes:
-- 1. RANK() + DENSE_RANK() side by side, partitioned by region
-- 2. Running total that resets at each new partition (ROWS BETWEEN UNBOUNDED PRECEDING)
-- 3. Moving 7-day average with ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
-- Run all three. Compare to expected output.
```

**Default: System Architecture (if the gap is architectural)**
- Draw the Kafka + Flink + Delta Lake streaming pipeline from scratch (10 min)
- Annotate: what provides exactly-once? Where does the checkpoint go? Where is the sink?
- Compare to your Day 22 / Day 39 notes

---

## Behavioral Sprint (15 min)

Pick 2 behavioral questions that felt weak in recent interviews (or from this list if no interview yet):

1. "What's the most important thing you've learned about working in data at scale?"
2. "Tell me about a time you had to push back on a technical decision."

Answer both out loud. Time each. Force yourself to be concrete — no abstract principles, only stories.

---

## Day 46 Checklist

- [ ] Gap 1 identified and filled in (LC pattern)
- [ ] Gap 2 identified and filled in (SQL/tech topic)
- [ ] All 3 Gap 1 problems attempted (timed, no solutions first)
- [ ] All 3 Gap 2 queries written and run
- [ ] Both behavioral questions answered out loud, specifically
- [ ] Any problems still weak → scheduled for repeat on Day 48 or 50
