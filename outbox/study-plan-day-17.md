---
created: 2026-03-02
updated: 2026-03-02
summary: Day 17 — Tries (Prefix Trees), Federated SQL with Trino/Presto, Config & Secrets Management in Python, MLflow and Feature Stores.
tags: [study-plan, day-17, tries, federated-sql, trino, config-management, mlflow]
---

# Day 17 — Tries | Federated SQL (Trino) | Config & Secrets | MLflow & Feature Stores

**Theme:** The tools that make systems observable, queryable, and reproducible at scale.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is the backtracking "undo" step and why is it critical?
2. In 2D DP, what does `dp[i][j]` represent in the Edit Distance problem?
3. What is SCD Type 2 and what are the two columns that track history?
4. What is the difference between ABC and typing.Protocol in Python?
5. Name the 4 principles of Data Mesh.
6. What does `@abstractmethod` enforce?

---

## A. LeetCode — Tries (Prefix Trees) (60 min)

### What is a Trie?

A Trie (prefix tree) is a tree where each node represents one character. Words share prefixes — "apple" and "app" share the same `a → p → p` path.

**When to use a Trie:**
- Autocomplete / search suggestions
- Spell checking
- IP routing tables
- Any "does this prefix exist?" query that would be O(n) with a list

### Trie Node Structure

```python
class TrieNode:
    def __init__(self):
        self.children = {}    # char → TrieNode
        self.is_end = False   # True if a word ends at this node
```

### LC #208: Implement Trie (Medium)

**Operations needed:** `insert(word)`, `search(word)`, `startsWith(prefix)`

```python
class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end   # must be a complete word

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True          # prefix exists — don't check is_end
```

**Complexity:** O(m) per operation where m = word length. Space: O(total characters across all words).

---

### LC #211: Design Add and Search Words Data Structure (Medium)

**Adds a wildcard:** `.` matches any single character.

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        return self._dfs(word, 0, self.root)

    def _dfs(self, word, idx, node):
        if idx == len(word):
            return node.is_end
        char = word[idx]
        if char == '.':
            # Wildcard: try all children
            for child in node.children.values():
                if self._dfs(word, idx + 1, child):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._dfs(word, idx + 1, node.children[char])
```

**Key insight:** Wildcard forces branching → use DFS recursion.

---

### LC #212: Word Search II (Hard)

**Problem:** Given a board of characters and a list of words, return all words found in the board. (Combine Word Search I with a Trie.)

```python
def findWords(board, words):
    # Build Trie from word list
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = word   # store word at end node (not just True)

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(r, c, node):
        char = board[r][c]
        if char not in node.children:
            return
        next_node = node.children[char]
        if next_node.is_end:
            result.add(next_node.is_end)   # found a word
            next_node.is_end = False       # dedup — don't add same word twice

        board[r][c] = '#'   # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node)
        board[r][c] = char  # restore

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return list(result)
```

**Why Trie beats brute force here:** Without Trie, you'd call Word Search I for every word separately — O(words × board × 4^word_length). With Trie, all words are searched simultaneously in one pass.

---

### Trie — Interview Summary

| Question | Answer |
|----------|--------|
| Time per operation | O(m) where m = word/prefix length |
| Space | O(alphabet_size × max_word_len × num_words) |
| Best for | Prefix queries, autocomplete, multi-word search |
| Alternative for simple membership | HashSet (O(1) but no prefix search) |
| Wildcard search | DFS within the Trie |

---

## B. SQL — Federated SQL with Trino/Presto (45 min)

### What is Federated SQL?

Federated SQL engines (Trino, Presto, Dremio) let you query multiple data sources in one SQL statement — without moving data first.

```sql
-- Query Postgres, S3 (Hive/Glue), and MySQL in one join
SELECT
    s.server_id,
    s.tier,                              -- from Postgres (config DB)
    m.avg_cpu,                           -- from S3 Parquet (via Hive connector)
    i.incident_count                     -- from MySQL (incidents DB)
FROM postgresql.config.servers s
JOIN hive.warehouse.daily_metrics m ON s.server_id = m.server_id
JOIN mysql.ops.incidents i ON s.server_id = i.server_id
WHERE m.report_date = CURRENT_DATE;
```

### Trino Architecture

```
Client (SQL) → Trino Coordinator
                  ├── Parses + plans the query
                  ├── Splits work across Workers
                  └── Merges results
                        ↓
              Trino Workers (parallel)
                  ├── Connect to Hive/S3 (via Hive connector)
                  ├── Connect to Postgres (via PostgreSQL connector)
                  ├── Connect to Kafka (via Kafka connector)
                  └── Stream results back to coordinator
```

**Key connectors (know these):**
- `hive` — S3 Parquet/ORC via Glue or Hive Metastore
- `postgresql` / `mysql` — JDBC-based relational
- `kafka` — stream the latest N messages from a topic as a table
- `tpcds` / `tpch` — built-in benchmark datasets
- `iceberg` — native Iceberg table support
- `delta` — Delta Lake support (via Delta connector or Hive)

### Trino vs Athena vs Spark SQL

| Dimension | Trino/Presto | Athena | Spark SQL |
|-----------|-------------|--------|-----------|
| Architecture | Separate compute cluster | Serverless (AWS-managed) | Driver + executors |
| Multi-source federation | Native (pluggable connectors) | Limited (only S3/Glue) | Via JDBC + Spark |
| Interactive query speed | Very fast (MPP, no JVM startup) | Fast (serverless, but cold start) | Slower start (JVM + executor allocation) |
| Cost | Cluster cost (EC2) | Per-query (TB scanned) | Cluster cost (EMR/Databricks) |
| Best for | Cross-source analytics, BI tools | Ad hoc S3 queries | Heavy ETL, ML pipelines |

### Trino SQL — Practice Queries

**Setup context:** Imagine you have:
- `hive.warehouse.daily_metrics` — S3 Parquet
- `postgresql.config.servers` — RDS Postgres

**Query 1 — Cross-source enriched report:**
```sql
SELECT
    m.server_id,
    s.tier,
    s.region,
    AVG(m.avg_cpu) OVER (
        PARTITION BY m.server_id
        ORDER BY m.report_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS cpu_7d_avg
FROM hive.warehouse.daily_metrics m
JOIN postgresql.config.servers s
    ON m.server_id = s.server_id
WHERE m.report_date >= CURRENT_DATE - INTERVAL '30' DAY;
```

**Query 2 — Trino-specific functions:**
```sql
-- Trino uses INTERVAL differently than PostgreSQL/DuckDB
SELECT
    server_id,
    date_diff('day', MIN(report_date), MAX(report_date)) AS days_of_data,
    approx_distinct(server_id)                            AS approx_unique_servers
FROM hive.warehouse.daily_metrics
GROUP BY server_id;
```

**Query 3 — Pushdown awareness:**
```sql
-- Trino pushes predicates to the connector when possible
-- Adding a partition column in WHERE → Hive connector skips whole S3 partitions
SELECT * FROM hive.warehouse.daily_metrics
WHERE report_date = DATE '2026-02-26'   -- partition column → S3 partition skip
  AND avg_cpu > 80;                      -- pushed to ORC/Parquet column stats
```

### Trino Interview Points

- **Coordinator bottleneck:** Single coordinator can be a SPOF. Use HA setup with Pinot or a coordinator failover.
- **Memory pressure:** Trino is in-memory MPP. Large joins can OOM. Use `SET SESSION query_max_memory = '10GB'` per session.
- **Graceful restarts:** Workers can be added/removed without coordinator restart.
- **Cost-based optimizer:** Trino has one — but you need table stats. Run `ANALYZE` on Hive tables.

---

## C. Python — Config & Secrets Management (30 min)

### The Problem

Hardcoded credentials in scripts = security incident waiting to happen. But getting config/secrets right is harder than it looks. The goal: secrets NEVER in code or logs, config changes don't require code deploys.

### Layer 1 — Environment Variables (minimum viable)

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL")
API_KEY = os.environ.get("TELEMETRY_API_KEY")

if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL is not set")
```

**Problem:** You need to manage env var injection (`.env` files, CI/CD secrets). Not auditable.

### Layer 2 — `python-dotenv` for local dev

```python
from dotenv import load_dotenv
import os

load_dotenv()   # reads .env file if present (ignored in prod)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
```

**.env file (NEVER commit this):**
```
DB_HOST=db.prod.local
DB_PORT=5432
TELEMETRY_API_KEY=sk-abc123...
```

**.gitignore must contain:**
```
.env
*.env
.env.*
```

### Layer 3 — Pydantic Settings (type-safe, validated)

```python
from pydantic_settings import BaseSettings
from typing import Optional

class PipelineConfig(BaseSettings):
    db_host: str
    db_port: int = 5432
    db_name: str
    api_key: str
    batch_size: int = 1000
    dry_run: bool = False
    log_level: str = "INFO"

    class Config:
        env_file = ".env"              # fallback for local dev
        env_file_encoding = "utf-8"
        case_sensitive = False         # DB_HOST or db_host both work

config = PipelineConfig()   # raises ValidationError if required fields missing
print(config.db_host)       # type: str — mypy knows this
```

**Why Pydantic Settings is the right answer in interviews:**
- Type validation at startup (fail fast, not mid-run)
- Documentation baked in (field = type hint + default)
- Reads from env vars, `.env`, or nested config (priority chain)

### Layer 4 — AWS Secrets Manager (production)

```python
import boto3
import json
from functools import lru_cache

@lru_cache(maxsize=None)
def get_secret(secret_name: str) -> dict:
    """Fetch secret from AWS Secrets Manager. Cached after first call."""
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])

# Usage
db_creds = get_secret("prod/telemetry/db")
db_host = db_creds["host"]
db_password = db_creds["password"]
```

**Rotation:** Secrets Manager can auto-rotate credentials (RDS, Redshift) on a schedule. Lambda is triggered, new password generated, old one expires.

### Config for Airflow

```python
# In DAGs — use Airflow Connections and Variables
from airflow.hooks.base import BaseHook
from airflow.models import Variable

# Connection (credentials stored in Airflow metastore, encrypted)
conn = BaseHook.get_connection("my_postgres_conn")
db_host = conn.host
db_password = conn.password

# Variable (non-sensitive config)
batch_size = int(Variable.get("telemetry_batch_size", default_var=1000))
```

### Security Checklist — Never Break These Rules

- [ ] No secrets in code (including comments)
- [ ] No secrets in logs (`logging.info(f"Connecting with password={pwd}")` is a violation)
- [ ] `.env` in `.gitignore`
- [ ] Secrets Manager or Vault in prod, never plain env files on EC2
- [ ] IAM roles for AWS access (not access keys if avoidable)
- [ ] Secrets rotated on schedule

---

## D. Technology — MLflow & Feature Stores (45 min)

### Why DE Needs to Know This

Data engineers build the pipelines that feed ML models. In mature orgs, DE owns the feature store and model artifact storage. Understanding MLflow and feature stores is what separates a "pipeline builder" from a "senior ML-adjacent DE."

### MLflow Components

**1. Tracking — experiment logging**
```python
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LinearRegression

mlflow.set_experiment("cpu_forecasting")

with mlflow.start_run(run_name="linear_baseline"):
    # Log parameters
    mlflow.log_param("model_type", "linear_regression")
    mlflow.log_param("feature_window_days", 30)

    # Train
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Log metrics
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("r2", r2_score(y_test, y_pred))

    # Log the model artifact
    mlflow.sklearn.log_model(model, "model", registered_model_name="cpu_forecast")
```

**2. Model Registry — lifecycle management**
```
Stages: None → Staging → Production → Archived

Promoting to Production:
  mlflow.MlflowClient().transition_model_version_stage(
      name="cpu_forecast",
      version=3,
      stage="Production"
  )
```

**3. Model Serving (MLflow Models)**
```bash
# Serve a registered model locally
mlflow models serve -m "models:/cpu_forecast/Production" -p 5000

# Predict
curl -X POST http://localhost:5000/invocations \
     -H "Content-Type: application/json" \
     -d '{"dataframe_records": [{"cpu_7d_avg": 78.3, "mem_util": 65.1}]}'
```

### Feature Stores — What and Why

A feature store solves: "how do I share ML features between teams, ensure training/serving consistency, and avoid recomputing the same features?"

**Two stores in one:**
- **Offline store** (historical, for training): Parquet on S3, Delta Lake, BigQuery
- **Online store** (real-time, for inference): Redis, DynamoDB, Cassandra — low latency

```
Feature Pipeline (batch):
  raw data → compute features → write to offline store (S3 Parquet)
                              → write to online store (Redis)

Training:
  historical features ← offline store

Serving:
  real-time features ← online store (< 10ms lookup)
```

### Feast (Open Source Feature Store)

```python
from feast import FeatureStore

store = FeatureStore(repo_path=".")

# Get historical features for training
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "server_stats:cpu_7d_avg",
        "server_stats:mem_util",
        "server_stats:disk_iops",
    ]
).to_df()

# Get online features for inference
features = store.get_online_features(
    features=["server_stats:cpu_7d_avg"],
    entity_rows=[{"server_id": "srv-001"}]
).to_dict()
```

### DE's Role in the ML Platform

| Component | Who Builds | Who Owns |
|-----------|-----------|----------|
| Raw telemetry pipeline | DE | DE |
| Feature computation pipeline | DE + MLE | DE |
| Feature store infra (Feast, DynamoDB) | Platform/DE | Platform |
| MLflow tracking server | Platform/DE | Platform |
| Model training code | MLE | MLE |
| Model serving infra | MLE + Platform | Platform |
| Feature SLA monitoring | DE | DE |

**Interview framing:**
> "The DE owns the data that feeds the model and the feature pipelines. We don't train models, but we guarantee the features are correct, fresh, and consistent between training and serving. Training/serving skew is a data problem before it's an ML problem."

### Point-in-Time Correct Joins (Critical DE Concept for ML)

When building training data, you must never use features from the future relative to the label timestamp. This is **data leakage**.

```python
# Wrong: uses ALL history to compute features, not just what was known at prediction time
training_df = pd.merge(labels, all_features, on="server_id")

# Correct: use Feast's point-in-time join
# entity_df has an "event_timestamp" column — Feast joins features that were
# available AT THAT TIMESTAMP only
training_df = store.get_historical_features(
    entity_df=entity_df_with_timestamps,
    features=["server_stats:cpu_7d_avg"],
).to_df()
```

---

## Behavioral Anchor — Day 17

> "Tell me about a time you made a system easier for others to use."

Strong answers cover:
- A real pain point you observed (others frustrated, slow, error-prone)
- Your solution (tooling, abstraction, documentation)
- Adoption and measurable improvement

For Sean: consider stories around making monitoring/alerting accessible to non-DE teams.

---

## Day 17 Checklist

- [ ] Implemented Trie from scratch: `insert`, `search`, `startsWith`
- [ ] Can code LC #211 wildcard search using DFS
- [ ] Understand why Trie beats brute force for multi-word search (LC #212)
- [ ] Can describe Trino architecture: coordinator + workers + connectors
- [ ] Can contrast Trino vs Athena vs Spark SQL
- [ ] Implemented PydanticSettings config class from scratch
- [ ] Know the AWS Secrets Manager pattern (boto3 + `lru_cache`)
- [ ] Can explain MLflow's 3 components: Tracking, Registry, Serving
- [ ] Can explain what a feature store solves and the two stores it contains
- [ ] Know what point-in-time correct joins are and why they matter
