---
created: 2026-03-02
updated: 2026-03-02
summary: Day 78 — Notice period and knowledge transfer. How to leave your current role professionally and completely.
tags: [study-plan, day-78, week-12, notice-period, knowledge-transfer, transition]
---

# Day 78 — Notice Period + Knowledge Transfer

**Theme:** How you leave is remembered. A clean handoff builds your professional reputation and closes your current chapter without loose ends.

---

## Daily Maintenance (20 min)

**LC — Binary Search (2 problems, timed):**
- LC #33 Search in Rotated Sorted Array (8 min — determine which half is sorted, check if target falls in it)
- LC #81 Search in Rotated Sorted Array II (6 min — same, but handle `nums[left] == nums[mid]` with `left++`)

**SQL — Deduplication from memory:**
Write the ROW_NUMBER deduplication pattern: given `daily_metrics` with possible duplicate `(server_id, report_date)` rows, keep only the most recently loaded row. Use `ROW_NUMBER() OVER (PARTITION BY server_id, report_date ORDER BY loaded_at DESC)`, then filter where `rn = 1`.

---

## Notice Period Session (50 min)

### The 2-Week Transition Plan

Don't wing it. Build a written transition plan on Day 1 of your notice period and share it with your manager. This signals professionalism and makes the conversation easier.

**Template:**

```
Transition Plan — [Your Name]
Last day: [date]

Open projects and status:
  Project A: ___
    Status: ___
    Handoff to: ___
    Outstanding items: ___
    Documentation location: ___

  Project B: ___
    Status: ___
    Handoff to: ___

Regular responsibilities:
  Daily/weekly task: ___  → Handoff to: ___
  On-call rotation: ___  → Notify: ___
  Recurring meeting: ___  → Transfer ownership to: ___

Documentation I'll write:
  [ ] Architecture decision records for ___
  [ ] README updates for ___
  [ ] Runbook for ___

People to brief:
  [ ] Direct manager
  [ ] Downstream teams who depend on my work
  [ ] Key internal stakeholders
```

---

### Documentation Priorities

The most valuable thing you can leave is documentation that a new person could use without asking questions. Focus on:

**1. "Why" documentation** — not what the code does (they can read it), but why it was designed that way. What constraints existed. What was tried and didn't work.

**2. Runbooks** — for any on-call or operational responsibility. What are the alerts? What do they mean? What are the remediation steps?

**3. Data dictionary entries** — for any tables, schemas, or pipelines you own. What does each field mean? What are the known quirks?

**4. Contact list** — who are the people (vendors, internal partners, downstream consumers) you talked to regularly? A name and context note is invaluable.

---

### The Right Attitude During Notice

**Do:**
- Stay fully engaged until your last day
- Over-communicate on handoffs
- Be honest in exit interviews (professional, not venting)
- Thank people individually — a short, specific note goes further than a group email

**Don't:**
- Start "mentally checking out" on Day 1 of notice
- Badmouth the company, team, or management — even if deserved
- Accept a counter-offer without thinking through why you wanted to leave in the first place
- Share details about your new role, salary, or company unless specifically asked by someone you trust

---

### The Exit Interview

HR will likely offer one. You can participate or decline — both are fine. If you participate:

**Focus on structural issues, not personal ones.** "The team would benefit from clearer oncall escalation paths" is actionable. "My manager was frustrating" is a grievance, not a contribution.

**Don't say anything you wouldn't want read back to you 5 years from now.** These conversations are often documented.

**The one thing worth saying honestly:** if there's a systemic issue that's causing turnover and you have specific evidence — say it once, clearly. It might actually help.

---

## Day 78 Checklist

- [ ] Both LC problems solved (Search Rotated II: handle duplicates with left++)
- [ ] Deduplication SQL written from memory (ROW_NUMBER + filter rn=1)
- [ ] Transition plan template reviewed — adapt for your actual responsibilities
- [ ] Documentation priorities identified (3 most important things to write)
- [ ] Notice period mindset set: stay engaged, over-communicate, leave professionally
