---
created: 2026-03-02
updated: 2026-03-02
summary: Day 64 — Week 10 opens. Final round format deep-dive. What evaluators look for at senior level. LC maintenance.
tags: [study-plan, day-64, week-10, final-round, senior-evaluation, leadership]
---

# Day 64 — Final Round Format + Senior Evaluation Criteria

**Theme:** Final rounds are not harder technically. They are different. You are evaluated as a colleague, not a candidate.

---

## Daily Maintenance (30 min)

**LC — Tries + Dijkstra sprint:**
- LC #208 Implement Trie (8 min)
- LC #743 Network Delay Time — Dijkstra (10 min)

Both should be automatic by now. If either takes more than the target time, that's the gap to fix today.

**SQL — Comprehensive review query:**
```sql
-- Write a single query that uses ALL of these in one result:
-- CTE, Window function (RANK or LAG), JOIN, GROUP BY, HAVING, ORDER BY
-- Topic: "For each region, find the server with the highest avg CPU growth
--          over the last 7 days vs the prior 7 days."
```

---

## Final Round Format Guide (50 min)

### What Changes at the Final Round

At technical screens: "Can you do the job?"
At final rounds: "Do I want to work with this person every day?"

**Final round formats vary by firm but typically include:**
- Engineering leader interview (Director or VP level): System design + strategic thinking
- Peer team interview: Technical depth + collaboration signals
- Business stakeholder interview: Communication + business value
- Culture / values interview: HR-led or manager-led

### What Senior Evaluators Are Looking For

**1. Ownership without title**
They want to see that you take responsibility without being asked. In stories and design discussions: you aren't just the person who executed — you identified the problem, proposed the solution, built it, and owned the outcome.

**2. Judgment under ambiguity**
Real problems don't come with clean requirements. They listen for: "When I didn't have all the information, here's how I decided what to do."

**3. Scale of thinking**
Senior engineers think about what happens at 10x scale before building. In design discussions: "This works now, but at 10x volume I'd need to change X."

**4. Communication to non-engineers**
At VP/Director level: they are not your hands-on technical peer. Can you explain your system's value in business terms? "This pipeline saves the risk team 3 hours of manual reconciliation per day" lands better than "This uses Flink with exactly-once semantics."

**5. Self-awareness**
"Tell me about a mistake" is a final-round staple. The answer should be real, specific, and show growth. Candidates who deflect or minimize fail this question.

### Adjusting Your Answers for Final Round Audience

| Technical screen answer | Final round answer |
|------------------------|-------------------|
| "I used a min-heap to optimize to O(n log n)" | "The core optimization reduced processing time from 4 hours to 40 minutes — which meant the morning report was ready before the team arrived" |
| "Kafka gives us at-least-once delivery" | "The stream architecture means we never lose a server event even during restarts — reliability that wasn't possible before" |
| "I used DFS with memoization" | (Same — some final rounds still test coding. Know your audience.) |

---

## Final Round Behavioral Prep (20 min)

These questions are common in final rounds at senior level. Practice each out loud:

1. "How do you influence people who don't report to you?"
2. "Tell me about a time you disagreed with your manager's technical decision. What did you do?"
3. "What do you think data engineering will look like in 5 years?"
4. "How would your previous team describe your biggest weakness?"
5. "What does good data engineering culture look like to you?"

For each: concrete answer, not philosophy. Stories, not principles.

---

## Day 64 Checklist

- [ ] Trie and Dijkstra both coded at target speed
- [ ] Complex CTE + window + JOIN query written and run
- [ ] Read and internalized the 5 senior evaluation criteria
- [ ] Know how to adjust answer framing for executive audience
- [ ] All 5 final round behavioral questions answered out loud
- [ ] Any answer that felt thin → rewrite with a specific story
