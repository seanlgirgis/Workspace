---
created: 2026-03-02
updated: 2026-03-02
summary: Day 88 — Tools and environment setup. Getting your dev environment ready before Day 1.
tags: [study-plan, day-88, week-13, tools-setup, dev-environment, productivity]
---

# Day 88 — Tools + Environment Setup

**Theme:** Senior engineers who are immediately productive on Day 1 have usually set up their environment before they arrived. The tooling you can pre-configure is time you save from onboarding overhead.

---

## Daily Maintenance (15 min)

**LC — Light (1 problem, 10 min):**
LC #121 Best Time to Buy and Sell Stock — write it from memory (`min_price = inf`, `max_profit = 0`, one pass). Classic, quick, clears the cobwebs.

**SQL — One last time:**
Write from memory whichever CTE or window function pattern you still want to make automatic. Pick the one you'd be least comfortable being asked in your first week.

---

## Environment Setup Session (75 min)

### What You Can Set Up Before Day 1

Most companies will provide a new laptop, but you'll often have some flexibility to configure your own tooling. Prepare your standard setup so you can deploy it quickly.

---

**Terminal and Shell**

- Install/configure your preferred terminal: Windows Terminal, iTerm2, or built-in
- Shell config: if you have a `.zshrc` or `.bashrc` with aliases and functions you rely on — back it up and know what's in it
- Key aliases you probably use:
  - `alias gs='git status'`, `alias gd='git diff'`
  - `alias py='python3'` or your venv shortcut
  - `ll` for `ls -la`

**Git Configuration**

```bash
git config --global user.name "Sean Girgis"
git config --global user.email "your.work.email@company.com"
git config --global core.editor "code --wait"   # or vim, nano
git config --global init.defaultBranch main
git config --global pull.rebase false
```

Know how to configure Git for an enterprise environment (SSH keys, GPG signing if required, corporate proxy settings if applicable).

**Python Setup**

You're using `C:/py_venv/proj_educate/Scripts/python.exe` in this vault, but for professional work:
- Understand your company's standard Python version (3.11, 3.12?)
- Be ready to use `uv`, `pyenv`, `conda`, or whatever virtualenv management the team uses
- Standard packages you'll want immediately: `pandas`, `pyspark`, `boto3`, `sqlalchemy`, `dbt-core`, `great_expectations`

**VS Code / IDE Setup**

Extensions to have ready (install when you get the new machine):
- Python extension (Pylance)
- SQL Formatter
- GitLens
- Rainbow CSV (for quick CSV inspection)
- Jupyter (if notebooks are in your workflow)
- Thunder Client or REST Client (for API testing)
- Docker (if containers are in scope)

**DuckDB CLI**

If you've been using DuckDB for SQL practice (as in this study plan), install the CLI on your work machine early. It's a zero-dependency portable binary. Great for ad hoc SQL on local data without spinning up infrastructure.

---

### Productivity System at Work

Think about how you'll manage work:
- Where will you track tasks? (Company Jira/Linear, or personal system alongside it)
- How will you take meeting notes? (Obsidian, Notion, just a text file)
- How will you manage your calendar? (Default blocking strategies)

**Calendar hygiene from Day 1:**
- Block "focus time" on your calendar early — before it fills with meetings
- Don't accept every recurring meeting invitation. In the first 2 weeks, you'll be added to things. Evaluate each one after 30 days.

---

### Your Personal Knowledge System at Work

You've been using this vault to capture technical knowledge. At work, you'll want a similar system — but separate from personal notes.

Options:
- Confluence / Notion (whatever the company uses) for shared documentation
- A personal `notes/` folder in your dotfiles or local vault for things not worth sharing
- A running "things I learned" document in the first 90 days

The goal: don't rely on memory for things you've seen once. Write it down. Your future self will thank you.

---

## Day 88 Checklist

- [ ] LC #121 written from memory (one pass, min_price + max_profit)
- [ ] Last-priority SQL pattern written from memory
- [ ] Terminal + shell config documented (ready to deploy on new machine)
- [ ] Git global config commands ready
- [ ] VS Code extensions list prepared
- [ ] Productivity system decided: task tracking + note-taking approach
- [ ] Calendar hygiene strategy: focus time blocking plan
