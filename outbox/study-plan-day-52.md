---
created: 2026-03-02
updated: 2026-03-02
summary: Day 52 — Architecture concepts oral review. Python patterns review. Heap and Two Pointers maintenance.
tags: [study-plan, day-52, week-8, architecture-review, python-review, heap, two-pointers]
---

# Day 52 — Architecture Oral Review + Python Patterns

**Theme:** Verbalize every concept today. The interview is spoken. Silent reading does not build spoken fluency.

---

## Daily Maintenance (30 min)

**LC — Heap + Two Pointers sprint (2 each, timed):**
- LC #215 Kth Largest Element (8 min — min-heap of size k)
- LC #295 Find Median from Data Stream (10 min — two heaps)
- LC #167 Two Sum II (4 min — two pointers on sorted array)
- LC #11 Container With Most Water (6 min — move shorter pointer)

---

## Architecture Oral Review (45 min)

For each topic, close your notes and answer out loud in 60 seconds. If you can't fill 60 seconds — the knowledge isn't deep enough.

**Round 1 — Streaming:**
1. "Explain Kafka partitions and why they matter for parallelism."
2. "What is the difference between Kafka Streams and Apache Flink?"
3. "What is a watermark in Flink and what problem does it solve?"

**Round 2 — Storage:**
4. "What is Delta Lake and what 3 things does its transaction log enable?"
5. "When would you use Iceberg instead of Delta Lake?"
6. "What is a compacted Kafka topic and when do you use one?"

**Round 3 — Orchestration:**
7. "What is the difference between Airflow XCom and a shared database?"
8. "Why would you choose KubernetesExecutor over LocalExecutor for Airflow?"
9. "In Airflow, what is `catchup=False` and when would you set it to True?"

**Round 4 — Data Quality:**
10. "What is Great Expectations and what does a 'suite' contain?"
11. "How do you ensure a pipeline is idempotent when writing to a relational database?"
12. "What is a control total reconciliation?"

**Round 5 — Finance:**
13. "What is BCBS 239 and why do data engineers care about it?"
14. "What is an audit trail and what fields must it contain?"
15. "What is the risk of NOT IN with NULLs in SQL?"

Score yourself: Strong (answered in 60s with depth) / OK (answered but thin) / Weak (couldn't fill 30s).

---

## Python Patterns Review (30 min)

Write each of these from memory (5-10 lines each):

1. A retry decorator with exponential backoff
2. A context manager using `contextlib.contextmanager` that wraps a DuckDB transaction
3. A `typing.Protocol` for a DataSource (connect, read, close)
4. A Pydantic Settings class for a pipeline config (4 fields, one with default)
5. A `concurrent.futures.ThreadPoolExecutor` example fetching 100 URLs in parallel

---

## Day 52 Checklist

- [ ] All 4 LC problems coded and timed
- [ ] All 15 architecture questions answered verbally (score logged)
- [ ] Any "Weak" scores → add to tomorrow's drill list
- [ ] All 5 Python patterns written from memory
- [ ] Any pattern that took > 5 min → repeat it before bed
