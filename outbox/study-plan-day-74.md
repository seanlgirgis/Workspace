---
created: 2026-03-02
updated: 2026-03-02
summary: Day 74 — Reference check preparation. Who to ask, what they'll be asked, and how to brief them.
tags: [study-plan, day-74, week-11, references, reference-check]
---

# Day 74 — Reference Check Prep

**Theme:** Reference checks happen after an offer, but the preparation happens before. A poorly chosen or unprepared reference can slow or derail an offer. A well-chosen, briefed reference reinforces everything you said in the interview.

---

## Daily Maintenance (25 min)

**LC — Backtracking (2 problems, timed):**
- LC #39 Combination Sum (8 min — sort, recurse with start index, allow repeat use, append copy when sum matches)
- LC #131 Palindrome Partitioning (10 min — backtrack with `is_palindrome(s, l, r)` helper, append partition copy at base case)

**SQL — FILTER clause from memory:**
Write a query that computes, in a single pass over `daily_metrics`:
- Count of all rows
- Count of rows where `avg_cpu > 80`
- Count of rows where `avg_cpu > 95`

Use `COUNT(*) FILTER (WHERE ...)` — no subqueries, no CASE WHEN.

---

## Reference Check Session (45 min)

### Who to Choose

**Strong reference:** Someone who has directly managed or worked alongside you on technical work, can speak to your impact with specifics, and is enthusiastic — not just willing.

**Avoid:**
- Anyone who you think will give a "warm but vague" reference ("Sean is great to work with")
- Anyone from a job where you left on ambiguous terms
- Peers who can't speak to your leadership or technical depth

**Ideal reference profile:**
- A former manager (primary)
- A senior technical peer or tech lead who observed your work closely (secondary)
- An internal stakeholder from another team who depended on your work (optional third)

---

### How to Ask

Don't ask: "Can you be a reference?"

Ask: "I'm in the final stages of a process at [Company]. The role is [title], focused on [brief description]. I think you've seen my work closely enough to speak to [specific area]. Would you be comfortable being a strong reference for this role?"

The word "strong" is intentional. It gives them an out if they're not comfortable, and it signals what you need.

---

### How to Brief Your Reference

After they agree, send a brief email (not a 10-paragraph briefing):

```
Subject: Reference call prep — [Company Name]

Hi [Name],

Thank you for agreeing to be a reference. Here's a quick brief:

Company: [Name]
Role: Senior Data Engineer / Capacity Planning Engineer
Likely call focus: [2-3 things they may ask — see below]

What I'd love for you to speak to:
- [Specific project or impact you worked on together]
- [A quality or skill you want highlighted]
- [Any measurable outcome from your work together]

Things I've emphasized in interviews:
- [APM background and monitoring depth]
- [Finance data pipeline experience]
- [System design at scale]

The recruiter is [Name] from [Company]. They may call or email.

Thank you again — really appreciate it.
```

Keep it short. Give them the ammunition to be specific. Don't script them — just remind them of the facts.

---

### What References Are Actually Asked

Standard reference check questions:
1. "How long did you work with [candidate] and in what capacity?"
2. "What were their greatest strengths?"
3. "What areas did they need to develop?"
4. "Would you hire them again?" ← this is the one that matters most
5. "Is there anything that would concern you about them in a senior engineering role?"

Finance-specific additions:
- "How did they handle deadlines and pressure?"
- "Did they take ownership, or did they need to be managed closely?"
- "How did they communicate with non-technical stakeholders?"

---

### Preparing for the "Weakness" Question

Your references will be asked about your development areas. Brief them on a real, non-fatal weakness that you've worked on — so their answer is consistent with what you told the company.

If you said in the interview: "I've been working on improving how I communicate timelines to stakeholders when projects get complicated" — your reference should be able to say something like: "Sean has been proactive about improving his stakeholder communication — he's grown a lot in that area."

Misaligned weakness answers are one of the few ways references can hurt you.

---

## Day 74 Checklist

- [ ] Both LC problems solved (Palindrome Partitioning: palindrome check helper + backtrack)
- [ ] FILTER clause query written from memory (3 counts in one pass)
- [ ] 3 references identified and ranked
- [ ] References asked — using the "strong reference" framing
- [ ] Brief email drafted for each reference who agreed
- [ ] "Weakness" answer aligned between what you told the company and what references may say
