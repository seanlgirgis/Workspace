---
created: 2026-03-02
updated: 2026-03-02
summary: Day 31 — Binary Search review, complex JOIN practice, and deep-dive company research on Citi.
tags: [study-plan, day-31, week-5, binary-search, joins, citi-research]
---

# Day 31 — Binary Search + Complex JOINs + Citi Research

**Theme:** Company research is not optional at senior level. Today you understand Citi as a data engineering employer — before any recruiter contacts you.

---

## Daily Maintenance (35 min)

**LC — Binary Search (3 problems, timed):**
- LC #704 Binary Search (3 min — warm-up, should be automatic)
- LC #153 Find Minimum in Rotated Sorted Array (8 min)
- LC #33 Search in Rotated Sorted Array (10 min — two conditions in the if/elif)

For LC #153 and #33: say out loud which half is sorted before writing any code.

**SQL — Complex JOINs:**
```sql
-- 1. LEFT JOIN with anti-join pattern:
--    Find all servers that have NO entry in daily_metrics
--    for the last 3 days. Show server_id, last_seen_date (NULL if never).

-- 2. Self-join:
--    Find pairs of servers in the same region where the CPU gap
--    between them on the same day is > 30%.

-- 3. FULL OUTER JOIN:
--    Compare two snapshots (yesterday vs today) of server tiers.
--    Show servers that changed tier, were added, or were removed.
```

**Behavioral:** Speak Story 3 (change management) — timed.

---

## Company Research: Citi (45 min)

### What to Find

Search: "Citi data engineering", "Citi cloud migration", "Citi technology strategy", "Citi data platform"

Fill in from your research:

```
Citi DE Research Template
━━━━━━━━━━━━━━━━━━━━━━━━
What Citi uses for data storage/warehouse:
  Likely: ___

What Citi uses for orchestration:
  Likely: ___

What Citi is publicly doing in data/cloud:
  Reference: ___ (source URL)

Citi's tech transformation context:
  (e.g., consent orders, cloud migration mandate, Modernizing Finance)

Key DE roles at Citi right now (LinkedIn search):
  Title: ___  Location: ___  Posted: ___

Common tech stack in Citi DE JDs:
  ___

My angle for Citi:
  "My [APM/capacity planning] experience maps to their [___] problem
   because ___"

Questions I'd ask a Citi interviewer:
  1. ___
  2. ___
  3. ___
```

### Citi-Specific Technical Context

**Regulatory environment:** Citi has been under regulatory consent orders — this means data governance, audit trails, and data quality are existential priorities, not nice-to-haves.

**Your angle:** Your APM background means you understand reliability-critical infrastructure. Your capacity planning experience means you think at scale. Your data quality work (Great Expectations, dbt tests, control totals) maps directly to their compliance requirements.

**Frame for Citi:** "I've worked in environments where data errors have real operational consequences. That's the same stakes as financial data."

---

## Day 31 Checklist

- [ ] 3 Binary Search problems timed — #33 solved correctly on first attempt
- [ ] All 3 JOIN queries written and run in DuckDB
- [ ] Story 3 spoken and timed (< 90 sec)
- [ ] Citi research template filled in
- [ ] Have 3 Citi-specific interview questions ready
- [ ] Applied to any open Citi DE roles found during research
