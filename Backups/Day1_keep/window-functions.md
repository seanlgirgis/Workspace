---
created: 2026-02-26
updated: 2026-02-27
summary: SQL window functions — full concepts, code examples, 10 interview Q&A with answers, Citi talking points
tags: [sql, window-functions, interview-prep, study, day1]
---

# SQL Window Functions

## Lifecycle
- [x] Collected (2026-02-27)
- [x] To Study
- [x] Studied (2026-02-27)
- [ ] To Review

---

## Core Concept (Plain Language)

A window function performs a calculation across a set of rows **related to the current row** — without collapsing the rows like GROUP BY does.

- **GROUP BY**: gives you one row per group
- **Window function**: keeps all rows but adds a calculated column alongside them

## The Concise "Cheat Code" Summary

### 1. The Rankers (Leaderboards)
- **`ROW_NUMBER()`**: The Stubborn Counter. Always counts 1, 2, 3. Even on ties, someone gets 1 and the other gets 2.
- **`RANK()`**: The Olympic Medal System. If two people tie for 1st, they both get 1. The next person gets 3rd (Bronze). *It skips numbers.*
- **`DENSE_RANK()`**: The Fair System. Ties get the same number, but it *never skips*. (1, 1, 2). **Always use this for "Top N" reporting so nobody is skipped.**

### 2. Time Travel (Comparisons)
- **`LAG()`**: Look backwards. Use this to compare today's CPU usage to yesterday's without an expensive self-join.
- **`LEAD()`**: Look forwards. Use this to see what the *next* state of a server will be.

### 3. Aggregates (Math)
- **The Rolling Window:** `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW`.
- SQL automatically handles the boundary (if you ask for 3 days on Day 1, it just averages Day 1).

### Interview Trap to Remember
You CANNOT put a window function directly in a `WHERE` clause. You must wrap the window function inside a **CTE (Common Table Expression)** first, and then build a query that filters the CTE.

---

## The Four Must-Know Functions

### 1. ROW_NUMBER()
Assigns a unique number to each row within a partition.
```sql
ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)
```
Use case: "Give me the highest paid person per department"

---

### 2. RANK() and DENSE_RANK()
Like ROW_NUMBER but handles ties.
- RANK() skips numbers after ties (1, 1, 3)
- DENSE_RANK() doesn't skip (1, 1, 2)

```sql
RANK() OVER (PARTITION BY department ORDER BY salary DESC)
```

---

### 3. LAG() and LEAD()
Look backwards or forwards in the dataset.
```sql
LAG(revenue, 1) OVER (PARTITION BY region ORDER BY month)
```
Use case: "Compare this month's revenue to last month"

---

### 4. SUM() / AVG() as Running Totals
```sql
SUM(bytes_processed) OVER (
  PARTITION BY server_id
  ORDER BY timestamp
  ROWS BETWEEN 7 PRECEDING AND CURRENT ROW
)
```
Use case: "Rolling 7-day average of CPU utilization" — **this is exactly what you did at Citi**

---

## My Citi Talking Point

> "At Citi I processed telemetry from 6,000+ endpoints. I used window functions extensively — LAG() to detect utilization spikes by comparing current vs previous collection interval, and rolling SUM/AVG windows to smooth out noise in capacity forecasting. This let us identify servers trending toward bottleneck 6 months ahead."

That answer is worth gold. It's real, specific, and shows scale.

---

## Key Syntax Reference

```sql
ROW_NUMBER() OVER (PARTITION BY x ORDER BY y)
LAG(col, 1) OVER (PARTITION BY x ORDER BY y)
AVG(col) OVER (PARTITION BY x ORDER BY y ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
```

---

## Interview Traps

- Window functions **cannot** be used in WHERE clause — wrap in CTE first
- ROWS BETWEEN vs RANGE BETWEEN — always use ROWS for time series (predictable)
- RANK skips numbers after ties, DENSE_RANK never skips

---

## 10 Interview Questions + Your Answers

**Q1: What's the difference between ROW_NUMBER, RANK, and DENSE_RANK?**

> ROW_NUMBER always gives unique numbers. RANK skips after ties — so 1, 1, 3. DENSE_RANK never skips — 1, 1, 2. I use DENSE_RANK when I need to find top N per group without gaps in ranking.

---

**Q2: When would you use LAG() vs a self join?**

> LAG() is cleaner, more readable, and performs better than a self join for sequential comparisons. At Citi I used LAG() to compare server utilization between collection intervals — a self join on 6,000 endpoints would have been expensive.

---

**Q3: What's the difference between PARTITION BY and GROUP BY?**

> GROUP BY collapses rows into one per group. PARTITION BY keeps all rows and adds the calculation alongside them. Window functions never reduce row count.

---

**Q4: How would you calculate a 7-day rolling average?**

```sql
AVG(cpu_utilization) OVER (
  PARTITION BY server_id
  ORDER BY collection_date
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

> I used this pattern at Citi to smooth telemetry noise before feeding data into Prophet forecasting models.

---

**Q5: What is ROWS BETWEEN vs RANGE BETWEEN?**

> ROWS BETWEEN is physical — it counts actual rows. RANGE BETWEEN is logical — it includes all rows with the same ORDER BY value. For time series I always use ROWS BETWEEN for predictability.

---

**Q6: How do you find the top 3 salaries per department?**

```sql
WITH ranked AS (
  SELECT *,
    DENSE_RANK() OVER (
      PARTITION BY department
      ORDER BY salary DESC
    ) as rnk
  FROM employees
)
SELECT * FROM ranked WHERE rnk <= 3
```

---

**Q7: What's a practical use case for LEAD()?**

> Detecting job transitions. LEAD() lets you look at the next row's value — useful for finding when a server's status changed from normal to warning, or identifying gaps in time series data.

---

**Q8: Can you use window functions in a WHERE clause?**

> No — window functions are evaluated after WHERE. You wrap them in a CTE or subquery first, then filter on the result. Classic interview trap.

---

**Q9: How would you calculate month-over-month growth?**

```sql
(revenue - LAG(revenue) OVER (ORDER BY month))
/ LAG(revenue) OVER (ORDER BY month) * 100
```

---

**Q10: What's the performance consideration with window functions on large datasets?**

> Window functions require sorting and can be expensive at scale. At Citi processing millions of telemetry rows I always ensured the PARTITION BY columns were indexed, and used Athena's columnar Parquet format to minimize data scanned.

---

## Practice on DuckDB

Install DuckDB — no setup, no server needed:
```
pip install duckdb
```
Then test all queries above on sample data. DuckDB reads CSV/Parquet directly.

---

## Key Terms to Drop in Interviews

- "window frame" — the ROWS/RANGE clause
- "partition" — the grouping that the window operates over
- "ordered set" — the ORDER BY within the window
- "rolling aggregate" — SUM/AVG with ROWS BETWEEN
- "columnar format" — when discussing performance (Parquet, Athena)
