---
created: 2026-03-02
updated: 2026-03-02
summary: Day 43 — Week 7 opens. Pre-technical interview preparation protocol. Linked Lists review. SCD MERGE SQL practice.
tags: [study-plan, day-43, week-7, linked-lists, scd-merge, pre-interview-protocol]
---

# Day 43 — Linked Lists + SCD MERGE + Pre-Technical Interview Protocol

**Theme:** Week 7 is the technical interview loop. You should have screens scheduled. Today's protocol is what you do the day before any technical interview.

---

## Daily Maintenance (35 min)

**LC — Linked Lists (3 problems, timed):**
- LC #206 Reverse Linked List (5 min — iterative: prev/curr/next dance)
- LC #21 Merge Two Sorted Lists (8 min — dummy head, compare and advance)
- LC #141 Linked List Cycle (7 min — fast/slow pointers; if they meet → cycle)

Write from memory:
```python
def reverseList(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
```

**SQL — SCD Type 2 MERGE:**
From Day 16 — rebuild the MERGE pattern from scratch:
```sql
-- Schema: server_dim(surrogate_key, server_id, tier, region, valid_from, valid_to, is_current)
-- Staging: server_staging(server_id, tier, region, snapshot_date)

-- Step 1: MERGE to expire changed rows
-- Step 2: INSERT new rows for changed servers
-- Step 3: INSERT new rows for brand-new servers (NOT MATCHED)
```
Write all three steps. No looking at Day 16.

**Behavioral:** "Tell me about your most impactful technical contribution." (This is the opener many interviewers use — have it crisp.)

---

## Pre-Technical Interview Protocol (40 min)

Use this protocol the evening before every technical interview.

### 2 Hours Before Cutoff

**Step 1 — Company-specific review (20 min):**
- Re-read your research template for this company
- Read one recent engineering blog post or press release about their data/tech
- Review the JD one more time — note any specific technology named

**Step 2 — Warm-up problems (20 min):**
Do 2 problems you know cold — not hard problems, fast problems:
- 1 Easy (confirms your rhythm is working)
- 1 Medium you've done before (confirms pattern recall)
Do NOT practice anything new the day before. Only confirmation.

**Step 3 — Story review (10 min):**
Say your 2 most relevant stories out loud (matching this company's priorities).
Say "Why this company" out loud one more time.

**Step 4 — Logistics (10 min):**
- Confirm the interview link works
- Confirm your coding environment (shared editor? HackerRank? CoderPad?)
- Know the interviewer's name(s)
- Have water nearby
- Mute phone, close unnecessary browser tabs

### Day-Of Morning (30 min before)

- No heavy studying
- Write the problem-solving framework on paper as a warm-up:
  ```
  1. Restate the problem in my own words
  2. Clarify edge cases (empty input, duplicates, negative numbers?)
  3. Brute force first (state it, then optimize)
  4. State time + space complexity before coding
  5. Code it
  6. Trace through 1 example
  7. Check edge cases
  ```
- Review your opening line: "Happy to be here. Should I jump straight into the problem, or would you like a brief intro first?"

### During the Interview

- If stuck after 3 min: "I'm going to think through this out loud..."
- If you don't know the optimal: "My brute force is O(n²). I'm going to start here and optimize."
- If you make a mistake: "Let me step back — I think there's an issue with this line."
- Never go silent for more than 30 seconds without narrating

---

## Day 43 Checklist

- [ ] All 3 Linked List problems coded — reverse list written from memory
- [ ] SCD MERGE written in 3 steps from scratch
- [ ] "Most impactful contribution" answered — specific, quantified
- [ ] Pre-interview protocol reviewed and ready to execute for next interview
- [ ] Coding environment tested for upcoming interview (CoderPad, HackerRank, etc.)
