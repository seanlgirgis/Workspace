---
created: 2026-03-02
updated: 2026-03-02
summary: Day 65 — Leadership system design. Design for a VP-level audience. LC maintenance on 2D DP.
tags: [study-plan, day-65, week-10, leadership-design, vp-audience, 2d-dp]
---

# Day 65 — Leadership System Design + 2D DP Review

**Theme:** In a final round design interview with a VP, the question is about strategy and judgment, not just architecture. Design for that audience.

---

## Daily Maintenance (25 min)

**LC — 2D DP sprint (2 problems, timed):**
- LC #62 Unique Paths (6 min — rolling 1D array)
- LC #72 Edit Distance (12 min — write the recurrence in English first, then code)

**SQL — Recursive CTE from memory:**
Write the infra hierarchy recursive CTE (from Day 22) without any notes. Root → leaves, with full path column.

---

## Leadership System Design Session (60 min)

### The Difference — Leadership Design vs Technical Design

**Technical design audience:** peer DEs, tech lead
- They want: correctness, scalability, trade-offs
- They assess: do you know the tools and their limitations?

**Leadership design audience:** VP, Engineering Director, CTO
- They want: business value, risk, cost, build vs buy, timeline
- They assess: do you think like a senior engineer who ships, not just designs?

### Design for Leadership: Data Platform Modernization

**Prompt:** "Our data team uses a 7-year-old on-premises Hadoop cluster. We're moving to the cloud. How would you approach this migration?"

**What a technical answer looks like:**
"I'd use AWS EMR to replace Hadoop, S3 for HDFS, Glue for the metastore, and migrate Hive queries to Athena. We'd use AWS Database Migration Service where possible."

**What a leadership answer looks like:**
"Migration of this scale is a 6-12 month program, not a single project. I'd approach it in three phases:

Phase 1 — Assessment (4-6 weeks): Inventory all workloads. Classify by complexity (simple Hive queries vs complex Spark jobs vs custom MR code). Identify quick wins vs high-risk migrations. Quantify what's being spent on on-prem hardware today.

Phase 2 — Parallel operation (3-4 months): Migrate low-risk workloads first. Build the cloud platform alongside the Hadoop cluster — no cutover until cloud is proven. Establish SLAs for cloud parity. Identify any workloads that shouldn't move (latency-sensitive, regulatory constraints).

Phase 3 — Cutover (2-3 months): Migrate remaining workloads. Decommission on-prem gradually. Measure: cost reduction, reliability improvement, team productivity.

The biggest risk isn't technical — it's adoption. If the data team isn't trained on the new tooling, the migration succeeds technically and fails operationally. Training and change management are in scope."

### Practice This Design

Set a 20-minute timer. Answer this prompt out loud as if presenting to a VP:
"We want to build a self-serve analytics platform so business teams can query data without waiting for the DE team. How would you approach this?"

After: ask yourself — did you mention business value? Did you mention adoption risk? Did you give a phased timeline?

---

## Day 65 Checklist

- [ ] Both 2D DP problems solved (Edit Distance recurrence in English first)
- [ ] Recursive CTE written from memory, no notes
- [ ] Read the leadership vs technical design contrast
- [ ] Self-serve analytics platform answered out loud (20 min) — VP framing
- [ ] "Did you mention: business value, adoption risk, phased timeline?" → Yes for all three
- [ ] One behavioral story reframed for executive audience (business impact, not technical detail)
