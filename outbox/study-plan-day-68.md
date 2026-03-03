---
created: 2026-03-02
updated: 2026-03-02
summary: Day 68 — Ceiling-raiser LC session. Hard problems designed to push beyond comfortable Medium difficulty.
tags: [study-plan, day-68, week-10, leetcode, hard, ceiling-raiser]
---

# Day 68 — Ceiling-Raiser LC Session

**Theme:** A hard LC problem in a final round is a filter, not a trick. The company isn't expecting perfection — they're watching how you think when you're stuck. Today you practice thinking out loud under pressure.

---

## Daily Maintenance (20 min)

**SQL — Window function from memory:**
Write a query that computes, for each trading desk, the 7-day rolling average P&L, the 7-day max P&L, and the rank of today's P&L within those 7 days. Use `OVER (PARTITION BY desk_id ORDER BY trade_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`.

---

## Ceiling-Raiser Session (90 min)

### Rules for This Session

1. **Always narrate.** Say what you're thinking before you code it.
2. **If stuck for 3 minutes — draw the example.** Manually trace through it.
3. **If stuck for 5 minutes — ask yourself:** "What is the state I need to track?"
4. **Never give up silently.** Even if you can't finish, narrate the approach you'd take.

These are the same behaviors that matter in a real interview. The session trains the behavior, not just the solution.

---

### Problem Set (attempt in order, timed)

**Problem 1 — LC #42 Trapping Rain Water (15 min)**

Classic hard. Two approaches exist:
- Stack-based: maintain decreasing stack, compute trapped water when stack decreases
- Two-pointer O(1) space: `left_max`, `right_max`; process side with smaller max first

If you solved this before: write the two-pointer version from memory, then explain why the side with the smaller max is the bottleneck.

If this is new: write the stack approach first (easier to reason about), then optimize.

**Problem 2 — LC #295 Find Median from Data Stream (20 min)**

Two-heap approach:
- `small` = max-heap (negate values in Python) — lower half
- `large` = min-heap — upper half
- Invariant: `len(small) == len(large)` or `len(small) == len(large) + 1`
- Median: `small[0]` if odd, `(-small[0] + large[0]) / 2` if even

Walk through the invariant maintenance out loud before coding.

**Problem 3 — LC #239 Sliding Window Maximum (20 min)**

Deque approach — monotonic decreasing deque of indices:
- Pop from right while `nums[dq[-1]] <= nums[i]`
- Pop from left while `dq[0] < i - k + 1` (out of window)
- Append `i`, record `nums[dq[0]]` as window max when `i >= k-1`

This is a pattern — same deque logic appears in other hard problems.

**Problem 4 — Choice (15 min)**

Pick based on your real weakness:
- Trees: LC #297 Serialize/Deserialize Binary Tree (BFS with null markers)
- DP: LC #312 Burst Balloons (interval DP, `dp[i][j]` = max coins bursting all between i and j last)
- Graph: LC #127 Word Ladder (BFS with character substitution, build adjacency on the fly)
- Heap: LC #23 Merge K Sorted Lists (min-heap of `(val, list_index, node)`)

---

### After the Session — Stuck Point Analysis

For each problem where you got stuck:

```
Problem: ___
Where I got stuck: ___
The insight I was missing: ___
The pattern this belongs to: ___
What I'll recognize next time: ___
```

The goal isn't to memorize solutions — it's to internalize the "stuck → insight" pathway so it happens faster in the real interview.

---

### The "What Would You Do Next?" Protocol

For any problem you didn't finish: write a 3-sentence description of the approach you'd take if you had 10 more minutes. Practice saying this out loud.

In a real final round: "I haven't finished the implementation, but here's exactly how I'd complete it..." — this signals problem-solving judgment even without a fully working solution.

---

## Day 68 Checklist

- [ ] Rolling 7-day window SQL written from memory (ROWS BETWEEN 6 PRECEDING)
- [ ] Trapping Rain Water solved (two-pointer version preferred)
- [ ] Find Median from Data Stream solved (two-heap, invariant stated before coding)
- [ ] Sliding Window Maximum solved (deque, monotonic decreasing)
- [ ] Problem 4 attempted — weakest pattern chosen
- [ ] Stuck point analysis completed for any problem that took > time limit
- [ ] "What would you do next?" narrated out loud for any incomplete solution
