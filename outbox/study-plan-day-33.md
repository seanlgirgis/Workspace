---
created: 2026-03-02
updated: 2026-03-02
summary: Day 33 — Heap review, recursive CTE practice, and company research on JPMorgan Chase.
tags: [study-plan, day-33, week-5, heap, recursive-cte, jpmorgan-research]
---

# Day 33 — Heap Review + Recursive CTE + JPMorgan Research

**Theme:** JPMorgan is the largest DE employer in finance and has been on an aggressive cloud-native modernization. Know their story.

---

## Daily Maintenance (35 min)

**LC — Heap / Priority Queue (3 problems, timed):**
- LC #347 Top K Frequent Elements (10 min — Counter + heapq.nlargest, or bucket sort)
- LC #215 Kth Largest Element in an Array (8 min — min-heap of size k)
- LC #295 Find Median from Data Stream (12 min — two heaps: max-heap left, min-heap right)

After #295: draw the two-heap diagram and explain the rebalancing rule out loud.

**SQL — Recursive CTE:**
Write a recursive CTE from scratch that:
1. Starts from a root node (e.g., `us-east-1` region)
2. Walks down through availability zones, racks, to individual servers
3. Returns: node_id, depth, full path, node_type

No looking at Day 22. Build from the pattern: anchor → UNION ALL → recursive join.

**Behavioral:** Speak Story 5 (cross-functional collaboration) — timed.

---

## Company Research: JPMorgan Chase (45 min)

### JPMorgan DE Context

**Key facts:**
- Largest bank in the US by assets — massive data engineering footprint
- **Fusion** (formerly Axiom): their cloud data platform initiative
- Heavy AWS investment, significant Snowflake and Databricks usage
- Published engineering blog content on DE at scale
- Active on open-source: Perspective (data visualization), FINOS contributions
- Chief Data & Analytics Office (CDAO): unified data governance initiative

**What JPMorgan interviews test:**
- Cloud architecture knowledge (AWS, Azure) — they are multi-cloud
- Python and PySpark — large-scale ETL is the dominant use case
- Data governance and lineage — regulatory requirements are explicit
- System design with scale emphasis — JP has massive data volumes

```
JPMorgan DE Research Template
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Known tech stack at JPMorgan:
  Cloud: AWS (primary) + Azure
  Warehouse: Snowflake + some legacy Oracle
  Processing: Spark (EMR / Databricks)
  Orchestration: Airflow (managed) + some proprietary
  Streaming: Kafka
  Data Catalog: Apache Atlas (CDAO initiative)

JPMorgan's public DE initiatives:
  - Fusion Data Platform (cloud migration of trading data)
  - CDAO data quality and lineage mandate
  - Open-source: FINOS, Legend (data modeling language)

My angle for JPMorgan:
  "The CDAO's focus on data lineage and quality aligns directly
   with my experience in [pipeline monitoring / idempotency /
   control totals]. I've built systems where correctness isn't
   optional — same stakes."

JPMorgan-specific questions:
  1. "How does the CDAO mandate affect day-to-day DE work —
     is lineage tracking baked into the pipeline framework or
     enforced by the data team separately?"
  2. ___
  3. ___
```

### JPMorgan Interview Format

JPMorgan typically runs:
1. Recruiter screen (30 min)
2. Coding screen (HackerRank or live: 2 problems, 1 SQL)
3. Technical interview (system design + technical concepts)
4. Final round (behavioral + business case)

**Time pressure:** JPMorgan coding screens are often on tight timers. The Heap and BFS/DFS patterns appear frequently.

---

## Day 33 Checklist

- [ ] 3 Heap problems timed — two-heap median explained out loud
- [ ] Recursive CTE written from scratch without looking at notes
- [ ] Story 5 spoken and timed (< 90 sec)
- [ ] JPMorgan research template filled in
- [ ] Know JPMorgan's interview format (4 rounds)
- [ ] Applied to open JPMorgan DE roles
