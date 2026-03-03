---
created: 2026-03-02
updated: 2026-03-02
summary: Day 44 — Bit Manipulation review, anti-join SQL patterns, and the interview day execution framework.
tags: [study-plan, day-44, week-7, bit-manipulation, anti-join, interview-day]
---

# Day 44 — Bit Manipulation + Anti-Join SQL + Interview Day Framework

**Theme:** If today is your interview day — use the framework below. If not, use it to simulate.

---

## Daily Maintenance (25 min)

**LC — Bit Manipulation (2 problems, timed):**
- LC #136 Single Number (3 min — `result ^= num` for all nums)
- LC #338 Counting Bits (8 min — `dp[i] = dp[i >> 1] + (i & 1)`)

Core operations — verify from memory (write each):
```
n & (n-1)   → clear lowest set bit
n & (-n)    → isolate lowest set bit
n >> 1      → divide by 2
n << 1      → multiply by 2
a ^ a       → 0 (XOR self)
a ^ 0       → a (XOR zero)
```

**SQL — Anti-Join Patterns:**
```sql
-- Three equivalent anti-join patterns — know all three:

-- 1. LEFT JOIN + IS NULL (most common)
SELECT s.server_id FROM servers s
LEFT JOIN daily_metrics m ON s.server_id = m.server_id
    AND m.report_date = '2026-03-01'
WHERE m.server_id IS NULL;

-- 2. NOT EXISTS (clearest intent)
SELECT server_id FROM servers s
WHERE NOT EXISTS (
    SELECT 1 FROM daily_metrics m
    WHERE m.server_id = s.server_id
      AND m.report_date = '2026-03-01'
);

-- 3. NOT IN (dangerous with NULLs — know the risk)
SELECT server_id FROM servers
WHERE server_id NOT IN (
    SELECT server_id FROM daily_metrics
    WHERE report_date = '2026-03-01'
    -- Bug: if any server_id in subquery is NULL, result is always empty
);
```

---

## Interview Day Framework (use this if you have an interview today)

### Before the Call Starts

- Log in 5 minutes early
- Say: "Hi [Name], great to meet you. I'm excited to be here."
- If shared coding environment: open it, make sure it's working

### The Problem Statement

When the problem is read to you:
1. **Listen fully** — don't start typing
2. **Restate** in your own words: "So I need to find X, given Y constraints, returning Z?"
3. **Ask about edge cases**: "Should I handle empty input? Can values be negative? Are duplicates possible?"
4. **Confirm the output format**: "Do you want a list, a single value, a modified input?"

### Working the Problem

```
Phase 1 (3-5 min): Think out loud
  "My first instinct is [brute force approach]. That's O(n²).
   I think I can improve it to O(n) by [pattern/insight]."

Phase 2 (coding): Narrate as you write
  "I'm initializing a hash map here to track..."
  "This while loop runs until..."
  "I'm returning the length of the path..."

Phase 3 (done): Test before saying "done"
  "Let me trace through the example: input is [2,7,11,15], target is 9.
   i=0, complement is 7, not in map yet. i=1, complement is 2, found at index 0.
   Return [0, 1]. Correct."

Phase 4: Complexity
  "Time: O(n) because we iterate once and each hash lookup is O(1).
   Space: O(n) for the hash map in the worst case."
```

### Common Pitfalls During the Interview

| Situation | What to do |
|-----------|-----------|
| Completely blank | "Let me think out loud — a brute force would be..." |
| Wrong approach halfway through | "I see an issue — let me step back. The problem with my current approach is..." |
| Interviewer gives a hint | "That's helpful — so if I [apply hint], then..." Thank them, use it. |
| Finished early | "I'm done. Let me check edge cases: what if the input is empty? ...what if there are duplicates?" |
| Ran out of time | "I didn't finish coding but my approach would be [explain]. The key insight is [X]." Partial credit is real. |

### After Every Question

- "Does that solution look correct to you?"
- "Is there anything you'd like me to optimize or change?"

---

## Day 44 Checklist

- [ ] Both bit manipulation problems solved from memory
- [ ] All 6 bit operations written without looking
- [ ] All 3 anti-join patterns written — NOT IN NULL risk explained
- [ ] Interview day framework memorized (know the 4 phases)
- [ ] Know what to say when completely blank
- [ ] If interview today: executed the protocol. Post-screen reflection started.
