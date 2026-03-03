---
created: 2026-02-28
updated: 2026-02-28
summary: Day 4 blueprint — Binary Search | SQL Query Optimization | NumPy & Vectorization | APM & Observability. Full notebook content pre-written. Gemini formats only.
tags: [study-plan, day-4, leetcode, sql, python, apm, observability, blueprint]
---

# Study Day 4: Search, Optimization, and Observability
**Theme:** Binary Search + SQL Optimization + NumPy + APM — Sean's Core Differentiator

> **Gemini instruction:** This file is the complete notebook blueprint. Every labeled `[CELL N: ...]` block is the exact content for that notebook cell. Read a section, copy the labeled blocks into the .ipynb JSON. Do not invent, rewrite, or supplement. Format only.

---

## Spaced Repetition — Review from Days 1-3
*60 seconds each.*

**SR-1:** HashMap Top-K — fastest approach in O(n)?
> Count with Counter/HashMap (O(n)), then bucket sort by frequency using frequency as index (O(n)) — avoids heap's O(n log k).

**SR-2:** Sliding window — what triggers left pointer movement in LC #3 (no repeating chars)?
> When current char is already in the window. Jump left to one position past the previous occurrence of that char.

**SR-3:** Monotonic stack — what makes it "monotonic"?
> Elements in the stack maintain a sorted order (increasing or decreasing). Elements that violate the order are popped before the new element is pushed.

**SR-4:** Anti-join — why is NOT IN dangerous?
> If the subquery returns any NULL, the entire NOT IN condition evaluates to NULL (unknown), filtering out all rows. Use NOT EXISTS instead.

**SR-5:** Lambda vs Kappa architecture — what's Lambda's main weakness?
> Two codebases (batch + streaming) for the same logic. They drift apart over time, causing inconsistencies in results.

**SR-6:** Spark shuffle — name two operations that trigger it.
> groupBy, join (without broadcast), repartition, distinct, sort.

---

## A. LeetCode — Binary Search

> **Discussion opener:** "Binary search is O(log n) — not just for sorted arrays. The real pattern: define a search space, write a condition that tells you if you're too high or too low, eliminate half the space at each step. Works on any monotonic condition."

---

### LC #704 — Binary Search [Easy]

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\lc-0704-binary-search.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day4\lc-0704-binary-search.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 704: Binary Search
---

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #e3f2fd; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The array is sorted. Every comparison eliminates HALF the remaining candidates. Binary search is O(log n) because you halve the problem space at every step — 1 billion elements requires at most 30 comparisons.
</div>

### 🛠️ The Mathematical Model

Binary search works on any **monotonic condition**: a predicate that is False for the first part of the array and True for the rest (or vice versa). We exploit this to eliminate half the search space with each comparison.

$$T(n) = T(n/2) + O(1) \Rightarrow O(\log n)$$

---

### 📋 Problem

Given a sorted array of integers `nums` and an integer `target`, return the index of `target` or `-1` if not found. You must write an algorithm with O(log n) runtime complexity.

**Example 1:**
```
Input:  nums = [-1,0,3,5,9,12], target = 9
Output: 4
```

**Example 2:**
```
Input:  nums = [-1,0,3,5,9,12], target = 2
Output: -1
```

**Constraints:** 1 ≤ nums.length ≤ 10⁴ | -10⁴ < nums[i], target < 10⁴ | All integers are unique | nums is sorted ascending
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Phone Book</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"I need page 500 in a 1000-page book. I open to 500 — if it's there, done. If the name I want comes after, I ignore the left half entirely."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Sorted order + midpoint comparison → eliminate half the pages with each flip</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Guess the Number</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Guess 1-100. I say 'too low' or 'too high'. Optimal play: always guess the midpoint. 7 guesses to cover 100 numbers."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Binary feedback → geometric convergence → log₂(n) steps maximum</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Linear scan ignores sorted order entirely. For 10,000 elements, brute force may check all 10,000. Binary search checks at most 14.
</div>

## 🐢 Approach 1: Brute Force — $O(n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def search_brute(nums, target):
    """
    Brute Force: Linear scan — check every element
    Time: O(n) | Space: O(1)
    """
    for i, num in enumerate(nums):
        if num == target:
            return i
    return -1


# Test Cases
print(search_brute([-1, 0, 3, 5, 9, 12], 9))   # Expected: 4
print(search_brute([-1, 0, 3, 5, 9, 12], 2))   # Expected: -1
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n)$ vs. $O(\log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> Sorted order is information. Linear scan throws that information away. Binary search exploits it — every comparison is a question: "Is my target in the left half or the right half?" The answer eliminates 50% of remaining candidates.
</div>

---

## 📉 Why Brute Force Fails: The $O(n)$ Trap

Linear scan checks elements one by one. On a sorted array of n=10,000 elements with target at index 9,999, brute force makes 10,000 comparisons. Binary search makes 14.

$$\text{Brute}: n \text{ comparisons} \quad \text{vs} \quad \text{Binary}: \lceil \log_2 n \rceil \text{ comparisons}$$

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **Target at end** | n comparisons | Must scan everything before finding it |
| **Target missing** | n comparisons | Must exhaust all elements to confirm absence |

---

## 🚀 The Optimal Approach: $O(\log n)$

Maintain two pointers `left` and `right` defining the current search window. At each step, check `mid = (left + right) // 2`. Three cases: found, go left, go right. Window halves each iteration.

### The Key Lifecycle Rule
1. **When `nums[mid] == target`:** return mid — found it
2. **When `nums[mid] < target`:** target is to the right — set `left = mid + 1`
3. **When `nums[mid] > target`:** target is to the left — set `right = mid - 1`

---

## ✅ Mathematical Proof

$$\text{After 1 step: } n/2 \text{ elements remain} \quad \text{After k steps: } n/2^k \text{ remain}$$
$$\text{Stop when } n/2^k = 1 \Rightarrow k = \log_2 n$$

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Binary search makes exactly ⌈log₂ n⌉ comparisons — 14 for n=10,000, 30 for n=1,000,000,000. The sorted invariant guarantees every comparison eliminates exactly half the search space.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Binary Search — $O(\log n)$
---

Instead of scanning linearly, we use **two pointers** as a **shrinking search window**.

As we iterate:
1. Compute `mid = left + (right - left) // 2` (overflow-safe)
2. Compare `nums[mid]` to target — eliminate the half that cannot contain the target
3. Continue until `left > right` (not found) or `nums[mid] == target` (found)
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def search(nums, target):
    """
    Optimal: Binary Search
    Time: O(log n) | Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2   # avoid integer overflow (good habit from C/Java)
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1      # target is in the right half
        else:
            right = mid - 1     # target is in the left half

    return -1


print("Optimal:", search([-1, 0, 3, 5, 9, 12], 9))   # Expected: 4
print("Optimal:", search([-1, 0, 3, 5, 9, 12], 2))   # Expected: -1
print("Optimal:", search([5], 5))                       # Expected: 0 (single element)
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why use `left + (right - left) // 2` instead of `(left + right) // 2`?

**Answer:** Integer overflow prevention. In Python, integers are unbounded — so both work. But in C/Java, if `left` and `right` are both near INT_MAX (~2 billion), `left + right` overflows to a negative number. The subtraction form avoids this. It's a signal to interviewers that you know systems-level concerns.

---

### Q2: When is `left <= right` correct vs `left < right`?

**Answer:** Use `left <= right` when you need to examine single-element windows (you might need to check the last remaining element). Use `left < right` when you're converging on a *boundary* — e.g., finding the first position where a condition is True. LC #704 needs `<=` because the target might be the last remaining element.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** $O(\log n)$. Each iteration, the search window `[left, right]` is cut in half. Starting from n elements, after k iterations, n/2^k elements remain. We stop when n/2^k = 1, which means k = log₂(n) iterations. The number of steps grows as the logarithm of the input size.

---

### Q4: What does binary search require of the input?

**Answer:** The input must be **sorted** (or more generally, the predicate must be **monotonic** — False for one contiguous range and True for another). Without sorted order, we cannot guarantee that eliminating a half is safe. Also assumes no duplicates in standard binary search; duplicates require variant logic.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Empty array — `left=0, right=-1`, while loop never executes, returns -1 correctly. (2) Single element — `left=right=0`, mid=0, checks the one element. (3) Target smaller than all elements — `right` shrinks to -1, exits with -1. (4) Target larger than all — `left` grows past `right`, exits with -1. All handled by `left <= right` condition.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Binary Search** | Divide-and-conquer search algorithm for sorted arrays — eliminates half the search space per step |
| **Search Window** | The subarray `[left, right]` currently under consideration — shrinks by half each iteration |
| **Midpoint** | `mid = left + (right - left) // 2` — the pivot index compared to the target |
| **Monotonic Condition** | A predicate that transitions from False to True exactly once across the array — binary search requires this |
| **Integer Overflow** | When an arithmetic result exceeds the max value of a fixed-size integer type — `(left + right)` overflows in C/Java |
| **Search Space** | The set of candidate values that could contain the target — binary search halves this each step |
| **Invariant** | A property that remains true throughout an algorithm — here: target, if it exists, is always within `[left, right]` |
| **Convergence** | `left > right` — the termination condition when the search window is exhausted |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi APM infrastructure — 6,000 monitored endpoints, daily capacity baselines stored as sorted time-series data.

**Scenario:** When an analyst queried "what was the CPU reading for server SRV-1042 closest to timestamp 14:37:00 on a given day?" the naive approach scanned the entire day's readings (1,440 minutes = 1,440 records per server) linearly.

**How this pattern applied:** Because readings were stored sorted by timestamp, binary search was applicable. For any timestamp query, `bisect.bisect_right` on the sorted timestamp list returned the insertion point in O(log 1440) ≈ 11 comparisons instead of up to 1,440. This same pattern powered LC #981 (Time Based KV Store) — the algorithmic connection between the monitor query and the interview problem is direct.

**Impact:** Query response time for point-in-time lookups dropped from O(n) linear scans to O(log n) — for a system with 6,000 servers × 1,440 readings each, this reduced worst-case comparisons from 1,440 to 11. Dashboards that showed historical point-in-time readings became interactive (sub-second) instead of requiring 2–3 second waits.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Implement binary search to find the LEFTMOST
# position where target could be inserted to keep nums sorted.
# (This is bisect_left behavior — find first index where nums[i] >= target)
# -------------------------------------------------------

def search_insert(nums, target):
    # Your solution here — use binary search
    pass


# Test
print(search_insert([1, 3, 5, 6], 5))   # Expected: 2
print(search_insert([1, 3, 5, 6], 2))   # Expected: 1
print(search_insert([1, 3, 5, 6], 7))   # Expected: 4
print(search_insert([1, 3, 5, 6], 0))   # Expected: 0
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Binary Search** — Exploit sorted order to halve the search space at every step

### When to Use It
- ✅ Array is sorted (or condition is monotonic)
- ✅ Need O(log n) search instead of O(n)
- ✅ "Find position of X", "Find first/last occurrence of X", "Find boundary between True/False"
- ❌ **Don't use when:** Array is unsorted and sorting first (O(n log n)) outweighs the search savings

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (linear scan) | $O(n)$ | $O(1)$ |
| Optimal (Binary Search) | $O(\log n)$ | $O(1)$ |

### Interview Confidence Checklist
- [ ] Can explain why sorted order enables binary search
- [ ] Can state `left <= right` vs `left < right` difference
- [ ] Can write the solution from memory in 3 minutes
- [ ] Can state time and space complexity with justification
- [ ] Can name the overflow-safe midpoint formula and why it matters
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Binary Search and you've mastered one of the most fundamental patterns in computer science — the mathematical consequence of sorted order. 🚀
```

---

### LC #74 — Search a 2D Matrix [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\lc-0074-search-2d-matrix.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day4\lc-0074-search-2d-matrix.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 74: Search a 2D Matrix
---

<div style="padding: 15px; border-left: 8px solid #9C27B0; background-color: #f3e5f5; color: #4a148c; border-radius: 4px;">
    <strong>The Core Insight:</strong> This matrix is one sorted array folded into a 2D grid. If you unfold it back into 1D, standard binary search applies. The key is the index conversion: row = mid // cols, col = mid % cols.
</div>

### 🛠️ The Mathematical Model

A matrix with `rows × cols` elements has indices 0 to `rows*cols - 1` in 1D. Element at 1D index `i` sits at `matrix[i // cols][i % cols]` in 2D. Binary search runs on the 1D index space.

$$\text{1D index} \rightarrow \text{row} = \lfloor i / \text{cols} \rfloor, \quad \text{col} = i \bmod \text{cols}$$

---

### 📋 Problem

Write an efficient algorithm that searches for a value `target` in an `m × n` integer matrix where each row is sorted ascending and the first integer of each row is greater than the last integer of the previous row.

**Example 1:**
```
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
Output: true
```

**Example 2:**
```
Input:  matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
Output: false
```

**Constraints:** m, n ∈ [1, 100] | -10⁴ ≤ matrix[i][j], target ≤ 10⁴
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Unfolded Array</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Imagine cutting the matrix row by row and laying the rows end-to-end — you get a sorted array. Binary search that array, then fold the index back into 2D coordinates."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">mid // cols = row, mid % cols = col — the fold/unfold math</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>1D Abstraction</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"I don't see rows and columns. I see positions 0 to m*n-1. The 2D structure is just a display format."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Binary search on integer range [0, rows*cols-1], translate at access time</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> A nested loop scans every cell — O(m × n). Binary search treats the matrix as a 1D sorted array and runs in O(log(m × n)).
</div>

## 🐢 Approach 1: Brute Force — $O(m \times n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def searchMatrix_brute(matrix, target):
    """
    Brute Force: Check every cell
    Time: O(m * n) | Space: O(1)
    """
    for row in matrix:
        for val in row:
            if val == target:
                return True
    return False


print(searchMatrix_brute([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3))   # True
print(searchMatrix_brute([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13))  # False
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(m \times n)$ vs. $O(\log(m \times n))$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The matrix's row-ordering property means the entire grid is a sorted 1D sequence in disguise. Once we recognize this, we can apply standard binary search on the index range [0, m*n-1], converting 1D indices to 2D coordinates at each step.
</div>

---

## 📉 Why Brute Force Fails: The $O(m \times n)$ Trap

A nested loop iterates through every cell without using the sorted property. For a 100×100 matrix, that's 10,000 cell checks. Binary search needs at most log₂(10,000) ≈ 14 checks.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **Target in last cell** | m × n comparisons | Must scan the entire matrix |
| **Target not present** | m × n comparisons | Cannot short-circuit without sorted property |

---

## 🚀 The Optimal Approach: $O(\log(m \times n))$

Treat the matrix as a 1D sorted array of length `rows × cols`. Binary search on indices 0 to `rows*cols - 1`. For each `mid` index, convert to matrix coordinates: `row = mid // cols`, `col = mid % cols`.

### The Key Lifecycle Rule
1. **Compute mid** in 1D space: `mid = left + (right - left) // 2`
2. **Convert to 2D**: `row = mid // cols`, `col = mid % cols`, access `matrix[row][col]`
3. **Compare and eliminate** exactly like standard binary search

---

## ✅ Mathematical Proof

$$\text{1D size} = m \times n \Rightarrow \text{Binary search steps} = \lceil \log_2(m \times n) \rceil = \lceil \log_2 m + \log_2 n \rceil$$

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> The 2D structure is irrelevant once we see the matrix as a sorted 1D array. Index math (// and %) converts between representations in O(1). Binary search runs in O(log(m*n)).
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Binary Search on Flattened Index — $O(\log(m \times n))$
---

Instead of nested loops, we use **1D binary search** with a **2D index translation** at each step.

As we iterate:
1. Set `left = 0, right = rows * cols - 1`
2. Compute `mid`, translate to `row = mid // cols, col = mid % cols`
3. Compare `matrix[row][col]` to target — eliminate left or right half
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def searchMatrix(matrix, target):
    """
    Optimal: Binary Search on 1D flattened index
    Time: O(log(m * n)) | Space: O(1)
    """
    rows, cols = len(matrix), len(matrix[0])
    left, right = 0, rows * cols - 1

    while left <= right:
        mid = left + (right - left) // 2
        row, col = mid // cols, mid % cols   # key: unfold 1D index to 2D coordinates
        val = matrix[row][col]

        if val == target:
            return True
        elif val < target:
            left = mid + 1
        else:
            right = mid - 1

    return False


print("Optimal:", searchMatrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 3))   # True
print("Optimal:", searchMatrix([[1,3,5,7],[10,11,16,20],[23,30,34,60]], 13))  # False
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: How do you convert a 1D index to 2D matrix coordinates?

**Answer:** For a matrix with `cols` columns: `row = index // cols`, `col = index % cols`. This is integer division for the row, modulo for the column. Example: in a 4-column matrix, 1D index 7 → row = 7 // 4 = 1, col = 7 % 4 = 3 → matrix[1][3].

---

### Q2: What if the matrix rows are sorted but the first element of each row is NOT greater than the last of the previous row?

**Answer:** Then the matrix is not a contiguous sorted sequence — we can't use 1D binary search. Instead, use the staircase search: start at top-right corner (largest in row 1, smallest in last column). If target < current, move left. If target > current, move down. O(m + n) time.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** $O(\log(m \times n))$. The search space has `m * n` elements. Each step eliminates half. So the number of steps is log₂(m × n). The 2D index conversion (// and %) is O(1), so it doesn't change the asymptotic complexity.

---

### Q4: Could you binary search each row individually instead?

**Answer:** Yes — binary search each of the `m` rows for target: O(m log n). This is worse than O(log(m*n)) = O(log m + log n) which equals O(log(m*n)). The full-matrix binary search is strictly better because it uses the *inter-row* sorted property, not just within-row sorting.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) 1×1 matrix — `left=right=0`, checks the single element. (2) Single row — same as 1D binary search. (3) Single column — `cols=1`, every `mid // 1 = mid` gives row correctly, `mid % 1 = 0` gives col 0 correctly. All edge cases are handled by the general formula.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Flattening** | Converting a multi-dimensional structure to 1D — a matrix of m×n becomes an array of length m*n |
| **Index Translation** | Converting between 1D and 2D coordinates: `row = i // cols`, `col = i % cols` |
| **Contiguous Sorted** | The matrix property that every row is sorted AND each row's first element exceeds the previous row's last — enables 1D binary search |
| **Staircase Search** | Alternative algorithm starting at top-right: move left if too big, down if too small — O(m+n), used when row-first-element property doesn't hold |
| **Integer Division (//)** | Floor division — used to compute the row in 2D translation |
| **Modulo (%)** | Remainder — used to compute the column in 2D translation |
| **Search Space** | The range of 1D indices [0, m*n-1] considered as binary search candidates |
| **2D Matrix** | An m×n grid — in Python, a list of lists; rows are the outer list, columns the inner |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Capacity reporting at Citi — daily metric snapshots stored as a 2D structure: rows = servers (6,000), columns = time slots (24 hourly readings). Finding whether a specific (server, hour) reading exceeded a threshold.

**Scenario:** Given a sorted report matrix (sorted by server_id, then by hour within each row), determine if a specific utilization value exists without scanning all 144,000 cells.

**How this pattern applied:** The report matrix satisfied the contiguous-sorted property — server IDs increase row by row, and within each row, hourly readings increase. Binary search on the flattened index found any value in O(log 144,000) ≈ 17 comparisons instead of up to 144,000.

**Impact:** Threshold-existence queries on the daily capacity matrix went from full-table scans to sub-millisecond lookups. This enabled interactive capacity dashboards — analysts could ask "did any server hit 90% CPU at any hour yesterday?" and get an answer in real time.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Implement the STAIRCASE search for a matrix
# where rows are sorted but the inter-row property does NOT hold.
# Start at top-right. If target < current, go left. If target > current, go down.
# -------------------------------------------------------

def searchMatrixII(matrix, target):
    # Your solution here
    pass


# Test
print(searchMatrixII([[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], 5))    # Expected: True
print(searchMatrixII([[1,4,7,11],[2,5,8,12],[3,6,9,16],[10,13,14,17]], 20))   # Expected: False
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Binary Search on Flattened Index** — Treat a 2D matrix as a 1D sorted array; translate indices at access time

### When to Use It
- ✅ Matrix where each row is sorted AND row[i][0] > row[i-1][-1] (contiguous sorted)
- ✅ Need O(log(m×n)) instead of O(m×n)
- ❌ **Don't use when:** Matrix is sorted within rows but not between rows — use staircase search instead

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (nested loop) | $O(m \times n)$ | $O(1)$ |
| Optimal (Binary Search on 1D) | $O(\log(m \times n))$ | $O(1)$ |

### Interview Confidence Checklist
- [ ] Can explain why this matrix enables 1D binary search
- [ ] Can write the index translation formula from memory
- [ ] Can explain the staircase alternative and when to use it
- [ ] Can state time and space complexity with justification
- [ ] Can connect to the Citi capacity matrix use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master 2D Binary Search and you've mastered a key insight: structure is just a display format. The algorithm operates on the underlying data. 🚀
```

---

### LC #153 — Find Minimum in Rotated Sorted Array [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\lc-0153-find-minimum-rotated.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day4\lc-0153-find-minimum-rotated.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 153: Find Minimum in Rotated Sorted Array
---

<div style="padding: 15px; border-left: 8px solid #FF5722; background-color: #fbe9e7; color: #bf360c; border-radius: 4px;">
    <strong>The Core Insight:</strong> A rotated sorted array has exactly ONE inflection point — the pivot where the array "wraps." Everything left of the pivot is larger than everything right of it. Binary search finds this inflection point by comparing mid to the right boundary.
</div>

### 🛠️ The Mathematical Model

The array `[4,5,6,7,0,1,2]` has two sorted halves: `[4,5,6,7]` and `[0,1,2]`. The minimum is always at the start of the second (smaller) half. We eliminate the larger half each step.

$$\text{If } nums[mid] > nums[right]: \text{ minimum is in } [mid+1, right]$$
$$\text{If } nums[mid] \leq nums[right]: \text{ minimum is in } [left, mid]$$

---

### 📋 Problem

Suppose an array of length n sorted in ascending order is rotated between 1 and n times. Find the minimum element. You must write an algorithm that runs in O(log n).

**Example 1:**
```
Input:  [3,4,5,1,2]
Output: 1
```

**Example 2:**
```
Input:  [4,5,6,7,0,1,2]
Output: 0
```

**Constraints:** n ∈ [1, 5000] | -5000 ≤ nums[i] ≤ 5000 | All integers are unique | Array was originally sorted then rotated 1 to n times
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Two Mountains</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"The array looks like two ascending slopes with a valley between them. The minimum is in the valley. If mid is higher than right, the valley is to the right. If mid is lower than right, the valley is here or to the left."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Compare nums[mid] to nums[right] — tells us which slope mid is on</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>The Drop Point</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"There's exactly one drop in the array — where it goes from high back to low. Find that drop and the minimum is just after it."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">nums[mid] > nums[right] means we're before the drop (in the big half). Search right. Else we're past it or at it. Search left including mid.</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Linear scan checks every element for O(n). The rotation property gives us enough information to binary search in O(log n).
</div>

## 🐢 Approach 1: Brute Force — $O(n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def findMin_brute(nums):
    """
    Brute Force: Linear scan for minimum
    Time: O(n) | Space: O(1)
    """
    return min(nums)   # Python's built-in min is O(n) linear scan


print(findMin_brute([3, 4, 5, 1, 2]))       # Expected: 1
print(findMin_brute([4, 5, 6, 7, 0, 1, 2])) # Expected: 0
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n)$ vs. $O(\log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The rotation creates a structural property we can exploit: if nums[mid] > nums[right], we know with certainty that mid is in the larger left half and the minimum must be in the right half. This lets us eliminate half the array per step.
</div>

---

## 📉 Why Brute Force Fails: The $O(n)$ Trap

Linear scan ignores the rotation structure. For any input, it checks every element.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **Minimum at end** | n comparisons | Must scan everything |
| **Already sorted (rotation=0)** | n comparisons | No early termination |

---

## 🚀 The Optimal Approach: $O(\log n)$

Compare `nums[mid]` to `nums[right]` (not to `nums[left]`):
- `nums[mid] > nums[right]` → mid is in the larger left portion → minimum is in `[mid+1, right]`
- `nums[mid] <= nums[right]` → mid is in the smaller right portion → minimum is in `[left, mid]`

### The Key Lifecycle Rule
1. **When `nums[mid] > nums[right]`:** minimum is to the right — `left = mid + 1`
2. **When `nums[mid] <= nums[right]`:** minimum is here or to the left — `right = mid`

---

## ✅ Mathematical Proof

At termination, `left == right`. At every step, we guaranteed the minimum stays in `[left, right]`:
- If mid is in the big half (nums[mid] > nums[right]), minimum is in `[mid+1, right]` — left grows
- If mid is in the small half, minimum is in `[left, mid]` — right shrinks
- Window strictly narrows: the invariant holds until `left == right` = the minimum

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Comparing to nums[right] (not nums[left]) is the key — right is always a valid reference point. Comparing to left is ambiguous when left == mid (two elements).
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Binary Search on Rotation — $O(\log n)$
---

Instead of linear scan, we use **comparison to right boundary** to determine which sorted half contains the minimum.

As we iterate:
1. Compare `nums[mid]` to `nums[right]`
2. If `nums[mid] > nums[right]`: we're in the big left half — minimum is to our right
3. If `nums[mid] <= nums[right]`: we're in the small right half (or at minimum) — minimum is here or left
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def findMin(nums):
    """
    Optimal: Binary Search comparing to right boundary
    Time: O(log n) | Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left < right:   # note: < not <= — we converge to a single element
        mid = left + (right - left) // 2

        if nums[mid] > nums[right]:
            # mid is in the larger left half — minimum is in [mid+1, right]
            left = mid + 1
        else:
            # mid is in the smaller right half — minimum is in [left, mid]
            right = mid

    return nums[left]   # left == right at convergence


print("Optimal:", findMin([3, 4, 5, 1, 2]))         # Expected: 1
print("Optimal:", findMin([4, 5, 6, 7, 0, 1, 2]))   # Expected: 0
print("Optimal:", findMin([11, 13, 15, 17]))         # Expected: 11 (no rotation)
print("Optimal:", findMin([2, 1]))                   # Expected: 1
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why compare nums[mid] to nums[right] instead of nums[left]?

**Answer:** Comparing to `nums[right]` is unambiguous. Right is always a valid fixed reference — if nums[mid] > nums[right], mid is in the big half (100% certain). Comparing to `nums[left]` is ambiguous when `left == mid` (two-element window) — mid equals left, so the comparison tells us nothing about which half contains the minimum.

---

### Q2: Why is the loop condition `left < right` instead of `left <= right`?

**Answer:** We converge on a single element (the minimum). When `left == right`, we've found it — no need to check further. Using `left <= right` with `right = mid` (not `mid - 1`) would cause an infinite loop when `left == right == mid`. The `< right` condition ensures termination.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** $O(\log n)$. Each iteration either sets `left = mid + 1` or `right = mid`. In either case, the window `[left, right]` strictly shrinks — from n to n/2 to n/4 etc. After at most log₂(n) iterations, `left == right` and we return.

---

### Q4: What if the array has duplicates (LC #154)?

**Answer:** Duplicates break the invariant. If `nums[mid] == nums[right]`, we can't tell which half the minimum is in — both halves look equal. The fix: when `nums[mid] == nums[right]`, do `right -= 1` (shrink by one, not half). This degrades worst case to O(n) for arrays like `[3,3,3,1,3]`.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Array not rotated (original sorted) — `nums[mid] <= nums[right]` always true, right shrinks to 0, returns first element correctly. (2) Two elements — mid = 0 (left), compared to right = 1. Works correctly. (3) All same elements — handled by the duplicates variant (LC #154). (4) Single element — while loop never executes, returns nums[0].
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Rotation** | Shifting a sorted array so that the last k elements move to the front — e.g., [1,2,3,4,5] rotated by 2 = [4,5,1,2,3] |
| **Pivot** | The inflection point in a rotated array where the sequence drops from high to low — the minimum is at the pivot |
| **Right Boundary** | `nums[right]` — the reference point used in the comparison; always in the smaller right half |
| **Convergence** | The condition `left == right` — the loop terminates with left pointing at the minimum |
| **Monotonic Binary Search** | Using binary search on any condition that is monotonically True/False, not just sorted arrays |
| **Left Half** | The larger portion of a rotated array — elements from the original end that wrapped to the front |
| **Right Half** | The smaller portion of a rotated array — the original beginning after the wrap point |
| **Invariant** | Maintained throughout: the minimum is always within `[left, right]` |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's daily capacity data was stored as rolling 90-day windows — each day, the oldest record was "rotated out" and the newest added at the end. Occasionally, due to pipeline errors, the sorted daily index became rotated: records from a later date appeared before earlier dates.

**Scenario:** Finding the earliest valid record (minimum timestamp) in a possibly-rotated daily index without scanning all 90 entries.

**How this pattern applied:** The rotated daily index had the same structure as LC #153 — one rotation point where newer-than-expected dates appeared at the start. Binary search comparing `timestamps[mid]` to `timestamps[right]` found the rotation point (minimum timestamp) in O(log 90) ≈ 7 comparisons.

**Impact:** Data validation scripts that previously scanned the full index on each run (90 comparisons) were optimized to binary search (7 comparisons). More importantly, the pattern demonstrated in code reviews that the team understood sorted-but-rotated structures — a concept that later appeared in a production Kafka offset recovery scenario.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given a rotated sorted array WITH DUPLICATES,
# find the minimum element. (LC #154 variant)
# Hint: when nums[mid] == nums[right], you can only shrink right by 1
# -------------------------------------------------------

def findMinWithDuplicates(nums):
    # Your solution here
    pass


# Test
print(findMinWithDuplicates([1, 3, 5]))         # Expected: 1
print(findMinWithDuplicates([2, 2, 2, 0, 1]))   # Expected: 0
print(findMinWithDuplicates([3, 1, 3, 3, 3]))   # Expected: 1
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Binary Search on Rotation** — Compare to right boundary to determine which sorted half contains the minimum

### When to Use It
- ✅ Rotated sorted array, need minimum in O(log n)
- ✅ Array has no duplicates (or duplicates handled separately)
- ❌ **Don't use when:** Array has duplicates — use the duplicates variant with right -= 1 for equal case

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (min scan) | $O(n)$ | $O(1)$ |
| Optimal (Binary Search) | $O(\log n)$ | $O(1)$ |

### Interview Confidence Checklist
- [ ] Can explain why we compare to right (not left)
- [ ] Can explain why loop condition is `<` not `<=`
- [ ] Can write the solution from memory in 3 minutes
- [ ] Can state how duplicates change the approach
- [ ] Can connect to a real system use case (rotated timestamp index)
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Rotated Binary Search and you've learned to see structure in apparent disorder. 🚀
```

---

### LC #33 — Search in Rotated Sorted Array [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\lc-0033-search-rotated.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day4\lc-0033-search-rotated.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 33: Search in Rotated Sorted Array
---

<div style="padding: 15px; border-left: 8px solid #009688; background-color: #e0f2f1; color: #004d40; border-radius: 4px;">
    <strong>The Core Insight:</strong> In a rotated array, at least ONE of the two halves (left of mid or right of mid) is always fully sorted. Identify which half is sorted, check if the target falls in that range, and eliminate the other half.
</div>

### 🛠️ The Mathematical Model

At any midpoint, either the left half `[left, mid]` or the right half `[mid, right]` is guaranteed to be sorted. We check which half is sorted, then ask: "Is the target in the sorted half's range?" Binary decision at each step.

$$\text{If } nums[left] \leq nums[mid]: \text{ left half is sorted}$$
$$\text{If } nums[mid] \leq nums[right]: \text{ right half is sorted}$$

---

### 📋 Problem

Given a rotated sorted array `nums` and a `target`, return the index of `target` or `-1` if not found. Integers are distinct. Must run in O(log n).

**Example 1:**
```
Input:  nums = [4,5,6,7,0,1,2], target = 0
Output: 4
```

**Example 2:**
```
Input:  nums = [4,5,6,7,0,1,2], target = 3
Output: -1
```

**Constraints:** 1 ≤ n ≤ 5000 | -10⁴ ≤ nums[i] ≤ 10⁴ | All integers are unique | Originally sorted then rotated
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Two Sorted Segments</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"The array has two sorted halves joined at a seam. At any midpoint, one of the two sub-halves (left or right of mid) must be clean and sorted. Look at which one is clean, check if target is in it."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">One half always sorted → range check → standard elimination</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Safe Zone</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Find the 'safe zone' — the half with predictable sorted order. If target is in the safe zone, search there. If not, search the other half."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Safe zone = sorted half. Range check = is target within [safe_start, safe_end]. Eliminates the unsafe half.</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Linear scan ignores the rotation structure entirely. With 5,000 elements, brute force checks up to 5,000. Binary search on rotation: at most 13.
</div>

## 🐢 Approach 1: Brute Force — $O(n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def search_brute(nums, target):
    """
    Brute Force: Linear scan
    Time: O(n) | Space: O(1)
    """
    for i, num in enumerate(nums):
        if num == target:
            return i
    return -1


print(search_brute([4, 5, 6, 7, 0, 1, 2], 0))   # Expected: 4
print(search_brute([4, 5, 6, 7, 0, 1, 2], 3))   # Expected: -1
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n)$ vs. $O(\log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The rotation creates exactly one "break" in the sorted order. At any midpoint, exactly ONE of the two halves (left-of-mid or right-of-mid) is guaranteed to be fully sorted. We exploit this to do a range check — if target is in the sorted half's range, search it; otherwise search the other half.
</div>

---

## 📉 Why Brute Force Fails: The $O(n)$ Trap

No use of the sorted/rotation structure.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **Target at end** | n comparisons | Must scan to the end |
| **Target not present** | n comparisons | Exhausts all elements |

---

## 🚀 The Optimal Approach: $O(\log n)$

At each midpoint, determine which half is sorted (`nums[left] <= nums[mid]` → left sorted; else → right sorted). Then check if target falls in the sorted half's range. Eliminate the half that cannot contain the target.

### The Key Lifecycle Rule
1. **Check which half is sorted** — compare `nums[left]` to `nums[mid]`
2. **Range check in the sorted half** — does target fall between the endpoints?
3. **Eliminate the other half** — adjust `left` or `right` accordingly

---

## ✅ Mathematical Proof

At each step, we eliminate one half. The invariant: target, if present, is always in `[left, right]`. After log₂(n) steps, `left > right` (not found) or `nums[mid] == target` (found).

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> The key is recognizing that one half is ALWAYS sorted in a rotated array — this gives us the range check that standard binary search relies on. The rotation doesn't break binary search; it just requires one more decision per step.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Binary Search with Rotation Logic — $O(\log n)$
---

Instead of linear scan, we use **sorted-half detection** + **range check** at each step.

As we iterate:
1. Determine which half `[left, mid]` or `[mid, right]` is fully sorted
2. Check if target falls in the sorted half's numeric range
3. If yes, search that half. If no, search the other half.
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
def search(nums, target):
    """
    Optimal: Binary Search with Rotation Detection
    Time: O(log n) | Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid

        # Left half [left, mid] is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1    # target is in the sorted left half
            else:
                left = mid + 1     # target is NOT in the left half — go right
        # Right half [mid, right] is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1     # target is in the sorted right half
            else:
                right = mid - 1   # target is NOT in the right half — go left

    return -1


print("Optimal:", search([4, 5, 6, 7, 0, 1, 2], 0))    # Expected: 4
print("Optimal:", search([4, 5, 6, 7, 0, 1, 2], 3))    # Expected: -1
print("Optimal:", search([1], 0))                        # Expected: -1
print("Optimal:", search([1, 3], 3))                     # Expected: 1
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: How do you determine which half is sorted?

**Answer:** Compare `nums[left]` to `nums[mid]`. If `nums[left] <= nums[mid]`, the left half `[left, mid]` is fully sorted (no rotation occurred in this range). Otherwise, the right half `[mid, right]` is fully sorted. One of the two halves must always be sorted in a singly-rotated array.

---

### Q2: Why use `nums[left] <= nums[mid]` (≤) instead of strict <)?

**Answer:** When `left == mid` (two-element window), we need `<=` to correctly identify that the one-element left "half" is trivially sorted. Strict `<` would incorrectly classify a two-element left half as unsorted when both elements are equal (which can't happen here since all integers are unique, but the `<=` is still correct and conventional).

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** $O(\log n)$. Each iteration eliminates one half — either `left = mid + 1` or `right = mid - 1`. The window strictly shrinks by at least half each time. After at most log₂(n) iterations, we either find the target or exhaust the window.

---

### Q4: How does this differ from LC #153 (Find Minimum)?

**Answer:** LC #153 finds the minimum — we search for the pivot. LC #33 searches for a specific target — we use the sorted-half property plus a range check. Both compare `nums[mid]` to a boundary but for different purposes: #153 to find the inflection point, #33 to locate a specific value.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Array not rotated — `nums[left] <= nums[mid]` always true, behaves like standard binary search. (2) Target equals `nums[left]` or `nums[right]` — handled by `left <= right` condition, found at first or last step. (3) Two elements — mid = left, left half is one element, range check works correctly. (4) Single element — while runs once, mid = 0, first check finds it or returns -1.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Rotated Sorted Array** | A sorted array that has been "rotated" — the last k elements are moved to the front |
| **Sorted Half** | In a rotated array, at any midpoint, one of the two halves (left or right of mid) is guaranteed fully sorted |
| **Range Check** | Testing whether target falls within `[nums[left], nums[mid])` or `(nums[mid], nums[right]]` — determines which half to search |
| **Rotation Point** | The index where the sequence "drops" — everything to the left is larger than everything to the right |
| **Standard Binary Search** | The classic form on a fully sorted array — rotated binary search adds one decision (which half is sorted) |
| **Pivot** | The index of the minimum element in a rotated sorted array — the inflection point |
| **Invariant** | Maintained throughout: if target exists, it is within `[left, right]` at every iteration |
| **Elimination** | Discarding half the search space by proving target cannot be there — the core of binary search |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi ran circular log buffers for APM data — a 24-hour rolling window implemented as a circular array. The buffer was "rotated" relative to the logical time order: midnight's data might start at physical index 300, not 0.

**Scenario:** Finding whether a specific alert event (by timestamp) occurred within the circular buffer without knowing the rotation offset — equivalent to LC #33 on timestamps.

**How this pattern applied:** The circular buffer had the exact rotated-sorted-array structure. Binary search with rotation detection located any timestamp in O(log 1440) ≈ 11 comparisons instead of a linear scan of 1,440 minute-slots.

**Impact:** Real-time alert correlation — "did server X have a CPU spike in the last 24 hours?" — became a binary search operation on the circular buffer instead of a linear scan. This made the correlation check fast enough to run in the alerting hot path (< 1ms), enabling smarter alert deduplication.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Search in rotated sorted array WITH DUPLICATES (LC #81)
# Return True/False (not index). When nums[left] == nums[mid],
# you can't determine which half is sorted — shrink left by 1.
# -------------------------------------------------------

def searchWithDuplicates(nums, target):
    # Your solution here
    pass


# Test
print(searchWithDuplicates([2, 5, 6, 0, 0, 1, 2], 0))   # Expected: True
print(searchWithDuplicates([2, 5, 6, 0, 0, 1, 2], 3))   # Expected: False
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Rotated Binary Search** — At each midpoint, one half is sorted. Range-check the sorted half to eliminate the other.

### When to Use It
- ✅ Rotated sorted array (one rotation), distinct elements, O(log n) required
- ✅ Circular buffers, time-series with wrap-around
- ❌ **Don't use when:** Array has duplicates without modification (use LC #81 variant with `left++` when equal)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (linear) | $O(n)$ | $O(1)$ |
| Optimal (Rotated Binary Search) | $O(\log n)$ | $O(1)$ |

### Interview Confidence Checklist
- [ ] Can explain "one half is always sorted" invariant
- [ ] Can write the range check conditions without looking
- [ ] Can identify which comparison detects which sorted half
- [ ] Can explain the duplicates variant
- [ ] Can connect to circular buffer / time-series use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Rotated Binary Search and you understand that binary search is a mindset — find the sorted half, use its range, eliminate the other. 🚀
```

---

### LC #981 — Time Based Key-Value Store [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\lc-0981-time-based-kv.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day4\lc-0981-time-based-kv.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 981: Time Based Key-Value Store
---

<div style="padding: 15px; border-left: 8px solid #E91E63; background-color: #fce4ec; color: #880e4f; border-radius: 4px;">
    <strong>The Core Insight:</strong> Timestamps are always added in increasing order — so each key's timestamp list is automatically sorted. "Find the value at the largest timestamp ≤ query_time" is a binary search for the rightmost element ≤ a target — Python's bisect_right solves this in one line.
</div>

### 🛠️ The Mathematical Model

For each key, store `[(timestamp, value)]` sorted by timestamp (guaranteed by problem constraints). A `get(key, timestamp)` query asks: "what is the most recent value at or before this timestamp?" — binary search for the rightmost timestamp ≤ query.

$$\text{get}(key, t) = \max\{ts \leq t : (ts, v) \in store[key]\} \rightarrow v$$

---

### 📋 Problem

Design a time-based key-value data structure that stores multiple values for the same key at different timestamps and can retrieve the key's value at a certain time.

- `set(key, value, timestamp)` — stores the key-value pair at timestamp (timestamps strictly increasing per key)
- `get(key, timestamp)` — returns the value with the largest timestamp ≤ given timestamp. If none, return ""

**Example 1:**
```
Input:  set("foo","bar",1), set("foo","bar2",4)
get("foo",4) → "bar2"
get("foo",3) → "bar"
get("foo",5) → "bar2"
```

**Constraints:** 1 ≤ key.length, value.length ≤ 100 | 1 ≤ timestamp ≤ 10⁷ | All timestamps for set() calls are strictly increasing | At most 2×10⁵ calls
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Version Control</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Like Git — each commit has a timestamp. 'git checkout HEAD~3' means 'give me the state at the closest commit before this point.' We binary search commit timestamps."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Sorted timestamps per key + bisect_right gives the rightmost timestamp ≤ query</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Monitoring Snapshot</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"APM stores CPU readings every 60 seconds. Query: 'what was the CPU at 14:37?' Answer: the last reading AT or BEFORE 14:37. Binary search the timestamp list."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Sorted time-series + floor query = bisect_right minus 1</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Linear scan through timestamps for each get() call is O(n) per query. With up to 2×10⁵ calls, this scales to O(n²) total. Binary search reduces each get() to O(log n).
</div>

## 🐢 Approach 1: Brute Force — $O(n)$ per get
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
from collections import defaultdict

class TimeMap_Brute:
    """
    Brute Force: Linear scan for each get()
    set: O(1) | get: O(n) where n = number of set() calls for this key
    """
    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        best = ""
        for ts, val in self.store[key]:
            if ts <= timestamp:
                best = val   # keep overwriting — last one wins (timestamps increasing)
        return best


tm = TimeMap_Brute()
tm.set("foo", "bar", 1)
tm.set("foo", "bar2", 4)
print(tm.get("foo", 4))   # Expected: "bar2"
print(tm.get("foo", 3))   # Expected: "bar"
print(tm.get("foo", 5))   # Expected: "bar2"
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n)$ vs. $O(\log n)$ per get

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> Timestamps are always added in strictly increasing order (per the constraints). This means each key's timestamp list is automatically sorted — making it binary-searchable. The "rightmost timestamp ≤ query" is a classic floor query, solved by bisect_right.
</div>

---

## 📉 Why Brute Force Fails: The $O(n)$ Trap

Linear scan for each get() call. With 10⁵ set() and 10⁵ get() calls, worst case is 10⁵ × 10⁵ = 10¹⁰ operations.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **Many gets on one key** | O(n) per get | Scans all timestamps every time |
| **High-frequency time series** | O(n²) total | n sets × n gets = n² comparisons |

---

## 🚀 The Optimal Approach: $O(\log n)$ per get

Store `(timestamp, value)` pairs per key. Since timestamps are always increasing, the list is sorted. Use `bisect.bisect_right` to find the insertion point for `(query_timestamp, MAX_CHAR)` — everything to the left is ≤ query_timestamp. The element at `index - 1` is the answer.

### The Key Lifecycle Rule
1. **set():** append `(timestamp, value)` to `store[key]` — list stays sorted automatically
2. **get():** binary search with `bisect_right` to find rightmost ≤ query_timestamp, return value at that index

---

## ✅ Mathematical Proof

`bisect_right(pairs, (ts, chr(127)))` returns the first position where `(ts+ε, ...)` would be inserted. Everything at indices `[0, result-1]` has timestamp ≤ ts. Index `result-1` is the most recent valid entry.

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> The key insight is that the problem's constraint (strictly increasing timestamps per set() call) gives us a free sorted list. Binary search on that list gives O(log n) get() — trading nothing for a dramatic speedup.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Binary Search on Sorted Timestamps — $O(\log n)$ per get
---

Instead of linear scan, we use **Python's bisect module** to find the rightmost timestamp ≤ query.

As we iterate:
1. `set()`: append `(timestamp, value)` — list is always sorted (constraint guarantees it)
2. `get()`: `bisect_right(pairs, (timestamp, chr(127)))` finds insertion point; `index - 1` is the answer
3. If `index - 1 < 0`: no valid entry (all timestamps > query), return ""
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
from collections import defaultdict
import bisect

class TimeMap:
    """
    Optimal: Binary Search on sorted timestamp list
    set: O(1) | get: O(log n)
    """
    def __init__(self):
        self.store = defaultdict(list)   # key → [(timestamp, value), ...]

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))
        # timestamps are always increasing → list stays sorted — no sort needed

    def get(self, key, timestamp):
        if key not in self.store:
            return ""
        pairs = self.store[key]
        # bisect_right with (timestamp, chr(127)) finds the first position
        # where (timestamp+ε, anything) would go — everything left is ≤ timestamp
        idx = bisect.bisect_right(pairs, (timestamp, chr(127))) - 1
        if idx >= 0:
            return pairs[idx][1]   # return the value
        return ""   # no timestamp ≤ query exists


tm = TimeMap()
tm.set("foo", "bar", 1)
tm.set("foo", "bar2", 4)
print("Optimal:", tm.get("foo", 4))   # Expected: "bar2"
print("Optimal:", tm.get("foo", 3))   # Expected: "bar"
print("Optimal:", tm.get("foo", 5))   # Expected: "bar2"
print("Optimal:", tm.get("foo", 0))   # Expected: "" (before first timestamp)
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why is this highly relevant to data engineering?

**Answer:** Time-series lookups are everywhere in data systems — "give me the metric value at time T" or "what was the most recent configuration before this deployment?" Monitoring systems (APM tools), SLA calculations, capacity trending, audit trails — all require floor queries on timestamps. This problem is the algorithmic core of every such lookup.

---

### Q2: What is `bisect.bisect_right` and how does it work?

**Answer:** `bisect_right(array, value)` returns the rightmost index where `value` could be inserted to keep the array sorted. All elements at `[0, result-1]` are ≤ `value`. Elements at `[result, end]` are > `value`. We use `bisect_right` rather than `bisect_left` because we want all timestamps equal to the query to count as valid (≤ not <).

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** `set()` = O(1) — just an append. `get()` = O(log n) where n is the number of `set()` calls for that key — binary search on the sorted timestamp list. Overall for k operations: O(k) for set calls, O(k log k) worst case for get calls.

---

### Q4: What if timestamps in set() were NOT guaranteed to be increasing?

**Answer:** We'd need to sort the list on each `set()` call — O(n log n) per insert, making it worse than brute force for frequent writes. Or use a sorted container like `SortedList` from the `sortedcontainers` library — O(log n) insert and O(log n) search. The problem's constraint of increasing timestamps is the key gift.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Key doesn't exist — return "". (2) Query timestamp before all stored timestamps — `bisect_right` returns 0, `idx = -1 < 0`, return "". (3) Exact timestamp match — `bisect_right` puts exact matches before the insertion point for `(ts, chr(127))`, so `idx` points to the exact match correctly. (4) Multiple values at different timestamps for same key — sorted order ensures we return the most recent ≤ query.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Floor Query** | Finding the largest key ≤ a given value — the "what was the state at time T?" query pattern |
| **bisect_right** | Python stdlib: returns rightmost insertion index in a sorted array — all elements left are ≤ target |
| **bisect_left** | Returns leftmost insertion index — all elements left are < target (not ≤) |
| **Time Series** | A sequence of data points indexed in time order — the structure underlying all monitoring, metrics, APM data |
| **Append-Only** | Data structure where new entries are only added to the end — guarantees sorted order when values are monotonically increasing |
| **chr(127)** | The DEL character — used as a sentinel to ensure tuples `(ts, chr(127))` sort after all `(ts, value)` pairs with the same timestamp |
| **defaultdict** | Python dict subclass that provides a default value for missing keys — `defaultdict(list)` initializes missing keys with `[]` |
| **Sorted Container** | Data structure that maintains sorted order on insert — `SortedList` from sortedcontainers is the non-stdlib option |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's APM infrastructure stored per-server metric snapshots every 60 seconds. Post-incident analysis required "what was the CPU for server SRV-1042 at 14:37:00?" — a floor query on the sorted timestamp list for that server.

**Scenario:** The monitoring database had 6,000 servers × 1,440 minutes = 8.64 million timestamp-value pairs per day. Ad-hoc point-in-time queries for specific servers during incident investigation needed to return in under 1 second.

**How this pattern applied:** Each server's readings were stored chronologically — automatically sorted by timestamp. A binary search on the server's timestamp list (bisect_right) returned the floor value in O(log 1440) ≈ 11 comparisons. This is exactly the TimeMap.get() operation.

**Impact:** Incident triage queries that previously required a `WHERE timestamp <= '14:37' ORDER BY timestamp DESC LIMIT 1` full-table-scan on 8.64M rows ran in microseconds against the in-memory sorted structure. This was critical for the 5-minute SLA on incident reports — investigators got exact point-in-time readings instantly.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Implement a simplified version using manual
# binary search (without the bisect module).
# Find the rightmost timestamp <= query_time in the list.
# -------------------------------------------------------

from collections import defaultdict

class TimeMapManual:
    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        # Implement binary search manually — do not use bisect
        # Find the rightmost (ts, val) where ts <= timestamp
        pass


# Test
tm = TimeMapManual()
tm.set("foo", "bar", 1)
tm.set("foo", "bar2", 4)
print(tm.get("foo", 4))   # Expected: "bar2"
print(tm.get("foo", 3))   # Expected: "bar"
print(tm.get("foo", 0))   # Expected: ""
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Binary Search on Sorted Timestamps** — Exploit monotonically increasing timestamps for O(log n) floor queries

### When to Use It
- ✅ Time-series data with monotonically increasing timestamps
- ✅ "Most recent value at or before time T" queries
- ✅ Version control, audit logs, sensor readings, monitoring data
- ❌ **Don't use when:** Timestamps are not guaranteed sorted — need SortedList or sort on insert

### Complexity
| Approach | Time (get) | Space |
|----------|-----------|-------|
| Brute Force (linear) | $O(n)$ | $O(n)$ |
| Optimal (Binary Search) | $O(\log n)$ | $O(n)$ |

### Interview Confidence Checklist
- [ ] Can explain why the "increasing timestamp" constraint enables binary search
- [ ] Can explain bisect_right and the chr(127) sentinel trick
- [ ] Can write the solution from memory in 5 minutes
- [ ] Can explain floor query concept and where it appears in real systems
- [ ] Can connect to monitoring/APM use case with specific numbers
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Time-Based KV Store and you've solved the core algorithmic problem behind every monitoring and time-series system. 🚀
```

---

## B. SQL — Query Optimization

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\sql-query-optimization.ipynb`

> The SQL concept notebook uses the `_TEMPLATE-python-concept.ipynb` structure (19 cells). All content below maps to those cells. Fill `{{PLACEHOLDERS}}` with content from this blueprint.

**Core Concept Summary for notebook cells:**
- Topic: SQL Query Optimization
- Core insight: "Query optimization separates analysts from engineers. Know EXPLAIN output, why indexes matter, and how the planner decides between nested loop, hash join, and merge join."
- Why it matters: Slow queries in production cause SLA breaches. At Citi, a poorly indexed telemetry query scanned 500M rows — 45 seconds. After partition + composite index: 0.3 seconds.
- Citi angle: Citi telemetry DB — query went from 45s to 0.3s via composite index + partition pruning + covering index.
- 5 interview Q&A (pre-written in the existing study plan — use them verbatim)
- Key terms to define: Sequential Scan, Index Scan, Hash Join, Nested Loop Join, Composite Index, Covering Index, Partial Index, Partition Pruning, Cardinality, EXPLAIN ANALYZE
- The code sections are already in the existing Day 4 study plan (the SQL section starting at "EXPLAIN / EXPLAIN ANALYZE") — copy them verbatim

**Use the SQL section in the existing study plan (marked "## B. SQL — Query Optimization") for all code cells. Do not invent new code.**

---

## C. Python — NumPy & Vectorization

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\python-numpy-vectorization.ipynb`

**Use the Python section in the existing study plan (marked "## C. Python — NumPy & Vectorization") for all code cells. Do not invent new code.**

Core concept for notebook: "NumPy operations run in C. A Python loop over 1M elements takes ~seconds. NumPy does the same in milliseconds. This is the difference between a pipeline that finishes in 2 minutes vs 2 hours."

Citi narrative: Citi capacity matrix — 1000 timestamps × 6000 servers = 6M values. Python loop: 180 seconds. NumPy vectorized operations: 1.2 seconds. Impact: daily capacity analysis went from a 3-minute batch to real-time interactive query.

---

## D. Technology — APM & Observability

**Notebook file:** `D:\Workspace\StudyMaterial\Day4\apm-observability.ipynb`

**Use the Tech section in the existing study plan (marked "## D. Technology — APM & Observability") for all code cells. Do not invent new code.**

Core concept: "Observability = three pillars: metrics (what), logs (why), traces (where). OpenTelemetry unifies all three with a vendor-neutral SDK."

Citi narrative: Citi moved from CA APM to Dynatrace for auto-discovery. Problem: static threshold alerts → 70% false positives. Solution: trend-based alerting using window functions on APM data. Impact: alert volume reduced 70%, real incidents caught earlier.

---

## Behavioral Anchor — Citi Story #4 (The APM Story)

> *"At Citi I worked with CA APM (Introscope) and later AppDynamics to monitor 6,000+ endpoints. One challenge was alert fatigue — we had hundreds of threshold alerts firing daily that nobody trusted. I redesigned the alerting strategy from static thresholds to trend-based: using SQL window functions to compute rolling 7-day baselines, then alerting on deviation from trend rather than absolute value. This reduced alert volume by approximately 70% while actually catching more real incidents earlier. The key insight was that a server at 90% CPU that's been at 90% for 6 months is not an emergency — a server that jumped from 40% to 85% overnight is."*

---

## End of Day 4 — Wrap-Up

Gemini reports:
```
Day 4 Complete.
Strong: [list]
Review: [list]
Weak: [list]

Tomorrow — Day 5: Heap/Priority Queue + Analytical SQL + ETL Patterns + Capacity Planning
```
