---
created: 2026-03-02
updated: 2026-03-02
summary: Day 76 — Verbal acceptance and next steps. What happens after you say yes, and how to close cleanly.
tags: [study-plan, day-76, week-11, acceptance, offer-letter, background-check]
---

# Day 76 — Verbal Acceptance + Next Steps

**Theme:** Accepting an offer is not the end. It's the start of a transition. The first 72 hours after "yes" determine whether the experience is smooth or chaotic.

---

## Daily Maintenance (25 min)

**LC — Linked List (2 problems, timed):**
- LC #206 Reverse Linked List (4 min — iterative: `prev, curr, curr.next = None, head, None; while curr: next=curr.next; curr.next=prev; prev=curr; curr=next`)
- LC #143 Reorder List (10 min — find mid (slow/fast), reverse second half, merge alternating)

**SQL — Window function recall:**
Write from memory: for each server_id, compute the running 7-day average CPU, and flag any day where that rolling average exceeds the overall server average by more than 20%. Use a CTE for the rolling avg and a second CTE for the server overall average.

---

## Acceptance + Transition Session (60 min)

### Step 1 — Verbal Acceptance Call

Don't accept via email. Call the recruiter.

> "Hi [Name], I've reviewed everything and I'm excited to accept [Company]'s offer. I'll sign the offer letter today. I just want to confirm the start date is [date] — does that still work?"

Keep it warm and brief. Express genuine excitement. Ask one logistical confirmation question.

After the call, send a brief email:

> "Thank you for the call — I'm thrilled to be joining [Company]. I'll sign the offer letter now and look forward to getting started on [date]. Please let me know if there's anything you need from me before then."

---

### Step 2 — Sign the Offer Letter

Read it before signing. Check:
- Base salary matches what was verbally agreed
- Bonus target % is written as agreed
- Equity grant amount and vesting schedule are documented
- Start date is correct
- Sign-on amount and clawback period (typically 1-2 years if you leave voluntarily)
- Any non-compete or IP assignment clauses — if anything looks unusual, ask before signing

Sign it promptly. Delay after verbal acceptance creates anxiety on the company's side.

---

### Step 3 — Decline All Other Offers

Do this the same day you accept. Call first, then email.

> "Hi [Name], I wanted to let you know personally — I've accepted another offer and am withdrawing from your process. I genuinely appreciated the time your team spent with me. [Company] is a company I respect and I hope our paths cross in the future."

Do not ghost. Do not make up a reason. "I accepted another offer" is a complete and professional explanation.

For companies where you're still early in process, an email is acceptable.

---

### Step 4 — Background Check Preparation

Most offers are contingent on a background check. It typically covers:
- Employment history (dates, titles, reason for leaving)
- Education verification
- Criminal background
- Credit check (more common in financial services)
- Professional license verification (if applicable)

**Be accurate on your resume.** If your title was "Data Engineer" and your resume says "Senior Data Engineer," that's a discrepancy. If you left a job for a reason you've been smoothing over in interviews, the background check won't change the record — but if you lied about it, that's a problem.

For financial services specifically: if you have any issues in your credit history or regulatory record (FINRA, SEC), proactively disclose them to the recruiter before the check completes. Being upfront is almost always better than being discovered.

---

### Step 5 — Notice Period Planning

Standard in the US: 2 weeks. Finance may ask for more.

What to prepare for at your current employer:
- Wrap up open projects with documentation
- Don't start anything you can't complete
- Identify handoff recipients for your responsibilities
- Stay professional — the data industry is small, and references come from everywhere

What NOT to do during notice:
- Don't trash the company or team to colleagues
- Don't share confidential information about your new role
- Don't mentally check out — your reputation for the last 2 weeks matters

---

### Week 11 Done — Transition Mind Map

```
After "yes":
────────────────────────────────────
[ ] Signed offer letter
[ ] All competing offers declined
[ ] Background check complete
[ ] Start date confirmed
[ ] Notice given at current employer
[ ] References thanked
[ ] Recruiter + hiring manager thanked
```

---

## Day 76 Checklist

- [ ] Both LC problems solved (Reorder List: find mid → reverse half → merge)
- [ ] Rolling average + flag SQL written (two CTEs + join + CASE WHEN flag)
- [ ] Verbal acceptance script read out loud
- [ ] Offer letter review checklist understood
- [ ] Decline scripts ready for every other company
- [ ] Notice period plan thought through
