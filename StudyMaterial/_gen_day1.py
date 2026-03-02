"""
Day 1 generator: Arrays & HashMaps | SQL CTEs | Python Generators | AWS Data Platform
Output: D:/Workspace/StudyMaterial/Day1/

Files created:
  lc-0001-two-sum.ipynb / .html
  lc-0217-contains-duplicate.ipynb / .html
  lc-0242-valid-anagram.ipynb / .html
  lc-0238-product-except-self.ipynb / .html
  lc-0347-top-k-frequent.ipynb / .html
  sql-ctes.ipynb
  python-generators.ipynb
  aws-data-platform.ipynb
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/Workspace/StudyMaterial/Day1'
os.makedirs(BASE, exist_ok=True)

# ── notebook helpers ──────────────────────────────────────────────────────────

def nb(cells):
    return {
        "nbformat": 4, "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "cells": cells
    }

def md(cid, text):
    lines = text.split('\n')
    src = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    return {"cell_type": "markdown", "id": cid, "metadata": {}, "source": src}

def code(cid, text):
    lines = text.split('\n')
    src = [l + '\n' for l in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    return {"cell_type": "code", "id": cid, "metadata": {}, "outputs": [], "execution_count": None, "source": src}

def write_nb(path, cells):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb(cells), f, indent=1, ensure_ascii=False)
    print(f'  Written: {path}')

# ── HTML generation (self-contained for HashMap theme) ────────────────────────

HASHMAP_GRAD1  = '#667eea'
HASHMAP_GRAD2  = '#764ba2'
HASHMAP_ACCENT = '#5a4f8f'

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_inline(text):
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def md_to_html(text, accent=HASHMAP_ACCENT):
    lines = text.split('\n')
    out = []
    in_code = False
    code_buf = []
    in_list = False
    in_table = False

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def flush_table():
        nonlocal in_table
        if in_table:
            out.append('</tbody></table>')
            in_table = False

    for line in lines:
        if re.match(r'^```', line) and not in_code:
            flush_list(); flush_table()
            in_code = True; code_buf = []; continue
        if in_code:
            if re.match(r'^```', line):
                in_code = False
                code_html = escape_html('\n'.join(code_buf))
                out.append(
                    '<pre style="background:#1e1e1e;color:#d4d4d4;padding:16px;'
                    'border-radius:8px;overflow-x:auto;font-size:0.87em;line-height:1.5;">'
                    f'<code>{code_html}</code></pre>')
                code_buf = []
            else:
                code_buf.append(line)
            continue
        s = line.strip()
        if s.startswith('|'):
            flush_list()
            cols = [c.strip() for c in s.split('|')[1:-1]]
            if all(re.match(r'^[-: ]+$', c) for c in cols):
                continue
            if not in_table:
                in_table = True
                out.append('<table style="width:100%;border-collapse:collapse;margin:12px 0;font-size:0.9em;">')
                out.append('<thead><tr style="background:#f5f5f5;">')
                for c in cols:
                    out.append(f'<th style="padding:9px;border:1px solid #ddd;text-align:left;">{md_inline(c)}</th>')
                out.append('</tr></thead><tbody>')
            else:
                out.append('<tr>')
                for c in cols:
                    out.append(f'<td style="padding:9px;border:1px solid #ddd;color:#555;vertical-align:top;">{md_inline(c)}</td>')
                out.append('</tr>')
            continue
        else:
            flush_table()
        if s.startswith('<') and not s.startswith('<strong') and not s.startswith('<em') and not s.startswith('<code'):
            flush_list(); out.append(line); continue
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            flush_list()
            lvl = min(len(m.group(1)) + 1, 5)
            sizes = {2: '1.4em', 3: '1.15em', 4: '1.0em', 5: '0.95em'}
            sz = sizes.get(lvl, '1em')
            color = accent if lvl <= 3 else '#444'
            out.append(f'<h{lvl} style="color:{color};font-size:{sz};margin:16px 0 8px;">{md_inline(m.group(2))}</h{lvl}>')
            continue
        if s == '---':
            flush_list(); out.append('<hr style="border:0;border-top:1px solid #eee;margin:14px 0;">'); continue
        lm = re.match(r'^[-*]\s+(.*)', s)
        if lm:
            if not in_list:
                out.append('<ul style="margin-left:20px;color:#555;line-height:1.8;">')
                in_list = True
            out.append(f'<li>{md_inline(lm.group(1))}</li>'); continue
        nm = re.match(r'^\d+\.\s+(.*)', s)
        if nm:
            if not in_list:
                out.append('<ol style="margin-left:20px;color:#555;line-height:1.8;">')
                in_list = True
            out.append(f'<li>{md_inline(nm.group(1))}</li>'); continue
        if not s:
            if not in_list: out.append('')
            continue
        flush_list()
        out.append(f'<p style="color:#555;line-height:1.7;margin:8px 0;">{md_inline(s)}</p>')

    flush_list(); flush_table()
    return '\n'.join(out)


def gen_html(slug, nb_path, html_path, num, title, difficulty):
    with open(nb_path, encoding='utf-8') as f:
        notebook = json.load(f)
    cells = {}
    for cell in notebook['cells']:
        cid = cell.get('id', '')
        cells[cid] = (cell.get('cell_type', 'markdown'), ''.join(cell.get('source', [])))

    def get(cid):
        return cells.get(cid, ('markdown', ''))[1]

    c_title    = get('cell-title')
    c_models   = get('cell-mental-models')
    c_complex  = get('cell-complexity')
    c_optimal  = get('cell-optimal-code')
    c_qa       = get('cell-qa')
    c_citi     = get('cell-citi-narrative')
    c_summary  = get('cell-summary')

    diff_color = {'easy': '#155724', 'medium': '#856404', 'hard': '#721c24'}[difficulty]
    diff_bg    = {'easy': '#d4edda', 'medium': '#fff3cd', 'hard': '#f8d7da'}[difficulty]
    accent     = HASHMAP_ACCENT

    def section(icon, heading, content_html):
        return f'''
<div class="card">
<h2 style="color:{accent};font-size:1.3em;font-weight:600;margin-bottom:16px;">{icon} {heading}</h2>
{content_html}
</div>'''

    grid_open  = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:28px;">'
    grid_close = '</div>'

    body = ''.join([
        section('📋', 'Problem + Core Insight', md_to_html(c_title, accent)),
        grid_open,
        section('🧠', 'Mental Models', md_to_html(c_models, accent)),
        section('📊', 'Complexity Analysis', md_to_html(c_complex, accent)),
        grid_close,
        section('🚀', 'Optimal Solution',
            f'<pre style="background:#1e1e1e;color:#d4d4d4;padding:20px;border-radius:8px;'
            f'overflow-x:auto;font-size:0.88em;line-height:1.5;">'
            f'<code>{escape_html(c_optimal)}</code></pre>'),
        section('🎤', 'Interview Q&amp;A', md_to_html(c_qa, accent)),
        section('💼', 'The Citi Angle',
            f'<div style="background:#fff8e1;border-left:5px solid {accent};padding:18px;border-radius:8px;">'
            + md_to_html(c_citi, accent) + '</div>'),
        section('🎯', 'Summary', md_to_html(c_summary, accent)),
    ])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LC #{num} \u2014 {title} \u2014 HashMap</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
       background: linear-gradient(135deg, {HASHMAP_GRAD1} 0%, {HASHMAP_GRAD2} 100%);
       min-height: 100vh; padding: 40px 20px; }}
.container {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ color: white; text-align: center; font-size: 2.2em; font-weight: 300;
      letter-spacing: -1px; margin-bottom: 8px; }}
.subtitle {{ color: rgba(255,255,255,0.85); text-align: center; font-size: 1em; margin-bottom: 35px; }}
.badge {{ display: inline-block; padding: 3px 12px; border-radius: 20px;
          font-size: 0.55em; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
          margin-left: 10px; vertical-align: middle;
          background: {diff_bg}; color: {diff_color}; }}
.card {{ background: white; border-radius: 12px; padding: 28px;
         box-shadow: 0 20px 60px rgba(0,0,0,0.25); margin-bottom: 28px; }}
code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px;
        font-family: 'Courier New', monospace; font-size: 0.88em; color: #d63384; }}
pre code {{ background: none; color: #d4d4d4; padding: 0; font-size: 1em; }}
@media (max-width: 800px) {{
  div[style*="grid-template-columns:1fr 1fr"] {{ grid-template-columns: 1fr !important; }}
}}
</style>
</head>
<body>
<div class="container">
<h1>LC #{num} \u2014 {title} <span class="badge">{difficulty}</span></h1>
<p class="subtitle">HashMap Pattern &nbsp;|&nbsp; Day 1 Study Material</p>
{body}
</div>
</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  HTML: {html_path}')


# =============================================================================
# LC #1 — TWO SUM
# =============================================================================

TWO_SUM_CELLS = [

md('cell-title', '''# LC #1 — Two Sum
**Category:** HashMap | **Difficulty:** Easy | **Day 1**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>The Problem:</strong> Given an integer array <code>nums</code> and an integer <code>target</code>,
return the indices of two numbers that add up to <code>target</code>.
Exactly one solution exists. Each element may only be used once.
</div>

**Example:**
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]   (nums[0] + nums[1] = 2 + 7 = 9)

Input:  nums = [3, 2, 4], target = 6
Output: [1, 2]
```

**Core Insight:** For each number `x`, you need `target - x`. Instead of scanning for it (O(n) per lookup = O(n²) total), store every number you've seen in a hashmap. Then each lookup is O(1).'''),

md('cell-mental-models', '''## Mental Models

**1. The Complement Store**
Every number has a "partner" it needs: `partner = target - num`. Before checking the current number, ask: "Is my partner already in the store?" If yes — done. If no — add yourself to the store and keep going.

**2. One-Pass Building**
You don't need to build the entire hashmap first and then search. Build and search simultaneously. The moment you find a pair, return. This makes it genuinely O(n) — not O(n) + O(n).

**3. Space for Time Tradeoff**
The classic optimization pattern: spend O(n) extra space (the hashmap) to buy O(n) total time instead of O(n²). At scale — 6,000 servers, millions of data points — this difference is enormous.'''),

code('cell-brute-force', '''# Brute Force — O(n²) time, O(1) space
# Check every pair. Simple but slow.

def twoSum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    # n*(n-1)/2 comparisons — 1000 elements = ~500,000 checks

# Test
print(twoSum_brute([2, 7, 11, 15], 9))   # [0, 1]
print(twoSum_brute([3, 2, 4], 6))         # [1, 2]
print(twoSum_brute([3, 3], 6))            # [0, 1]'''),

md('cell-walkthrough', '''## Step-by-Step: HashMap Approach

Trace through `nums = [2, 7, 11, 15]`, `target = 9`:

| Step | `i` | `num` | `complement` | In `seen`? | Action |
|------|-----|-------|-------------|-----------|--------|
| 1 | 0 | 2 | 7 | No | `seen = {2: 0}` |
| 2 | 1 | 7 | 2 | **Yes** | Return `[seen[2], 1]` = `[0, 1]` ✓ |

The key insight: at step 2, we check "is 2 in seen?" before adding 7. This means we find the pair in one pass, even if the earlier element came first.'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(n) space
# One pass: check complement, then store current number.

def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}  # maps value → index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    # Guaranteed to find a solution (problem states exactly one exists)

# Test
print(twoSum([2, 7, 11, 15], 9))   # [0, 1]
print(twoSum([3, 2, 4], 6))         # [1, 2]
print(twoSum([3, 3], 6))            # [0, 1]  ← works: checks seen before adding self'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force (two loops) | O(n²) | O(1) | n*(n-1)/2 comparisons |
| Sort + Two Pointers | O(n log n) | O(n) | Loses original indices |
| **HashMap (Optimal)** | **O(n)** | **O(n)** | One pass, O(1) lookup |

**Why O(1) lookup?**
Python `dict` is a hash table. Average case O(1) for `in` and `[]` operations. Worst case O(n) with pathological hash collisions — doesn't happen with integers in practice.

**Space note:** We store at most n entries in the hashmap — one per element. O(n) space.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why check complement before adding to the map?**
A: Prevents using the same element twice. If `nums = [3, 3]` and target = 6: when we process the second 3, the first 3 is already in seen at index 0. We return [0, 1]. If we added first and then checked, we'd look up index 0 for both — but the problem says same index can't be used twice.

**Q: What's `seen` storing — keys or values?**
A: Keys are the **values** from `nums`, values in the dict are the **indices**. `seen = {value: index}`. This is the reverse of what you might expect — we look up by number to get its position.

**Q: What if the array had multiple valid pairs?**
A: Return on the first found. To return all pairs: collect into a list instead, skip returning early.

**Q: What data structure is Python `{}` (dict) under the hood?**
A: A hash table. The CPython implementation uses open addressing with pseudo-random probing. Average O(1) for insert/lookup/delete. Guaranteed O(n) worst case (very rare with integers).

**Q: Could you solve this with O(1) space?**
A: Yes — sort a copy (keeping original indices), then use two pointers. But sorting loses index info, so you'd need to track original indices separately. And it's O(n log n) time, not O(n).'''),

md('cell-citi-narrative', '''## The Citi Angle

**Pattern recognition:** At Citi, monitoring 6,000+ endpoints, I frequently needed to find pairs or groups of resources with complementary behavior — servers where one's CPU spike was offset by another's idle period (capacity balancing).

**Direct application:** If you have a list of server CPU readings and want to find two servers whose combined utilization equals exactly 100% (for load-balancing pairing):
```python
cpu_readings = {server_id: cpu_pct for server_id in servers}
# Two Sum pattern: complement = 100 - cpu_pct
```

**Interview tie-in:** "The HashMap pattern is foundational to data engineering. At Citi, fast lookup against growing datasets was constant — whether matching alert IDs, deduplicating metric keys, or joining telemetry streams. O(1) lookup vs O(n) lookup on 6,000 servers per collection cycle is the difference between milliseconds and seconds."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | HashMap — complement lookup |
| **Time** | O(n) |
| **Space** | O(n) |
| **Key line** | `if complement in seen: return [seen[complement], i]` |
| **Say in interview** | "This is a complement-store problem. O(n) time by trading O(n) space for O(1) lookup." |

**The one-liner to memorize:**
```python
seen = {}
for i, num in enumerate(nums):
    if target - num in seen: return [seen[target-num], i]
    seen[num] = i
```'''),

]

write_nb(f'{BASE}/lc-0001-two-sum.ipynb', TWO_SUM_CELLS)
gen_html('lc-0001-two-sum', f'{BASE}/lc-0001-two-sum.ipynb',
         f'{BASE}/lc-0001-two-sum.html', 1, 'Two Sum', 'easy')


# =============================================================================
# LC #217 — CONTAINS DUPLICATE
# =============================================================================

CONTAINS_DUP_CELLS = [

md('cell-title', '''# LC #217 — Contains Duplicate
**Category:** HashSet | **Difficulty:** Easy | **Day 1**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>The Problem:</strong> Given an integer array <code>nums</code>, return <code>true</code> if
any value appears at least twice. Return <code>false</code> if every element is distinct.
</div>

**Examples:**
```
Input: [1, 2, 3, 1]  → true   (1 appears twice)
Input: [1, 2, 3, 4]  → false  (all distinct)
Input: [1, 1, 1, 3]  → true
```

**Core Insight:** You need O(1) membership testing as you scan. A HashSet is exactly that — add each element, and if it's already there, you found a duplicate. Exit immediately (early termination).'''),

md('cell-mental-models', '''## Mental Models

**1. The Seen Set**
Maintain a set of everything encountered so far. For each new element: "Have I seen you before?" If yes — duplicate found. If no — add to the set, continue. The set is your memory.

**2. Early Termination**
You don't need to process the entire array. The moment you find a duplicate, return `True`. This matters in practice — duplicates near the front of large arrays mean very fast execution.

**3. Set vs HashMap**
A set is a hashmap where you only care about keys, not values. Use a set when you only need membership testing (is X in the collection?). Use a dict when you also need to store data alongside each key (Two Sum stores the index).'''),

code('cell-brute-force', '''# Approach 1 — Sort, then check adjacent
# O(n log n) time, O(1) extra space (modifies input)

def containsDuplicate_sort(nums):
    nums.sort()  # adjacent duplicates will be neighbors
    for i in range(1, len(nums)):
        if nums[i] == nums[i - 1]:
            return True
    return False

# Approach 2 — Compare length with set length (Pythonic one-liner)
# O(n) time but builds the full set before checking
def containsDuplicate_oneliner(nums):
    return len(nums) != len(set(nums))

# Test
print(containsDuplicate_sort([1, 2, 3, 1]))   # True
print(containsDuplicate_sort([1, 2, 3, 4]))   # False'''),

md('cell-walkthrough', '''## Why HashSet Beats Both

**Sort approach:** O(n log n) and **mutates** the input array. You often can't destroy the caller's data. Also slower.

**One-liner `set(nums)`:** Correct and Pythonic, but builds the **entire** set before any comparison. If the first two elements are duplicates, it still processes all n elements. No early exit.

**HashSet with early exit:** Processes elements one at a time. Stops the moment a duplicate is found. For arrays like `[1, 1, 2, 3, ..., 999999]`, this returns after 2 iterations instead of n.

In production data pipelines, you often deduplicate event streams. Early exit means you can flag bad data faster.'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(n) space
# HashSet with early termination.

def containsDuplicate(nums: list[int]) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True   # found duplicate — exit immediately
        seen.add(num)
    return False

# One-liner alternative (no early exit, but clean):
# return len(nums) != len(set(nums))

# Test
print(containsDuplicate([1, 2, 3, 1]))    # True
print(containsDuplicate([1, 2, 3, 4]))    # False
print(containsDuplicate([1, 1, 1, 3, 3])) # True'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force (nested loops) | O(n²) | O(1) | Compare every pair |
| Sort + adjacent check | O(n log n) | O(1) | Mutates input |
| `len(nums) != len(set(nums))` | O(n) | O(n) | No early exit |
| **HashSet with early exit** | **O(n)** | **O(n)** | **Stops on first dup** |

**Space note:** In the worst case (no duplicates), the set holds all n elements. O(n) space.

**Practical note:** For very large arrays with early duplicates, the expected runtime is much better than O(n). The O(n) is the worst case (no duplicate or duplicate at the very end).'''),

md('cell-qa', '''## Interview Q&A

**Q: When would you prefer the sort approach over the hashset?**
A: When memory is extremely constrained — O(1) extra space vs O(n). In embedded systems or when the array is nearly sorted already. Sorting in-place (`.sort()` in Python) uses O(log n) stack space for Timsort, essentially O(1) extra.

**Q: Why does `len(nums) != len(set(nums))` work?**
A: A set only keeps unique elements. If any duplicates exist, `set(nums)` has fewer elements than `nums`. If lengths are equal, all elements are unique.

**Q: What's the difference between a Python `set` and `frozenset`?**
A: `set` is mutable (you can add/remove). `frozenset` is immutable and hashable — you can use it as a dict key or store it inside another set.

**Q: Could this problem appear in a data engineering context?**
A: Constantly. Deduplication is a core ETL operation — ensuring metric IDs are unique, detecting double-counted events, validating primary keys before loading to a data warehouse. The HashSet pattern is fundamental.'''),

md('cell-citi-narrative', '''## The Citi Angle

**ETL deduplication:** At Citi, telemetry agents sometimes sent duplicate metric records (network retries, agent restarts). Before aggregating, we needed to detect and drop duplicates.

**Direct analogy:**
```python
# Checking for duplicate server_id in a batch before inserting
seen_ids = set()
for record in batch:
    if record['server_id'] in seen_ids:
        log_duplicate(record)
        continue
    seen_ids.add(record['server_id'])
    insert(record)
```

**Interview tie-in:** "Deduplication before aggregation was a daily concern at Citi — 6,000 endpoints with retry logic meant we saw duplicate metric records. The HashSet pattern — add and check — is exactly what prevents double-counting in capacity utilization reports."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | HashSet — membership testing with early exit |
| **Time** | O(n) worst case, much better average |
| **Space** | O(n) |
| **Key line** | `if num in seen: return True` |
| **Say in interview** | "HashSet for O(1) membership testing. Early exit on first duplicate." |

**When to choose which:**
- Need early exit + no mutation → HashSet loop (this solution)
- Memory constrained → Sort approach
- Idiomatic Python, no early exit needed → `len(nums) != len(set(nums))`'''),

]

write_nb(f'{BASE}/lc-0217-contains-duplicate.ipynb', CONTAINS_DUP_CELLS)
gen_html('lc-0217-contains-duplicate', f'{BASE}/lc-0217-contains-duplicate.ipynb',
         f'{BASE}/lc-0217-contains-duplicate.html', 217, 'Contains Duplicate', 'easy')


# =============================================================================
# LC #242 — VALID ANAGRAM
# =============================================================================

VALID_ANAGRAM_CELLS = [

md('cell-title', '''# LC #242 — Valid Anagram
**Category:** HashMap / Counter | **Difficulty:** Easy | **Day 1**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>The Problem:</strong> Given two strings <code>s</code> and <code>t</code>, return <code>true</code>
if <code>t</code> is an anagram of <code>s</code>.
An anagram uses the same characters in any order.
</div>

**Examples:**
```
"anagram", "nagaram"  → true   (same letters, rearranged)
"rat",     "car"      → false  (different letters)
"listen",  "silent"   → true
```

**Core Insight:** Two strings are anagrams if and only if they have **identical character frequency maps**. Build the frequency map for both and compare — or build one and cancel-out with the other.'''),

md('cell-mental-models', '''## Mental Models

**1. The Frequency Fingerprint**
Every string has a unique fingerprint: a map of `{char: count}`. Two strings are anagrams iff their fingerprints are identical. This is the most direct mental model — build both maps, compare.

**2. The Cancel-Out Pattern**
More elegant: increment counts for `s`, decrement for `t`. If they're anagrams, every character added by `s` is cancelled by `t`. Any non-zero count at the end means they differ. This works in a single combined map.

**3. Bounded Space Observation**
For lowercase English letters: at most 26 distinct keys in the hashmap, regardless of string length. This makes space complexity O(1) — not O(n). This is a key interview insight: "bounded alphabet = O(1) space."'''),

code('cell-brute-force', '''# Approach 1 — Sort both strings and compare
# O(n log n) time, O(n) space (sorting creates copies)

def isAnagram_sort(s: str, t: str) -> bool:
    return sorted(s) == sorted(t)

# Test
print(isAnagram_sort("anagram", "nagaram"))  # True
print(isAnagram_sort("rat", "car"))          # False

# Approach 2 — Python Counter (built-in, clean)
from collections import Counter

def isAnagram_counter(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

print(isAnagram_counter("listen", "silent"))  # True'''),

md('cell-walkthrough', '''## Trace: Cancel-Out Approach

Trace `s = "rat"`, `t = "car"`:

**Build count from `s = "rat"`:**
```
count = {'r': 1, 'a': 1, 't': 1}
```

**Cancel with `t = "car"`:**
- `c`: not in count → count['c'] = -1 → return False ✓

**Trace `s = "anagram"`, `t = "nagaram"`:**

Build from `s`: `{'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}`

Cancel with `t = "nagaram"`:
- n: 1→0, a: 3→2, g: 1→0, a: 2→1, r: 1→0, a: 1→0, m: 1→0

All counts are 0 → return True ✓'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(1) space (26-letter bounded hashmap)
# Manual cancel-out — most instructive for interviews.

def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False          # early exit — different lengths can't be anagrams

    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1   # build frequency map for s
    for c in t:
        count[c] = count.get(c, 0) - 1   # cancel out with t
        if count[c] < 0:
            return False                   # t has a char not in s (or more of it)

    return True   # all counts cancelled to 0 (or 0 remaining)

# Pythonic one-liner:
# return Counter(s) == Counter(t)

# Test
print(isAnagram("anagram", "nagaram"))  # True
print(isAnagram("rat", "car"))          # False
print(isAnagram("a", "ab"))             # False  (length check catches this instantly)'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Sort comparison | O(n log n) | O(n) | Creates sorted copies |
| `Counter(s) == Counter(t)` | O(n) | O(1)* | Pythonic, two passes |
| **Manual cancel-out** | **O(n)** | **O(1)*** | **Early exit on mismatch** |

*O(1) because the alphabet is bounded: at most 26 keys for lowercase English. If the alphabet were unbounded (Unicode), space would be O(k) where k = unique characters.

**Why early length check matters:** Strings of different lengths can never be anagrams. This check costs O(1) and avoids building the entire frequency map for clearly non-anagram inputs.'''),

md('cell-qa', '''## Interview Q&A

**Q: What if the input contains Unicode characters?**
A: Counter and the hashmap approach both still work — keys are just Unicode code points instead of letters. Space complexity becomes O(k) where k is the number of unique characters, not O(1).

**Q: Why is `Counter` O(1) space for lowercase letters?**
A: At most 26 unique keys regardless of string length. `Counter("aaaaaaaaaaaa")` has one key: `{'a': 12}`. The map size is bounded by the alphabet, not the string length.

**Q: Your early exit checks `count[c] < 0`. Why not `!= 0`?**
A: We're cancelling as we go. A count of 0 is fine (character balanced). Negative means `t` has more of this character than `s` — that's a mismatch. Positive counts remaining at the end would also mean mismatch, but the length check prevents that case (equal lengths + no negatives = all counts are 0).

**Q: What's the difference between `Counter` and a plain `dict` for this problem?**
A: Functionally equivalent here. `Counter` handles missing keys gracefully (returns 0 for unseen keys), subtraction of two Counters drops negative/zero counts automatically. `Counter` is cleaner but knowing the manual approach shows you understand what's happening.'''),

md('cell-citi-narrative', '''## The Citi Angle

**Character frequency = data fingerprinting.** The same mental model applies to data integrity checks: if you expect a set of metric names from 6,000 servers and want to verify no names changed between collection cycles, you compare frequency fingerprints.

**Practical analogy:**
```python
# Verify expected vs actual metric keys in telemetry batch
expected = Counter(["cpu_pct", "mem_pct", "disk_read", "disk_write"])
actual   = Counter([m["metric_name"] for m in batch])
if expected != actual:
    alert(f"Metric schema drift: {expected - actual} missing, {actual - expected} unexpected")
```

**Interview tie-in:** "The frequency map pattern generalizes beyond characters — at Citi I used it to fingerprint metric schemas and catch schema drift between APM tool upgrades. Same O(n) build, O(1) comparison."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | HashMap — frequency fingerprint |
| **Time** | O(n) |
| **Space** | O(1) for lowercase English (bounded alphabet) |
| **Key line** | `if count[c] < 0: return False` |
| **Say in interview** | "Frequency map. O(n) time, O(1) space because the alphabet is bounded at 26 characters." |

**The two patterns to know:**
```python
# Pattern A: Counter comparison (Pythonic)
return Counter(s) == Counter(t)

# Pattern B: Manual cancel-out (shows understanding)
count = {}
for c in s: count[c] = count.get(c, 0) + 1
for c in t:
    count[c] = count.get(c, 0) - 1
    if count[c] < 0: return False
return True
```'''),

]

write_nb(f'{BASE}/lc-0242-valid-anagram.ipynb', VALID_ANAGRAM_CELLS)
gen_html('lc-0242-valid-anagram', f'{BASE}/lc-0242-valid-anagram.ipynb',
         f'{BASE}/lc-0242-valid-anagram.html', 242, 'Valid Anagram', 'easy')


# =============================================================================
# LC #238 — PRODUCT OF ARRAY EXCEPT SELF
# =============================================================================

PRODUCT_CELLS = [

md('cell-title', '''# LC #238 — Product of Array Except Self
**Category:** Array / Prefix Products | **Difficulty:** Medium | **Day 1**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>The Problem:</strong> Given an integer array <code>nums</code>, return an array <code>output</code>
where <code>output[i]</code> is the product of all elements in <code>nums</code> except <code>nums[i]</code>.
<strong>No division allowed. Must run in O(n).</strong>
</div>

**Example:**
```
Input:  [1, 2, 3, 4]
Output: [24, 12, 8, 6]

Check: output[0] = 2*3*4 = 24 ✓
       output[1] = 1*3*4 = 12 ✓
       output[2] = 1*2*4 = 8  ✓
       output[3] = 1*2*3 = 6  ✓
```

**Core Insight:** `output[i] = product of everything LEFT of i × product of everything RIGHT of i`. Build each half in a single pass. Two passes total = O(n).'''),

md('cell-mental-models', '''## Mental Models

**1. Left × Right Decomposition**
Any position `i` has exactly two "contributions" — everything to its left, and everything to its right. Compute a left-products array and a right-products array, then multiply element-wise. This is the conceptual foundation.

**2. The Running Product Trick**
You don't need two extra arrays. Use one result array. First pass: fill result[i] with the left product. Second pass: maintain a running right product and multiply into result[i] in-place. O(1) extra space.

**3. Why No Division?**
If you could divide: `total_product / nums[i]`. But — what if nums[i] = 0? Division by zero is undefined. The prefix/suffix approach handles zeros naturally with no special cases. This is why the constraint exists: it forces the elegant solution.'''),

code('cell-brute-force', '''# Brute Force — O(n²) time, O(n) space
# For each position, multiply all other elements.

def productExceptSelf_brute(nums):
    n = len(nums)
    result = []
    for i in range(n):
        product = 1
        for j in range(n):
            if i != j:
                product *= nums[j]
        result.append(product)
    return result

print(productExceptSelf_brute([1, 2, 3, 4]))  # [24, 12, 8, 6]
print(productExceptSelf_brute([-1, 1, 0, -3, 3]))  # [0, 0, 9, 0, 0]'''),

md('cell-walkthrough', '''## Trace: Two-Pass Prefix/Suffix

Input: `[1, 2, 3, 4]`

**Left pass** — result[i] = product of everything to the LEFT:
```
Start: result = [1, 1, 1, 1], prefix = 1

i=0: result[0] = 1  (nothing to left),  prefix = 1 * 1 = 1
i=1: result[1] = 1  (only nums[0]=1),   prefix = 1 * 2 = 2
i=2: result[2] = 2  (nums[0]*nums[1]),  prefix = 2 * 3 = 6
i=3: result[3] = 6  (nums[0..2]),       prefix = 6 * 4 = 24
Result after left pass: [1, 1, 2, 6]
```

**Right pass** — multiply by product of everything to the RIGHT:
```
Start: suffix = 1

i=3: result[3] *= 1  → 6*1  = 6,  suffix = 1 * 4 = 4
i=2: result[2] *= 4  → 2*4  = 8,  suffix = 4 * 3 = 12
i=1: result[1] *= 12 → 1*12 = 12, suffix = 12 * 2 = 24
i=0: result[0] *= 24 → 1*24 = 24, suffix = 24 * 1 = 24
Final: [24, 12, 8, 6]  ✓
```'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(1) extra space
# Left pass fills result with left products.
# Right pass multiplies in right products using running suffix.

def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [1] * n

    # Left pass: result[i] = product of nums[0..i-1]
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]

    # Right pass: multiply result[i] by product of nums[i+1..n-1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]

    return result

# Test
print(productExceptSelf([1, 2, 3, 4]))         # [24, 12, 8, 6]
print(productExceptSelf([-1, 1, 0, -3, 3]))    # [0, 0, 9, 0, 0]
print(productExceptSelf([0, 0]))               # [0, 0]'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force | O(n²) | O(n) | Product for each position |
| Left + Right arrays | O(n) | O(n) | Two extra arrays |
| **Left + Running suffix** | **O(n)** | **O(1)*** | **In-place on result** |

*The output array `result` doesn't count as extra space per the problem statement — you must return an array anyway.

**Handles zeros:** If nums = [0, 1, 2]:
- prefix pass:  result = [1, 0, 0]
- suffix pass:  result = [1*2, 0*2, 0*1] = [2, 0, 0]

The zero propagates naturally — no special casing needed.

**Multiple zeros:** If nums = [0, 0, 1], all products are 0 (two zeros → neither side can avoid having a zero). The algorithm handles this correctly without any branches.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why is division not allowed?**
A: Division by zero is undefined. If `nums[i] = 0`, you'd divide by zero. The prefix/suffix approach handles zero naturally — no special cases needed.

**Q: What's the extra space in your O(1) solution?**
A: Just two scalar variables — `prefix` and `suffix`. The output array `result` is required (the problem asks for it), so it doesn't count as extra space.

**Q: What happens with two zeros in the array?**
A: Every output value becomes 0. If two elements are 0, every subarray "except self" contains at least one 0. The algorithm computes this correctly without any special handling.

**Q: How is this pattern useful in data engineering?**
A: Running products appear in cumulative calculations — compounding growth rates, probability chains (joint probability of a sequence of events), or building prefix-product lookup tables for O(1) range product queries. Once you have the prefix products array, `product(nums[i..j]) = prefix[j+1] / prefix[i]` — but with division, so pre-compute for zero-safe arrays.

**Q: Can you solve this with a single pass?**
A: No — to know the right product at index `i`, you need to have seen everything to the right. Single-pass isn't possible without extra space. Two passes is the theoretical minimum for this approach.'''),

md('cell-citi-narrative', '''## The Citi Angle

**Running products in capacity planning:** At Citi, compound growth calculations were common — if a server's CPU grows 2% per week, what is the cumulative utilization after k weeks? This is a prefix product computation.

**More directly:** When computing a rolling efficiency score across a chain of pipeline stages, you multiply stage efficiencies together. If any stage has 0% efficiency (is down), the entire pipeline product is 0. The prefix/suffix decomposition handles this correctly.

**Interview tie-in:** "The 'no division' constraint is a proxy for zero-robustness — and in telemetry data, zeros are common (servers that are off, metrics that aren't reporting). The prefix/suffix pattern handles zeros without special-casing, which matters in production."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Prefix + Suffix products |
| **Time** | O(n) |
| **Space** | O(1) extra |
| **Key insight** | `result[i] = left_product × right_product` — build each in one pass |
| **Say in interview** | "Decompose into left product and right product. Two passes, O(1) extra space." |

**Template to memorize:**
```python
result = [1] * n
prefix = 1
for i in range(n):
    result[i] = prefix; prefix *= nums[i]

suffix = 1
for i in range(n-1, -1, -1):
    result[i] *= suffix; suffix *= nums[i]
```'''),

]

write_nb(f'{BASE}/lc-0238-product-except-self.ipynb', PRODUCT_CELLS)
gen_html('lc-0238-product-except-self', f'{BASE}/lc-0238-product-except-self.ipynb',
         f'{BASE}/lc-0238-product-except-self.html', 238, 'Product of Array Except Self', 'medium')


# =============================================================================
# LC #347 — TOP K FREQUENT ELEMENTS
# =============================================================================

TOP_K_CELLS = [

md('cell-title', '''# LC #347 — Top K Frequent Elements
**Category:** HashMap + Heap (or Bucket Sort) | **Difficulty:** Medium | **Day 1**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>The Problem:</strong> Given an integer array <code>nums</code> and integer <code>k</code>,
return the <code>k</code> most frequent elements. Answer may be in any order.
</div>

**Examples:**
```
nums = [1, 1, 1, 2, 2, 3],  k = 2  → [1, 2]
nums = [1],                  k = 1  → [1]
```

**Core Insight:** Always decompose Top-K into two steps: (1) count frequencies with a hashmap, (2) find the top k by frequency. Step 2 can be done with a min-heap in O(n log k) or bucket sort in O(n) — know both.'''),

md('cell-mental-models', '''## Mental Models

**1. Count First, Rank Second**
Never try to do both in one pass. Build the frequency map. Then find the top k from it. This clean separation makes both problems simple.

**2. Min-Heap of Size K**
Maintain a min-heap with exactly k elements (by frequency). For each new element: if its frequency > the min in the heap, pop the min and push the new one. At the end, the heap contains the top k. O(n log k) — better than O(n log n) sort when k << n.

**3. Bucket Sort Insight (O(n))**
Frequency is bounded: it can't exceed `len(nums)`. Use frequency as an array index: `buckets[freq].append(num)`. Iterate buckets from high to low, collecting elements until you have k. No comparisons needed — O(n) total.'''),

code('cell-brute-force', '''# Approach 1 — HashMap + Full Sort  O(n log n)
# Count frequencies, sort all items by frequency, take top k.

from collections import Counter

def topKFrequent_sort(nums, k):
    count = Counter(nums)
    # sort by frequency descending, take first k keys
    return sorted(count, key=count.get, reverse=True)[:k]

print(topKFrequent_sort([1, 1, 1, 2, 2, 3], 2))   # [1, 2]

# Approach 2 — heapq.nlargest  (O(n log k), concise)
import heapq

def topKFrequent_nlargest(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

print(topKFrequent_nlargest([1, 1, 1, 2, 2, 3], 2))  # [1, 2]'''),

md('cell-walkthrough', '''## Trace: Bucket Sort Approach

Input: `nums = [1, 1, 1, 2, 2, 3]`, `k = 2`

**Step 1 — Frequency count:**
```
Counter: {1: 3, 2: 2, 3: 1}
```

**Step 2 — Build frequency buckets:**
```
len(nums) = 6, so buckets has indices 0..6
buckets[3] = [1]    (element 1 appears 3 times)
buckets[2] = [2]    (element 2 appears 2 times)
buckets[1] = [3]    (element 3 appears 1 time)
```

**Step 3 — Collect from highest bucket down:**
```
i=6: [] — skip
i=5: [] — skip
i=4: [] — skip
i=3: [1] → result = [1]       (len=1, need 2)
i=2: [2] → result = [1, 2]    (len=2, done!)
Return [1, 2] ✓
```'''),

code('cell-optimal-code', '''# Optimal — Bucket Sort, O(n) time, O(n) space
# Frequency bounded by len(nums) — use as array index.

from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)

    # buckets[freq] = list of numbers with that frequency
    # max possible frequency = len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, freq in count.items():
        buckets[freq].append(num)

    # Collect from highest frequency down until we have k elements
    result = []
    for freq in range(len(buckets) - 1, 0, -1):
        result.extend(buckets[freq])
        if len(result) >= k:
            return result[:k]

    return result  # shouldn't reach here if k <= len(unique elements)

# Test
print(topKFrequent([1, 1, 1, 2, 2, 3], 2))    # [1, 2]
print(topKFrequent([1], 1))                    # [1]
print(topKFrequent([4, 1, -1, 2, -1, 2, 3], 2))  # [-1, 2]'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| HashMap + full sort | O(n log n) | O(n) | Overkill — sorting all unique elements |
| `heapq.nlargest(k, ...)` | O(n log k) | O(n + k) | Good when k << n |
| **Bucket sort** | **O(n)** | **O(n)** | **Bounded frequency = linear** |

**Why heap is O(n log k) not O(n log n):**
A min-heap of fixed size k: each push/pop is O(log k). We do at most n heap operations. Total: O(n log k). When k = 1, this is O(n). When k = n, it's O(n log n) — same as sort.

**Bucket sort intuition:** Counting sort is O(n + range). Here range = n (max frequency ≤ array length), so O(n + n) = O(n). The key is that the range is bounded.'''),

md('cell-qa', '''## Interview Q&A

**Q: When would you use heap over bucket sort in production?**
A: When memory matters — heap uses O(k) extra space vs O(n) for buckets. When k is very small (top 3 of 1 million), heap is the right call. When k is large or you need O(n), use buckets.

**Q: What is `Counter` under the hood?**
A: A subclass of `dict`. `Counter(nums)` iterates once, incrementing counts. Time: O(n). Access pattern: `count[key]` = 0 for missing keys (doesn't raise KeyError).

**Q: Why does `heapq.nlargest` outperform a full sort?**
A: `nlargest(k, ...)` uses a min-heap of size k. It processes all n elements in O(n log k) instead of sorting all n in O(n log n). Python's implementation is especially efficient for small k — it switches to a simple scan when k=1.

**Q: How is Top-K relevant in data engineering?**
A: Everywhere. Top-K slow queries (query optimization). Top-K error codes (alert prioritization). Top-K resource consumers (capacity planning). At Citi: which 10 servers out of 6,000 are consistently the highest CPU consumers? Exactly this pattern.

**Q: What if there are ties at position k?**
A: The problem says any valid answer is acceptable. In practice for Top-K problems in production, you'd sort by secondary key (name, ID) to make results deterministic.'''),

md('cell-citi-narrative', '''## The Citi Angle

**Top-K is a capacity planning primitive.** At Citi, out of 6,000 monitored endpoints:
- Which 10 servers have the highest average CPU over 30 days? → Top-K by average.
- Which 5 servers trigger the most alerts? → Top-K by alert count.
- Which application tier consumes the most memory? → Top-K by aggregate consumption.

**Direct code analogy:**
```python
# Top 10 servers by average CPU (last 30 days)
from collections import Counter
# cpu_readings: {server_id: [list of cpu_pct values]}
avg_cpu = {sid: sum(vals)/len(vals) for sid, vals in cpu_readings.items()}

# heapq approach for large fleet:
import heapq
top_10 = heapq.nlargest(10, avg_cpu, key=avg_cpu.get)
```

**Interview tie-in:** "Top-K queries are one of the most common patterns in monitoring and observability. At Citi, weekly capacity reports always started with: 'Show me the top 10 most stressed servers.' That's exactly this problem — count, then rank."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Count frequencies (HashMap), then find top K |
| **Heap approach** | O(n log k) time, O(n + k) space — use when k << n |
| **Bucket approach** | O(n) time, O(n) space — use when you need true linear |
| **Key insight** | Frequency ≤ len(nums) → use frequency as array index |
| **Say in interview** | "Two-step: count with Counter, then heap of size k. Or bucket sort for O(n)." |

**Two templates:**

```python
# Template A: Heap (O(n log k))
count = Counter(nums)
return heapq.nlargest(k, count, key=count.get)

# Template B: Bucket Sort (O(n))
count = Counter(nums)
buckets = [[] for _ in range(len(nums) + 1)]
for num, freq in count.items(): buckets[freq].append(num)
result = []
for freq in range(len(buckets)-1, 0, -1):
    result.extend(buckets[freq])
    if len(result) >= k: return result[:k]
```'''),

]

write_nb(f'{BASE}/lc-0347-top-k-frequent.ipynb', TOP_K_CELLS)
gen_html('lc-0347-top-k-frequent', f'{BASE}/lc-0347-top-k-frequent.ipynb',
         f'{BASE}/lc-0347-top-k-frequent.html', 347, 'Top K Frequent Elements', 'medium')


# =============================================================================
# SQL — CTEs
# =============================================================================

SQL_CTES_CELLS = [

md('c01', '''# SQL — Common Table Expressions (CTEs)
**Day 1 — SQL Module**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>Core Insight:</strong> CTEs are a <em>readability</em> feature, not a performance feature.
They name intermediate result sets so complex multi-step queries read like sequential logic
instead of nested spaghetti. The optimizer often treats them the same as subqueries — but
your colleagues (and future you) will thank you.
</div>

### Why It Matters
At Citi, capacity queries had 4-5 logical steps: filter raw telemetry → deduplicate → daily average → 30-day trend → flag at-risk servers. Without CTEs, this is 4 levels of nested subqueries. With CTEs, each step is named and readable.'''),

md('c02', '''## The Syntax

```sql
WITH cte_name AS (
    SELECT ...
    FROM   ...
    WHERE  ...
),
second_cte AS (
    SELECT ...
    FROM   cte_name   -- reference the first CTE by name
    WHERE  ...
)
SELECT *
FROM second_cte;
```

**Key rules:**
- Start with `WITH`, not `SELECT`
- Separate multiple CTEs with commas — the **last one has no comma**
- Reference earlier CTEs by name in later CTEs
- The final `SELECT` is the actual query that returns results — it's not part of the CTE'''),

code('c03', '''-- Example 1: Find employees earning above their department average
-- Step 1: Calculate average salary per department (named CTE)
-- Step 2: Join back to find employees above that average

WITH dept_averages AS (
    SELECT
        department_id,
        AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT
    e.name,
    e.salary,
    d.avg_salary,
    ROUND(e.salary - d.avg_salary, 2) AS above_average_by
FROM employees e
JOIN dept_averages d ON e.department_id = d.department_id
WHERE e.salary > d.avg_salary
ORDER BY above_average_by DESC;

-- Without CTE (nested subquery — same result, harder to read):
SELECT e.name, e.salary,
       (SELECT AVG(salary) FROM employees e2
        WHERE e2.department_id = e.department_id) AS avg_salary
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees e2
                  WHERE e2.department_id = e.department_id);'''),

md('c04', '''## Chained CTEs — Multi-Step Pipeline

This is where CTEs shine: expressing a data pipeline as sequential, named steps.'''),

code('c05', '''-- Capacity planning pipeline:
-- Step 1: Deduplicate raw telemetry
-- Step 2: Compute daily averages
-- Step 3: Identify at-risk servers (peak > 80%)

WITH deduped AS (
    -- Remove any duplicate records from the same server/day
    SELECT DISTINCT
        server_id,
        collection_date,
        cpu_utilization
    FROM telemetry_raw
    WHERE collection_date >= CURRENT_DATE - INTERVAL '30 days'
),
daily_avg AS (
    -- One row per server per day
    SELECT
        server_id,
        collection_date,
        AVG(cpu_utilization) AS avg_cpu,
        MAX(cpu_utilization) AS peak_cpu
    FROM deduped
    GROUP BY server_id, collection_date
),
monthly_stats AS (
    -- Aggregate to 30-day summary per server
    SELECT
        server_id,
        AVG(avg_cpu)  AS avg_30d,
        MAX(peak_cpu) AS peak_30d,
        COUNT(*)      AS days_sampled
    FROM daily_avg
    GROUP BY server_id
)
SELECT
    server_id,
    ROUND(avg_30d, 2)  AS avg_cpu_30d,
    ROUND(peak_30d, 2) AS peak_cpu_30d,
    days_sampled,
    CASE WHEN peak_30d > 80 THEN 'AT RISK'
         WHEN avg_30d  > 65 THEN 'MONITOR'
         ELSE 'HEALTHY' END AS status
FROM monthly_stats
ORDER BY peak_30d DESC;'''),

md('c06', '''## Recursive CTEs — Walk a Hierarchy

Use when data has a parent-child relationship: org charts, folder trees, alert escalation chains, network topology.'''),

code('c07', '''-- Recursive CTE: Walk an org chart from CEO down to all reports

WITH RECURSIVE org_chart AS (
    -- BASE CASE: The root node (CEO has no manager)
    SELECT
        employee_id,
        name,
        manager_id,
        1 AS org_level,
        name AS path
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- RECURSIVE CASE: Join employees to their manager
    SELECT
        e.employee_id,
        e.name,
        e.manager_id,
        oc.org_level + 1,
        oc.path || ' > ' || e.name   -- build the path string
    FROM employees e
    JOIN org_chart oc ON e.manager_id = oc.employee_id
    WHERE oc.org_level < 10           -- SAFETY: prevent infinite loops from cycles
)
SELECT
    LPAD(' ', (org_level - 1) * 4, ' ') || name AS org_tree,
    org_level,
    path
FROM org_chart
ORDER BY path;

-- Without the depth limit, a cycle (A manages B, B manages A) would loop forever.
-- Always add WHERE level < N or a MAXRECURSION hint.'''),

md('c08', '''## Interview Q&A

**Q: What is the difference between a CTE and a subquery?**
A: CTEs are named and reusable within the same query — you can reference a CTE multiple times. Subqueries are inline and can't be referenced elsewhere. CTEs are significantly more readable for multi-step logic. Functionally, most optimizers treat them the same (no materialization guarantee).

**Q: Do CTEs improve performance?**
A: Not inherently. In PostgreSQL ≥ 12, the optimizer can "inline" CTEs and optimize them as if they were subqueries. In PostgreSQL < 12, CTEs were optimization fences — always materialized. In SQL Server, you can use `WITH (NOEXPAND)`. Always check your engine.

**Q: CTE vs temp table — when does temp table win?**
A: When you need to reference the result many times (e.g., in multiple subsequent queries, not just once), or when you need to index the intermediate result. Temp tables materialize and can be indexed. CTEs may or may not materialize depending on the optimizer.

**Q: When would you use a recursive CTE?**
A: Hierarchy traversal — org charts, file system paths, category trees, network hops, alert escalation chains. At Citi: "Show me the full escalation chain from a base alert up to the management team" — that's a recursive CTE on an alert_hierarchy table.

**Q: What is the risk of recursive CTEs?**
A: Infinite loops from cycles in the data. Always add a depth limit: `WHERE level < 10` or `MAXRECURSION 100` (SQL Server). In production, also add cycle detection if the data might have genuine cycles.'''),

md('c09', '''## The Citi Angle

**The capacity pipeline above is a real pattern.** At Citi, the multi-step telemetry query was:
1. Filter last 90 days of raw APM data
2. Deduplicate (APM agents sometimes sent duplicate records)
3. Daily aggregates (avg, max, percentile)
4. Trend calculation (linear regression or 14-day moving average)
5. Flag at-risk: projected to exceed capacity in < 35 days

Without CTEs: a query with 4 nested subqueries, unreadable and untestable.
With CTEs: each step named, each step independently testable.

**Interview line:** *"At Citi, I wrote a 5-step CTE chain that processed 500M telemetry rows to identify capacity risks. The CTE structure meant each pipeline stage was readable and independently debuggable — critical when troubleshooting data quality issues in production."*

```sql
-- The debugging superpower: test any step in isolation
WITH deduped AS ( ... ),
daily_avg AS ( SELECT ... FROM deduped ... )
SELECT * FROM daily_avg LIMIT 100;  -- examine intermediate step
```'''),

]

write_nb(f'{BASE}/sql-ctes.ipynb', SQL_CTES_CELLS)
print(f'  Written: {BASE}/sql-ctes.ipynb')


# =============================================================================
# PYTHON — GENERATORS
# =============================================================================

PYTHON_GEN_CELLS = [

md('g01', '''# Python — Generators & List Comprehensions
**Day 1 — Python Module**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>Core Insight:</strong> Generators are <em>lazy</em> — they produce one value at a time instead
of building the whole result in memory. For data engineering with millions of rows, this is
the difference between crashing and streaming. A generator expression on 10 million items
uses ~200 bytes. A list comprehension uses ~80 MB.
</div>

### Why It Matters
In data pipelines, you rarely need all records in memory at once. You need to process them one at a time (or in chunks). Generators are Python's native streaming mechanism.'''),

md('g02', '''## List Comprehensions — Fast and Readable

```python
# Standard pattern: [expression for item in iterable if condition]
squares = [x**2 for x in range(10) if x % 2 == 0]
# → [0, 4, 16, 36, 64]

# Nested: flatten a 2D list
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
# → [1, 2, 3, 4, 5, 6]

# Dict comprehension
word_lengths = {word: len(word) for word in ["data", "engineer", "SQL"]}
# → {'data': 4, 'engineer': 8, 'SQL': 3}

# Set comprehension (deduplication)
unique_lengths = {len(word) for word in ["data", "engineer", "SQL", "cat"]}
# → {3, 4, 8}
```

**Rule:** Use list comprehension when you need the full list in memory at once (small data, or data you'll iterate multiple times). Use a generator when processing once in sequence.'''),

code('g03', '''# Memory comparison — list vs generator

import sys

# List comprehension: builds the entire list in memory
squares_list = [x**2 for x in range(10_000_000)]
print(f"List size:      {sys.getsizeof(squares_list):>15,} bytes")  # ~80 MB

# Generator expression: lazy, holds state only
squares_gen = (x**2 for x in range(10_000_000))
print(f"Generator size: {sys.getsizeof(squares_gen):>15,} bytes")   # ~208 bytes

# Both iterate identically — but generator can only go forward, once
total_gen  = sum(squares_gen)            # consumes the generator
total_list = sum(squares_list)           # list is reusable
print(f"Equal totals: {total_gen == total_list}")  # True'''),

md('g04', '''## Generator Functions — `yield`

A generator function uses `yield` instead of `return`. When called, it returns a generator object — an iterator that runs the function body up to the next `yield`, pauses, and resumes on the next call.

**Execution model:**
1. Call the function → get a generator object (nothing runs yet)
2. `next(gen)` → runs until `yield`, suspends, returns the yielded value
3. `next(gen)` → resumes from after `yield`, runs until next `yield`
4. When function returns (or falls off the end) → raises `StopIteration`'''),

code('g05', '''# Generator function — process a large file in chunks
# Never loads more than chunk_size rows into memory

def read_csv_chunks(filepath: str, chunk_size: int = 1000):
    """Yield lists of lines in chunks. Constant memory regardless of file size."""
    with open(filepath, encoding='utf-8') as f:
        chunk = []
        for line in f:
            chunk.append(line.rstrip())
            if len(chunk) == chunk_size:
                yield chunk        # pause, hand chunk to caller
                chunk = []         # reset — old chunk is GC'd
        if chunk:
            yield chunk            # yield the final partial chunk

# Usage: never more than 1000 rows in memory
# for chunk in read_csv_chunks("telemetry_10gb.csv", chunk_size=1000):
#     process_chunk(chunk)    # process 1000 rows, then release them

# Demonstrate with a simple counter generator
def counter_gen(n):
    """Yields 0, 1, 2, ..., n-1"""
    i = 0
    while i < n:
        yield i
        i += 1

gen = counter_gen(5)
print(next(gen))   # 0  — runs until yield, pauses
print(next(gen))   # 1
print(list(gen))   # [2, 3, 4] — consume the rest
# next(gen)        # → StopIteration (generator exhausted)'''),

code('g06', '''# Real pipeline: generator chaining
# Process a stream of server metrics without loading everything

def parse_line(line: str) -> dict:
    """Parse a CSV line into a metric dict."""
    parts = line.split(',')
    return {'server_id': parts[0], 'metric': parts[1], 'value': float(parts[2])}

def filter_high_cpu(records, threshold=80):
    """Generator: yield only records above threshold."""
    for rec in records:
        if rec['metric'] == 'cpu_pct' and rec['value'] > threshold:
            yield rec

def enrich_with_tier(records, server_tiers: dict):
    """Generator: add tier information to each record."""
    for rec in records:
        rec['tier'] = server_tiers.get(rec['server_id'], 'unknown')
        yield rec

# Chain generators — each step lazy, zero intermediate lists
# lines       = open("metrics.csv")              # lazy file read
# parsed      = (parse_line(l) for l in lines)   # lazy parse
# high_cpu    = filter_high_cpu(parsed, 80)       # lazy filter
# enriched    = enrich_with_tier(high_cpu, tiers) # lazy enrich
# results     = list(enriched)                    # materialize ONLY here

# This processes a 10GB file using only ~O(1) memory at each step.
print("Generator pipeline demo (no actual file needed)")
print("Each step is lazy — data flows one record at a time")'''),

md('g07', '''## itertools — Production-Grade Iteration

`itertools` provides lazy combinators for generators. Key tools for data engineering:'''),

code('g08', '''import itertools

# chain: combine multiple iterables lazily (no intermediate list)
servers   = ["srv-01", "srv-02", "srv-03"]
databases = ["db-01", "db-02"]
all_resources = list(itertools.chain(servers, databases))
print("chain:", all_resources)   # ['srv-01', 'srv-02', 'srv-03', 'db-01', 'db-02']

# islice: take the first N items from a generator (safe — doesn't exhaust it)
def infinite_counter(start=0):
    while True:
        yield start
        start += 1

first_five = list(itertools.islice(infinite_counter(100), 5))
print("islice:", first_five)    # [100, 101, 102, 103, 104]

# groupby: group consecutive items (sort first! groupby is NOT a SQL GROUP BY)
from itertools import groupby

data = sorted([
    ("production", "srv-01"), ("production", "srv-02"),
    ("staging",    "srv-03"), ("dev",        "srv-04"),
], key=lambda x: x[0])

for env, items in groupby(data, key=lambda x: x[0]):
    servers_in_env = [s for _, s in items]
    print(f"  {env}: {servers_in_env}")

# batched (Python 3.12+): split an iterable into batches of N
# For older Python, use islice in a loop:
def batched(iterable, n):
    it = iter(iterable)
    while batch := list(itertools.islice(it, n)):
        yield batch

for batch in batched(range(10), 3):
    print("batch:", batch)  # [0,1,2], [3,4,5], [6,7,8], [9]'''),

md('g09', '''## Interview Q&A

**Q: What's the difference between a list comprehension and a generator expression?**
A: A list comprehension `[x for x in ...]` builds the full list in memory immediately — eager evaluation. A generator expression `(x for x in ...)` is lazy — yields one value at a time. Use generators for large data where you only need one pass.

**Q: When does `yield` pause execution?**
A: Exactly at the `yield` statement. The function's local state (all variables, the position in the code) is saved. On the next `next()` call, execution resumes from the line after `yield`.

**Q: How would you process a 10GB CSV without loading it into memory?**
A: Use a generator that reads and yields rows (or chunks) one at a time. `pandas.read_csv(filepath, chunksize=1000)` is built on this exact pattern — it returns an iterator of DataFrames, each with 1000 rows.

**Q: What is a generator's key limitation vs a list?**
A: Generators are single-pass and forward-only. Once an element is yielded and consumed, you can't go back. If you need to iterate the data multiple times (e.g., compute mean, then compute variance), materialize to a list first — or use two separate generators.

**Q: What is `itertools.groupby` and what's the gotcha?**
A: `groupby` groups consecutive equal elements. The gotcha: it only groups consecutive items, not all items with the same key (unlike SQL GROUP BY). You **must sort by the grouping key first** or you'll get multiple groups for the same key.'''),

md('g10', '''## The Citi Angle

**At Citi, generators were the right tool for telemetry pipelines.** APM data from 6,000 servers generated millions of metric records per collection cycle. Loading everything into memory was never an option.

**The chunk-processing pattern:**
```python
def process_telemetry_file(path: str, batch_size: int = 5000):
    """Process telemetry CSV in memory-safe batches."""
    for chunk in read_csv_chunks(path, batch_size):
        # Each chunk is a list of 5000 lines
        records = [parse_metric(line) for line in chunk]
        records = [r for r in records if r['cpu_pct'] > 70]  # filter
        if records:
            insert_to_db(records)   # batch insert, not row-by-row
        # chunk goes out of scope, memory freed immediately
```

**Interview line:** *"For capacity data processing at Citi — 6,000 servers, millions of rows per cycle — Python generators were essential. The chunk pattern kept memory constant while processing arbitrarily large files. Same mental model as Spark's lazy execution: don't materialize until you have to."*'''),

]

write_nb(f'{BASE}/python-generators.ipynb', PYTHON_GEN_CELLS)
print(f'  Written: {BASE}/python-generators.ipynb')


# =============================================================================
# TECHNOLOGY — AWS DATA PLATFORM
# =============================================================================

AWS_CELLS = [

md('a01', '''# AWS Data Platform
**Day 1 — Technology & Architecture Module**

---

<div style="padding:15px;border-left:8px solid #667eea;background:#f0f0ff;border-radius:4px;">
<strong>Core Insight:</strong> AWS has three services that form the backbone of most modern data lakes:
S3 (store), Glue (catalog + transform), Athena (query). You can build a production
data platform with no servers to manage. Understanding how they fit together — and
their cost/performance tradeoffs — is what separates data engineers from data analysts.
</div>

### The Core Stack
```
Raw Data → S3 (data lake)  →  Glue Crawler  →  Glue Data Catalog
                                                       ↓
                                               Athena (SQL query)
                                                       ↓
                                       QuickSight / Jupyter / API Consumer
```'''),

md('a02', '''## S3 — The Foundation

S3 is an object store, not a file system. A "file path" like `s3://my-bucket/data/2026/02/27/file.parquet` is a **key string** — there are no actual folders, just key prefixes.

### Partitioning — Your First Performance Decision

```
s3://telemetry-lake/
  metrics/
    year=2026/
      month=02/
        day=27/
          part-0001.parquet
          part-0002.parquet
        day=28/
          ...
```

When Athena queries `WHERE year='2026' AND month='02'`, it skips all other partitions entirely. A 365-day dataset queried for 7 days = Athena reads ~2% of the data.

**Partition key rule:** Partition by the columns you filter on most. Date is almost always first. Environment (prod/dev), region, or customer tier often follow.

### Storage Classes (Cost vs Access Speed)

| Class | Use When | Retrieval |
|-------|---------|-----------|
| Standard | Hot data, frequent access | Instant |
| Standard-IA | 30+ days old, infrequent access | Instant, higher per-read |
| Glacier Instant | 90+ days old, occasional access | Instant, higher cost |
| Glacier Deep Archive | Multi-year cold archive | 12 hours |'''),

code('a03', '''# S3 with boto3 — common data engineering patterns

import boto3

s3 = boto3.client('s3')

# List partitions to understand data coverage
response = s3.list_objects_v2(
    Bucket='telemetry-lake',
    Prefix='metrics/year=2026/month=02/',
    Delimiter='/'        # treat as folder — list "subdirectories" only
)

for prefix in response.get('CommonPrefixes', []):
    print(prefix['Prefix'])   # metrics/year=2026/month=02/day=01/, day=02/, ...

# Upload a Parquet file with correct partition path
import pandas as pd
import io

df = pd.DataFrame({'server_id': ['srv-01'], 'cpu_pct': [75.2]})

buffer = io.BytesIO()
df.to_parquet(buffer, index=False)
buffer.seek(0)

s3.put_object(
    Bucket='telemetry-lake',
    Key='metrics/year=2026/month=02/day=27/batch_001.parquet',
    Body=buffer.getvalue()
)
print("Uploaded to S3 with partition path")'''),

md('a04', '''## Glue — Catalog + ETL

AWS Glue has two distinct functions:

**1. Glue Data Catalog:** A metadata store — tables, schemas, partition info. Athena reads from it. Redshift Spectrum reads from it. It's the central "yellow pages" for your data lake.

**2. Glue Crawlers:** Point at an S3 path → crawler scans the data → automatically creates/updates tables in the catalog. No schema definition needed for well-structured Parquet/CSV.

**3. Glue Jobs:** Managed Spark (PySpark) jobs. Pay per DPU-second. No cluster to spin up. Timeout-based cleanup.'''),

code('a05', '''# Glue Job (PySpark ETL) — production template
# Runs on managed Spark. No cluster management.

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pyspark.sql.functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'source_table', 'target_path'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from Glue Data Catalog (schema auto-detected by crawler)
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="telemetry_db",
    table_name=args['source_table'],
    push_down_predicate="year='2026' and month='02'"   # partition pruning
)

# Transform: filter high-CPU records, add processing timestamp
df = datasource.toDF()
df_filtered = (df
    .filter(F.col("cpu_utilization") > 80)
    .withColumn("processed_at", F.current_timestamp())
    .withColumn("alert_tier",
        F.when(F.col("cpu_utilization") > 95, "critical")
         .when(F.col("cpu_utilization") > 80, "warning")
         .otherwise("normal"))
)

# Write back as Parquet, partitioned by date
df_filtered.write.mode("overwrite").partitionBy("year", "month", "day") \\
    .parquet(args['target_path'])

job.commit()
print(f"Glue job complete. Wrote high-CPU records to {args['target_path']}")'''),

md('a06', '''## Athena — Serverless SQL on S3

Athena runs SQL directly on S3 files. No server, no cluster, no maintenance. **Pay per TB scanned.** This makes format and partitioning choices critical for cost.

### Cost Math

| Format | Compression | 1 TB uncompressed data | Athena query cost |
|--------|-------------|----------------------|------------------|
| CSV | None | 1 TB scanned | $5.00 |
| CSV | GZIP | ~250 GB scanned | $1.25 |
| Parquet | Snappy | ~100 GB scanned | $0.50 |
| Parquet + partitioning | Snappy | ~2 GB scanned (7-day filter) | $0.01 |

**Columnar = only read the columns you SELECT.** Parquet stores each column separately. A `SELECT server_id, avg_cpu FROM ...` on a 50-column table reads only 2 columns' worth of data.'''),

code('a07', '''-- Athena SQL — production patterns

-- 1. Partition pruning (critical for cost)
SELECT
    server_id,
    ROUND(AVG(cpu_utilization), 2) AS avg_cpu,
    MAX(cpu_utilization)           AS peak_cpu,
    COUNT(*)                       AS sample_count
FROM telemetry_db.server_metrics
WHERE year  = '2026'
  AND month = '02'              -- these are partition columns
  AND day   BETWEEN '20' AND '28'
  AND cpu_utilization > 80
GROUP BY server_id
ORDER BY avg_cpu DESC
LIMIT 100;

-- 2. Repair partitions after new data lands (if no auto-update)
MSCK REPAIR TABLE telemetry_db.server_metrics;

-- 3. Check what partitions exist
SHOW PARTITIONS telemetry_db.server_metrics;

-- 4. CTAS (Create Table As Select) — materialize a derived table
CREATE TABLE telemetry_db.high_cpu_monthly
WITH (
    format           = 'PARQUET',
    parquet_compression = 'SNAPPY',
    partitioned_by   = ARRAY['year', 'month'],
    external_location = 's3://telemetry-lake/high-cpu-monthly/'
) AS
SELECT
    server_id, year, month,
    ROUND(AVG(cpu_utilization), 2) AS avg_cpu
FROM telemetry_db.server_metrics
WHERE cpu_utilization > 80
GROUP BY server_id, year, month;'''),

md('a08', '''## The Full Architecture: APM → Data Lake

```
APM Agents (6,000 servers)
       │
       ▼
Amazon Kinesis Data Firehose
  - Buffers in-flight data
  - Auto-batches and writes to S3
  - Converts to Parquet (optional, with schema registry)
       │
       ▼
S3 Data Lake  (partitioned: year/month/day/env)
       │
       ├──→ AWS Glue Crawler
       │        Scans new partitions → updates Glue Data Catalog
       │
       ├──→ Glue ETL Jobs
       │        Transform + enrich → write derived tables back to S3
       │
       └──→ Amazon Athena
                Ad-hoc SQL queries
                Cost: pay per TB scanned (use Parquet + partitions)
                      │
                      ▼
              Amazon QuickSight (BI dashboards)
              Jupyter Notebooks (data science)
              API consumers (capacity planning services)
```

**Lake Formation:** Fine-grained access control layer on top of this stack. Column-level and row-level security. Relevant in regulated industries (finance, healthcare) — at Citi, this controls who can see which servers' data.'''),

md('a09', '''## Interview Q&A

**Q: What is a Glue Crawler?**
A: A managed job that scans S3 (or RDS, etc.) and automatically infers schema, creating or updating tables in the Glue Data Catalog. Point it at a bucket, run it on a schedule, and your catalog stays current with new partitions automatically.

**Q: What's the difference between Glue and EMR?**
A: Glue is serverless — no cluster to manage, pay per DPU-second. EMR gives you a full Hadoop/Spark cluster you control — more flexible, better for complex Spark tuning, but more ops overhead. Glue is faster to start with; EMR wins for heavy, custom workloads.

**Q: How does Athena pricing work and why does it matter?**
A: $5 per TB scanned. Columnar format (Parquet/ORC) + compression + partitioning can reduce what Athena actually reads by 90%+. A monthly report that scans 10 TB as CSV costs $50. The same report on Parquet with partitions might scan 200 GB and cost $1. Format choice is a cost engineering decision.

**Q: What is Lake Formation and when does it matter?**
A: Fine-grained access control for your data lake — column-level and row-level security on S3/Glue/Athena. At Citi, you'd use it to ensure only the network team can see network device data, while the application team can only see application server data — without separate copies of the data.

**Q: Design a pipeline to ingest server metrics from 6,000 endpoints into S3 for daily reporting.**
A: Agents push to Kinesis Firehose → Firehose batches and writes Parquet to S3 (partitioned by date + env) → Glue Crawler updates catalog → daily Glue job aggregates to summary tables → Athena for ad-hoc + QuickSight for dashboards. CloudWatch Events triggers daily Glue job. S3 lifecycle rules archive data older than 90 days to Glacier.'''),

md('a10', '''## The Citi Angle

**This stack solves exactly the Citi problem.** Managing 4 different APM tools (CA APM, AppDynamics, Dynatrace, BMC TrueSight) meant 4 different data formats, 4 different schemas, no unified view. The AWS data platform pattern solves this:

1. **Normalize:** Each APM tool's export goes through a Glue job that maps to a common schema
2. **Land:** All normalized data lands in S3 under the same partition structure
3. **Query:** Athena queries across all tools transparently — "show me the top 10 CPU consumers regardless of which APM monitors them"

**The quantified win:**
- Before: Monthly capacity report required 2 analyst-days of manual data collection and Excel aggregation
- After: Athena query + QuickSight dashboard → 2 hours automated, daily refresh

**Interview line:** *"At Citi, unifying 4 APM data sources into a single S3-based data lake with Athena on top was the architectural north star. The Glue + Athena stack gave us a single SQL interface across all our observability data. That's the same pattern I'd use for any APM ingestion problem."*'''),

]

write_nb(f'{BASE}/aws-data-platform.ipynb', AWS_CELLS)
print(f'  Written: {BASE}/aws-data-platform.ipynb')


print(f'''
Day 1 generation complete!
Output: {BASE}/

LeetCode notebooks + HTML:
  lc-0001-two-sum
  lc-0217-contains-duplicate
  lc-0242-valid-anagram
  lc-0238-product-except-self
  lc-0347-top-k-frequent

Concept notebooks:
  sql-ctes.ipynb
  python-generators.ipynb
  aws-data-platform.ipynb
''')
