---
description: Automatically process a daily study plan markdown file, create the destination folder, and generate all required notebooks and HTML guides.
---
# PROCESS DAILY STUDY PLAN (Super Workflow)

**Trigger Statement:** `"process study plan: [Path to Study Plan MD File]"`
Example: `process study plan: D:\Workspace\outbox\study-plan-day-10.md`

**Instructions for the Agent:**

1. **Extract Day & Set Folder:**
   - Extract the day identifier from the file name. For example, if the file is `study-plan-day-10.md`, the identifier is `Day10`.
   - Determine the destination folder path, e.g., `D:\Workspace\StudyMaterial\Day10`.
   - Execute the **`set_workflow_folder`** workflow logic to verify/create this folder and set it as the default output folder for the duration of the task.

2. **Read and Parse the Document:**
   - Use the `view_file` tool to read the contents of the provided study plan markdown file.
   - Analyze the document and segment it into its logical subject sections (e.g., LeetCode, SQL, Python, Technology/Architecture).
   - *Note: Be adaptable. Not all files contain all sections. Only process the sections that actually exist in the file.*

3. **Iterative Generation Pipeline:**
   Iterate through the extracted sections and execute the appropriate sub-workflows using the parsed text. Since the default folder is already set, you just need to pass the extracted descriptions.

   - **LeetCode Section(s):**
     - Carefully split the LeetCode content so that each individual problem is isolated.
     - For **EACH** discrete LeetCode problem, you MUST run the generation process **TWICE**:
       1. Apply the **`lc_text_to_html`** workflow to generate the HTML study guide card.
       2. Apply the **`lc_text_to_notebook`** workflow to generate the Jupyter Notebook.

   - **SQL Section:**
     - If an SQL section exists, extract its full content and apply the **`sql_text_to_notebook`** workflow.

   - **Python Section:**
     - If a Python section exists, extract its full content and apply the **`python_text_to_notebook`** workflow.

   - **Technology / Architecture Section:**
     - If a Tech or Architecture section exists, extract its full content and apply the **`tech_text_to_notebook`** workflow.

4. **Execution Rules:**
   - Act autonomously. You do not need to pause and ask the user for permission between each section.
   - Use task boundaries to keep your progress organized and visible to the user as you iterate through the different sections of the document.
   - Ensure you use the exact formatting rules defined in the individual sub-workflows when generating the content.

5. **Completion Summary:**
   - Once the entire document is processed, provide a final confirmation to the user listing exactly which files were successfully generated and placed into the day's folder.

6. **Git Commit & Push:**
   - Execute the `gitq` command in the `D:\Workspace` directory to automatically check in and commit all newly generated materials to GitHub.
