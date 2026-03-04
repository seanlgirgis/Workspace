import json
import os

path = r'D:\Workspace\StudyMaterial\Day10\dbt-architecture.ipynb'

with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    cell_id = cell.get('id')
    
    # cell d03: SQL code formatted as python code cell, causing SyntaxError. Change to markdown.
    if cell_id == 'd03':
        cell['cell_type'] = 'markdown'
        if 'outputs' in cell:
            del cell['outputs']
        if 'execution_count' in cell:
            del cell['execution_count']
        
        # Add markdown code block around source
        source = cell['source']
        cell['source'] = ['```sql\n'] + source + ['```\n']

    # cell d05: YAML code formatted as python code cell, causing SyntaxError. Change to markdown.
    elif cell_id == 'd05':
        cell['cell_type'] = 'markdown'
        if 'outputs' in cell:
            del cell['outputs']
        if 'execution_count' in cell:
            del cell['execution_count']
            
        source = []
        source.append('```yaml\n')
        for line in cell['source']:
            if '"""' not in line and '# Production dbt Testing (YAML configuration)' not in line and '# File: models/staging/schema.yml' not in line:
                source.append(line)
        source.insert(0, '# Production dbt Testing (YAML configuration)\n')
        source.insert(1, '# File: models/staging/schema.yml\n')
        source.append('```\n')
        cell['source'] = source

    # cell d07: Syntax error due to unclosed string literal in Python code
    elif cell_id == 'd07':
        # Clear output since code will change
        if 'outputs' in cell:
            cell['outputs'] = []
            
        new_source = []
        for line in cell['source']:
            if 'conn.executescript("CREATE TABLE raw_events (event_id TEXT, ts TEXT);\\n' in line:
                new_source.append('conn.executescript("""CREATE TABLE raw_events (event_id TEXT, ts TEXT);\\n')
            elif '                 INSERT INTO raw_events VALUES (\'e3\', \'2026-02-27\');")\\n' in line:
                new_source.append('                 INSERT INTO raw_events VALUES (\'e3\', \'2026-02-27\');""")\\n')
            else:
                new_source.append(line)
        cell['source'] = new_source

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)

print("Notebook fixed gracefully.")
