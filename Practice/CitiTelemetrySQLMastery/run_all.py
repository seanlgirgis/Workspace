import os
import psycopg2
import pandas as pd
from urllib.parse import quote_plus

# Database Connection Settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "practice_db"
DB_USER = "postgres"
DB_PASS = "mysecretpassword"

# SQLAlchemy connection string compatible format for pandas
conn_str = f"postgresql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def run_query(query: str):
    """Executes a SQL query and returns the result as a DataFrame."""
    try:
        # We use SQLAlchemy connection string format with pandas
        df = pd.read_sql(query, conn_str)
        return df
    except Exception as e:
        print(f"Error executing query:\n{e}")
        return None

def main():
    print("==================================================")
    print("Citi Telemetry SQL Mastery - Execution Environment")
    print("==================================================")
    
    print("\nTesting database connection...")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        print("✅ Successfully connected to PostgreSQL!")
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    print("\n--- Available Tables ---")
    tables_query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
    """
    df_tables = run_query(tables_query)
    if df_tables is not None and not df_tables.empty:
        print(df_tables.to_string(index=False))
    else:
        print("No tables found. Did you run setup.sql?")
        
    print("\n--- Example Execution: Top 5 Employees by Salary ---")
    example_query = """
    SELECT e.name, d.dept_name, e.salary
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
    ORDER BY salary DESC
    LIMIT 5;
    """
    df_example = run_query(example_query)
    if df_example is not None:
        print(df_example.to_string(index=False))

    print("\nReady! You can use this script to test your exercise queries by replacing the 'example_query' variable.")

if __name__ == "__main__":
    main()
