---
created: 2026-03-02
updated: 2026-03-02
summary: Day 80 — Technical prep for the new role. Domain deepening on APM/capacity planning and the specific tech stack you'll use.
tags: [study-plan, day-80, week-12, technical-prep, apm, capacity-planning, new-role]
---

# Day 80 — Technical Prep for the New Role

**Theme:** You were hired for your background. Show up knowing it cold. The areas where you're newest — not your strengths — are where to spend prep time today.

---

## Daily Maintenance (20 min)

**LC — Two Pointers (2 problems, timed):**
- LC #15 3Sum (10 min — sort, fix first element, two-pointer on rest; skip duplicates with `while left < right and nums[left] == nums[left-1]: left++`)
- LC #16 3Sum Closest (8 min — same sort + two-pointer, track `min_diff = abs(total - target)`)

**SQL — Platform-specific syntax recall:**
Write, from memory, the Snowflake Time Travel query (query a table as it was 1 hour ago), the Snowflake STREAM check (SYSTEM$STREAM_HAS_DATA), and the Delta Lake equivalent (`VERSION AS OF n` and `TIMESTAMP AS OF ts`).

---

## Technical Deepening Session (60 min)

### Your Differentiator: APM Background

You're coming in with 10+ years of APM experience (CA APM, AppDynamics, Dynatrace, BMC TrueSight). This is your moat. But translating it to a data engineering context requires deliberate framing.

**How APM experience maps to data engineering:**

| APM Concept | Data Engineering Equivalent |
|-------------|----------------------------|
| Agent instrumentation | OTel SDK / custom metrics emission |
| Metrics collection pipeline | Kafka → Prometheus → time-series DB |
| Alert thresholds and baselines | SLA definitions, anomaly detection |
| Topology discovery | Data lineage mapping |
| Capacity planning dashboards | Resource utilization tracking pipelines |
| Correlated problem isolation | Root cause analysis in streaming data |
| SLA breach detection | Data freshness monitoring, pipeline SLA alerting |

Be able to explain these mappings in an interview or on-the-job conversation. You're not "transitioning from APM." You're bringing APM operational depth to data systems.

---

### Know the Stack You're Walking Into

Before Day 1, research the specific tooling at your new employer. For each tool, make sure you can:
1. Explain what it does and why it exists
2. State its key limitation or trade-off
3. Describe one real scenario where it's the right choice

**Common Senior DE stack (fill in what your company uses):**

```
Ingestion:      ___ (Kafka / Kinesis / Pub/Sub)
Processing:     ___ (Spark / Flink / dbt / Beam)
Storage:        ___ (Delta Lake / Iceberg / S3 + Parquet)
Orchestration:  ___ (Airflow / Prefect / Dagster)
Catalog:        ___ (Glue / Unity Catalog / OpenMetadata)
Monitoring:     ___ (Prometheus / Datadog / OTel)
BI/Serving:     ___ (Snowflake / Redshift / Databricks SQL)
```

For any tool where you'd rate yourself < 3/5: do a focused 2-hour deep dive. Not comprehensive learning — just enough to be productive on Day 1.

---

### Capacity Planning Specifics

If the role involves capacity planning, your APM background is direct experience. Refresh the vocabulary:

**Key metrics:**
- CPU utilization: `avg`, `p95`, `p99` — not just average. P99 CPU spikes often cause cascading failures that averages hide.
- Memory pressure: `RSS`, `heap used`, swap utilization
- Disk I/O: read/write throughput and IOPS ceilings
- Network: bandwidth saturation vs connection limits
- Queue depth: length and lag (Kafka consumer lag is a primary signal)

**Key analysis patterns:**
- Trend-based projection: fit a regression to the last 30/60/90 days of utilization, extrapolate to capacity ceiling
- Seasonal adjustment: traffic patterns repeat weekly and around business cycles — your baseline must account for this
- Headroom policy: most orgs target < 70% utilization to maintain headroom for unexpected spikes

**Capacity alert threshold setting:**
The APM way: set thresholds based on historical P99 + buffer, not gut feel. Thresholds that are too sensitive produce noise. Too loose and you miss real issues.

---

### Building Your "Day 1 Cheat Sheet"

Before your first day, write a 1-page cheat sheet:

```
Team:
  Manager: ___
  Key teammates: ___
  Key downstream consumers: ___

Systems I'll touch first:
  System 1: ___  (what it does, rough tech)
  System 2: ___

Questions I want to answer in week 1:
  1. ___
  2. ___
  3. ___

Things I want to avoid doing in the first 30 days:
  - Proposing architecture changes before I understand the current state
  - ___
```

---

## Day 80 Checklist

- [ ] Both LC problems solved (3Sum: sort + two-pointer + skip duplicates)
- [ ] Platform-specific SQL syntax written from memory (Snowflake TT + STREAM + Delta Lake VERSION AS OF)
- [ ] APM-to-DE mapping table reviewed — can explain all mappings conversationally
- [ ] New role tech stack filled in — any gaps identified for focused prep
- [ ] Capacity planning vocabulary reviewed — P99, headroom, trend projection
- [ ] Day 1 cheat sheet drafted (team, systems, questions, limits)
