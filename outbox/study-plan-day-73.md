---
created: 2026-03-02
updated: 2026-03-02
summary: Day 73 — Managing multiple offers. Exploding offers, timeline compression, and coordinating parallel processes.
tags: [study-plan, day-73, week-11, multiple-offers, exploding-offer, timeline-compression]
---

# Day 73 — Managing Multiple Offers

**Theme:** Multiple offers is the best problem to have. The candidates who manage it poorly either take the wrong offer under pressure or lose offers by stalling. Here's how to control the timeline.

---

## Daily Maintenance (25 min)

**LC — Union-Find (2 problems, timed):**
- LC #547 Number of Provinces (8 min — UF with path compression and rank; `find()` with compression, `union()` with rank)
- LC #684 Redundant Connection (8 min — process edges, union each; if `find(u) == find(v)` before union → that edge is redundant)

**SQL — GROUPING SETS from memory:**
Write a query on `daily_metrics(server_id, region, report_date, avg_cpu)` that produces:
- A row per `(region, server_id)` with average CPU
- A subtotal row per `region` (all servers in that region)
- A grand total row

Use `GROUPING SETS ((region, server_id), (region), ())`.

---

## Multiple Offers Session (60 min)

### The Fundamental Problem

You're in process at 3 companies. Company A gives you an offer with a 72-hour exploding deadline. Company B is in final round (decision next week). Company C is still in technical screen.

If you take A immediately, you might miss a better offer from B. If you stall too long, A rescinds. If you rush B, you look desperate or force a rejection.

This is a coordination problem. Here's how to solve it.

---

### Step 1 — Extend the Exploding Deadline

Exploding deadlines are usually soft. Companies rarely rescind offers at the 73rd hour if you've been communicating.

Call the recruiter at Company A:

> "I'm very excited about this offer and want to make the right decision. I'm currently in final rounds with one other company and expect to have clarity by [date 5-7 days out]. Would you be able to give me until [date] to respond? I want to be transparent rather than just accepting without thinking it through."

Most recruiters will say yes. Some will not budge — at which point you have to make a judgment call about how much you want that offer.

If they say no, ask: "What's the latest I can let you know?" — sometimes there's a day or two of flexibility even when they say the deadline is firm.

---

### Step 2 — Accelerate Company B

Call Company B's recruiter:

> "I've received an offer from another company and have a deadline of [date]. You're my first choice, and I want to make sure you have time to complete your process. Is there any way to accelerate the timeline? I'd hate for a scheduling issue to prevent us from working together."

Most companies have a fast-track mechanism for candidates who have competing offers. Use it. If they can't move faster, you have information: either they're genuinely constrained (acceptable) or you're not a priority (also information).

---

### Step 3 — Let Company C Know

Call Company C:

> "I wanted to give you an update — I've received an offer and have a decision deadline coming up. You're still a company I'm genuinely interested in. Can you give me a sense of your timeline? If it's significantly longer, I may have to make a decision before your process concludes."

This is professional transparency. It may accelerate C's process. If C is still weeks out, you may simply have to decide between A and B without C.

---

### The Prioritization Matrix

When you have to choose, rate each offer on the 5 dimensions from Day 71:

```
               Company A    Company B    Company C
Year 2 comp:   ___          ___          ___
Role scope:    ___ / 5      ___ / 5      ___ / 5
Team quality:  ___ / 5      ___ / 5      ___ / 5
Growth:        ___ / 5      ___ / 5      ___ / 5
Logistics:     ___ / 5      ___ / 5      ___ / 5
────────────────────────────────────────────────
Total:         ___ / 20     ___ / 20     ___ / 20
```

If the scores are close, go with gut. If you'd be equally happy at two companies, pick the one with the better team — that's the variable you can't fix later.

---

### What NOT to Do

- **Don't lie about competing offers.** Say you have offers in process or an offer in hand. Don't invent a company.
- **Don't ghost recruiters.** It's a small world. A "no, thank you" is always better than silence.
- **Don't accept and then renege.** Accepting and then backing out destroys your professional reputation, particularly in concentrated industries like finance.
- **Don't rush into a decision just because of social pressure.** A 72-hour deadline is real. A recruiter saying "we really need to know soon" is usually not.

---

### Declining an Offer — The Right Way

> "Thank you so much for the offer and for your patience through this process. After careful consideration, I've decided to accept a different offer that's a better fit for where I want to take my career right now. I have enormous respect for [Company] and would welcome the chance to stay in touch."

Short. Grateful. No detailed explanations. No comparisons. Leave every door open.

---

## Day 73 Checklist

- [ ] Both LC problems solved (Redundant Connection: find before union, return edge where find(u)==find(v))
- [ ] GROUPING SETS query written from memory (3-level: detail, region subtotal, grand total)
- [ ] Exploding deadline extension script read out loud
- [ ] Accelerate competing company script read out loud
- [ ] Prioritization matrix filled in for active offers (or saved for when offers arrive)
- [ ] Decline script read — know how to say no professionally
