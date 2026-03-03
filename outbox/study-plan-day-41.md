---
created: 2026-03-02
updated: 2026-03-02
summary: Day 41 — Tries review, JSON SQL patterns, and targeted prep for any scheduled technical interview this week.
tags: [study-plan, day-41, week-6, tries, json-sql, technical-interview-prep]
---

# Day 41 — Tries Review + JSON SQL + Technical Interview Prep

**Theme:** If you have a technical interview this week, today is your focused preparation day for it. If not, this is pure maintenance.

---

## Daily Maintenance (35 min)

**LC — Tries (2 problems, timed):**
- LC #208 Implement Trie (10 min — `children = {}`, `is_end = False`, insert/search/startsWith)
- LC #211 Design Add and Search Words (12 min — DFS for `.` wildcard)

Write TrieNode from memory:
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
```
This should be automatic. If it isn't — repeat it 5 times.

**SQL — JSON in DuckDB:**
```sql
-- Given raw JSON telemetry events (from Day 15 schema):

-- 1. Extract nested field (disk.read_iops)
-- 2. Unnest the tags array — one row per tag
-- 3. Aggregate: servers with 'production' tag, avg CPU over 80
-- 4. Build a pivot: columns for cpu, mem, read_iops from one JSON column
```
Run all four. Time yourself: target < 15 minutes for all four.

**Behavioral:** "Tell me about a time you had to make a decision with incomplete information."

---

## Technical Interview Day Prep (if you have one this week)

Fill this in for the specific company:

```
Company: ___  Date: ___  Format: ___  Duration: ___

Known topics (from JD or recruiter call):
  LC pattern: ___
  SQL topic: ___
  System design: ___

My 3 most relevant stories for this company:
  Story A: ___  → maps to their [problem/value]
  Story B: ___  → maps to their [problem/value]
  Story C: ___  → maps to their [problem/value]

My APM story for this company:
  "At [COMPANY], I built [SYSTEM] for [SCALE] servers.
   The specific challenge that applies here is [BRIDGE TO JD]."

Tech stack I know they use (from research):
  ___

Last-minute review (today):
  1. Re-read Day [N] for [topic most likely to appear]
  2. Re-read Day [M] for [second topic]
  3. Run through behavioral stories × 3 tonight

Day-of plan:
  - No new studying the morning of the interview
  - Review your 5 stories over coffee
  - 30 minutes before: write 2 easy LC problems on paper to warm up
```

---

## If No Interview This Week

Use the 40 minutes for these targeted drills:

**Gap drill (pick your weakest from Day 28 self-assessment):**
- If LC gap: code 3 problems from that pattern, timed, no notes
- If SQL gap: write 3 queries from that topic, run in DuckDB
- If architecture gap: draw the system design for that topic from scratch in 10 minutes

---

## Day 41 Checklist

- [ ] TrieNode written from memory (both structure and all 3 methods)
- [ ] LC #211 wildcard search coded correctly — DFS for `.` explained
- [ ] All 4 JSON SQL queries run in DuckDB
- [ ] Behavioral story answered — decision with incomplete info
- [ ] Technical interview prep form filled in (or gap drill completed if no interview)
