---
created: 2026-03-02
updated: 2026-03-02
summary: Day 87 — Domain deepening. Targeted reading on the technical area you'll own in the new role.
tags: [study-plan, day-87, week-13, domain-deepening, technical-prep, apm, capacity-planning]
---

# Day 87 — Domain Deepening

**Theme:** You have a few days before you start. Spend 2 hours on the one technical area where you'll be least covered by your existing knowledge. Not broad survey — deep on one thing.

---

## Daily Maintenance (15 min)

**LC — Hard problem (optional, timed):**
If you want a final challenge: LC #42 Trapping Rain Water or LC #76 Minimum Window Substring. Otherwise: skip and use the full session for domain deepening.

**SQL — Finance SQL spoken:**
Pick any 2 finance queries from Days 48 or 69. Don't write them — explain them out loud, narrating the business problem, the data model, and the query structure. Verbal fluency is the final form of SQL mastery.

---

## Domain Deepening Session (90 min)

### How to Spend This Session

You're choosing one of the following, based on what your new role most needs:

---

**Option A — If your role is primarily Capacity Planning:**

Read and annotate: [Google's Site Reliability Engineering book, Chapter 17: Testing for Reliability](https://sre.google/sre-book/testing-reliability/) and Chapter 18: Software Engineering in SRE.

Then write answers to:
1. What is the Google SRE definition of reliability? How does it connect to capacity planning?
2. What is the difference between load testing and stress testing? When would you use each?
3. What is a toil reduction strategy, and how does it apply to a capacity planning automation workflow?

**Option B — If your role is primarily Data Engineering (streaming):**

Deep-read on Kafka consumer groups and offset management. Write answers to:
1. What happens if a consumer group falls too far behind? What are the recovery options?
2. What is the difference between `earliest` and `latest` `auto.offset.reset`? When does each matter?
3. If you have 12 partitions and 3 consumer instances, how does partition assignment work? What if one consumer dies?

**Option C — If your role is primarily Data Engineering (batch / finance):**

Deep-read on data lineage in a financial services context. Write answers to:
1. What does "field-level lineage" mean, and why does it matter for regulatory reporting?
2. What is BCBS 239, and what does it require of a bank's data architecture?
3. What are the 3 most common lineage collection approaches (push/pull/hybrid), and what are their trade-offs?

**Option D — If you're still searching (not yet accepted):**

Pick a company in your active pipeline. Spend the full session on their tech blog:
- Read 3 engineering posts
- Write a 1-paragraph summary of what engineering challenges they've solved and how
- Write 2 informed questions you could ask in a final round

---

### After Deep Reading — Write, Don't Just Read

Reading without writing is watching someone else exercise. Write:
- A 3-bullet summary of the most important things you learned
- 1 specific thing you'll do differently in your first month because of this reading
- 1 question this reading raised that you want to answer in your first week on the job

---

## Day 87 Checklist

- [ ] SQL spoken fluency: 2 finance queries explained out loud (no writing)
- [ ] Domain chosen (A, B, C, or D)
- [ ] 90-minute deep session completed
- [ ] 3-bullet summary written
- [ ] 1 specific application to first month written
- [ ] 1 follow-up question for your first week written
