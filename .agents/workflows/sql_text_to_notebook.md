---
description: Convert SQL topic descriptions into a structured Jupyter Notebook (.ipynb) study guide with PostgreSQL and DuckDB execution templates.
---

# SQL TEXT-TO-NOTEBOOK (Skill 25)

**Trigger Statement:** `"sql notebook: [description] — folder: [Destination Folder Path]"`

**Instructions for the Agent:**

0. **Reference Notebook Constraint:** Before you generate any JSON, you MUST use the `view_file` tool to read `D:\Workspace\StudyMaterial\Day2\sql-window-functions-advanced.ipynb`. Pay extremely close attention to its unique 12-cell dual-pattern structure, ASCII diagrams, and cost tables before proceeding.

1. **JSON Structure Foundation:**
   - The `.ipynb` format is strictly JSON. Construct the complete JSON skeleton in memory.
   - Adhere to standard JSON escaping rules (`"` becomes `\"`, `\` becomes `\\`).
   - Every string in the `source` array must end with `\n` EXCEPT the last line of the cell.

2. **Mandatory 9 Cells & Fixed Order:**
   Construct exactly 9 cells with these specific IDs mapping to their contents:
   
   - **`c01` (Markdown):** Intro with topic title, green HTML insight box (`#1a8a5a`), and a Citi capacity-planning narrative.
   - **`c02` (Code):** PostgreSQL runner: **EXACT** `run_sql()` template via sqlalchemy. (DO NOT MODIFY THIS BLOCK).
   - **`c03` (Code):** DuckDB setup: `CREATE TABLE [name] AS VALUES ...` containing realistic mock data that matches the requirements for all SQL examples in the subsequent cells. **CRITICAL:** Because this is a DDL operation, do NOT use `run_sql()`. Instead, explicitly execute it with: `with engine.connect() as conn: conn.execute(text(setup_sql)); conn.commit()` to prevent SQLAlchemy mapping errors.
   - **`c04` (Code):** SQL pattern cell #1 using `run_sql(sql)` + DuckDB parallel block + explanation comments + expected output notes.
   - **`c05` (Code):** SQL pattern cell #2 using `run_sql(sql)` + DuckDB parallel block + explanation comments + expected output notes.
   - **`c06` (Code):** SQL pattern cell #3 using `run_sql(sql)` + DuckDB parallel block + explanation comments + expected output notes.
   - **`c07` (Code):** SQL pattern cell #4 using `run_sql(sql)` + DuckDB parallel block + explanation comments + expected output notes.
   - **`c08` (Markdown):** 5 interview Q&A in **Q1: ...** bold format with `---` separators.
   - **`c09` (Markdown):** 8–10 Key Terms table + canonical SQL snippet + 5-item checklist + closing signature: `"Simplicity and clarity is Gold." — Sean's Study Mantra 🚀`

3. **Cell 02 (c02) Exact Template:**
   You MUST emit the following precise Python code in `c02`:
   ```python
   import pandas as pd
   from sqlalchemy import create_engine, text
   from urllib.parse import quote_plus
   
   # Your existing settings
   DB_HOST = "localhost"
   DB_PORT = "5432"
   DB_NAME = "practice_db"
   DB_USER = "postgres"
   DB_PASS = "mysecretpassword"
   
   conn_str = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
   engine = create_engine(conn_str)
   
   def run_sql(query: str):
       try:
           with engine.connect() as conn:
               result = conn.execute(text(query))
               df = pd.DataFrame(result.mappings())   # ← this handles SQLAlchemy 2.0+
               display(df)
       except Exception as e:
           print(f"Error executing query:\n{e}")
   
   print("✅ Fixed SQL execution environment ready!")
   ```

4. **Cell 04-07 Pattern Execution:**
   SQL code cells MUST define the query string and execute it via `run_sql(sql)`, for example:
   ```python
   sql=\"\"\"
   -- Ex 1. Above-average earners using a named CTE
   -- Return: name, dept_name, salary, dept_avg, difference
   WITH calc AS ( ... )
   SELECT ... FROM calc
   \"\"\"
   run_sql(sql)
   ```

5. **PostgreSQL Syntax Constraints (Hard Rules):**
   - **`generate_series()`:** In PostgreSQL, `generate_series(start, end, step)` natively returns a set of rows. **DO NOT** wrap it in `UNNEST()` (e.g. `SELECT UNNEST(generate_series...)` will cause an UndefinedFunction error). Correct usage: `SELECT generate_series('2026-02-01'::DATE, '2026-02-14'::DATE, INTERVAL '1 day')::DATE`.
   - **DDL Commits:** Always use `conn.commit()` after `CREATE TABLE` and `DROP TABLE` execution (as enforced in `c03`), because `.mappings()` cannot be safely called on queries that do not return rows.

6. **Output Execution & Naming:**
   - Ensure the JSON is valid and well-formed.
   - Auto-generate a descriptive slugified filename: `sql-[topic].ipynb` (e.g., `sql-case-when-pivot.ipynb`).
   - Use the `write_to_file` tool to save the `.ipynb` file to the requested destination folder.

7. **Escalation Path:**
   - If SQL environment setup (`c02`) fails consistently during local execution tests, log the stack trace and escalate promptly.