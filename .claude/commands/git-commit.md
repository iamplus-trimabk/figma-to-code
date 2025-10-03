---
description: "Smart commit with auto-generated message, impact analysis, and context preservation"
allowed_tools: ["Bash", "Read", "Grep", "Glob", "Write"]
---

Smart git commit with intelligent analysis and context preservation.

## 🔍 Git Commit Process

### Phase 1: Change Analysis
1. **Scan Current Changes**
   - Run `git status` to see all modified, added, and deleted files
   - Run `git diff --staged` and `git diff` to understand changes
   - Identify scope: features, fixes, refactoring, docs, tests, etc.

2. **Impact Assessment**
   - Analyze files changed and their relationships
   - Identify breaking changes or API modifications
   - Check for security implications
   - Assess test coverage for changes

### Phase 2: Context Detection
1. **Project Context**
   - Read current epic/sprint/story from .claude/project.json active context
   - Check if changes align with current story objectives
   - Identify which team member profile is committing (trimabk/sarthak)

2. **Technical Context**
   - Determine technology stack affected (React, Node.js, TypeScript, MongoDB)
   - Identify patterns: component changes, API updates, database migrations
   - Check for dependency updates or configuration changes

### Phase 3: Commit Message Generation
1. **Conventional Commits Format**
   ```
   <type>(<scope>): <description>
   
   <body>
   
   <footer>
   ```

2. **Message Components**
   - **Type**: feat, fix, refactor, docs, test, chore, style, perf, ci
   - **Scope**: epic/sprint/story context or component affected
   - **Description**: Clear, imperative mood, 50 chars max
   - **Body**: Detailed explanation of changes and reasoning
   - **Footer**: Breaking changes, closes issues, references

### Phase 4: Quality Checks
1. **Pre-commit Validation**
   - Check for secrets or sensitive data in changes
   - Validate code follows project conventions
   - Ensure no debugging code or console.logs remain
   - Check for TODO comments or incomplete work

2. **Test Integration**
   - Run quick linting if available
   - Check if tests need to be updated
   - Suggest test additions for new features

### Phase 5: Context Preservation
1. **Decision Documentation**
   - Document why changes were made, not just what
   - Include architectural decisions or trade-offs
   - Reference epic/sprint/story objectives
   - Note future considerations or follow-up work

2. **Team Handoff Context**
   - Include information needed for code review
   - Note integration points or dependencies
   - Highlight areas needing special attention

### Example Output Format
```bash
# Proposed commit message:
feat(auth): implement email login with JWT validation

- Add EmailLoginForm component with validation
- Create JWT authentication service
- Implement login API endpoint with bcrypt password hashing
- Add login integration tests

Addresses user story AUTH-001: "As a user I want to login with email"
Epic: User Authentication System (EPIC-001)

Breaking: Changes login API response format
Closes: #123
```

### Phase 6: Execution
1. **Stage Files Intelligently**
   - Stage related changes together
   - Separate unrelated changes into different commits
   - Handle new files and deletions appropriately

2. **Commit Execution**
   - Execute git commit with generated message
   - Verify commit was successful
   - Show commit hash and summary

### Expected Deliverables
- [ ] Comprehensive change analysis
- [ ] Context-aware commit message following conventions
- [ ] Quality checks and validation
- [ ] Proper file staging and commit execution
- [ ] Team handoff context preservation

**Smart commit should align with current epic/sprint/story context and follow the active team member's profile approach (architect vs developer perspective).**