---
created: 2026-03-02
updated: 2026-03-02
summary: Day 72 — Negotiation execution. Counter-offer scripts, silence as a tool, and what to say (and not say) in each exchange.
tags: [study-plan, day-72, week-11, negotiation, counter-offer, salary]
---

# Day 72 — Negotiation Execution

**Theme:** Negotiation is not confrontation. It is information exchange. You are helping the company understand what it takes to get you. Most candidates leave 10-20% on the table by not asking.

---

## Daily Maintenance (25 min)

**LC — Heap (2 problems, timed):**
- LC #215 Kth Largest Element (8 min — min-heap of size k; if heap[0] < new element, push and pop)
- LC #373 Find K Pairs with Smallest Sums (10 min — min-heap of `(a[0]+b[j], 0, j)`, push next `(a[i+1]+b[j], i+1, j)` on pop)

**SQL — Date gap detection from memory:**
Write a query that finds all `server_id` values in `daily_metrics` that have a gap of more than 1 day between consecutive `report_date` entries. Use `LAG()` to find the prior date, then filter where `report_date - prior_date > 1`.

---

## Negotiation Session (60 min)

### The Negotiation Principles

**1. Never give a number first.**
If asked for your salary expectation before receiving an offer: "I'd want to understand the full scope of the role before anchoring on a number — I'm confident we can find something that works."

**2. The first offer is not the final offer.**
Almost every company has a negotiation range built in. Accepting the first offer signals you either didn't know this or didn't care.

**3. Silence is a tool.**
After stating your counter, stop talking. Do not fill the silence. Let them respond. This is where most candidates fold and preemptively undercut themselves.

**4. Never negotiate against yourself.**
Do not say "I know this might not be possible, but..." — that phrase pre-defeats you. State what you want. Let them push back.

**5. Competing offers are leverage — use them.**
If you have another offer (or are close to one), say so. You don't have to reveal the exact number unless you want to. "I'm in process with another company and expect to have an offer by [date]."

---

### The Negotiation Conversation — Script

**When you receive the offer:**

Don't accept or reject immediately. Say:
> "Thank you — I'm genuinely excited about this role and the team. I want to review the details carefully and come back to you. Can I have until [date — 2-3 business days] to respond?"

This is always acceptable. It is never rude.

**When you're ready to counter:**

Call, don't email (if possible). Email is fine if that's how the recruiter has been communicating.

> "I've had a chance to review the offer carefully. I'm very excited about the role — the team, the technical challenges, and the fit all feel right. I do want to revisit the base. Based on my research and the competing processes I'm in, I was hoping we could get to [TARGET — typically 10-15% above offer]. Is there flexibility there?"

Then stop talking.

**If they say no immediately:**

> "I appreciate the directness. Can you help me understand what the comp band looks like for this role? Is there anything else with room — equity, sign-on, or performance review timing?"

**If they say they'll check:**

> "Of course — I appreciate it. I can hold until [deadline you established]. If it helps, [TARGET] is the number I need to feel good about saying yes."

**If there's a competing offer:**

> "I do have another offer in hand for $[X] — [Company name or just "another firm" is fine]. My strong preference is this role, which is why I'm talking to you first. If you can get to [TARGET], I'm ready to accept."

---

### What You Can Negotiate Beyond Base

If base is truly fixed, negotiate these:

| Item | What to ask |
|------|-------------|
| Sign-on bonus | "Could we include a sign-on to bridge the gap?" |
| Equity grant | "Is there room on the RSU grant size?" |
| Performance review timing | "Could my first review be at 6 months instead of 12?" |
| Start date | "I need X weeks notice — is that workable?" |
| Remote flexibility | "I'd like to confirm the remote/hybrid arrangement in writing." |
| Title | "Is there any flexibility on the title? Senior vs Staff affects my longer-term trajectory." |

---

### After Negotiation — Get It in Writing

Before verbally accepting, confirm:
- Revised total comp (base, bonus target, equity grant)
- Start date
- Any sign-on terms (clawback period is typically 1-2 years — ask)
- Remote/hybrid arrangement

Once you have it in writing, verbal acceptance is appropriate:

> "I'm excited to accept. I'll sign the offer letter today."

---

## Day 72 Checklist

- [ ] Both LC problems solved (kth largest: min-heap of size k)
- [ ] Date gap SQL written from memory (LAG + filter where gap > 1)
- [ ] Negotiation principles read — internalized (especially: silence is a tool)
- [ ] Counter-offer script read out loud — practice saying it naturally
- [ ] "Competing offer" script practiced out loud
- [ ] Non-base negotiation levers reviewed — know your list
