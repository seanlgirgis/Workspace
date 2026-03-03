---
created: 2026-03-02
updated: 2026-03-02
summary: Day 32 — Stack review, finance SQL (mark-to-market P&L), and deep-dive company research on Goldman Sachs.
tags: [study-plan, day-32, week-5, stack, finance-sql, goldman-research]
---

# Day 32 — Stack Review + Finance SQL + Goldman Sachs Research

**Theme:** Goldman has the highest technical bar of any finance DE employer. Know what you're walking into.

---

## Daily Maintenance (35 min)

**LC — Stack (3 problems, timed):**
- LC #20 Valid Parentheses (5 min)
- LC #150 Evaluate Reverse Polish Notation (8 min — stack, operators pop two operands)
- LC #739 Daily Temperatures (10 min — monotonic decreasing stack of indices)

After #739: explain out loud why this is O(n) despite the nested-looking loop.

**SQL — Finance SQL (mark-to-market P&L pattern):**

From the Day 27 mock — rebuild this from scratch:
```sql
-- Schema:
-- positions(trade_id, asset_id, position_date, quantity, book_id)
-- reference_prices(asset_id, price_date, close_price)

-- Goal: daily P&L per book
-- Step 1: join positions to prices
-- Step 2: aggregate market value per book per day
-- Step 3: LAG to get prior day value
-- Step 4: compute P&L = today - yesterday, filter out NULL prior days
```
Write it completely. Run it. Verify the LAG handles NULL correctly.

**Behavioral:** Speak Story 4 (production incident) — timed.

---

## Company Research: Goldman Sachs (45 min)

### Goldman DE Context

**Key facts:**
- Goldman built SecDB — their proprietary real-time risk system (one of the most complex financial systems ever built)
- Marquee platform: Goldman's data/analytics API product for institutional clients
- Marcus: consumer banking arm with modern cloud stack
- Goldman tech is famous for high standards and long interview loops (6+ rounds possible)

**What Goldman DE interviews test (harder than most):**
- Python is treated as a first-class engineering language — you will be judged on code quality, not just correctness
- System design includes distributed systems thinking
- Behavioral: Goldman uses "competency-based" interviews with very high bar for "impact" and "leadership"

```
Goldman Sachs DE Research Template
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Goldman's known tech stack (from public sources):
  Strats language (proprietary): note awareness, don't need to know it
  Python: first-class — know it cold
  Data platform (Marcus/Consumer): Snowflake likely
  Execution systems: proprietary, but they hire cloud engineers now

Goldman's data engineering hiring areas:
  - Global Markets (trading data, risk)
  - Asset Management (portfolio analytics)
  - Engineering Division (platform, infrastructure)
  - Marcus (consumer, cloud-native)

My best-fit Goldman division:
  ___ because ___

My angle for Goldman:
  ___

Goldman-specific questions to ask:
  1. "How does the Engineering Division's data platform interact with
     the trading systems — what's the data flow for end-of-day risk?"
  2. ___
  3. ___
```

### Goldman Behavioral Bar

Goldman uses a framework of "core competencies" — expect:
- **Leadership:** "Tell me about a time you led without formal authority"
- **Analytical thinking:** "Walk me through how you approached a complex data problem"
- **Client/stakeholder focus:** "Tell me about a time you built something for a business partner"
- **Excellence:** "Tell me about a time your work directly impacted the business"

For Goldman: answers need numbers. "Significantly improved" doesn't pass. "Reduced MTTR from 4 hours to 20 minutes, preventing $X of SLA penalties" does.

---

## Day 32 Checklist

- [ ] 3 Stack problems timed — Daily Temperatures explained out loud
- [ ] Mark-to-market P&L SQL written from scratch, runs correctly
- [ ] Story 4 spoken and timed (< 90 sec)
- [ ] Goldman research template filled in
- [ ] Know Goldman's 4 business areas and which is your best fit
- [ ] Applied to any Goldman DE roles found
