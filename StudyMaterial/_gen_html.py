import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BSLASH = chr(92)

PROBLEMS = {
    'lc-0704-binary-search':          (704,  'Binary Search',                       'easy',   'Binary Search', 4),
    'lc-0033-search-rotated':         (33,   'Search in Rotated Sorted Array',      'medium', 'Binary Search', 4),
    'lc-0153-find-minimum-rotated':   (153,  'Find Minimum in Rotated Sorted Array','medium', 'Binary Search', 4),
    'lc-0074-search-2d-matrix':       (74,   'Search a 2D Matrix',                  'medium', 'Binary Search', 4),
    'lc-0981-time-based-kv':          (981,  'Time Based Key-Value Store',           'medium', 'Binary Search', 4),
    'lc-0703-kth-largest-stream':     (703,  'Kth Largest Element in a Stream',     'easy',   'Heap', 5),
    'lc-1046-last-stone-weight':      (1046, 'Last Stone Weight',                   'easy',   'Heap', 5),
    'lc-0973-k-closest-points':       (973,  'K Closest Points to Origin',          'medium', 'Heap', 5),
    'lc-0215-kth-largest-array':      (215,  'Kth Largest Element in an Array',     'medium', 'Heap', 5),
    'lc-0295-median-data-stream':     (295,  'Find Median from Data Stream',        'hard',   'Heap', 5),
    'lc-0056-merge-intervals':        (56,   'Merge Intervals',                     'medium', 'Intervals', 6),
    'lc-0057-insert-interval':        (57,   'Insert Interval',                     'medium', 'Intervals', 6),
    'lc-0435-non-overlapping':        (435,  'Non-overlapping Intervals',           'medium', 'Intervals', 6),
    'lc-0253-meeting-rooms-ii':       (253,  'Meeting Rooms II',                    'medium', 'Intervals', 6),
    'lc-0986-interval-intersections': (986,  'Interval List Intersections',         'medium', 'Intervals', 6),
}

THEMES = {
    'Binary Search': ('#f093fb', '#f5576c', '#d94f8a'),
    'Heap':          ('#fa709a', '#fee140', '#e05b85'),
    'Intervals':     ('#a18cd1', '#fbc2eb', '#8a5cc4'),
}

def join_source(source):
    return ''.join(source)

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def md_inline(text):
    text = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    return text

def md_to_html(text, accent='#667eea'):
    lines = text.split('\n')
    out = []
    in_code = False
    code_buf = []
    in_list = False
    in_table = False
    table_has_header = False

    def flush_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def flush_table():
        nonlocal in_table, table_has_header
        if in_table:
            out.append('</tbody></table>')
            in_table = False
            table_has_header = False

    for line in lines:
        # Code fence
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
                    f'<code>{code_html}</code></pre>'
                )
                code_buf = []
            else:
                code_buf.append(line)
            continue

        s = line.strip()

        # Table rows
        if s.startswith('|'):
            flush_list()
            cols = [c.strip() for c in s.split('|')[1:-1]]
            if all(re.match(r'^[-: ]+$', c) for c in cols):
                continue  # separator row
            if not in_table:
                in_table = True
                table_has_header = True
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

        # Pass-through HTML blocks
        if s.startswith('<') and not s.startswith('<strong') and not s.startswith('<em') and not s.startswith('<code'):
            flush_list()
            out.append(line)
            continue

        # LaTeX / math (just show as italic text)
        if s.startswith('$$') or s.startswith('\\('):
            flush_list()
            out.append(f'<p style="color:#555;font-style:italic;text-align:center;margin:8px 0;">{escape_html(s)}</p>')
            continue

        # Headings
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            flush_list()
            lvl = min(len(m.group(1)) + 1, 5)
            sizes = {2:'1.4em', 3:'1.15em', 4:'1.0em', 5:'0.95em'}
            sz = sizes.get(lvl, '1em')
            color = accent if lvl <= 3 else '#444'
            out.append(f'<h{lvl} style="color:{color};font-size:{sz};margin:16px 0 8px;">{md_inline(m.group(2))}</h{lvl}>')
            continue

        # HR
        if s == '---':
            flush_list()
            out.append('<hr style="border:0;border-top:1px solid #eee;margin:14px 0;">')
            continue

        # Checkbox list items
        if re.match(r'^-\s+\[[ xX]\]', s):
            checked = re.match(r'^-\s+\[[xX]\]', s) is not None
            label = re.sub(r'^-\s+\[[ xX]\]\s*', '', s)
            chk = '&#9745;' if checked else '&#9744;'
            if not in_list:
                out.append('<ul style="list-style:none;margin-left:10px;color:#555;">')
                in_list = True
            out.append(f'<li style="margin:4px 0;">{chk} {md_inline(label)}</li>')
            continue

        # Regular list items
        lm = re.match(r'^[-*]\s+(.*)', s)
        if lm:
            if not in_list:
                out.append('<ul style="margin-left:20px;color:#555;line-height:1.8;">')
                in_list = True
            out.append(f'<li>{md_inline(lm.group(1))}</li>')
            continue

        # Numbered list
        nm = re.match(r'^\d+\.\s+(.*)', s)
        if nm:
            if not in_list:
                out.append('<ol style="margin-left:20px;color:#555;line-height:1.8;">')
                in_list = True
            out.append(f'<li>{md_inline(nm.group(1))}</li>')
            continue

        # Blank
        if not s:
            if in_list: pass
            else: out.append('')
            continue

        # Paragraph
        flush_list()
        out.append(f'<p style="color:#555;line-height:1.7;margin:8px 0;">{md_inline(s)}</p>')

    flush_list()
    flush_table()
    return '\n'.join(out)


def get_cells(nb_path):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)
    cells = {}
    for cell in nb['cells']:
        cid = cell.get('id', '')
        src = join_source(cell.get('source', []))
        ctype = cell.get('cell_type', 'markdown')
        cells[cid] = (ctype, src)
    return cells


def gen_html(slug, nb_path, html_path, num, title, difficulty, pattern, day):
    cells = get_cells(nb_path)
    g1, g2, accent = THEMES[pattern]

    def get(cid):
        return cells.get(cid, ('markdown', ''))[1]

    c1  = get('cell-title')
    c2  = get('cell-mental-models')
    c5  = get('cell-complexity')
    c7  = get('cell-optimal-code')
    c8  = get('cell-qa')
    c10 = get('cell-citi-narrative')
    c12 = get('cell-summary')

    diff_color = {'easy': '#155724', 'medium': '#856404', 'hard': '#721c24'}[difficulty]
    diff_bg    = {'easy': '#d4edda', 'medium': '#fff3cd', 'hard': '#f8d7da'}[difficulty]
    c7_escaped = escape_html(c7)

    def section(icon, heading, content_html, extra_style=''):
        return f'''
<div class="card" style="{extra_style}">
<h2 style="color:{accent};font-size:1.3em;font-weight:600;margin-bottom:16px;">{icon} {heading}</h2>
{content_html}
</div>'''

    grid_open  = '<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:28px;">'
    grid_close = '</div>'

    body_parts = [
        section('📋', 'Problem + Core Insight', md_to_html(c1, accent)),
        grid_open,
        section('🧠', 'Mental Models', md_to_html(c2, accent)),
        section('📊', 'Complexity Analysis', md_to_html(c5, accent)),
        grid_close,
        section('🚀', 'Optimal Solution',
            f'<pre style="background:#1e1e1e;color:#d4d4d4;padding:20px;border-radius:8px;'
            f'overflow-x:auto;font-size:0.88em;line-height:1.5;"><code>{c7_escaped}</code></pre>'),
        section('🎤', 'Interview Q&amp;A', md_to_html(c8, accent)),
        section('💼', 'The Citi Angle',
            f'<div style="background:#fff8e1;border-left:5px solid {accent};padding:18px;border-radius:8px;">'
            + md_to_html(c10, accent) + '</div>'),
        section('🎯', 'Summary', md_to_html(c12, accent)),
    ]

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LC #{num} \u2014 {title} \u2014 {pattern}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
       background: linear-gradient(135deg, {g1} 0%, {g2} 100%);
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
<p class="subtitle">{pattern} Pattern &nbsp;|&nbsp; Day {day} Study Material</p>
{"".join(body_parts)}
</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  OK: {html_path}')


BASE = 'D:/Workspace/StudyMaterial'
for slug, (num, title, diff, pattern, day) in PROBLEMS.items():
    nb_path   = f'{BASE}/Day{day}/{slug}.ipynb'
    html_path = f'{BASE}/Day{day}/{slug}.html'
    if not os.path.exists(nb_path):
        print(f'  SKIP (no notebook): {nb_path}')
        continue
    print(f'Generating: {slug}...')
    try:
        gen_html(slug, nb_path, html_path, num, title, diff, pattern, day)
    except Exception as e:
        print(f'  ERROR: {e}')
        import traceback; traceback.print_exc()

print('\nAll HTML done!')
