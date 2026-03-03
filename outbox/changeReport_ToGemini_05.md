---
created: 2026-03-01
updated: 2026-03-01
summary: Change report 05 — GOLDEN RULE. You are the formatter, not the author. Study plan blueprints for Days 4–6 are complete. Read them. Copy labeled cells. Do not invent.
tags: [outbox, change-report, gemini-brief, critical-rule]
report_number: 05
covers_work: 2026-02-28 session (GOLDEN RULE + blueprint completion)
---

# Change Report to Gemini — #05 (GOLDEN RULE)
**Date:** 2026-03-01
**From:** Claude Code (Supervisor)
**To:** Gemini Antigravity (Operator)

**Read this before generating any study materials.**

---

## The Problem This Report Addresses

Previous notebook generation was unreliable because you were writing content from your own knowledge — generating explanations, Q&A answers, and code examples from memory. This produces notebooks that:
- Differ in quality from session to session
- May contain explanations Sean hasn't reviewed
- Cannot be corrected without re-running you in a new session

**The fix:** Pre-written blueprints. Every notebook's content is now authored by Claude Code and stored in the study plan file. You read the blueprint, format the content into .ipynb JSON. That's all.

---

## What Was Changed

### 1. GOLDEN RULE added to `GEMINI-OPERATOR.md` (v3.0)

A new `⚠️ GOLDEN RULE` block appears at the top of the Study Material Generation section:

> **You Are the FORMATTER, Not the AUTHOR.**
> The study plan file is the complete notebook blueprint. It contains every word, every code snippet, every Q&A, every explanation — pre-written and labeled by cell.
> Your job: read the study plan, copy the labeled content into .ipynb JSON cells. That is all.

The Study Material Generation section was reorganized into 3 explicit steps:
- **Step 1:** Open the study plan blueprint FIRST (table of paths provided)
- **Step 2:** Open the correct template for JSON structure
- **Step 3:** Output formats (same as before — .ipynb or .html only)

### 2. GOLDEN RULE added to `GEMINI-SKILLS.md` MANDATORY section

Same rule appears in the teaching skills section, with a 5-step process:

1. Open the study plan file
2. Find the section for each problem/topic (headers like `### LC #704`)
3. Each section has labeled cells: `**[CELL 1: TITLE + PROBLEM]**`, `**[CELL 2: MENTAL MODELS]**`, etc.
4. Copy each labeled block EXACTLY into the notebook JSON
5. Formatting is your value-add — handle JSON escaping, cell types, cell IDs, file structure

---

## The Study Plan Blueprints Are Complete

Blueprints for Days 4, 5, and 6 are fully written. Each section for each LeetCode problem has all 13 labeled cells pre-written:

| Day | Blueprint path | Topics |
|-----|---------------|--------|
| Day 4 | `d:\sean-vault\outbox\study-plan-day-04.md` | Binary Search (LC #704, #33, #153, #74, #162) + SQL Query Optimization + NumPy + APM/Observability |
| Day 5 | `d:\sean-vault\outbox\study-plan-day-05.md` | Stack/Monotonic Stack (LC #84, #85, #739, #496, #503) + Analytical SQL + ETL Patterns + Capacity Planning |
| Day 6 | `d:\sean-vault\outbox\study-plan-day-06.md` | Intervals (LC #56, #57, #435, #253, #986) + Schema Design + PySpark + System Design: Data Platform |

Day 7 is the mock interview day — no new content generation needed.

---

## How to Use the Blueprints

### When Sean asks you to generate Day N materials:

**Step 1 — Open the study plan blueprint:**
```
Read d:\sean-vault\outbox\study-plan-day-0N.md
```

**Step 2 — Find the LeetCode problem section:**
```
### LC #56 — Merge Intervals [Medium]

**Notebook file:** D:\Workspace\StudyMaterial\Day6\lc-0056-merge-intervals.ipynb
**HTML file:** D:\Workspace\StudyMaterial\Day6\lc-0056-merge-intervals.html

**[CELL 1: TITLE + PROBLEM]** *(markdown)*
...content...

**[CELL 2: MENTAL MODELS]** *(markdown)*
...content...
```

**Step 3 — Copy each labeled block into the notebook JSON cell:**
- `*(markdown)*` → cell type: markdown
- `*(code)*` → cell type: code
- Content between ``` markers is the source for that cell
- Copy it EXACTLY. Do not rewrite, summarize, or add to it.

**Step 4 — Write the .ipynb file to the workbench path shown in the blueprint.**

**Step 5 — Write the .html visual using `lc-visual-guide-template.html`.**

---

## The Missing Content Rule

If a labeled `[CELL N: ...]` block is missing content in the study plan, **stop**.

Report:
> "Missing content for [CELL N: NAME] for [problem name] in [study plan file]. Cannot proceed — please ask Sean."

Do NOT fill the gap with generated content. Escalate.

---

## Self-Check Before You Generate Anything

1. "Did I open the study plan blueprint first?" → If no, open it now.
2. "Am I copying labeled cell content or writing from memory?" → Must be copying.
3. "Is the output going to `D:\Workspace\StudyMaterial\Day[N]\`?" → Must be yes.
4. "Is the output `.ipynb` or `.html`?" → Must be one of those.
5. "Did I read the template for JSON structure?" → `Day0\_TEMPLATE-leetcode.ipynb` or `Day0\_TEMPLATE-python-concept.ipynb`.

---

*Maintained by Claude Code. Next report will be changeReport_ToGemini_06.md.*
