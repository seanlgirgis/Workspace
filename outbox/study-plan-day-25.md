---
created: 2026-03-02
updated: 2026-03-02
summary: Day 25 — Idempotency and exactly-once semantics in pipelines, Data Contracts with OpenMetadata, Apache Beam model, OpenTelemetry for distributed DE observability.
tags: [study-plan, day-25, idempotency, exactly-once, data-contracts, apache-beam, opentelemetry]
---

# Day 25 — Idempotency + Exactly-Once | Data Contracts | Apache Beam | OpenTelemetry

**Theme:** The concepts that distinguish "I built a pipeline that works" from "I built a pipeline that's correct under all failure conditions." This is the senior/staff DE differentiation.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is a monotonic stack and what is its time complexity advantage?
2. What does `NTILE(4) OVER (ORDER BY avg_cpu DESC)` produce?
3. What is a lateral join and when is it more useful than a window function?
4. What is the difference between Polars lazy and eager execution?
5. What is ClickHouse's MergeTree `ORDER BY` key used for?
6. In Snowflake Streams, what does `METADATA$ACTION` contain?

---

## A. LeetCode — No New Pattern Today

Day 25 is architecture-heavy. Instead of new LC patterns:

**30-minute speed drill — timed from memory, no hints:**

| Problem | Target time |
|---------|-------------|
| LC #78 Subsets (Backtracking) | 5 min |
| LC #1143 LCS (2D DP) | 8 min |
| LC #208 Implement Trie | 8 min |
| LC #743 Network Delay (Dijkstra) | 9 min |

After each: check complexity. Identify any hesitation points. Note them.

---

## B. SQL / Architecture — Idempotency and Exactly-Once Semantics (45 min)

### What is Idempotency?

An operation is **idempotent** if running it N times produces the same result as running it once.

**Why it matters:** Pipelines fail. Airflow retries. Kafka consumers restart mid-batch. If your write operation is not idempotent, failures cause duplicate data.

**Non-idempotent (bad):**
```python
# INSERTS accumulate duplicates on retry
INSERT INTO daily_metrics VALUES ('srv-001', '2026-03-02', 82.5);
# Run twice → two rows for the same server/date
```

**Idempotent (correct):**
```sql
-- UPSERT: INSERT or REPLACE if conflict
INSERT INTO daily_metrics (server_id, report_date, avg_cpu)
VALUES ('srv-001', '2026-03-02', 82.5)
ON CONFLICT (server_id, report_date) DO UPDATE SET avg_cpu = EXCLUDED.avg_cpu;

-- Or: delete-then-insert for a partition
DELETE FROM daily_metrics WHERE report_date = '2026-03-02';
INSERT INTO daily_metrics SELECT * FROM staging WHERE report_date = '2026-03-02';
-- Safe if you re-run: delete is a no-op if no rows, insert is fresh
```

**Idempotent Airflow DAGs:**
```python
# WRONG: appends data on each run
def load_metrics(**context):
    df = pd.read_parquet(source_path)
    df.to_sql("daily_metrics", conn, if_exists='append')

# CORRECT: replace partition each run
def load_metrics(**context):
    run_date = context['ds']   # dag run date
    df = pd.read_parquet(f"{source_path}/date={run_date}/")
    # Delete the partition first
    conn.execute(f"DELETE FROM daily_metrics WHERE report_date = '{run_date}'")
    df.to_sql("daily_metrics", conn, if_exists='append')
    # Idempotent: re-running same date always produces same result
```

### Exactly-Once vs At-Least-Once vs At-Most-Once

| Guarantee | What it means | Risk |
|-----------|--------------|------|
| At-most-once | Message might be lost, never duplicated | Data loss |
| At-least-once | Message guaranteed delivered, might be delivered > once | Duplicates |
| Exactly-once | Delivered exactly once, no loss, no dups | Highest overhead |

**In practice:**
- Kafka consumers: **at-least-once** by default. Your consumer must handle duplicates (idempotent writes).
- Kafka `enable.idempotence=true`: deduplicates within a producer session.
- Kafka transactions: exactly-once semantics (EOS) — atomic read-process-write across topics.
- Flink with checkpointing: exactly-once semantics for stateful stream processing.
- Spark Structured Streaming + Delta: exactly-once via write-ahead log.

### Deduplication in SQL

```sql
-- Pattern 1: Window function dedup (keep latest per key)
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY server_id, report_date
            ORDER BY ingested_at DESC
        ) AS rn
    FROM raw_metrics
)
INSERT INTO daily_metrics
SELECT server_id, report_date, avg_cpu
FROM ranked
WHERE rn = 1;

-- Pattern 2: NOT EXISTS anti-join (insert only if not already present)
INSERT INTO daily_metrics (server_id, report_date, avg_cpu)
SELECT r.server_id, r.report_date, r.avg_cpu
FROM raw_metrics r
WHERE NOT EXISTS (
    SELECT 1 FROM daily_metrics d
    WHERE d.server_id = r.server_id
      AND d.report_date = r.report_date
);
```

### Watermark Tables — Track What's Been Processed

```sql
-- Track last processed offset per source partition
CREATE TABLE pipeline_watermarks (
    source_name     VARCHAR,
    partition_id    INT,
    last_offset     BIGINT,
    processed_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_name, partition_id)
);

-- In the pipeline: read only new data
SELECT * FROM raw_events e
WHERE e.kafka_offset > (
    SELECT COALESCE(MAX(last_offset), -1)
    FROM pipeline_watermarks
    WHERE source_name = 'server-telemetry'
      AND partition_id = e.partition_id
);

-- After processing: update the watermark (atomic with the write)
INSERT INTO pipeline_watermarks (source_name, partition_id, last_offset)
VALUES ('server-telemetry', 0, 12345)
ON CONFLICT (source_name, partition_id) DO UPDATE
    SET last_offset = EXCLUDED.last_offset,
        processed_at = CURRENT_TIMESTAMP;
```

---

## C. Data Engineering Concepts — Data Contracts + OpenMetadata (30 min)

### What is a Data Contract?

A data contract is a formal, machine-readable agreement between a data producer (who owns and publishes data) and data consumers (teams who build on it).

It specifies:
- **Schema** — column names, types, nullable rules
- **SLA** — freshness, availability, latency
- **Quality rules** — value ranges, referential integrity, completeness
- **Ownership** — team, slack channel, escalation path
- **Versioning** — backward-compatible changes allowed, breaking changes require negotiation

### Why Data Contracts Matter (Finance Context)

In finance, a downstream team might use a `positions` table to calculate regulatory capital. If the upstream team silently changes a column type or removes a column, the downstream calculation breaks — potentially with regulatory consequences.

Data contracts enforce:
- Producers cannot make breaking changes without notification
- Breaking changes require a migration window
- Schema changes are versioned and tracked

### Data Contract Format (YAML)

```yaml
# data-contract.yaml — machine-readable, version-controlled
id: server-daily-metrics-v2
name: Server Daily Metrics
version: "2.0.0"
domain: infrastructure
owner:
  team: infra-data-platform
  email: infra-data@company.com
  slack: "#infra-data-support"

servers:
  - type: s3
    location: s3://data-warehouse/metrics/daily/
    format: parquet
    partitioned_by: [report_date]

schema:
  - name: server_id
    type: VARCHAR
    required: true
    description: "Unique server identifier (format: srv-NNN)"
    pii: false
  - name: report_date
    type: DATE
    required: true
  - name: avg_cpu
    type: FLOAT
    required: true
    constraints:
      minimum: 0.0
      maximum: 100.0
  - name: avg_mem
    type: FLOAT
    required: false
    description: "Memory utilization (added in v2.0)"

quality:
  - type: row_count
    minimum: 5000
    description: "At least 5000 servers must report daily"
  - type: no_nulls
    columns: [server_id, report_date, avg_cpu]
  - type: freshness
    maximum_age: "6 hours"

sla:
  availability: "99.5%"
  freshness: "daily by 06:00 UTC"
  support_hours: "business hours"

changelog:
  - version: "2.0.0"
    date: "2026-03-01"
    breaking: false
    description: "Added avg_mem column (nullable for backward compatibility)"
  - version: "1.0.0"
    date: "2026-01-15"
    breaking: true
    description: "Initial contract"
```

### OpenMetadata — Catalog + Lineage + Governance

OpenMetadata is an open-source metadata platform (alternative to Apache Atlas, Alation, Collibra).

**Key capabilities:**
- **Data catalog:** searchable index of all tables, dashboards, pipelines
- **Data lineage:** track how data flows from source → pipeline → table → dashboard
- **Data quality:** run tests, track freshness, alert on breaches
- **Data contracts:** enforce schema agreements
- **Collaboration:** owners, tags, descriptions, glossary terms

**Why interviewers ask about this:**
> Finance firms have regulatory requirements for data lineage (e.g., BCBS 239 — Risk Data Aggregation principles). Being able to say "I've implemented OpenMetadata or Apache Atlas for lineage" is a significant differentiator.

### Lineage in Practice

```
Data lineage example:
  Source: Kafka topic "server-telemetry"
      ↓ (Flink consumer)
  Raw table: s3://warehouse/raw/telemetry/
      ↓ (Glue ETL job)
  Processed: s3://warehouse/processed/daily_metrics/
      ↓ (Athena view)
  View: capacity_planning.daily_metrics_enriched
      ↓ (dbt model)
  Model: capacity_planning.capacity_risk_scores
      ↓ (Tableau)
  Dashboard: "Infrastructure Capacity Dashboard"

If avg_cpu column type changes at source → OpenMetadata shows all downstream
assets affected BEFORE the change is deployed.
```

---

## D. Technology — Apache Beam and OpenTelemetry (45 min)

### Apache Beam — Unified Batch and Streaming

Apache Beam is a programming model (not a runtime) for building portable data pipelines that run on any runner: Apache Flink, Google Dataflow, Apache Spark, or locally.

**Why it matters:**
- Write once, run on Flink or Dataflow → no vendor lock-in
- Same code handles batch and streaming (same API)
- Google Cloud Dataflow is Beam-native (big in finance cloud migrations)

### Beam Core Concepts

```
Pipeline    → the overall computation graph
PCollection → an immutable, distributed dataset (like an RDD/DataFrame)
PTransform  → an operation on a PCollection (like a Spark transformation)
Runner      → the execution engine (Flink, Dataflow, Direct)
```

### PyBeam Example

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions([
    '--runner=FlinkRunner',          # or DataflowRunner, DirectRunner
    '--project=my-gcp-project',
    '--temp_location=gs://my-bucket/temp/',
])

with beam.Pipeline(options=options) as p:
    (
        p
        | 'Read from Kafka'   >> beam.io.ReadFromKafka(
              consumer_config={'bootstrap.servers': 'kafka:9092'},
              topics=['server-telemetry']
          )
        | 'Parse JSON'        >> beam.Map(parse_telemetry_event)
        | 'Filter High CPU'   >> beam.Filter(lambda e: e['avg_cpu'] > 80)
        | 'Window 5 min'      >> beam.WindowInto(
              beam.window.FixedWindows(5 * 60)
          )
        | 'Aggregate by server' >> beam.CombinePerKey(beam.combiners.MeanCombineFn())
        | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
              'project:dataset.table',
              schema='server_id:STRING,avg_cpu:FLOAT,window_end:TIMESTAMP'
          )
    )
```

**When to recommend Beam:**
> "If the team is deploying to Google Cloud and wants Dataflow (managed, serverless), or if they need the same pipeline to run as batch today and streaming tomorrow without rewriting — Beam is the right abstraction. If they're on AWS and committed to Flink, skip Beam and write native Flink directly."

### OpenTelemetry — Distributed Observability for DE

OpenTelemetry (OTel) is the open standard for distributed tracing, metrics, and logs. It replaced the fragmented world of Jaeger, Zipkin, Prometheus-specific exporters, etc.

**Three signals:**
- **Traces:** end-to-end journey of a request or pipeline run across services
- **Metrics:** numeric measurements over time (latency, error rate, record count)
- **Logs:** structured event records (already covered with structlog — OTel adds context)

### OTel in a Data Pipeline

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Setup (once at startup)
provider = TracerProvider()
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("telemetry-pipeline")

# Instrument your pipeline
def run_pipeline(report_date: str):
    with tracer.start_as_current_span("pipeline_run") as span:
        span.set_attribute("report_date", report_date)
        span.set_attribute("environment", "production")

        with tracer.start_as_current_span("ingest_raw_data"):
            raw_df = ingest_from_s3(report_date)
            span.set_attribute("rows_ingested", len(raw_df))

        with tracer.start_as_current_span("transform"):
            result_df = transform(raw_df)

        with tracer.start_as_current_span("write_output"):
            write_to_duckdb(result_df)
```

**What you get:**
- Waterfall trace: see exactly which step took how long
- Correlate pipeline spans with Airflow task IDs
- Set up SLA alerts: "alert if ingest_raw_data span > 10 minutes"
- Correlate with logs and metrics automatically (OTel context propagation)

### OTel Collector Architecture

```
Pipeline code (OTel SDK)
    ↓ OTLP (gRPC)
OTel Collector (sidecar or centralized)
    ├── Traces   → Jaeger / Tempo / Lightstep / Honeycomb
    ├── Metrics  → Prometheus / Datadog / CloudWatch
    └── Logs     → Loki / Elasticsearch / CloudWatch Logs
```

**Why OTel matters for DE at senior level:**
> "Observability in DE has historically been an afterthought — we know the pipeline ran because the downstream table got data. OTel brings the same structured observability that SREs have had for services: trace the flow of a record through your pipeline, see exactly where latency lives, correlate a spike in processing time with a change in data volume. I've started adding OTel spans to Airflow tasks and it dramatically reduced MTTR when pipelines degrade."

---

## Behavioral Anchor — Day 25

> "Tell me about a time data from your pipeline was wrong and you had to own the impact."

Strong answer:
- What was wrong and how you discovered it (not the downstream team discovering it first)
- What the impact was on the business
- How you communicated (transparent, timely, solution-focused)
- What you built to prevent recurrence
- What you would do differently

This is a values question disguised as a technical one. Interviewers want honesty and ownership.

---

## Day 25 Checklist

- [ ] Speed-drilled 4 LC problems in 30 minutes total (timed)
- [ ] Can explain idempotency with a concrete SQL example
- [ ] Can write the delete-then-insert idempotent pattern from scratch
- [ ] Can explain at-least-once vs exactly-once and when each is acceptable
- [ ] Wrote a watermark table pattern for tracking pipeline progress
- [ ] Can describe what a data contract contains (5 sections)
- [ ] Can explain why data contracts matter in finance (regulatory lineage)
- [ ] Know what OpenMetadata does: catalog + lineage + quality + governance
- [ ] Can describe Apache Beam's 4 core concepts (Pipeline, PCollection, PTransform, Runner)
- [ ] Know when to recommend Beam vs native Flink
- [ ] Can explain OTel's 3 signals and what a trace span is
- [ ] Behavioral story drafted for "owned a data quality incident"
