---
description: Convert Python topic descriptions into a structured Jupyter Notebook (.ipynb) study guide following the exact 10-cell Python model structure.
---

# PYTHON TEXT-TO-NOTEBOOK (Skill 26)

**Trigger Statement:** `"python notebook: [description] — folder: [Destination Folder Path]"`

**Instructions for the Agent:**

0. **Reference Notebook Constraint:** Before you generate any JSON, you MUST use the `view_file` tool to read `D:\Workspace\StudyMaterial\Day1\python-generators.ipynb`. Pay extremely close attention to its exact metadata tags, HTML styling, and markdown structure before proceeding.

1. **JSON Structure Foundation:**
   - The `.ipynb` format is strictly JSON. Construct the complete JSON skeleton in memory.
   - Adhere to standard JSON escaping rules (`"` becomes `\"`, `\` becomes `\\`).
   - Every string in the `source` array must end with `\n` EXCEPT the last line of the cell.

2. **Mandatory 10 Cells & Fixed Order:**
   Construct exactly 10 cells based strictly on the sample notebook. You must prefix the cell tags using the first letter of the topic (e.g., `[g01]` for generators, `[d01]` for decorators, `[a01]` for async).
   
   - **`[prefix]01` (Markdown):** Title + blue insight box (color: `#667eea`) + "Why It Matters" section.
   - **`[prefix]02` (Markdown):** Static markdown reference card — syntax variants with `# → output` comments.
   - **`[prefix]03` (Code):** Runnable demo: concept 1 proving efficiency (employ `sys.getsizeof()` or `time.time()` execution timing proof). **MUST** have expected textual console outputs pre-rendered directly into the JSON `outputs` array.
   - **`[prefix]04` (Markdown):** Mechanics explanation detailing a numbered execution model.
   - **`[prefix]05` (Code):** Runnable demo: concept 2 utilizing embedded `io.StringIO` streaming mock data. Data MUST use Citi-adjacent fields (e.g., `srv-01`, `cpu_pct`, `production/staging/dev`). **MUST** have standard outputs embedded.
   - **`[prefix]06` (Code):** Pipeline showcase — demonstrating a lazy, functional chain (e.g. `parse → filter → enrich → materialize once`). **MUST** have standard outputs embedded.
   - **`[prefix]07` (Markdown):** Introduction markdown for concept 3 (integrating standard library modules like `itertools`, `functools`, etc.).
   - **`[prefix]08` (Code):** Tool library demo — 4–6 functions exhibiting the concept, each with a `# → output` comment inline and actual execution outputs embedded in the JSON.
   - **`[prefix]09` (Markdown):** Exactly 5 Q&A pairs. **CRITICAL:** Use `**Q:**` in bold, appending `<br>` at the end of the line so that `A:` starts on the immediate next line visually. **DO NOT** use any `---` thematic breaks between the questions. **HOWEVER**, you MUST include a blank markdown line (`"\\n",`) between each distinct Q&A pair so Jupyter's markdown engine doesn't collapse them all into a single massive paragraph.
   - **`[prefix]10` (Markdown):** **Citi Angle** — Narrative header containing a python code block modeling the scenario, followed by an explicitly *italicized* interview quote `*"..."*` representing a plausible workplace explanation.

3. **Output Expectations:**
   - In all code blocks (`03`, `05`, `06`, `08`), you must hard-code the simulated standard output inside the JSON `outputs` mapping array identical to the sample `.ipynb` behavior, reflecting the data printed.
   - Generate a slugified filename: `python-[topic].ipynb` (e.g., `python-decorators.ipynb`).
   - Use the `write_to_file` tool to save the `.ipynb` file to the destination folder parameter.
