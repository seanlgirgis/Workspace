# Game Rules

1. **Workspace Operations**: For the directory structure starting at `d:\Workspace` and any directories below it, the agent should proceed with listing, creating directories, creating files, or deleting files as needed without asking for permission.
2. **Script Execution**: The agent should not ask for permission before executing scripts that have actions within this workspace directory.
3. **Automatic Environment Setup**: The agent MUST always run the `/setup_python_env` skill at the beginning of every session or when Python execution is required to ensure the environment is correctly configured.
