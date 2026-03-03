---
created: 2026-02-28
updated: 2026-02-28
summary: Day 5 blueprint — Heap/Priority Queue | Analytical SQL (YoY, cohort, funnel) | ETL Patterns | Capacity Planning. Full notebook content pre-written. Gemini formats only.
tags: [study-plan, day-05, leetcode, sql, python, capacity-planning, blueprint]
---

# Day 5 — Heap/Priority Queue + Analytical SQL + ETL Patterns + Capacity Planning

**Theme:** The heap efficiently tracks "top K" without sorting. Analytical SQL is how interviewers test business intelligence. Capacity planning is YOUR differentiator — own it.

> **Gemini instruction:** This file is the complete notebook blueprint. Every labeled `[CELL N: ...]` block is the exact content for that notebook cell. Read a section, copy the labeled blocks into the .ipynb JSON. Do not invent, rewrite, or supplement. Format only.

---

## Spaced Repetition — Questions from Days 1–4

*Run all 8. Time each one. Mark Strong / Review / Weak.*

**From Day 1:**
1. What data structure lets you find the top K frequent elements in O(n log k) instead of O(n log n)? *(Answer: min-heap of size k — push all, pop when heap exceeds k)*
2. What is a recursive CTE and what risk does it carry? *(Answer: a CTE that references itself; risk = infinite recursion if termination condition is missing)*

**From Day 2:**
3. What is the sliding window pattern and when do you use it? *(Answer: two pointers expand/contract a window — use for contiguous subarrays/substrings with a constraint)*
4. What does LAST_VALUE return by default and why is that surprising? *(Answer: it returns the current row's value, not the last row in the partition — because the default window frame is ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)*

**From Day 3:**
5. What is the key difference between NOT IN and NOT EXISTS when NULLs are present? *(Answer: NOT IN with a NULL in the subquery returns no rows — NULL comparisons propagate as UNKNOWN; NOT EXISTS handles NULLs correctly)*
6. What does `@functools.wraps(func)` do and why does it matter? *(Answer: copies the wrapped function's metadata — name, docstring — so introspection tools show the original function, not `wrapper`)*

**From Day 4:**
7. When you binary search a rotated sorted array, how do you decide which half to search? *(Answer: check which half is sorted — if left half is sorted and target is in that range, go left; otherwise go right)*
8. What is an error budget and how do you calculate it? *(Answer: error budget = 1 - SLO. If SLO = 99.9%, error budget = 0.1% downtime allowed = ~43.8 min/month)*

---

## A. LeetCode — Heap / Priority Queue

**Pattern:** `heapq` in Python is a **min-heap**. For max-heap: negate values. For "top K largest": use a min-heap of size K — the root is always the smallest of the K largest, so you can efficiently evict when K is exceeded.

---

### LC #703 — Kth Largest Element in a Stream [Easy]

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\lc-0703-kth-largest-stream.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day5\lc-0703-kth-largest-stream.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 703: Kth Largest Element in a Stream
---

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #e3f2fd; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> A min-heap of size k maintains the k largest elements seen so far. The root — the smallest in the heap — is always the kth largest overall. When a new element arrives: push it, and if the heap exceeds size k, pop the root (evicting the smallest of the top k, which is no longer in the top k).
</div>

### 🛠️ The Mathematical Model

Maintain the invariant: heap contains exactly the k largest elements. The root is the minimum of the top k = the kth largest.

$$\text{heap root} = \min(\text{top } k \text{ elements}) = k\text{th largest element}$$

---

### 📋 Problem

Design a class that finds the kth largest element in a stream. Initialize with integer `k` and array `nums`. Implement `add(val)` which appends a value to the stream and returns the kth largest element.

**Example 1:**
```
Input:  k = 3, nums = [4, 5, 8, 2]
add(3) → 4 | add(5) → 5 | add(10) → 5 | add(9) → 8 | add(4) → 8
```

**Constraints:** 1 ≤ k ≤ 10⁴ | 0 ≤ nums.length ≤ 10⁴ | -10⁴ ≤ nums[i] ≤ 10⁴ | At most 10⁴ calls to add | It's guaranteed kth largest always exists
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Bouncer's VIP List</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Maintain a VIP list of the top k people. The person at the door of the list (the least VIP) is position k. When someone new arrives, check if they belong. If yes, add them and evict whoever is now position k+1."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">min-heap of size k — root = k-th VIP. heappush + heappop when size exceeds k</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Sliding Cutoff</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"The kth largest is a moving bar. New values above the bar replace the bar. Values below the bar are irrelevant. The min-heap's root IS the bar."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Heap root tracks the current cutoff. Elements below it are outside the top k.</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Sorting the entire list after each add() is O(n log n) per call. With 10,000 add() calls, total work is O(n² log n). Min-heap of size k makes each add() O(log k) — far better.
</div>

## 🐢 Approach 1: Brute Force — $O(n \log n)$ per add
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
class KthLargest_Brute:
    """
    Brute Force: Sort entire list after each add()
    Time: O(n log n) per add | Space: O(n)
    """
    def __init__(self, k, nums):
        self.k = k
        self.nums = nums

    def add(self, val):
        self.nums.append(val)
        self.nums.sort(reverse=True)
        return self.nums[self.k - 1]


kl = KthLargest_Brute(3, [4, 5, 8, 2])
print(kl.add(3))    # Expected: 4
print(kl.add(5))    # Expected: 5
print(kl.add(10))   # Expected: 5
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n \log n)$ vs. $O(\log k)$ per add

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> We don't need to know all n elements in sorted order — we only need the k largest. A min-heap of fixed size k maintains exactly this. Push: O(log k). Pop: O(log k). The heap size never grows beyond k, so each add() is O(log k) regardless of how many total elements have been seen.
</div>

---

## 📉 Why Brute Force Fails: The $O(n \log n)$ Trap

Sort + index after each add() re-sorts the growing list. After m add() calls on initial n elements, total work is O((n+m) log(n+m)) per call.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **10,000 add() calls** | O(n² log n) total | Each add re-sorts the full list |
| **Streaming data** | Unbounded cost | Sort cost grows with stream length |

---

## 🚀 The Optimal Approach: $O(\log k)$ per add

Keep a min-heap of exactly k elements. Push the new value, then pop if size > k. The root is always the kth largest.

### The Key Lifecycle Rule
1. **Push new element** onto the heap — O(log k)
2. **If heap size > k:** pop the root (smallest element, no longer in top k) — O(log k)
3. **Root is the answer** — O(1)

---

## ✅ Mathematical Proof

The heap invariant: heap contains the k largest elements seen. When we push a new element:
- If new > root: new displaces root in top k, root is evicted
- If new ≤ root: new is below the kth largest, immediately evicted
After each add, heap contains the k largest, root = kth largest. ✓

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> By fixing the heap size at k, we get O(log k) operations — independent of total stream length. The heap size is a constant; only the heap structure changes.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Min-Heap of Size k — $O(\log k)$ per add
---

Instead of sorting on each add, we **maintain a fixed-size min-heap** where the root is always the kth largest.

As we iterate:
1. heappush(heap, val) — add the new element
2. If len(heap) > k: heappop(heap) — evict the smallest (it's no longer top k)
3. heap[0] is the kth largest
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
import heapq

class KthLargest:
    """
    Optimal: Min-Heap of size k
    __init__: O(n log k) | add: O(log k) | Space: O(k)
    """
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []
        for num in nums:
            self.add(num)   # reuse add() logic to build heap correctly

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)   # evict the smallest of the top k+1
        return self.heap[0]            # root = kth largest


kl = KthLargest(3, [4, 5, 8, 2])
print("Optimal:", kl.add(3))    # Expected: 4
print("Optimal:", kl.add(5))    # Expected: 5
print("Optimal:", kl.add(10))   # Expected: 5
print("Optimal:", kl.add(9))    # Expected: 8
print("Optimal:", kl.add(4))    # Expected: 8
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why a min-heap instead of a max-heap for "kth largest"?

**Answer:** The root of a min-heap of size k is the smallest of the k largest elements — which is the kth largest overall. A max-heap would give us the largest element as root, which isn't directly the kth largest without knowing k's position. The min-heap of size k IS the top-k filter: everything below root isn't in the top k.

---

### Q2: What if k equals 1 — what does the heap become?

**Answer:** A heap of size 1 — always holds the single maximum element. `add()` returns the running maximum of the entire stream. The heap simply tracks the one largest value seen.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** `__init__`: O(n log k) — n elements, each heappush is O(log k). `add()`: O(log k) — one heappush + at most one heappop, each O(log k). Space: O(k) — the heap never exceeds k elements. If k << n, this is a massive improvement over O(n log n) sorting.

---

### Q4: How does this pattern apply to real-time leaderboards or percentile tracking?

**Answer:** Exact same structure. For a live P95 (95th percentile) response time across n = 1,000,000 requests: a min-heap of size k = 50,000 (top 5%) tracks the P95 boundary as a stream. Each new response time is pushed; if it exceeds the current P95 threshold (heap root), it enters the top 5% and evicts the old boundary. O(log 50000) ≈ 16 operations per request.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Initial nums array shorter than k — heap has fewer than k elements, add() still returns heap[0] correctly once heap size reaches k. (2) Add value smaller than all existing — heappush then immediately heappop (size > k case), root unchanged. (3) k = 1 — heap always size 1, returns running maximum. (4) All values equal — heap fills with equal values, root = that value, always returned.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Min-Heap** | A complete binary tree where each node is ≤ its children — the root is always the minimum element |
| **Max-Heap** | A complete binary tree where each node is ≥ its children — the root is always the maximum |
| **heapq** | Python's standard library heap module — implements a min-heap on a list |
| **heappush** | Add an element to the heap in O(log n) — maintains heap property |
| **heappop** | Remove and return the minimum element in O(log n) — maintains heap property |
| **Top-K Problem** | Finding the k largest (or smallest) elements from n elements — heap approach: O(n log k) |
| **Heap Invariant** | At all times, heap[0] is the minimum (min-heap) or maximum (max-heap) element |
| **Stream** | An unbounded sequence of values arriving over time — the algorithm must handle each value as it arrives |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi monitored 6,000 server endpoints for CPU utilization. Business requirement: maintain a real-time list of the Top 100 most-utilized servers at any point — updated every minute as new readings arrived.

**Scenario:** 6,000 new CPU readings arrive every minute. Sorting all 6,000 to find the top 100 takes O(6000 log 6000) ≈ 72,000 operations per minute. A min-heap of size 100 needs O(6000 × log 100) ≈ 40,000 operations — and the heap can be maintained incrementally without re-sorting from scratch.

**How this pattern applied:** KthLargest(k=100, nums=initial_readings) built the initial heap once. Each subsequent minute, 6,000 `add()` calls updated the heap — only elements entering the top 100 caused structural changes. The heap root at any point was the 100th highest CPU reading — the alerting threshold boundary.

**Impact:** Real-time top-100 server list maintained with O(n log k) cost instead of O(n log n) sort per minute. The heap root served as a dynamic alerting threshold — servers that entered the top 100 triggered investigation automatically, without a fixed static threshold that didn't adapt to fleet-wide load patterns.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Find the Kth SMALLEST element in a stream.
# Hint: use a MAX-heap of size k (negate values for max-heap in Python).
# The root of a max-heap of size k = the kth smallest.
# -------------------------------------------------------

import heapq

class KthSmallest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = []   # max-heap (negate values)
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        # Your solution here
        pass


# Test
ks = KthSmallest(3, [4, 5, 8, 2])
print(ks.add(3))    # Expected: 4
print(ks.add(1))    # Expected: 3
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Min-Heap of Size k** — Track the k largest elements in a stream; the root is always the kth largest

### When to Use It
- ✅ Streaming data, need running kth largest/smallest
- ✅ "Top K" without sorting all n elements
- ✅ Real-time leaderboards, percentile tracking, capacity monitoring
- ❌ **Don't use when:** You need all k elements sorted (heap gives unordered top k) — need heapq.nlargest()

### Complexity
| Approach | Time (per add) | Space |
|----------|---------------|-------|
| Brute Force (sort) | $O(n \log n)$ | $O(n)$ |
| Optimal (Min-Heap size k) | $O(\log k)$ | $O(k)$ |

### Interview Confidence Checklist
- [ ] Can explain why min-heap of size k gives the kth largest
- [ ] Can write the add() method from memory
- [ ] Can explain why we evict when size > k
- [ ] Can apply to percentile tracking use case with specific numbers
- [ ] Can describe the k=1 edge case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Kth Largest in a Stream and you've unlocked the pattern behind real-time leaderboards, SLO percentile monitoring, and capacity alert thresholds. 🚀
```

---

### LC #1046 — Last Stone Weight [Easy]

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\lc-1046-last-stone-weight.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day5\lc-1046-last-stone-weight.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 1046: Last Stone Weight
---

<div style="padding: 15px; border-left: 8px solid #FF9800; background-color: #fff3e0; color: #e65100; border-radius: 4px;">
    <strong>The Core Insight:</strong> Each turn requires the two heaviest stones. A max-heap gives us the two largest values in O(log n) each. Python's heapq is a min-heap — negate all values to simulate a max-heap.
</div>

### 🛠️ The Mathematical Model

At each step: pop the two maximum elements, compute difference, push back if nonzero. A max-heap (negated in Python) ensures O(log n) access to the maximum at every step.

$$\text{Total turns} \leq n-1 \quad \text{Each turn: 2 pops + at most 1 push} \Rightarrow O(n \log n)$$

---

### 📋 Problem

You have stones with positive weights. Each turn: take the two heaviest stones y ≥ x. If y == x: both destroyed. If y != x: x destroyed, y becomes y - x. Return the weight of the last remaining stone, or 0 if none.

**Example 1:**
```
Input:  stones = [2,7,4,1,8,1]
Output: 1
Explanation: 8,7→1 | 4,2→2 | 2,1→1 | 1,1→0 | Last stone: 1
```

**Constraints:** 1 ≤ stones.length ≤ 30 | 1 ≤ stones[i] ≤ 1000
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Rock Crusher</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"The machine always grabs the two heaviest rocks. It smashes them. If one survived, it goes back in the pile. Repeat until one or zero rocks remain. I need the 'two heaviest' instantly each turn."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Max-heap: root always = heaviest. Two pops = two heaviest. One conditional push.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Priority Processor</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Tasks scheduled by priority. Each round: process the top two priority tasks. The higher-priority task reduces by the lower-priority task's amount and re-queues if it has remaining work."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Same structure — priority queue / max-heap with conditional re-insert</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Sorting descending each turn is O(n log n) per turn, O(n² log n) total. Max-heap gives O(log n) per operation, O(n log n) total.
</div>

## 🐢 Approach 1: Brute Force — $O(n^2 \log n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def lastStoneWeight_brute(stones):
    """
    Brute Force: Sort descending each turn
    Time: O(n^2 log n) | Space: O(1)
    """
    stones = stones[:]   # don't mutate input
    while len(stones) > 1:
        stones.sort(reverse=True)
        heavy, light = stones[0], stones[1]
        stones = stones[2:]
        if heavy != light:
            stones.append(heavy - light)
    return stones[0] if stones else 0


print(lastStoneWeight_brute([2, 7, 4, 1, 8, 1]))   # Expected: 1
print(lastStoneWeight_brute([1]))                    # Expected: 1
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n^2 \log n)$ vs. $O(n \log n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> We repeatedly need the two largest elements. A max-heap provides the largest element as root in O(1), and extracting it takes O(log n). Two pops per turn = O(log n) per turn. Over n turns total, O(n log n). No full sort needed each turn.
</div>

---

## 📉 Why Brute Force Fails: The $O(n^2 \log n)$ Trap

Sort each turn: O(n log n) per turn × up to n turns = O(n² log n). With n = 1,000 stones: ~10 million sort operations per run.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **30 stones** | ~27,000 sort ops | Sort each of 29 turns on shrinking list |
| **Large n** | n² log n | Sort cost per turn × n turns |

---

## 🚀 The Optimal Approach: $O(n \log n)$

Build a max-heap (negate all values for Python's min-heap). Each turn: pop the two maximum values in O(log n) each. If they differ, push the difference back. Continue until ≤ 1 stone remains.

### The Key Lifecycle Rule
1. **Negate all values** to simulate max-heap with Python's min-heap
2. **Pop twice** to get the two heaviest (negated → most negative = heaviest)
3. **Push difference** (if nonzero) back as negated value

---

## ✅ Mathematical Proof

Each turn removes at least one stone (both destroyed if equal, one destroyed if different). Starting from n stones, at most n-1 turns. Each turn: O(log n) heap operations. Total: O(n log n).

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Max-heap provides O(log n) access to the maximum — no sort needed each turn. The negation trick is standard Python idiom: negate on push, negate on pop.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Max-Heap (Negated) — $O(n \log n)$
---

Instead of sorting each turn, we use a **negated min-heap** as a max-heap.

As we iterate:
1. Build the max-heap: `[-s for s in stones]`, then `heapq.heapify(heap)`
2. While len(heap) > 1: pop two heaviest (negate back), compare, push difference if nonzero
3. Return `(-heap[0]) if heap else 0`
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    """
    Optimal: Max-Heap via negation
    Time: O(n log n) | Space: O(n) for the heap
    """
    heap = [-s for s in stones]   # negate for max-heap simulation
    heapq.heapify(heap)           # O(n) — builds heap in linear time

    while len(heap) > 1:
        heavy = -heapq.heappop(heap)   # largest (negate back)
        light = -heapq.heappop(heap)   # second largest

        if heavy != light:
            heapq.heappush(heap, -(heavy - light))   # push survivor (negated)

    return -heap[0] if heap else 0


print("Optimal:", lastStoneWeight([2, 7, 4, 1, 8, 1]))   # Expected: 1
print("Optimal:", lastStoneWeight([1]))                    # Expected: 1
print("Optimal:", lastStoneWeight([2, 2]))                 # Expected: 0
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: How do you simulate a max-heap with Python's heapq?

**Answer:** Negate all values on push; negate again on pop. Python's heapq is a min-heap, so pushing `-x` means the "smallest" in the heap is `-max(original)`, i.e., the negated maximum. Popping returns the most negative value = negative of the original maximum. Negate it back to get the true maximum.

---

### Q2: What does `heapq.heapify` do and what's its time complexity?

**Answer:** `heapify` rearranges a list in-place into a valid min-heap in O(n) time — not O(n log n). It uses a bottom-up sift-down approach, starting from the middle of the array. The O(n) proof uses the fact that most elements are near leaves and need only small sift-down operations.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(n log n). `heapify` builds the initial heap in O(n). Each of at most n-1 turns does 2 pops + at most 1 push, each O(log n). Total: O(n) + O(n × log n) = O(n log n). Much better than the brute force O(n² log n).

---

### Q4: When would you use `heapreplace` instead of pop + push?

**Answer:** `heapreplace(heap, val)` is an atomic pop + push in O(log n) — more efficient than two separate operations when you know you'll always push after popping. In Last Stone Weight, we sometimes don't push (when heavy == light), so separate pop + conditional push is correct. Use `heapreplace` only when push is unconditional.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Single stone — while loop never executes, returns that stone. (2) Two equal stones — both destroyed, heap empty, return 0. (3) All stones equal — they cancel pairwise; return 0 if even count, the stone value if odd count. (4) Already sorted — heapify handles any input order.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Max-Heap** | Complete binary tree where each parent ≥ its children — root is always the maximum |
| **Negation Trick** | Simulating a max-heap with Python's min-heap by negating all values — most negative = original maximum |
| **heapify** | O(n) in-place conversion of a list to a valid heap — more efficient than n individual pushes |
| **heappop** | Extract and return the minimum (or negated maximum) in O(log n) |
| **heappush** | Insert an element maintaining heap property in O(log n) |
| **heapreplace** | Atomic pop + push in O(log n) — use when you always push after popping |
| **Priority Queue** | Abstract data structure supporting insert + extract-max/min in O(log n) — heap is the standard implementation |
| **Smash and Survive** | The problem's turn mechanic: larger stone absorbs smaller, difference survives if nonzero |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's batch job scheduler used a priority queue to manage competing ETL jobs. Jobs had priority scores (1-1000); each scheduling cycle, the two highest-priority jobs were compared — if they conflicted for a shared resource, the higher-priority job ran and its priority was reduced by the lower-priority job's score, which was then re-queued.

**Scenario:** With 50 jobs competing for limited database connections, naive scheduling (sort all 50 each cycle) ran in O(50 log 50) per cycle × many cycles = slow. A max-heap of job priorities handled each scheduling decision in O(log 50).

**How this pattern applied:** The max-heap maintained the priority order efficiently. Each scheduling round = two heappops + conditional heappush — exactly the Last Stone Weight mechanics with "job priorities" as "stone weights."

**Impact:** Scheduler overhead dropped from O(n log n) sort per cycle to O(log n) per decision. For a scheduler running hundreds of cycles per minute with 50+ competing jobs, this mattered for scheduling latency and throughput — critical for ensuring high-priority capacity analysis jobs ran before lower-priority report generation.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given a list of numbers, repeatedly replace the
# two largest numbers with their sum until one number remains.
# Return that number. (Variant: instead of difference, use sum)
# -------------------------------------------------------

import heapq

def smashAndSum(nums):
    # Your solution here — max-heap approach
    pass


# Test
print(smashAndSum([3, 1, 4, 1, 5]))   # Expected: 14 (3+1+4+1+5 — all additions)
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Max-Heap (Negated)** — Repeatedly access the maximum in O(log n) using Python's min-heap with negated values

### When to Use It
- ✅ Repeatedly need the maximum element from a changing collection
- ✅ Simulation problems where you process the largest items each turn
- ✅ Priority queues where max-priority items are processed first
- ❌ **Don't use when:** You need both min and max — use two separate heaps (median problem pattern)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (sort each turn) | $O(n^2 \log n)$ | $O(1)$ |
| Optimal (Max-Heap) | $O(n \log n)$ | $O(n)$ |

### Interview Confidence Checklist
- [ ] Can explain the negation trick for max-heap in Python
- [ ] Can explain heapify and its O(n) complexity
- [ ] Can write the solution from memory in 3 minutes
- [ ] Can explain when to use heapreplace vs separate pop + push
- [ ] Can map to job scheduler or priority processor use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Last Stone Weight and you've internalized the max-heap pattern — every "process the two largest" problem is solved the same way. 🚀
```

---

### LC #973 — K Closest Points to Origin [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\lc-0973-k-closest-points.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day5\lc-0973-k-closest-points.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 973: K Closest Points to Origin
---

<div style="padding: 15px; border-left: 8px solid #4CAF50; background-color: #e8f5e9; color: #1b5e20; border-radius: 4px;">
    <strong>The Core Insight:</strong> We need the k CLOSEST points — not all n points sorted. A max-heap of size k keeps the k closest seen so far. The root (farthest of the k closest) is our eviction threshold: any new point farther than the root gets discarded.
</div>

### 🛠️ The Mathematical Model

Euclidean distance²: `x² + y²` (skip sqrt — monotone transformation preserves ordering). Maintain a max-heap of size k on distance². Root = farthest of top k = eviction boundary.

$$d^2 = x^2 + y^2 \quad \text{(no sqrt needed — monotone, preserves ordering)}$$

---

### 📋 Problem

Given a list of points on a plane and integer k, return the k closest points to the origin (0, 0). Distance formula: Euclidean. No sorting requirement for the output.

**Example 1:**
```
Input:  points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
```

**Example 2:**
```
Input:  points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
```

**Constraints:** 1 ≤ k ≤ points.length ≤ 10⁴ | -10⁴ ≤ xi, yi ≤ 10⁴
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Shrinking Circle</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Draw a circle around the origin. Start large. As you scan each point, if it fits inside the current k-point circle, it enters. If not, it's evicted. The circle shrinks as better points arrive."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Max-heap root = current circle radius. New point closer than root → enters, root leaves.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>VIP Nearest Neighbors</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"In a store, the k closest customers get a coupon. As new customers arrive, check if they're closer than the current farthest VIP customer. If yes, they get the coupon and the farthest VIP loses it."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Max-heap of size k on distance — root is farthest VIP = eviction candidate</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Sorting all n points by distance is O(n log n). A max-heap of size k processes each point in O(log k) for a total of O(n log k) — better when k << n.
</div>

## 🐢 Approach 1: Brute Force — $O(n \log n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def kClosest_brute(points, k):
    """
    Brute Force: Sort all points by distance, take first k
    Time: O(n log n) | Space: O(n) for sort
    """
    points.sort(key=lambda p: p[0]**2 + p[1]**2)
    return points[:k]


print(kClosest_brute([[1,3],[-2,2]], 1))          # Expected: [[-2, 2]]
print(kClosest_brute([[3,3],[5,-1],[-2,4]], 2))   # Expected: [[3,3],[-2,4]]
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n \log n)$ vs. $O(n \log k)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> We don't need all n points sorted — we only need the k closest. A max-heap of size k is our filter: it keeps the k closest seen so far, with the farthest-of-the-closest as the eviction boundary. New points farther than the boundary are rejected in O(log k).
</div>

---

## 📉 Why Brute Force Fails: The $O(n \log n)$ Trap

Sort computes relative order for ALL n points. When k = 10 and n = 10,000, sorting ranks 9,990 irrelevant points.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **k = 1, n = 10,000** | O(n log n) = ~130,000 ops | Sorted all 10k points for 1 answer |
| **k << n** | Wasteful | Ranks all n when only k needed |

---

## 🚀 The Optimal Approach: $O(n \log k)$

Max-heap of size k on distance². Push new point as `(-dist², x, y)` (negated for max-heap). If heap exceeds k, heappop removes the farthest point.

### The Key Lifecycle Rule
1. **Push** `(-distance², x, y)` — negated so largest distance² becomes min-heap root
2. **If heap size > k:** heappop removes the farthest (most negative = farthest negated)
3. **Extract** all `[x, y]` from the heap at the end

---

## ✅ Mathematical Proof

n pushes, each O(log k). At most n pops (one per push when heap > k), each O(log k). Total: O(n log k). When k << n, this is significantly better than O(n log n).

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> The max-heap of size k is the "best k seen so far" filter — exactly what we need without sorting all n points.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Max-Heap of Size k — $O(n \log k)$
---

Instead of sorting all points, we use a **max-heap of size k** where root = farthest of the k closest.

As we iterate:
1. For each point, compute `dist² = x² + y²` (no sqrt — preserves ordering)
2. Push `(-dist², x, y)` — negated for max-heap simulation
3. If heap size > k: heappop removes the farthest point
4. Extract all `[x, y]` from the final heap
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
import heapq

# Option A: Manual max-heap of size k — O(n log k)
def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Optimal: Max-Heap of size k
    Time: O(n log k) | Space: O(k)
    """
    heap = []
    for x, y in points:
        dist = -(x*x + y*y)   # negate for max-heap (most distant = largest dist² = min in negated heap)
        heapq.heappush(heap, (dist, x, y))
        if len(heap) > k:
            heapq.heappop(heap)   # evict the farthest of the top k+1
    return [[x, y] for (_, x, y) in heap]


# Option B: heapq.nsmallest — cleaner, same complexity
def kClosest_v2(points, k):
    """
    Optimal (cleaner): heapq.nsmallest with key
    Time: O(n log k) | Space: O(k)
    """
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)


print("Optimal:", kClosest([[1,3],[-2,2]], 1))          # Expected: [[-2, 2]]
print("Optimal:", kClosest([[3,3],[5,-1],[-2,4]], 2))   # Expected: [[3,3],[-2,4]]
print("Cleaner:", kClosest_v2([[1,3],[-2,2]], 1))       # Expected: [[-2, 2]]
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why not compute the square root for Euclidean distance?

**Answer:** The square root function is monotone — if x² + y² < a² + b², then √(x²+y²) < √(a²+b²). This means the ordering of distances is identical whether we use d² or d. Since we only compare distances (never use the actual value), skipping sqrt saves computation and avoids floating-point precision issues.

---

### Q2: When would you use QuickSelect instead of a heap for "k closest"?

**Answer:** QuickSelect runs in O(n) average time but O(n²) worst case. Use QuickSelect when: (1) k ≈ n/2 (heap advantage shrinks since log k ≈ log n), (2) you need guaranteed O(n) average with acceptable worst case, (3) you want in-place without extra space. Use heap when: (1) k << n (log k << log n), (2) you need guaranteed O(n log k) without variance, (3) streaming data where points arrive one by one.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** O(n log k). We process each of the n points once. For each point: heappush is O(log k), and heappop (if heap > k) is O(log k). Both operations are on a heap that never exceeds k+1 elements, so O(log k) not O(log n). Total: n × O(log k) = O(n log k).

---

### Q4: What does `heapq.nsmallest` do internally?

**Answer:** For small k relative to n, `heapq.nsmallest(k, iterable, key)` uses a max-heap of size k internally — same algorithm as Option A. For large k, it falls back to sorting. Python chooses the better approach based on k vs n ratio. The manual Option A is equivalent but more explicit.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) k = n — return all points (heap ends up with all n, same as sorting). (2) k = 1 — return the single closest point; heap size 1 throughout. (3) Duplicate distances — heap handles equal distances fine, keeps k of them. (4) Points at origin (0,0) — distance = 0, always closest, always in heap.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Euclidean Distance** | d = √(x² + y²) — straight-line distance from point (x,y) to origin |
| **Distance Squared** | d² = x² + y² — same ordering as d, avoids sqrt computation |
| **Max-Heap of Size k** | Maintains the k smallest elements seen so far; the root (maximum) is the eviction boundary |
| **Negation Trick** | Simulating a max-heap by negating keys — most negative = original maximum |
| **QuickSelect** | Partial sort algorithm — O(n) average to find kth smallest without fully sorting |
| **K Nearest Neighbors** | The problem of finding the k points closest to a query — fundamental in ML, spatial indexing, recommendation systems |
| **Eviction Threshold** | The root of the max-heap of size k — any element farther than this is immediately discarded |
| **nsmallest** | heapq.nsmallest(k, iterable) — returns k smallest using a max-heap internally |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's infrastructure team maintained regional data centers with servers distributed across geographic locations. For latency optimization, new applications needed to be routed to their k nearest data center nodes — minimizing round-trip time.

**Scenario:** Given 500 data center nodes with lat/lon coordinates, find the 3 nearest nodes to each of 10,000 application deployments. Naive: sort all 500 for each deployment = 10,000 × O(500 log 500) = 45 million sort operations. Max-heap: O(500 log 3) ≈ 8,000 operations per deployment.

**How this pattern applied:** For each deployment, the max-heap of size 3 scanned all 500 nodes in O(500 log 3) ≈ 7,900 comparisons. The heap root at each step was the "farthest acceptable node" — any node farther was immediately rejected. Final heap contained exactly the 3 nearest nodes.

**Impact:** Routing computation for 10,000 deployments completed in seconds instead of minutes. More importantly, the approach was streaming-friendly: as new data center nodes came online, they could be evaluated against the current k-nearest without rerunning the full search.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Given a list of points and a query point (not origin),
# find the k closest points to the QUERY POINT (not origin).
# -------------------------------------------------------

import heapq

def kClosestToQuery(points, query, k):
    # Compute distance² from each point to query (qx, qy)
    # Use max-heap of size k
    qx, qy = query
    # Your solution here
    pass


# Test
points = [[1,3],[-2,2],[5,5],[0,0]]
print(kClosestToQuery(points, [1,1], 2))   # Expected: [[1,3],[0,0]] (or [[0,0],[1,3]])
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Max-Heap of Size k** — Filter for k smallest without sorting all n; root = current farthest-acceptable boundary

### When to Use It
- ✅ K nearest neighbors / k smallest / k closest
- ✅ k << n (heap advantage over sort is large)
- ✅ Streaming data where points arrive one by one
- ❌ **Don't use when:** k ≈ n — just sort (heap overhead isn't worth it for large k)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (sort) | $O(n \log n)$ | $O(n)$ |
| Optimal (Max-Heap size k) | $O(n \log k)$ | $O(k)$ |

### Interview Confidence Checklist
- [ ] Can explain why d² (no sqrt) is correct for comparison
- [ ] Can explain max-heap eviction boundary concept
- [ ] Can write both the manual and nsmallest versions
- [ ] Can compare to QuickSelect and state when to use each
- [ ] Can map to spatial routing use case with numbers
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master K Closest Points and you've unlocked the foundation of spatial indexing, K-nearest neighbors in ML, and network routing optimization. 🚀
```

---

### LC #215 — Kth Largest Element in an Array [Medium]

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\lc-0215-kth-largest-array.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day5\lc-0215-kth-largest-array.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 215: Kth Largest Element in an Array
---

<div style="padding: 15px; border-left: 8px solid #9C27B0; background-color: #f3e5f5; color: #4a148c; border-radius: 4px;">
    <strong>The Core Insight:</strong> Two approaches: (1) Min-heap of size k — O(n log k), guaranteed. (2) QuickSelect — O(n) average, O(n²) worst case, in-place. Know both. In interviews, start with heap (safer), then offer QuickSelect as the O(n) optimization.
</div>

### 🛠️ The Mathematical Model

kth largest = (n-k)th smallest (0-indexed). QuickSelect partially sorts the array: the pivot ends up at its final sorted position. If pivot position == target index, done. Otherwise recurse on one half.

$$\text{kth largest} = \text{element at index } (n-k) \text{ in sorted order}$$

---

### 📋 Problem

Given an integer array `nums` and integer `k`, return the kth largest element. Note: kth largest, not kth distinct largest.

**Example 1:**
```
Input:  nums = [3,2,1,5,6,4], k = 2
Output: 5
```

**Example 2:**
```
Input:  nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

**Constraints:** 1 ≤ k ≤ nums.length ≤ 10⁵ | -10⁴ ≤ nums[i] ≤ 10⁴
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Heap Filter (Safe)</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Maintain the top k seen so far — the root is always the kth largest. Scan all n elements through this k-sized filter."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Min-heap size k: push all n, evict when > k, root = kth largest. O(n log k).</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>QuickSelect (Fast)</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Each QuickSelect step places one pivot at its final sorted position. If that position is the target rank, done. We only recurse on the half that contains the target rank."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Partition + pivot placement + one-sided recursion. O(n) average.</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Full sort is O(n log n) and ignores the fact that we only need one element. Heap approach: O(n log k). QuickSelect: O(n) average.
</div>

## 🐢 Approach 1: Brute Force — $O(n \log n)$
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
def findKthLargest_brute(nums, k):
    """
    Brute Force: Full sort, index from end
    Time: O(n log n) | Space: O(1) (in-place sort)
    """
    nums.sort(reverse=True)
    return nums[k - 1]


print(findKthLargest_brute([3,2,1,5,6,4], 2))             # Expected: 5
print(findKthLargest_brute([3,2,3,1,2,4,5,5,6], 4))       # Expected: 4
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n \log n)$ vs. $O(n \log k)$ vs. $O(n)$

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> Three approaches with different tradeoffs. Sort: O(n log n), simple. Heap: O(n log k), guaranteed, streaming-friendly. QuickSelect: O(n) average but O(n²) worst case — use random shuffle to prevent worst case.
</div>

---

## 📉 Why Brute Force Fails: The $O(n \log n)$ Trap

Full sort ranks all n elements when we only need one. For k = 1 (find maximum), sorting is dramatically wasteful.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **k = 1** | O(n log n) | Sort all n for one max element |
| **Already sorted** | O(n log n) | Sort still runs regardless of input |

---

## 🚀 The Optimal Approach: $O(n)$ average (QuickSelect) or $O(n \log k)$ (Heap)

**Heap approach:** Min-heap of size k — same as LC #703 pattern. `heapq.nlargest(k, nums)[-1]` is one line.

**QuickSelect:** Partition array around pivot. Pivot lands at its final sorted index. If `pivot_idx == target_idx`, return it. Otherwise recurse on the half containing target.

### The Key Lifecycle Rule (QuickSelect)
1. **Choose pivot** (random element — prevents O(n²) worst case on sorted input)
2. **Partition** — elements ≤ pivot go left, elements > pivot go right; pivot at final position
3. **Compare pivot position** to target index — recurse left or right (one half only)

---

## ✅ Mathematical Proof (Heap)

n pushes at O(log k) each = O(n log k). Since k ≤ n, log k ≤ log n. Heap approach strictly better than sort.

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> For interviews, lead with heap (O(n log k), safe, clear). Offer QuickSelect as the optimization that achieves O(n) average. Know both; code the heap from memory.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2a: Min-Heap of Size k — $O(n \log k)$
## 🚀 Approach 2b: QuickSelect — $O(n)$ average
---

Two valid optimal approaches:
- **Heap:** Guaranteed O(n log k), streaming-friendly, simpler to write
- **QuickSelect:** O(n) average, in-place O(1) space, complex to write — offer as upgrade
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
import heapq, random

# ── Approach 2a: Heap — O(n log k) ──────────────────────────────────────
def findKthLargest_heap(nums: list[int], k: int) -> int:
    """
    Optimal (Heap): Min-heap of size k
    Time: O(n log k) | Space: O(k)
    """
    return heapq.nlargest(k, nums)[-1]
    # Equivalent manual version:
    # heap = []
    # for n in nums:
    #     heapq.heappush(heap, n)
    #     if len(heap) > k: heapq.heappop(heap)
    # return heap[0]


# ── Approach 2b: QuickSelect — O(n) average ─────────────────────────────
def findKthLargest_quickselect(nums: list[int], k: int) -> int:
    """
    Optimal (QuickSelect): Partial sort
    Time: O(n) average, O(n²) worst | Space: O(1) in-place
    """
    target = len(nums) - k   # kth largest = (n-k)th smallest

    def quickselect(left, right):
        pivot = nums[right]
        p = left
        for i in range(left, right):
            if nums[i] <= pivot:
                nums[i], nums[p] = nums[p], nums[i]
                p += 1
        nums[p], nums[right] = nums[right], nums[p]  # pivot to final position

        if p == target:   return nums[p]
        elif p < target:  return quickselect(p + 1, right)
        else:             return quickselect(left, p - 1)

    random.shuffle(nums)   # prevent O(n²) worst case on sorted input
    return quickselect(0, len(nums) - 1)


print("Heap:", findKthLargest_heap([3,2,1,5,6,4], 2))              # Expected: 5
print("QS:", findKthLargest_quickselect([3,2,1,5,6,4], 2))         # Expected: 5
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: What is the worst case for QuickSelect and how do you prevent it?

**Answer:** O(n²) when the pivot is always the minimum or maximum — e.g., picking the last element as pivot on an already-sorted array means every partition is maximally unbalanced: one side has n-1 elements, the other has 0. Fix: shuffle the array randomly before starting (`random.shuffle(nums)`). This makes worst-case astronomically unlikely in practice.

---

### Q2: When would you prefer heap over QuickSelect in production?

**Answer:** (1) Streaming data — heap processes elements one at a time; QuickSelect needs all data in memory. (2) Latency-sensitive systems — QuickSelect's O(n²) worst case (even with shuffle) is unacceptable; heap guarantees O(n log k). (3) Immutable data — QuickSelect mutates the array in-place. Use heap when you can't modify the input.

---

### Q3: What is the time complexity of the optimal approach and why?

**Answer:** Heap: O(n log k). QuickSelect: O(n) average. For heap — n elements, each pushed in O(log k), total n × O(log k). For QuickSelect — each partition eliminates one side: expected T(n) = T(n/2) + O(n) = O(n) (like binary search but with O(n) work per step instead of O(1)).

---

### Q4: How does `random.shuffle` help QuickSelect avoid O(n²)?

**Answer:** Worst case O(n²) requires consistently bad pivot choices. If we randomly shuffle before starting, the probability of always picking the worst pivot is (1/n)^n — essentially zero for any reasonable n. The expected case is O(n) because each partition is expected to be roughly balanced after shuffling.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) k = 1 — find maximum. Both heap and QuickSelect handle correctly. (2) k = n — find minimum. Both handle correctly. (3) Duplicate values — QuickSelect partitions correctly (elements ≤ pivot go left). (4) All same values — QuickSelect's partition creates unbalanced splits, but random shuffle + ≤ condition handles it. Heap works fine with duplicates.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **QuickSelect** | A partial sorting algorithm based on quicksort's partition step — finds the kth smallest in O(n) average without fully sorting |
| **Partition** | Rearranging an array around a pivot so all elements ≤ pivot are left, all > pivot are right, pivot at its final sorted position |
| **Pivot** | The reference element used in partition — ends up at its final sorted index after partitioning |
| **Target Index** | `n - k` — the 0-indexed sorted position of the kth largest element |
| **In-Place** | Algorithm that uses O(1) extra space, operating on the input array itself |
| **Random Shuffle** | Randomly permuting the input before QuickSelect to prevent adversarial worst cases |
| **nlargest** | `heapq.nlargest(k, iterable)` — returns k largest elements using a min-heap of size k |
| **Deterministic** | Heap-based approach is deterministic — same input always gives same runtime. QuickSelect with random shuffle is randomized. |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Capacity planning at Citi required identifying the top 10 most-utilized servers each morning from 6,000 daily readings — to prioritize for immediate investigation.

**Scenario:** Every morning at 8am, a batch job received 6,000 CPU utilization percentages and needed to return the top 10 for the daily capacity report within 30 seconds. Full sort: O(6000 log 6000) ≈ 72,000 comparisons. Min-heap of size 10: O(6000 × log 10) ≈ 20,000 comparisons.

**How this pattern applied:** `heapq.nlargest(10, daily_readings)` — Python's heapq.nlargest uses a min-heap of size k internally, matching the optimal approach exactly. The top-10 servers were identified in O(n log k) without sorting all 6,000.

**Impact:** The morning capacity triage report completed in seconds instead of minutes. More importantly, the pattern was generalizable: top 50 servers for weekly review, top 100 for monthly capacity planning — all with the same heap approach, just changing k. This became a reusable component in the capacity pipeline.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Find the kth SMALLEST element in an array.
# Use a MAX-heap of size k (negate values).
# The root of a max-heap of size k = the kth smallest.
# -------------------------------------------------------

import heapq

def findKthSmallest(nums, k):
    # Your solution here — max-heap approach (negate values)
    pass


# Test
print(findKthSmallest([3,2,1,5,6,4], 2))       # Expected: 2
print(findKthSmallest([3,2,3,1,2,4,5,5,6], 4))  # Expected: 3
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Two approaches:** Min-Heap (O(n log k), safe) vs QuickSelect (O(n) average, in-place)

### When to Use It
- ✅ Heap: streaming data, immutable input, latency-sensitive systems
- ✅ QuickSelect: mutable in-place data, O(n) performance required, randomization acceptable
- ❌ **Don't use QuickSelect when:** Guaranteed worst-case O(n log n) is required (use heap)

### Complexity
| Approach | Time | Space |
|----------|------|-------|
| Brute Force (full sort) | $O(n \log n)$ | $O(1)$ |
| Optimal (Min-Heap size k) | $O(n \log k)$ | $O(k)$ |
| Optimal (QuickSelect) | $O(n)$ average | $O(1)$ |

### Interview Confidence Checklist
- [ ] Can state when to use heap vs QuickSelect
- [ ] Can write the heap version in 2 minutes
- [ ] Can explain QuickSelect partition step clearly
- [ ] Can explain why random.shuffle prevents O(n²)
- [ ] Can connect to top-k server monitoring use case
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Kth Largest and you've mastered the heap vs QuickSelect tradeoff — a recurring design question in production systems. 🚀
```

---

### LC #295 — Find Median from Data Stream [Hard]

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\lc-0295-median-data-stream.ipynb`
**HTML file:** `D:\Workspace\StudyMaterial\Day5\lc-0295-median-data-stream.html`

---

**[CELL 1: TITLE + PROBLEM]** *(markdown)*

```
## 🏗️ LeetCode 295: Find Median from Data Stream
---

<div style="padding: 15px; border-left: 8px solid #F44336; background-color: #ffebee; color: #b71c1c; border-radius: 4px;">
    <strong>The Core Insight:</strong> Split the data in half. The lower half lives in a max-heap (we want its maximum — the lower median). The upper half lives in a min-heap (we want its minimum — the upper median). Keep the two heaps balanced in size. The median is at the boundary.
</div>

### 🛠️ The Mathematical Model

$$\text{lo} = \text{max-heap (lower half)}, \quad \text{hi} = \text{min-heap (upper half)}$$
$$\text{Invariant: } |\text{lo}| = |\text{hi}| \text{ or } |\text{lo}| = |\text{hi}| + 1$$
$$\text{Median: lo[0] if odd count; } (\text{lo}[0] + \text{hi}[0]) / 2 \text{ if even}$$

---

### 📋 Problem

Implement `MedianFinder` class:
- `addNum(int num)` — adds a number to the data structure
- `findMedian()` — returns the median of all elements so far

**Example 1:**
```
addNum(1) | addNum(2) | findMedian() → 1.5
addNum(3) | findMedian() → 2.0
```

**Constraints:** -10⁵ ≤ num ≤ 10⁵ | At most 5×10⁴ calls to addNum and findMedian | At least one element before findMedian is called
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
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Two Sorted Stacks</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"Sort all values and cut them in half. The left half faces right (you see its top = max of lower half). The right half faces left (you see its top = min of upper half). The median is between these two tops."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Max-heap lo (top = lower median), min-heap hi (top = upper median). Balance sizes. Median at boundary.</td>
    </tr>
    <tr>
        <td style="padding: 12px; border: 1px solid #ddd;"><b>Balance Scale</b></td>
        <td style="padding: 12px; border: 1px solid #ddd;">"A balance scale with two pans. Left pan = lower half, right pan = upper half. They must stay within 1 element of each other. The center weight is the median."</td>
        <td style="padding: 12px; border: 1px solid #ddd;">Size invariant: |lo| == |hi| or |lo| == |hi| + 1. Rebalance after each add.</td>
    </tr>
</table>
```

---

**[CELL 3: BRUTE FORCE HEADER]** *(markdown)*

```
---

### ⚠️ Performance Warning

<div style="padding: 10px; border: 1px solid #ffe58f; background-color: #fffbe6; border-radius: 4px;">
    <strong>Note:</strong> Sorting the entire list after each addNum() is O(n log n) per call. Two-heap approach: O(log n) per addNum(), O(1) per findMedian().
</div>

## 🐢 Approach 1: Brute Force — $O(n \log n)$ per addNum
```

---

**[CELL 4: BRUTE FORCE CODE]** *(code)*

```python
class MedianFinder_Brute:
    """
    Brute Force: Sort on every findMedian call
    addNum: O(1) | findMedian: O(n log n) | Space: O(n)
    """
    def __init__(self):
        self.nums = []

    def addNum(self, num: int) -> None:
        self.nums.append(num)

    def findMedian(self) -> float:
        self.nums.sort()
        n = len(self.nums)
        if n % 2 == 1:
            return float(self.nums[n // 2])
        else:
            return (self.nums[n // 2 - 1] + self.nums[n // 2]) / 2.0


mf = MedianFinder_Brute()
mf.addNum(1); mf.addNum(2)
print(mf.findMedian())   # Expected: 1.5
mf.addNum(3)
print(mf.findMedian())   # Expected: 2.0
```

---

**[CELL 5: COMPLEXITY ANALYSIS]** *(markdown)*

```
## 🔬 Complexity Analysis: $O(n \log n)$ vs. $O(\log n)$ per add

<div style="padding: 15px; border-left: 8px solid #2196F3; background-color: #f0f7ff; color: #0d47a1; border-radius: 4px;">
    <strong>The Core Insight:</strong> The median only depends on two values: the maximum of the lower half and the minimum of the upper half. We don't need the full sorted order. Two heaps maintain exactly these two boundary values in O(log n) per update and O(1) per query.
</div>

---

## 📉 Why Brute Force Fails: The $O(n \log n)$ Trap

Sort on each findMedian() call scales with list size. After m add() calls, findMedian() costs O(m log m) per call.

| Input Type | Brute Force Performance | Reason |
|------------|------------------------|--------|
| **50,000 calls** | O(n² log n) total | n sorts, each O(n log n) |
| **High-frequency streaming** | Unusable | Sort cost grows with stream length |

---

## 🚀 The Optimal Approach: $O(\log n)$ per addNum, $O(1)$ per findMedian

Two heaps partition the data:
- `lo`: max-heap (negated in Python) — holds the lower half
- `hi`: min-heap — holds the upper half
- Invariant: `|lo| == |hi|` (even count) or `|lo| == |hi| + 1` (odd count, lo has extra)

### The Key Lifecycle Rule
1. **Always push to lo first** (negate for max-heap)
2. **Rebalance ordering:** if lo's max > hi's min, move lo's top to hi
3. **Rebalance sizes:** if |lo| > |hi| + 1, move lo's top to hi; if |hi| > |lo|, move hi's top to lo

---

## ✅ Mathematical Proof

After every addNum(), the invariant holds: lo contains the lower ⌈n/2⌉ elements, hi contains the upper ⌊n/2⌋. Both heaps give O(1) access to their tops. findMedian() reads lo[0] (and optionally hi[0]) in O(1).

<div style="padding: 10px; border-left: 8px solid #4CAF50; background-color: #f1f8f4; color: #1b5e20; border-radius: 4px;">
    <strong>✅ Summary:</strong> Two heaps maintain the "boundary" of the sorted data. We never need the full order — just the maximum-of-lower and minimum-of-upper. That's exactly what heaps provide.
</div>
```

---

**[CELL 6: OPTIMAL HEADER]** *(markdown)*

```
## 🚀 Approach 2: Two Heaps — $O(\log n)$ per addNum, $O(1)$ per findMedian
---

Instead of full sort, we **split the data into two heaps** at the median boundary.

As we iterate:
1. Push to lo (max-heap) first — everything goes through lo
2. Rebalance ordering: ensure lo's max ≤ hi's min (move lo's top to hi if violated)
3. Rebalance sizes: ensure |lo| == |hi| or |lo| == |hi| + 1
4. findMedian(): read lo[0] if odd, average of both tops if even
```

---

**[CELL 7: OPTIMAL CODE]** *(code)*

```python
import heapq

class MedianFinder:
    """
    Optimal: Two Heaps
    addNum: O(log n) | findMedian: O(1) | Space: O(n)
    """
    def __init__(self):
        self.lo = []   # max-heap (lower half) — store negated values
        self.hi = []   # min-heap (upper half)

    def addNum(self, num: int) -> None:
        heapq.heappush(self.lo, -num)   # always push to lo first (negated)

        # Rebalance ordering: lo's max must be <= hi's min
        if self.lo and self.hi and (-self.lo[0]) > self.hi[0]:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))

        # Rebalance sizes: lo can have at most 1 more element than hi
        if len(self.lo) > len(self.hi) + 1:
            heapq.heappush(self.hi, -heapq.heappop(self.lo))
        elif len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])   # odd count — median is lo's top
        return (-self.lo[0] + self.hi[0]) / 2.0   # even count — average of both tops


mf = MedianFinder()
mf.addNum(1); mf.addNum(2)
print("Optimal:", mf.findMedian())   # Expected: 1.5
mf.addNum(3)
print("Optimal:", mf.findMedian())   # Expected: 2.0
```

---

**[CELL 8: Q&A]** *(markdown)*

```
## 🎤 5 Interview Q&A

### Q1: Why two heaps instead of a sorted list?

**Answer:** Insertion into a sorted list is O(n) — you need to find the correct position and shift elements. Heap insertion (heappush) is O(log n). For streaming data with m addNum() calls, sorted list costs O(m × n) total vs. O(m log n) with heaps. The two-heap approach is also O(1) for findMedian, while sorted list requires no extra computation at query time but pays more at insert time.

---

### Q2: Why always push to lo first, then rebalance?

**Answer:** By routing everything through lo first, we ensure every new element is evaluated against the lower half. If it turns out the element belongs in the upper half (lo's max > hi's min after insert), we move it. This "push-then-check" pattern is simpler than trying to determine the correct heap before pushing.

---

### Q3: What is the time complexity of addNum and findMedian?

**Answer:** addNum = O(log n) — at most 2-3 heap operations (heappush + heappop for rebalancing), each O(log n). findMedian = O(1) — just reads the tops of both heaps without modifying them. Space = O(n) — the two heaps together hold all n elements.

---

### Q4: Where does this pattern apply in real monitoring systems?

**Answer:** Rolling P50 (median) for SLO monitoring. You can extend to rolling P95 by changing the split ratio: lo has 5% of elements, hi has 95% — the P95 is lo's top. In Citi's APM infrastructure, rolling percentile computation over 5-minute windows on response times used this exact pattern: two heaps, rebalanced each minute as new readings arrived and old ones expired.

---

### Q5: What are the edge cases to watch for?

**Answer:** (1) Single element — lo has 1 element, hi is empty. findMedian returns lo[0]. (2) Two elements — after rebalancing, lo has 1, hi has 1. findMedian averages both tops. (3) Even vs odd count — the size check `len(lo) > len(hi)` (not >=) correctly identifies the odd-count case. (4) Negative numbers — negation for max-heap works correctly: `-(-5) = 5`, `-(-3) = 3`.
```

---

**[CELL 9: KEY TERMINOLOGY]** *(markdown)*

```
## 📚 Key Terminology

| Term | Definition |
|------|------------|
| **Median** | The middle value of a sorted dataset; for even count, average of two middle values |
| **Two-Heap Pattern** | Split data into lower/upper halves using max-heap + min-heap; median is at the boundary |
| **Lower Half** | All elements ≤ median — stored in a max-heap (lo); lo's top = lower median |
| **Upper Half** | All elements ≥ median — stored in a min-heap (hi); hi's top = upper median |
| **Size Invariant** | |lo| == |hi| or |lo| == |hi| + 1 — maintained after every addNum() |
| **Ordering Invariant** | lo's max ≤ hi's min — ensures lo contains only lower-half elements |
| **Rolling Percentile** | Extending two-heap to any percentile p: lo holds p% of elements, hi holds (1-p)% |
| **Streaming Median** | Computing the median of a sequence as elements arrive, without storing all of them sorted |
```

---

**[CELL 10: CITI NARRATIVE]** *(markdown)*

```
## 💼 The Citi Narrative

**Context:** Citi's SLO monitoring required tracking P50 (median) API response times in real time for 6,000 monitored services — updated every minute as new requests were logged.

**Scenario:** Each service received ~100 requests per minute. The naive approach: sort 100 response times each minute for each service = 6,000 × O(100 log 100) ≈ 4 million sort operations per minute. Two-heap approach: 6,000 × O(100 × log 100) for add() calls + O(1) for each findMedian() query.

**How this pattern applied:** Each service maintained its own MedianFinder instance. As response times arrived, addNum() updated the two heaps in O(log n). At each minute boundary, findMedian() returned the P50 in O(1) — feeding the SLO dashboard. The pattern extended naturally to P95 by adjusting the size ratio: lo held 5% of responses (max-heap), hi held 95% (min-heap), lo's top = P95.

**Impact:** Real-time P50 and P95 SLO monitoring across 6,000 services without batch sorting. Response time deviation alerts fired within seconds of threshold breach — compared to minute-level delays with the previous sort-based approach.
```

---

**[CELL 11: PRACTICE CODE]** *(code)*

```python
# -------------------------------------------------------
# PRACTICE: Extend MedianFinder to track the RUNNING AVERAGE
# alongside the median. Add an average() method.
# -------------------------------------------------------

import heapq

class MedianAndMeanFinder:
    def __init__(self):
        self.lo = []   # max-heap (lower half)
        self.hi = []   # min-heap (upper half)
        self.total = 0
        self.count = 0

    def addNum(self, num: int) -> None:
        # Your solution — same two-heap logic + track total and count
        pass

    def findMedian(self) -> float:
        # Your solution
        pass

    def findMean(self) -> float:
        # Return the running average
        pass


# Test
mf = MedianAndMeanFinder()
for n in [1, 2, 3, 4, 5]:
    mf.addNum(n)
print(mf.findMedian())   # Expected: 3.0
print(mf.findMean())     # Expected: 3.0
```

---

**[CELL 12: SUMMARY]** *(markdown)*

```
## 🎯 Summary: Key Takeaways

### The Pattern
**Two Heaps** — Max-heap for lower half + min-heap for upper half. Median at the boundary.

### When to Use It
- ✅ Streaming median — elements arrive one by one
- ✅ Rolling percentiles (P50, P95) — change the size ratio
- ✅ Need O(1) median query with O(log n) updates
- ❌ **Don't use when:** Batch median on static array — just sort and index

### Complexity
| Approach | addNum | findMedian | Space |
|----------|--------|------------|-------|
| Brute Force (sort) | $O(1)$ | $O(n \log n)$ | $O(n)$ |
| Optimal (Two Heaps) | $O(\log n)$ | $O(1)$ | $O(n)$ |

### Interview Confidence Checklist
- [ ] Can explain why two heaps give O(1) median access
- [ ] Can describe the size invariant and ordering invariant
- [ ] Can write the full MedianFinder from memory in 8 minutes
- [ ] Can extend to arbitrary percentiles (P95, P99)
- [ ] Can connect to SLO monitoring use case with specific numbers
```

---

**[CELL 13: CLOSING]** *(markdown)*

```
---

**"Simplicity and clarity is Gold."** — Sean's Study Mantra

Master Two-Heap Median and you've mastered the most elegant data structure trick in streaming algorithms. 🚀
```

---

## B. SQL — Analytical SQL: YoY Growth, Cohort Analysis, Funnel

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\sql-analytical.ipynb`

**Use the SQL section in the existing study plan (marked "## B. SQL — Analytical SQL: YoY Growth, Cohort Analysis, Funnel") for all code cells. Do not invent new code.**

Core concept for notebook: "Analytical SQL separates analysts from engineers. YoY, cohort, and funnel queries appear in every data engineering interview."

Citi narrative: Citi capacity planning team tracked server cohorts by provisioning quarter — "of servers provisioned in Q1 2024, how many are still active in Q4 2025?" The cohort analysis pattern was applied to server lifecycle data instead of user events. Impact: identified decommissioning backlog — 340 servers provisioned but not yet decommissioned, freeing $X in licensing costs.

---

## C. Python — ETL Patterns: argparse, Logging, Pipeline Structure

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\python-etl-patterns.ipynb`

**Use the Python section in the existing study plan (marked "## C. Python — ETL Patterns: argparse, Logging, Pipeline Structure") for all code cells. Do not invent new code.**

Citi narrative: The ETL pipeline template pattern came directly from Citi's capacity data pipeline — `--env`, `--date`, `--dry-run` flags, structured JSON logging, `sys.exit(1)` on failure for Airflow retry detection. Impact: same pipeline code ran in dev, staging, and production with zero code changes — only environment variable differed.

---

## D. Technology — Capacity Planning Methodology

**Notebook file:** `D:\Workspace\StudyMaterial\Day5\capacity-planning.ipynb`

**Use the Tech section in the existing study plan (marked "## D. Technology — Capacity Planning Methodology") for all code cells. Do not invent new code.**

Citi narrative: The Four-Step Loop is Sean's actual methodology from Citi. Baseline: 90-day CA APM data. Model: requests/sec as capacity driver. Forecast: linear extrapolation with 70% ceiling. Result: "We hit ceiling in 47 days" delivered as a Jira ticket 6 weeks before the breach — zero capacity outages in the following 12 months.

---

## Behavioral Anchor — Citi Story #5: Proactive Capacity Planning Win

> **Gemini:** At end of session, say: "Tell me about a time you prevented an outage through proactive capacity planning at Citi. Two minutes — go."

**Story framework (Sean fills in with his details):**
- **Situation:** Monitoring 6,000 endpoints, growing application portfolio
- **Task:** Build a proactive capacity alerting system — no more reactive 3am pages
- **Action:** Built trending model in Python using 90-day APM baselines; set alerts at 60% utilization on the trend line, not the current reading; automated weekly capacity reports to infrastructure teams
- **Result:** Caught 3 servers on a collision course 8 weeks before breach, provisioned before impact. Zero capacity-related outages in the following 12 months.

---

## End of Day 5 — Wrap-Up Format

```
Day 5 Scorecard
Spaced Repetition: [N/8 Strong] [N Review] [N Weak]
LeetCode: [5 problems — mark each: Strong/Review/Weak]
SQL (Analytical): [Strong/Review/Weak]
Python (ETL): [Strong/Review/Weak]
Tech (Capacity Planning): [Strong/Review/Weak]
Behavioral: [Citi Story #5 — Strong / Needs work]

Notable captures (Sean's words):
→
→
```

If 3+ items are WEAK → tell Sean: "Escalate to Claude Code — these need reinforcement."
