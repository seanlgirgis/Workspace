---
created: 2026-03-02
updated: 2026-03-02
summary: Day 50 — Week 8 opens. Hard LC session targeting the patterns most frequently seen in senior DE interviews.
tags: [study-plan, day-50, week-8, hard-lc, senior-patterns, gap-filling]
---

# Day 50 — Hard LC Session + Architecture Review

**Theme:** Week 8 is about closing the ceiling. You're past the basics. Now you sharpen the hard stuff.

---

## Hard LC Session (60 min)

Attempt each. Set a 15-minute timer per problem. If you don't finish — that's data about your gap.

**Problem 1 — LC #23: Merge K Sorted Lists (Hard, 15 min)**
```
Input:  lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
```
Approach: min-heap of (val, list_index, node). O(N log k) where N = total nodes, k = lists.

```python
import heapq

def mergeKLists(lists):
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

**Problem 2 — LC #297: Serialize and Deserialize Binary Tree (Hard, 15 min)**
Re-solve this — from the Day 27 mock. Can you do it faster now?

**Problem 3 — LC #76: Minimum Window Substring (Hard, 15 min)**
```
Input:  s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```
Sliding window: expand right until all chars covered, shrink left while still valid.

```python
from collections import Counter

def minWindow(s, t):
    need = Counter(t)
    have = {}
    formed = 0
    required = len(need)
    left = 0
    best = (float('inf'), 0, 0)

    for right, c in enumerate(s):
        have[c] = have.get(c, 0) + 1
        if c in need and have[c] == need[c]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            lc = s[left]
            have[lc] -= 1
            if lc in need and have[lc] < need[lc]:
                formed -= 1
            left += 1

    return "" if best[0] == float('inf') else s[best[1]:best[2]+1]
```

**Problem 4 — LC #987: Vertical Order Traversal of Binary Tree (Hard, 15 min)**

BFS/DFS with (col, row) tracking. Sort by (col, row, val). Group by col.

---

## Architecture Deep Dive — Kafka at Scale (30 min)

Review and answer these questions from memory (no notes):

1. You have 10 million events/day from 6,000 servers (every 5 min = 20 events/sec). How many Kafka partitions?
   *20 events/sec is trivial. 3 partitions is fine. Design for 10x headroom: 30 partitions.*

2. A Kafka consumer group is falling behind — the lag keeps growing. What do you check?
   *Consumer processing time per message. If processing > 1/(messages/sec): bottleneck. Fix: increase consumers (up to partition count), or move heavy processing outside the poll loop (async), or increase batch size.*

3. How does Kafka guarantee ordering?
   *Ordering guaranteed within a partition only. Events with the same key (e.g., server_id) always go to the same partition → ordered per server. Across partitions: no ordering guarantee.*

4. What is the difference between `auto.offset.reset = earliest` vs `latest`?
   *`earliest`: start from the oldest available message (full replay). `latest`: start from now (skip existing messages). Use `earliest` for new consumers that need historical data; `latest` for consumers that only care about new events.*

---

## Day 50 Checklist

- [ ] LC #23 Merge K Sorted Lists coded correctly (heap approach)
- [ ] LC #297 Serialize Tree — faster than Day 27 attempt?
- [ ] LC #76 Minimum Window Substring — sliding window with Counter
- [ ] LC #987 attempted (even partial approach counts)
- [ ] All 4 Kafka questions answered verbally without notes
- [ ] Gap identified for weakest of the 4 hard problems → scheduled for next drill
