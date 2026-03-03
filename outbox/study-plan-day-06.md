---
created: 2026-02-28
updated: 2026-02-28
summary: Day 6 blueprint — Intervals + Schema Design (star/snowflake/SCD) + PySpark + System Design (Data Platform). Full notebook content pre-written. Gemini formats only.
tags: [study-plan, day-06, leetcode, sql, python, system-design, blueprint]
---

# Day 6 — Intervals + Schema Design + PySpark + System Design: Data Platform

**Theme:** Intervals are everywhere in data engineering — time ranges, scheduling windows, overlap detection. Schema design and PySpark complete the data engineering picture. System design is the capstone.

> **Gemini instruction:** This file is the complete notebook blueprint. Every labeled `[CELL N: ...]` block is the exact content for that notebook cell. Read a section, copy the labeled blocks into the .ipynb JSON. Do not invent, rewrite, or supplement. Format only.

---

## Spaced Repetition — Questions from Days 1–5

*Run all 9. Mark Strong / Review / Weak. Weak items = drill twice today.*

**From Day 1:**
1. Explain how HashMap solves Two Sum in O(n). *(Answer: as you iterate, check if `target - num` is already in the map. Store each num → index. One pass.)*

**From Day 2:**
2. Sliding Window — when do you shrink the left pointer? *(Answer: when the window violates the constraint — e.g., duplicate found, window length exceeds k, character count exceeds allowed.)*
3. What is lazy evaluation in Spark? Name one example. *(Answer: transformations like `filter()` and `map()` are not executed until an action — like `count()` or `write()` — is called. Allows the Catalyst optimizer to build the full execution plan.)*

**From Day 3:**
4. What is a monotonic stack and what is it useful for? *(Answer: a stack that is always kept in sorted order. Useful for "next greater element", "largest rectangle", "daily temperatures".)*

**From Day 4:**
5. How do you binary search a 2D matrix as if it were 1D? *(Answer: flatten index: row = mid // cols, col = mid % cols. Total elements = rows × cols.)*
6. What are the three pillars of observability? *(Answer: Metrics — what is happening. Logs — why it happened. Traces — where in the distributed system it happened.)*

**From Day 5:**
7. How does a two-heap median finder work? *(Answer: max-heap (lower half) + min-heap (upper half). Balance sizes — lo can have at most 1 more than hi. Median = root of lo if odd count, average of both roots if even.)*
8. What is the Four-Step Capacity Planning Loop? *(Answer: Baseline → Model (identify driver) → Forecast (70% ceiling) → Right-size (provision + document review date).)*
9. What is the difference between `log.error` and `log.exception`? *(Answer: `log.exception` includes the full stack trace automatically — use it in except blocks.)*

---

## A. LeetCode — Intervals

**Pattern:** Intervals `[start, end]` — most problems require **sorting by start**. Then:
- **Merge overlapping:** track max end as you iterate
- **Insert interval:** find where new interval fits; merge with overlaps
- **Non-overlapping removal:** sort by END, greedy keep earliest-ending
- **Meeting rooms:** min-heap of end times, count concurrent

**Golden rule:** Two intervals `[a, b]` and `[c, d]` overlap if and only if `a <= d AND c <= b`.

---

### LC #56 — Merge Intervals [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\lc-0056-merge-intervals.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day6\lc-0056-merge-intervals.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 56: Merge Intervals
---

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #e3f2fd; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> Sort by start time. Then a single pass is sufficient: if the current interval's start is ≤ the last merged interval's end, they overlap — extend the last merged interval's end to max(both ends). If not, they don't overlap — add current as a new merged interval.
</div>

### 🛠️ The Mathematical Model

After sorting by start, two adjacent intervals overlap if and only if `intervals[i][0] <= merged[-1][1]`. When they overlap, the merged end is `max(merged[-1][1], intervals[i][1])`.

$$\text{overlap condition: } start_i \leq end_{last} \Rightarrow end_{merged} = \max(end_{last}, end_i)$$

---

### 📋 Problem

Given an array of intervals where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return the resulting array of non-overlapping intervals.

**Example 1:**
```
Input:  [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```

**Example 2:**
```
Input:  [[1,4],[4,5]]
Output: [[1,5]]
```

**Constraints:** 1 ≤ intervals.length ≤ 10⁴ | 0 ≤ start_i ≤ end_i ≤ 10⁴
```

---

**[CELL 2: MENTAL MODELS]** *(markdown)*

```
### 🧠 Choose Your Mental Model

<table style="width:100%; border-collapse: collapse;">
    <tr style="background-color: #f2f2f2; text-align: left;">
        <th style="padding: 12px; border: 1px solid #ddd;">Model</th>
        <th style="padding: 12px; border: 1px solid #ddd;">The "Story"</th>
        <th style="padding: 12px; border: 1px solid #ddd;">Mechanism</th>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Timeline Painter</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"I'm painting a timeline. Each interval is a stroke. Sort strokes by start. If the next stroke starts before my current stroke ends, extend my current stroke. If it starts after, finish the current stroke and start a new one."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Track `last_end`. Extend if `start <= last_end`. Otherwise append new interval.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Booking Consolidator</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Consolidate overlapping hotel bookings into continuous stays. Sort by check-in. If next guest checks in before current guest checks out, merge into one stay (checkout = latest of both)."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Sort by start + max(ends) merging = contiguous stay consolidation</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Naive pairwise comparison checks all O(n²) pairs. After sorting once (O(n log n)), a single linear pass merges in O(n). Total: O(n log n) — the sort dominates.
</div>

## 🐢 Approach 1: Brute Force — $O(n^2)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def merge_brute(intervals):
    """
    Brute Force: Repeatedly scan for any pair that overlaps and merge them
    Time: O(n^2) | Space: O(n)
    """
    intervals = [list(i) for i in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(intervals)):
            for j in range(i + 1, len(intervals)):
                a, b = intervals[i], intervals[j]
                # Overlap check: [a0,a1] and [b0,b1] overlap if a0<=b1 and b0<=a1
                if a[0] <= b[1] and b[0] <= a[1]:
                    intervals[i] = [min(a[0], b[0]), max(a[1], b[1])]
                    intervals.pop(j)
                    changed = True
                    break
            if changed:
                break
    return sorted(intervals)


print(merge_brute([[1,3],[2,6],[8,10],[15,18]]))   # Expected: [[1,6],[8,10],[15,18]]
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n^2)$ vs. $O(n \log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> After sorting by start time, overlapping intervals are always adjacent. We never need to check non-adjacent pairs. A single linear pass from left to right processes each interval exactly once — O(n) after the O(n log n) sort.
</div>

---

## 📉 Why Brute Force Fails: The $O(n^2)$ Trap

Pairwise comparison: for n = 10,000 intervals, that's 50 million pair checks. Each merge requires another scan from the beginning.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **All overlapping** | O(n²) merges | Each merge triggers full rescan |
| **Already sorted** | O(n²) pair checks | Still checks all pairs |

---

## 🚀 The Optimal Approach: $O(n \log n)$

Sort by start time. Maintain a `merged` result list. For each interval:
- If it overlaps with the last merged (start ≤ last_end), extend last merged's end
- Otherwise, append as a new merged interval

### The Key Lifecycle Rule
1. **Sort by start time** — ensures overlapping intervals are adjacent
2. **Initialize merged** with the first interval
3. **For each subsequent interval:** extend if overlap, append if not

---

## ✅ Mathematical Proof

After sorting, if intervals i and j overlap (i < j), there is no non-overlapping interval k between them (otherwise j's start > k's end > i's end, contradiction). So all overlapping intervals form contiguous groups — a single pass processes each group.

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Sorting transforms a 2D comparison problem into a 1D scan. After sorting by start, all overlapping intervals are adjacent — one pass with max(ends) merging is sufficient.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Sort + Linear Merge — $O(n \log n)$
---

Instead of pairwise comparison, we use **sort once, scan once**.

As we iterate:
1. Sort intervals by start time
2. Initialize merged = [intervals[0]]
3. For each interval: if start ≤ merged[-1][1], extend. Else append.
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """
    Optimal: Sort by start, single linear merge pass
    Time: O(n log n) | Space: O(n) for output
    """
    intervals.sort(key=lambda x: x[0])   # sort by start time
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        if start <= last_end:           # overlap — extend
            merged[-1][1] = max(last_end, end)   # critical: max, not just end
        else:                           # no overlap — new interval
            merged.append([start, end])

    return merged


print("Optimal:", merge([[1,3],[2,6],[8,10],[15,18]]))   # Expected: [[1,6],[8,10],[15,18]]
print("Optimal:", merge([[1,4],[4,5]]))                   # Expected: [[1,5]]
print("Optimal:", merge([[1,4],[2,3]]))                   # Expected: [[1,4]] (containment)
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: What is the time complexity and why?

**Answer:** O(n log n) — dominated by the sort. The subsequent linear scan is O(n). For n = 10,000 intervals: sort takes ~130,000 comparisons, scan takes 10,000. Total = O(n log n).

---

### Q2: Why `max(last_end, end)` and not just `end`?

**Answer:** One interval can completely contain another — e.g., [1,10] followed by [2,5] in sorted order. Without max, processing [2,5] after [1,10] would shrink the merged end to 5, losing the [5,10] portion. `max(last_end, end)` preserves the farthest endpoint seen.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(n log n). The sort is O(n log n) — this dominates. The merge pass is O(n) — each interval is processed exactly once. Overall: O(n log n + n) = O(n log n).

---

### Q4: How would you solve this if intervals were already sorted?

**Answer:** Skip the sort, go straight to the merge pass: O(n). Initialize merged = [intervals[0]], then the same extend/append logic. The sort is the only thing that makes the naive O(n²) problem solvable in O(n) — if it's free, we get O(n).

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Single interval — for loop never executes, merged = [[start, end]], returned directly. (2) All overlapping — all intervals merge into one. (3) No overlapping (already disjoint) — each interval appended as-is, output = sorted input. (4) One interval containing another — [1,10] then [2,5]: max(10, 5) = 10, correctly extends. (5) Adjacent touching — [1,4],[4,5]: start=4 ≤ last_end=4, merged. Problem says [4,5] as example.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Interval** | A range `[start, end]` representing a contiguous segment of values or time |
| **Overlap** | Two intervals `[a,b]` and `[c,d]` overlap if `a ≤ d AND c ≤ b` — they share at least one point |
| **Merge** | Combining two overlapping intervals into one: `[min(starts), max(ends)]` |
| **Sort by Start** | The key preprocessing step — makes overlapping intervals adjacent in the sorted order |
| **Max(ends)** | Critical in merge: accounts for containment (one interval fully inside another) |
| **Containment** | When interval B is fully inside interval A — A contains B. max(ends) handles this case. |
| **Disjoint Intervals** | Non-overlapping intervals — the output of merge() is always disjoint |
| **Linear Scan** | Single O(n) pass after sorting — processes each interval exactly once |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's capacity planning team tracked server maintenance windows — time ranges when servers were taken offline for patching. For compliance reporting, they needed to report total downtime hours per server per quarter, without double-counting overlapping windows.

**Scenario:** A server might have three maintenance windows in a quarter: [09:00-11:00], [10:30-12:30], [15:00-16:00]. Naive sum = 5.5 hours. Correct merged: [[09:00-12:30],[15:00-16:00]] = 4.5 hours. Merge Intervals was the algorithm.

**How this pattern applied:** For 6,000 servers × multiple maintenance windows each quarter, sorting windows by start time and then linear merge pass produced accurate per-server downtime in O(n log n). The alternative — pairwise overlap checks — was O(n²) per server.

**Impact:** Quarterly downtime compliance reports for 6,000 servers produced in seconds instead of hours. More importantly, accurate merged downtime caught double-counting errors in the previous manual process — the real total downtime was 15% lower than previously reported, which changed SLA compliance calculations.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given a list of intervals representing employee
# working hours, find the free time (gaps between working hours).
# E.g. [[1,3],[6,7],[9,12]] → free time: [[3,6],[7,9]]
# -------------------------------------------------------

def findFreeTime(intervals):
    intervals.sort(key=lambda x: x[0])
    # Your solution here — find gaps between merged intervals
    pass


# Test
print(findFreeTime([[1,3],[6,7],[9,12]]))     # Expected: [[3,6],[7,9]]
print(findFreeTime([[1,3],[2,4],[5,6]]))      # Expected: [[4,5]]
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Sort + Linear Merge** — Sort by start time; one pass with max(ends) merging handles all overlap cases

### When to Use It
- ✅ Merging overlapping time ranges, windows, bookings, events
- ✅ Computing total covered time without double-counting
- ✅ Preprocessing for other interval operations (insert interval, etc.)
- ❌ **Don't use when:** Intervals are streaming (need different approach — interval tree or sorted container)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (pairwise) | $O(n^2)$ | $O(n)$ |
| Optimal (Sort + Scan) | $O(n \log n)$ | $O(n)$ |

### Interview Confidence Checklist
- [ ] Can state the overlap condition from memory: `a ≤ d AND c ≤ b`
- [ ] Can explain why max(ends) is needed (containment case)
- [ ] Can write the solution from memory in 4 minutes
- [ ] Can reduce to O(n) when input is pre-sorted
- [ ] Can connect to maintenance window / downtime reporting use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Merge Intervals and you've mastered the foundational interval technique — sort once, scan once, handle all cases. 🚀
```

---

### LC #57 — Insert Interval [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\lc-0057-insert-interval.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day6\lc-0057-insert-interval.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 57: Insert Interval
---

<div style="padding: 15px; border-left: 8px solid #FF5722; background-color: #fbe9e7; color: #bf360c; border-radius: 4px;">
    <strong>The Core Insight:</strong> The existing intervals are already sorted and non-overlapping. Process them in three phases: (1) intervals entirely before the new one — add directly. (2) Intervals overlapping the new one — merge all into one. (3) Intervals entirely after — add directly. Three sequential while loops, each handling one phase.
</div>

### 🛠️ The Mathematical Model

For existing interval `[s, e]` and new interval `[ns, ne]`:
- Before: `e < ns` — no overlap, add `[s, e]`
- Overlap: `s <= ne` — merge: `ns = min(ns,s)`, `ne = max(ne,e)`
- After: `s > ne` — no overlap, add remaining

---

### 📋 Problem

You are given a sorted, non-overlapping array of intervals and a new interval. Insert the new interval (merging if necessary) and return the result.

**Example 1:**
```
Input:  intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
Output: [[1,2],[3,10],[12,16]]
```

**Example 2:**
```
Input:  intervals = [[1,5]], newInterval = [2,3]
Output: [[1,5]]
```

**Constraints:** 0 ≤ intervals.length ≤ 10⁴ | intervals sorted by start, non-overlapping | 0 ≤ start_i ≤ end_i ≤ 10⁵
```

---

**[CELL 2: MENTAL MODELS]** *(markdown)*

```
### 🧠 Choose Your Mental Model

<table style="width:100%; border-collapse: collapse;">
    <tr style="background-color: #f2f2f2; text-align: left;">
        <th style="padding: 12px; border: 1px solid #ddd;">Model</th>
        <th style="padding: 12px; border: 1px solid #ddd;">The "Story"</th>
        <th style="padding: 12px; border: 1px solid #ddd;">Mechanism</th>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Three-Phase Scan</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"I'm walking along a sorted timeline. First, I pass intervals that end before my new one starts — copy them. Then, I hit intervals that overlap my new one — merge them all into one big interval. Finally, I copy everything after."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Three sequential while loops: before, merge, after. Linear O(n).</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Maintenance Blackout Insert</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Adding a new maintenance window to a sorted schedule. Windows before it stay. Windows that overlap with it get absorbed. Windows after it stay."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Three clear phases, each handled by one while loop condition</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Appending the new interval and re-running merge is O(n log n) — the sort is unnecessary since intervals are already sorted. Three-phase scan is O(n) — no sort needed.
</div>

## 🐢 Approach 1: Brute Force — $O(n \log n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def insert_brute(intervals, newInterval):
    """
    Brute Force: Append new interval and re-run merge
    Time: O(n log n) — re-sorts even though input was already sorted
    """
    intervals = intervals + [newInterval]
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


print(insert_brute([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]))  # Expected: [[1,2],[3,10],[12,16]]
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n \log n)$ vs. $O(n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The input is already sorted. We don't need to sort again. The three-phase scan exploits the pre-sorted order: scan past intervals before the new one, merge all overlapping ones into the new interval, then copy the rest. One linear pass = O(n).
</div>

---

## 📉 Why Brute Force Fails: The $O(n \log n)$ Trap

Re-sorting throws away the pre-sorted property of the input — wasted work.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **Already sorted input** | O(n log n) | Sort runs even though input is sorted |
| **n = 10,000** | ~130,000 sort ops | All wasted — could be 10,000 with linear scan |

---

## 🚀 The Optimal Approach: $O(n)$

Three sequential while loops, each with a clear stopping condition:
1. **Phase 1:** `intervals[i][1] < new[0]` — interval ends before new starts → add to result
2. **Phase 2:** `intervals[i][0] <= new[1]` — interval overlaps new → expand new's boundaries
3. **Phase 3:** Remaining intervals after the merge — add all directly

### The Key Lifecycle Rule
1. **Copy all intervals that end before new starts** (`end < new_start`)
2. **Merge all overlapping intervals into new** (`start <= new_end`)
3. **Append new, then copy remaining intervals**

---

## ✅ Mathematical Proof

Each interval is visited exactly once by exactly one of the three while loops. Three loops together = O(n) total. No comparisons are repeated.

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Three-phase scan is the optimal pattern for insert-into-sorted-intervals. Each phase has one clean stopping condition. O(n) total — no sort needed.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Three-Phase Linear Scan — $O(n)$
---

Instead of re-sorting, we exploit the pre-sorted order with **three sequential while loops**.

As we iterate:
1. **Loop 1:** Copy intervals that end before new interval starts
2. **Loop 2:** Merge all intervals that overlap with new interval (expand new's boundaries)
3. Append the (now merged) new interval; **Loop 3:** Copy remaining intervals
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def insert(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """
    Optimal: Three-phase linear scan
    Time: O(n) | Space: O(n) for output
    """
    result = []
    i = 0
    n = len(intervals)

    # Phase 1: intervals that end before new starts — no overlap
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Phase 2: intervals that overlap with new — merge into new
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])   # expand new's start if needed
        new[1] = max(new[1], intervals[i][1])   # expand new's end if needed
        i += 1
    result.append(new)   # append the merged new interval

    # Phase 3: intervals that start after new ends — no overlap
    while i < n:
        result.append(intervals[i])
        i += 1

    return result


print("Optimal:", insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]))   # [[1,2],[3,10],[12,16]]
print("Optimal:", insert([[1,5]], [2,3]))                               # [[1,5]]
print("Optimal:", insert([], [5,7]))                                    # [[5,7]]
print("Optimal:", insert([[1,5]], [6,8]))                               # [[1,5],[6,8]]
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: What are the three phases of the algorithm?

**Answer:** Phase 1: copy all intervals whose end is strictly before the new interval's start — they can't overlap. Stopping condition: `intervals[i][1] < new[0]`. Phase 2: merge all intervals that overlap with new — stopping condition: `intervals[i][0] <= new[1]`. Phase 3: copy all remaining intervals — they start after the new interval ends.

---

### Q2: Why is this O(n) while the brute force is O(n log n)?

**Answer:** The input is already sorted. The optimal algorithm exploits this — no sort needed. Three sequential while loops, each scanning forward without backtracking, means each interval is visited exactly once. Total: O(n). Brute force re-sorts (O(n log n)) unnecessarily.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(n). Each of the n intervals is processed by exactly one of the three while loops — they collectively scan the array left to right without revisiting any interval. The pointer `i` only ever increments. No nested loops, no sorting = O(n).

---

### Q4: What if the new interval doesn't overlap with any existing interval?

**Answer:** Phase 2 may execute zero iterations (new interval fits in a gap — its start is after all Phase 1 intervals end and before Phase 3 intervals start). The new interval is appended at the correct sorted position between the Phase 1 and Phase 3 results. The algorithm handles this naturally.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Empty intervals — Phase 1 and Phase 3 are skipped, Phase 2 is skipped, just append new. (2) New interval before all — Phase 1 is empty, Phase 2 may start from index 0. (3) New interval after all — Phase 1 processes all, Phase 2 is empty, new is appended at end. (4) New interval contains all existing — Phase 2 processes all, result is just [new] after merging. All handled by the three-loop structure.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Insert Interval** | Adding a new interval to a sorted non-overlapping list, merging with any overlapping intervals |
| **Three-Phase Scan** | Algorithm structure: before-merge-after, each phase a separate while loop with a clear stopping condition |
| **Pre-Sorted Property** | The given intervals are already sorted by start — enables O(n) insertion without re-sorting |
| **Phase 1 Condition** | `intervals[i][1] < new[0]` — interval ends before new starts, no overlap, safe to copy |
| **Phase 2 Condition** | `intervals[i][0] <= new[1]` — interval starts before new ends, overlap, must merge |
| **Expand Boundaries** | In Phase 2: `new[0] = min(new[0], intervals[i][0])`, `new[1] = max(new[1], intervals[i][1])` |
| **Non-overlapping** | Intervals in the output are guaranteed disjoint (no two share any point) |
| **In-order Processing** | The pointer `i` only increments — each interval is visited at most once |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's server scheduling system maintained a sorted list of approved maintenance windows. When a new unplanned maintenance was emergency-approved, it needed to be inserted into the existing schedule — merging with any windows it overlapped.

**Scenario:** Existing schedule: [[02:00-04:00], [06:00-08:00], [14:00-16:00]]. Emergency maintenance: [03:30-07:00]. Result: [[02:00-04:00] overlaps → extend, [06:00-08:00] overlaps → extend] = merged window [02:00-08:00]. Final schedule: [[02:00-08:00],[14:00-16:00]].

**How this pattern applied:** The three-phase scan found Phase 1 intervals (none here since [02:00] overlaps [03:30-07:00]), merged Phase 2 overlapping windows, and appended Phase 3 remainder. The algorithm ran in O(n) — no re-sort of the existing approved schedule.

**Impact:** Emergency maintenance insertions became instant — no recalculation of the full schedule. The system updated the maintenance calendar in real time as emergency windows were approved, preventing scheduling conflicts where two maintenance operations would have targeted the same server simultaneously.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Add a meeting to a calendar. The calendar
# has existing non-overlapping meetings sorted by start time.
# If the new meeting overlaps any existing meeting, return False
# (cannot schedule it). Otherwise insert it and return the new calendar.
# -------------------------------------------------------

def addMeeting(calendar, new_meeting):
    # Check for any overlap — if overlap exists, return False
    # If no overlap, insert at correct sorted position and return new calendar
    pass


# Test
print(addMeeting([[1,3],[5,7]], [4,5]))    # Expected: [[1,3],[4,5],[5,7]] — wait, [4,5] and [5,7] touch
print(addMeeting([[1,3],[5,7]], [3,5]))    # Expected: False (overlaps [1,3] at 3, [5,7] at 5)
print(addMeeting([[1,3],[6,8]], [4,5]))    # Expected: [[1,3],[4,5],[6,8]]
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Three-Phase Linear Scan** — Before | Merge | After, each phase a while loop with a clear stopping condition

### When to Use It
- ✅ Insert into sorted non-overlapping interval list
- ✅ Adding events/windows to a sorted calendar
- ✅ When input is guaranteed sorted — O(n), no sort needed
- ❌ **Don't use when:** Input is unsorted — sort first then use Merge Intervals (LC #56)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (re-sort) | $O(n \log n)$ | $O(n)$ |
| Optimal (Three-Phase) | $O(n)$ | $O(n)$ |

### Interview Confidence Checklist
- [ ] Can describe all three phases and their stopping conditions
- [ ] Can write all three while loops from memory
- [ ] Can explain why no sort is needed (pre-sorted input)
- [ ] Can trace through the edge case where new interval overlaps all existing
- [ ] Can connect to maintenance window scheduling use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Insert Interval and you've mastered the three-phase pattern — before, merge, after. It's clean, linear, and elegant. 🚀
```

---

### LC #435 — Non-overlapping Intervals [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\lc-0435-non-overlapping.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day6\lc-0435-non-overlapping.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 435: Non-overlapping Intervals
---

<div style="padding: 15px; border-left: 8px solid #4CAF50; background-color: #e8f5e9; color: #1b5e20; border-radius: 4px;">
    <strong>The Core Insight:</strong> To minimize removals = maximize intervals we can keep. Greedy rule: when two intervals overlap, always keep the one that ends earlier — it leaves the most room for future intervals. Sort by END time and apply this greedy choice.
</div>

### 🛠️ The Mathematical Model

Minimum removals = n - maximum non-overlapping intervals we can keep.
Greedy: always select the interval with the earliest end time from the remaining non-overlapping candidates.

$$\text{min removals} = n - \text{count of non-overlapping intervals (greedy)}$$

---

### 📋 Problem

Find the minimum number of intervals to remove to make the remaining intervals non-overlapping.

**Example 1:**
```
Input:  [[1,2],[2,3],[3,4],[1,3]]
Output: 1   (remove [1,3])
```

**Example 2:**
```
Input:  [[1,2],[1,2],[1,2]]
Output: 2   (keep one, remove two)
```

**Constraints:** 1 ≤ intervals.length ≤ 10⁵ | -5×10⁴ ≤ start_i < end_i ≤ 5×10⁴
```

---

**[CELL 2: MENTAL MODELS]** *(markdown)*

```
### 🧠 Choose Your Mental Model

<table style="width:100%; border-collapse: collapse;">
    <tr style="background-color: #f2f2f2; text-align: left;">
        <th style="padding: 12px; border: 1px solid #ddd;">Model</th>
        <th style="padding: 12px; border: 1px solid #ddd;">The "Story"</th>
        <th style="padding: 12px; border: 1px solid #ddd;">Mechanism</th>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Activity Selection</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"I can only do one activity at a time. To fit the MOST activities in a day, always pick the activity that finishes earliest — it frees up time for the next one soonest."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Sort by end time. Keep intervals that start ≥ last_end. Count removals = n - kept.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Conference Room Optimizer</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"One conference room, many meetings. Cancel the minimum meetings so the rest don't conflict. Always cancel the meeting that ends later when two conflict — the shorter meeting leaves more room."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">When two intervals overlap, the one ending later is removed (or equivalently: the one ending earlier is kept).</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Trying all subsets of intervals is O(2^n). The greedy approach runs in O(n log n) — sort once, scan once.
</div>

## 🐢 Approach 1: Brute Force — $O(2^n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
from itertools import combinations

def eraseOverlapIntervals_brute(intervals):
    """
    Brute Force: Try all subsets, find largest non-overlapping subset
    Time: O(2^n * n) | Space: O(n)
    """
    def is_non_overlapping(subset):
        subset = sorted(subset)
        for i in range(1, len(subset)):
            if subset[i][0] < subset[i-1][1]:   # overlap check
                return False
        return True

    n = len(intervals)
    max_kept = 0
    for size in range(n, 0, -1):
        for subset in combinations(intervals, size):
            if is_non_overlapping(list(subset)):
                max_kept = size
                break
        if max_kept:
            break
    return n - max_kept


# Small test only (exponential — don't run on large input)
print(eraseOverlapIntervals_brute([[1,2],[2,3],[3,4],[1,3]]))   # Expected: 1
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(2^n)$ vs. $O(n \log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> Greedy correctness: when two intervals overlap, keeping the one that ends earlier is always optimal — it cannot reduce the number of future intervals we can keep (it ends sooner, freeing up more timeline). This greedy choice is provably optimal for the Activity Selection Problem.
</div>

---

## 📉 Why Brute Force Fails: The $O(2^n)$ Trap

2^n subsets for n = 50 intervals: ~10¹⁵ subsets. Infeasible.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **n = 20** | ~1 million subsets | Exponential growth |
| **n = 50** | ~10¹⁵ subsets | Completely infeasible |

---

## 🚀 The Optimal Approach: $O(n \log n)$

Sort by END time. Greedily keep intervals. For each interval:
- If `start >= last_end`: no overlap — keep it, update `last_end = end`
- If `start < last_end`: overlap — remove it (increment counter)

### The Key Lifecycle Rule
1. **Sort by END time** (not start time — this is the key difference from Merge Intervals)
2. **Greedily keep** intervals that start after the last kept interval's end
3. **Count removals** = number of skipped intervals

---

## ✅ Mathematical Proof (Greedy Correctness)

Suppose optimal solution keeps interval A (ends late) over interval B (ends early, overlaps A). Swap A for B — B ends earlier, so it cannot conflict with more future intervals than A does. Therefore swapping never makes the solution worse. The greedy choice (keep earliest-ending) is optimal. ∎

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Sort by END (not start). Keep intervals that don't overlap the last kept. Count removals. The greedy proof shows that keeping the earliest-ending interval is always optimal.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Greedy — Sort by End Time — $O(n \log n)$
---

Instead of trying all subsets, we use a **greedy rule: always keep the interval that ends earliest**.

As we iterate:
1. Sort by END time (critical — not start time)
2. Track `last_end = -∞`
3. For each interval: if `start >= last_end`, keep it (update last_end). Else, remove it (increment counter).
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    """
    Optimal: Greedy — sort by end time, keep earliest-ending
    Time: O(n log n) | Space: O(1)
    """
    intervals.sort(key=lambda x: x[1])   # sort by END time (not start!)
    removals = 0
    last_end = float('-inf')

    for start, end in intervals:
        if start >= last_end:    # no overlap — keep this interval
            last_end = end
        else:
            removals += 1        # overlap — remove (we implicitly keep the earlier-ending one)

    return removals


print("Optimal:", eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]]))   # Expected: 1
print("Optimal:", eraseOverlapIntervals([[1,2],[1,2],[1,2]]))          # Expected: 2
print("Optimal:", eraseOverlapIntervals([[1,2],[2,3]]))                # Expected: 0
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why sort by end time instead of start time?

**Answer:** Greedy correctness — we want to maximize the number of intervals we can keep. The interval that ends earliest leaves the most remaining timeline for future intervals. Sorting by end time ensures that when we scan left to right, we encounter the earliest-ending interval first and greedily keep it. Sorting by start time does NOT have this property.

---

### Q2: Is this the Activity Selection Problem?

**Answer:** Yes — exactly. The Activity Selection Problem asks: given activities with start and end times, select the maximum number of non-conflicting activities. The greedy solution is identical: sort by end time, greedily select each activity that starts after the previous one ends. LC #435 is the complement: min removals = n - max kept activities.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(n log n) — dominated by the sort. The greedy scan is O(n) — each interval is visited exactly once, and `last_end` and `removals` are updated in O(1). Overall: O(n log n + n) = O(n log n).

---

### Q4: How does this differ from Merge Intervals (LC #56) sorting?

**Answer:** LC #56 sorts by START time — we need adjacent overlapping intervals to be adjacent in sorted order for the merge to work. LC #435 sorts by END time — we need to greedily select intervals that end earliest. Two different interval problems, two different sort keys. Start = merge. End = greedy removal/selection.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) No overlapping — removals = 0. Last_end updates each iteration, start ≥ last_end always true. (2) All same interval — all overlap except first; removals = n-1. (3) Touching intervals (end = next start) — `start >= last_end` with `>=` correctly treats touching as non-overlapping (problem uses open/closed convention — verify). (4) Single interval — for loop runs once, no removals.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Activity Selection Problem** | Classic CS problem: maximum non-conflicting activities from n activities with start/end times. Greedy solution: sort by end, select greedily. |
| **Greedy Algorithm** | Makes the locally optimal choice at each step with the goal of finding a global optimum |
| **Greedy Correctness** | Proof that the greedy choice (keep earliest-ending) is always optimal — shown by exchange argument |
| **Sort by End** | The non-obvious sort key for greedy interval selection problems — enables the Activity Selection greedy |
| **Exchange Argument** | Proof technique: show that swapping the greedy choice for any other never improves the solution |
| **Min Removals** | n minus the maximum number of non-overlapping intervals we can keep |
| **last_end** | Tracks the end time of the last kept interval — the current "right boundary" of the selected set |
| **Touching Intervals** | Intervals that share only an endpoint (e.g., [1,2] and [2,3]) — typically considered non-overlapping |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's infrastructure team had a maintenance calendar with 80 approved maintenance windows for a given weekend — but the network could only support 40 simultaneous maintenance operations (capacity constraint). Many windows overlapped. The goal: cancel the minimum number of windows.

**Scenario:** 80 maintenance windows, sorted by end time. Greedy: keep the window that ends earliest when conflicts arise. In practice, this maximized the number of maintenance operations completed over the weekend — cancelled windows could be rescheduled next weekend.

**How this pattern applied:** The greedy algorithm processed 80 windows in O(80 log 80) ≈ 500 comparisons. For each conflict, the window ending later was cancelled (it blocked more future windows). The result: minimum cancellations with maximum maintenance throughput.

**Impact:** Weekend maintenance scheduling went from manual negotiation (which windows to cancel) to automated greedy optimization. The algorithm consistently found 5-10% more maintenance slots per weekend compared to manual approaches, accelerating the patching backlog reduction.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given intervals, find the MAXIMUM number of
# non-overlapping intervals you can keep (complement of LC #435).
# -------------------------------------------------------

def maxNonOverlapping(intervals):
    # Your solution here — greedy, sort by end
    pass


# Test
print(maxNonOverlapping([[1,2],[2,3],[3,4],[1,3]]))   # Expected: 3 (keep [1,2],[2,3],[3,4])
print(maxNonOverlapping([[1,2],[1,2],[1,2]]))          # Expected: 1
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Greedy — Sort by End** — Always keep the interval that ends earliest; minimizes future conflicts

### When to Use It
- ✅ Minimize removals to make intervals non-overlapping
- ✅ Maximize number of non-conflicting activities (Activity Selection)
- ✅ Scheduling problems where "fewest conflicts" is the goal
- ❌ **Don't use when:** You need to merge overlapping intervals — use LC #56 (sort by start)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (all subsets) | $O(2^n)$ | $O(n)$ |
| Optimal (Greedy, sort by end) | $O(n \log n)$ | $O(1)$ |

### Interview Confidence Checklist
- [ ] Can explain why sort by END (not start) for this problem
- [ ] Can state the greedy correctness proof (exchange argument)
- [ ] Can write the solution in 3 minutes from memory
- [ ] Can relate to Activity Selection Problem by name
- [ ] Can contrast with LC #56 sorting approach
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Non-overlapping Intervals and you've mastered the Activity Selection greedy — one of the most elegant algorithm design insights. 🚀
```

---

### LC #253 — Meeting Rooms II [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\lc-0253-meeting-rooms-ii.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day6\lc-0253-meeting-rooms-ii.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 253: Meeting Rooms II
---

<div style="padding: 15px; border-left: 8px solid #9C27B0; background-color: #f3e5f5; color: #4a148c; border-radius: 4px;">
    <strong>The Core Insight:</strong> We need the peak number of simultaneously running meetings. Use a min-heap of end times. For each new meeting (sorted by start), check if the earliest-ending room is free. If yes, reuse it (heapreplace). If no, open a new room (heappush). The heap size = number of rooms in use.
</div>

### 🛠️ The Mathematical Model

The minimum rooms needed = the maximum simultaneous meetings at any point in time.
We track "rooms in use" via a min-heap of end times — the root is the room that becomes free soonest.

$$\text{min rooms} = \max_{t} |\{[s_i, e_i] : s_i \leq t < e_i\}|$$

---

### 📋 Problem

Given an array of meeting time intervals `[start, end]`, find the minimum number of conference rooms required.

**Example 1:**
```
Input:  [[0,30],[5,10],[15,20]]
Output: 2
```

**Example 2:**
```
Input:  [[7,10],[2,4]]
Output: 1
```

**Constraints:** 1 ≤ intervals.length ≤ 10⁴ | 0 ≤ start_i < end_i ≤ 10⁶
```

---

**[CELL 2: MENTAL MODELS]** *(markdown)*

```
### 🧠 Choose Your Mental Model

<table style="width:100%; border-collapse: collapse;">
    <tr style="background-color: #f2f2f2; text-align: left;">
        <th style="padding: 12px; border: 1px solid #ddd;">Model</th>
        <th style="padding: 12px; border: 1px solid #ddd;">The "Story"</th>
        <th style="padding: 12px; border: 1px solid #ddd;">Mechanism</th>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Room Reuse</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"As each meeting starts, check if any room is free. The room that finishes soonest is checked first. If it's done, reuse it. If not, open a new room. A min-heap of end times tells us which room finishes soonest."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Min-heap of end times. heap[0] = earliest-ending room. If heap[0] ≤ new_start: reuse. Else: new room.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Peak Concurrency</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"The heap size at any point = number of rooms currently in use. The maximum heap size over all time = the minimum rooms needed."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">heappush adds a room. heapreplace reuses a room (no size change). max(len(heap)) = answer.</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Checking all time points for concurrent meetings is O(T × n) where T is the time range. Min-heap approach: O(n log n) — sort once, process each meeting once.
</div>

## 🐢 Approach 1: Brute Force — $O(T \times n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def minMeetingRooms_brute(intervals):
    """
    Brute Force: Check each time point for concurrent meetings
    Time: O(T * n) where T = max time range | Space: O(T)
    """
    if not intervals:
        return 0
    max_time = max(e for _, e in intervals)
    max_rooms = 0
    for t in range(max_time + 1):
        concurrent = sum(1 for s, e in intervals if s <= t < e)
        max_rooms = max(max_rooms, concurrent)
    return max_rooms


print(minMeetingRooms_brute([[0,30],[5,10],[15,20]]))   # Expected: 2
print(minMeetingRooms_brute([[7,10],[2,4]]))             # Expected: 1
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(T \times n)$ vs. $O(n \log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> We only care about "room availability" at meeting START times — not every point in time. Sort meetings by start. At each start, check if the earliest-ending room (min-heap root) is available. If yes: reuse it. If no: add a room. The heap size tracks current room count.
</div>

---

## 📉 Why Brute Force Fails: The $O(T \times n)$ Trap

Checking every time unit up to max_time (potentially 10⁶) × n meetings = up to 10¹⁰ operations.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **max_time = 10⁶, n = 10⁴** | 10¹⁰ checks | One check per time unit per meeting |
| **Long meetings** | Slow | Each long meeting counted at every time unit |

---

## 🚀 The Optimal Approach: $O(n \log n)$

Sort by start time. Maintain a min-heap of end times (each occupied room's end time). For each meeting:
- If `heap[0] <= start`: earliest room just freed → reuse it (`heapreplace(heap, end)`)
- Else: no room available → open new room (`heappush(heap, end)`)
Final answer: `len(heap)` = rooms in use at peak.

### The Key Lifecycle Rule
1. **Sort meetings by start time** — process in chronological order
2. **For each meeting:** check if the soonest-finishing room is free
3. **Reuse or open** — heapreplace (reuse) or heappush (new room)

---

## ✅ Mathematical Proof

The min-heap always contains exactly the set of currently occupied rooms' end times. When we process meeting i (start_i), heap[0] is the earliest that any room becomes free. If heap[0] <= start_i, that room is free — we can reuse it. If not, all rooms are still occupied — we must add one. At the end, len(heap) = number of rooms needed for the peak concurrent period.

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> The heap encodes the "earliest available room." Reuse when available, add when not. len(heap) at end = minimum rooms needed.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Min-Heap of End Times — $O(n \log n)$
---

Instead of checking every time point, we process meetings in **start-time order** and track **room end times** in a min-heap.

As we iterate:
1. Sort by start time
2. For each meeting: check heap[0] (earliest room to free)
3. If heap[0] ≤ start: heapreplace (reuse room). Else: heappush (new room)
4. len(heap) = final room count
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
import heapq

def minMeetingRooms(intervals: list[list[int]]) -> int:
    """
    Optimal: Min-Heap of end times
    Time: O(n log n) | Space: O(n) for heap
    """
    if not intervals:
        return 0
    intervals.sort(key=lambda x: x[0])   # sort by start time
    heap = []   # min-heap of end times (each entry = end time of an occupied room)

    for start, end in intervals:
        if heap and heap[0] <= start:    # earliest room is free
            heapq.heapreplace(heap, end) # reuse that room (pop old end, push new end)
        else:
            heapq.heappush(heap, end)    # all rooms occupied — open new room

    return len(heap)


print("Optimal:", minMeetingRooms([[0,30],[5,10],[15,20]]))   # Expected: 2
print("Optimal:", minMeetingRooms([[7,10],[2,4]]))             # Expected: 1
print("Optimal:", minMeetingRooms([[1,5],[5,10]]))             # Expected: 1 (back-to-back, not concurrent)
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: How does this relate to capacity planning?

**Answer:** Replace "meetings" with "ETL jobs," "monitoring agents," or "database queries." The algorithm tells you the minimum number of worker threads or servers needed to handle peak concurrent workload. At Citi: replace meetings with APM polling intervals — what's the minimum number of polling agents needed to monitor 6,000 servers with no gaps?

---

### Q2: What does `heapreplace` do vs pop + push?

**Answer:** `heapreplace(heap, val)` is an atomic pop + push in O(log n) — it pops the minimum and pushes the new value in a single heap operation. This is more efficient than `heappop` + `heappush` (which would be two O(log n) operations). Use `heapreplace` when you know you'll always push after popping (the room is always reused, not discarded).

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(n log n). Sorting: O(n log n). Processing: n meetings, each does one heap operation (heapreplace or heappush) in O(log n). Total: O(n log n + n log n) = O(n log n). The heap never grows beyond n elements.

---

### Q4: Why sort by start time and not end time?

**Answer:** We process meetings as they start — chronologically. At each meeting's start time, we need to know if any room has become free (end time ≤ current start time). Sorting by start time means we process meetings in the order they begin, which is the natural order for room allocation decisions.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Empty intervals — early return 0. (2) Back-to-back meetings (end = next start) — `heap[0] <= start` uses `<=`, so [0,5] and [5,10] correctly reuse the same room. (3) All at same time — heap grows to n, returns n. (4) All sequential — heap never grows past 1, returns 1.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Peak Concurrency** | The maximum number of meetings/tasks/jobs running simultaneously — what Meeting Rooms II computes |
| **Min-Heap of End Times** | Tracks occupied rooms by their end times — root = earliest room to become free |
| **heapreplace** | Atomic heappop + heappush — removes minimum, inserts new value, single O(log n) operation |
| **Room Reuse** | When heap[0] ≤ new start: the earliest-finishing room is free and can be reassigned |
| **Back-to-back** | Meetings where one ends exactly when the next begins — these are typically non-concurrent (use ≤ for reuse) |
| **Worker Pool** | The heap size = number of workers/rooms/threads needed at peak — the answer to capacity questions |
| **Sort by Start** | Process meetings in chronological order — necessary for correct room allocation decisions |
| **Concurrent** | Multiple meetings occupying different rooms simultaneously — the heap encodes this state |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's monitoring infrastructure needed to determine how many APM polling agents were needed to cover 6,000 servers — each server had a polling window [start, end) during which it expected a heartbeat check.

**Scenario:** 6,000 polling windows with various start/end times. At peak morning hours, many windows overlapped. The minimum number of polling agents = peak concurrent polling windows = Meeting Rooms II on polling intervals.

**How this pattern applied:** Sorted 6,000 polling intervals by start time. Min-heap of end times tracked active polling windows. At peak morning, heap grew to 420 — meaning 420 concurrent polling windows. This set the minimum agent pool size.

**Impact:** Instead of provisioning 6,000 agents (one per server), the algorithm showed 420 agents sufficed for full coverage — a 93% reduction in infrastructure cost. Agent pool was right-sized to peak demand, with 10% buffer added: 462 agents deployed instead of 6,000.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given CPU job intervals [start, end],
# find the MINIMUM number of CPU cores needed to run
# all jobs (no job can be split across cores).
# Same algorithm as Meeting Rooms II.
# -------------------------------------------------------

import heapq

def minCpuCores(jobs):
    # Your solution here — same as minMeetingRooms
    pass


# Test
print(minCpuCores([[0,3],[1,4],[2,5]]))    # Expected: 3 (all concurrent at t=2)
print(minCpuCores([[0,2],[2,4],[4,6]]))    # Expected: 1 (sequential)
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Min-Heap of End Times** — Track occupied rooms; reuse the earliest-finishing room; heap size = current room count

### When to Use It
- ✅ Minimum resources needed for peak concurrent workload
- ✅ Meeting rooms, CPU cores, server agents, worker threads
- ✅ Any "how many do I need simultaneously?" problem
- ❌ **Don't use when:** You want to maximize throughput differently — use LC #435 (greedy by end)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (scan all times) | $O(T \times n)$ | $O(T)$ |
| Optimal (Min-Heap) | $O(n \log n)$ | $O(n)$ |

### Interview Confidence Checklist
- [ ] Can explain the min-heap of end times approach
- [ ] Can explain heapreplace and why it's used
- [ ] Can write the solution from memory in 4 minutes
- [ ] Can explain the relationship to capacity planning
- [ ] Can state the back-to-back edge case and how <= handles it
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Meeting Rooms II and you've solved the algorithmic foundation of capacity planning — minimum resources for peak concurrent demand. 🚀
```

---

### LC #986 — Interval List Intersections [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\lc-0986-interval-intersections.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day6\lc-0986-interval-intersections.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 986: Interval List Intersections
---

<div style="padding: 15px; border-left: 8px solid #FF9800; background-color: #fff3e0; color: #e65100; border-radius: 4px;">
    <strong>The Core Insight:</strong> Two pointers on two sorted interval lists. The intersection of [a,b] and [c,d] is [max(a,c), min(b,d)] — valid only if max(a,c) ≤ min(b,d). After checking, advance the pointer for whichever interval ends first — it can't overlap any remaining intervals in the other list.
</div>

### 🛠️ The Mathematical Model

$$\text{Intersection}([a,b], [c,d]) = [\max(a,c), \min(b,d)] \text{ if } \max(a,c) \leq \min(b,d)$$
$$\text{Advance pointer: advance } i \text{ if } b < d, \text{ else advance } j$$

---

### 📋 Problem

Given two lists of closed intervals, each sorted and non-overlapping within itself, return their intersection.

**Example 1:**
```
A = [[0,2],[5,10],[13,23],[24,25]]
B = [[1,5],[8,12],[15,24],[25,26]]
Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
```

**Constraints:** 0 ≤ firstList.length, secondList.length ≤ 1000 | 0 ≤ start_i < end_i ≤ 10⁹
```

---

**[CELL 2: MENTAL MODELS]** *(markdown)*

```
### 🧠 Choose Your Mental Model

<table style="width:100%; border-collapse: collapse;">
    <tr style="background-color: #f2f2f2; text-align: left;">
        <th style="padding: 12px; border: 1px solid #ddd;">Model</th>
        <th style="padding: 12px; border: 1px solid #ddd;">The "Story"</th>
        <th style="padding: 12px; border: 1px solid #ddd;">Mechanism</th>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Two Highlighters</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Two people highlight sections of a document with different colors. The overlapping (doubly-highlighted) sections are the intersections. Walk both highlights left to right with two pointers — whenever they overlap, record it. Advance whichever highlight ends first."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Two pointers i, j on sorted lists. Intersection = [max(starts), min(ends)] if valid. Advance lesser end.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Calendar Overlap</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Find when two people are both available (or both busy). Walk their schedules with two pointers — when their intervals overlap, that's the intersection. Move the pointer for whoever's interval ends first."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Two pointers, advance shorter interval — it can't overlap any further intervals from the other list</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Checking all O(m × n) pairs is O(m × n). Two-pointer approach exploits the sorted order to process all pairs in O(m + n).
</div>

## 🐢 Approach 1: Brute Force — $O(m \times n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def intervalIntersection_brute(A, B):
    """
    Brute Force: Check all O(m * n) pairs
    Time: O(m * n) | Space: O(1) extra
    """
    result = []
    for a, b in A:
        for c, d in B:
            lo = max(a, c)
            hi = min(b, d)
            if lo <= hi:
                result.append([lo, hi])
    return result


A = [[0,2],[5,10],[13,23],[24,25]]
B = [[1,5],[8,12],[15,24],[25,26]]
print(intervalIntersection_brute(A, B))   # Expected: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(m \times n)$ vs. $O(m + n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The lists are sorted. An interval that ends before the current interval in the other list can't possibly overlap any future intervals in the other list. So when we process a pair, we can safely advance the pointer for whichever interval ends first. This ensures we never revisit any interval from either list.
</div>

---

## 📉 Why Brute Force Fails: The $O(m \times n)$ Trap

Every interval in A checked against every interval in B: m × n pairs. For m = n = 1000: 1,000,000 pair checks.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **m = n = 1000** | 1 million comparisons | All pairs checked |
| **Disjoint lists** | m × n checks | Still checks all pairs before concluding no overlap |

---

## 🚀 The Optimal Approach: $O(m + n)$

Two pointers i=0 (into A) and j=0 (into B). At each step:
- Compute intersection `[max(A[i][0], B[j][0]), min(A[i][1], B[j][1])]`
- If valid (lo ≤ hi): add to result
- Advance the pointer for whichever interval ends first (it can't overlap the next interval in the other list)

### The Key Lifecycle Rule
1. **Intersection formula:** `[max(starts), min(ends)]` — valid if max ≤ min
2. **Advance:** pointer for interval with smaller end. It's "used up" — can't overlap anything further in the other list.

---

## ✅ Mathematical Proof

If A[i][1] < B[j][1], then A[i] ends before B[j]. Any future B intervals start at B[j+1][0] ≥ B[j][0] > A[i][1] (since B is sorted and non-overlapping). So A[i] can't intersect any B[j'] for j' > j. Safe to advance i.

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Two pointers + sorted order → each interval is visited at most once. O(m + n) instead of O(m × n). The advance-the-shorter rule is the key — the shorter interval is "done," it can't overlap anything further in the other list.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Two Pointers — $O(m + n)$
---

Instead of checking all pairs, we use **two pointers advancing through both sorted lists simultaneously**.

As we iterate:
1. Compute intersection: `lo = max(A[i][0], B[j][0])`, `hi = min(A[i][1], B[j][1])`
2. If `lo <= hi`: valid intersection — append
3. Advance the pointer for whichever interval ends first: `if A[i][1] < B[j][1]: i += 1; else: j += 1`
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def intervalIntersection(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    """
    Optimal: Two pointers on sorted lists
    Time: O(m + n) | Space: O(1) extra (output not counted)
    """
    result = []
    i = j = 0

    while i < len(A) and j < len(B):
        lo = max(A[i][0], B[j][0])   # intersection start = max of both starts
        hi = min(A[i][1], B[j][1])   # intersection end = min of both ends
        if lo <= hi:                  # valid intersection (non-empty)
            result.append([lo, hi])

        # Advance the pointer for the interval that ends first
        # That interval is "used up" — can't overlap anything further in the other list
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1

    return result


A = [[0,2],[5,10],[13,23],[24,25]]
B = [[1,5],[8,12],[15,24],[25,26]]
print("Optimal:", intervalIntersection(A, B))
# Expected: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: How do you compute the intersection of two intervals?

**Answer:** For intervals [a,b] and [c,d], the intersection is [max(a,c), min(b,d)]. It's valid (non-empty) if `max(a,c) ≤ min(b,d)`. The max of starts ensures we start where both are active. The min of ends ensures we stop when the first one ends. If max > min, they don't overlap.

---

### Q2: Why advance the pointer for the interval that ends first?

**Answer:** If A[i][1] < B[j][1], then A[i] ends before B[j]. B[j] and all subsequent B intervals start at or after B[j][0] > A[i][1] (sorted, non-overlapping). So A[i] cannot intersect with B[j] or any later B interval. Advancing i is safe — we've found all possible intersections involving A[i].

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(m + n). Each pointer (i for A, j for B) only ever increments — never decrements. i goes from 0 to m-1, j goes from 0 to n-1. Total iterations ≤ m + n. Each iteration is O(1). No intervals from either list are visited more than once.

---

### Q4: What real-world problem is this pattern solving?

**Answer:** "Find when two systems were both operational" — e.g., when were both System A and System B running simultaneously (for SLA joint compliance)? Or: "find time windows when two server maintenance schedules overlap." The two interval lists represent uptime windows for each system; intersections are the joint uptime.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) One list is empty — while loop never executes, returns []. (2) No overlaps — lo > hi for every pair, result is []. (3) One interval contains another — e.g., [1,10] and [2,5]: intersection = [2,5], then advance j (5 < 10). (4) Touching intervals [a,b] and [b,c] — intersection = [b,b] (valid since lo = b ≤ hi = b). Point intersection is included.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Interval Intersection** | The overlap between two intervals [a,b] and [c,d] = [max(a,c), min(b,d)], valid if max ≤ min |
| **Two-Pointer Technique** | Two indices advancing through two sorted structures — O(m+n) instead of O(m×n) brute force |
| **Advance the Shorter** | The rule that determines which pointer advances: the interval ending first is "done" |
| **Valid Intersection** | When `lo ≤ hi` — the computed intersection is non-empty and should be recorded |
| **Closed Interval** | [a,b] includes both endpoints a and b — touching intervals [a,b] and [b,c] have a point intersection [b,b] |
| **Joint Uptime** | Time windows when two systems are simultaneously operational — computed via interval intersection |
| **Monotone Advance** | Pointers only move forward — ensures O(m+n) total iterations |
| **Disjoint Lists** | When A and B have no overlapping intervals — two-pointer exits with empty result in O(m+n) |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's SLA compliance team needed to compute "joint uptime" — time windows when BOTH the primary monitoring system and the backup monitoring system were simultaneously operational, for regulatory reporting.

**Scenario:** Primary system uptime intervals (sorted): [[00:00-06:00],[08:00-20:00],[22:00-24:00]]. Backup system uptime intervals (sorted): [[01:00-07:00],[09:00-21:00],[23:00-24:00]]. Joint uptime = intersection of both lists.

**How this pattern applied:** Two-pointer technique on the two sorted uptime interval lists. At each step: compute intersection, record if valid, advance the pointer for whichever uptime window ends first. O(m + n) for any number of uptime windows.

**Impact:** Monthly joint uptime reports for 6,000 server pairs (primary + backup pairs) computed in O(m + n) per pair instead of O(m × n). Report generation time dropped from 45 minutes (nested loop approach) to under 30 seconds. Regulators received accurate joint uptime percentages for SLA compliance documentation.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given two sorted lists of "busy time" intervals
# for two people, find all times when BOTH are free.
# Complement: free time = gaps in combined busy time.
# Step 1: find union of all busy time. Step 2: find gaps.
# -------------------------------------------------------

def findJointFreeTime(person_a_busy, person_b_busy, day_start, day_end):
    # Step 1: find intersection (joint busy time)
    # or alternatively: merge all busy times, find gaps
    pass


# Test
a_busy = [[1,3],[5,8]]
b_busy = [[2,4],[6,9]]
print(findJointFreeTime(a_busy, b_busy, 0, 10))   # Both free during [4,5] and [9,10]
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Two Pointers on Sorted Lists** — O(m+n) intersection instead of O(m×n) brute force; advance the shorter interval

### When to Use It
- ✅ Intersection of two sorted non-overlapping interval lists
- ✅ "When are both systems simultaneously active?"
- ✅ Joint availability windows, concurrent uptime, overlap detection
- ❌ **Don't use when:** Lists are unsorted — sort first (O(n log n + m log m))

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (all pairs) | $O(m \times n)$ | $O(1)$ extra |
| Optimal (Two Pointers) | $O(m + n)$ | $O(1)$ extra |

### Interview Confidence Checklist
- [ ] Can state the intersection formula [max(starts), min(ends)]
- [ ] Can explain the "advance the shorter" rule and why it's correct
- [ ] Can write the solution from memory in 3 minutes
- [ ] Can explain the valid intersection condition (lo ≤ hi)
- [ ] Can connect to joint uptime / SLA compliance use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Interval Intersections and you've mastered the two-pointer pattern applied to intervals — a clean O(m+n) algorithm for a problem that looks like O(m×n). 🚀
```

---

## B. SQL — Schema Design: Star Schema, Snowflake, SCD Type 2

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\sql-schema-design.ipynb`

**Use the SQL section in the existing study plan (marked "## B. SQL — Schema Design: Star Schema, Snowflake, SCD Type 2") for all code cells. Do not invent new code.**

Core concept for notebook: "Schema design separates data engineers from analysts. Star = denormalized for speed. Snowflake = normalized for consistency. SCD Type 2 = the standard for tracking historical changes."

Citi narrative: Citi's capacity analytics warehouse used a star schema. Fact table: fact_monitoring (event_id, server_id, date_id, metric_id, value). Dimension: dim_server with SCD Type 2 — when a server moved teams, a new row was added. This let analysts ask "which team owned this server at the time of the incident?" — critical for incident post-mortems. Impact: historical accuracy in incident reports went from "current team" to "team at incident time" — changed root cause attribution for 12% of incidents.

---

## C. Python — PySpark for Data Engineering

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\python-pyspark.ipynb`

**Use the Python section in the existing study plan (marked "## C. Python — PySpark for Data Engineering") for all code cells. Do not invent new code.**

Citi narrative: Citi's ETL pipeline migrated from pandas to PySpark when data volume exceeded 50GB/day. Key lesson: Python UDFs were the bottleneck — they serialized data row-by-row from JVM to Python, 10x slower than built-in F. functions. Replacing Python UDFs with `F.when().otherwise()` chains cut job runtime from 45 minutes to 4 minutes for the daily capacity aggregation.

---

## D. Technology — System Design: Design a Data Platform

**Notebook file:** `D:\Workspace\StudyMaterial\Day6\system-design-data-platform.ipynb`

**Use the Tech section in the existing study plan (marked "## D. Technology — System Design: Real-Time Monitoring & Capacity Data Platform") for all code cells. Do not invent new code.**

This is a narration notebook, not a code notebook. The cells should present the design framework as structured markdown — architecture diagram (ASCII art), key design decisions, trade-offs. Use concept notebook template format.

Citi narrative: This is Sean's actual Citi architecture. The design exists — describe it accurately. Kafka → Flink/Spark Streaming → S3 Parquet → Glue → Athena → Grafana. Key trade-off: Athena ($5/TB scanned, serverless, good for ad-hoc) vs Redshift (provisioned, faster for repeated complex BI queries).

---

## Behavioral Anchor — Citi Story #6: System Design in Production

> **Gemini:** At end of session, say: "Tell me about the most complex data system you designed or contributed to at Citi. Two minutes — go."

**Story framework:**
- **Situation:** 6,000 monitored endpoints, growing. Data siloed in APM tools — no unified platform for capacity analysis across applications.
- **Task:** Design a scalable, queryable data store for monitoring telemetry supporting both real-time alerting and trend analysis.
- **Action:** Evaluated Kafka vs. direct S3 ingest (chose Kafka for replay capability); built Glue + Athena layer for ad-hoc SQL; wrote Python pipeline to compute rolling baselines daily.
- **Result:** Single platform replaced 4 separate APM reporting processes. Query time for monthly capacity reports dropped from 2 hours to 8 minutes.

---

## End of Day 6 — Wrap-Up Format

```
Day 6 Scorecard
Spaced Repetition: [N/9 Strong] [N Review] [N Weak]
LeetCode (Intervals): [5 problems — mark each: Strong/Review/Weak]
SQL (Schema Design): [Strong/Review/Weak]
Python (PySpark): [Strong/Review/Weak]
Tech (System Design): [Strong/Review/Weak]
Behavioral: [Citi Story #6 — Strong / Needs work]

WEAK items to drill in Day 7 mock:
→
→
```

**Gemini:** List all WEAK items from this session AND from prior sessions. Tell Sean:
> "Tomorrow is the mock interview. These are your known gaps: [list]. I'll target them."

If 3+ items are WEAK → tell Sean: "Escalate to Claude Code — these need reinforcement files."
