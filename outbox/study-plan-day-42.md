---
created: 2026-03-02
updated: 2026-03-02
summary: Day 42 — Week 6 close. Graphs and topological sort review, query optimization deep dive, pipeline review.
tags: [study-plan, day-42, week-6, graphs, topological-sort, query-optimization, weekly-review]
---

# Day 42 — Graphs + Topological Sort + Query Optimization + Week 6 Close

**Theme:** Six weeks done. The interview pipeline is active. Today's close determines Week 7's focus.

---

## Daily Maintenance (35 min)

**LC — Graphs + Topological Sort (2 problems, timed):**
- LC #207 Course Schedule (10 min — build adjacency list, DFS with states: 0=unvisited, 1=visiting, 2=done; cycle = True if visiting node reached again)
- LC #210 Course Schedule II (12 min — same DFS, but append to result in post-order; return `result[::-1]`)

After #207: write the 3-state DFS cycle detection from memory.

**SQL — Query Optimization Deep Dive:**
```sql
-- Given this slow query, identify all performance problems and fix them:

SELECT s.server_id, s.region,
       AVG(m.avg_cpu) as avg_cpu,
       COUNT(*) as days
FROM servers s, daily_metrics m
WHERE s.server_id = m.server_id
AND m.report_date BETWEEN '2026-01-01' AND '2026-03-01'
AND s.tier = 'production'
AND avg_cpu > (SELECT AVG(avg_cpu) FROM daily_metrics)
GROUP BY s.server_id, s.region
HAVING COUNT(*) > 10
ORDER BY avg_cpu DESC;

-- Problems to find and fix:
-- 1. Old-style comma join (implicit cross join risk)
-- 2. Correlated scalar subquery in WHERE (runs N times)
-- 3. Missing index hints / partition filter
-- 4. Ordering on non-aliased column
```

**Behavioral:** "What's the biggest mistake you made in your career? What did you learn?"

---

## Week 6 Close — Pipeline Review (25 min)

```
Week 6 Pipeline Update
━━━━━━━━━━━━━━━━━━━━━
Applications sent (cumulative): ___
Recruiter screens completed: ___
Technical screens completed: ___
Final rounds: ___
Offers: ___

Active processes (company + stage + next step + deadline):
  1. ___ → stage: ___  next: ___  deadline: ___
  2. ___ → stage: ___  next: ___  deadline: ___
  3. ___ → stage: ___  next: ___  deadline: ___

Interview learnings this week (new questions/patterns seen):
  ___

Patterns that came up in real interviews:
  ___  (add to SR rotation if new)

Week 7 focus areas (based on gap analysis):
  LC pattern: ___
  SQL topic: ___
  Architecture: ___
  Behavioral: ___
```

**Week 7 plan:** The technical interview loop intensifies. The goal for Week 7 is to get at least 2 technical interviews on the calendar and close at least 1 of them into a final round.

---

## Day 42 Checklist

- [ ] Course Schedule II coded — post-order append, reversed result
- [ ] 3-state DFS written from memory
- [ ] Query optimization: identified all 4 problems, rewrote the query
- [ ] Behavioral story told — real mistake, real lesson, no deflection
- [ ] Week 6 pipeline review completed and logged
- [ ] Week 7 focus areas identified
- [ ] Weekend: rest. One light review of behavioral stories.
