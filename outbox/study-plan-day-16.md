---
created: 2026-03-02
updated: 2026-03-02
summary: Day 16 — 2D Dynamic Programming, SCD Type 2 MERGE SQL, typing.Protocol and ABC in Python, Data Mesh Architecture.
tags: [study-plan, day-16, dynamic-programming, scd, data-mesh, python-protocols]
---

# Day 16 — 2D Dynamic Programming | SCD MERGE SQL | typing.Protocol + ABC | Data Mesh

**Theme:** Senior engineers think in abstractions. Today you learn 2D DP tables, dimensional modeling updates, Python interfaces, and modern data governance architecture.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is the backtracking template? Write the 5-line skeleton.
2. In DuckDB JSON, what is the difference between `->` and `->>`?
3. What does `structlog.bind()` do?
4. Name three things Spark's Catalyst optimizer does automatically.
5. What is AQE and what is the most important problem it solves?
6. In Kafka, you have 10 partitions and 11 consumers in the same group. What happens to the 11th consumer?

---

## A. LeetCode — 2D Dynamic Programming (60 min)

### Why 2D DP

1D DP tracks one dimension of state (e.g., "best sum ending here"). 2D DP tracks two dimensions simultaneously — length, subsequence, grid position — and is the foundation for:
- Edit distance (Levenshtein) — string similarity
- Longest Common Subsequence — diff algorithms, gene alignment
- Unique paths — robot navigation, grid problems
- Coin change with denomination tracking

**Mental model:** Build a table where `dp[i][j]` = the answer for sub-problem involving first `i` elements of A and first `j` elements of B (or grid position `(i,j)`).

---

### Problem 1 — LC #62: Unique Paths (Medium)

**Problem:** A robot is on an m×n grid. It can only move right or down. How many unique paths from top-left to bottom-right?

```
Input:  m=3, n=7
Output: 28
```

**2D DP approach:**

```python
def uniquePaths(m, n):
    # dp[i][j] = number of ways to reach cell (i, j)
    dp = [[1] * n for _ in range(m)]   # base: first row and col all 1

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]   # came from above or left

    return dp[m-1][n-1]
```

**Space optimization (1D rolling array):**
```python
def uniquePaths(m, n):
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]   # dp[j] = above (old dp[j]) + left (dp[j-1])
    return dp[n-1]
```

**Complexity:** O(m×n) time, O(n) space after optimization.

---

### Problem 2 — LC #1143: Longest Common Subsequence (Medium)

**Problem:** Given two strings `text1` and `text2`, return the length of their longest common subsequence. A subsequence doesn't require contiguous characters.

```
Input:  text1 = "abcde", text2 = "ace"
Output: 3  (common subsequence: "ace")
```

```python
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    # dp[i][j] = LCS of text1[:i] and text2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1    # extend matching chars
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # skip one char

    return dp[m][n]
```

**Recurrence explained:**
- If characters match: extend the LCS from the diagonally preceding sub-problem
- If they don't match: take the best of "skip last char of text1" vs "skip last char of text2"

---

### Problem 3 — LC #72: Edit Distance (Hard)

**Problem:** Given two strings `word1` and `word2`, return the minimum number of operations (insert, delete, replace) to convert word1 to word2.

```
Input:  word1 = "horse", word2 = "ros"
Output: 3  (horse → rorse → rose → ros)
```

```python
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    # dp[i][j] = edit distance between word1[:i] and word2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: convert to/from empty string
    for i in range(m + 1): dp[i][0] = i   # delete all of word1
    for j in range(n + 1): dp[0][j] = j   # insert all of word2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]              # no operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],     # delete from word1
                    dp[i][j-1],     # insert into word1
                    dp[i-1][j-1]    # replace
                )

    return dp[m][n]
```

---

### Problem 4 — LC #64: Minimum Path Sum (Medium)

**Problem:** Given an m×n grid filled with non-negative numbers, find the path from top-left to bottom-right that minimizes the sum of all numbers along the path. Can only move right or down.

```
Input:  [[1,3,1],[1,5,1],[4,2,1]]
Output: 7  (path: 1→3→1→1→1)
```

```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])

    # In-place modification (avoids extra space)
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]   # only came from left
            elif j == 0:
                grid[i][j] += grid[i-1][j]   # only came from above
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])

    return grid[m-1][n-1]
```

---

### 2D DP Pattern Recognition

| Problem | `dp[i][j]` represents | Recurrence |
|---------|----------------------|------------|
| Unique Paths | # paths to (i,j) | `dp[i-1][j] + dp[i][j-1]` |
| LCS | LCS of first i of A, first j of B | match: `dp[i-1][j-1]+1`, else `max(skip)` |
| Edit Distance | edit ops between word1[:i], word2[:j] | match: `dp[i-1][j-1]`, else `1+min(3 ops)` |
| Min Path Sum | min cost to reach (i,j) | `grid[i][j] + min(above, left)` |

---

## B. SQL — SCD Type 2 with MERGE (45 min)

### What is SCD Type 2?

Slowly Changing Dimension Type 2 = track full history by adding new rows when an attribute changes.

**When a server moves from tier "standard" to tier "premium":**
- Type 1: Overwrite (no history)
- Type 2: Expire the old row, insert a new row with new effective dates

**Schema:**
```sql
CREATE TABLE server_dim (
    surrogate_key    INTEGER PRIMARY KEY,
    server_id        VARCHAR,
    tier             VARCHAR,
    region           VARCHAR,
    valid_from       DATE,
    valid_to         DATE,        -- NULL means "current"
    is_current       BOOLEAN
);
```

### MERGE Statement (UPSERT)

Most data warehouses support MERGE (Snowflake, BigQuery, Databricks SQL, PostgreSQL 15+).

```sql
-- Staging table with today's snapshot of all servers
-- server_staging(server_id, tier, region, snapshot_date)

MERGE INTO server_dim AS target
USING (
    SELECT
        s.server_id,
        s.tier,
        s.region,
        s.snapshot_date
    FROM server_staging s
) AS source ON (target.server_id = source.server_id AND target.is_current = TRUE)

-- CASE 1: Server exists and something changed → expire the old row
WHEN MATCHED AND (
    target.tier    != source.tier OR
    target.region  != source.region
) THEN UPDATE SET
    valid_to   = source.snapshot_date - INTERVAL '1 day',
    is_current = FALSE

-- CASE 2: No change → do nothing (implicit — MATCHED without action)

-- CASE 3: New server (not in target at all) → handled by INSERT below
WHEN NOT MATCHED THEN INSERT (
    surrogate_key, server_id, tier, region, valid_from, valid_to, is_current
) VALUES (
    NEXTVAL('server_dim_seq'),
    source.server_id,
    source.tier,
    source.region,
    source.snapshot_date,
    NULL,
    TRUE
);

-- CASE 4: After MERGE, insert new row for changed servers
-- (MERGE alone can't insert for matched+changed — do in a second pass)
INSERT INTO server_dim (surrogate_key, server_id, tier, region, valid_from, valid_to, is_current)
SELECT
    NEXTVAL('server_dim_seq'),
    s.server_id,
    s.tier,
    s.region,
    s.snapshot_date,
    NULL,
    TRUE
FROM server_staging s
JOIN server_dim d ON s.server_id = d.server_id
WHERE d.is_current = FALSE
  AND d.valid_to = s.snapshot_date - INTERVAL '1 day'
  AND NOT EXISTS (
      SELECT 1 FROM server_dim d2
      WHERE d2.server_id = s.server_id AND d2.is_current = TRUE
  );
```

### Practice Query — Point-in-Time Lookup

**Problem:** What tier was server `srv-001` on `2025-12-01`?

```sql
SELECT tier, region
FROM server_dim
WHERE server_id = 'srv-001'
  AND valid_from <= '2025-12-01'
  AND (valid_to IS NULL OR valid_to >= '2025-12-01');
```

### dbt SCD Type 2 (snapshot)

In dbt, instead of writing MERGE by hand, you use **snapshots**:

```yaml
# snapshots/server_snapshot.sql
{% snapshot server_snapshot %}
    {{
        config(
            target_schema='snapshots',
            unique_key='server_id',
            strategy='check',
            check_cols=['tier', 'region'],
        )
    }}
    SELECT * FROM {{ source('raw', 'servers') }}
{% endsnapshot %}
```

dbt generates `dbt_scd_id`, `dbt_updated_at`, `dbt_valid_from`, `dbt_valid_to` automatically.

---

## C. Python — `typing.Protocol` and `ABC` (30 min)

### Why Interfaces Matter in DE

Large pipelines have many interchangeable components: different ingestion sources, different writers (S3, local, BigQuery). Without interfaces, you end up with `if source_type == "kafka"` chains everywhere. Interfaces let you swap implementations without changing the code that calls them.

### Abstract Base Classes (ABC) — enforce at definition time

```python
from abc import ABC, abstractmethod
from typing import Iterator
import pandas as pd

class DataSource(ABC):
    """All data sources must implement these methods."""

    @abstractmethod
    def connect(self) -> None:
        """Establish connection."""
        ...

    @abstractmethod
    def read(self) -> Iterator[pd.DataFrame]:
        """Yield DataFrames in batches."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Release resources."""
        ...

    def read_all(self) -> pd.DataFrame:
        """Concrete method — uses abstract read()."""
        return pd.concat(list(self.read()), ignore_index=True)


class KafkaSource(DataSource):
    def __init__(self, topic: str, bootstrap_servers: str):
        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self._consumer = None

    def connect(self) -> None:
        # self._consumer = KafkaConsumer(...)
        print(f"Connected to Kafka topic: {self.topic}")

    def read(self) -> Iterator[pd.DataFrame]:
        # Yield batches from Kafka
        yield pd.DataFrame({"msg": ["batch_1"]})

    def close(self) -> None:
        if self._consumer:
            self._consumer.close()

# ABC enforces at instantiation — won't let you create KafkaSource if a method is missing
```

### `typing.Protocol` — structural subtyping (duck typing with hints)

`Protocol` doesn't require inheritance. Any class that has the right methods satisfies the protocol automatically — this is called **structural subtyping**.

```python
from typing import Protocol, Iterator, runtime_checkable
import pandas as pd

@runtime_checkable
class DataSource(Protocol):
    def connect(self) -> None: ...
    def read(self) -> Iterator[pd.DataFrame]: ...
    def close(self) -> None: ...

# This class does NOT inherit from DataSource
class CSVSource:
    def __init__(self, path: str):
        self.path = path

    def connect(self) -> None:
        print(f"Opening {self.path}")

    def read(self) -> Iterator[pd.DataFrame]:
        yield pd.read_csv(self.path)

    def close(self) -> None:
        pass

# Works with Protocol — even without explicit inheritance
def run_pipeline(source: DataSource) -> None:
    source.connect()
    for batch in source.read():
        print(f"Processing {len(batch)} rows")
    source.close()

csv = CSVSource("data.csv")
run_pipeline(csv)  # type: ignore — but mypy approves because CSVSource satisfies DataSource

# isinstance check works with @runtime_checkable
print(isinstance(csv, DataSource))  # True
```

### ABC vs Protocol — When to Use Which

| Feature | ABC | Protocol |
|---------|-----|---------|
| Enforcement | Instantiation-time error if abstract method missing | Only checked by mypy/pyright (not at runtime by default) |
| Inheritance required | Yes — must `class Foo(MyABC)` | No — structural ("if it has the methods, it qualifies") |
| Best for | Internal framework, you control all implementations | External/third-party code, open extension |
| Concrete methods | Yes (`@property`, default impl) | No (only `...` stubs) |
| Common in DE | Plugin architectures, base pipeline classes | Type hints for external adapters, testing mocks |

### Generic Typed Pipeline (putting it together)

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Pipeline(Generic[T]):
    def __init__(self, source: DataSource, transformer, sink):
        self.source = source
        self.transformer = transformer
        self.sink = sink

    def run(self) -> None:
        self.source.connect()
        for batch in self.source.read():
            transformed = self.transformer(batch)
            self.sink.write(transformed)
        self.source.close()
```

---

## D. Technology — Data Mesh Architecture (45 min)

### What is Data Mesh?

Data Mesh (coined by Zhamak Dehghani, 2019) is a decentralized data architecture pattern. Instead of a central data team owning all pipelines, domain teams own their own data products.

**The 4 principles:**
1. **Domain ownership** — teams that create the data own the data pipelines
2. **Data as a product** — data treated with SLAs, documentation, versioning (not raw dumps)
3. **Self-serve data platform** — infra team provides tools, domain teams self-service
4. **Federated computational governance** — global standards (PII, data types) enforced automatically

### Monolithic Data Lake vs Data Mesh

| Dimension | Monolithic Lake | Data Mesh |
|-----------|----------------|-----------|
| Ownership | Central data team | Domain teams |
| Bottleneck | Central team is the bottleneck | Each domain scales independently |
| Quality | Central team may not understand domain data | Domain team knows the data best |
| Governance | Enforced manually by gatekeeping | Federated — policy as code |
| Failure mode | Central team outage affects all consumers | Domain failures are isolated |
| Best for | Small orgs, limited domains | Large orgs, many domains, scaling pain |

### Data Product Specification

A "data product" is more than a table. It has:
- **Schema** (versioned, documented)
- **SLA** (freshness guarantee: "updated by 9am daily")
- **Data quality contracts** (row counts, null checks, value ranges)
- **Ownership** (team, Slack channel, oncall)
- **Access control** (who can query, who can consume)
- **Lineage** (where the data came from)

```yaml
# data-product.yaml
name: server_capacity_metrics
domain: infrastructure
owner: infra-platform-team
sla:
  freshness: "daily by 06:00 UTC"
  availability: "99.5%"
schema:
  version: "2.1.0"
  columns:
    - name: server_id
      type: VARCHAR
      description: "Unique server identifier"
      nullable: false
    - name: avg_cpu_7d
      type: FLOAT
      description: "7-day trailing average CPU utilization"
quality_contracts:
  - "no nulls in server_id"
  - "avg_cpu_7d between 0 and 100"
  - "row count > 5000 daily"
access:
  consumers: [finance-team, capacity-planning-team]
  pii: false
```

### Implementation on AWS

```
Domain teams self-serve using:
  - AWS Glue Data Catalog → register schemas
  - S3 (per-domain prefix /domain=infra/product=capacity_metrics/)
  - Athena or Redshift Spectrum → federated query across domains
  - Lake Formation → column-level, row-level access control
  - AWS Data Exchange (optional) → publish data products externally

Governance layer:
  - Great Expectations / dbt tests → quality contracts as code
  - Apache Atlas or OpenMetadata → catalog + lineage
  - EventBridge → trigger downstream when data product is updated
```

### Where Data Mesh Fits in Interviews

When asked about designing data platforms for large organizations:
- Mention Data Mesh as the alternative to the "central lake" pattern
- Know when NOT to use it: small orgs, limited domains, immature data engineering culture
- Know the failure modes: domain teams don't have DE skills, governance gaps, data discoverability problems
- Frame your APM experience: "In the APM space I saw centralized monitoring fail at scale — domain teams need ownership of their telemetry."

### Key Terminology for Interviews

| Term | What It Means |
|------|--------------|
| Data product | A versioned, documented, SLA-backed dataset with an owner |
| Federated governance | Global rules (PII, compliance) enforced automatically, not by gatekeeping |
| Self-serve platform | Infrastructure team builds tools; domain teams provision their own pipelines |
| Domain | Business unit with bounded context (e.g., Sales, Infrastructure, Finance) |
| Data contract | Machine-readable schema + quality + SLA agreement between producer and consumer |
| Data catalog | Searchable index of all data products (Apache Atlas, OpenMetadata, AWS Glue) |

---

## Behavioral Anchor — Day 16

> "Describe a time you had to convince stakeholders to adopt a new architecture or process."

Frame answer around:
- Old way was failing (the pain)
- You researched alternatives and made a case with data
- You addressed concerns specifically
- Adoption was measurable (X teams onboarded, Y% reduction in incidents)

This maps naturally to Data Mesh if you've pushed for domain ownership of monitoring/telemetry.

---

## Day 16 Checklist

- [ ] Coded all 4 2D DP problems without looking at solutions
- [ ] Can explain the LCS recurrence in words, not just code
- [ ] Can write the Edit Distance base cases from memory
- [ ] Wrote a MERGE statement for SCD Type 2 from scratch
- [ ] Know what dbt `snapshot` does and its 3 config fields
- [ ] Can explain ABC vs Protocol with one concrete example each
- [ ] Can describe Data Mesh in 4 principles without reading
- [ ] Know when Data Mesh is NOT the right answer
