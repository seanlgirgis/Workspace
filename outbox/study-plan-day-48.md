---
created: 2026-03-02
updated: 2026-03-02
summary: Day 48 — Finance SQL deep dive session. Complex multi-table queries for regulatory reporting patterns. Dijkstra review.
tags: [study-plan, day-48, week-7, finance-sql-deep-dive, dijkstra, regulatory-reporting]
---

# Day 48 — Finance SQL Deep Dive + Dijkstra Review

**Theme:** Finance DE interviews are SQL-heavy. Today you run the hardest SQL queries in the entire plan.

---

## Daily Maintenance (20 min)

**LC — Dijkstra (timed recall):**

Write from memory — no looking:
```python
import heapq
from collections import defaultdict

def dijkstra(graph, start, n):
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    heap = [(0, start)]
    while heap:
        cost, u = heapq.heappop(heap)
        if cost > dist[u]: continue
        for v, w in graph[u]:
            if cost + w < dist[v]:
                dist[v] = cost + w
                heapq.heappush(heap, (dist[v], v))
    return dist
```
Then solve LC #743 Network Delay Time from scratch (10 min).

---

## Finance SQL Deep Dive (70 min)

**Schema:**
```sql
-- positions(trade_id, book_id, asset_id, position_date DATE, quantity FLOAT, direction VARCHAR)
-- reference_prices(asset_id, price_date DATE, close_price FLOAT, currency VARCHAR)
-- books(book_id, book_name, desk VARCHAR, region VARCHAR)
-- assets(asset_id, asset_name, asset_class VARCHAR, issuer VARCHAR)
```

**Query 1 — Mark-to-Market by Desk (15 min):**
```sql
-- Calculate total market value per desk per day.
-- Use SUM(quantity * close_price), handle long (positive) vs short (negative) positions.
-- Only include the most recent price if multiple prices exist per day.
```

**Query 2 — Daily P&L with Attribution (15 min):**
```sql
-- Daily P&L per book:
--   P&L = today's MtM - yesterday's MtM
-- Show: book_id, book_name, desk, region, position_date, market_value, prior_value, pnl
-- Include only days where both today and yesterday have prices.
-- Order by ABS(pnl) DESC — biggest movers first.
```

**Query 3 — Asset Class Exposure Report (15 min):**
```sql
-- For each desk, show exposure by asset class:
--   exposure = SUM(quantity * close_price) per asset_class
-- Also show: pct_of_total (exposure / total desk exposure * 100)
-- Use window functions, not subqueries.
```

**Query 4 — Stale Price Detection (10 min):**
```sql
-- Find all (book_id, asset_id) pairs where the latest available price
-- is more than 2 business days old relative to the maximum price_date in the table.
-- Return: book_id, asset_id, last_price_date, days_stale
```

**Query 5 — Top 10 Positions by PnL (15 min):**
```sql
-- Across all books and all days in the last 30 days,
-- find the top 10 (book_id, asset_id) combinations by total accumulated P&L.
-- Show: book_id, asset_id, asset_name, desk, total_pnl, avg_daily_pnl
```

---

## Day 48 Checklist

- [ ] Dijkstra written from memory (no notes)
- [ ] LC #743 solved in 10 min
- [ ] Query 1 (MtM by desk) written and produces correct output
- [ ] Query 2 (P&L with attribution) includes BOTH the LAG and the NULL filter
- [ ] Query 3 (asset class exposure) uses window function for pct_of_total
- [ ] Query 4 (stale price) correctly identifies 2-business-day threshold
- [ ] Query 5 (top 10 by PnL) returns correct ranking
- [ ] Can explain each query verbally in 30 seconds
