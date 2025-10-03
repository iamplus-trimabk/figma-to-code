---
description: "Create sprint under existing epic with story templates and detailed planning"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Grep", "Glob"]
---

Create sprint: **$ARGUMENTS**

## 🏃 Sprint Creation Process

**Expected format**: `/sprint [Sprint Goal/Name] under [EPIC-ID]`
**Example**: `/sprint Login & Registration under EPIC-001`

### Phase 1: Sprint Analysis
1. **Parse Epic Context**
   - Read existing epic documentation from docs/epics/EPIC-XXX/
   - Understand epic scope and current progress
   - Identify sprint position in overall epic timeline

2. **Sprint Scope Definition**
   - Define clear sprint goal and deliverables
   - Estimate 1-2 week duration based on team capacity
   - Identify sprint-specific success criteria
   - Map to epic acceptance criteria

### Phase 2: Git Branch Structure
1. **Create Sprint Branch**
   - Format: `epic/EPIC-XXX/sprint-YYY/planning`
   - Branch from epic planning branch
   - Create git worktree for sprint development

2. **Sprint Documentation**
   ```
   docs/epics/EPIC-XXX/sprints/SPRINT-YYY/
   ├── sprint-overview.md
   ├── sprint-goal.md
   ├── story-breakdown.md
   ├── acceptance-criteria.md
   ├── testing-plan.md
   └── handoff-template.md
   ```

### Phase 3: Story Breakdown
1. **User Story Creation**
   - Break sprint into 5-8 user stories maximum
   - Follow "As a [user], I want [goal] so that [benefit]" format
   - Define story points (1, 2, 3, 5, 8, 13)
   - Prioritize stories by business value and dependencies

2. **Story Templates**
   - Create markdown template for each story
   - Include acceptance criteria
   - Define testing requirements
   - Set up handoff checkpoints

### Phase 4: Planning Artifacts
1. **Sprint Backlog**
   - Prioritized list of stories
   - Story point estimates
   - Dependencies and blockers
   - Definition of done criteria

2. **Team Assignments**
   - Map stories to team member profiles
   - Consider expertise and capacity
   - Plan handoff sequences

### Phase 5: Database Registration
1. **Sprint Entry**
   - Add sprint to SQLite database
   - Link to parent epic
   - Set status to 'planning'
   - Record created_by from active profile

2. **Story Placeholders**
   - Create story entries in database
   - Link to sprint
   - Set initial estimates and priorities

### Expected Deliverables
- [ ] Sprint planning documentation
- [ ] Git branch structure for sprint
- [ ] User story breakdown with templates
- [ ] Sprint backlog with priorities
- [ ] Database entries for tracking
- [ ] Handoff templates ready

**Align with project technology stack and current team profile approach (architect vs developer focus).**