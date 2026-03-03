---
created: 2026-03-02
updated: 2026-03-02
summary: Day 47 — Persistent gap drill session 2 plus Union-Find review and lateral join SQL.
tags: [study-plan, day-47, week-7, gap-drill-2, union-find, lateral-join]
---

# Day 47 — Gap Drill 2 + Union-Find + Lateral Join SQL

**Theme:** Repetition under time pressure is the only thing that builds interview-speed recall.

---

## Daily Maintenance (35 min)

**LC — Union-Find (2 problems, timed):**
- LC #200 Number of Islands (10 min — can do DFS or Union-Find; do BOTH, compare)
- LC #547 Number of Provinces (8 min — Union-Find on adjacency matrix)

Union-Find template (write from memory):
```python
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # path compression
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if rank[px] < rank[py]: px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]: rank[px] += 1
    return True
```

**SQL — Lateral Joins:**
```sql
-- 1. For each server, get its 3 most recent reports (lateral + row_number)
-- 2. For each region, get the top server by CPU in each tier (lateral)
-- 3. Unnest a pipe-delimited tags string into rows using lateral + UNNEST
```

**Behavioral:** "Describe a technical decision that, in hindsight, you'd make differently."

---

## Gap Drill 2 — Remaining Persistent Gaps (45 min)

From your Day 45 post-interview reflection, address your next 2 gaps:

**If your gap is Trees (BFS/DFS):**
- LC #102 Binary Tree Level Order Traversal (queue-based — write it)
- LC #543 Diameter of Binary Tree (DFS — `left_depth + right_depth` at each node, track max)
- LC #572 Subtree of Another Tree (DFS — recursive match check at each node)

**If your gap is Greedy:**
- LC #134 Gas Station (greedy — when curr < 0, reset start; check total ≥ 0)
- LC #435 Non-overlapping Intervals (sort by end, count overlaps)
- LC #452 Minimum Number of Arrows (sort by end, advance arrow only when needed)

**If your gap is SQL data quality:**
```sql
-- 1. Find servers reporting more than once per day (count > 1 on server_id + date)
-- 2. Find the percentage of NULL values per column
-- 3. Identify rows where avg_cpu jumped more than 40 points from the previous day
-- 4. Find servers where the max reported CPU never exceeds 5 (stuck/phantom reporting)
```

---

## Application Check (15 min)

- Respond to any recruiter emails or LinkedIn messages promptly
- If a company has been silent for 10+ business days → send one follow-up, then move on
- Identify 2-3 new job postings to apply to today

---

## Day 47 Checklist

- [ ] Union-Find template written from memory (with path compression and rank)
- [ ] LC #200 solved with both DFS and Union-Find approaches
- [ ] All 3 lateral join SQL queries written and run
- [ ] Behavioral story answered — real decision, honest hindsight
- [ ] Gap Drill 2 completed (all 3 problems/queries for chosen gap)
- [ ] Application tracker updated — responses acted on
