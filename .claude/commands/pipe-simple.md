---
description: "Simple pipeline executor that reads markdown task lists and executes them sequentially"
allowed_tools: ["TodoWrite", "Task", "Read", "Write", "Bash"]
---

Execute pipeline from markdown file: **$ARGUMENTS**

## 🔄 Simple Pipeline Executor

**This is the actual implementation of /pipe command**

### How it works:
1. Read pipeline markdown file from `.claude/pipelines/[name].md`
2. Parse all Task sections
3. Add each task to TodoWrite
4. Execute tasks sequentially
5. Pass context file between tasks
6. Mark todos as completed as we go

### Pipeline Execution Process:

```python
# Pseudo-code for what Claude does:

1. pipeline_file = read(".claude/pipelines/$ARGUMENTS.md")
2. tasks = parse_tasks(pipeline_file)
3. context_file = "./pipeline-context.md"

4. TodoWrite(tasks) # Add all tasks to todo list

5. for task in tasks:
    - Set todo status: "in_progress"
    - Read context from previous tasks
    - Execute task prompt (which may include slash commands)
    - Write output to context file
    - Set todo status: "completed"
    
6. Generate final report from context
```

### Example Pipeline File Structure:
```markdown
## Task 1: [Name]
**Prompt**: /epic Create User System
**Context**: None

## Task 2: [Name]  
**Prompt**: /sprint Planning under EPIC-001
**Context**: ./pipeline-context.md
```

### What makes this brilliant:
- No complex YAML needed
- Just markdown with tasks
- Claude's existing TodoWrite tool tracks progress
- Context accumulates naturally
- Slash commands work as-is
- Dead simple to understand and create

### To execute:
1. Find pipeline file: `.claude/pipelines/$ARGUMENTS.md`
2. Parse tasks from markdown
3. Create todo list with all tasks
4. Execute each task's prompt
5. Pass context between tasks via file
6. Complete todos as tasks finish

This IS the pipe implementation - using Claude's existing capabilities!