---
created: 2026-03-02
updated: 2026-03-02
summary: Day 34 — Greedy + Intervals review, data quality SQL, and a full behavioral mock session.
tags: [study-plan, day-34, week-5, greedy, intervals, behavioral-mock]
---

# Day 34 — Greedy + Intervals + Data Quality SQL + Behavioral Mock

**Theme:** Behavioral is half the interview. Today you run a real mock — all 5 stories under pressure, back to back.

---

## Daily Maintenance (35 min)

**LC — Greedy / Intervals (3 problems, timed):**
- LC #55 Jump Game (7 min — greedy: track max reachable index)
- LC #56 Merge Intervals (10 min — sort by start, extend end greedily)
- LC #435 Non-overlapping Intervals (8 min — greedy: sort by end, count removals)

After #56: explain why you sort by start and not by end.

**SQL — Data Quality Patterns:**
```sql
-- Write queries that detect each of these problems:
-- 1. Duplicate rows (same server_id + report_date appears more than once)
-- 2. Orphaned records (daily_metrics rows with no matching server in servers table)
-- 3. Out-of-range values (avg_cpu < 0 or > 100)
-- 4. Stale data (no report for a server in last 48 hours)
-- 5. Null rate per column (show columns with > 5% nulls)
```

**Behavioral:** Today you run all 5 stories back-to-back.

---

## Full Behavioral Mock Session (45 min)

Run this as a real mock. Set a timer. Speak out loud. Record yourself if possible.

**Rules:**
- No notes. No pausing to think for more than 10 seconds.
- Every story must be under 2 minutes.
- After each story, immediately answer the "hard press" question.

---

**Story 1 — Silent Failure:**
Tell it. (Timer: ___s)
Hard press: "What exactly was failing? How did YOU detect it? What metric or alert caught it?"

**Story 2 — Technical Complexity:**
Tell it. (Timer: ___s)
Hard press: "What specifically made it hard? What would you do differently?"

**Story 3 — Change Management:**
Tell it. (Timer: ___s)
Hard press: "Who pushed back? What did they say? How did you respond to their specific objection?"

**Story 4 — Production Incident:**
Tell it. (Timer: ___s)
Hard press: "What was the root cause? What process change prevents it from happening again?"

**Story 5 — Cross-Functional:**
Tell it. (Timer: ___s)
Hard press: "What was the fundamental misalignment? How did you bridge it?"

---

## Post-Mock Self-Scoring

For each story, rate:
- **Specific** (1-5): Does it have real names, numbers, systems?
- **Owned** (1-5): Is "I" the subject throughout?
- **Compelling** (1-5): Would you hire someone who told this story?

Stories scoring < 3 on any dimension → rewrite that story tonight.

---

## Day 34 Checklist

- [ ] 3 Greedy/Intervals problems timed — Merge Intervals explained verbally
- [ ] All 5 data quality SQL queries written and run
- [ ] Full 5-story behavioral mock completed (timed)
- [ ] Self-scores logged for each story
- [ ] Any story < 3/5 on any dimension → rewritten
- [ ] Application tracker updated (current status, next steps per company)
