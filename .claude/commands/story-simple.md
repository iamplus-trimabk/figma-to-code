---
description: "Create user story with actual implementation - branches, tasks, acceptance criteria"
allowed_tools: ["Bash", "Write", "Read", "Edit"]
---

Create user story: **$ARGUMENTS**

## 📖 Story Creation Implementation

### Step 1: Parse Arguments and Setup
```bash
# Expected format: "As user I want..." in SPRINT-XXX
STORY_DESCRIPTION=$(echo "$ARGUMENTS" | sed 's/ in.*//')
SPRINT_ID=$(echo "$ARGUMENTS" | sed 's/.* in //')

# Find epic from sprint
EPIC_ID=$(find docs/epics -name "$SPRINT_ID" -type d | cut -d'/' -f3)

# Generate story ID
STORY_COUNT=$(find "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories" -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
STORY_ID="STORY-$(printf "%03d" $((STORY_COUNT + 1)))"

echo "Creating Story: $STORY_ID - $STORY_DESCRIPTION in $SPRINT_ID"
```

### Step 2: Create Story Branch
```bash
# Create story planning and implementation branches
STORY_PLANNING_BRANCH="epic/$EPIC_ID/$SPRINT_ID/$STORY_ID/planning"
STORY_IMPL_BRANCH="epic/$EPIC_ID/$SPRINT_ID/$STORY_ID/implementation"

git checkout -b "$STORY_PLANNING_BRANCH"
git checkout -b "$STORY_IMPL_BRANCH"
git checkout "$STORY_PLANNING_BRANCH"

echo "✅ Created branches: planning and implementation"
```

### Step 3: Create Story Documentation
```bash
# Create story directory structure
mkdir -p "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories/$STORY_ID"/{tasks,tests,acceptance}

cat > "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories/$STORY_ID/README.md" << EOF
# $STORY_ID: $STORY_DESCRIPTION

## User Story
$STORY_DESCRIPTION

## Story Details
- **Story ID**: $STORY_ID
- **Sprint**: $SPRINT_ID
- **Epic**: $EPIC_ID
- **Status**: Planning
- **Created**: $(date)
- **Planning Branch**: $STORY_PLANNING_BRANCH
- **Implementation Branch**: $STORY_IMPL_BRANCH

## Acceptance Criteria
**Given** [initial context/state]
**When** [user action/trigger]
**Then** [expected outcome/result]

**Given** [another context]
**When** [another action]
**Then** [another outcome]

## Technical Requirements
- [ ] Frontend Components Needed
- [ ] Backend API Endpoints
- [ ] Database Schema Changes
- [ ] Third-party Integrations
- [ ] Authentication/Authorization

## Task Breakdown
- [ ] **Planning**: Define detailed requirements
- [ ] **Design**: UI/UX mockups and API design
- [ ] **Backend**: Implement API endpoints
- [ ] **Frontend**: Implement UI components
- [ ] **Testing**: Unit and integration tests
- [ ] **Documentation**: Update API and user docs
- [ ] **Review**: Code review and approval

## Estimation
- **Story Points**: [1, 2, 3, 5, 8, 13]
- **Effort**: [hours estimated]
- **Complexity**: Low/Medium/High
- **Risk Level**: Low/Medium/High

## Dependencies
- [ ] Dependency 1: [Description]
- [ ] Dependency 2: [Description]

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Feature deployed to staging
- [ ] Stakeholder approval received

## Implementation Notes
[Add any technical notes, decisions, or considerations]

## Testing Strategy
- **Unit Tests**: Test individual functions/components
- **Integration Tests**: Test API endpoints and data flow
- **E2E Tests**: Test complete user workflow
- **Manual Tests**: UI/UX validation

EOF

echo "✅ Created story documentation"
```

### Step 4: Create Acceptance Criteria Template
```bash
cat > "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories/$STORY_ID/acceptance/acceptance-criteria.md" << EOF
# Acceptance Criteria: $STORY_ID

## Scenario 1: [Main Happy Path]
**Given** the user is [initial state]
**When** the user [performs action]  
**Then** the system should [expected result]
**And** [additional verification]

## Scenario 2: [Edge Case]
**Given** the user has [different state]
**When** the user [performs action]
**Then** the system should [handle gracefully]

## Scenario 3: [Error Handling]
**Given** [error condition exists]
**When** the user [attempts action]
**Then** the system should [show appropriate error]
**And** [guide user to resolution]

## Validation Checklist
- [ ] User can successfully complete main workflow
- [ ] Error messages are clear and helpful
- [ ] UI is responsive and accessible
- [ ] Data is validated and secure
- [ ] Performance meets requirements
EOF

echo "✅ Created acceptance criteria"
```

### Step 5: Create Task Template
```bash
cat > "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories/$STORY_ID/tasks/implementation-tasks.md" << EOF
# Implementation Tasks: $STORY_ID

## Backend Tasks
- [ ] **API Design**: Define endpoint specifications
- [ ] **Data Model**: Create/update database schema
- [ ] **Business Logic**: Implement core functionality
- [ ] **Validation**: Add input validation and error handling
- [ ] **Testing**: Write unit and integration tests
- [ ] **Documentation**: Update API documentation

## Frontend Tasks  
- [ ] **Component Design**: Create UI component structure
- [ ] **State Management**: Implement data flow
- [ ] **User Interface**: Build responsive UI
- [ ] **Form Handling**: Add validation and submission
- [ ] **Testing**: Write component and E2E tests
- [ ] **Styling**: Implement design system

## Integration Tasks
- [ ] **API Integration**: Connect frontend to backend
- [ ] **Error Handling**: Implement error boundaries
- [ ] **Loading States**: Add loading and empty states
- [ ] **Navigation**: Update routing if needed
- [ ] **Security**: Implement authorization checks

## Quality Assurance
- [ ] **Unit Tests**: >80% code coverage
- [ ] **Integration Tests**: All API endpoints
- [ ] **E2E Tests**: Complete user workflow
- [ ] **Performance**: Load time <2 seconds
- [ ] **Accessibility**: WCAG compliance
- [ ] **Security**: Input validation and sanitization
EOF

echo "✅ Created implementation tasks"
```

### Step 6: Update Sprint Tracking
```bash
# Update sprint README with story
SPRINT_README="docs/epics/$EPIC_ID/sprints/$SPRINT_ID/README.md"
if grep -q "## Sprint Backlog" "$SPRINT_README"; then
    sed -i.bak "/## Sprint Backlog/a\\
- [ ] **$STORY_ID**: $STORY_DESCRIPTION" "$SPRINT_README"
fi

echo "✅ Updated sprint tracking"
```

### Step 7: Project Logging
```bash
# Log story creation
echo "Story $STORY_ID created: $STORY_DESCRIPTION" >> .claude/project-log.txt
echo "Sprint: $SPRINT_ID" >> .claude/project-log.txt
echo "Epic: $EPIC_ID" >> .claude/project-log.txt
echo "Branches: $STORY_PLANNING_BRANCH, $STORY_IMPL_BRANCH" >> .claude/project-log.txt
echo "Created: $(date)" >> .claude/project-log.txt
echo "---" >> .claude/project-log.txt

echo "✅ Updated project log"
```

### Step 8: Output Results
```bash
echo ""
echo "🎉 USER STORY CREATED SUCCESSFULLY!"
echo ""
echo "Story Details:"
echo "- ID: $STORY_ID"
echo "- Description: $STORY_DESCRIPTION"
echo "- Sprint: $SPRINT_ID"  
echo "- Epic: $EPIC_ID"
echo "- Planning Branch: $STORY_PLANNING_BRANCH"
echo "- Implementation Branch: $STORY_IMPL_BRANCH"
echo "- Documentation: docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories/$STORY_ID/"
echo ""
echo "Next Steps:"
echo "1. Fill out acceptance criteria"
echo "2. Break down implementation tasks"
echo "3. Estimate story points"
echo "4. Begin implementation on implementation branch"
echo ""
echo "Current Branch:"
git branch --show-current
echo ""
echo "Available Branches:"
git branch | grep "$EPIC_ID"
```

**This story command actually CREATES:**
- Real git branches (planning + implementation)
- Complete story documentation
- Acceptance criteria templates
- Task breakdown structure
- Updates sprint tracking
- Ready for actual development work