---
description: Convert tech/architecture text into a structured Jupyter Notebook (.ipynb) study guide.
---
# TECH/ARCHITECTURE TEXT-TO-NOTEBOOK (Skill 27)

**Trigger Statement:** `"tech notebook: [description] — folder: [Destination Folder Path]"`

**Instructions for the Agent:**

0. **Reference Notebook Constraint:** Before you generate any JSON, you MUST use the `view_file` tool to read `D:\Workspace\StudyMaterial\Day1\aws-data-platform.ipynb`. Pay extremely close attention to its unique 12-cell dual-pattern structure, ASCII diagrams, and cost tables before proceeding.

1. **JSON Structure Foundation:**
   - The `.ipynb` format is strictly JSON. Construct the complete JSON skeleton in memory.
   - Adhere to standard JSON escaping rules (`"` becomes `\"`, `\` becomes `\\`).
   - Every string in the `source` array must end with `\n` EXCEPT the last line of the cell.

2. **Mandatory 12 Cells & Specific Dual-Pattern Order:**
   Construct exactly 12 cells based strictly on the sample notebook. You must prefix the cell tags using the first letter of the topic (e.g., `[a01]` for AWS, `[k01]` for Kafka).
   
   - **`[prefix]01` (Markdown):** Intro + ASCII overview diagram + blue insight box (color: `#667eea`).
   - **`[prefix]02` (Markdown):** Service 1: sub-sections + ASCII tree + tradeoff table.
   - **`[prefix]03` (Code):** Production SDK code (e.g., boto3, awsglue, real DB drivers). This cell represents production code, so **it does not need embedded mock outputs**. Use comments indicating how it behaves in production.
   - **`[prefix]03b` (Code):** Local simulation code. This is the **crucial dual-pattern**: replicate the exact logical behavior of `[prefix]03` but exclusively using local Python stdlib, pandas, strings, or dicts so it runs seamlessly locally. **MUST** have standard expected text outputs embedded in the JSON.
   - **`[prefix]04` (Markdown):** Service 2 explanation.
   - **`[prefix]05` (Code):** Production API pattern code. No outputs needed.
   - **`[prefix]05b` (Code):** Stdlib simulation of Service 2. **MUST** have standard expected text outputs embedded.
   - **`[prefix]06` (Markdown):** Service 3 explanation with a **Cost Math Table** highlighting pay-per-use pricing.
   - **`[prefix]07` (Code):** SQLite + pandas query demo simulating Service 3. **MUST** have standard expected text outputs embedded.
   - **`[prefix]08` (Markdown):** Full ASCII architecture overview (using `│ ├──→ └──→` branching styles) + a governance/security note (e.g., IAM, Lake Formation, RBAC).
   - **`[prefix]09` (Markdown):** Exactly 5 Q&A pairs. **CRITICAL Formatting:** Use `**Q:**` in bold, appending `<br>` at the end of the line so that `A:` starts on the immediate next line visually. **DO NOT** use any `---` thematic breaks between the questions. **HOWEVER**, you MUST include a blank markdown string (`"\\n",`) between each distinct Q&A pair so Jupyter's markdown engine doesn't collapse them all into a single paragraph. **Content Rule:** Question 5 MUST always be: *"Design a pipeline to..."* end-to-end.
   - **`[prefix]10` (Markdown):** **Citi Angle** — Narrative header containing a quantified Before/After bullet list, followed by an explicitly *italicized* interview quote `*"..."*`.

3. **Output Expectations:**
   - In the simulation code blocks (`03b`, `05b`, `07`), you must hard-code the simulated standard output inside the JSON `outputs` mapping array identical to the sample `.ipynb` behavior.
   - Generate a slugified filename: `[topic]-architecture.ipynb` (e.g., `aws-data-platform.ipynb`).
   - Use the `write_to_file` tool to save the `.ipynb` file to the destination folder parameter.
