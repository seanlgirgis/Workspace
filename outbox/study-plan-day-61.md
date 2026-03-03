---
created: 2026-03-02
updated: 2026-03-02
summary: Day 61 — Company C deep prep day. Final company simulation prep of Week 9. LC maintenance on advanced patterns.
tags: [study-plan, day-61, week-9, company-prep, company-c, advanced-patterns]
---

# Day 61 — Company C: Preparation Day + Advanced Pattern Drill

**Theme:** Company C is your hardest target. Prepare accordingly.

---

## Daily Maintenance (35 min)

**LC — Advanced Patterns (2 problems, timed):**
- LC #269 Alien Dictionary (Hard — topological sort on char graph, Day 27)
- LC #297 Serialize/Deserialize Binary Tree (Hard — BFS with null markers)

Both of these appeared in your Week 4 mock. Speed should be better now.

**SQL — Complex multi-step query:**
```sql
-- End-to-end pipeline query:
-- 1. Build a CTE: servers with their 30-day CPU average
-- 2. Build a second CTE: servers with CPU trending up (today > 30d avg * 1.1)
-- 3. Join to server metadata (region, tier)
-- 4. Add a RANK() per region by current CPU
-- 5. Return top-5 per region by risk
```
Write this as a single query with 3 CTEs and window functions.

---

## Company C Full Preparation (55 min)

Company C = your hardest target (highest bar, most competitive, most desired).

### Deep Research (15 min)

This one gets extra research time. Find:
- A recent engineering blog post or conference talk from their data team
- A LinkedIn post from someone on their DE team about their stack/challenges
- Recent job postings — any new requirements compared to what you first saw?

### Extended Tech Stack Map (15 min)

```
Company C Stack               My Experience              Gap?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Tool 1] ──────────────→ [My exp] ─────────→ Yes / No
[Tool 2] ──────────────→ [My exp] ─────────→ Yes / No
[Tool 3] ──────────────→ [My exp] ─────────→ Yes / No
[Tool 4] ──────────────→ [My exp] ─────────→ Yes / No

Biggest gap for Company C: ___
How I'll address it in the interview: ___
```

### The Hard Question You'll Face (15 min)

At Company C, there is likely one question that will be hard for you.
Name it:
> "They will probably ask me about [X]. My answer will be: ___"

Write a full answer. Practice it out loud.

### Your Differentiated Value for Company C (10 min)

> "At Company C specifically, the unique value I bring that other candidates likely don't have is ___. Here's the story that proves it: ___"

---

## Day 61 Checklist

- [ ] LC #269 Alien Dictionary attempted (Hard — even partial counts)
- [ ] LC #297 Serialize/Deserialize faster than Day 27?
- [ ] Complex 3-CTE + window function SQL written and tested
- [ ] Company C extra research completed
- [ ] Tech stack map with gap column filled in
- [ ] "The hard question" written and practiced out loud
- [ ] Differentiated value for Company C articulated
- [ ] Ready for Day 62 simulation
