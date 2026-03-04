---
description: Convert LeetCode problem text into a structured Jupyter Notebook (.ipynb) study guide.
---

# LC-TEXT-TO-NOTEBOOK (Skill 24)

**Trigger Statement:** `"lc notebook: [paste problem text] — folder: [Destination Folder Path]"`

**Instructions for the Agent:**
0. **Reference Notebook Constraint:** Before you generate any JSON, you MUST use the `view_file` tool to read `D:\Workspace\StudyMaterial\Day1\lc-0001-two-sum.ipynb`. Pay extremely close attention to its unique 12-cell dual-pattern structure, ASCII diagrams, and cost tables before proceeding.

1. **JSON Structure Foundation:**
   - The `.ipynb` format is strictly JSON. **Do not** use an external reference file; instead, construct the complete JSON skeleton in memory.
   - You must adhere to standard JSON escaping rules (`"` becomes `\"`, `\` becomes `\\`).
   - Every string in the `source` array must end with `\n` EXCEPT the last line of the cell.

2. **Cell Templates:**
   - **Markdown Cells:** Must have `"cell_type": "markdown"`, `"metadata": {}`, and `"source": [...]`.
   - **Code Cells:** Must have `"cell_type": "code"`, `"metadata": {}`, `"execution_count": null`, `"outputs": []`, and `"source": [...]`.

3. **Mandatory 10 Cells & Fixed Order:**
   Construct exactly 10 cells with these exact metadata tags (or inferred order to be compatible with `_gen_html.py`):
   1. `cell-title` (Markdown)
   2. `cell-problem` (Markdown)
   3. `cell-insight` (Markdown)
   4. `cell-mental-models` (Markdown)
   5. `cell-test-suite` (Code)
   6. `cell-brute-code` (Code)
   7. `cell-optimal-code` (Code)
   8. `cell-complexity` (Markdown)
   9. `cell-qa` (Markdown)
   10. `cell-citi-angle` (Markdown)

4. **Tree Problems Requirement:**
   - For any problem tagged or related to Trees/Binary Trees, `cell-brute-code` MUST start with the full `TreeNode` class definition and a `build_tree` helper function.

5. **Practice Problem Generation:**
   - You MUST generate a "Practice Problem" extension block in the appropriate cell (or as part of Q&A/Summary). Use a lookup strategy to ensure the recommended practice problem is a natural extension of the current concept, rather than an unrelated problem.

6. **Comprehensive Testing Suite & Test Cases:**
   - **`cell-test-suite`**: Must contain a robust, generalized test runner function (e.g., `def run_tests(test_cases, func):`) that iterates through inputs, passes them to the arbitrary function, and compares the result to the expected output cleanly.
   - **Inline Solution Execution**: At the bottom of *every* solution code cell (e.g., `cell-brute-code` and `cell-optimal-code`), you MUST configure the problem's specific test cases and invoke the `run_tests` function (e.g., `run_tests(test_cases, twoSum)`) to prove the solution works inside the notebook.

7. **Output Execution:**
   - Ensure the JSON is valid and well-formed.
   - Use the `write_to_file` tool to save the `.ipynb` file to the requested destination folder.
   - Auto-generate a descriptive slugified filename (e.g., `lc-0167-two-sum-ii.ipynb`).