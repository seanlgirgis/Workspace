---
created: 2026-03-02
updated: 2026-03-02
summary: Day 66 — Executive-level behavioral questions. Answering for senior stakeholder audiences with business impact and judgment.
tags: [study-plan, day-66, week-10, behavioral, executive-audience, final-round]
---

# Day 66 — Executive-Level Behavioral

**Theme:** Executive audiences don't want to hear what you did. They want to hear how you think, how you lead, and whether your judgment is trustworthy at scale.

---

## Daily Maintenance (25 min)

**LC — 1D DP sprint (2 problems, timed):**
- LC #152 Maximum Product Subarray (8 min — track both max and min at each step, swap if negative)
- LC #91 Decode Ways (8 min — `dp[i] = dp[i-1] if valid 1-char + dp[i-2] if valid 2-char`)

**SQL — Idempotency from memory:**
Write the watermark-based deduplication pattern: table with `(pipeline_id, batch_id, processed_at)` — insert only if `batch_id > MAX(batch_id)` for that pipeline.

---

## Executive Behavioral Session (60 min)

### What Changes at the Executive Level

**Junior/mid behavioral:** "Tell me about a time you solved a hard technical problem."
- Evaluates: can you do the work?

**Senior/final round behavioral:** "Tell me about a time you changed how your organization operates."
- Evaluates: can you lead at scale, without a title?

The difference is scope. Your answer must include:
1. **The org context** — who was affected, what was at stake at the business level
2. **Your judgment call** — what the trade-off was, why you chose that path
3. **The resistance** — who pushed back, how you handled it
4. **The measurable outcome** — not just "it worked," but by how much

---

### The 6 Executive Questions

Work through each. Answer out loud. 2-3 minutes per answer.

**Q1: "Tell me about a time you had to influence a decision you didn't control."**

What they're probing:
- Can you lead without authority?
- How do you build consensus when you have no mandate?
- Did you understand the political and business context, not just the technical one?

Frame your answer around: what decision was being made, who owned it, what your position was, how you built the case, what the outcome was.

**Q2: "Tell me about a time your technical recommendation was rejected. What did you do?"**

What they're probing:
- Resilience and ego management
- Do you understand that being right technically isn't always enough?
- Can you separate your identity from your ideas?

Frame: the recommendation, the rejection reason (budget, timing, risk), how you responded (did you escalate, adapt, or accept?), what you learned about stakeholder management.

**Q3: "Tell me about a time you had to make a decision with incomplete information."**

What they're probing:
- Judgment under ambiguity — this is the #1 senior signal
- Do you freeze, or do you make a call?
- Do you know how to bound your uncertainty?

Frame: the situation, what was unknown, how you assessed the risk, the decision you made, the outcome, and what you'd do differently.

**Q4: "Tell me about a time you drove a cultural or process change."**

What they're probing:
- Scale of thinking — did you change a system, not just fix a problem?
- How do you handle organizational inertia?
- Can you get people to change behavior?

Frame: what was broken, who owned the status quo, how you diagnosed root cause (not just symptoms), how you built a coalition, what changed, and how you measured it.

**Q5: "Tell me about a failure that affected more than your immediate team."**

What they're probing:
- Accountability — do you own it or deflect?
- Self-awareness — do you know what you'd do differently?
- Impact awareness — do you think about blast radius?

Frame: the failure, its scope, your role (even if partial), what you did in the moment (contain or escalate?), the aftermath, and the most important lesson.

**Q6: "Where do you think data engineering is headed in the next 3-5 years, and what are you doing to prepare?"**

What they're probing:
- Do you think beyond your current role?
- Are you a practitioner or a leader?
- Do you have genuine intellectual curiosity about the field?

Your answer should name 2-3 specific trends (e.g., declarative data pipelines, AI/ML integration in orchestration, data mesh at scale, real-time everywhere) and connect them to your own career arc.

---

### Reframing Stories for Executive Audiences

Take one of your existing behavioral stories and rewrite it with the executive lens:

**Original (technical):** "I rewrote our ETL pipeline using Spark Structured Streaming to reduce latency from 4 hours to 15 minutes."

**Executive version:** "Our trading desk was making decisions on data that was 4 hours stale. That's not a pipeline problem — that's a risk management problem. I built the case for a real-time architecture, got buy-in from the data platform lead and the risk CTO, and led the migration to streaming. Latency dropped from 4 hours to 15 minutes. The desk's market timing improved measurably — they told us directly."

The difference: **business context first**, **stakeholder coalition included**, **outcome connected to business value**.

---

## Day 66 Checklist

- [ ] Both LC problems solved (max product: track min AND max)
- [ ] Watermark deduplication SQL written from memory
- [ ] All 6 executive questions answered out loud (2-3 min each)
- [ ] One existing story rewritten with executive lens
- [ ] Answer check: org context ✓, judgment call ✓, resistance ✓, measurable outcome ✓
