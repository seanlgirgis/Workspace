---
created: 2026-03-02
updated: 2026-03-02
summary: Day 49 — Week 7 close. Greedy algorithm review, query plan analysis, pipeline update, and Week 8 planning.
tags: [study-plan, day-49, week-7, greedy, query-plans, weekly-review]
---

# Day 49 — Greedy Review + Query Plans + Week 7 Close

**Theme:** Seven weeks done. You've been in active interviews. The data from those interviews is now your most valuable resource.

---

## Daily Maintenance (35 min)

**LC — Greedy (3 problems, timed):**
- LC #55 Jump Game (6 min — track max reachable, return True if we ever reach the end)
- LC #134 Gas Station (8 min — reset start when curr < 0; check total >= 0)
- LC #45 Jump Game II (10 min — farthest + current_end pattern, from Day 27)

After #134: explain in one sentence why we only need to check total >= 0 at the end.

**SQL — EXPLAIN and Query Plans:**
```sql
-- In DuckDB, use EXPLAIN or EXPLAIN ANALYZE:
EXPLAIN SELECT s.server_id, AVG(m.avg_cpu)
FROM servers s
JOIN daily_metrics m ON s.server_id = m.server_id
WHERE m.report_date >= '2026-01-01'
GROUP BY s.server_id;

-- Look at the output:
-- What is the join type? (HASH JOIN vs NESTED LOOP)
-- Where does the filter on report_date appear? (before or after join?)
-- What would you add to make this faster?
```

**Behavioral:** "How do you prioritize when you have more work than time?"

---

## Week 7 Close — Pipeline Review (25 min)

```
Week 7 Pipeline Status
━━━━━━━━━━━━━━━━━━━━━━
Technical interviews completed: ___
Technical interviews passed (advanced to next round): ___
Technical interviews where feedback is pending: ___
Rejections this week: ___  (note the stage — early rejection = different diagnosis than final round)

Real interview questions collected (add any new ones to your SR rotation):
  1. ___
  2. ___
  3. ___

Companies in final rounds: ___
Expected timeline for next-step feedback: ___

My biggest performance insight from this week's interviews:
  ___

My adjusted confidence level by domain (update from Day 28):
  LC Medium: ___ / 5
  SQL complex: ___ / 5
  System design: ___ / 5
  Behavioral: ___ / 5
```

**Diagnosis by rejection stage:**
- **Recruiter screen rejection:** Resume/branding mismatch or over/under-qualified. Fix: revise resume, target differently.
- **Coding screen rejection:** Specific pattern weakness. Fix: gap drill that pattern.
- **System design rejection:** Missing depth on a specific component. Fix: re-read that architecture topic + draw design from scratch daily.
- **Final round rejection:** Behavioral/culture or senior judgment signals. Fix: story depth + leadership framing.

**Week 8 focus (set these now):**
```
LC pattern to drill: ___
SQL topic to drill: ___
Architecture concept to deepen: ___
Behavioral to strengthen: ___
```

---

## Day 49 Checklist

- [ ] All 3 greedy problems coded — Jump Game II from memory
- [ ] EXPLAIN output read and explained (join type, filter position)
- [ ] Behavioral — prioritization answered with a real example
- [ ] Week 7 pipeline review completed
- [ ] Week 8 focus areas set
- [ ] Weekend: rest and process. No grinding. One read of your behavioral stories.
