---
created: 2026-03-02
updated: 2026-03-02
summary: Day 35 — Week 5 close. BFS on trees, query optimization practice, pipeline status review, and Week 6 planning.
tags: [study-plan, day-35, week-5, bfs-trees, query-optimization, weekly-review]
---

# Day 35 — BFS Trees + Query Optimization + Week 5 Close

**Theme:** Every Friday is a review day. You assess your pipeline, your weak spots, and your plan for next week before the weekend.

---

## Daily Maintenance (35 min)

**LC — BFS on Trees (3 problems, timed):**
- LC #102 Binary Tree Level Order Traversal (8 min — queue, capture level by queue size)
- LC #199 Binary Tree Right Side View (8 min — level order, take last element of each level)
- LC #513 Find Bottom Left Tree Value (7 min — level order, first element of last level)

Template (write from memory):
```python
from collections import deque
def levelOrder(root):
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):   # freeze level size
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

**SQL — Query Optimization:**
```sql
-- Take this slow query and rewrite it to be faster:
SELECT s.server_id, s.region,
       (SELECT AVG(avg_cpu) FROM daily_metrics m
        WHERE m.server_id = s.server_id
          AND m.report_date >= CURRENT_DATE - INTERVAL '7 days') AS avg_7d
FROM servers s
WHERE s.tier = 'production';

-- Problems: correlated subquery runs once per server row (N+1 problem)
-- Fix: rewrite using JOIN + GROUP BY, or window function
```

**Behavioral:** "Why do you want to leave your current role?" — speak it. Under 60 seconds. Honest but forward-looking.

---

## Week 5 Close — Pipeline Review (20 min)

Fill in honestly:

```
Applications sent this week:       ___
Total applications sent to date:   ___
Recruiter screens scheduled:       ___
Recruiter screens completed:       ___
Technical interviews scheduled:    ___
Feedback received:                 ___

Companies that have gone silent (> 7 days):
  ___  → follow up or move on?

Companies actively progressing:
  ___  → next step: ___  deadline: ___
```

**Recruiter screen tips (if you have one this week or next):**
- Have your 60-second intro rehearsed: name, background, what you built, what you're looking for
- Know your answer to "What are you looking for in terms of compensation?"
- Have 3 questions ready about the team and role
- End with: "What are the next steps in the process?"

---

## Week 6 Preview

Next week's focus: First technical screens. You will likely have your first real coding interview within 7-14 days of applying. Week 6 is about technical interview execution, not more studying.

**Week 6 daily rotation:**
- LC: Two Pointers → 1D DP → Backtracking → 2D DP → Tries → Graphs
- SQL: Date/Time → GROUPING SETS → Snowflake-specific → Delta Lake → Advanced Window
- Company focus: Snowflake-specific prep, Databricks-specific prep

---

## Day 35 Checklist

- [ ] 3 BFS Tree problems timed — level order template written from memory
- [ ] Correlated subquery rewritten as JOIN + GROUP BY and confirmed faster
- [ ] "Why leaving" answer rehearsed (< 60 sec, forward-looking)
- [ ] Week 5 pipeline review completed and logged
- [ ] Week 6 plan understood — ready to shift into interview execution mode
- [ ] Weekend plan: no grinding. Rest and one light review of your 5 behavioral stories.
