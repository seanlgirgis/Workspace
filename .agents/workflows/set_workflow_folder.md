---
description: Set the default destination folder for all subsequent notebook/study guide generation workflows. Automatically creates the folder if it does not exist.
---
# SET WORKFLOW FOLDER (State Manager)

**Trigger Statement:** `"set folder: [Destination Folder Path]"`

**Instructions for the Agent:**

1. **Folder Verification & Creation:**
   - You MUST use the `run_command` tool (PowerShell) to check if the `[Destination Folder Path]` exists.
   - If it does not exist, use `run_command` (`New-Item -ItemType Directory -Force -Path "[Destination Folder Path]"`) to create it.
   - **Do not** ask the user for permission to create the folder if it's missing; just create it proactively to save time.

2. **State Management (The Core Purpose):**
   - Acknowledge to the user that this folder path is now the **default implicit target** for all subsequent `/tech_text_to_notebook`, `/python_text_to_notebook`, and similar generation workflows in this conversation.
   - For all future workflow triggers in this chat session (e.g., if the user just types `@[/python_text_to_notebook] [description]`), you MUST automatically append the `-folder: "[Destination Folder Path]"` argument in your mind before executing the generation skill.
   - You are acting as a stateful memory bank. The user no longer needs to type `-folder: ...` on every single prompt.

3. **User Confirmation:**
   - Reply to the user with a brief confirmation message: *"Default workspace folder set and verified at: `[Destination Folder Path]`. All future script generators in this session will output here unless explicitly overridden."*
