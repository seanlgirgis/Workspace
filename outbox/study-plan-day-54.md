---
created: 2026-03-02
updated: 2026-03-02
summary: Day 54 — Rapid-fire full practice session covering LC, SQL, architecture concepts, and behavioral all in one sitting.
tags: [study-plan, day-54, week-8, rapid-fire, full-practice, interview-simulation]
---

# Day 54 — Full Rapid-Fire Practice Session

**Theme:** Simulate the cognitive load of a real technical interview day — multiple formats back-to-back with no breaks.

---

## Rules for Today

- No notes during any section
- Timer on for everything
- Treat every answer as if an interviewer is watching
- After each section: score yourself honestly

---

## Section 1 — LC Sprint (30 min)

5 problems, 6 minutes each. No hints.

1. LC #1 Two Sum
2. LC #322 Coin Change
3. LC #207 Course Schedule (cycle detection)
4. LC #84 Largest Rectangle in Histogram
5. LC #300 Longest Increasing Subsequence

After: score each. Full = solved correctly in time. Partial = correct approach, syntax error. None = wrong or no progress.

`Score: ___ / 5`

---

## Section 2 — SQL Sprint (20 min)

Write each query from scratch. Run if possible.

1. (4 min) 7-day trailing average CPU per server using window function
2. (4 min) Servers not reporting in last 3 days (LEFT JOIN anti-join)
3. (4 min) Top 3 servers by CPU per region (ROW_NUMBER + WHERE rn <= 3)
4. (4 min) Daily P&L per book (positions × prices → LAG for prior day)
5. (4 min) Recursive CTE to walk infra_hierarchy from root to leaves

`Score: ___ / 5`

---

## Section 3 — Architecture Rapid Fire (15 min)

60 seconds per question. Out loud.

1. What is the difference between a Kafka consumer offset and a consumer group?
2. What does `enable.idempotence=true` do in a Kafka producer?
3. What is AQE in Spark and what does it fix?
4. When does Delta Lake's MERGE outperform a DELETE + INSERT?
5. What is a data contract and what does it contain?

`Score: ___ / 5`

---

## Section 4 — Behavioral Sprint (15 min)

3 questions, 90 seconds each. No rambling.

1. "Tell me about a time you caught a data issue before it reached production."
2. "What would your previous team say is your biggest strength as a data engineer?"
3. "Why are you the right person for a Senior DE role at a finance firm?"

After: is each answer under 90 seconds? Specific? Owned?

`Score: ___ / 3`

---

## Total Score: ___ / 18

**Interpretation:**
- 16-18: Interview-ready for this round
- 13-15: Strong, 1-2 weak spots to drill
- 10-12: 3+ gaps, need focused practice
- Below 10: Return to specific week's material

---

## Post-Session Analysis (10 min)

```
Weakest section today: ___
Specific problem/question that stumped me: ___
Study action: revisit Day [N], problem [X]
Pattern I need more reps on: ___
```

---

## Day 54 Checklist

- [ ] All 4 sections completed with timer running
- [ ] Total score logged: ___ / 18
- [ ] Post-session analysis written
- [ ] Study action identified for weakest area
- [ ] Application tracker checked — any new responses to act on?
