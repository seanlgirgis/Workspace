---
created: 2026-03-02
updated: 2026-03-02
summary: Day 39 — Backtracking review, Delta Lake SQL patterns, and Databricks-specific technical prep.
tags: [study-plan, day-39, week-6, backtracking, delta-lake, databricks]
---

# Day 39 — Backtracking Review + Delta Lake SQL + Databricks Prep

**Theme:** Databricks is everywhere in DE interviews now — even at firms that use it indirectly (via partners, migration tools, or Delta Lake). Know the platform.

---

## Daily Maintenance (35 min)

**LC — Backtracking (2 problems, timed):**
- LC #78 Subsets (8 min — `start = i+1`, append at every node)
- LC #39 Combination Sum (10 min — sorted candidates, prune when > remaining, `start = i` for reuse)

Template check — write the backtracking skeleton from memory:
```python
def backtrack(start, path, state):
    if base_case:
        result.append(path[:])
        return
    for i in range(start, len(choices)):
        if prune_condition: continue  # or break
        path.append(choices[i])
        backtrack(i+1, path, new_state)  # or i if reuse allowed
        path.pop()
```

**SQL — Delta Lake Patterns:**
```sql
-- These are Databricks SQL / Delta Lake specific:

-- 1. Time Travel
SELECT * FROM daily_metrics VERSION AS OF 5;
SELECT * FROM daily_metrics TIMESTAMP AS OF '2026-03-01 09:00:00';

-- 2. MERGE INTO (Delta upsert)
MERGE INTO daily_metrics AS target
USING staging AS source
ON target.server_id = source.server_id
   AND target.report_date = source.report_date
WHEN MATCHED THEN UPDATE SET avg_cpu = source.avg_cpu
WHEN NOT MATCHED THEN INSERT *;

-- 3. OPTIMIZE and ZORDER (Databricks-specific maintenance)
OPTIMIZE daily_metrics ZORDER BY (server_id, report_date);

-- 4. DESCRIBE HISTORY (see all Delta transactions)
DESCRIBE HISTORY daily_metrics;
```

**Behavioral:** "Tell me about a time you had to learn a new technology quickly to solve a problem."

---

## Databricks Technical Prep (40 min)

### What Databricks Interviews Test

Databricks interviews for DE roles test:
1. Spark (Delta Lake is built on Spark — know DataFrames, transformations, actions)
2. Delta Lake (ACID, time travel, MERGE, OPTIMIZE)
3. Notebooks and collaboration (know their notebook workflow)
4. Unity Catalog (data governance layer — replacing legacy metastores)
5. Structured Streaming (Spark Streaming with Delta sink)

### Unity Catalog — Know This

```python
# Unity Catalog: 3-level namespace (catalog.schema.table)
# Before Unity Catalog: just database.table

# Old (Hive Metastore):
spark.table("finance_db.daily_metrics")

# With Unity Catalog:
spark.table("prod_catalog.finance.daily_metrics")

# Benefits:
# - Row-level and column-level security
# - Cross-workspace data sharing
# - Audit logs (who accessed what)
# - Lineage tracking
```

### Databricks Structured Streaming with Delta

```python
# Real-time write to Delta Lake
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("telemetry-stream").getOrCreate()

# Read from Kafka
stream_df = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "server-telemetry")
    .load()
)

# Transform
from pyspark.sql.functions import from_json, col, schema_of_json

parsed = stream_df.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# Write to Delta — checkpoint enables exactly-once
(parsed.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "s3://my-bucket/checkpoints/telemetry")
    .trigger(processingTime="1 minute")
    .table("prod_catalog.telemetry.daily_metrics")
)
```

### Interview Framing for Databricks

> "I've worked with Delta Lake for its ACID guarantees — particularly MERGE for CDC-style upserts and time travel for audit queries. In a capacity planning context, being able to say 'show me the capacity state as of last Friday before the incident' is operationally powerful. The OPTIMIZE + ZORDER maintenance is something I'd schedule as a weekly Airflow task on large partitioned tables."

---

## Day 39 Checklist

- [ ] Backtracking template written from memory (no notes)
- [ ] Both backtracking problems coded and timed
- [ ] All 4 Delta Lake SQL patterns written (Time Travel, MERGE, OPTIMIZE, HISTORY)
- [ ] Behavioral question answered (learning new tech — specific, concrete)
- [ ] Know Unity Catalog's 3-level namespace and what it adds over Hive Metastore
- [ ] Know Structured Streaming + Delta sink pattern
