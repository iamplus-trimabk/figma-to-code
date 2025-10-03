---
description: "Quick git pipeline for add, commit, and push operations"
allowed_tools: ["Bash", "Write", "Read"]
---

Execute git pipeline: **$ARGUMENTS**

## 🔄 Git Pipeline Execution

**Usage**: `/git-pipe [commit-message]`
**Examples**: 
- `/git-pipe "feat: add new feature"`
- `/git-pipe "fix: resolve authentication bug"`
- `/git-pipe` (uses smart commit message generation)

### Quick Git Pipeline

This is a streamlined pipeline for common git operations.

### Pipeline Steps:

1. **Git Status Check**
   ```bash
   git status --short
   ```
   Show what files will be included

2. **Smart Add**
   ```bash
   # Add all relevant files based on changes
   git add -A
   ```
   Stage all changes intelligently

3. **Pre-commit Review**
   Use `/git-self-review` to check changes before committing

4. **Smart Commit**
   If no message provided, use `/git-commit` to generate intelligent commit message
   Otherwise use provided message

5. **Push to Remote**
   ```bash
   git push origin HEAD
   ```
   Push to current branch on origin

### Expected Flow:
- Check current changes
- Review what will be committed  
- Generate or use commit message
- Create commit
- Push to remote repository

This provides a quick way to execute the full git workflow with a single command!