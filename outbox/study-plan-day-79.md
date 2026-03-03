---
created: 2026-03-02
updated: 2026-03-02
summary: Day 79 — First 30/60/90 day plan deep-dive. Onboarding strategy for a senior DE role in financial services.
tags: [study-plan, day-79, week-12, onboarding, 30-60-90, first-90-days]
---

# Day 79 — First 30/60/90 Day Plan

**Theme:** Senior engineers who succeed in new roles don't start by building. They start by listening. The first 30 days are about learning the right things to build.

---

## Daily Maintenance (20 min)

**LC — Graph (2 problems, timed):**
- LC #323 Number of Connected Components in an Undirected Graph (8 min — UF or DFS, count connected clusters)
- LC #261 Graph Valid Tree (8 min — n-1 edges, no cycles via UF; `if find(u) == find(v): return False`)

**SQL — Recursive CTE from memory:**
Write the infra hierarchy recursive CTE (manager → reports at any depth). Start from a given root node. Include: `node_id`, `name`, `depth`, `full_path` (string concatenation across depth). No notes.

---

## 30/60/90 Deep Dive (60 min)

### Why Most New Hires Fail in the First 90 Days

The most common failure mode for senior hires: they start building before they understand.

They ship something. It conflicts with an existing system they didn't know about. Or it solves a problem the team already solved a different way. Or it works — but it wasn't what the team actually needed.

The antidote: deliberate listening in the first 30 days.

---

### First 30 Days — Orientation

**Goal:** Understand the system before touching it.

**Technical:**
- [ ] Map the full data flow: where does data come in? Where does it land? Who consumes it?
- [ ] Read the last 6 months of architecture decision records (if they exist)
- [ ] Run the monitoring dashboards — what does "healthy" look like? What does "degraded" look like?
- [ ] Shadow on-call for at least one rotation before owning it

**Relational:**
- [ ] 1:1 with every person on your immediate team (30 min, asking questions — not talking about yourself)
- [ ] 1:1 with key stakeholders from other teams who depend on your team's data
- [ ] Coffee with your manager outside the formal context: "What does success look like for me at 90 days? At 1 year?"

**Cultural:**
- [ ] Who are the informal leaders? Who do people turn to when they're stuck?
- [ ] What's the team's relationship with the business teams they serve? (Partners vs cost center)
- [ ] What are the "sacred cows" — systems or decisions nobody questions, even if they should?

**Questions to ask on Day 1:**
- "What's the biggest pain point on this team right now?"
- "What's a project you tried that didn't work, and why?"
- "Who are the most important relationships to build outside this team?"

---

### Days 31-60 — First Contribution

**Goal:** One visible, scoped deliverable that demonstrates your value.

Characteristics of a good first project:
- High signal-to-noise ratio (teaches you a lot about the team's systems)
- Low risk (not on the critical path for an existing deadline)
- Measurable (you can say it's done, not just "improved")
- Builds relationships (requires working with at least one other person outside your team)

**Anti-patterns:**
- Don't pick the biggest problem to solve. You don't know enough yet.
- Don't refactor the thing you noticed is "wrong." First understand why it is the way it is.
- Don't propose a complete architecture change in month 2. There's context you're missing.

**What to aim for:**
- A runbook that didn't exist, now exists
- A data quality check that catches real issues
- A pipeline optimization that's measurable (latency, cost, reliability)
- A dashboard that makes the team's work visible to stakeholders

---

### Days 61-90 — Establish Your Operating Rhythm

**Goal:** Become someone the team relies on.

By Day 90, you should be able to say:
- "I own [X]. It's my responsibility. Here's its current state."
- "I've met [Y people] outside my team who depend on what we build."
- "I've shipped [Z] — it's done, measured, and the team knows about it."

**Establish your working style:**
- How do you communicate? (Written first, or verbal? Async or sync?)
- What's your on-call philosophy?
- What's your code review style? (High-signal comments, no nit-picking)

**Your 90-day status meeting with your manager:**
Request it. Don't wait for them to schedule it. Come with:
- What you've accomplished
- What you're still learning
- What you want to own next
- Any blocker or concern you want their help with

---

### Finance-Specific Onboarding Considerations

In financial services, you're also onboarding into a regulated environment:

- **Data lineage matters from Day 1.** Any pipeline you touch should have documented lineage. If it doesn't — add it.
- **Access controls are strict.** Get your access sorted in Week 1 (production read access, etc.) so you can actually do work.
- **Compliance training.** Complete it promptly. It's mandatory and ignoring it creates problems.
- **Don't push to production without understanding the deployment process.** Financial services environments often have strict change management. Ask before you deploy.

---

## Day 79 Checklist

- [ ] Both LC problems solved (Graph Valid Tree: n-1 edges + no cycle via UF)
- [ ] Recursive CTE with depth + full_path written from memory
- [ ] First 30-day checklist reviewed — which items are most important for your role?
- [ ] First contribution project criteria understood (high signal, low risk, measurable)
- [ ] Finance-specific onboarding considerations noted — data lineage, access, compliance training
- [ ] 90-day manager meeting: commit to requesting it in your first week
