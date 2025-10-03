---
description: "Create comprehensive epic with planning docs, git branches, and sprint breakdown"
allowed_tools: ["Bash", "Write", "Read", "TodoWrite", "Edit", "Glob", "LS"]
---

Create a comprehensive epic for: **$ARGUMENTS**

## 🎯 Epic Creation Process

**Use the current active profile approach** (architect vs developer focused based on `active_profile` in .claude/project.json).

### Phase 1: Epic Planning
1. **Epic Analysis**
   - Break down the epic requirements
   - Identify key user personas and use cases
   - Define success criteria and acceptance criteria
   - Analyze technical complexity and dependencies

2. **Architecture Planning** (if trimabk profile)
   - System design implications
   - Integration points and dependencies
   - Scalability and performance considerations
   - Security and compliance requirements

3. **Implementation Planning** (if sarthak profile)
   - Technology stack alignment with project.json
   - Component breakdown and development approach
   - Testing strategy and quality gates
   - Deployment and rollout strategy

### Phase 2: Git Structure Creation
1. **Create Epic Branch**
   - Format: `epic/EPIC-XXX/planning` where XXX is auto-incremented
   - Create git worktree for parallel development
   - Set up branch protection and tracking

2. **Documentation Structure**
   ```
   docs/epics/EPIC-XXX/
   ├── epic-overview.md
   ├── requirements.md
   ├── architecture.md (if architect)
   ├── implementation-plan.md (if developer)
   ├── testing-strategy.md
   └── sprint-breakdown.md
   ```

### Phase 3: Sprint Breakdown
1. **Sprint Planning**
   - Break epic into 2-3 sprints maximum
   - Define sprint goals and deliverables
   - Estimate story points and complexity
   - Identify dependencies and blockers

2. **Story Templates**
   - Create user story templates for each sprint
   - Define acceptance criteria
   - Set up handoff points between team members

### Phase 4: Database & Tracking
1. **Epic Registration**
   - Add epic to SQLite database (data/sqlite/project.db)
   - Set status to 'planning'
   - Assign to current profile user

2. **Handoff Preparation**
   - Create handoff template for planning → implementation
   - Document all context and decisions
   - Set up review checkpoints

### Expected Deliverables
- [ ] Epic planning documentation
- [ ] Git branch structure with worktrees
- [ ] Sprint breakdown with story templates
- [ ] Database entry for tracking
- [ ] Handoff template for next phase

**Use comprehensive analysis and follow the current project's technology stack from .claude/project.json**