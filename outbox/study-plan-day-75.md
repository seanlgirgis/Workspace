---
created: 2026-03-02
updated: 2026-03-02
summary: Day 75 — Decision framework. Choosing between offers when scores are close, and making a decision you'll be at peace with.
tags: [study-plan, day-75, week-11, decision-framework, offer-decision]
---

# Day 75 — Decision Framework

**Theme:** Spreadsheets help. But the final decision is made by instinct informed by data. Today you build the framework so that when the moment comes, you're ready.

---

## Daily Maintenance (25 min)

**LC — String DP (2 problems, timed):**
- LC #1143 LCS Longest Common Subsequence (8 min — `dp[i][j] = dp[i-1][j-1]+1 if match else max(skip row, skip col)`)
- LC #583 Delete Operations for Two Strings (6 min — `min_deletes = m + n - 2 * LCS(word1, word2)`)

**SQL — Stale price detection from memory:**
Write the query: given `prices(asset_id, price_date, close_price)`, find all `asset_id` values where the most recent `price_date` is more than 1 business day before today. Use `MAX(price_date)` grouped by `asset_id`, filter where `CURRENT_DATE - max_price_date > 1`.

---

## Decision Session (60 min)

### When the Scores Are Close

If your Day 71 scorecard shows two offers within 2-3 points of each other, the spreadsheet can't decide for you. Here's what does:

**The "Monday Morning" test:**
Imagine it's Monday morning. You accepted Offer A. You're about to start. How do you feel? Now imagine you accepted Offer B. How do you feel?

This test bypasses rationalization. Your gut knows which one you want.

**The "2 Years From Now" test:**
In 2 years, looking back, which offer advanced your career more? Higher comp now is obvious. But which role builds the skills, relationships, and reputation that open the next door?

**The "Coffee with the Hiring Manager" signal:**
During your final round, did you think "I'd like to work for this person" or "I'll manage this relationship"? That's a 3-year signal. Management is the single largest determinant of whether your time at a company is growth or survival.

---

### The Regret Minimization Framework

Jeff Bezos' framework, adapted:

Imagine yourself at 80. Which decision would you regret more?
- "I turned down the higher base" — or
- "I took the higher base and spent 3 years in a stagnant team"

Most people, with distance, regret risk aversion more than risk. They don't regret the job that didn't work out. They regret not trying the thing that excited them.

---

### The Non-Negotiables Checklist

Before deciding, verify these. If any answer is "no" or "I don't know," find out before accepting.

```
[ ] I know what success looks like in the first 6 months
[ ] I've spoken to at least one person on the team (not just the recruiter)
[ ] I understand the vesting schedule and cliff date
[ ] I know the actual hybrid/remote expectation, not just the policy
[ ] I know who I report to and have met them
[ ] I've asked "what happened to the last person in this role?"
[ ] I'm not accepting out of fear of losing the offer
```

If you're missing information on any of these — ask now, before accepting. A recruiter who won't answer these questions before you sign is a signal about the culture.

---

### If You're Genuinely Torn

Do this: flip a coin. Seriously. Assign A to heads, B to tails. Flip. Notice your reaction in the moment the coin lands. Relief or disappointment — that's your answer.

If you feel relief: take the one the coin chose.
If you feel disappointment: take the other one.

Your gut has already decided. The exercise just lets you hear it.

---

### Writing Down Your Decision

When you decide, write one paragraph:

```
I'm accepting [Company] because:

The decision came down to: ___
What I'm most excited about: ___
What I'm less certain about: ___
What I'll do in the first 30 days to validate the decision: ___
```

Writing it down commits you to it and gives you a reference point when doubt creeps in later (and it will).

---

## Day 75 Checklist

- [ ] Both LC problems solved (Delete Operations: m + n - 2*LCS)
- [ ] Stale price detection SQL written from memory
- [ ] "Monday Morning" test and "2 Years From Now" test done for active offers
- [ ] Non-negotiables checklist completed for every active offer
- [ ] Any missing items identified — follow-up questions drafted
- [ ] Decision written down (or template ready for when the moment arrives)
