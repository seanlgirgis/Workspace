---
created: 2026-03-02
updated: 2026-03-02
summary: Day 86 — Team research. Learning about the people you'll be working with before Day 1.
tags: [study-plan, day-86, week-13, team-research, onboarding, relationships]
---

# Day 86 — Team Research

**Theme:** You'll spend 40+ hours a week with these people. Knowing who they are before you start is not stalking — it's preparation. It makes your first conversations richer and your ramp faster.

---

## Daily Maintenance (20 min)

**LC — Light session (1 problem, 15 min cap):**
LC #200 Number of Islands — if you haven't done it with Union-Find (only DFS/BFS before), try it now. Or just trace through it from memory to confirm you can still see the pattern.

**SQL — Recursive CTE recall:**
Write the org hierarchy CTE one more time — the classic `employees(id, name, manager_id)` pattern, top-down from CEO, with depth and full_path. This is a common final round question. Own it.

---

## Team Research Session (50 min)

### What to Research and Why

You already know the company. Now know the people.

**Your manager:**
- LinkedIn: career path, tenures, technical background vs management background
- GitHub (if public): do they write code? What kind?
- Any public talks, blog posts, conference appearances
- How long have they been at this company?

What you're trying to understand: what does this person value? How do they communicate publicly? What's their background — are they a former engineer who moved into management, or have they always been in management?

**Your immediate team:**
- LinkedIn for each person: how long at the company? Where were they before?
- Look at their tenure as a signal: a team where everyone has been there 3+ years is different from a team with high churn
- Any GitHub, blog, or conference presence

**Key stakeholders (from your onboarding docs or final round conversations):**
- Who are the downstream consumers of your team's work?
- Who did your interviewer mention specifically? ("You'll work closely with X from the risk team")
- Research them: background, tenure, likely priorities

---

### How to Use This Research

Not as small talk ammunition ("I saw on your LinkedIn that you...") — that's awkward.

As context for better questions:
- If your manager has a background in streaming: you know to ask informed questions about the streaming layer
- If a teammate recently joined from a competitor: there's probably a reason they switched. What are they building?
- If your team has high tenure: stability, but also potentially some calcification. Worth understanding what's been tried before you arrived.

---

### Building Your "People Map"

Create a simple document — doesn't need to be formal:

```
My Team
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name         Role              Tenure   Background note
________     _____________     ______   _______________
________     _____________     ______   _______________
________     _____________     ______   _______________

Manager
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name:       ___
Background: ___
At company: ___
Note:       ___

Key stakeholders outside the team
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name         Team              Why they matter
________     _____________     _______________
________     _____________     _______________
```

Bring this with you (digitally) on Day 1. Refer to it as you meet people to confirm what you'd learned and update it.

---

### Preparing Your Introduction

You'll introduce yourself many times in the first week. Have a crisp version ready — 60-90 seconds:

> "I'm Sean. I'm joining the [team] as a Senior Data Engineer. I spent the last [X] years in APM — CA APM, AppDynamics, Dynatrace — which is essentially building the monitoring and capacity infrastructure for large-scale systems. I've been moving into the data engineering side of that problem, which is why I'm excited to be here. I'm still learning the specifics of your stack and am looking forward to getting oriented this week."

Key elements:
- Your name and role
- Where you came from (brief, no resume recitation)
- Why it's relevant to this role
- Signal that you're in listening mode this week

---

## Day 86 Checklist

- [ ] LC #200 traced from memory (UF or DFS/BFS — pick one, know it)
- [ ] Recursive CTE (org hierarchy with depth + full_path) written from memory
- [ ] Manager researched: career path, background, communication style noted
- [ ] Team members researched: tenure patterns noted
- [ ] People map document created (can be a simple text file)
- [ ] 60-second introduction written and practiced out loud
