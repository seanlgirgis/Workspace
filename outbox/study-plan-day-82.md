---
created: 2026-03-02
updated: 2026-03-02
summary: Day 82 — Personal finance planning. Compensation change, benefits enrollment, equity management, and financial baseline.
tags: [study-plan, day-82, week-12, personal-finance, benefits, equity, compensation]
---

# Day 82 — Personal Finance Planning

**Theme:** A new job often means a significant comp change, new benefits, and new equity. Getting this right in the first 30 days prevents costly mistakes that take years to undo.

---

## Daily Maintenance (20 min)

**LC — HashMap review (2 problems, timed):**
- LC #560 Subarray Sum Equals K (8 min — prefix sum + hashmap `{0: 1}`; `count += prefix_map.get(curr_sum - k, 0)` before updating map)
- LC #49 Group Anagrams (6 min — `defaultdict(list)`, key = `tuple(sorted(word))`)

**SQL — Window function recall:**
Write from memory: for each `(desk_id, trade_date)`, compute daily P&L as the sum of `(quantity * close_price - quantity * cost_basis)`, then compute the 30-day rolling average P&L per desk using `AVG() OVER (PARTITION BY desk_id ORDER BY trade_date ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)`.

---

## Personal Finance Session (50 min)

### Benefits Enrollment

Benefits open enrollment typically happens in the first 30 days. Decisions made now are often locked for 12 months.

**Health Insurance:**
- Don't default to the lowest premium plan without comparing total cost of ownership (premium + deductible + out-of-pocket max)
- If you use healthcare regularly: the "premium" high-deductible plan may cost more total
- If you're generally healthy: HDHP + HSA is often the best financial choice (HSA contributions are triple-tax-advantaged)

**HSA (if you choose HDHP):**
- Contribute the max: $4,150 (single) / $8,300 (family) for 2026
- Invest the HSA balance if the account allows — don't let it sit in cash
- HSA is the best retirement vehicle available: pre-tax contributions, tax-free growth, tax-free withdrawals for medical expenses (and penalty-free for anything at 65)

**401(k):**
- Maximize the employer match immediately — it's free compensation
- Ideally, contribute to the IRS limit ($23,500 for 2026, or $31,000 if 50+)
- Choose funds with the lowest expense ratio — index funds (target date or total market) beat actively managed funds over time in the vast majority of cases

**Life/Disability Insurance:**
- If you have dependents, company-provided life insurance (usually 1-2x salary) may not be enough
- Disability insurance is often overlooked — if you're unable to work, long-term disability (60-70% of income) is critical

---

### Equity Management

**RSUs (Restricted Stock Units):**
- They vest over time — typically 4 years with a 1-year cliff
- When they vest, they're taxed as ordinary income (the company withholds shares for taxes automatically in most cases)
- After vesting: you own the shares. Decide promptly whether to hold or sell based on your portfolio concentration.
- **Don't hold excessive concentration in your employer's stock.** If your income AND your investments are in the same company, a bad quarter hurts you twice.

**Stock Options:**
- Know your strike price vs the current 409A valuation — if the strike price > current value, the options are underwater
- Understand your exercise window: when you leave, options typically expire in 90 days (some companies now offer longer windows — check your grant agreement)
- NSO vs ISO: tax treatment differs significantly. ISO has AMT risk on exercise. Ask your accountant.

---

### Tax Planning for a Job Change

A job change often has tax implications:

- **Sign-on bonus:** Treated as ordinary income, subject to supplemental withholding rate (22% federal). If the bonus pushes you into a higher bracket, you may owe more at tax time.
- **Clawback provision:** If you leave within the clawback window, you typically repay the gross bonus — but you've already paid taxes. Consult a tax professional before leaving early.
- **State tax change:** If you're moving states, tax treatment of equity, bonuses, and income can differ significantly.
- **ESPP:** If your new employer has an Employee Stock Purchase Plan — typically 15% discount off lower of beginning or end of period price — participate. It's almost always a good deal.

---

### Your Financial Baseline Checklist

Complete within the first 30 days:

```
Benefits:
[ ] Health insurance selected (HDHP/HSA if eligible and healthy)
[ ] 401k contribution rate set — at minimum, capture full employer match
[ ] HSA opened and funded if applicable
[ ] Beneficiaries designated on 401k, life insurance

Equity:
[ ] RSU vesting schedule documented (cliff date, quarterly vest dates)
[ ] Current stock price noted — and a diversification plan if grants are significant
[ ] Exercise window for any options understood

Cash flow:
[ ] Net paycheck calculated (after taxes, benefits, 401k)
[ ] Budget updated to reflect new income
[ ] Emergency fund still intact (3-6 months expenses)
```

---

## Day 82 Checklist

- [ ] Both LC problems solved (Subarray Sum K: prefix + hashmap, add to map AFTER checking)
- [ ] Rolling 30-day P&L SQL written from memory (ROWS BETWEEN 29 PRECEDING AND CURRENT ROW)
- [ ] Benefits checklist reviewed — health insurance, 401k, HSA decisions understood
- [ ] RSU vesting schedule documented (or ready to document on Day 1)
- [ ] Tax implications of sign-on bonus noted if applicable
- [ ] Financial baseline checklist saved for action in first 30 days
