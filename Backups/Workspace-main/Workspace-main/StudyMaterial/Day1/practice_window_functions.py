import duckdb
import pandas as pd

# Sample employee data
employees = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan'],
    'department': ['IT', 'IT', 'IT', 'Sales', 'Sales', 'HR', 'HR', 'HR', 'IT'],
    'salary': [90000, 120000, 115000, 80000, 95000, 60000, 65000, 50000, 90000]
})

# Sample telemetry data for rolling averages (the "Citi" scenario)
telemetry = pd.DataFrame({
    'server_id': ['S1', 'S1', 'S1', 'S1', 'S1', 'S2', 'S2', 'S2'],
    'collection_date': pd.to_datetime([
        '2026-02-20', '2026-02-21', '2026-02-22', '2026-02-23', '2026-02-24', 
        '2026-02-20', '2026-02-21', '2026-02-22'
    ]),
    'cpu_utilization': [45.5, 50.2, 55.8, 80.1, 85.0, 30.0, 31.5, 30.8]
})

# Connect to in-memory DuckDB
con = duckdb.connect()

# Load DataFrames into DuckDB tables
con.execute("CREATE TABLE employees AS SELECT * FROM employees")
con.execute("CREATE TABLE telemetry AS SELECT * FROM telemetry")

print("Created DuckDB in-memory database with two tables: 'employees' and 'telemetry'")

# Example Query
print("\n--- Testing connection: First 3 Employees ---")
print(con.sql("SELECT * FROM employees LIMIT 3").df())

print(f"""
    Rolling 3-day average of CPU utilization per server:
    {con.sql('''
    SELECT server_id, collection_date, cpu_utilization, 
    AVG(cpu_utilization) OVER 
    (PARTITION BY server_id ORDER BY collection_date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS rolling_avg 
    FROM telemetry
    ''').df()}
    """)
print("\n--- Example: Teaching the CTE + Window Function ---")
print("""
# The Goal: We want to only show employees who are ranked #1 in their department by salary.
# The Problem: We can't put a window function inside a WHERE clause like this: 
#      WHERE RANK() OVER (...) = 1   <-- THIS WILL CRASH SQL

# The Solution: Put the window function inside a Common Table Expression (CTE) first.
# Think of a CTE as just creating a virtual table on the fly so we can filter its columns in the real query.
""")

example_query = """
WITH RankedEmployees AS (
    -- Step 1: Create our virtual table with the rank column attached
    SELECT 
        name, 
        department, 
        salary,
        RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
    FROM employees
)
-- Step 2: Now we can filter that virtual column exactly like a normal column!
SELECT name, department, salary 
FROM RankedEmployees 
WHERE salary_rank = 1;
"""

print(con.sql(example_query).df())

print("\n--- Your Turn: The Practice Problem ---")
print("Challenge: Write a CTE query to find the Top 2 highest-paid employees in each department.\n (Hint: change the WHERE clause of the example!)")
print("You can practice writing SQL queries directly against 'con' using con.sql(\"\"\" SELECT ... \"\"\").df()")

query2 = """
WITH RankedEmployees AS (
    -- Step 1: Create our virtual table with the rank column attached
    SELECT 
        name, 
        department, 
        salary,
        RANK() OVER (PARTITION BY department ORDER BY salary DESC) as salary_rank
    FROM employees
)
-- Step 2: Now we can filter that virtual column exactly like a normal column!
SELECT name, department, salary 
FROM RankedEmployees 
WHERE salary_rank <=2 ;
"""
print(con.sql(query2).df())

print("\n\n" + "="*50)
print("LESSON 3: TIME TRAVEL (LAG and LEAD)")
print("="*50)

print("""
# The Concept:
# Sometimes you don't want an aggregate (AVG) or a rank. You just want to look at the row *before* this one, or the row *after* this one.
# LAG() = Look backwards (What was the value yesterday?)
# LEAD() = Look forwards (What is the value tomorrow?)

# The Citi Interview Answer:
# "At Citi I used LAG() extensively to monitor telemetry. Instead of doing a massive, expensive Self-Join to compare today's CPU usage to yesterday's, I just used LAG(cpu_utilization, 1) to pull yesterday's value right next to today's. Then I could easily calculate the day-over-day spike."
""")

lag_example_query = """
SELECT 
    server_id,
    collection_date,
    cpu_utilization as cpu_today,
    -- Pull the value from 1 row ago (chronologically)
    LAG(cpu_utilization, 1) OVER (PARTITION BY server_id ORDER BY collection_date) as cpu_yesterday
FROM telemetry
"""

print("\n--- Example: Comparing Today to Yesterday ---")
print(con.sql(lag_example_query).df())

print("\n--- Your Turn: The Growth Spike Challenge ---")
print("""Challenge: Write a CTE that uses the LAG query above, and then filters for *only* the days 
        where the CPU utilization spiked by more than 10 points compared to the day before.""")
print("(Hint: Where cpu_today - cpu_yesterday > 10)")

# Write your query3 here!

lag_query2 = """
with anamoly_telemetry as (
SELECT 
    server_id,
    collection_date,
    cpu_utilization as cpu_today,
    -- Pull the value from 1 row ago (chronologically)
    LAG(cpu_utilization, 1) OVER (PARTITION BY server_id ORDER BY collection_date) as cpu_yesterday
FROM telemetry) select * from anamoly_telemetry
WHERE (cpu_today - cpu_yesterday) > 10
"""
print("\n--- Example: Comparing Today to Yesterday Show only %10 jump ---")
print(con.sql(lag_query2).df())