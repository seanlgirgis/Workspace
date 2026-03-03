---
created: 2026-03-02
updated: 2026-03-02
summary: Day 18 — Bit Manipulation, Advanced String/Array SQL, Python Packaging with uv/poetry, and Kubernetes for Data Engineers.
tags: [study-plan, day-18, bit-manipulation, sql-strings, python-packaging, kubernetes]
---

# Day 18 — Bit Manipulation | Advanced Array/String SQL | Python Packaging | Kubernetes for DE

**Theme:** The final technical day before interview simulation. Fill the last gaps.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. What is the time complexity of Trie `insert` and `search`?
2. In LC #211, how does wildcard `.` force a different algorithm than exact search?
3. What does federated SQL mean and name two engines that do it?
4. What is point-in-time correct joining and why does it matter?
5. In Pydantic Settings, what happens if a required field is not in the environment?
6. What are the two stores in a feature store and what is each used for?

---

## A. LeetCode — Bit Manipulation (60 min)

### Why Bit Manipulation

Not asked frequently — but when it appears it's a differentiator. Also: understanding bit ops makes you a better systems engineer (flags, masks, permissions). Most bit manipulation problems have O(1) or O(log n) solutions vs O(n) for naive approaches.

### Core Operations — Know These Cold

```python
# AND  (&)  — both bits must be 1
# OR   (|)  — either bit is 1
# XOR  (^)  — bits differ (1 if different, 0 if same)
# NOT  (~)  — flip all bits (in Python: ~n = -(n+1) due to two's complement)
# Left shift  (<<)  — multiply by 2 per shift: n << 1 = n * 2
# Right shift (>>)  — divide by 2 per shift: n >> 1 = n // 2

# Check if bit i is set
is_set = (n >> i) & 1

# Set bit i
n = n | (1 << i)

# Clear bit i
n = n & ~(1 << i)

# Toggle bit i
n = n ^ (1 << i)

# Check if n is a power of 2
is_pow2 = n > 0 and (n & (n - 1)) == 0

# Get lowest set bit (isolate rightmost 1)
lowest = n & (-n)

# Clear lowest set bit
n = n & (n - 1)
```

---

### Problem 1 — LC #191: Number of 1 Bits (Easy)

**Problem:** Write a function that takes a positive integer and returns the number of '1' bits in its binary representation (Hamming weight).

```
Input:  11  (binary: 00000000000000000000000000001011)
Output: 3
```

```python
def hammingWeight(n: int) -> int:
    count = 0
    while n:
        count += n & 1    # check if LSB is 1
        n >>= 1           # shift right
    return count

# Better: Brian Kernighan's algorithm
def hammingWeight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1        # clears the lowest set bit each time
        count += 1
    return count

# One-liner (Python)
def hammingWeight(n: int) -> int:
    return bin(n).count('1')
```

**Key insight:** `n & (n-1)` always clears exactly the lowest set bit. So if you loop until n=0, you loop exactly as many times as there are 1-bits.

---

### Problem 2 — LC #338: Counting Bits (Easy)

**Problem:** Given n, return an array of length n+1 where `ans[i]` = number of 1 bits in `i`.

```
Input:  5
Output: [0, 1, 1, 2, 1, 2]
```

**O(n) DP solution using the pattern:**
- `i >> 1` = `i // 2` (just `i` with last bit removed)
- `i & 1` = 1 if i is odd, 0 if even

```python
def countBits(n: int) -> list:
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp
```

**Why this works:** `i` has the same number of 1-bits as `i//2` PLUS 1 if `i` is odd.

---

### Problem 3 — LC #136: Single Number (Easy)

**Problem:** Every element in `nums` appears twice except for one. Find the single element. O(n) time, O(1) space.

```
Input:  [4, 1, 2, 1, 2]
Output: 4
```

```python
def singleNumber(nums: list) -> int:
    result = 0
    for num in nums:
        result ^= num   # XOR: a ^ a = 0, a ^ 0 = a
    return result
```

**Why XOR works:** `a ^ a = 0` for any value. All paired numbers cancel. The singleton survives. Order doesn't matter.

---

### Problem 4 — LC #371: Sum of Two Integers (Medium)

**Problem:** Calculate sum of two integers without using `+` or `-`.

```python
def getSum(a: int, b: int) -> int:
    # In Python, integers are arbitrary precision — mask to 32 bits
    mask = 0xFFFFFFFF
    while b & mask:
        carry = (a & b) << 1     # where carries will be added
        a = a ^ b                 # XOR = sum without carry
        b = carry
    # Handle Python's infinite precision negative numbers
    return a if a <= 0x7FFFFFFF else ~(a ^ mask)
```

**Concept:** XOR gives the sum without carries. AND gives the carry positions. Shift carry left by 1 and repeat until no carries remain.

---

### Problem 5 — LC #268: Missing Number (Easy)

**Problem:** Given array containing n distinct numbers in range [0, n], find the missing one.

```python
def missingNumber(nums: list) -> int:
    # Method 1: XOR — XOR all indices AND all values; pairs cancel
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

# Method 2: Math
def missingNumber(nums: list) -> int:
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
```

---

### Bit Manipulation Cheat Sheet

| Pattern | Code | Use case |
|---------|------|----------|
| Count 1-bits | `n & (n-1)` in loop | Hamming weight |
| XOR pairs | `a ^ b` | Find unique, swap without temp |
| Isolate LSB | `n & (-n)` | Power of 2 check, segment trees |
| Is power of 2 | `n & (n-1) == 0` | Alignment checks |
| Check bit i | `(n >> i) & 1` | Bitmask flags |
| Set bit i | `n \| (1 << i)` | Enable a flag |
| Clear bit i | `n & ~(1 << i)` | Disable a flag |

---

## B. SQL — Advanced Array and String Functions (45 min)

### Why String/Array SQL Matters

Raw telemetry arrives dirty: hostnames with suffixes, pipe-delimited tags, version strings. Senior DE interviews test: can you clean and reshape this data in-database?

### String Functions Practice

```sql
-- Setup
CREATE TABLE raw_servers AS
SELECT * FROM (VALUES
    ('SRV-001.prod.us-east.internal', 'web|production|critical', '2.14.3'),
    ('SRV-002.staging.eu-west.internal', 'db|staging', '2.13.1'),
    ('SRV-003.prod.us-west.internal', 'web|production', '2.14.3'),
    ('SRV-004.dev.us-east.internal', 'cache|dev', '2.15.0-beta')
) AS t(hostname, tags, version);

-- 1. Extract components from structured hostname
SELECT
    hostname,
    SPLIT_PART(hostname, '.', 1)   AS server_id,     -- SRV-001
    SPLIT_PART(hostname, '.', 2)   AS environment,   -- prod
    SPLIT_PART(hostname, '.', 3)   AS region,         -- us-east
    REGEXP_REPLACE(hostname, '\.internal$', '') AS clean_fqdn
FROM raw_servers;

-- 2. Parse version string into components
SELECT
    version,
    SPLIT_PART(version, '.', 1)::INT AS major,
    SPLIT_PART(version, '.', 2)::INT AS minor,
    SPLIT_PART(version, '.', 3)      AS patch_raw,
    REGEXP_EXTRACT(version, '^(\d+\.\d+\.\d+)') AS stable_version
FROM raw_servers;

-- 3. Split pipe-delimited tags into rows (DuckDB UNNEST + STRING_SPLIT)
SELECT
    hostname,
    UNNEST(STRING_SPLIT(tags, '|')) AS tag
FROM raw_servers;

-- 4. Pivot: is this server "production"?
SELECT
    hostname,
    CASE WHEN tags LIKE '%production%' THEN TRUE ELSE FALSE END AS is_production,
    CASE WHEN tags LIKE '%critical%'   THEN TRUE ELSE FALSE END AS is_critical
FROM raw_servers;
```

### Array Functions in DuckDB

```sql
-- Working with native arrays
CREATE TABLE server_tags AS
SELECT
    SPLIT_PART(hostname, '.', 1) AS server_id,
    STRING_SPLIT(tags, '|') AS tag_array   -- native VARCHAR[] type
FROM raw_servers;

-- Query array content
SELECT
    server_id,
    tag_array,
    len(tag_array)                             AS num_tags,
    array_contains(tag_array, 'production')    AS is_production,
    array_filter(tag_array, x -> x != 'dev')   AS non_dev_tags
FROM server_tags;

-- Unnest array + aggregate back
SELECT
    tag,
    COUNT(*) AS server_count,
    LIST(server_id) AS servers
FROM (
    SELECT server_id, UNNEST(tag_array) AS tag FROM server_tags
)
GROUP BY tag
ORDER BY server_count DESC;
```

### Full Pipeline Query — Clean and Aggregate

**Problem:** From raw_servers, produce a clean report: server_id, environment, region, major_version, is_production, tag_count.

```sql
SELECT
    LOWER(SPLIT_PART(hostname, '.', 1))                AS server_id,
    SPLIT_PART(hostname, '.', 2)                       AS environment,
    SPLIT_PART(hostname, '.', 3)                       AS region,
    SPLIT_PART(version, '.', 1)::INT                   AS major_version,
    CASE WHEN tags LIKE '%production%' THEN TRUE
         ELSE FALSE END                                AS is_production,
    len(STRING_SPLIT(tags, '|'))                       AS tag_count
FROM raw_servers
ORDER BY is_production DESC, server_id;
```

### Regex in SQL — Key Patterns

| Function | Purpose | Example |
|----------|---------|---------|
| `REGEXP_MATCHES(s, pattern)` | Returns TRUE/FALSE | Filter hostnames |
| `REGEXP_EXTRACT(s, pattern)` | Returns first match group | Extract version number |
| `REGEXP_REPLACE(s, pat, rep)` | Replace matches | Clean suffixes |
| `REGEXP_SPLIT_TO_TABLE` | Split on regex (Postgres) | Split on multiple delimiters |

---

## C. Python — Packaging with uv and poetry (30 min)

### Why This Matters

A senior DE who can't properly package a pipeline tool is a liability. Interviewers notice if you say "I just pip install things on the server." Modern DE packaging uses isolated environments, locked dependencies, and reproducible builds.

### The Landscape

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| `pip` | Install packages | Script-level, not for projects |
| `venv` + `pip` + `requirements.txt` | Basic isolated env | Legacy, simple projects |
| `poetry` | Dependency management + packaging + lock file | Production pipelines, packages |
| `uv` | Ultra-fast package manager (Rust) | Modern default, replaces pip + venv |
| `conda` | Env + non-Python deps (BLAS, CUDA) | Data science, ML with native deps |

### uv — The Modern Standard

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create project with virtual env
uv init telemetry-pipeline
cd telemetry-pipeline

# Add dependencies (writes to pyproject.toml + uv.lock)
uv add pandas duckdb pydantic-settings structlog

# Add dev dependencies
uv add --dev pytest ruff mypy

# Run script in project env (no activation needed)
uv run python pipeline.py

# Run tests
uv run pytest

# Lock + sync (reproducible install from uv.lock)
uv sync
```

### Project Structure (what `uv init` generates)

```
telemetry-pipeline/
├── pyproject.toml       ← project metadata + deps
├── uv.lock              ← exact pinned versions (commit this!)
├── .python-version      ← python version pin
├── src/
│   └── telemetry_pipeline/
│       ├── __init__.py
│       ├── ingestion.py
│       └── transforms.py
└── tests/
    └── test_ingestion.py
```

### pyproject.toml (modern Python packaging standard)

```toml
[project]
name = "telemetry-pipeline"
version = "0.1.0"
description = "Server telemetry ingestion and capacity planning pipeline"
requires-python = ">=3.11"
dependencies = [
    "pandas>=2.0",
    "duckdb>=0.10",
    "pydantic-settings>=2.0",
    "structlog>=23.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.4", "mypy>=1.9"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]  # pycodestyle errors, pyflakes, isort

[tool.mypy]
python_version = "3.11"
strict = true
```

### Makefile for Common Tasks

```makefile
.PHONY: install test lint typecheck run

install:
    uv sync

test:
    uv run pytest tests/ -v

lint:
    uv run ruff check src/ tests/

typecheck:
    uv run mypy src/

run:
    uv run python -m telemetry_pipeline
```

### AWS Lambda Packaging (DE-specific)

```bash
# Lambda requires a zip with dependencies
uv export --format requirements-txt > requirements.txt
pip install -r requirements.txt -t package/
cp -r src/telemetry_pipeline package/
cd package && zip -r ../lambda.zip .
aws lambda update-function-code \
    --function-name telemetry-ingest \
    --zip-file fileb://../lambda.zip
```

### Interview-Ready Answer

**Q: "How do you manage Python dependencies in your pipelines?"**
> "For production pipelines I use uv with pyproject.toml and a committed lock file — this guarantees the same exact versions in dev, CI, and prod. For Lambda I export requirements.txt from the lock and build a deployment zip. I never pip install globally; each project gets an isolated environment. For multi-service repos, I use namespace packages within a monorepo structure."

---

## D. Technology — Kubernetes for Data Engineers (45 min)

### Why DE Needs to Know K8s

Airflow on Kubernetes is the production standard (KubernetesExecutor). Spark on K8s (via spark-operator) is replacing YARN clusters. dbt runs as K8s jobs. Lambda alternatives (when more than 15 min) run as K8s Jobs.

### Core Concepts DE Needs (not the full K8s syllabus)

**Pod** — the smallest deployable unit. One or more containers sharing network and storage.

**Job** — runs a pod to completion (batch workload). For pipeline steps.

**CronJob** — runs a Job on a schedule (like Airflow DagRuns without Airflow).

**Deployment** — keeps N replicas of a pod running (for services, not batch).

**ConfigMap** — inject config as env vars or files.

**Secret** — like ConfigMap but for sensitive data (base64-encoded, not encrypted by default — use Sealed Secrets or External Secrets Operator in prod).

**Namespace** — logical isolation within a cluster (e.g., `namespace: data-platform`).

**ResourceQuota** — limit CPU/memory per namespace (prevents a runaway Spark job from starving other services).

### A Pipeline Job in Kubernetes

```yaml
# batch-telemetry-ingest.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: telemetry-ingest-20260302
  namespace: data-platform
spec:
  backoffLimit: 3          # retry up to 3 times on failure
  ttlSecondsAfterFinished: 86400   # auto-clean after 24h
  template:
    spec:
      restartPolicy: OnFailure
      containers:
        - name: ingest
          image: myregistry.io/telemetry-pipeline:v1.2.0
          command: ["python", "-m", "telemetry_pipeline.ingest"]
          env:
            - name: REPORT_DATE
              value: "2026-03-02"
          envFrom:
            - secretRef:
                name: pipeline-secrets     # DB creds from K8s Secret
            - configMapRef:
                name: pipeline-config      # non-sensitive config
          resources:
            requests:
              cpu: "500m"       # 0.5 core minimum
              memory: "1Gi"
            limits:
              cpu: "2000m"      # 2 core max
              memory: "4Gi"
```

### Airflow KubernetesExecutor

When Airflow uses the KubernetesExecutor, each task runs as its own Pod:

```python
# In Airflow DAG
from airflow.providers.cncf.kubernetes.operators.pod import KubernetesPodOperator

ingest_task = KubernetesPodOperator(
    task_id="telemetry_ingest",
    name="telemetry-ingest",
    namespace="data-platform",
    image="myregistry.io/telemetry-pipeline:v1.2.0",
    cmds=["python", "-m", "telemetry_pipeline.ingest"],
    env_vars={"REPORT_DATE": "{{ ds }}"},
    resources={
        "request_cpu": "500m",
        "request_memory": "1Gi",
        "limit_cpu": "2",
        "limit_memory": "4Gi"
    },
    is_delete_operator_pod=True,    # clean up pod after task
    dag=dag,
)
```

**Why KubernetesExecutor over LocalExecutor:**
- Task isolation (failures don't affect other tasks)
- Auto-scaling (nodes added/removed based on queue depth)
- Per-task resource limits (expensive tasks get more RAM)
- No shared state between tasks

### Spark on Kubernetes

```bash
# Submit Spark job to K8s cluster
spark-submit \
  --master k8s://https://<k8s-api-server>:6443 \
  --deploy-mode cluster \
  --name telemetry-transform \
  --conf spark.kubernetes.container.image=myregistry.io/spark-telemetry:v3.5.0 \
  --conf spark.executor.instances=5 \
  --conf spark.kubernetes.namespace=data-platform \
  local:///app/transform.py
```

### DE Interview: K8s Questions and Answers

**Q: "How would you run dbt in production?"**
> "As a K8s CronJob or triggered by Airflow using KubernetesPodOperator. The dbt image contains the models and profiles.yml. Credentials injected via K8s Secrets. CronJob runs on schedule; on failure, K8s retries up to N times. Logs go to CloudWatch or Loki. Artifacts (run results, manifest) pushed to S3."

**Q: "A Spark job OOM-killed on K8s — how do you diagnose?"**
> "First: `kubectl describe pod <pod-name>` to see the OOMKilled reason. Then check `spark.executor.memory` vs the K8s limits — they must be aligned (Spark memory + overhead < K8s limit). Increase limits or reduce shuffle partitions. Enable AQE to coalesce small partitions. Also check for data skew — one executor getting all the data."

---

## Behavioral Anchor — Day 18

> "Tell me about a time you built something that ran reliably without you having to babysit it."

Strong answer covers:
- Automation of a previously manual or fragile process
- Monitoring/alerting you added
- How long it ran without intervention
- What would have broken without your design

This maps directly to Kubernetes CronJobs, Airflow DAGs, and automated capacity alerts.

---

## Day 18 Checklist

- [ ] Memorized 8 core bit operations (can write without looking)
- [ ] Coded LC #136 (Single Number) using XOR — explains WHY XOR works
- [ ] Coded LC #338 (Counting Bits) using DP bit pattern
- [ ] Ran at least 3 of the string/array SQL queries in DuckDB
- [ ] Can produce the "tag pivot" query from scratch
- [ ] Can explain what `uv` does and why it's better than raw pip+venv
- [ ] Knows what a pyproject.toml contains (4 sections)
- [ ] Can describe what a K8s Job is and when to use it vs Deployment
- [ ] Can explain KubernetesExecutor vs LocalExecutor for Airflow
- [ ] Can diagnose an OOMKilled Spark pod on K8s
