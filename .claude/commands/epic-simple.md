---
description: "Create epic with actual implementation - git branches, docs, and structure"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Glob"]
---

Create epic: **$ARGUMENTS**

## 🎯 Epic Creation Implementation

### Step 1: Generate Epic ID and Setup
```bash
# Generate next epic ID
EPIC_COUNT=$(find docs/epics -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
EPIC_ID="EPIC-$(printf "%03d" $((EPIC_COUNT + 1)))"
echo "Creating Epic: $EPIC_ID - $ARGUMENTS"
```

### Step 2: Create Git Branch Structure
```bash
# Create epic planning branch
git checkout -b "epic/$EPIC_ID/planning"
echo "✅ Created branch: epic/$EPIC_ID/planning"

# Create sprint planning branches
git checkout -b "epic/$EPIC_ID/sprint-001/planning"
git checkout -b "epic/$EPIC_ID/sprint-002/planning"
git checkout "epic/$EPIC_ID/planning"
echo "✅ Created sprint branches"
```

### Step 3: Create Documentation Structure
```bash
# Create epic directories
mkdir -p "docs/epics/$EPIC_ID"/{sprints,stories,handoffs}
mkdir -p "docs/epics/$EPIC_ID/sprints"/{sprint-001,sprint-002,sprint-003}
mkdir -p ".claude/epics/$EPIC_ID"

echo "✅ Created directory structure"
```

### Step 4: Create Epic Documentation
```bash
# Create epic overview
cat > "docs/epics/$EPIC_ID/README.md" << EOF
# $EPIC_ID: $ARGUMENTS

## Overview
Epic for implementing: $ARGUMENTS

## Details
- **Epic ID**: $EPIC_ID
- **Title**: $ARGUMENTS  
- **Status**: Planning
- **Created**: $(date)
- **Branch**: epic/$EPIC_ID/planning

## Objectives
- [Define main objectives here]
- [Break down into measurable goals]
- [Identify success criteria]

## Sprint Breakdown
- [ ] **Sprint 1**: Core Features
- [ ] **Sprint 2**: Advanced Features  
- [ ] **Sprint 3**: Polish & Testing

## Technical Approach
- Technology Stack: React, Node.js, TypeScript, MongoDB
- Testing Strategy: Jest (unit), Playwright (e2e)
- Deployment: Docker containers

## Team Assignment
- **Architect**: trimabk - System design and architecture
- **Developer**: sarthak - Implementation and code quality

## Acceptance Criteria
- [ ] All user stories completed
- [ ] Tests passing (>80% coverage)
- [ ] Security review completed
- [ ] Performance benchmarks met
- [ ] Documentation complete

## Next Steps
1. Run: \`/sprint "Sprint 1 - Core Features" under $EPIC_ID\`
2. Break down into user stories
3. Begin implementation planning
EOF

echo "✅ Created epic documentation"
```

### Step 5: Update Project Tracking
```bash
# Add to project tracking
echo "Epic $EPIC_ID created: $ARGUMENTS" >> .claude/project-log.txt
echo "Branch: epic/$EPIC_ID/planning" >> .claude/project-log.txt
echo "Created: $(date)" >> .claude/project-log.txt
echo "---" >> .claude/project-log.txt

echo "✅ Updated project tracking"
```

### Step 6: Output Results
```bash
echo ""
echo "🎉 EPIC CREATED SUCCESSFULLY!"
echo ""
echo "Epic Details:"
echo "- ID: $EPIC_ID"
echo "- Title: $ARGUMENTS"
echo "- Branch: epic/$EPIC_ID/planning"
echo "- Documentation: docs/epics/$EPIC_ID/"
echo ""
echo "Next Commands:"
echo "1. /sprint \"Sprint 1 - Core Features\" under $EPIC_ID"
echo "2. /story \"As user I want...\" in SPRINT-001"
echo ""
echo "Git Branches Created:"
git branch | grep "$EPIC_ID"
```

**This command actually CREATES everything:**
- Real git branches
- Real directory structure  
- Real documentation files
- Real project tracking
- Ready for next steps

**No complex implementation needed - just bash commands in markdown!**