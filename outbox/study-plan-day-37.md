---
created: 2026-03-02
updated: 2026-03-02
summary: Day 37 — Two Pointers review, GROUPING SETS SQL, and a simulated phone screen exercise.
tags: [study-plan, day-37, week-6, two-pointers, grouping-sets, phone-screen-simulation]
---

# Day 37 — Two Pointers + GROUPING SETS + Phone Screen Simulation

**Theme:** Simulate a real phone screen today. The discomfort of simulation is exactly what makes the real thing easier.

---

## Daily Maintenance (30 min)

**LC — Two Pointers (3 problems, timed):**
- LC #167 Two Sum II (sorted array) (5 min)
- LC #15 3Sum (12 min — sort, outer loop, two-pointer inner, skip duplicates)
- LC #11 Container With Most Water (8 min — two pointers, move the shorter side)

After #15: write the duplicate-skip lines and explain why they're necessary.

**SQL — GROUPING SETS / ROLLUP / CUBE:**
```sql
-- Using the server_snapshot table (server_id, region, tier, avg_cpu):

-- 1. ROLLUP(region, tier): subtotals at region level AND grand total
-- 2. CUBE(region, tier): all combinations of region/tier subtotals
-- 3. Use GROUPING() function to label subtotal rows vs detail rows
-- 4. GROUPING SETS((region), (tier), ()): specific set of aggregations

-- For each: write the query, explain what rows it produces
```

---

## Phone Screen Simulation (40 min)

Run this as a timed exercise. Set a 30-minute timer. Close all notes. Use Gemini as the interviewer.

**Gemini prompt for this exercise:**
> "Conduct a 30-minute phone screen for a Senior Data Engineer role. Ask a 60-second intro, 2 coding questions (Easy and Medium), 1 SQL question, and 2 behavioral questions. Time each section strictly. I am the candidate. Begin."

**If no Gemini session available:** Do the self-drill version:

- 60-second intro (timed)
- LC #1 Two Sum (5 min — yes, again. Speed matters on screens.)
- LC #322 Coin Change (10 min — DP, 1D array)
- SQL: "Write a query that finds servers in the top 25% of CPU utilization per region" (8 min — use NTILE or PERCENT_RANK)
- Behavioral: "Tell me about a time you improved a data pipeline" (90 sec)
- Behavioral: "Why are you looking for a new role?" (60 sec)

---

## Post-Screen Reflection (if you had a real screen today)

Fill in immediately after any real recruiter/technical screen:

```
Date: ___  Company: ___  Interviewer: ___
Type: Recruiter screen / Technical screen / Final round

Questions asked:
  1. ___
  2. ___
  3. ___

Where I felt strong:
  ___

Where I stumbled:
  ___

New topic/pattern I hadn't seen before:
  ___

Impression I left:
  ___

Next step they said:
  ___  Timeline: ___

My follow-up action:
  Send thank-you within 24 hours: [ ] Yes
  Add to tracker: [ ] Yes
```

---

## Day 37 Checklist

- [ ] 3 Two Pointer problems — 3Sum duplicate skip lines written and explained
- [ ] All 4 GROUPING SETS queries written (ROLLUP, CUBE, GROUPING(), GROUPING SETS)
- [ ] 30-minute phone screen simulation completed (timed)
- [ ] Post-screen reflection completed (for any real screen, or for the simulation)
- [ ] Thank-you note sent within 24 hours of any real screen
