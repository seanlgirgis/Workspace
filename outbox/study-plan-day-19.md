---
created: 2026-03-02
updated: 2026-03-02
summary: Day 19 — System Design Patterns (LRU Cache, Rate Limiter), Behavioral Story Refinement, and Company-Specific Research Framework.
tags: [study-plan, day-19, system-design, lru-cache, rate-limiter, behavioral, company-research]
---

# Day 19 — System Design Patterns | Behavioral Polish | Company Research

**Theme:** The day before the final review. Stop learning new material. Start pressure-testing what you know.

---

## Spaced Repetition Check-In (15 min)

Answer from memory:

1. In bit manipulation, what does `n & (n-1)` do?
2. What does XOR do when you XOR a number with itself? With zero?
3. What is the difference between a K8s Job and a K8s CronJob?
4. What is point-in-time correct joining and what problem does it prevent?
5. What is a data product in Data Mesh? What 5 things does it have?
6. Name three things the Catalyst optimizer does automatically in Spark.

---

## A. System Design Patterns — LRU Cache and Rate Limiter (60 min)

These are canonical "design a data structure" problems. They test whether you can translate verbal requirements into implementation decisions.

### Pattern 1 — LRU Cache (LC #146)

**Problem:** Design a data structure that supports:
- `get(key)` → return value if key exists, else -1
- `put(key, value)` → insert or update. If capacity is exceeded, evict the Least Recently Used item.

All operations must be O(1).

**Why O(1) LRU requires both a HashMap and a Doubly Linked List:**

- HashMap gives O(1) access to any node by key
- Doubly linked list maintains access order (most recent at head, least recent at tail)
- When an item is accessed: move it to the head (O(1) with prev/next pointers)
- When evicting: remove the tail node (O(1))

```python
class DLinkedNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}   # key → DLinkedNode

        # Sentinel nodes — avoid null checks at boundaries
        self.head = DLinkedNode()   # most recently used side
        self.tail = DLinkedNode()   # least recently used side
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)          # move to front = "just used"
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            node = DLinkedNode(key, value)
            self.cache[key] = node
            self._add_to_front(node)
            if len(self.cache) > self.capacity:
                lru = self.tail.prev          # evict LRU
                self._remove(lru)
                del self.cache[lru.key]       # clean up HashMap too
```

**Python shortcut (interview acceptable if you explain the tradeoff):**
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)   # O(1) in CPython
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)   # remove LRU (front)
```

---

### Pattern 2 — Rate Limiter Design

**Problem:** Design a rate limiter that allows at most N requests per minute per user. Reject requests that exceed the limit.

This is a system design question, not a coding question. The interviewer wants architectural reasoning.

#### Algorithm Options

**Fixed Window Counter:**
```
Window: [0s, 60s) → count requests. Reset at 60s.
Problem: burst at window edge — 100 req at 59s + 100 req at 61s = 200 in 2 seconds.
```

**Sliding Window Log:**
```
Store timestamp of each request in a sorted set (per user).
On new request: remove entries older than now-60s. Count remaining.
If count < limit → allow, add timestamp.
Accurate, but O(limit) storage per user.
```

**Sliding Window Counter (best trade-off):**
```
Hybrid: use current window count + weighted previous window count.
rate = prev_count × (time_remaining / window) + curr_count
Approximate but O(1) per user. Used by Nginx, Cloudflare.
```

**Token Bucket (most common in practice):**
```
Each user has a bucket of N tokens. Tokens refill at rate R/sec.
Request costs 1 token. Rejected if bucket empty.
Allows bursting up to N (bucket capacity).
```

#### Implementation Sketch (Redis-backed Sliding Window Log)

```python
import redis
import time

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis.Redis()

    def is_allowed(self, user_id: str) -> bool:
        key = f"rate:{user_id}"
        now = time.time()
        window_start = now - self.window

        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, window_start)    # remove old entries
        pipe.zcard(key)                                  # count remaining
        pipe.zadd(key, {str(now): now})                 # add current request
        pipe.expire(key, self.window)                   # auto-expire key
        results = pipe.execute()

        count = results[1]   # count BEFORE adding current request
        return count < self.limit
```

**Trade-offs to know:**
| Approach | Memory | Accuracy | Burst Handling |
|----------|--------|----------|----------------|
| Fixed Window | O(1) | Poor (edge burst) | Bad |
| Sliding Window Log | O(limit) | Perfect | Good |
| Sliding Window Counter | O(1) | ~99% | Good |
| Token Bucket | O(1) | Good | Configurable burst |
| Leaky Bucket | O(1) | Good | Fixed output rate |

---

### System Design Framework — Use This for Any Question

```
1. Clarify requirements (2 min)
   - Scale: how many users/requests/records?
   - Read vs write ratio
   - Consistency requirements (eventual OK, or strict?)
   - Latency SLA

2. High-level design (5 min)
   - Draw boxes: clients → load balancer → service → storage
   - Identify the core data flow

3. Deep dive (10 min)
   - Pick 2-3 components to detail based on interviewer's interest
   - Address the hardest part: scaling, consistency, failure

4. Trade-offs (3 min)
   - What did you sacrifice? Why?
   - What would you do differently with more time?
```

---

## B. Behavioral Story Refinement (45 min)

This is not "study" time. This is performance rehearsal. Say answers out loud. Time yourself. Record if possible.

### The 5 Stories You Need

You need 5 strong STAR stories that cover the competencies interviewers test. Each story should be under 2 minutes when spoken.

---

**Story 1 — Silent Failure (observability, proactiveness)**

Template trigger: "Tell me about a time you caught something nobody else noticed."

Your story must include:
- Specific system and specific failure (not "something was slow")
- Why it was silent (no monitoring, no alerts, wrong threshold)
- How you discovered it (curiosity, investigation, anomaly in data)
- What you did to fix AND prevent recurrence
- Measurable impact (hours of downtime prevented, revenue protected, SLA maintained)

**Polish checklist:**
- [ ] "I" not "we" — you are the subject of this story
- [ ] Specific number (6 hours, 2,000 servers, $40K/month)
- [ ] Concrete action (wrote the alert, set up the dashboard, added the check)
- [ ] Stakes were real (not a toy project)

---

**Story 2 — Technical Complexity**

Template trigger: "Tell me about the most complex technical problem you solved."

Your story must include:
- Why it was technically hard (ambiguity, scale, constraints — not just "it was a lot of data")
- Your diagnostic approach (how you broke it into pieces)
- The key insight that unlocked the solution
- What you would do differently

**For Sean — capacity planning angle:**
The data engineering challenge of forecasting at 6,000-server scale: data quality (missing agents, silent reporters), seasonal CPU patterns breaking linear models, operationalizing alerts into Jira tickets automatically.

---

**Story 3 — Change Management / Influence**

Template trigger: "Tell me about a time you convinced a team to do something differently."

Your story must include:
- What the old way was and its real cost
- Why you thought it needed to change
- How you built the case (data, not opinion)
- The specific pushback you faced and how you addressed it
- Measurable adoption or outcome

---

**Story 4 — Reliability / Production Operations**

Template trigger: "Tell me about a time something broke in production."

Your story must include:
- What broke, when, and what was the impact
- Your incident response (who you called, how you communicated)
- Root cause analysis
- The permanent fix (not just "we restarted it")
- Process change that prevented recurrence

---

**Story 5 — Collaboration / Cross-Functional**

Template trigger: "Tell me about a time you worked with a team outside engineering."

Your story must include:
- Who the other team was (finance, ops, infrastructure)
- What misalignment existed (different goals, language, priorities)
- How you bridged it (translated technical to business terms)
- Joint outcome

---

### Behavioral Anti-Patterns to Eliminate

| Bad Pattern | Fix |
|-------------|-----|
| "We decided to..." | "I proposed... the team agreed because..." |
| "It was pretty complex" | "The specific challenge was X because Y" |
| Vague numbers | "3 servers" → "3 production servers handling $2M/day of transactions" |
| No conflict | If there was no challenge, find a different story |
| Story ends at solution | Add: "The result was X. I then..." |
| Rushing past the result | The result is the whole point — slow down there |

---

### Behavioral Questions Bank — Practice These

> Time yourself. 90 seconds is ideal. 2 minutes max.

1. Tell me about a time you had to learn something quickly.
2. Tell me about a project you're most proud of.
3. Tell me about a time you disagreed with your manager.
4. Tell me about a time you failed. What did you learn?
5. Tell me about a time you had to prioritize multiple urgent things.
6. Why are you leaving your current role?
7. Why do you want this specific role?
8. Where do you see yourself in 3 years?

---

## C. Company Research Framework (30 min)

### The Framework — For Every Target Company

Before any interview, you should know:

**1. What does the company do with data?**
- What is their data volume? (public info: blog posts, engineering blog)
- What decisions does data inform? (ops, product, finance, risk)
- What data problems are publicly known? (job postings reveal pain)

**2. What tech do they use?**
- Check job postings: Spark, Snowflake, Airflow, Kafka, dbt, BigQuery?
- Engineering blogs (Confluent, Databricks, Medium tech blogs)
- GitHub repos (some companies open-source their data tools)
- LinkedIn: what tools do their DEs list?

**3. What is their data team structure?**
- Central DE team vs embedded (domain ownership = Data Mesh influence)
- Separate ML platform team?
- How big is the team? (LinkedIn headcount)

**4. What specific value can you bring?**
- Map your APM experience to their domain
- Map your capacity planning work to their scale problems
- Identify the gap in their stack you could help fill

---

### Finance / Banking DE — Specific Context

For Citi, Goldman, JPMorgan:

**What's different in finance DE:**
- Regulatory data retention (7-10 years, immutable audit trails)
- Strict lineage requirements (know where every number came from)
- Batch-heavy (overnight settlement, end-of-day risk calculations)
- Data governance is not optional — it's regulatory compliance
- Low tolerance for downtime in trade-adjacent systems

**Their tech landscape:**
- Legacy: Oracle, Sybase, IBM MQ, IBM DataStage
- Modern: Snowflake, dbt, Spark (on-prem Hadoop clusters still common), Airflow
- Risk/quant: Python (pandas, numpy), sometimes R
- Streaming: Kafka for trade events, market data feeds

**Frame your value for finance:**
- "My APM experience is directly relevant — financial systems need the same observability: when did this calculation run, what data did it use, where did the result go?"
- "Capacity planning for financial infrastructure has regulatory urgency — a storage overflow during end-of-day processing is not just an ops issue."
- "I have direct experience with the reliability requirements of production systems at scale."

---

### Research Template — Fill This In Before Each Interview

```
Company: _______________
Role: Senior Data Engineer

Data Scale:
  Volume: ___
  Speed: ___
  Variety: ___

Known Tech Stack:
  Ingest: ___
  Storage: ___
  Processing: ___
  Orchestration: ___
  Serving: ___

Their Public DE Content:
  Blog post URL: ___
  Key challenge they've written about: ___

My Specific Value:
  Story 1 maps to their ___
  Story 2 maps to their ___
  My background in ___ solves their problem with ___

Questions I'll Ask:
  1. ___
  2. ___
  3. ___
```

### Questions to Ask Interviewers (always have 3 ready)

These signal senior-level thinking:

1. "How does the data team handle schema changes in production pipelines — what's the process when a source system changes a column type?"
2. "What does data quality monitoring look like today — are there automated checks, or is it caught in dashboards?"
3. "How are data engineering priorities set — is it driven by the data team roadmap, or are you primarily responding to business requests?"
4. "What's the biggest gap in the current data infrastructure that this role is expected to address?"
5. "How does the team think about the balance between the central platform and domain teams owning their own pipelines?"

---

## Day 19 Checklist

- [ ] Implemented LRU Cache from scratch (DLL + HashMap version, not OrderedDict shortcut)
- [ ] Can explain the 4 rate limiting algorithms and their trade-offs
- [ ] Can draw the Rate Limiter architecture (Redis-backed sliding window) from scratch
- [ ] Spoke Story 1 (silent failure) out loud — timed < 2 min
- [ ] Spoke Story 2 (technical complexity) out loud — timed < 2 min
- [ ] Spoke Story 3 (change management) out loud — timed < 2 min
- [ ] Have a target company researched using the framework above
- [ ] Have 3 questions ready to ask an interviewer
- [ ] Know what's different about finance/banking DE vs typical DE roles
