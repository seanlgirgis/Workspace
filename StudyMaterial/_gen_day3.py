"""
Day 3 generator: Stack | Complex JOINs | Decorators | Lambda/Kappa Architecture
Output: D:/Workspace/StudyMaterial/Day3/

Files created:
  lc-0020-valid-parentheses.ipynb / .html
  lc-0155-min-stack.ipynb / .html
  lc-0739-daily-temperatures.ipynb / .html
  lc-0853-car-fleet.ipynb / .html
  sql-complex-joins.ipynb
  python-decorators.ipynb
  pipeline-architecture.ipynb
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'D:/Workspace/StudyMaterial/Day3'
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

# ── HTML generation (Stack / Orange-Yellow theme) ─────────────────────────────

ST_GRAD1  = '#f7971e'
ST_GRAD2  = '#ffd200'
ST_ACCENT = '#c47a10'

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_inline(text):
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def md_to_html(text, accent=ST_ACCENT):
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
    accent     = ST_ACCENT

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
<title>LC #{num} \u2014 {title} \u2014 Stack</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
       background: linear-gradient(135deg, {ST_GRAD1} 0%, {ST_GRAD2} 100%);
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
        font-family: 'Courier New', monospace; font-size: 0.88em; color: #c47a10; }}
pre code {{ background: none; color: #d4d4d4; padding: 0; font-size: 1em; }}
@media (max-width: 800px) {{
  div[style*="grid-template-columns:1fr 1fr"] {{ grid-template-columns: 1fr !important; }}
}}
</style>
</head>
<body>
<div class="container">
<h1>LC #{num} \u2014 {title} <span class="badge">{difficulty}</span></h1>
<p class="subtitle">Stack Pattern &nbsp;|&nbsp; Day 3 Study Material</p>
{body}
</div>
</body>
</html>"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  HTML: {html_path}')


# =============================================================================
# LC #20 — VALID PARENTHESES
# =============================================================================

VALID_PARENS_CELLS = [

md('cell-title', '''# LC #20 — Valid Parentheses
**Category:** Stack | **Difficulty:** Easy | **Day 3**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>The Problem:</strong> Given string <code>s</code> containing <code>()[]{}</code>,
return <code>true</code> if the string is valid. Valid means every opener has a matching
closer in the correct order, and they are properly nested.
</div>

**Examples:**
```
"()[]{}"   → true
"()[]{}"   → true
"(]"       → false  (wrong closer)
"([)]"     → false  (wrong nesting order)
"{[]}"     → true   (properly nested)
```

**Core Insight:** Push openers onto the stack. For each closer, check that the top of the stack is its matching opener. Any mismatch or leftover items = invalid.'''),

md('cell-mental-models', '''## Mental Models

**1. The Stack as "Pending Openers"**
The stack holds openers that haven't been matched yet. They're "waiting" for their closing partner. LIFO (last in, first out) naturally enforces proper nesting — the most recent opener must be closed first.

**2. The Pairing Map**
`{')': '(', ']': '[', '}': '{'}` maps each closer to its expected opener. This avoids long if-elif chains and makes the logic extensible to new bracket types.

**3. Two Failure Modes**
- Mismatch: closer doesn't match top of stack (wrong type or empty stack)
- Leftover: stack is non-empty at end (unclosed openers)'''),

code('cell-brute-force', '''# No efficient "brute force" exists — the stack approach IS the optimal.
# This shows what iterative shrinking would look like (O(n²)):

def isValid_shrink(s: str) -> bool:
    """Replace matching pairs iteratively until no more can be removed."""
    prev = None
    while s != prev:
        prev = s
        for pair in ["()", "[]", "{}"]:
            s = s.replace(pair, "")
    return s == ""

# Correct but O(n²) — each pass is O(n), up to n/2 passes
print(isValid_shrink("()[]{}"))   # True
print(isValid_shrink("([)]"))     # False
print(isValid_shrink("{[]}"))     # True'''),

md('cell-walkthrough', '''## Step-by-Step: `"([)]"`

| i | char | Action | Stack |
|---|------|--------|-------|
| 0 | `(` | opener → push | `[(]` |
| 1 | `[` | opener → push | `[(, []` |
| 2 | `)` | closer → top is `[`, expected `(` → **MISMATCH** | return False |

The key: at step 2, `)` expects `(` on top but finds `[`. The string is invalid because `[` was opened more recently and must be closed first.

**Correct nesting:** `{[()]}` — innermost opens last, closes first.'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(n) space
# Stack: push openers, pop and verify for closers.

def isValid(s: str) -> bool:
    stack = []
    pairs = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}

    for char in s:
        if char in \'([{\':
            stack.append(char)
        elif char in \')]}\':\
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()

    return len(stack) == 0   # empty = all openers matched

# Test
print(isValid("()[]{}"))   # True
print(isValid("(]"))       # False
print(isValid("([)]"))     # False
print(isValid("{[]}"))     # True
print(isValid(""))         # True (empty string is valid)
print(isValid("("))        # False (unclosed opener)'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Iterative shrink | O(n²) | O(n) |
| **Stack (Optimal)** | **O(n)** | **O(n)** |

**Space note:** In the worst case (all openers, no closers), the stack holds n items: `((((...` → O(n) space.

**Best case:** Alternating opener-closer: `()()()` → stack never exceeds size 1.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why check `not stack` before `stack[-1]`?**
A: Short-circuit evaluation. If the stack is empty and we see a closer, it's immediately invalid — there's nothing to match. Checking `not stack` first prevents an IndexError on `stack[-1]`.

**Q: What happens with an empty string?**
A: The loop never runs, stack remains empty, `len(stack) == 0` returns True. An empty string is considered valid.

**Q: Real-world applications?**
A: Validating nested structures: JSON/XML parsing, nested SQL subqueries, template engines (Jinja, Handlebars), config file validation (YAML, TOML). At Citi: validating nested alert condition expressions.

**Q: How would you extend this for additional bracket types?**
A: Just add entries to the `pairs` dict. The algorithm generalizes to any matching delimiter pair without code changes — a good extensibility answer.'''),

md('cell-citi-narrative', '''## The Citi Angle

**Nested configuration validation.** At Citi, monitoring rules were expressed as nested conditions:

```python
# Validate nested alert condition expression
def validate_condition(expr: str) -> bool:
    """
    Valid: "(cpu > 80 AND (mem > 70 OR disk > 90))"
    Invalid: "(cpu > 80 AND [mem > 70])"  — mixed brackets
    """
    stack = []
    pairs = {\')\': \'(\', \']\': \'[\', \'}\': \'{\'}
    for char in expr:
        if char in \'([{\':
            stack.append(char)
        elif char in \')]}\':\
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0

tests = [
    ("(cpu > 80 AND (mem > 70 OR disk > 90))", True),
    ("(cpu > 80 AND [mem > 70])", False),
]
for expr, expected in tests:
    result = validate_condition(expr)
    status = "PASS" if result == expected else "FAIL"
    print(f"{status}: {repr(expr[:40])} → {result}")
```

**Interview tie-in:** "Valid parentheses is the foundation of any parser or config validator. I used this pattern to validate nested monitoring expressions — ensuring alert conditions were syntactically correct before deployment."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Stack — push openers, pop and verify for closers |
| **Time** | O(n) |
| **Space** | O(n) |
| **Key insight** | LIFO naturally enforces proper nesting |
| **Say in interview** | "Push openers. For each closer, top of stack must be the matching opener. Empty stack at end = valid." |

**Two failure modes to mention:** Wrong closer type (mismatch). Unclosed openers remaining in stack (leftover).'''),

]

write_nb(f'{BASE}/lc-0020-valid-parentheses.ipynb', VALID_PARENS_CELLS)
gen_html('lc-0020-valid-parentheses', f'{BASE}/lc-0020-valid-parentheses.ipynb',
         f'{BASE}/lc-0020-valid-parentheses.html', 20, 'Valid Parentheses', 'easy')


# =============================================================================
# LC #155 — MIN STACK
# =============================================================================

MIN_STACK_CELLS = [

md('cell-title', '''# LC #155 — Min Stack
**Category:** Stack with Auxiliary State | **Difficulty:** Medium | **Day 3**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>The Problem:</strong> Design a stack supporting <code>push</code>, <code>pop</code>,
<code>top</code>, and <code>getMin()</code> — all in O(1) time.
</div>

**Interface:**
```
MinStack ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
ms.getMin()  → -3
ms.pop()
ms.top()     → 0
ms.getMin()  → -2
```

**Core Insight:** A parallel `min_stack` tracks the running minimum at every state. When you pop the main stack, pop min_stack too — the previous minimum is automatically exposed.'''),

md('cell-mental-models', '''## Mental Models

**1. Two Synchronized Stacks**
`stack` holds actual values. `min_stack` holds the current minimum at each corresponding stack state. They stay in sync: push to both, pop from both simultaneously.

**2. Why Parallel, Not Just One Value?**
If you only stored one minimum variable and then popped it, you'd lose the *previous* minimum. The parallel stack remembers the minimum at *every* state the stack has been in.

**3. The Invariant**
`min_stack[-1]` is always the minimum of all elements currently in `stack`. This invariant is maintained by pushing `min(val, min_stack[-1])` on every push.'''),

code('cell-brute-force', '''# Alternative: single stack storing (value, min_at_this_point) tuples
# Same complexity but cleaner mental model for some

class MinStackTuple:
    def __init__(self):
        self.stack = []   # each entry: (value, min_so_far)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]

# Test
ms = MinStackTuple()
ms.push(-2); ms.push(0); ms.push(-3)
print(f"getMin: {ms.getMin()}")   # -3
ms.pop()
print(f"top:    {ms.top()}")      # 0
print(f"getMin: {ms.getMin()}")   # -2'''),

md('cell-walkthrough', '''## State Trace

Operations: `push(-2)`, `push(0)`, `push(-3)`, `pop()`, `top()`, `getMin()`

| Operation | stack | min_stack | Notes |
|-----------|-------|-----------|-------|
| push(-2) | [-2] | [-2] | first element, min = itself |
| push(0) | [-2, 0] | [-2, -2] | 0 > -2, min stays -2 |
| push(-3) | [-2, 0, -3] | [-2, -2, -3] | -3 < -2, new min |
| getMin() | — | — | min_stack[-1] = **-3** |
| pop() | [-2, 0] | [-2, -2] | both stacks sync-popped |
| top() | — | — | stack[-1] = **0** |
| getMin() | — | — | min_stack[-1] = **-2** ✓ |

After popping -3, the previous minimum (-2) is automatically the top of min_stack.'''),

code('cell-optimal-code', '''# Optimal — O(1) all operations, O(n) space
# Two synchronized stacks.

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []   # min_stack[-1] = current minimum

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Current min is either new val or existing min — whichever is smaller
        if self.min_stack:
            self.min_stack.append(min(val, self.min_stack[-1]))
        else:
            self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()    # sync: both stacks stay the same length

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

# Test
ms = MinStack()
ms.push(-2); ms.push(0); ms.push(-3)
print(f"getMin after push(-2,0,-3): {ms.getMin()}")   # -3
ms.pop()
print(f"top after pop:              {ms.top()}")       # 0
print(f"getMin after pop:           {ms.getMin()}")    # -2'''),

md('cell-complexity', '''## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| push | O(1) | O(n) total |
| pop | O(1) | |
| top | O(1) | |
| getMin | O(1) | |

**Space:** O(n) — both stacks combined hold 2n elements in the worst case. This is the trade-off for O(1) getMin.

**Alternative approaches:**
- Store `(val, min)` pairs in single stack — same complexity, different ergonomics
- Store only the deltas (space optimization for large min values) — same O(1) but more complex'''),

md('cell-qa', '''## Interview Q&A

**Q: What's the space trade-off?**
A: Double the memory — O(n) for both stacks combined. In exchange, getMin() is O(1) instead of O(n) (scanning the full stack). Classic space-for-time trade.

**Q: How would you track the maximum instead of the minimum?**
A: Identical pattern with a `max_stack`. Push `max(val, max_stack[-1])` instead of `min(...)`.

**Q: Why does this need two stacks instead of one variable?**
A: A single variable loses the history. When you pop the current minimum, you need to know what the previous minimum was. The parallel stack preserves the minimum at every point in history.

**Q: What if you popped from an empty stack?**
A: The problem guarantees valid calls. In production code, you'd add an assertion or raise an exception on empty pop/top/getMin.'''),

md('cell-citi-narrative', '''## The Citi Angle

**The "minimum with history" pattern** shows up in sliding-window baseline tracking:

```python
# Track running minimum CPU baseline with the ability to "roll back"
# (e.g., when a server is decommissioned, restore the previous baseline)

class BaselineTracker:
    """Tracks minimum CPU baseline — supports undo/rollback."""
    def __init__(self):
        self._readings = []
        self._min_stack = []

    def record(self, cpu: float):
        self._readings.append(cpu)
        prev_min = self._min_stack[-1] if self._min_stack else float(\'inf\')
        self._min_stack.append(min(cpu, prev_min))

    def rollback(self):
        """Remove last reading (server decommissioned)."""
        if self._readings:
            self._readings.pop()
            self._min_stack.pop()

    def baseline(self) -> float:
        return self._min_stack[-1] if self._min_stack else float(\'inf\')

tracker = BaselineTracker()
for cpu in [72.5, 68.1, 91.3, 45.2, 88.7]:
    tracker.record(cpu)
    print(f"CPU: {cpu:.1f}  Baseline min: {tracker.baseline():.1f}")
tracker.rollback()  # remove 88.7
print(f"After rollback, baseline: {tracker.baseline():.1f}")
```

**Interview tie-in:** "Min Stack is the building block for any system that needs O(1) minimum queries with rollback — capacity baseline tracking, undo operations in config management."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Two synchronized stacks (main + min_stack) |
| **All operations** | O(1) |
| **Space** | O(n) — 2n total across both stacks |
| **Invariant** | `min_stack[-1]` always = current minimum of all stack elements |
| **Say in interview** | "Parallel min_stack: push min(val, current_min), pop both simultaneously. Invariant: min_stack[-1] is always the current minimum." |'''),

]

write_nb(f'{BASE}/lc-0155-min-stack.ipynb', MIN_STACK_CELLS)
gen_html('lc-0155-min-stack', f'{BASE}/lc-0155-min-stack.ipynb',
         f'{BASE}/lc-0155-min-stack.html', 155, 'Min Stack', 'medium')


# =============================================================================
# LC #739 — DAILY TEMPERATURES
# =============================================================================

DAILY_TEMP_CELLS = [

md('cell-title', '''# LC #739 — Daily Temperatures
**Category:** Monotonic Stack | **Difficulty:** Medium | **Day 3**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>The Problem:</strong> Given array <code>temperatures</code>, for each day return how many
days until a warmer temperature. Return 0 if no warmer day exists.
</div>

**Example:**
```
Input:  [73, 74, 75, 71, 69, 72, 76, 73]
Output: [ 1,  1,  4,  2,  1,  1,  0,  0]
```
*Day 2 (75°): next warmer day is day 6 (76°) — 4 days away.*

**Core Insight:** Maintain a **monotonic decreasing stack** of indices of "unresolved" days. When a warmer temperature arrives, pop and compute the gap.'''),

md('cell-mental-models', '''## Mental Models

**1. Unresolved Days Waiting for Resolution**
Each index on the stack represents a day that hasn't yet found a warmer day. The stack holds them "in suspense." When a warmer day arrives, it resolves all waiting days that are colder than it.

**2. Monotonic Decreasing = Never Redundant**
We maintain the stack in decreasing order of temperatures. Why? Because if temperature[i] ≤ temperature[j] and i < j, then i will never be the answer for any day after j — j always blocks it. So i is useless once j is on the stack.

**3. Amortized O(n)**
Each element enters the stack once and exits at most once. Despite the inner while loop, total operations ≤ 2n across all iterations.'''),

code('cell-brute-force', '''# Brute Force — O(n²) time
def dailyTemperatures_brute(temperatures: list[int]) -> list[int]:
    result = [0] * len(temperatures)
    for i in range(len(temperatures)):
        for j in range(i + 1, len(temperatures)):
            if temperatures[j] > temperatures[i]:
                result[i] = j - i
                break
    return result

temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(dailyTemperatures_brute(temps))   # [1, 1, 4, 2, 1, 1, 0, 0]'''),

md('cell-walkthrough', '''## Stack Trace: `[73, 74, 75, 71, 69, 72, 76, 73]`

| i | temp | While loop (pop warmer) | stack (indices) | result[popped] |
|---|------|------------------------|-----------------|----------------|
| 0 | 73 | none | [0] | — |
| 1 | 74 | pop 0 (73<74) | [1] | result[0]=1-0=1 |
| 2 | 75 | pop 1 (74<75) | [2] | result[1]=2-1=1 |
| 3 | 71 | none (71<75) | [2,3] | — |
| 4 | 69 | none (69<71) | [2,3,4] | — |
| 5 | 72 | pop 4 (69<72), pop 3 (71<72) | [2,5] | result[4]=1, result[3]=2 |
| 6 | 76 | pop 5 (72<76), pop 2 (75<76) | [6] | result[5]=1, result[2]=4 |
| 7 | 73 | none (73<76) | [6,7] | — |
| end | — | stack [6,7] → result stays 0 | | — |'''),

code('cell-optimal-code', '''# Optimal — O(n) time, O(n) space (amortized)
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    result = [0] * len(temperatures)
    stack = []   # indices of unresolved days (temperatures are decreasing)

    for i, temp in enumerate(temperatures):
        # Current day is warmer — resolve all colder waiting days
        while stack and temperatures[stack[-1]] < temp:
            prev_day = stack.pop()
            result[prev_day] = i - prev_day

        stack.append(i)   # current day is now waiting
    # Days still in stack: no warmer day found → result stays 0

    return result

# Test
temps = [73, 74, 75, 71, 69, 72, 76, 73]
print(dailyTemperatures(temps))   # [1, 1, 4, 2, 1, 1, 0, 0]

# Edge cases
print(dailyTemperatures([30, 40, 50, 60]))   # [1, 1, 1, 0]
print(dailyTemperatures([30, 60, 90]))        # [1, 1, 0]
print(dailyTemperatures([90, 80, 70, 60]))   # [0, 0, 0, 0]'''),

md('cell-complexity', '''## Complexity Analysis

| Approach | Time | Space |
|----------|------|-------|
| Brute Force | O(n²) | O(1) |
| **Monotonic Stack** | **O(n)** | **O(n)** |

**Why O(n) despite while loop?** Each index is pushed to the stack at most once and popped at most once. Total push + pop operations ≤ 2n across all iterations — amortized O(1) per element.

**Stack max size:** In the worst case (monotonically decreasing temperatures), all indices accumulate in the stack → O(n) space.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why maintain a monotonic decreasing stack?**
A: We only keep elements that could be the answer for future days. If temperature[i] < temperature[j] and i < j, then j is "blocking" i — any day warmer than i is also warmer than j, and j is closer. So i can never be the "next warmer" for anything to the right of j. We pop it.

**Q: What's amortized O(n)?**
A: Each element is pushed exactly once and popped at most once. The inner while loop's total iterations across all i = at most n pops. So total work = O(n) pushes + O(n) pops = O(n).

**Q: What about elements still in the stack at the end?**
A: They represent days with no warmer day to the right. Result stays 0 (initialized value). No cleanup needed.

**Q: Data engineering application?**
A: "Next time a metric exceeds its current value" — first-occurrence detection. "For each day's CPU reading, how many days until a higher reading?" Same algorithm.'''),

md('cell-citi-narrative', '''## The Citi Angle

**"Next time CPU exceeds current peak" — capacity trend detection:**

```python
# For each day, how many days until CPU exceeds today's reading?
# Monotonic stack: same algorithm as dailyTemperatures

def days_until_higher_cpu(daily_readings: list[float]) -> list[int]:
    """For each day, days until a higher CPU reading is observed."""
    result = [0] * len(daily_readings)
    stack = []   # indices of unresolved days

    for i, cpu in enumerate(daily_readings):
        while stack and daily_readings[stack[-1]] < cpu:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)

    return result

# 8 days of srv-01 CPU readings
readings = [72.5, 68.1, 75.3, 71.0, 69.2, 77.8, 91.3, 88.4]
gaps = days_until_higher_cpu(readings)
for i, (cpu, gap) in enumerate(zip(readings, gaps)):
    note = f"→ exceeded in {gap} days" if gap else "→ no higher reading found"
    print(f"Day {i+1}: {cpu:.1f}% {note}")
```

**Interview tie-in:** "Daily temperatures is the 'next greater element' pattern. At Citi, I used this to find the first day a server's CPU exceeded its historical peak — an early warning signal for capacity planning."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Monotonic Stack (decreasing) |
| **Time** | O(n) amortized |
| **Space** | O(n) |
| **Stack content** | Indices of days waiting for a warmer day |
| **Say in interview** | "Monotonic decreasing stack of unresolved indices. When warmer temp arrives, pop all colder days and compute gap. Amortized O(n): each element pushed and popped at most once." |'''),

]

write_nb(f'{BASE}/lc-0739-daily-temperatures.ipynb', DAILY_TEMP_CELLS)
gen_html('lc-0739-daily-temperatures', f'{BASE}/lc-0739-daily-temperatures.ipynb',
         f'{BASE}/lc-0739-daily-temperatures.html', 739, 'Daily Temperatures', 'medium')


# =============================================================================
# LC #853 — CAR FLEET
# =============================================================================

CAR_FLEET_CELLS = [

md('cell-title', '''# LC #853 — Car Fleet
**Category:** Stack / Sorting | **Difficulty:** Medium | **Day 3**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>The Problem:</strong> <code>n</code> cars head to <code>target</code> miles away.
Given <code>position[]</code> and <code>speed[]</code>. Cars that catch up to a car ahead
form a fleet (the faster car slows to the slower car's speed). Return the number of fleets.
</div>

**Example:**
```
target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3] → 3
```
*Car at 10 arrives at t=1. Car at 8 arrives at t=1 too — same fleet. Others form 2 separate fleets.*

**Core Insight:** Sort by position descending. Calculate time to target for each car. If a car's arrival time is ≤ the car ahead's, they join the same fleet (the slower car's time dominates).'''),

md('cell-mental-models', '''## Mental Models

**1. Arrival Time is the Key**
`time = (target - position) / speed` — how long to reach target at constant speed.
If car B (behind) arrives before or at the same time as car A (ahead): B catches up → same fleet. B's actual arrival time is then A's (it slows to A's speed).

**2. Sort Descending = Process Closest First**
Process cars from closest to target to furthest. A car can only join the fleet ahead of it (closer to target). It cannot "jump over" a car.

**3. Stack = Fleet Representatives**
The stack holds arrival times of distinct fleets. If the current car arrives after the fleet ahead (top of stack), it forms a new fleet. Otherwise it joins the existing one.'''),

code('cell-brute-force', '''# Simulation approach — sort and check
# O(n log n) — same as optimal but more verbose

def carFleet_verbose(target: int, position: list[int], speed: list[int]) -> int:
    cars = sorted(zip(position, speed), reverse=True)  # closest to target first
    fleets = []

    for pos, spd in cars:
        time = (target - pos) / spd
        # If no fleet ahead OR this car arrives after the current lead fleet
        if not fleets or time > fleets[-1]:
            fleets.append(time)   # new fleet
        # else: joins the fleet ahead (its time is absorbed — not added)

    return len(fleets)

# Test
print(carFleet_verbose(12, [10,8,0,5,3], [2,4,1,1,3]))   # 3
print(carFleet_verbose(10, [3], [3]))                       # 1
print(carFleet_verbose(100, [0,2,4], [4,2,1]))             # 1'''),

md('cell-walkthrough', '''## Trace: `target=12, position=[10,8,0,5,3], speed=[2,4,1,1,3]`

After sorting by position descending: `[(10,2), (8,4), (5,1), (3,3), (0,1)]`

| car (pos,spd) | time=(12-pos)/spd | stack (fleet times) | Action |
|---------------|-------------------|---------------------|--------|
| (10, 2) | (12-10)/2 = **1.0** | [1.0] | new fleet |
| (8, 4) | (12-8)/4 = **1.0** | [1.0] | 1.0 ≤ 1.0 → joins fleet |
| (5, 1) | (12-5)/1 = **7.0** | [1.0, 7.0] | 7.0 > 1.0 → new fleet |
| (3, 3) | (12-3)/3 = **3.0** | [1.0, 7.0] | 3.0 ≤ 7.0 → joins fleet |
| (0, 1) | (12-0)/1 = **12.0** | [1.0, 7.0, 12.0] | 12.0 > 7.0 → new fleet |

Result: **3 fleets**. Stack length = number of fleets.'''),

code('cell-optimal-code', '''# Optimal — O(n log n) time (sort dominates), O(n) space

def carFleet(target: int, position: list[int], speed: list[int]) -> int:
    pairs = sorted(zip(position, speed), reverse=True)  # closest to target first
    stack = []   # arrival times of distinct fleets

    for pos, spd in pairs:
        time = (target - pos) / spd
        # New fleet if: stack empty OR arrives AFTER the fleet ahead
        if not stack or time > stack[-1]:
            stack.append(time)
        # else: joins the fleet ahead (slower car determines fleet arrival)

    return len(stack)

# Test
print(carFleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]))   # 3
print(carFleet(10, [3], [3]))                               # 1
print(carFleet(100, [0, 2, 4], [4, 2, 1]))                # 1  — all join same fleet
print(carFleet(10, [6, 8], [3, 2]))                        # 2  — separate fleets'''),

md('cell-complexity', '''## Complexity Analysis

| Step | Time | Notes |
|------|------|-------|
| Sort | O(n log n) | Dominates |
| Stack scan | O(n) | Single pass |
| **Total** | **O(n log n)** | **Sort bound** |

**Space:** O(n) — the stack holds at most n fleet arrival times.

**Why sorting by position descending matters:** A car can only catch up to cars closer to the target. Processing closest-first ensures we evaluate each car's ability to catch the car immediately ahead.'''),

md('cell-qa', '''## Interview Q&A

**Q: Why sort by position descending?**
A: Cars can only catch up to cars ahead (closer to target). Processing closest-to-target first means when we evaluate a car, we can immediately compare it to the fleet it would join.

**Q: Why is arrival time the deciding factor?**
A: If car B (behind) arrives before or at the same time as car A (ahead): B physically catches A before the target, joins A's fleet, and slows to A's speed. B's arrival time becomes A's time.

**Q: What if two cars start at the same position?**
A: The problem states all positions are unique.

**Q: When does time > stack[-1] form a new fleet?**
A: When a car arrives *after* the fleet ahead — it can never catch up. It forms its own fleet with all cars behind it that join it.'''),

md('cell-citi-narrative', '''## The Citi Angle

**The "merging groups" pattern:** Batch jobs or service requests that start at different times but converge on the same resource.

```python
# How many distinct "batches" will reach the database given staggered starts?
# Jobs that arrive within the same second merge into one batch

def count_db_batches(submissions: list[tuple]) -> int:
    """
    submissions: list of (ready_time, processing_rate) pairs.
    Jobs that "catch up" to the job ahead merge into one batch.
    """
    # Sort by ready_time descending (most ready first)
    jobs = sorted(submissions, reverse=True)
    batch_arrivals = []

    db_capacity = 1.0   # 1 unit of work per second
    for ready_time, rate in jobs:
        arrival = ready_time + (1.0 / rate)   # time to complete 1 unit
        if not batch_arrivals or arrival > batch_arrivals[-1]:
            batch_arrivals.append(arrival)

    return len(batch_arrivals)

# 4 jobs at different ready times with different processing rates
submissions = [(0, 2), (1, 1), (2, 3), (5, 1)]
print(f"Distinct DB batches: {count_db_batches(submissions)}")
```

**Interview tie-in:** "Car Fleet maps to any resource contention problem — multiple requestors converging on a shared bottleneck. The stack tracks distinct arrival groups, which equals distinct load spikes on the resource."'''),

md('cell-summary', '''## Summary

| | Value |
|--|--|
| **Pattern** | Sort + Stack |
| **Time** | O(n log n) |
| **Space** | O(n) |
| **Key step** | Sort descending by position; compare arrival times |
| **Say in interview** | "Sort closest-to-target first. For each car, compute arrival time. If it arrives after the fleet ahead, it's a new fleet. Stack length = fleet count." |'''),

]

write_nb(f'{BASE}/lc-0853-car-fleet.ipynb', CAR_FLEET_CELLS)
gen_html('lc-0853-car-fleet', f'{BASE}/lc-0853-car-fleet.ipynb',
         f'{BASE}/lc-0853-car-fleet.html', 853, 'Car Fleet', 'medium')


# =============================================================================
# SQL — COMPLEX JOINs
# =============================================================================

SQL_JOIN_CELLS = [

code('j00-setup', '''import sqlite3
import pandas as pd

conn = sqlite3.connect(':memory:')
conn.executescript("""
CREATE TABLE servers (
    server_id TEXT PRIMARY KEY,
    region TEXT,
    tier TEXT
);
INSERT INTO servers VALUES
    ('srv-01','us-east','gold'),
    ('srv-02','us-east','silver'),
    ('srv-03','us-west','gold'),
    ('srv-04','us-west','bronze'),
    ('srv-05','us-east','silver'),
    ('srv-06','eu-west','gold');

CREATE TABLE daily_metrics (
    server_id TEXT,
    report_date TEXT,
    avg_cpu REAL
);
INSERT INTO daily_metrics VALUES
    ('srv-01','2026-02-26',72.5),
    ('srv-01','2026-02-27',74.1),
    ('srv-02','2026-02-26',45.2),
    ('srv-02','2026-02-27',48.3),
    ('srv-03','2026-02-26',91.3),
    ('srv-03','2026-02-27',89.7),
    ('srv-04','2026-02-26',33.1),
    ('srv-05','2026-02-26',55.0);
    -- srv-06 has NO metrics (gap detection test)
    -- srv-04 and srv-05 missing 2026-02-27 (partial gap)
""")
print("Sample database ready!")
print("Servers: 6 rows | daily_metrics: 8 rows")
print()
print(pd.read_sql_query("SELECT * FROM servers", conn).to_string(index=False))'''),

md('j01', '''# SQL — Complex JOINs
**Day 3 — SQL Module**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>Core Insight:</strong> Most candidates know INNER JOIN. What separates senior engineers:
self-joins, cross joins for combinations, and anti-joins for gap detection.
These show up constantly in data quality, missing-data detection, and combinatorial analysis.
</div>

**Run j00-setup first** to create the sample database.'''),

md('j02', '''## Self Join — Compare Rows Within the Same Table

A self join joins a table to itself. Use it to compare rows within the same table:
- Year-over-year comparison
- Server pairs in the same region
- Sequential record analysis (day-over-day delta)'''),

code('j03', '''# Self Join: find server pairs in the same region with CPU gap > 20%

sql_self = """
SELECT
    a.server_id AS server_1,
    b.server_id AS server_2,
    a.region,
    ROUND(a.avg_cpu, 1) AS cpu_1,
    ROUND(b.avg_cpu, 1) AS cpu_2,
    ROUND(ABS(a.avg_cpu - b.avg_cpu), 1) AS cpu_gap
FROM daily_metrics a
JOIN daily_metrics b
    ON a.report_date = b.report_date
    AND a.server_id < b.server_id       -- avoid (A,B) and (B,A) duplicates
JOIN servers sa ON a.server_id = sa.server_id
JOIN servers sb ON b.server_id = sb.server_id
WHERE sa.region = sb.region             -- same region
  AND a.report_date = '2026-02-26'
  AND ABS(a.avg_cpu - b.avg_cpu) > 20
ORDER BY cpu_gap DESC
"""

result = pd.read_sql_query(sql_self, conn)
print("Server pairs in same region with CPU gap > 20% (date: 2026-02-26):")
print(result.to_string(index=False))
print()
print("Note: 'a.server_id < b.server_id' prevents (srv-01,srv-02) and (srv-02,srv-01) both appearing.")

# Day-over-day delta using self join
sql_dod = """
SELECT
    a.server_id,
    a.report_date AS today,
    b.report_date AS yesterday,
    ROUND(a.avg_cpu, 1) AS today_cpu,
    ROUND(b.avg_cpu, 1) AS yesterday_cpu,
    ROUND(a.avg_cpu - b.avg_cpu, 1) AS delta
FROM daily_metrics a
JOIN daily_metrics b
    ON a.server_id = b.server_id
    AND b.report_date = date(a.report_date, '-1 day')
ORDER BY ABS(a.avg_cpu - b.avg_cpu) DESC
"""

print()
print("Day-over-day CPU delta (self join on server_id + date offset):")
print(pd.read_sql_query(sql_dod, conn).to_string(index=False))'''),

md('j04', '''## Anti-Join — Find Missing Records (Data Gap Detection)

Anti-join returns rows from the left table with NO matching row in the right table.
This is the core pattern for:
- Servers that reported no data yesterday
- Products with no sales
- Users who never logged in

**Three equivalent methods — choose based on your database:**
1. `LEFT JOIN + WHERE right.key IS NULL` — most portable
2. `NOT EXISTS (subquery)` — often most readable
3. `NOT IN (subquery)` — **dangerous with NULLs** — avoid unless you know subquery has no NULLs'''),

code('j05', '''# Anti-Join: servers that reported NO data on 2026-02-27

# Method 1: LEFT JOIN + IS NULL (most portable, works everywhere)
sql_antijoin1 = """
SELECT s.server_id, s.region, s.tier
FROM servers s
LEFT JOIN daily_metrics m
    ON s.server_id = m.server_id
    AND m.report_date = '2026-02-27'
WHERE m.server_id IS NULL
ORDER BY s.server_id
"""
result1 = pd.read_sql_query(sql_antijoin1, conn)
print("Anti-join (LEFT JOIN + IS NULL): servers missing 2026-02-27 data:")
print(result1.to_string(index=False))

# Method 2: NOT EXISTS (readable, safe with NULLs)
sql_antijoin2 = """
SELECT server_id, region, tier
FROM servers s
WHERE NOT EXISTS (
    SELECT 1 FROM daily_metrics m
    WHERE m.server_id = s.server_id
    AND m.report_date = '2026-02-27'
)
ORDER BY server_id
"""
result2 = pd.read_sql_query(sql_antijoin2, conn)
print()
print("Anti-join (NOT EXISTS): same result, different approach:")
print(result2.to_string(index=False))
print()
print("Both return the same servers: those with no row in daily_metrics for 2026-02-27.")
print("srv-06 has NO data at all. srv-04, srv-05 only have 2026-02-26 data.")'''),

md('j06', '''## Cross Join — Generate All Combinations

Cross join produces every combination of rows from two tables.
Use cases:
- Generate a complete grid (server × metric_type)
- Create date × server combinations for gap detection
- Combinatorial analysis

```sql
-- Generate all (server, metric) combinations
SELECT s.server_id, m.metric_type
FROM servers s
CROSS JOIN (VALUES ('cpu'), ('memory'), ('disk')) AS m(metric_type);
-- Then LEFT JOIN actual metrics to find what's missing
```'''),

code('j07', '''# Cross Join: generate all (server, date) combinations, then find gaps

# All servers × all dates in our range
sql_cross = """
SELECT s.server_id, d.report_date
FROM servers s
CROSS JOIN (
    SELECT DISTINCT report_date FROM daily_metrics
) d
ORDER BY s.server_id, d.report_date
"""
all_combos = pd.read_sql_query(sql_cross, conn)
print(f"Cross join: {len(all_combos)} (server, date) combinations")
print(all_combos.head(8).to_string(index=False))

# Now find gaps: combinations that exist in cross join but NOT in daily_metrics
sql_gaps = """
SELECT s.server_id, d.report_date, s.tier
FROM servers s
CROSS JOIN (
    SELECT DISTINCT report_date FROM daily_metrics
) d
WHERE NOT EXISTS (
    SELECT 1 FROM daily_metrics m
    WHERE m.server_id = s.server_id AND m.report_date = d.report_date
)
ORDER BY d.report_date, s.server_id
"""
gaps = pd.read_sql_query(sql_gaps, conn)
print()
print(f"Missing data gaps ({len(gaps)} server-date combinations):")
print(gaps.to_string(index=False))'''),

md('j08', '''## Interview Q&A

**Q: Why is `NOT IN` dangerous with NULLs?**
A: If the subquery returns any NULL value, the entire NOT IN comparison returns NULL for every row — effectively returning no results. Always use NOT EXISTS or LEFT JOIN + IS NULL instead. Rule: never use NOT IN with a subquery unless you can 100% guarantee no NULLs in the subquery result.

**Q: Self-join use cases in data engineering?**
A: Year-over-year comparison (join table to itself on year offset), sequential record pairing (day N vs day N-1), hierarchy traversal (employee to their manager in the same table), finding duplicate records.

**Q: What's a hash join?**
A: Build a hash table from the smaller table, probe it with the larger table. O(n+m). Most databases choose this automatically for large joins. Contrast with nested loop join: O(n×m) — only used for small tables or indexed lookups.

**Q: USING vs ON — when do you use each?**
A: `USING (server_id)` when the join column has the same name in both tables — cleaner, only appears once in SELECT *. `ON a.id = b.server_id` when column names differ or when you want explicitness. Prefer ON for clarity in complex queries.

**Q: What is a broadcast join in Spark?**
A: A small table is replicated to all Spark executors — avoids the expensive shuffle that a regular join would require. Use when one table is small (< a few hundred MB). `F.broadcast(small_df)` hint in PySpark.'''),

md('j09', '''## The Citi Angle

**Data gap detection was a daily operation.** At Citi, 6,000 servers reporting telemetry — any gap meant an agent went down, a network issue occurred, or a server was decommissioned without notice.

**The morning data quality check:**
```sql
-- Run every morning: find servers that didn't report yesterday
SELECT s.server_id, s.region, s.tier,
       MAX(m.report_date) AS last_seen
FROM servers s
LEFT JOIN daily_metrics m ON s.server_id = m.server_id
GROUP BY s.server_id, s.region, s.tier
HAVING MAX(m.report_date) < date('now', '-1 day')
    OR MAX(m.report_date) IS NULL
ORDER BY last_seen NULLS FIRST
```

This query combines LEFT JOIN (for servers with no data at all) with HAVING (for servers whose last report is stale). The result was fed into an alerting pipeline.

**Interview line:** *"Anti-join was the foundation of our data quality monitoring at Citi — LEFT JOIN + IS NULL pattern to detect the 'silent failure' of a server that stopped reporting. We reduced gap detection time from hours to minutes by running this query on a schedule."*'''),

]

write_nb(f'{BASE}/sql-complex-joins.ipynb', SQL_JOIN_CELLS)
print(f'  Written: {BASE}/sql-complex-joins.ipynb')


# =============================================================================
# PYTHON — DECORATORS & CONTEXT MANAGERS
# =============================================================================

DECORATORS_CELLS = [

md('d01', '''# Python — Decorators & Context Managers
**Day 3 — Python Module**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>Core Insight:</strong> Decorators are functions that wrap other functions — adding
behavior (timing, logging, retry) without modifying the original code.
Context managers guarantee cleanup (connections closed, sessions stopped) even if an exception occurs.
Both are fundamental to production Python pipelines.
</div>'''),

code('d02', '''# Basic decorator structure — understand the pattern first
import functools

def my_decorator(func):
    @functools.wraps(func)   # preserves func.__name__, __doc__ — ALWAYS use this
    def wrapper(*args, **kwargs):
        print(f"Before {func.__name__}")
        result = func(*args, **kwargs)
        print(f"After {func.__name__}")
        return result
    return wrapper

@my_decorator
def process_data(n: int) -> int:
    """Doubles a number."""
    return n * 2

result = process_data(5)
print(f"Result: {result}")
print(f"Function name preserved: {process_data.__name__}")   # "process_data" not "wrapper"
print(f"Docstring preserved: {process_data.__doc__}")'''),

code('d03', '''# Timing decorator — essential for pipeline profiling
import functools
import time

def timer(func):
    """Log execution time for any function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

@timer
def simulate_db_query(n_rows: int) -> list:
    """Simulate a database query with n_rows results."""
    time.sleep(0.05)   # 50ms simulated latency
    return list(range(n_rows))

@timer
def process_records(records: list) -> int:
    """Process each record."""
    return sum(r * 2 for r in records)

# Run both — timer wraps each transparently
data = simulate_db_query(1000)
total = process_records(data)
print(f"Processed {len(data)} records, total={total:,}")'''),

code('d04', '''# Retry decorator — resilient data pipeline calls with exponential backoff
import functools, time, random

def retry(max_attempts: int = 3, delay: float = 1.0, exceptions=(Exception,)):
    """
    Retry decorator with exponential backoff.
    max_attempts: total tries (including first)
    delay: initial delay in seconds; doubles each attempt
    exceptions: tuple of exception types to catch
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise   # final attempt — re-raise
                    wait = delay * (2 ** attempt)
                    print(f"[RETRY] {func.__name__} attempt {attempt+1} failed: {e}")
                    print(f"[RETRY] Waiting {wait:.1f}s before retry...")
                    time.sleep(wait)
        return wrapper
    return decorator

# Simulate a flaky API call
call_count = 0

@retry(max_attempts=3, delay=0.1)
def fetch_server_metrics(server_id: str) -> dict:
    global call_count
    call_count += 1
    if call_count < 3:   # fails first 2 times
        raise ConnectionError(f"Transient network error (attempt {call_count})")
    return {"server_id": server_id, "cpu": 72.5, "mem": 68.1}

result = fetch_server_metrics("srv-01")
print(f"\\nSuccess: {result}")'''),

code('d05', '''# Stacking decorators — order matters
# Applied bottom-up, executed outside-in

import functools, time

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[TIMER] {func.__name__}: {time.perf_counter()-start:.4f}s")
        return result
    return wrapper

def log_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__}({args}, {kwargs})")
        return func(*args, **kwargs)
    return wrapper

@timer           # applied second (outer wrapper)
@log_args        # applied first (inner wrapper)
def expensive_etl(n: int, batch_size: int = 100) -> int:
    """Simulate ETL processing."""
    time.sleep(0.02)
    return n // batch_size

# Execution order: timer wraps log_args wraps expensive_etl
# Call sequence: timer.wrapper → log_args.wrapper → expensive_etl
result = expensive_etl(10000, batch_size=50)
print(f"Result: {result}")'''),

code('d06', '''# Context Managers — guaranteed cleanup
import contextlib, time

# Method 1: class-based context manager
class DatabaseConnection:
    """Simulates a database connection with guaranteed cleanup."""
    def __init__(self, conn_string: str):
        self.conn_string = conn_string
        self.conn = None

    def __enter__(self):
        print(f"[DB] Connecting to {self.conn_string}")
        self.conn = {"connected": True, "queries": 0}   # simulated connection
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[DB] Closing connection (ran {self.conn[\'queries\']} queries)")
        self.conn = None
        if exc_type:
            print(f"[DB] Exception occurred: {exc_type.__name__}: {exc_val}")
        return False   # don\'t suppress exceptions

# Normal usage
with DatabaseConnection("sqlite:///telemetry.db") as db:
    db["queries"] += 1
    print(f"  Running query 1... conn={db}")
    db["queries"] += 1
    print(f"  Running query 2...")
print("Connection closed automatically.\\n")

# Method 2: contextlib.contextmanager (simpler)
@contextlib.contextmanager
def timed_section(label: str):
    """Context manager for timing a block of code."""
    start = time.perf_counter()
    print(f"[TIMER] Starting: {label}")
    try:
        yield   # execution of the with block happens here
    finally:
        elapsed = time.perf_counter() - start
        print(f"[TIMER] Done: {label} ({elapsed:.4f}s)")  # always runs

with timed_section("data loading"):
    time.sleep(0.03)
    data = list(range(1000))
    print(f"  Loaded {len(data)} records")'''),

md('d07', '''## Interview Q&A

**Q: What does `@functools.wraps` do and why is it non-negotiable?**
A: Preserves the wrapped function's `__name__`, `__doc__`, `__module__` attributes. Without it, every decorated function shows as "wrapper" in logs, stack traces, and introspection. This breaks debugging, monitoring, and auto-generated documentation.

**Q: What are the three arguments to `__exit__`?**
A: `exc_type`, `exc_val`, `exc_tb` — exception type, value, and traceback. All are None if the with block completed normally. Return True to suppress the exception; False (or None) to re-raise it.

**Q: When would you use a retry decorator in data engineering?**
A: External API calls (Datadog, AWS S3, monitoring endpoints), database connections that may fail transiently. Use exponential backoff to avoid thundering herd. Add jitter (random noise to the delay) in production to prevent synchronized retries.

**Q: Decorator stacking order — how does it work?**
A: Decorators apply bottom-up but execute outside-in. `@timer @log_args def f()` creates `timer(log_args(f))`. When called: timer's wrapper runs first, then calls log_args's wrapper, then the original f.

**Q: Why use a context manager for a Spark session?**
A: Guarantees `spark.stop()` runs even if the job crashes mid-execution — releases cluster resources immediately. Without it, the cluster resources stay allocated until timeout (minutes to hours).'''),

md('d08', '''## The Citi Angle

**Production decorators at Citi:**

```python
import functools, time, logging

# 1. Combined timing + logging decorator (used on every ETL function)
def pipeline_step(step_name: str):
    """Decorator factory: logs timing and errors for each pipeline step."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"STEP START: {step_name}")
            start = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                logging.info(f"STEP DONE: {step_name} ({elapsed:.2f}s)")
                return result
            except Exception as e:
                elapsed = time.perf_counter() - start
                logging.error(f"STEP FAIL: {step_name} ({elapsed:.2f}s) — {e}")
                raise
        return wrapper
    return decorator

@pipeline_step("deduplicate_telemetry")
def deduplicate(df):
    return df.drop_duplicates(subset=["server_id", "collection_date", "metric"])

@pipeline_step("compute_daily_averages")
def compute_averages(df):
    return df.groupby(["server_id", "collection_date"]).mean().reset_index()
```

**Interview line:** *"At Citi, every ETL function was wrapped with a pipeline_step decorator that provided consistent logging, timing, and error reporting. It separated cross-cutting concerns (observability) from business logic — 5 lines of decorator replaced 30+ lines of boilerplate across 50+ functions."*'''),

]

write_nb(f'{BASE}/python-decorators.ipynb', DECORATORS_CELLS)
print(f'  Written: {BASE}/python-decorators.ipynb')


# =============================================================================
# TECHNOLOGY — PIPELINE ARCHITECTURE: LAMBDA & KAPPA
# =============================================================================

PIPELINE_ARCH_CELLS = [

md('l01', '''# Pipeline Architecture: Lambda & Kappa
**Day 3 — Technology Module**

---

<div style="padding:15px;border-left:8px solid #f7971e;background:#fff8e1;border-radius:4px;">
<strong>Core Insight:</strong> Data pipeline architecture boils down to: batch vs streaming vs hybrid.
Lambda architecture separates batch (complete, slow) from streaming (fast, approximate).
Kappa simplifies this to one codebase by treating everything as a stream.
Understanding the trade-offs between them is a senior-level interview topic.
</div>

## Lambda Architecture

```
Source Data
    ↓
    ├── BATCH LAYER (Spark/Hadoop)
    │   Process ALL historical data
    │   Hours/days latency, complete accuracy
    │   Output: batch views
    │
    └── SPEED LAYER (Kafka + Flink/Kinesis)
        Process RECENT data in real-time
        Seconds latency, may be approximate
        Output: real-time views
              ↓
        SERVING LAYER (merges batch + speed views)
              ↓
        Query (reads from both; speed fills recency gap)
```

**Lambda pros:** Batch layer is always correct; speed layer gives low-latency recency.
**Lambda cons:** Two codebases (batch + streaming) for the same logic — they drift apart over time.'''),

md('l02', '''## Kappa Architecture (Simplified Lambda)

```
Source Data → Kafka (append-only log, full history retained)
                ↓
        Stream Processing (Flink / Spark Streaming)
        ONE codebase — handles both real-time and reprocessing
                ↓
        Serving Layer (Cassandra, DynamoDB, S3)
                ↓
        Query

Reprocessing historical data:
  → Replay from Kafka beginning with updated code
  → Same pipeline processes history as if it were new events
```

**Kappa pros:** One codebase, simpler ops, reprocessing = just replay from Kafka.
**Kappa cons:** Keeping full history in Kafka is expensive; not all stream processors handle complex batch semantics well.

**When to choose Kappa over Lambda:**
- Modern stream processor (Flink, Spark Structured Streaming) handles your batch complexity
- You want to avoid maintaining two separate pipelines
- Reprocessing is common (schema changes, bug fixes)'''),

md('l03', '''## Late Data — The Hard Problem

**The scenario:** Events that arrive after their expected processing window has closed.
Example: mobile device offline for 30 minutes, then sends all events when reconnected.

**Solutions:**
1. **Watermarks:** Tell the stream processor "tolerate up to N minutes of late data." Events within the watermark are processed in-window; beyond it, trigger the window result.
2. **Upsert to target:** Accept late events and update the serving layer record rather than ignoring them.
3. **Reprocess from source:** For large late-data batches, replay the relevant time window.

```
Event time: 14:00     (when the event actually occurred)
Processing time: 14:35 (when it arrived at the processor)
Lateness: 35 minutes

Watermark = 30 min → this event is LATE, window already closed
Watermark = 60 min → this event is within tolerance, processed normally
```'''),

md('l04', '''## Real Example — Telemetry Pipeline at Scale

```
6,000 APM agents (CA APM, AppDynamics, Dynatrace, BMC TrueSight)
    │
    ▼
Kafka (10 partitions, 7-day retention, keyed by server_id)
    │
    ├──→ Flink job (real-time)
    │       5-minute tumbling windows
    │       Compute avg/max CPU per server
    │       Threshold alerts → PagerDuty
    │       Write real-time views → Redis (30-second TTL)
    │
    └──→ S3 sink (micro-batch, 5-min)
            Parquet files, partitioned by date + env
                │
                ▼
            Glue Crawler (auto-update catalog)
                │
                ├──→ Athena (ad-hoc SQL, capacity team)
                └──→ Daily Glue ETL
                        → Aggregate summaries
                        → Prophet forecasting input
                        → QuickSight dashboard
```

**This is effectively Kappa:** One source (Kafka), two consumers (real-time + S3), same data model.'''),

code('l05', '''# LOCAL SIMULATION — Kafka-like stream processing with Python queues
# Illustrates the Lambda/Kappa concept without actual Kafka/Flink

import queue, time, threading
from collections import defaultdict
from datetime import datetime

# Simulate Kafka as a simple queue
kafka_topic = queue.Queue()

# Simulate incoming telemetry events
SAMPLE_EVENTS = [
    {"server_id": "srv-01", "cpu": 72.5, "ts": "2026-02-27T10:00:00"},
    {"server_id": "srv-02", "cpu": 91.3, "ts": "2026-02-27T10:00:01"},
    {"server_id": "srv-01", "cpu": 75.1, "ts": "2026-02-27T10:00:02"},
    {"server_id": "srv-03", "cpu": 45.2, "ts": "2026-02-27T10:00:03"},
    {"server_id": "srv-02", "cpu": 93.0, "ts": "2026-02-27T10:00:04"},
    {"server_id": "srv-01", "cpu": 80.4, "ts": "2026-02-27T10:00:05"},
    {"server_id": "srv-03", "cpu": 48.7, "ts": "2026-02-27T10:00:06"},
]

# SPEED LAYER: real-time alert processor (like Flink job)
alerts_fired = []
def speed_layer(event):
    if event["cpu"] > 90:
        alert = f"ALERT: {event[\'server_id\']} CPU={event[\'cpu\']}% at {event[\'ts\']}"
        alerts_fired.append(alert)

# BATCH LAYER: aggregate at end (like Spark job over micro-batch)
batch_buffer = defaultdict(list)
s3_sink = []    # what would be written to S3 Parquet

def batch_layer(events):
    for e in events:
        batch_buffer[e["server_id"]].append(e["cpu"])
    for server_id, cpus in batch_buffer.items():
        s3_sink.append({
            "server_id": server_id,
            "avg_cpu": round(sum(cpus) / len(cpus), 2),
            "max_cpu": max(cpus),
            "sample_count": len(cpus)
        })

# ── Process the stream ───────────────────────────────────────────────────────
print("Processing telemetry stream...")
for event in SAMPLE_EVENTS:
    kafka_topic.put(event)

all_events = []
while not kafka_topic.empty():
    event = kafka_topic.get()
    all_events.append(event)
    speed_layer(event)   # real-time processing

batch_layer(all_events)  # batch processing

print()
print("SPEED LAYER output (real-time alerts):")
for alert in alerts_fired:
    print(f"  {alert}")

print()
print("BATCH LAYER output (would write to S3 Parquet):")
for row in sorted(s3_sink, key=lambda x: x["server_id"]):
    print(f"  {row}")'''),

md('l06', '''## Interview Q&A

**Q: Why would you choose Kappa over Lambda?**
A: Simpler maintenance — one codebase, one team, no drift between batch and stream logic. Modern stream processors (Flink, Spark Structured Streaming) handle complex aggregations, joins, and windowing well enough to replace batch. Choose Kappa when the stream processor can handle all your computation requirements.

**Q: What is "late data" and how do you handle it?**
A: Events that arrive after their processing window has closed. Solutions: watermarks (tolerate N minutes of lateness), upsert to the target table for late corrections, reprocess from Kafka for large late-data volumes.

**Q: What is exactly-once semantics?**
A: Guarantee that each event is processed exactly once — not duplicated, not lost. Hard to achieve in distributed systems. At-least-once + idempotent sinks is a practical alternative: process events at least once, but make the write operation idempotent (same result whether written once or multiple times).

**Q: How would you design a pipeline for 6,000 endpoints producing 1 metric per second?**
A: 6,000 events/sec → Kinesis or Kafka (10 shards/partitions) → Flink or Lambda (real-time alerts, 5-min windowed aggregates) → S3 micro-batches in Parquet → Glue crawler → Athena. Daily Glue job for historical analytics. CloudWatch for orchestration.

**Q: What is a watermark in stream processing?**
A: A timestamp marker that tells the stream processor "all events up to time T have arrived." Events beyond the watermark in lateness are dropped or processed as late. The watermark moves forward as event time advances.'''),

md('l07', '''## The Citi Angle

**This architecture is directly from Citi experience.** Managing 4 APM tools with different data formats was the core challenge.

**The unified telemetry pipeline (real architecture):**
```
4 APM Tools (CA APM, AppDynamics, Dynatrace, BMC TrueSight)
    │ REST API polling (30-min cadence) + agent push (5-min cadence)
    ▼
Custom Python collectors (one per APM tool)
    │ normalize to common schema: {server_id, metric, value, timestamp}
    ▼
Message queue (RabbitMQ in practice, equivalent to Kafka)
    │
    ├──→ Real-time: threshold checks → email + ITSM ticket
    └──→ Batch sink: PostgreSQL + file exports → analytics
                │
                ▼
    Python ETL (pandas) → CSV → Excel reports (manual era)
    Later: S3 → Athena SQL → automated dashboards (target state)
```

**What I'd do differently with modern AWS:**
- Replace RabbitMQ with Kinesis Data Streams
- Replace Python batch ETL with Glue jobs
- Replace PostgreSQL analytics tables with S3 Parquet + Athena
- Add Flink for real-time aggregation instead of threshold-only checks

**Interview line:** *"At Citi, we had a Lambda-style architecture without knowing the name — batch aggregation in nightly jobs and a real-time alerting path from the same event stream. The lesson: keep the two codebases in sync. In Kappa, you get this for free by replaying from the source."*'''),

]

write_nb(f'{BASE}/pipeline-architecture.ipynb', PIPELINE_ARCH_CELLS)
print(f'  Written: {BASE}/pipeline-architecture.ipynb')


print('\nDay 3 generation complete!')
print(f'Output: {BASE}/')
print()
print('LeetCode notebooks + HTML:')
print('  lc-0020-valid-parentheses')
print('  lc-0155-min-stack')
print('  lc-0739-daily-temperatures')
print('  lc-0853-car-fleet')
print()
print('Concept notebooks:')
print('  sql-complex-joins.ipynb')
print('  python-decorators.ipynb')
print('  pipeline-architecture.ipynb')
