---
created: 2026-03-02
updated: 2026-03-02
summary: Day 51 — Full system design drill. Two complete end-to-end designs drawn and probed. LC maintenance on intervals.
tags: [study-plan, day-51, week-8, system-design, intervals, design-drill]
---

# Day 51 — System Design Full Drill + Intervals Review

**Theme:** System design is the round that most senior candidates lose. Practice the full 30-minute format — not just the drawing.

---

## Daily Maintenance (20 min)

**LC — Merge Intervals (2 problems, timed):**
- LC #56 Merge Intervals (8 min — sort by start, greedily extend)
- LC #57 Insert Interval (8 min — three phases: before overlap, merge overlap, after overlap)

After #57: write the three-phase logic without looking.

---

## Full System Design Session (60 min)

Do both designs. 20 minutes each. Probe yourself with the questions after each.

---

### Design 1: Real-Time Capacity Planning Alert System

**Prompt:** "6,000 servers report CPU/memory/disk every 5 minutes. Alert if any server is projected to exceed 90% capacity within 30 days. Alert within 10 minutes of the projection becoming true."

**Your design (20 min, draw it):**

Expected components:
- Ingest: Kafka (3-6 partitions, manageable throughput)
- Storage: S3 Parquet (daily snapshots), Delta Lake for history
- Trend computation: Airflow daily DAG → linear regression per server (Python + scikit-learn)
- Projection: For each server, `days_to_90pct = (90 - current_avg) / daily_trend_rate`
- Alert check: daily Airflow task → servers where `days_to_90pct < 30` → PagerDuty + Jira
- Dashboard: Athena → Grafana or Tableau for runway visualization

**Probes (answer after drawing):**
1. A server has batch jobs every Sunday — linear trend underestimates capacity risk. Fix?
   *(Seasonal decomposition or week-over-week comparison. Or: separate weekday vs weekend model.)*
2. Your Airflow job fails at 2am. When does the alert fire?
   *(Won't fire until next successful run. Fix: add retry + SLA alert on the Airflow task itself. Also: separate lightweight heartbeat check from the heavy forecasting job.)*
3. Cost estimate for this system on AWS?
   *(S3: cents/month. Glue/Athena: < $10/month at this scale. Lambda for alerts: free tier. Total: < $30/month.)*

---

### Design 2: Event-Driven ETL Pipeline for a Finance Firm

**Prompt:** "Design a pipeline that ingests trade events from 3 source systems in real time, applies business rules (enrichment, validation, transformation), and produces a clean positions table updated within 5 minutes of each trade."

**Your design (20 min, draw it):**

Expected components:
- Source: 3 Kafka topics (one per source system), Avro schema per topic
- Validation layer: Great Expectations or custom rules (reject invalid trades to dead letter queue)
- Enrichment: join to reference data (asset master, counterparty) from Redis (low latency)
- Transformation: Flink stateful job — accumulate positions per (book_id, asset_id)
- Sink: Delta Lake positions table + Snowflake for BI queries
- Dead letter queue: Kafka DLQ topic → manual review dashboard

**Probes:**
1. A trade arrives out of order (timestamp 3 minutes behind). Does it affect the positions table?
   *(Flink event-time processing with 5-minute watermark handles this. Trade processed in correct order.)*
2. The enrichment reference data changes (counterparty renamed). How do you avoid stale data in the stream?
   *(Cache invalidation: Redis TTL + a Kafka compacted topic for reference data updates. Flink reads the compacted topic to update its broadcast state.)*
3. How do you ensure the positions table is correct despite potential duplicate trades from source systems?
   *(Idempotent MERGE on (trade_id, book_id, asset_id). Each trade has a unique trade_id. Duplicate = same trade_id → overwrite, not insert.)*

---

## Day 51 Checklist

- [ ] LC #57 Insert Interval — three-phase logic written without looking
- [ ] Design 1 drawn on paper (all components)
- [ ] All 3 Design 1 probes answered verbally
- [ ] Design 2 drawn on paper (all components)
- [ ] All 3 Design 2 probes answered verbally
- [ ] Total system design time: < 50 minutes (20 min each + probes)
- [ ] Weakest probe identified and noted for Day 53 review
