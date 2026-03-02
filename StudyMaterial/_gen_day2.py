"""
Day 2 generator: Sliding Window | Advanced Window Functions | Pandas | Apache Spark
Output: D:/Workspace/StudyMaterial/Day2/

Files created:
  lc-0121-best-time-sell.ipynb / .html
  lc-0003-longest-substring.ipynb / .html
  lc-0424-char-replacement.ipynb / .html
  lc-0239-sliding-window-max.ipynb / .html
  lc-0076-minimum-window.ipynb / .html
  sql-window-functions-advanced.ipynb
  python-pandas.ipynb
  spark-architecture.ipynb
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/Workspace/StudyMaterial/Day2'
os.makedirs(BASE, exist_ok=True)

# ── notebook helpers ───────────────────────────────────────────────────────────

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

# ── HTML generation (Sliding Window theme) ────────────────────────────────────

SW_GRAD1  = '#11998e'
SW_GRAD2  = '#38ef7d'
SW_ACCENT = '#0a7a6b'

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_inline(text):
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def md_to_html(text, accent=SW_ACCENT):
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

    c_title   = get('cell-title')
    c_models  = get('cell-mental-models')
    c_complex = get('cell-complexity')
    c_optimal = get('cell-optimal-code')
    c_qa      = get('cell-qa')
    c_citi    = get('cell-citi-narrative')
    c_summary = get('cell-summary')

    diff_color = {'easy': '#155724', 'medium': '#856404', 'hard': '#721c24'}[difficulty]
    diff_bg    = {'easy': '#d4edda', 'medium': '#fff3cd', 'hard': '#f8d7da'}[difficulty]
    accent     = SW_ACCENT

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
            f'<div style="background:#e8faf5;border-left:5px solid {accent};padding:18px;border-radius:8px;">'
            + md_to_html(c_citi, accent) + '</div>'),
        section('🎯', 'Summary', md_to_html(c_summary, accent)),
    ])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LC #{num} \u2014 {title} \u2014 Sliding Window</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
       background: linear-gradient(135deg, {SW_GRAD1} 0%, {SW_GRAD2} 100%);
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
        font-family: 'Courier New', monospace; font-size: 0.88em; color: #0a7a6b; }}
pre code {{ background: none; color: #d4d4d4; padding: 0; font-size: 1em; }}
@media (max-width: 800px) {{
  div[style*="grid-template-columns:1fr 1fr"] {{ grid-template-columns: 1fr !important; }}
}}
</style>
</head>
<body>
<div class="container">
<h1>LC #{num} \u2014 {title} <span class="badge">{difficulty}</span></h1>
<p class="subtitle">Sliding Window Pattern &nbsp;|&nbsp; Day 2 Study Material</p>
{body}
</div>
</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  HTML: {html_path}')


# =============================================================================
# LC #121 — BEST TIME TO BUY AND SELL STOCK
# =============================================================================

BEST_TIME_CELLS = [

md('cell-title', '''# LC #121 — Best Time to Buy and Sell Stock
**Category:** Sliding Window / Two Pointers | **Difficulty:** Easy | **Day 2**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>The Problem:</strong> Given array <code>prices</code> where <code>prices[i]</code> is the stock price on day i,
return the maximum profit from one buy and one sell. Return 0 if no profit is possible.
</div>

**Examples:**
```
[7, 1, 5, 3, 6, 4] → 5   (buy at 1, sell at 6)
[7, 6, 4, 3, 1]    → 0   (prices only fall — no profit)
[1, 2]             → 1
```

**Core Insight:** For each potential sell day, the best buy is the *minimum price to its left*. Track the running minimum as you scan left-to-right. At each price, the potential profit is `current - min_so_far`.'''),

md('cell-mental-models', '''## Mental Models

**1. The Running Minimum**
As you scan left-to-right, maintain the lowest price seen so far. At each new price, calculate potential profit = `current - min_so_far`. Update the running max profit if higher.

**2. Sliding Window View**
The "window" implicitly spans from `min_price_index` to `current_index`. You never explicitly track the left pointer — the minimum tracks it for you.

**3. Time Series Analogy**
Identical pattern to: "For each day's CPU reading, what's the maximum improvement over any prior baseline?" Rolling maximum of (current - historical_min) is the same calculation.'''),

code('cell-brute-force', '''# Brute Force — O(n²) time, O(1) space
# Check every buy-sell pair.

def maxProfit_brute(prices):
    max_profit = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            max_profit = max(max_profit, prices[j] - prices[i])
    return max_profit

# Test
print(maxProfit_brute([7, 1, 5, 3, 6, 4]))   # 5
print(maxProfit_brute([7, 6, 4, 3, 1]))       # 0
print(maxProfit_brute([1, 2]))                 # 1'''),

md('cell-walkthrough', '''## Step-by-Step: One-Pass Approach

Trace through `[7, 1, 5, 3, 6, 4]`:

| Day | Price | min_price | profit = price - min | max_profit |
|-----|-------|-----------|---------------------|------------|
| 0 | 7 | 7 | 0 | 0 |
| 1 | 1 | **1** | 0 | 0 |
| 2 | 5 | 1 | **4** | 4 |
| 3 | 3 | 1 | 2 | 4 |
| 4 | 6 | 1 | **5** | **5** |
| 5 | 4 | 1 | 3 | 5 |

At day 4 we find the max: buy at 1 (day 1), sell at 6 (day 4) = profit 5.'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(1) space
# One pass: track min price and max profit simultaneously.

def maxProfit(prices: list[int]) -> int:
    min_price  = float('inf')
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price
        elif price - min_price > max_profit:
            max_profit = price - min_price

    return max_profit

# Test
print(maxProfit([7, 1, 5, 3, 6, 4]))   # 5
print(maxProfit([7, 6, 4, 3, 1]))       # 0
print(maxProfit([1, 2]))                # 1
print(maxProfit([2, 4, 1]))             # 2'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force (nested) | O(n²) | O(1) | Check every pair |
| **One-Pass (Optimal)** | **O(n)** | **O(1)** | Track running min |

**Why O(1) space?** Only two variables: `min_price` and `max_profit`. No data structure needed.

**Key constraint:** You must buy before you sell. Scanning left-to-right respects this — `min_price` is always from a prior day.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why is this categorized as sliding window?**
A: The window is the range [buy_day, sell_day]. The left boundary is the running minimum index (implicitly). The right boundary is the current day. Unlike explicit two-pointer sliding windows, we don't need to track both pointers — the min does it.

**Q: How would you modify this for "buy and sell multiple times"?**
A: LC #122 — Greedy: add all positive day-over-day differences. `sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))`.

**Q: How would you modify for "at most 2 transactions"?**
A: LC #123 — Track four states with DP: after first buy, after first sell, after second buy, after second sell.

**Q: What's the data engineering analog of this problem?**
A: "Find the maximum metric improvement over any prior baseline." Same algorithm — track rolling minimum, compute delta at each point.'''),

md('cell-citi-narrative', '''## The Citi Angle

**Direct capacity planning analog:** "What is the maximum performance headroom we ever had compared to our worst baseline in the past 30 days?"

```python
# Real pattern: rolling max improvement from historical low
readings = [72, 68, 75, 71, 80, 65, 88]   # daily avg CPU readings
baseline = float('inf')
max_headroom = 0

for cpu in readings:
    baseline = min(baseline, cpu)
    headroom = cpu - baseline   # how much headroom above historical low
    max_headroom = max(max_headroom, headroom)

print(f"Max usage swing from baseline: {max_headroom}%")
```

**Interview tie-in:** "The buy-sell pattern is identical to finding the maximum metric delta from a rolling baseline — a capacity planning calculation I did regularly at Citi to understand usage volatility."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Sliding Window / Running Minimum |
| **Time** | O(n) |
| **Space** | O(1) |
| **Key insight** | `profit = current_price - min_price_so_far` |
| **Say in interview** | "One pass: track running minimum and max profit. O(n) time, O(1) space." |

**The 3-line core:**
```python
for price in prices:
    min_price = min(min_price, price)
    max_profit = max(max_profit, price - min_price)
```'''),

]

write_nb(f'{BASE}/lc-0121-best-time-sell.ipynb', BEST_TIME_CELLS)
gen_html('lc-0121-best-time-sell', f'{BASE}/lc-0121-best-time-sell.ipynb',
         f'{BASE}/lc-0121-best-time-sell.html', 121, 'Best Time to Buy and Sell Stock', 'easy')


# =============================================================================
# LC #3 — LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS
# =============================================================================

LONGEST_SUB_CELLS = [

md('cell-title', '''# LC #3 — Longest Substring Without Repeating Characters
**Category:** Sliding Window + HashSet | **Difficulty:** Medium | **Day 2**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>The Problem:</strong> Given string <code>s</code>, return the length of the longest substring
without repeating characters.
</div>

**Examples:**
```
"abcabcbb" → 3   ("abc")
"bbbbb"    → 1   ("b")
"pwwkew"   → 3   ("wke")
""         → 0
```

**Core Insight:** Two pointers. Right expands to grow the window. When a repeat is found, jump left pointer past the previous occurrence of that character — not just one step, but directly to `prev_index + 1`.'''),

md('cell-mental-models', '''## Mental Models

**1. The Valid Window**
A window `[left, right]` is valid if all characters within it are unique. Expanding right may invalidate it. Shrinking left restores validity.

**2. Jump Left, Don't Shuffle**
When we see a repeat at position `right`, we don't shrink left one step at a time. We jump left to `char_index[char] + 1` — past the previous occurrence. This is what makes it O(n) rather than O(n²).

**3. Why Store Index (Not Just Membership)?**
If we only tracked whether a char is in the window (set membership), we'd have to shrink one step at a time. Storing the index lets us jump directly.'''),

code('cell-brute-force', '''# Brute Force — O(n³) time, O(min(n,m)) space
# Check every substring for uniqueness.

def lengthOfLongestSubstring_brute(s: str) -> int:
    max_len = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if len(s[i:j]) == len(set(s[i:j])):   # all unique?
                max_len = max(max_len, j - i)
    return max_len

# Test
print(lengthOfLongestSubstring_brute("abcabcbb"))   # 3
print(lengthOfLongestSubstring_brute("bbbbb"))      # 1
print(lengthOfLongestSubstring_brute("pwwkew"))     # 3'''),

md('cell-walkthrough', '''## Step-by-Step: Sliding Window

Trace through `"abcabcbb"` with `char_index = {}`, `left = 0`:

| right | char | char_index | In window? | Action | window | max_len |
|-------|------|-----------|-----------|--------|--------|---------|
| 0 | a | {a:0} | No | add | [a] | 1 |
| 1 | b | {a:0,b:1} | No | add | [ab] | 2 |
| 2 | c | {a:0,b:1,c:2} | No | add | [abc] | 3 |
| 3 | a | {a:3,b:1,c:2} | Yes (idx 0 ≥ left 0) | left=1 | [bca] | 3 |
| 4 | b | {a:3,b:4,c:2} | Yes (idx 1 ≥ left 1) | left=2 | [cab] | 3 |
| ... | | | | | | 3 |

When `a` repeats at right=3: left jumps from 0 to 1 (past old a). Window stays valid.'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(min(n,m)) space
# Sliding window with char→index map for O(1) jumps.

def lengthOfLongestSubstring(s: str) -> int:
    char_index = {}   # char → most recent index
    left = 0
    max_len = 0

    for right, char in enumerate(s):
        # If char is in window (index >= left), jump left past it
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)

    return max_len

# Test
print(lengthOfLongestSubstring("abcabcbb"))   # 3
print(lengthOfLongestSubstring("bbbbb"))      # 1
print(lengthOfLongestSubstring("pwwkew"))     # 3
print(lengthOfLongestSubstring(""))           # 0
print(lengthOfLongestSubstring("au"))         # 2'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Brute Force | O(n³) | O(min(n,m)) | Build+check every substring |
| Sliding Window (set) | O(n) | O(min(n,m)) | But shrinks one step at a time |
| **Sliding Window + index map** | **O(n)** | **O(min(n,m))** | Jumps left directly |

**Space note:** `m` = size of the character set. For ASCII: 128. For Unicode: up to thousands. In practice, the map never holds more than `min(n, charset_size)` entries.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why check `char_index[char] >= left`?**
A: A character might be in `char_index` but its stored index is to the left of the current window. We only care about repeats *within the current window*. If the stored index is before `left`, this character isn't actually in our window — it's safe to ignore.

**Q: What's the difference between using a set vs a dict here?**
A: Set gives O(1) membership testing but you'd need to shrink left one step at a time (O(n) per shrink in worst case = O(n²) total). Dict stores the index, enabling O(1) jumps.

**Q: What's `min(n, m)` in the space complexity?**
A: `n` = string length, `m` = character set size. The map holds at most the smaller of the two — you can't have more unique chars in the window than the entire string has, and you can't exceed the alphabet size.

**Q: What changes for Unicode vs ASCII?**
A: Only the constant in space complexity. The algorithm is the same.'''),

md('cell-citi-narrative', '''## The Citi Angle

**The "longest run of unique values" pattern:** In telemetry streams, you often need the longest consecutive sequence of distinct server IDs (deduplication run), distinct metric types, or distinct alert codes.

```python
# Longest run of distinct servers in a streaming event log
events = ["srv-01", "srv-02", "srv-01", "srv-03", "srv-04", "srv-02"]
server_idx = {}
left = 0
max_run = 0

for right, server in enumerate(events):
    if server in server_idx and server_idx[server] >= left:
        left = server_idx[server] + 1
    server_idx[server] = right
    max_run = max(max_run, right - left + 1)

print(f"Longest run of distinct servers: {max_run}")   # 3
```

**Interview tie-in:** "The sliding window with a hash map is the pattern for any contiguous-window uniqueness problem. I've applied this to detect the longest clean sequence in a telemetry stream before a repeated alert fired."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Sliding Window + HashMap (char → last index) |
| **Time** | O(n) |
| **Space** | O(min(n, charset)) |
| **Key line** | `if char in char_index and char_index[char] >= left: left = char_index[char] + 1` |
| **Say in interview** | "HashMap stores last index of each char. Jump left past the previous occurrence in O(1)." |

**The window invariant:** `s[left:right+1]` always contains unique characters.'''),

]

write_nb(f'{BASE}/lc-0003-longest-substring.ipynb', LONGEST_SUB_CELLS)
gen_html('lc-0003-longest-substring', f'{BASE}/lc-0003-longest-substring.ipynb',
         f'{BASE}/lc-0003-longest-substring.html', 3, 'Longest Substring Without Repeating Characters', 'medium')


# =============================================================================
# LC #424 — LONGEST REPEATING CHARACTER REPLACEMENT
# =============================================================================

CHAR_REPLACE_CELLS = [

md('cell-title', '''# LC #424 — Longest Repeating Character Replacement
**Category:** Sliding Window + HashMap | **Difficulty:** Medium | **Day 2**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>The Problem:</strong> Given string <code>s</code> and integer <code>k</code>,
return the length of the longest substring containing the same letter after at most <code>k</code>
character replacements.
</div>

**Examples:**
```
"AABABBA", k=1 → 4  ("AABA" or "ABBB": replace one B → AAAA, length 4)
"ABAB",    k=2 → 4  (replace both Bs → "AAAA")
"AAAA",    k=0 → 4
```

**Core Insight:** A window is valid if `(window_size - max_count_in_window) ≤ k`. The left term counts how many characters would need to be replaced. If that's ≤ k, we can make the whole window uniform.'''),

md('cell-mental-models', '''## Mental Models

**1. The Validity Formula**
`replacements_needed = window_size - count_of_most_frequent_char`
If `replacements_needed ≤ k`, the window is valid. This is the invariant.

**2. Why We Don't Update max_count on Shrink**
We only want the maximum valid window ever seen. `max_count` never decreases. Even if the most frequent char leaves the window, we don't shrink `max_count` — this can only prevent us from growing the window, not from finding a larger valid window later.

**3. The Sliding Window Contract**
Right pointer expands. When the window becomes invalid, left pointer moves up by exactly 1 (not until valid again). This maintains O(n) total movement.'''),

code('cell-brute-force', '''# Brute Force — O(n²) per window, O(1) per check
from collections import Counter

def characterReplacement_brute(s: str, k: int) -> int:
    max_len = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            window = s[i:j]
            most_common_count = Counter(window).most_common(1)[0][1]
            if len(window) - most_common_count <= k:
                max_len = max(max_len, len(window))
    return max_len

print(characterReplacement_brute("AABABBA", 1))  # 4
print(characterReplacement_brute("ABAB", 2))     # 4'''),

md('cell-walkthrough', '''## Why We Never Decrease max_count

Consider `"AABABBA"`, k=1:

Key insight: `max_count` tracks the best frequency we've seen in *any* window state.
- When we shrink left, max_count doesn't decrease.
- This means the window can only *stay the same size or grow* — we're searching for the maximum.
- If the actual max_count in the current window is less than stored max_count, the window is "artificially" large — but we just move left by 1, maintaining the search.

This is a valid optimization because we're looking for the largest window, not validating all windows.'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(1) space (at most 26 distinct chars)

def characterReplacement(s: str, k: int) -> int:
    count = {}
    left = 0
    max_count = 0   # max frequency of any single char in current window
    result = 0

    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_count = max(max_count, count[s[right]])

        # Characters to replace = window_size - most_frequent_count
        # If > k, shrink by 1 from left
        if (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1

        result = max(result, right - left + 1)

    return result

# Test
print(characterReplacement("AABABBA", 1))   # 4
print(characterReplacement("ABAB", 2))       # 4
print(characterReplacement("AAAA", 0))       # 4
print(characterReplacement("A", 0))          # 1'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n² × 26) | O(26) |
| **Sliding Window** | **O(n)** | **O(26) = O(1)** |

**Why O(1) space?** `count` can have at most 26 keys (uppercase English letters). That's a fixed-size map.

**Why O(n) time?** Left and right each move at most n steps total. The inner operations (update count, max_count) are O(1). Total: O(n).'''),

md('cell-qa', '''## Interview Q&A

**Q: Why don't we decrement max_count when shrinking the window?**
A: We're looking for the *maximum length*, so max_count should reflect the best window we've ever seen. If we shrink past the max-count character, the window is now "conservatively" sized — we'll grow it again when we find a better character. Keeping max_count high prevents us from mistakenly invalidating a window that's the same size as our target.

**Q: Is the window always valid?**
A: No — the window may temporarily be invalid (when we shrink left, we don't shrink until valid). The key insight: we're searching for the maximum window, so we only grow and move right by 1. We never shrink below the current max.

**Q: What changes if characters are lowercase or Unicode?**
A: The count map grows, but the algorithm is identical. Space would be O(charset_size) — still effectively O(1) for bounded alphabets.

**Q: Time-series analogy?**
A: "Longest period where a metric stayed within k standard deviations of its dominant value" — same invariant: (window_size - count_of_dominant_state) ≤ k.'''),

md('cell-citi-narrative', '''## The Citi Angle

**The "dominant state window" pattern:** How long did a server remain in a predominantly "healthy" state, tolerating up to k anomalous readings?

```python
# Longest stretch where srv-01 was "healthy" with at most 1 spike
states = ["H","H","S","H","H","S","S","H","H","H"]  # H=healthy, S=spike
k = 1

count = {}
left = 0
max_count = 0
longest_healthy = 0

for right, state in enumerate(states):
    count[state] = count.get(state, 0) + 1
    max_count = max(max_count, count[state])
    if (right - left + 1) - max_count > k:
        count[states[left]] -= 1
        left += 1
    longest_healthy = max(longest_healthy, right - left + 1)

print(f"Longest predominantly-healthy window: {longest_healthy} readings")
```

**Interview tie-in:** "Character replacement maps directly to alert tolerance windows — the longest period a server was in a dominant state, tolerating at most k deviations. That's a real capacity planning metric."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Sliding Window + frequency map |
| **Time** | O(n) |
| **Space** | O(26) = O(1) |
| **Invariant** | `(right - left + 1) - max_count ≤ k` |
| **Say in interview** | "Window valid if (size - max_freq) ≤ k. Expand right, shrink left by 1 when invalid. max_count never decreases." |'''),

]

write_nb(f'{BASE}/lc-0424-char-replacement.ipynb', CHAR_REPLACE_CELLS)
gen_html('lc-0424-char-replacement', f'{BASE}/lc-0424-char-replacement.ipynb',
         f'{BASE}/lc-0424-char-replacement.html', 424, 'Longest Repeating Character Replacement', 'medium')


# =============================================================================
# LC #239 — SLIDING WINDOW MAXIMUM
# =============================================================================

SLIDE_WIN_MAX_CELLS = [

md('cell-title', '''# LC #239 — Sliding Window Maximum
**Category:** Deque (Monotonic Queue) | **Difficulty:** Hard | **Day 2**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>The Problem:</strong> Given array <code>nums</code> and integer <code>k</code>, return an array
of the maximum value in each sliding window of size k.
</div>

**Examples:**
```
nums = [1,3,-1,-3,5,3,6,7], k=3 → [3,3,5,5,6,7]
nums = [1],                  k=1 → [1]
nums = [1,-1],               k=1 → [1,-1]
```

**Core Insight:** Maintain a **monotonic decreasing deque** of indices. The front always holds the index of the current window's maximum. Remove from the front when that index falls out of the window. Remove from the back when a larger element enters (those smaller elements can never become the max).'''),

md('cell-mental-models', '''## Mental Models

**1. The Monotonic Deque as a "Useful Candidates" List**
Only elements that could become the window max are worth keeping. If element `b` is smaller than and to the left of element `a`, then `b` can never be the max while `a` is in the window. Remove `b`.

**2. Deque Front = Current Max**
The deque is maintained in decreasing order of values (indices stored). The front index always points to the current window's maximum.

**3. Two Operations**
- Left cleanup: Pop front if its index is outside the window (`dq[0] < i - k + 1`)
- Right cleanup: Pop back while `nums[back] < nums[current]` (smaller elements are useless)

**4. Amortized O(n)**
Each element is added and removed from the deque at most once — so despite inner while loops, total work is O(n).'''),

code('cell-brute-force', '''# Brute Force — O(n*k) time
def maxSlidingWindow_brute(nums, k):
    result = []
    for i in range(len(nums) - k + 1):
        result.append(max(nums[i:i+k]))
    return result

print(maxSlidingWindow_brute([1,3,-1,-3,5,3,6,7], 3))   # [3,3,5,5,6,7]
print(maxSlidingWindow_brute([1], 1))                    # [1]'''),

md('cell-walkthrough', '''## Trace: `[1,3,-1,-3,5,3,6,7]`, k=3

| i | num | Front cleanup | Back cleanup | dq (indices) | Window | Result |
|---|-----|--------------|-------------|-------------|--------|--------|
| 0 | 1 | — | — | [0] | — | — |
| 1 | 3 | — | pop 0 (1<3) | [1] | — | — |
| 2 | -1 | — | -1<3, keep | [1,2] | full | **3** |
| 3 | -3 | — | -3<-1, keep | [1,2,3] | drop 0 → [1,2,3] | **3** |
| 4 | 5 | pop 1 (out) | pop 3,2 | [4] | | **5** |
| 5 | 3 | — | 3<5, keep | [4,5] | | **5** |
| 6 | 6 | — | pop 5,4 | [6] | | **6** |
| 7 | 7 | — | pop 6 | [7] | | **7** |'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(k) space
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    dq = deque()   # stores indices, values are decreasing
    result = []

    for i, num in enumerate(nums):
        # Remove indices outside the current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove indices whose values are smaller than current (they\'re useless)
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Window is full — record the max (front of deque)
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result

# Test
print(maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3))   # [3,3,5,5,6,7]
print(maxSlidingWindow([1], 1))                    # [1]
print(maxSlidingWindow([9,11], 2))                 # [11]
print(maxSlidingWindow([4,-2], 2))                 # [4]'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n×k) | O(1) |
| **Monotonic Deque** | **O(n)** | **O(k)** |

**Why O(n) despite inner loops?** Each element enters and exits the deque at most once. Amortized, the total number of push+pop operations across all iterations is ≤ 2n.

**Why O(k) space?** The deque holds at most k indices at any time (one window's worth).'''),

md('cell-qa', '''## Interview Q&A

**Q: Why store indices instead of values in the deque?**
A: We need to check if the front element has fallen outside the window. Comparing indices to `i - k + 1` requires the index, not the value.

**Q: What makes this "monotonic"?**
A: The values corresponding to indices in the deque are always in decreasing order. We maintain this monotonic property by removing smaller elements from the back on every insertion.

**Q: Real-world use case?**
A: Rolling maximum of a time series — "what was the peak CPU in the last 5 minutes?" With streaming data arriving per-second, this runs in O(1) per new reading rather than O(k) per reading.

**Q: How would you adapt this for rolling minimum?**
A: Flip the comparison: remove from back when `nums[dq[-1]] > num` (maintain increasing order). Front will always be the minimum.'''),

md('cell-citi-narrative', '''## The Citi Angle

**Direct application: rolling peak CPU detection.**

```python
# Rolling maximum CPU over a k-window — O(n) with monotonic deque
from collections import deque

def rolling_peak(readings: list[float], window: int) -> list[float]:
    """Returns peak CPU for each window position. O(n) time."""
    dq = deque()
    peaks = []
    for i, cpu in enumerate(readings):
        while dq and dq[0] < i - window + 1:
            dq.popleft()
        while dq and readings[dq[-1]] < cpu:
            dq.pop()
        dq.append(i)
        if i >= window - 1:
            peaks.append(readings[dq[0]])
    return peaks

# 6 hourly CPU readings, 3-hour rolling peak
readings = [72.1, 68.5, 81.3, 75.0, 90.2, 88.7, 65.4]
print("Rolling 3-hour peak CPU:", rolling_peak(readings, 3))
```

**Interview tie-in:** "At Citi, identifying the peak CPU in a rolling window was a core capacity alert. The monotonic deque gives O(n) — critical for streaming telemetry where n grows continuously."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Monotonic Deque |
| **Time** | O(n) amortized |
| **Space** | O(k) |
| **Deque invariant** | Values are decreasing (indices stored; front = current max) |
| **Say in interview** | "Monotonic deque: remove expired front, remove smaller elements from back. Front is always the window max. Each element enters and exits at most once — O(n) amortized." |'''),

]

write_nb(f'{BASE}/lc-0239-sliding-window-max.ipynb', SLIDE_WIN_MAX_CELLS)
gen_html('lc-0239-sliding-window-max', f'{BASE}/lc-0239-sliding-window-max.ipynb',
         f'{BASE}/lc-0239-sliding-window-max.html', 239, 'Sliding Window Maximum', 'hard')


# =============================================================================
# LC #76 — MINIMUM WINDOW SUBSTRING
# =============================================================================

MIN_WIN_CELLS = [

md('cell-title', '''# LC #76 — Minimum Window Substring
**Category:** Sliding Window + HashMap | **Difficulty:** Hard | **Day 2**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>The Problem:</strong> Given strings <code>s</code> and <code>t</code>, return the minimum window
substring of <code>s</code> that contains all characters of <code>t</code>.
</div>

**Examples:**
```
s = "ADOBECODEBANC", t = "ABC" → "BANC"
s = "a",             t = "a"  → "a"
s = "a",             t = "aa" → ""  (can't satisfy)
```

**Core Insight:** Expand right until the window contains all required characters (valid). Then shrink left as much as possible while still valid. Record the minimum. Repeat.'''),

md('cell-mental-models', '''## Mental Models

**1. The "Have / Required" Counter**
`required` = number of *distinct* characters in `t` that must be satisfied (each at the right count).
`have` = number of those characters currently satisfied in the window.
Window is valid when `have == required`.

**2. Satisfy vs Over-satisfy**
Satisfying means meeting exactly the required count — not exceeding it. If `t = "AA"`, the window must have at least 2 A's. Having 3 still satisfies (we only track when we reach *exactly* the needed count from below).

**3. Expand-then-Shrink Cycle**
Right expands until valid → record window → shrink left until invalid → right expands again. This two-pointer dance covers all candidate windows in O(n+m).'''),

code('cell-brute-force', '''# Brute Force — O(n² * m) where m = len(t)
from collections import Counter

def minWindow_brute(s: str, t: str) -> str:
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            window = Counter(s[i:j])
            # Check if window contains all of t
            if all(window[c] >= need[c] for c in need):
                if not best or j - i < len(best):
                    best = s[i:j]
    return best

print(minWindow_brute("ADOBECODEBANC", "ABC"))   # BANC
print(minWindow_brute("a", "a"))                  # a'''),

md('cell-walkthrough', '''## The Two-Pointer Strategy

```
s = "ADOBECODEBANC", t = "ABC"
need = {A:1, B:1, C:1}   required = 3

Phase 1 — Expand right until have == 3:
A→D→O→B→E→C  → window "ADOBEC", have=3 ✓

Phase 2 — Shrink left while have == 3:
Remove A → "DOBEC", have=2  ✗  →  record "ADOBEC" (len=6)

Phase 3 — Continue expanding right:
O→D→E→B → "DOBECODEB", have=2
→ A → "DOBECODEBAN", have=2
→ N → "DBECODEBANCB"...
→ C → "DOBECODEBANCB"... have=3 ✓

Shrink left:
D,O,B,E,C,O,D,E → "BANC" still has A,B,C → have=3 ✓ → record "BANC" (len=4) ✓
B removed → have=2 ✗

Final result: "BANC"
```'''),

code('cell-optimal-code', '''# Optimal — O(n+m) time, O(m) space
from collections import Counter

def minWindow(s: str, t: str) -> str:
    if not t or not s:
        return ""

    need = Counter(t)          # required freq for each char in t
    have, required = 0, len(need)
    left = 0
    result = ""
    window = {}

    for right, char in enumerate(s):
        window[char] = window.get(char, 0) + 1
        # Check if adding char satisfied its requirement (exactly met, not exceeded)
        if char in need and window[char] == need[char]:
            have += 1

        # Shrink left as long as window is valid
        while have == required:
            window_size = right - left + 1
            if not result or window_size < len(result):
                result = s[left:right+1]
            # Remove leftmost char
            left_char = s[left]
            window[left_char] -= 1
            if left_char in need and window[left_char] < need[left_char]:
                have -= 1
            left += 1

    return result

# Test
print(minWindow("ADOBECODEBANC", "ABC"))   # BANC
print(minWindow("a", "a"))                  # a
print(minWindow("a", "aa"))                 # (empty — can\'t satisfy)
print(minWindow("aa", "aa"))               # aa'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n² × m) | O(m) |
| **Sliding Window** | **O(n + m)** | **O(m)** |

**O(n+m):** We scan `s` once (O(n)) and build `need` from `t` (O(m)). Each character in `s` is added and removed from the window at most once.

**O(m) space:** `need` holds |t| unique characters. `window` holds at most |s| keys in the worst case.'''),

md('cell-qa', '''## Interview Q&A

**Q: What does `have` track exactly?**
A: The number of distinct characters from `t` whose count in the current window meets or exceeds the required count. When `have == required`, every character in `t` is satisfied.

**Q: Why check `window[char] == need[char]` (not `>=`)?**
A: We only increment `have` when we *first* reach the required count. If we already exceeded it, adding another copy doesn't increment `have` again (avoiding double-counting).

**Q: Why decrement `have` when `window[left_char] < need[left_char]`?**
A: When removing the left char drops its count *below* required, we've un-satisfied that character. `have` decrements to signal the window is no longer valid.

**Q: What's the general two-pointer template?**
A: Expand right to reach valid → record result → shrink left until invalid → repeat. This template works for minimum window, maximum window with constraint, etc.'''),

md('cell-citi-narrative', '''## The Citi Angle

**The "minimum covering set" pattern:** Find the shortest time window that contains at least one occurrence of every required metric type.

```python
from collections import Counter

# Minimum time window containing all required alert types
event_stream = ["cpu","mem","cpu","disk","net","cpu","mem","disk"]
required_types = ["cpu", "mem", "disk"]

events = list(enumerate(event_stream))  # (index, type)
need = Counter(required_types)
have, req = 0, len(need)
left = 0
window_counts = {}
min_window = None

for right, etype in events:
    window_counts[etype] = window_counts.get(etype, 0) + 1
    if etype in need and window_counts[etype] == need[etype]:
        have += 1
    while have == req:
        if min_window is None or right - left < min_window[1] - min_window[0]:
            min_window = (left, right)
        ltype = event_stream[left]
        window_counts[ltype] -= 1
        if ltype in need and window_counts[ltype] < need[ltype]:
            have -= 1
        left += 1

print(f"Minimum window: indices {min_window[0]}-{min_window[1]}")
print(f"Events: {event_stream[min_window[0]:min_window[1]+1]}")
```

**Interview tie-in:** "Minimum window substring is the pattern for finding the shortest time period covering all required event types — a real diagnostic tool for root cause analysis."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Sliding Window + HashMap (char counts) |
| **Time** | O(n + m) |
| **Space** | O(m) |
| **Key tracking** | `have` = satisfied chars; `required` = distinct chars in t |
| **Say in interview** | "Expand right until have==required (valid). Shrink left while still valid, recording minimum. have tracks distinct-char satisfaction, not total chars." |'''),

]

write_nb(f'{BASE}/lc-0076-minimum-window.ipynb', MIN_WIN_CELLS)
gen_html('lc-0076-minimum-window', f'{BASE}/lc-0076-minimum-window.ipynb',
         f'{BASE}/lc-0076-minimum-window.html', 76, 'Minimum Window Substring', 'hard')


# =============================================================================
# SQL — ADVANCED WINDOW FUNCTIONS
# =============================================================================

SQL_WINDOW_CELLS = [

code('w00-setup', '''import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript("""
CREATE TABLE server_daily_summary (
    server_id TEXT,
    collection_date TEXT,
    avg_cpu REAL,
    region TEXT
);
INSERT INTO server_daily_summary VALUES
    ('srv-01','2026-02-01',72.5,'us-east'),
    ('srv-01','2026-02-02',74.1,'us-east'),
    ('srv-01','2026-02-03',68.9,'us-east'),
    ('srv-01','2026-02-04',79.3,'us-east'),
    ('srv-01','2026-02-05',85.2,'us-east'),
    ('srv-01','2026-02-06',71.0,'us-east'),
    ('srv-01','2026-02-07',88.4,'us-east'),
    ('srv-02','2026-02-01',45.2,'us-east'),
    ('srv-02','2026-02-02',48.1,'us-east'),
    ('srv-02','2026-02-03',51.3,'us-east'),
    ('srv-02','2026-02-04',47.9,'us-east'),
    ('srv-02','2026-02-05',44.0,'us-east'),
    ('srv-02','2026-02-06',52.7,'us-east'),
    ('srv-02','2026-02-07',49.8,'us-east'),
    ('srv-03','2026-02-01',91.3,'us-west'),
    ('srv-03','2026-02-02',88.7,'us-west'),
    ('srv-03','2026-02-03',92.1,'us-west'),
    ('srv-03','2026-02-04',89.5,'us-west'),
    ('srv-03','2026-02-05',95.0,'us-west'),
    ('srv-03','2026-02-06',90.3,'us-west'),
    ('srv-03','2026-02-07',93.8,'us-west'),
    ('srv-04','2026-02-01',33.1,'us-west'),
    ('srv-04','2026-02-02',35.5,'us-west'),
    ('srv-04','2026-02-03',31.8,'us-west'),
    ('srv-04','2026-02-04',38.2,'us-west'),
    ('srv-04','2026-02-05',36.9,'us-west'),
    ('srv-04','2026-02-06',34.4,'us-west'),
    ('srv-04','2026-02-07',37.1,'us-west');
""")
print("Sample database ready!")
print("Table: server_daily_summary (28 rows, 4 servers, 7 days)")
print()
print(pd.read_sql_query("SELECT * FROM server_daily_summary LIMIT 6", conn).to_string(index=False))'''),

md('w01', '''# SQL — Advanced Window Functions
**Day 2 — SQL Module**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>Core Insight:</strong> You know ROW_NUMBER, RANK, LAG/LEAD, and rolling aggregates.
What separates senior candidates: NTILE, PERCENT_RANK, FIRST_VALUE/LAST_VALUE,
and named WINDOW clauses. These show up in business analytics — quartile ranking,
percentile scoring, baseline comparison, and DRY SQL.
</div>

**Reminder:** Window functions keep all rows. GROUP BY collapses rows. This is the fundamental difference.'''),

md('w02', '''## NTILE — Quartile / Bucket Analysis

`NTILE(n)` divides the result set into n equally-sized buckets, numbered 1 to n.
- Bucket 1 = highest (if ORDER BY DESC)
- Most common use: quartile analysis (n=4), decile analysis (n=10)
- Handles uneven divisions: earlier buckets get +1 row when n doesn't divide evenly'''),

code('w03', '''# NTILE: divide servers into 4 quartiles by average CPU (using first day only for clarity)
sql_ntile = """
SELECT
    server_id,
    ROUND(AVG(avg_cpu), 2) AS avg_cpu_overall,
    NTILE(4) OVER (ORDER BY AVG(avg_cpu) DESC) AS quartile
FROM server_daily_summary
GROUP BY server_id
ORDER BY avg_cpu_overall DESC
"""

result = pd.read_sql_query(sql_ntile, conn)
print("Server CPU Quartile Analysis (Q1=highest, Q4=lowest):")
print(result.to_string(index=False))
print()
print("NTILE(4): divides rows into 4 equal buckets. With 4 servers, each gets 1.")
print("With 10 servers and NTILE(4): buckets would be 3,3,2,2 rows each.")'''),

md('w04', '''## PERCENT_RANK and CUME_DIST

**PERCENT_RANK:** `(rank - 1) / (total_rows - 1)` — always 0 for first row, 1 for last
**CUME_DIST:** `rows_leq_current / total_rows` — fraction of rows ≤ current value

> **Note:** PERCENT_RANK and CUME_DIST require SQLite 3.44.0+ (Nov 2023).
> The cell below uses pandas to simulate these for maximum compatibility.'''),

code('w05', '''# PERCENT_RANK and CUME_DIST simulation using pandas
# (equivalent to what you would write in production SQL)

df = pd.read_sql_query("""
    SELECT server_id, ROUND(AVG(avg_cpu),2) AS avg_cpu
    FROM server_daily_summary GROUP BY server_id ORDER BY avg_cpu
""", conn)

n = len(df)
df = df.sort_values('avg_cpu').reset_index(drop=True)
df['rank'] = df['avg_cpu'].rank(method='min').astype(int)
df['percent_rank'] = ((df['rank'] - 1) / (n - 1)).round(3)
df['cume_dist'] = (df['avg_cpu'].rank(method='max') / n).round(3)

print("PERCENT_RANK and CUME_DIST simulation:")
print(df.to_string(index=False))
print()
print("PERCENT_RANK: (rank-1)/(n-1) — first=0, last=1")
print("CUME_DIST:    rows<=current/n — always > 0")
print()
print("In SQL (requires SQLite 3.44+ or PostgreSQL/Snowflake/DuckDB):")
print("""
SELECT server_id, avg_cpu,
    ROUND(PERCENT_RANK() OVER (ORDER BY avg_cpu) * 100, 1) AS percentile,
    ROUND(CUME_DIST()    OVER (ORDER BY avg_cpu) * 100, 1) AS cumulative_pct
FROM server_daily_summary;
""")'''),

md('w06', '''## FIRST_VALUE / LAST_VALUE — Baseline Comparison

Compare each row to the first (or last) value in its partition:
- `FIRST_VALUE(col) OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)` — first value in partition
- **LAST_VALUE gotcha:** Default frame is up to current row. You must explicitly set `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING` to get the true last value.'''),

code('w07', '''# FIRST_VALUE: compare each day's CPU to the first day of the week (baseline)
sql_first = """
SELECT
    server_id,
    collection_date,
    ROUND(avg_cpu, 2) AS avg_cpu,
    ROUND(FIRST_VALUE(avg_cpu) OVER (
        PARTITION BY server_id
        ORDER BY collection_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS baseline_cpu,
    ROUND(avg_cpu - FIRST_VALUE(avg_cpu) OVER (
        PARTITION BY server_id
        ORDER BY collection_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS delta_from_baseline
FROM server_daily_summary
WHERE server_id IN ('srv-01','srv-03')
ORDER BY server_id, collection_date
"""

result = pd.read_sql_query(sql_first, conn)
print("FIRST_VALUE: CPU delta from each server's day-1 baseline:")
print(result.to_string(index=False))
print()
print("Positive delta_from_baseline = CPU trending up vs baseline.")
print("srv-03 shows consistently high usage — capacity risk.")'''),

md('w08', '''## Named WINDOW Clause — DRY SQL

Define the window once, reuse it across multiple calculations. Prevents copy-paste errors.

```sql
SELECT
    server_id, collection_date, avg_cpu,
    AVG(avg_cpu) OVER w AS rolling_7d_avg,
    MAX(avg_cpu) OVER w AS rolling_7d_max,
    MIN(avg_cpu) OVER w AS rolling_7d_min
FROM server_daily_summary
WINDOW w AS (
    PARTITION BY server_id
    ORDER BY collection_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
);
```

The `WINDOW` clause requires SQLite 3.28.0+. Supported in PostgreSQL, Snowflake, BigQuery, DuckDB.'''),

code('w09', '''# Named WINDOW clause: rolling 3-day stats per server
# Uses WINDOW w AS (...) to define once, reference multiple times
sql_window = """
SELECT
    server_id,
    collection_date,
    ROUND(avg_cpu, 2) AS avg_cpu,
    ROUND(AVG(avg_cpu) OVER w, 2) AS roll_3d_avg,
    ROUND(MAX(avg_cpu) OVER w, 2) AS roll_3d_max,
    ROUND(MIN(avg_cpu) OVER w, 2) AS roll_3d_min
FROM server_daily_summary
WHERE server_id = 'srv-01'
WINDOW w AS (
    PARTITION BY server_id
    ORDER BY collection_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
ORDER BY collection_date
"""

result = pd.read_sql_query(sql_window, conn)
print("Named WINDOW clause: rolling 3-day stats for srv-01:")
print(result.to_string(index=False))
print()
print("WINDOW w defined once, referenced 3 times (AVG, MAX, MIN).")
print("Without WINDOW clause: copy the full OVER() 3 times — error-prone.")'''),

md('w10', '''## Interview Q&A

**Q: What is NTILE(4) useful for in capacity planning?**
A: Quartile analysis — "which servers are in the top 25% of CPU usage?" Q1 = at-risk tier, Q2 = monitor tier. Standard in executive capacity dashboards.

**Q: PERCENT_RANK vs CUME_DIST — what's the key difference?**
A: PERCENT_RANK = (rank-1)/(n-1) — first row is always 0. CUME_DIST = rows_leq_current/n — always > 0. PERCENT_RANK is position-based; CUME_DIST includes ties differently.

**Q: Why use the WINDOW clause?**
A: DRY principle — define the window once, use it in multiple expressions. One change (e.g., change ROWS from 6 to 13 PRECEDING) updates all calculations. Prevents drift bugs.

**Q: LAST_VALUE gotcha?**
A: Default frame is ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW. So LAST_VALUE returns the *current row's value*, not the last in the partition. Fix: use `ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING`.

**Q: Window functions vs GROUP BY — when do you use each?**
A: GROUP BY when you want one row per group (aggregation). Window functions when you want to add group statistics to each individual row while keeping all rows.'''),

md('w11', '''## The Citi Angle

**At Citi, these patterns were daily work:**

1. **NTILE** — Monthly capacity tiering: "assign each server to a risk tier (Q1=critical, Q2=high, Q3=medium, Q4=low) based on 30-day average CPU"

2. **FIRST_VALUE** — Trend analysis: "how much has this server's CPU grown since the start of the month?" Delta from baseline is the key input to capacity forecasting.

3. **Named WINDOW** — Complex dashboard queries with 5-6 window functions over the same partition needed the WINDOW clause to stay maintainable.

**The behavioral story:**
*"At Citi, I rewrote the capacity monitoring query from self-joins to window functions — the NTILE + rolling average approach. Query time dropped from ~8 seconds to under 1 second on 500M rows. The named WINDOW clause meant the business could adjust the rolling period in one place and all metrics updated consistently."*'''),

]

write_nb(f'{BASE}/sql-window-functions-advanced.ipynb', SQL_WINDOW_CELLS)
print(f'  Written: {BASE}/sql-window-functions-advanced.ipynb')


# =============================================================================
# PYTHON — PANDAS FOR DATA ENGINEERING
# =============================================================================

PANDAS_CELLS = [

code('p00-data', '''import pandas as pd
import numpy as np

# Sample telemetry data — use throughout this notebook
servers = pd.DataFrame({
    'server_id': ['srv-01', 'srv-02', 'srv-03', 'srv-04', 'srv-05'],
    'region':    ['us-east', 'us-east', 'us-west', 'us-west', 'us-east'],
    'tier':      ['gold', 'silver', 'gold', 'bronze', 'silver'],
})

metrics = pd.DataFrame({
    'server_id': ['srv-01', 'srv-01', 'srv-02', 'srv-02', 'srv-03',
                  'srv-03', 'srv-04', 'srv-04', 'srv-05'],
    'date':      ['2026-02-27', '2026-02-28', '2026-02-27', '2026-02-28',
                  '2026-02-27', '2026-02-28', '2026-02-27', '2026-02-28',
                  '2026-02-27'],
    'cpu':       [70, 85, 60, 95, 88, 91, 34, 37, 55],
    'mem':       [65, 72, 45, 80, 90, 92, 30, 32, 50],
})

print("servers table:")
print(servers.to_string(index=False))
print()
print("metrics table:")
print(metrics.to_string(index=False))'''),

md('p01', '''# Python — Pandas for Data Engineering
**Day 2 — Python Module**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>Core Insight:</strong> Pandas is the workhorse of Python data engineering.
Senior candidates know groupby internals, vectorization vs apply, and when NOT
to use pandas (use Spark instead). Run <code>p00-data</code> first to set up sample data.
</div>'''),

md('p02', '''## GroupBy — The Most Common Interview Topic

`groupby()` splits the DataFrame into groups, applies a function, and combines results.

**Key methods:**
- `.agg()` — reduce to one row per group
- `.transform()` — return same shape as input (window function equivalent)
- `.apply()` — most flexible, slowest
- `.filter()` — drop entire groups based on condition'''),

code('p03', '''# GroupBy examples — all runnable on the metrics DataFrame from p00-data

# 1. Basic aggregation — one row per server
summary = metrics.groupby('server_id')['cpu'].agg(['mean', 'max', 'min']).round(2).reset_index()
print("1. Basic agg (one row per server):")
print(summary.to_string(index=False))

# 2. Multiple columns, named aggregations
by_server = metrics.groupby('server_id').agg(
    avg_cpu=('cpu', 'mean'),
    peak_cpu=('cpu', 'max'),
    avg_mem=('mem', 'mean'),
    sample_count=('cpu', 'count')
).round(2).reset_index()
print("\n2. Named aggs (multiple metrics):")
print(by_server.to_string(index=False))

# 3. transform() — keeps all rows, adds group stat back
# Equivalent to SQL: AVG(cpu) OVER (PARTITION BY server_id)
metrics_with_avg = metrics.copy()
metrics_with_avg['server_avg_cpu'] = metrics.groupby('server_id')['cpu'].transform('mean').round(2)
metrics_with_avg['above_avg'] = metrics_with_avg['cpu'] > metrics_with_avg['server_avg_cpu']
print("\n3. transform() — adds per-server average to every row (PARTITION BY equivalent):")
print(metrics_with_avg[['server_id','date','cpu','server_avg_cpu','above_avg']].to_string(index=False))'''),

md('p04', '''## Merge — JOIN Equivalent

`pd.merge()` is the standard join operation. Use it over `.join()` — it's explicit about join columns.

```python
# Inner, left, right, outer — same as SQL
result = left_df.merge(right_df, on='key_column', how='left')
```

**Key patterns:**
- Inner join: keeps only matching rows (same as SQL INNER JOIN)
- Left join: keeps all left rows, fills NaN where no right match
- Anti-join: rows in left with NO match in right (`LEFT JOIN + WHERE right.key IS NULL`)'''),

code('p05', '''# Merge examples — joining servers + metrics

# 1. Left join (all servers, fill NaN where no metrics)
full = servers.merge(metrics, on='server_id', how='left')
print("1. Left join — all servers, NaN where no metrics:")
print(full[['server_id','tier','date','cpu']].to_string(index=False))

# 2. Anti-join: servers with NO metrics
# Pattern: left merge + filter where right key is NaN
servers_no_metrics = servers.merge(
    metrics[['server_id']].drop_duplicates(),
    on='server_id', how='left', indicator=True
).query('_merge == "left_only"').drop('_merge', axis=1)
print("\n2. Anti-join — servers with NO metrics:")
print(servers_no_metrics[['server_id','tier']].to_string(index=False))

# 3. Enrichment join — add server tier to metrics
enriched = metrics.merge(servers[['server_id','tier','region']], on='server_id', how='left')
print("\n3. Enriched metrics (with tier + region):")
print(enriched[['server_id','tier','region','date','cpu']].head(5).to_string(index=False))'''),

md('p06', '''## apply vs Vectorization — Performance Critical

**Rule:** Avoid `apply` with lambdas whenever possible. Vectorized operations are 10-100x faster on large DataFrames because they execute in NumPy's C layer, not Python.

| Method | Speed | Notes |
|--------|-------|-------|
| `apply(lambda x: ...)` | Slow | Python loop, one row at a time |
| `np.where(condition, a, b)` | Fast | C-speed, vectorized |
| `pd.cut(series, bins)` | Fast | C-speed, bin categorization |
| `series.map(dict)` | Fast | Hash lookup, no Python loop |'''),

code('p07', '''import time

# Generate larger sample for benchmarking
large_metrics = pd.DataFrame({
    'cpu': np.random.uniform(0, 100, 100_000)
})

# Method 1: apply with lambda — Python level, slow
start = time.time()
large_metrics['cat_apply'] = large_metrics['cpu'].apply(
    lambda x: 'critical' if x > 90 else ('high' if x > 75 else 'normal')
)
apply_time = time.time() - start

# Method 2: np.where — vectorized, C speed
start = time.time()
large_metrics['cat_vectorized'] = np.where(
    large_metrics['cpu'] > 90, 'critical',
    np.where(large_metrics['cpu'] > 75, 'high', 'normal')
)
vec_time = time.time() - start

# Method 3: pd.cut — bin categorization
start = time.time()
large_metrics['cat_cut'] = pd.cut(
    large_metrics['cpu'],
    bins=[0, 75, 90, 100],
    labels=['normal', 'high', 'critical']
)
cut_time = time.time() - start

print(f"apply(lambda):  {apply_time:.4f}s")
print(f"np.where:       {vec_time:.4f}s   ({apply_time/vec_time:.1f}x faster)")
print(f"pd.cut:         {cut_time:.4f}s   ({apply_time/cut_time:.1f}x faster)")
print()

# Verify all three give the same result
print("Results agree:", (large_metrics['cat_apply'] == large_metrics['cat_vectorized']).all())
print()

# Apply IS appropriate for: complex multi-column logic that can't be vectorized
# Example: format a string using multiple columns
sample = metrics[['server_id','date','cpu']].copy()
sample['label'] = sample.apply(
    lambda row: f"{row['server_id']} on {row['date']}: {row['cpu']}%", axis=1
)
print("apply for string formatting (no vectorized equivalent):")
print(sample['label'].head(3).to_string(index=False))'''),

md('p08', '''## Interview Q&A

**Q: What does `groupby().transform()` do vs `groupby().agg()`?**
A: `agg()` reduces — returns one row per group. `transform()` returns a Series with the same index as the original DataFrame — like SQL window PARTITION BY. Each row gets its group's aggregate value.

**Q: When would you use pandas over Spark?**
A: Dataset fits comfortably in memory (rule of thumb: < 1-2 GB). Spark has startup overhead, cluster management complexity, and serialization cost that outweigh benefits for small data.

**Q: What's the difference between `merge()` and `join()`?**
A: `merge()` joins on column values — explicit, flexible. `join()` joins on index — simpler but can be confusing. Use `merge()` always unless you specifically want index-based joining.

**Q: `apply` vs vectorization — why does it matter at scale?**
A: `apply` is Python-level iteration — each row is a Python function call. Vectorized operations use NumPy's C/Fortran layer. On 1M rows, `apply` might take seconds; `np.where` takes milliseconds.

**Q: What is `indicator=True` in `merge()`?**
A: Adds a `_merge` column showing whether each row came from 'left_only', 'right_only', or 'both'. Useful for anti-joins and debugging join behavior.'''),

md('p09', '''## The Citi Angle

**Pandas was the bridge from APM data exports to analysis.** APM tools (CA APM, AppDynamics) exposed data via REST APIs and CSV exports. Before loading into databases, pandas was the transformation layer.

**Real pattern — enrichment pipeline:**
```python
# Read raw telemetry export
raw = pd.read_csv("apm_export_2026_02.csv")

# Enrich with server metadata from CMDB
cmdb = pd.read_csv("cmdb_servers.csv")
enriched = raw.merge(cmdb[["server_id","tier","owner","environment"]], on="server_id", how="left")

# Vectorized categorization (never apply)
enriched["risk_tier"] = np.where(
    enriched["cpu_pct"] > 90, "critical",
    np.where(enriched["cpu_pct"] > 75, "high", "normal")
)

# Group by tier for executive summary
summary = (enriched.groupby(["environment","risk_tier"])
    .agg(count=("server_id","count"), avg_cpu=("cpu_pct","mean"))
    .round(2).reset_index())
```

**Interview tie-in:** *"Pandas was our ETL glue layer at Citi — joining APM exports to CMDB metadata, vectorized categorization, groupby summaries. The same patterns as SQL, but in Python with better testability and version control."*'''),

]

write_nb(f'{BASE}/python-pandas.ipynb', PANDAS_CELLS)
print(f'  Written: {BASE}/python-pandas.ipynb')


# =============================================================================
# TECHNOLOGY — APACHE SPARK ARCHITECTURE
# =============================================================================

SPARK_CELLS = [

md('s01', '''# Apache Spark Architecture
**Day 2 — Technology Module**

---

<div style="padding:15px;border-left:8px solid #11998e;background:#e8faf5;border-radius:4px;">
<strong>Core Insight:</strong> Spark is the industry standard for distributed data processing.
Senior data engineers know the execution model — not just "it's fast" but WHY it's fast
and what makes it slow. Key: lazy evaluation, DAG optimization, shuffle is the enemy.
</div>

### The Execution Model
```
Driver Program (your Python/Scala code)
    ↓  creates
SparkSession / SparkContext
    ↓  builds
DAG of Stages (Directed Acyclic Graph)
    ↓  each stage is a set of
Tasks (one per partition, runs in parallel)
    ↓  executed on
Executors (JVMs on worker nodes)
```

### RDD → DataFrame → Dataset
- **RDD:** Low-level, untyped. Use only for legacy code.
- **DataFrame:** Optimized by Catalyst query optimizer. Use this always.
- **Dataset:** Typed DataFrame (Scala/Java only). Python uses DataFrame.'''),

md('s02', '''## Transformations vs Actions

**Transformations** build the DAG but execute nothing:
```python
filtered = df.filter(df.cpu > 80)          # lazy
grouped  = filtered.groupBy("server_id")    # lazy
averaged = grouped.agg({"cpu": "avg"})      # lazy
# Nothing has run yet — DAG is just a plan
```

**Actions** trigger execution:
```python
averaged.show()                              # NOW the DAG runs
averaged.write.parquet("s3://output/")       # another action
count = averaged.count()                     # another action
```

The lazy model lets Spark optimize the *entire plan* before running anything — filter pushdown, join reordering, etc.'''),

code('s03-sim', '''# LOCAL SIMULATION — pandas equivalent of Spark transformations + actions
# In production, replace spark.read/write and spark.sql with the PySpark equivalents.

import pandas as pd
import numpy as np

# Simulate a large telemetry dataset (what would come from S3 in Spark)
np.random.seed(42)
n = 50_000
raw_telemetry = pd.DataFrame({
    'server_id':       [f'srv-{i:03d}' for i in np.random.randint(1, 101, n)],
    'cpu_utilization': np.random.uniform(20, 100, n).round(1),
    'mem_utilization': np.random.uniform(30, 95, n).round(1),
    'region':          np.random.choice(['us-east', 'us-west', 'eu-west'], n),
    'year': '2026', 'month': '02',
})

# ── "Transformations" (lazy in Spark, eager in pandas) ───────────────────────
# Step 1: filter
filtered = raw_telemetry[raw_telemetry['cpu_utilization'] > 80]

# Step 2: add derived column (withColumn in Spark)
filtered = filtered.assign(
    alert_tier=pd.cut(filtered['cpu_utilization'],
                      bins=[80, 90, 95, 100],
                      labels=['warning', 'high', 'critical'])
)

# Step 3: groupBy + agg
result = (filtered.groupby(['region', 'alert_tier'])
    .agg(
        server_count=('server_id', pd.Series.nunique),
        avg_cpu=('cpu_utilization', 'mean'),
        max_cpu=('cpu_utilization', 'max'),
    ).round(2).reset_index())

# ── "Action" — materialize and display ───────────────────────────────────────
print(f"Input rows: {len(raw_telemetry):,}")
print(f"After filter (cpu > 80): {len(filtered):,} rows")
print()
print("Aggregated result (Spark equivalent: .show()):")
print(result.to_string(index=False))
print()
print("Spark version of this pipeline:")
print("""
  df = spark.read.parquet("s3://telemetry/")
  filtered = df.filter(df.cpu_utilization > 80)
  result = filtered.groupBy("region", "alert_tier").agg(
      F.countDistinct("server_id").alias("server_count"),
      F.avg("cpu_utilization").alias("avg_cpu"),
  )
  result.show()   # ← this triggers execution of the entire DAG
""")'''),

md('s04', '''## Partitions = Parallelism

```
Dataset
  ├── Partition 1  →  Task 1  →  Executor A
  ├── Partition 2  →  Task 2  →  Executor B
  ├── Partition 3  →  Task 3  →  Executor C
  └── Partition 4  →  Task 4  →  Executor A
```

More partitions = more parallelism. But too many = scheduling overhead.

**Rule of thumb:** 2-4 partitions per CPU core. 128-256 MB per partition.

```python
# Check and adjust partitions
df.rdd.getNumPartitions()       # see current count

df.repartition(100)             # full shuffle — use when increasing or balancing
df.coalesce(10)                 # local merge — use when decreasing (no shuffle)

# Write partitioned by column (downstream query pruning)
df.write.partitionBy("year", "month").parquet("s3://output/")
```'''),

code('s05-sim', '''# Partition simulation — illustrate repartition vs coalesce behavior

import pandas as pd

# Simulate 12 "partitions" of data (in Spark, each would be a separate task)
data_by_partition = []
for part_id in range(12):
    size = 1000 + (part_id % 3) * 500   # simulate skew: some partitions are bigger
    data_by_partition.append({
        'partition': part_id,
        'row_count': size,
        'size_mb': round(size * 0.0001, 3)  # 100 bytes per row approx
    })

df_parts = pd.DataFrame(data_by_partition)
print("Current partitions (simulated):")
print(df_parts.to_string(index=False))
print(f"Total rows: {df_parts['row_count'].sum():,}")
print(f"Avg partition size: {df_parts['row_count'].mean():.0f} rows")
print(f"Max skew ratio: {df_parts['row_count'].max()/df_parts['row_count'].min():.1f}x")
print()
print("repartition(6):  full shuffle, 6 balanced partitions — expensive but balanced")
print("coalesce(6):     merge locally, 6 partitions no shuffle — cheap but may be uneven")
print()
print("When to use each:")
print("  repartition: increasing partition count OR fixing data skew (groupBy skew)")
print("  coalesce:    reducing partition count before write (avoid many tiny files)")'''),

md('s06', '''## What Causes a Shuffle?

A shuffle = moving data across the network between executors. It's the #1 Spark performance bottleneck.

**Operations that cause shuffle:**
- `groupBy()` — data for the same key must be on the same executor
- `join()` — join keys must be co-located
- `repartition()` — explicit redistribution
- `distinct()` — de-duplication requires comparing across all partitions

**How to minimize shuffle:**
1. **Filter early** — reduce data before shuffle operations
2. **Broadcast join** — replicate a small table to all executors (avoids shuffle entirely)
3. **Partition wisely** — write data partitioned by the join key you'll use most
4. **Cache before re-use** — if you'll run multiple actions on the same DataFrame, `df.cache()` avoids recomputing from scratch

```python
# Broadcast join — small lookup table (< few hundred MB)
from pyspark.sql import functions as F
server_metadata = spark.read.parquet("s3://metadata/servers/")   # small
df_enriched = df.join(F.broadcast(server_metadata), on="server_id", how="left")
```'''),

md('s07', '''## Interview Q&A

**Q: What is the Catalyst optimizer?**
A: Spark's query optimizer — transforms the logical plan (what you wrote) into an optimized physical plan (what Spark executes). It pushes filters down, reorders joins, eliminates unnecessary columns. Same role as a SQL query planner.

**Q: What's the difference between `repartition` and `coalesce`?**
A: `repartition` does a full shuffle — good for increasing partitions or fixing data skew. `coalesce` merges existing partitions locally — good for reducing partition count cheaply before a write. coalesce can't increase partition count.

**Q: Explain lazy evaluation.**
A: Transformations build a DAG but don't run. Only actions trigger execution. This lets Spark optimize the entire plan before running — filter pushdown, join reordering — things you can't do if you execute eagerly.

**Q: How many partitions should you have?**
A: 2-4 per CPU core. 128-256 MB per partition is typical. Too few = underutilized cores. Too many = excessive scheduling overhead. Adjust with `repartition()` or `coalesce()`.

**Q: What is data skew and how do you fix it?**
A: When one partition has far more data than others (one key dominates). Fix: (1) filter or pre-aggregate the skewed key separately, (2) salting — add a random suffix to the key to distribute it, (3) use a broadcast join if the table is small enough.'''),

md('s08', '''## The Citi Angle

**Spark was the natural evolution of our telemetry pipeline.** As data volume grew from gigabytes to terabytes, pandas jobs hit memory limits. Spark's partition model matched our data naturally — partition by server group, then process each group in parallel.

**The capacity forecasting pipeline:**
```
1. Spark reads 6 months of daily Parquet from S3 (partitioned by date)
   → Partition pruning: only reads relevant months
2. groupBy("server_id").agg(rolling averages, percentiles)
   → One shuffle — unavoidable
3. join with server_metadata (broadcast — metadata is < 50MB)
   → No shuffle — broadcast avoids it
4. Prophet forecasting model applied per server
   → mapPartitions: run Python model on each partition locally
5. Write predictions back to S3 (partitioned by forecast_date)
   → coalesce(50) before write — prevent small files
```

**Interview line:** *"Shuffle is Spark's most expensive operation. In the Citi forecasting pipeline, I reduced shuffle by broadcasting server metadata (avoiding a 6B-row join shuffle), partitioning input by date (partition pruning), and coalescing before write. Pipeline time dropped from 45 minutes to 12 minutes."*'''),

]

write_nb(f'{BASE}/spark-architecture.ipynb', SPARK_CELLS)
print(f'  Written: {BASE}/spark-architecture.ipynb')


print('\nDay 2 generation complete!')
print(f'Output: {BASE}/')
print()
print('LeetCode notebooks + HTML:')
print('  lc-0121-best-time-sell')
print('  lc-0003-longest-substring')
print('  lc-0424-char-replacement')
print('  lc-0239-sliding-window-max')
print('  lc-0076-minimum-window')
print()
print('Concept notebooks:')
print('  sql-window-functions-advanced.ipynb')
print('  python-pandas.ipynb')
print('  spark-architecture.ipynb')
