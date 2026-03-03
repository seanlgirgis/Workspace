---
created: 2026-03-02
updated: 2026-03-02
summary: Day 23 — String Dynamic Programming (LPS, Palindrome, Regex Matching), CDC with Debezium and Schema Registry (Avro/Protobuf), Python Dataclasses and Context Managers, Snowflake-specific features.
tags: [study-plan, day-23, string-dp, cdc, debezium, avro, protobuf, snowflake, dataclasses]
---

# Day 23 — String DP | CDC + Schema Registry | Dataclasses + Context Managers | Snowflake

**Theme:** Patterns that appear in enterprise DE stacks — CDC for database change capture, schema evolution management, and Snowflake's unique features.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is Dijkstra's key data structure and what constraint makes it fail?
2. Why does Bellman-Ford use a `temp` copy of the distances array?
3. In a recursive CTE, what is the anchor member and what is the recursive member?
4. What is a watermark in Apache Flink?
5. In asyncio, what does `asyncio.Semaphore(20)` do?
6. In LCS (2D DP), what is `dp[i][j]` and what are the two recurrence cases?

---

## A. LeetCode — String Dynamic Programming (60 min)

### Why String DP

String DP problems test whether you can model string manipulation decisions as a table. They appear in:
- Approximate string matching (edit distance, LCS — already covered)
- Palindrome problems (financial identifiers, data validation)
- Pattern matching (log parsing, schema validation)

---

### Problem 1 — LC #5: Longest Palindromic Substring (Medium)

**Problem:** Given a string s, return the longest substring that is a palindrome.

```
Input:  "babad"
Output: "bab"  (or "aba")
```

**Approach 1 — Expand Around Center (O(n²), O(1) space):**

```python
def longestPalindrome(s: str) -> str:
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left+1:right]   # after overshooting

    result = ""
    for i in range(len(s)):
        odd  = expand(i, i)       # odd-length palindrome: center at i
        even = expand(i, i+1)     # even-length palindrome: center between i and i+1
        result = max(result, odd, even, key=len)
    return result
```

**Approach 2 — DP (O(n²) time and space, interview alternative):**

```python
def longestPalindrome(s: str) -> str:
    n = len(s)
    # dp[i][j] = True if s[i..j] is a palindrome
    dp = [[False] * n for _ in range(n)]

    # Every single char is a palindrome
    for i in range(n):
        dp[i][i] = True

    start, max_len = 0, 1

    # Check length 2
    for i in range(n-1):
        if s[i] == s[i+1]:
            dp[i][i+1] = True
            start, max_len = i, 2

    # Check lengths 3 and above
    for length in range(3, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i+1][j-1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length

    return s[start:start+max_len]
```

---

### Problem 2 — LC #647: Palindromic Substrings (Medium)

**Problem:** Count the number of palindromic substrings in s.

```
Input:  "abc"
Output: 3   ("a", "b", "c")

Input:  "aaa"
Output: 6   ("a","a","a","aa","aa","aaa")
```

```python
def countSubstrings(s: str) -> int:
    count = 0

    def expand_and_count(left, right):
        nonlocal count
        while left >= 0 and right < len(s) and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

    for i in range(len(s)):
        expand_and_count(i, i)     # odd
        expand_and_count(i, i+1)   # even

    return count
```

---

### Problem 3 — LC #10: Regular Expression Matching (Hard)

**Problem:** Implement regex matching with `.` and `*`. `.` matches any single character. `*` matches zero or more of the preceding element.

```
Input:  s = "aa", p = "a*"
Output: True    (* = zero or more 'a')

Input:  s = "ab", p = ".*"
Output: True    (.* = zero or more of any char)
```

```python
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    # dp[i][j] = does s[:i] match p[:j]?
    dp = [[False] * (n+1) for _ in range(m+1)]
    dp[0][0] = True   # empty string matches empty pattern

    # Base case: pattern "a*b*c*..." can match empty string
    for j in range(2, n+1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]   # '*' eliminates preceding element

    for i in range(1, m+1):
        for j in range(1, n+1):
            if p[j-1] == '*':
                # Option 1: use '*' as zero occurrences (eliminate a*)
                dp[i][j] = dp[i][j-2]
                # Option 2: use '*' for one more occurrence (if chars match)
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]   # chars match: diagonal

    return dp[m][n]
```

**Key insight for `*` handling:** `*` can mean zero (eliminate the `x*` pair) or one-more (extend the match if the char matches).

---

### Problem 4 — LC #516: Longest Palindromic Subsequence (Medium)

**Problem:** Given string s, find the length of the longest palindromic subsequence. (Subsequence = doesn't have to be contiguous.)

```
Input:  "bbbab"
Output: 4   ("bbbb")
```

**Key insight:** LPS(s) = LCS(s, reverse(s))

```python
def longestPalindromeSubseq(s: str) -> int:
    # LPS = LCS of s and its reverse
    t = s[::-1]
    m = len(s)
    dp = [[0] * (m+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, m+1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][m]
```

---

## B. SQL — CDC + Debezium + Schema Registry (45 min)

### What is CDC?

Change Data Capture = capture every INSERT/UPDATE/DELETE from a source database as a stream of events. Instead of polling "what changed since last run?", the database itself publishes changes.

**Why it matters for finance DE:**
- Real-time replication of transactional data (orders, positions, settlements)
- Audit trails (immutable record of every change)
- Event-driven pipelines (trigger downstream processing on each change)
- Avoiding expensive full-table scans for incremental loads

### Debezium Architecture

```
Source DB (PostgreSQL) → Debezium Connector → Kafka Topic → Consumers
   ↓
WAL (Write-Ahead Log)
   ↓ Debezium reads the WAL
   ↓ Creates change events
   ↓ Publishes to Kafka topic per table
```

**Debezium event structure (JSON):**
```json
{
  "before": {
    "server_id": "srv-001",
    "tier": "standard",
    "region": "us-east-1"
  },
  "after": {
    "server_id": "srv-001",
    "tier": "premium",
    "region": "us-east-1"
  },
  "op": "u",
  "ts_ms": 1740920400000,
  "source": {
    "db": "config_db",
    "table": "servers",
    "lsn": 12345678
  }
}
```

**op values:** `c` = create (INSERT), `u` = update (UPDATE), `d` = delete, `r` = read (snapshot)

### SQL: Processing CDC Events in DuckDB/Athena

```sql
-- CDC events land in S3 as JSON, partitioned by date
-- Process: apply events to build current state

-- Step 1: Parse CDC stream into typed rows
WITH cdc_parsed AS (
    SELECT
        JSON_VALUE(payload, '$.after.server_id')   AS server_id,
        JSON_VALUE(payload, '$.after.tier')        AS tier,
        JSON_VALUE(payload, '$.after.region')      AS region,
        JSON_VALUE(payload, '$.op')                AS operation,
        CAST(JSON_VALUE(payload, '$.ts_ms') AS BIGINT) AS event_ts_ms,
        ROW_NUMBER() OVER (
            PARTITION BY JSON_VALUE(payload, '$.after.server_id')
            ORDER BY CAST(JSON_VALUE(payload, '$.ts_ms') AS BIGINT) DESC
        ) AS rn
    FROM cdc_events_raw
    WHERE event_date = '2026-03-02'
      AND JSON_VALUE(payload, '$.op') != 'd'   -- exclude deletes
),
-- Step 2: Keep only latest state per server
current_state AS (
    SELECT server_id, tier, region, event_ts_ms
    FROM cdc_parsed
    WHERE rn = 1
)
SELECT * FROM current_state ORDER BY server_id;
```

### Schema Registry — Avro and Protobuf

When Kafka messages use a schema registry, producers and consumers agree on a schema format. This prevents breaking changes from silently corrupting downstream consumers.

**How it works:**
1. Producer registers a schema (Avro or Protobuf) with the Schema Registry
2. Producer sends: `[magic byte][schema_id][encoded_payload]`
3. Consumer reads schema_id → fetches schema → deserializes

**Avro schema example (server telemetry):**
```json
{
  "type": "record",
  "name": "ServerTelemetry",
  "namespace": "com.company.telemetry",
  "fields": [
    {"name": "server_id", "type": "string"},
    {"name": "report_date", "type": "string", "logicalType": "date"},
    {"name": "avg_cpu", "type": "float"},
    {"name": "avg_mem", "type": "float"},
    {"name": "tags", "type": {"type": "array", "items": "string"}, "default": []}
  ]
}
```

**Schema evolution rules (backward compatibility):**

| Change | Backward Compatible? |
|--------|---------------------|
| Add optional field with default | YES |
| Add required field (no default) | NO — old readers can't read new data |
| Remove field | YES (if old readers handle missing field) |
| Change field type (int → long) | Depends on promotion rules |
| Rename field | NO (break old readers) |

**In DE interviews:**
> "When we use Kafka in production with schema registry, all schema changes go through a compatibility check — we use BACKWARD compatibility so new consumers can read old messages. Adding a field always requires a default value. Renaming a field requires a migration period where both old and new names are in the schema."

---

## C. Python — Dataclasses and Context Managers (30 min)

### Dataclasses — Structured Data Without Boilerplate

```python
from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import date

@dataclass
class ServerMetric:
    server_id: str
    report_date: date
    avg_cpu: float
    avg_mem: float
    tags: list[str] = field(default_factory=list)   # mutable default must use field()
    is_anomaly: bool = False
    anomaly_score: Optional[float] = None

    def __post_init__(self):
        # Validation on creation
        if not 0 <= self.avg_cpu <= 100:
            raise ValueError(f"avg_cpu {self.avg_cpu} out of range [0, 100]")
        if not 0 <= self.avg_mem <= 100:
            raise ValueError(f"avg_mem {self.avg_mem} out of range [0, 100]")

    @property
    def is_critical(self) -> bool:
        return self.avg_cpu > 90 or self.avg_mem > 95

# Usage
m = ServerMetric("srv-001", date(2026, 3, 2), 82.5, 74.1, ["production"])
print(m.is_critical)   # False
print(asdict(m))       # dict — for JSON serialization

# Dataclass provides __repr__, __eq__, __hash__ (if frozen=True) for free
```

**Dataclass vs Pydantic:**
| Feature | Dataclass | Pydantic |
|---------|-----------|---------|
| Validation | Manual (`__post_init__`) | Automatic (type coercion) |
| JSON parsing | Manual (with `dacite` or json) | Built-in `.model_validate()` |
| Performance | Faster | Slower (validation overhead) |
| Best for | Internal data structures | API boundaries, config, user input |

### Context Managers — Resource Lifecycle Control

A context manager ensures resources are properly acquired and released, even if an exception occurs.

**Using `with`:**
```python
# File — built-in CM
with open("data.csv", "r") as f:
    data = f.read()
# f.close() called automatically, even on exception

# DuckDB connection
import duckdb
with duckdb.connect("telemetry.duckdb") as con:
    results = con.execute("SELECT * FROM daily_metrics").fetchdf()
# Connection closed automatically
```

**Building a custom context manager — class-based:**
```python
class PipelineTimer:
    """Context manager that times a pipeline step."""
    import time

    def __init__(self, name: str):
        self.name = name
        self.start = None

    def __enter__(self):
        self.start = time.perf_counter()
        print(f"[{self.name}] started")
        return self   # available as 'as' target

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.perf_counter() - self.start
        status = "FAILED" if exc_type else "completed"
        print(f"[{self.name}] {status} in {elapsed:.3f}s")
        return False   # don't suppress exceptions

# Usage
with PipelineTimer("telemetry_ingest") as timer:
    process_batch(data)
```

**Building a custom context manager — `contextlib.contextmanager`:**
```python
from contextlib import contextmanager
import structlog

log = structlog.get_logger()

@contextmanager
def pipeline_step(name: str):
    """Log entry/exit and handle errors for a pipeline step."""
    log.info("step_started", step=name)
    try:
        yield
        log.info("step_completed", step=name)
    except Exception as e:
        log.error("step_failed", step=name, error=str(e))
        raise   # re-raise — don't swallow

# Usage
with pipeline_step("load_metrics"):
    load_data(source)

with pipeline_step("transform"):
    transform_data(df)
```

### Production Pattern — Transactional Context Manager

```python
@contextmanager
def duckdb_transaction(db_path: str):
    """Open a DuckDB connection and wrap in a transaction."""
    con = duckdb.connect(db_path)
    con.execute("BEGIN TRANSACTION")
    try:
        yield con
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        con.close()

# Usage
with duckdb_transaction("telemetry.duckdb") as con:
    con.execute("INSERT INTO daily_metrics VALUES (?)", (row,))
    con.execute("UPDATE server_dim SET last_seen = ? WHERE server_id = ?", ...)
    # Commits on success, rolls back on any exception
```

---

## D. Technology — Snowflake-Specific Features (45 min)

### Why Snowflake in Finance

Snowflake is the dominant cloud data warehouse in financial services. Citi, Goldman, JPMorgan all use it. Senior DE interviews at these firms will probe Snowflake-specific concepts.

### Snowflake Architecture Uniqueness

**Separation of storage and compute:**
- Storage: columnar data in S3 (compressed, encrypted)
- Compute: Virtual Warehouses (clusters of servers) that scale independently
- Multiple warehouses can read the same data simultaneously (no contention)
- Warehouses auto-suspend when idle, auto-resume on query

**Virtual Warehouses (compute clusters):**
```sql
-- Create a warehouse (compute cluster)
CREATE WAREHOUSE capacity_planning_wh
    WAREHOUSE_SIZE = 'MEDIUM'       -- XS/S/M/L/XL/2XL-6XL
    AUTO_SUSPEND = 60               -- seconds of inactivity before suspend
    AUTO_RESUME = TRUE
    COMMENT = 'Capacity planning team warehouse';

-- Use it for queries
USE WAREHOUSE capacity_planning_wh;

-- Scale up for heavy workload, then scale back
ALTER WAREHOUSE capacity_planning_wh SET WAREHOUSE_SIZE = 'LARGE';
```

### Time Travel — Built-In History

Snowflake stores historical versions of every table (configurable: 0-90 days for Enterprise).

```sql
-- Query data as it was at a specific time
SELECT * FROM daily_metrics
AT (TIMESTAMP => DATEADD(hours, -2, CURRENT_TIMESTAMP));

-- Query data as it was at a specific statement offset
SELECT * FROM daily_metrics
BEFORE (STATEMENT => '019d8f82-0000-1234-...');

-- Restore a table to a previous state
CREATE OR REPLACE TABLE daily_metrics AS
SELECT * FROM daily_metrics AT (OFFSET => -3600);   -- 1 hour ago
```

**Finance use case:** Regulatory audit — "What did our position table look like at 4pm on the trade date?" No separate audit log required.

### Streams — Change Data Capture (Built-in)

A Snowflake Stream is a CDC object that tracks changes to a table.

```sql
-- Create a stream on a source table
CREATE STREAM server_changes ON TABLE servers;

-- The stream shows new/changed/deleted rows since last consumed
SELECT *
FROM server_changes
WHERE METADATA$ACTION IN ('INSERT', 'UPDATE');
-- METADATA$ACTION: INSERT, DELETE (UPDATE = DELETE + INSERT pair)
-- METADATA$ISUPDATE: TRUE for the update DELETE/INSERT rows
-- METADATA$ROW_ID: unique row identifier for tracking

-- Consume the stream (processing it clears consumed rows)
INSERT INTO server_history
SELECT server_id, tier, region, METADATA$ACTION, CURRENT_TIMESTAMP
FROM server_changes;
```

### Tasks — Native Scheduling

Snowflake Tasks are a built-in scheduler (like a mini-Airflow for Snowflake-only pipelines).

```sql
-- Create a task that runs every 5 minutes
CREATE TASK process_server_changes
    WAREHOUSE = capacity_planning_wh
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('server_changes')   -- only run if stream has data
AS
INSERT INTO server_dim_history
SELECT server_id, tier, region, METADATA$ACTION, CURRENT_TIMESTAMP
FROM server_changes;

-- Enable the task (tasks start suspended)
ALTER TASK process_server_changes RESUME;
```

### Snowpark — Python in Snowflake

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, avg, lit

session = Session.builder.configs({
    "account": "myaccount",
    "user": "svc_capacity",
    "password": "...",
    "warehouse": "capacity_planning_wh",
    "database": "capacity_db",
    "schema": "public"
}).create()

# DataFrame operations run inside Snowflake (not locally)
df = session.table("daily_metrics")
result = (df
    .filter(col("avg_cpu") > 80)
    .group_by("server_id")
    .agg(avg("avg_cpu").alias("mean_cpu"))
    .order_by("mean_cpu", ascending=False)
    .limit(20)
)
result.show()
pandas_df = result.to_pandas()   # pull to local only when needed
```

**Snowpark pushdown:** All transformations run as SQL inside Snowflake's engine. `to_pandas()` triggers the actual computation and data transfer.

### Snowflake vs Alternatives

| Feature | Snowflake | Databricks | BigQuery |
|---------|-----------|-----------|---------|
| Separation of storage/compute | Native | Partial (Delta + clusters) | Native |
| Time Travel | 90 days (Enterprise) | Delta (unlimited with log) | 7 days |
| Built-in CDC | Streams | Delta CDF | N/A |
| Built-in scheduling | Tasks | Workflows | Scheduled queries |
| Multi-cloud | Yes | Yes | Yes (GCP native) |
| Best for | SQL-heavy analytics | ML + notebooks + streaming | Google ecosystem |

---

## Behavioral Anchor — Day 23

> "Tell me about a time you prevented a data quality issue from reaching production."

Strong answers include:
- What check you added and why
- How you built confidence in your detection (testing with known bad data)
- The specific issue it caught in practice
- What the downstream impact would have been without it

---

## Day 23 Checklist

- [ ] Coded "expand around center" palindrome from memory
- [ ] Coded LC #10 (Regex Matching) — understands the `*` zero-occurrence case
- [ ] Coded LC #516 (LPS as LCS of s and reverse) — understands the insight
- [ ] Can describe a Debezium CDC event structure and what `op` values mean
- [ ] Can write the "latest state from CDC stream" SQL from scratch
- [ ] Understands Schema Registry: what it prevents and the compatibility modes
- [ ] Can write a custom context manager using `contextlib.contextmanager`
- [ ] Knows the difference between dataclass `field(default_factory=list)` and `= []`
- [ ] Can describe Snowflake Time Travel and name a finance use case
- [ ] Can explain Streams and Tasks (Snowflake's built-in CDC + scheduler)
- [ ] Knows Snowpark's key benefit: pushdown (computation stays in Snowflake)
