---
created: 2026-03-02
updated: 2026-03-02
summary: Day 45 — Post-interview reflection protocol, monotonic stack review, string functions SQL.
tags: [study-plan, day-45, week-7, monotonic-stack, string-sql, post-interview-reflection]
---

# Day 45 — Monotonic Stack + String SQL + Post-Interview Reflection

**Theme:** The day after an interview is as important as the day before. Extraction and improvement come from deliberate reflection, not passive memory.

---

## Daily Maintenance (30 min)

**LC — Monotonic Stack (2 problems, timed):**
- LC #739 Daily Temperatures (8 min — monotonic decreasing, indices)
- LC #84 Largest Rectangle in Histogram (12 min — sentinel `[0]` appended, width = `i - stack[-1] - 1`)

After #84: walk through the trace for input `[2,1,5,6,2,3]`.

**SQL — String Functions:**
```sql
-- Using the raw_servers table (hostname, tags, version):

-- 1. Extract server_id from hostname: SPLIT_PART + LOWER
-- 2. Extract environment (prod/staging/dev) from hostname
-- 3. Check if version is a beta (contains '-beta' or '-rc')
-- 4. Count servers per major version (SPLIT_PART + CAST)
-- 5. Find hostnames that don't match the expected pattern SRV-NNN.*
```

**Behavioral:** Any question that stumped you in a recent interview — answer it now, correctly, out loud.

---

## Post-Interview Reflection Protocol (40 min)

Complete within 24 hours of every technical interview.

### Part 1 — Reconstruct (15 min)

Write down every question asked, as precisely as you remember:

```
Interview: ___ (company, date, round)
Interviewer(s): ___

Coding Q1: [reconstruct the problem statement]
  My approach: ___
  Did it work? ___
  Time I took: ___
  Interviewer reaction: ___

Coding Q2: [reconstruct]
  My approach: ___
  Did it work? ___

SQL: [reconstruct]
  My approach: ___
  Score: ___

System Design: [topic]
  My design: ___
  Probes asked: ___
  Where I was strong: ___
  Where I struggled: ___

Behavioral questions asked:
  1. ___
  2. ___
  Strength of my answers: ___
```

### Part 2 — Diagnosis (10 min)

For each question you stumbled on:
- What was the core pattern or concept?
- Which day of the study plan covers it?
- Was it a recall failure (I knew this but blanked) or a knowledge gap (I never learned this)?

```
Recall failure → do 3 problems of that pattern today (timed)
Knowledge gap  → read the study plan section + code 2 examples
```

### Part 3 — Thank-You Note (5 min)

Send within 24 hours of the interview ending:

> Subject: Thank you — Senior Data Engineer Interview

> Hi [Name],
>
> Thank you for taking the time to interview me today. I genuinely enjoyed the [problem on X / discussion of Y] — it gave me a better sense of the engineering challenges your team is working through.
>
> I remain very interested in the role and the team. Please let me know if there's any additional information I can provide.
>
> Best,
> Sean

### Part 4 — Adjust (10 min)

Based on what you learned:
- Update your study plan priorities for the rest of the week
- If a new pattern appeared: add it to your LC rotation
- If a technology question appeared that you didn't expect: add it to the company research file

---

## Day 45 Checklist

- [ ] Both monotonic stack problems coded — histogram trace walked through
- [ ] All 5 string SQL queries written and run
- [ ] Behavioral question (stumped one from interview) answered correctly
- [ ] Post-interview reflection Part 1 completed (all questions reconstructed)
- [ ] Post-interview reflection Part 2 completed (gaps diagnosed)
- [ ] Thank-you note sent within 24 hours
- [ ] Study plan priorities adjusted for remainder of week
