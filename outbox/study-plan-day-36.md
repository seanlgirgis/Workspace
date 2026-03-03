---
created: 2026-03-02
updated: 2026-03-02
summary: Day 36 — Pre-screen preparation template, DFS on trees review, Date/Time SQL patterns.
tags: [study-plan, day-36, week-6, dfs-trees, date-time-sql, phone-screen-prep]
---

# Day 36 — DFS Trees + Date/Time SQL + Pre-Screen Preparation

**Theme:** Week 6 is interview execution. Every day has a pre-screen component — because a screen could land any day now.

---

## Daily Maintenance (35 min)

**LC — DFS on Trees (3 problems, timed):**
- LC #104 Maximum Depth of Binary Tree (4 min — 2-line recursive solution)
- LC #112 Path Sum (8 min — DFS, pass `remaining - node.val`, check leaf)
- LC #236 Lowest Common Ancestor of a Binary Tree (10 min — return node if found left or right)

After #236: trace through the recursion on paper with a 5-node tree.

**SQL — Date/Time Patterns:**
```sql
-- Write all of these from scratch:
-- 1. All servers that haven't reported in 7+ days (CURRENT_DATE - 7)
-- 2. For each server, number of days since last report
-- 3. Servers that reported on BOTH last Monday and last Friday
-- 4. Rolling 30-day report count per server (window function)
-- 5. Gap detection: find (server_id, date) pairs where there is a gap
--    (missing report_date between first and last report for that server)
```

**Behavioral:** "Walk me through your background in 60 seconds." Practice this. It's the first thing every screen starts with.

---

## Pre-Screen Preparation Template (30 min)

When a recruiter screen lands, use this template the day before:

```
Company: _______________
Screen date/time: ___
Recruiter name: ___

What I know about this company:
  Size: ___  Industry: ___
  Why I'm interested: ___
  One thing they've done recently (news, blog, product): ___

What they're looking for (from JD):
  Must-have: ___
  Nice-to-have: ___
  Their language: ___  (use their words back to them)

My 60-second intro (customized):
  "I'm a Senior Data Engineer with [X] years of experience,
   most recently [ROLE] where I [KEY ACHIEVEMENT at SCALE].
   I'm looking for [WHAT THIS ROLE OFFERS] — specifically
   [SOMETHING COMPANY-SPECIFIC]. That's why I'm excited
   about this opportunity."

My answer to "Why this company?":
  ___

My answer to "What are your salary expectations?":
  "I'm targeting [RANGE] in total compensation. I understand
   that includes base and bonus — what does the structure
   look like here?"

3 questions I'll ask:
  1. ___
  2. ___
  3. ___

My ask at the end:
  "What are the next steps in the process?"
```

Fill this in today for any upcoming screens. If no screens yet — fill it in for your top target company anyway (practice the habit).

---

## Applications Today (15 min)

- 3-5 new applications
- Check tracker — any new responses to act on?
- If a recruiter emailed you this week, respond within 24 hours with enthusiasm and a proposed time slot

---

## Day 36 Checklist

- [ ] 3 DFS Tree problems coded and timed — LCA traced on paper
- [ ] All 5 Date/Time SQL queries written and run
- [ ] 60-second intro rehearsed and timed
- [ ] Pre-screen template filled in for at least one company
- [ ] 3-5 new applications submitted
- [ ] Any recruiter emails responded to promptly
