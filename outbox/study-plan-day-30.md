---
created: 2026-03-02
updated: 2026-03-02
summary: Day 30 — Sliding Window review, CTE practice, application follow-up, and a 30-day milestone reflection.
tags: [study-plan, day-30, week-5, sliding-window, cte, applications]
---

# Day 30 — Sliding Window Review + CTEs + Application Follow-Up

**Theme:** 30 days in. One month of structured work. Today is both maintenance and milestone.

---

## Daily Maintenance (35 min)

**LC — Sliding Window (3 problems, timed):**
- LC #3 Longest Substring Without Repeating Characters (8 min)
- LC #76 Minimum Window Substring (12 min — hard but you've seen it)
- LC #424 Longest Repeating Character Replacement (10 min — `count - max_count > k` is the key)

For each: write the solution, state the time complexity out loud, identify the window shrink condition.

**SQL — CTEs (non-recursive and recursive):**
```sql
-- 1. Write a 3-step CTE pipeline:
--    Step 1: filter servers with avg_cpu > 80
--    Step 2: add a 7d trailing avg
--    Step 3: flag servers where current > trailing avg * 1.1

-- 2. Write a recursive CTE that walks the infra_hierarchy table
--    (from Day 22) and outputs every node with its full path
```

**Behavioral:** Speak Story 2 (technical complexity) — timed. Under 90 seconds.

---

## 30-Day Milestone Reflection (15 min)

Answer these honestly in writing (3 sentences each, no more):

**What is your strongest domain right now?**

**What is your most persistent weak spot?**

**What habit from the study plan should you carry forward permanently?**

**What is your interview pipeline status today?**
- Applications sent: ___
- Recruiter screens scheduled: ___
- Technical interviews scheduled: ___
- Offers: ___

---

## Application Activities (30 min)

**Follow up:** Any application sent more than 5 business days ago with no response → send one polite follow-up email to the recruiter (if you have their contact):
> "Hi [Name], I wanted to briefly follow up on my application for the Senior Data Engineer role. I remain very interested and happy to answer any questions. Thanks for your time."

**New applications today:** 3-5 more. Focus on roles where you haven't applied yet.

**Recruiter prep:** If you have a recruiter screen this week, prepare:
- Your 60-second intro (name, background, what you're looking for)
- Your answer to "What are you looking for in your next role?"
- Your answer to "What's your current/expected compensation?"

---

## Day 30 Checklist

- [ ] 3 Sliding Window problems coded and timed
- [ ] CTE pipeline query written (3-step) and run
- [ ] Recursive CTE hierarchy query written and run
- [ ] 30-day milestone reflection written
- [ ] Pipeline status logged
- [ ] Follow-ups sent (if applicable)
- [ ] 3-5 new applications submitted
