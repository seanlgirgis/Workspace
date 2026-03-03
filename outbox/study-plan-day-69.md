---
created: 2026-03-02
updated: 2026-03-02
summary: Day 69 — Finance SQL final drill. The hardest SQL patterns targeting financial services interviews.
tags: [study-plan, day-69, week-10, sql, finance, final-drill, mark-to-market, regulatory]
---

# Day 69 — Finance SQL Final Drill

**Theme:** Finance SQL isn't just complex queries — it's queries with business meaning. Today you prove you understand both.

---

## Daily Maintenance (20 min)

**LC — String DP (2 problems, timed):**
- LC #647 Palindromic Substrings (6 min — expand around center, count both odd and even)
- LC #139 Word Break (8 min — `dp[i] = any(dp[j] and s[j:i] in word_set for j < i)`)

---

## Finance SQL Drill Session (75 min)

Work through each query. Write it, then explain what the business is trying to know.

---

### Query 1 — Mark-to-Market P&L with Prior Close (15 min)

```sql
-- positions: trade_id, desk_id, asset_id, quantity, cost_basis
-- prices: asset_id, price_date, close_price

WITH position_value AS (
    SELECT
        p.desk_id,
        p.asset_id,
        p.quantity,
        p.cost_basis,
        pr.close_price,
        pr.price_date,
        p.quantity * pr.close_price AS market_value,
        p.quantity * (pr.close_price - p.cost_basis) AS unrealized_pnl
    FROM positions p
    JOIN prices pr ON p.asset_id = pr.asset_id
    WHERE pr.price_date = CURRENT_DATE
),
with_prior AS (
    SELECT
        pv.*,
        LAG(pv.unrealized_pnl) OVER (
            PARTITION BY pv.desk_id, pv.asset_id
            ORDER BY pv.price_date
        ) AS prior_unrealized_pnl
    FROM position_value pv
)
SELECT
    desk_id,
    asset_id,
    unrealized_pnl,
    prior_unrealized_pnl,
    unrealized_pnl - COALESCE(prior_unrealized_pnl, 0) AS daily_pnl_change
FROM with_prior
ORDER BY desk_id, daily_pnl_change DESC;
```

**Business meaning:** The trading desk needs to know not just where they stand today, but how much their P&L moved from yesterday. A large daily change triggers risk review.

**What breaks this:** Stale prices (price_date != CURRENT_DATE for some assets). Add a check:
```sql
-- After the main query:
SELECT asset_id FROM prices
WHERE asset_id NOT IN (SELECT asset_id FROM prices WHERE price_date = CURRENT_DATE);
-- These assets have stale prices — their P&L is unreliable.
```

---

### Query 2 — Regulatory Exposure Report (15 min)

```sql
-- Report: for each desk, total long exposure and total short exposure by asset class.
-- Regulatory rule: net short exposure > $50M requires same-day reporting.

WITH exposure AS (
    SELECT
        p.desk_id,
        a.asset_class,
        SUM(CASE WHEN p.quantity > 0 THEN p.quantity * pr.close_price ELSE 0 END) AS long_exposure,
        SUM(CASE WHEN p.quantity < 0 THEN ABS(p.quantity) * pr.close_price ELSE 0 END) AS short_exposure,
        SUM(p.quantity * pr.close_price) AS net_exposure
    FROM positions p
    JOIN prices pr ON p.asset_id = pr.asset_id AND pr.price_date = CURRENT_DATE
    JOIN assets a ON p.asset_id = a.asset_id
    GROUP BY p.desk_id, a.asset_class
)
SELECT
    desk_id,
    asset_class,
    long_exposure,
    short_exposure,
    net_exposure,
    CASE WHEN net_exposure < -50000000 THEN 'REQUIRES_SAME_DAY_REPORT' ELSE 'OK' END AS regulatory_flag
FROM exposure
ORDER BY net_exposure ASC;
```

**Business meaning:** This feeds a regulatory report submitted to the regulator daily. If net_exposure is sufficiently negative (net short), the firm must report it same day. Missing this triggers fines.

---

### Query 3 — Top Drawdown Days (15 min)

```sql
-- Find the 5 worst daily P&L days per desk over the last 90 days.
-- "Drawdown" = most negative daily P&L change.

WITH daily_pnl AS (
    SELECT
        desk_id,
        price_date,
        SUM(quantity * close_price) AS portfolio_value
    FROM positions p
    JOIN prices pr ON p.asset_id = pr.asset_id
    WHERE pr.price_date >= CURRENT_DATE - 90
    GROUP BY desk_id, price_date
),
with_change AS (
    SELECT
        desk_id,
        price_date,
        portfolio_value,
        portfolio_value - LAG(portfolio_value) OVER (
            PARTITION BY desk_id ORDER BY price_date
        ) AS daily_change
    FROM daily_pnl
),
ranked AS (
    SELECT
        *,
        RANK() OVER (PARTITION BY desk_id ORDER BY daily_change ASC) AS loss_rank
    FROM with_change
    WHERE daily_change IS NOT NULL
)
SELECT desk_id, price_date, daily_change, loss_rank
FROM ranked
WHERE loss_rank <= 5
ORDER BY desk_id, loss_rank;
```

**Business meaning:** Risk management tracks "tail risk" days — the worst outlier losses. These inform VaR (Value at Risk) models and stress test scenarios.

---

### Query 4 — Settlement Lag Detection (10 min)

```sql
-- trades: trade_id, desk_id, trade_date, expected_settle_date, actual_settle_date
-- Find all trades that settled late and compute days late.
-- Flag trades > 2 days late as "T+2 breach" (common regulatory standard).

SELECT
    trade_id,
    desk_id,
    trade_date,
    expected_settle_date,
    actual_settle_date,
    actual_settle_date - expected_settle_date AS days_late,
    CASE
        WHEN actual_settle_date IS NULL THEN 'PENDING'
        WHEN actual_settle_date - expected_settle_date > 2 THEN 'T+2_BREACH'
        WHEN actual_settle_date > expected_settle_date THEN 'LATE'
        ELSE 'ON_TIME'
    END AS settlement_status
FROM trades
WHERE trade_date >= CURRENT_DATE - 30
ORDER BY days_late DESC NULLS LAST;
```

**Business meaning:** Late settlement creates counterparty risk and can trigger regulatory penalties. This query feeds the operations team's daily exception report.

---

### Query 5 — Idempotent Regulatory Batch (Write the pattern from memory, 10 min)

Write the complete batch insert pattern for a regulatory report table that must be idempotent:
- Table: `regulatory_reports(report_date, desk_id, report_type, payload, loaded_at)`
- Constraint: `(report_date, desk_id, report_type)` must be unique
- Pattern: delete partition first, then insert — or use ON CONFLICT

```sql
-- Your solution here — write from memory before looking at notes
```

---

## Day 69 Checklist

- [ ] Both LC problems solved (palindromic substrings: count each expansion)
- [ ] Query 1 written and explained (MtM P&L + stale price check)
- [ ] Query 2 written and explained (regulatory exposure + flag logic)
- [ ] Query 3 written and explained (top drawdown: LAG + RANK)
- [ ] Query 4 written and explained (settlement lag + T+2 breach flag)
- [ ] Query 5 idempotent batch pattern written from memory
- [ ] For each query: stated the business meaning out loud before writing
