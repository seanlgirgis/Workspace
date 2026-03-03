---
created: 2026-03-02
updated: 2026-03-02
summary: Day 29 — Week 5 opens. Application launch day. LC maintenance begins with HashMap/Two-Sum variants. SQL window function review.
tags: [study-plan, day-29, week-5, activation, hashmap, window-functions]
---

# Day 29 — Application Launch + HashMap Review + Window Functions

**Theme:** Study phase is over. Execution phase begins. Today you send the first applications AND maintain technical sharpness. Both matter.

---

## Daily Maintenance (35 min)

**LC — HashMap / Two-Sum Pattern (3 problems, timed):**
- LC #1 Two Sum (5 min — if it takes more than 3 min, something is wrong)
- LC #49 Group Anagrams (8 min — sort or count characters as key)
- LC #560 Subarray Sum Equals K (10 min — prefix sum + HashMap, O(n))

**SQL — Window Functions Sprint:**
Write from scratch, no notes:
```sql
-- 1. Rank servers by avg_cpu within each region (DENSE_RANK)
-- 2. 7-day trailing average CPU per server (ROWS BETWEEN)
-- 3. Difference from previous day's CPU per server (LAG)
```
Run all three in DuckDB against your telemetry dataset.

**Behavioral:** Speak Story 1 (silent failure) — timed. Must be under 90 seconds.

---

## Application Launch (60 min)

### Today's Goal: 5 applications sent

**Priority order:**
1. Firms with referrals or warm contacts (highest conversion)
2. Firms where you match ≥ 80% of the JD requirements
3. Reach firms (title bump or unfamiliar domain)

**For each application:**
- Tailor the first line of your cover letter/intro to the specific firm
- Match resume bullets to JD language where honest
- Log it in your tracker (Day 28 template)

### Resume Checklist (final pass before submitting)
- [ ] Top bullet: quantified APM impact (X servers, $Y savings, Z% improvement)
- [ ] Capacity planning described with scale (6,000 servers, not "large environment")
- [ ] Python, SQL, Spark, Airflow, Kafka all visible in skills section
- [ ] No more than 1 page (senior roles: 1.5 pages maximum)
- [ ] No "responsible for" — every bullet starts with an action verb
- [ ] Each bullet answers: what did you do, at what scale, with what result?

### LinkedIn — One-Time Setup
- [ ] "Open to Work" set to recruiter-only visibility
- [ ] Headline updated: "Senior Data Engineer | Capacity Planning | APM | Python · SQL · Spark"
- [ ] About section: 3 sentences — who you are, what you've built, what you're looking for
- [ ] Skills section: add Python, SQL, Apache Spark, Kafka, Airflow, dbt, AWS, Snowflake

---

## Outreach (20 min)

Identify 5 people in your network who work at target firms or know hiring managers there. Send one message each:

> "Hi [Name], I hope you're well. I'm actively exploring Senior DE opportunities — particularly in financial services and cloud infrastructure. If you know of anything relevant at [Firm] or elsewhere, I'd genuinely appreciate a connection. Happy to catch up either way."

Keep it short. No attachments. No formal cover letters. Just a conversation starter.

---

## Day 29 Checklist

- [ ] LC: 3 HashMap problems coded, timed, no errors
- [ ] SQL: 3 window function queries written and run in DuckDB
- [ ] Story 1 spoken and timed (< 90 sec)
- [ ] 5 applications submitted and logged in tracker
- [ ] LinkedIn updated
- [ ] 5 outreach messages sent
- [ ] Application tracker created (if not already done from Day 28)
