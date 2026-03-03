---
created: 2026-03-02
updated: 2026-03-02
summary: Day 71 — Offer evaluation framework. Total compensation breakdown, role scope analysis, team quality signals.
tags: [study-plan, day-71, week-11, offer-evaluation, total-comp, negotiation]
---

# Day 71 — Offer Evaluation Framework

**Theme:** An offer is not just a number. A bad offer at a great company can still be a great career move. A great number at the wrong team can cost you 2 years. Evaluate the whole deal.

---

## Daily Maintenance (25 min)

**LC — Monotonic Stack (2 problems, timed):**
- LC #901 Stock Spanner (8 min — decreasing stack of (price, span), accumulate spans when popping)
- LC #503 Next Greater Element II (8 min — circular array, iterate 2× with `i % n`, same decreasing stack)

**SQL — Anti-join from memory:**
Write all 3 anti-join patterns (LEFT JOIN + IS NULL, NOT EXISTS, NOT IN) for: "Find all server_ids in the `servers` table that have no corresponding entry in `daily_metrics` for the last 7 days."

---

## Offer Evaluation Session (60 min)

### The 5 Dimensions of an Offer

Never evaluate an offer on base salary alone. Evaluate all 5:

---

**Dimension 1 — Total Compensation**

```
Component              Year 1      Year 2      Year 3      Year 4
────────────────────────────────────────────────────────────────
Base salary            ___         ___         ___         ___
Annual bonus (target%) ___         ___         ___         ___
Sign-on (amortized)    ___         0           0           0
Equity (vesting sched) ___         ___         ___         ___
────────────────────────────────────────────────────────────────
Total                  ___         ___         ___         ___
```

Year 1 often looks inflated (sign-on). Year 2 is the real number. Build this table for every offer.

**Ask for the full equity breakdown:**
- Total grant amount ($)
- Vesting schedule (4-year cliff/monthly/quarterly)
- Type (RSU vs options — RSUs are simpler and safer)
- For options: strike price vs current 409A valuation

**On bonus:**
- What percentage is discretionary vs guaranteed?
- What's the actual payout history? ("Target is 15%, but last year average was 9%.")
- Ask: "What's the typical payout range for someone in this role at target performance?"

---

**Dimension 2 — Role Scope**

Answer these before accepting:
- What does success look like at 6 months? At 1 year?
- Who will I be working with day-to-day? (team size, seniority mix)
- What does the IC ladder look like? What's the path to the next level?
- Is this a new role or a backfill? (Backfill = someone left — find out why)
- What's the biggest technical challenge the team is facing right now?

If the recruiter can't answer these, ask to speak with the hiring manager directly before accepting.

---

**Dimension 3 — Team Quality**

What to look for during the final round process (you've already been through it):
- Did the engineers seem engaged, curious, and proud of their work?
- Was there psychological safety in the room? (Did people disagree with each other?)
- Did you understand the technical work they described?
- Did they ask good questions or just run through a checklist?

What to ask the recruiter:
- "What's the team's tenure? How many people have been there > 2 years?"
- "What's the manager's background?"
- "What happened to the last person in this role?" (If backfill)

---

**Dimension 4 — Growth Trajectory**

- Is the company growing or cutting?
- Is the data function mature (maintain) or being built (build)?
- What does the roadmap look like? (Will you be doing meaningful work in 18 months?)
- Who does the DE team report to? (Engineering vs Finance vs Operations — affects influence)

A company with lower base but a genuine build opportunity can be worth more than a higher base at a company where DE is a cost center.

---

**Dimension 5 — Logistics**

- Remote vs hybrid vs in-office — and what's the actual expectation, not the policy?
- Location (commute cost, relocation requirement)
- Benefits: healthcare quality, 401k match rate and vesting, PTO policy
- Start date flexibility

---

### Your Offer Scorecard Template

```
Company: ___
Offer received: ___
Deadline: ___

Year 2 total comp: $___
Floor I'll accept: $___

Role scope clarity (1-5): ___
Team quality signal (1-5): ___
Growth trajectory (1-5): ___
Logistics fit (1-5): ___

Total score (max 20): ___

Would I be excited to start Monday? [ ] Yes  [ ] No  [ ] Not sure
```

---

## Day 71 Checklist

- [ ] Both LC problems solved (Stock Spanner: accumulate spans correctly)
- [ ] All 3 anti-join patterns written from memory
- [ ] Offer evaluation framework read — all 5 dimensions understood
- [ ] Offer scorecard template filled in for any active offer (or saved for when one arrives)
- [ ] "Would I be excited to start Monday?" — answered honestly for each company in pipeline
