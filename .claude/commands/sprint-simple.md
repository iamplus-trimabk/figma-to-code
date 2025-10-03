---
description: "Create sprint with actual implementation - branches, docs, story templates"
allowed_tools: ["Bash", "Write", "Read", "Edit"]
---

Create sprint: **$ARGUMENTS**

## 🏃 Sprint Creation Implementation

### Step 1: Parse Arguments and Setup
```bash
# Expected format: "Sprint Name" under EPIC-XXX
SPRINT_NAME=$(echo "$ARGUMENTS" | sed 's/ under.*//')
EPIC_ID=$(echo "$ARGUMENTS" | sed 's/.* under //')

# Generate sprint ID
SPRINT_COUNT=$(find "docs/epics/$EPIC_ID/sprints" -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
SPRINT_ID="SPRINT-$(printf "%03d" $((SPRINT_COUNT)))"

echo "Creating Sprint: $SPRINT_ID - $SPRINT_NAME under $EPIC_ID"
```

### Step 2: Create Sprint Branch
```bash
# Create sprint branch
SPRINT_BRANCH="epic/$EPIC_ID/$SPRINT_ID/planning"
git checkout -b "$SPRINT_BRANCH"
echo "✅ Created branch: $SPRINT_BRANCH"
```

### Step 3: Create Sprint Documentation
```bash
# Create sprint directory and files
mkdir -p "docs/epics/$EPIC_ID/sprints/$SPRINT_ID"/{stories,tasks}

cat > "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/README.md" << EOF
# $SPRINT_ID: $SPRINT_NAME

## Sprint Details
- **Sprint ID**: $SPRINT_ID
- **Sprint Name**: $SPRINT_NAME
- **Epic**: $EPIC_ID
- **Status**: Planning
- **Created**: $(date)
- **Branch**: $SPRINT_BRANCH

## Sprint Goal
Define the main goal and deliverables for this sprint.

## Sprint Backlog
- [ ] Story 1: [To be defined]
- [ ] Story 2: [To be defined] 
- [ ] Story 3: [To be defined]

## Acceptance Criteria
- [ ] All stories completed
- [ ] Tests written and passing
- [ ] Code reviewed and approved
- [ ] Documentation updated

## Story Creation
Use: \`/story "As user I want..." in $SPRINT_ID\`

## Team Capacity
- Available story points: 20-30
- Sprint duration: 2 weeks
- Team members: 2-3 developers

## Definition of Done
- [ ] Feature implemented
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Deployed to staging
EOF

echo "✅ Created sprint documentation"
```

### Step 4: Create Story Templates
```bash
# Create story template directory
mkdir -p "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/story-templates"

cat > "docs/epics/$EPIC_ID/sprints/$SPRINT_ID/story-templates/story-template.md" << EOF
# STORY-XXX: [Story Title]

## User Story
**As a** [user type]
**I want** [goal/desire]
**So that** [benefit/value]

## Acceptance Criteria
Given [context]
When [action]
Then [outcome]

## Technical Requirements
- [ ] Frontend changes needed
- [ ] Backend API changes
- [ ] Database changes
- [ ] Third-party integrations

## Task Breakdown
- [ ] Task 1: [Implementation detail]
- [ ] Task 2: [Implementation detail]
- [ ] Task 3: [Testing]
- [ ] Task 4: [Documentation]

## Definition of Done
- [ ] Feature works as described
- [ ] All acceptance criteria met
- [ ] Tests written and passing
- [ ] Code reviewed
- [ ] Documentation updated
EOF

echo "✅ Created story templates"
```

### Step 5: Update Epic Tracking
```bash
# Update epic README with sprint info
EPIC_README="docs/epics/$EPIC_ID/README.md"
if grep -q "## Sprint Breakdown" "$EPIC_README"; then
    # Add sprint to existing breakdown
    sed -i.bak "/## Sprint Breakdown/a\\
- [x] **$SPRINT_ID**: $SPRINT_NAME (Created)" "$EPIC_README"
else
    echo "⚠️ Epic README not found or format unexpected"
fi

echo "✅ Updated epic tracking"
```

### Step 6: Project Logging
```bash
# Log sprint creation
echo "Sprint $SPRINT_ID created: $SPRINT_NAME" >> .claude/project-log.txt
echo "Epic: $EPIC_ID" >> .claude/project-log.txt  
echo "Branch: $SPRINT_BRANCH" >> .claude/project-log.txt
echo "Created: $(date)" >> .claude/project-log.txt
echo "---" >> .claude/project-log.txt

echo "✅ Updated project log"
```

### Step 7: Output Results
```bash
echo ""
echo "🎉 SPRINT CREATED SUCCESSFULLY!"
echo ""
echo "Sprint Details:"
echo "- ID: $SPRINT_ID"
echo "- Name: $SPRINT_NAME"  
echo "- Epic: $EPIC_ID"
echo "- Branch: $SPRINT_BRANCH"
echo "- Documentation: docs/epics/$EPIC_ID/sprints/$SPRINT_ID/"
echo ""
echo "Next Steps:"
echo "1. /story \"As user I want to login\" in $SPRINT_ID"
echo "2. /story \"As user I want to logout\" in $SPRINT_ID"
echo "3. /story \"As user I want password reset\" in $SPRINT_ID"
echo ""
echo "Current Branch:"
git branch --show-current
```

**This sprint command actually CREATES:**
- Real git branch for sprint
- Real sprint documentation
- Story templates ready to use
- Updates epic tracking
- Ready for story creation