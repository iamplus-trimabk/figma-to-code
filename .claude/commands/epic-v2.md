---
description: "Create epic with feature integration and proper branch management v2.0"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Glob"]
---

Create epic: **$ARGUMENTS** for feature: **$FEATURE_NAME**

## 🎯 Epic Creation Implementation v2.0

### Step 1: Validate Feature Context
```bash
# Ensure we're in proper feature context
if [ -z "$FEATURE_NAME" ]; then
    echo "❌ Error: FEATURE_NAME not set. Use pipeline or set FEATURE_NAME environment variable."
    exit 1
fi

# Ensure feature directory exists
if [ ! -d ".claude/$FEATURE_NAME" ]; then
    echo "❌ Error: Feature directory .claude/$FEATURE_NAME not found. Run idea-to-epic pipeline first."
    exit 1
fi

echo "✅ Feature context validated: $FEATURE_NAME"
```

### Step 2: Generate Epic ID and Setup
```bash
# Generate next epic ID
EPIC_COUNT=$(find docs/epics -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
EPIC_ID="EPIC-$(printf "%03d" $((EPIC_COUNT + 1)))"
echo "Creating Epic: $EPIC_ID - $ARGUMENTS for feature: $FEATURE_NAME"

# Set environment for subsequent tasks
export CURRENT_EPIC_ID=$EPIC_ID
export EPIC_NAME="$ARGUMENTS"
```

### Step 3: Branch Management
```bash
# Ensure we're on feature branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "feature-$FEATURE_NAME" ]; then
    echo "⚠️ Switching to feature branch: feature-$FEATURE_NAME"
    git checkout "feature-$FEATURE_NAME" || {
        echo "❌ Error: Cannot switch to feature-$FEATURE_NAME branch. Fix git conflicts and retry."
        exit 1
    }
fi

# Create epic branch
git checkout -b "feature-$FEATURE_NAME/epic-$EPIC_ID" || {
    echo "❌ Error: Cannot create epic branch. Fix git conflicts and retry."
    exit 1
}
echo "✅ Created branch: feature-$FEATURE_NAME/epic-$EPIC_ID"
```

### Step 4: Create Documentation Structure
```bash
# Create epic directories
mkdir -p "docs/epics/$EPIC_ID"/{sprints,stories,handoffs}
mkdir -p "docs/epics/$EPIC_ID/sprints"/{sprint-001,sprint-002,sprint-003}
mkdir -p ".claude/$FEATURE_NAME/epic-$EPIC_ID"

echo "✅ Created directory structure"
```

### Step 5: Create Epic Documentation with Feature Context
```bash
# Read feature context for epic creation
PRODUCT_BRIEF=""
PM_STRATEGY=""
UX_STRATEGY=""

if [ -f ".claude/$FEATURE_NAME/structured-product-brief.md" ]; then
    PRODUCT_BRIEF=$(head -20 ".claude/$FEATURE_NAME/structured-product-brief.md")
fi

if [ -f ".claude/$FEATURE_NAME/pm-product-strategy.md" ]; then
    PM_STRATEGY=$(head -20 ".claude/$FEATURE_NAME/pm-product-strategy.md")
fi

if [ -f ".claude/$FEATURE_NAME/ux-strategy.md" ]; then
    UX_STRATEGY=$(head -20 ".claude/$FEATURE_NAME/ux-strategy.md")
fi

# Create comprehensive epic documentation
cat > "docs/epics/$EPIC_ID/README.md" << EOF
# $EPIC_ID: $ARGUMENTS
*Part of Feature: $FEATURE_NAME*

## Overview
Epic for implementing: $ARGUMENTS

This epic is part of the larger **$FEATURE_NAME** feature development and incorporates market research, user needs analysis, and strategic product planning.

## Details
- **Epic ID**: $EPIC_ID
- **Feature**: $FEATURE_NAME
- **Title**: $ARGUMENTS  
- **Status**: Planning
- **Created**: $(date)
- **Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID

## Context from Feature Planning

### Product Brief Summary
$PRODUCT_BRIEF

### PM Strategy Context
$PM_STRATEGY

### UX Strategy Context
$UX_STRATEGY

## Objectives
Based on feature research and strategy:
- [Define main objectives from PM strategy]
- [Break down into measurable goals]
- [Identify success criteria from user research]
- [Align with competitive differentiation]

## Sprint Breakdown
- [ ] **Sprint 1**: Foundation & Core Features
- [ ] **Sprint 2**: User Experience & Advanced Features  
- [ ] **Sprint 3**: Integration & Quality Assurance

## Technical Approach
From feature technical landscape analysis:
- Technology Stack: React, Node.js, TypeScript, MongoDB
- Testing Strategy: Jest (unit), Playwright (e2e)
- Security: OAuth 2.1, input validation, OWASP compliance
- Deployment: Docker containers with CI/CD

## User Personas (from Feature Research)
- **Primary**: [Persona 1 from user research]
- **Secondary**: [Persona 2 from user research]
- **Enterprise**: [Persona 3 from user research]

## Success Criteria
Based on feature PM strategy:
- [ ] All user stories completed with acceptance criteria met
- [ ] Performance benchmarks achieved (response time, throughput)
- [ ] Security requirements validated (audit, penetration testing)
- [ ] User experience validated (usability testing, A/B testing)
- [ ] Tests passing (>90% coverage requirement)
- [ ] Documentation complete (API docs, user guides)
- [ ] Market differentiation objectives achieved

## Risk Assessment
From feature opportunity assessment:
- **Technical Risks**: [Identified in technical landscape research]
- **Market Risks**: [From competitive analysis]
- **User Adoption Risks**: [From user research validation]

## Team Assignment
- **Architect**: trimabk - System design and architecture decisions
- **Developer**: sarthak - Implementation and code quality standards
- **PM Review**: Regular strategy alignment and success metrics tracking

## Dependencies
- [ ] Feature market research completed
- [ ] PM and UX strategy finalized  
- [ ] Technical architecture decisions made
- [ ] User personas and journeys validated

## Next Steps
1. Create Sprint 1: \`/sprint "Sprint 1 - Foundation" under $EPIC_ID\`
2. Break down into user stories based on personas
3. Begin implementation with proper branch management
4. Regular review against feature success metrics

## Related Files
- Feature Context: \`.claude/$FEATURE_NAME/pipeline-context.md\`
- Product Strategy: \`.claude/$FEATURE_NAME/pm-product-strategy.md\`
- User Research: \`.claude/$FEATURE_NAME/user-research.md\`
- Technical Landscape: \`.claude/$FEATURE_NAME/technical-landscape.md\`
EOF

echo "✅ Created comprehensive epic documentation with feature context"
```

### Step 6: Update Feature Tracking
```bash
# Update feature pipeline context
echo "" >> ".claude/$FEATURE_NAME/pipeline-context.md"
echo "## Epic Created: $EPIC_ID" >> ".claude/$FEATURE_NAME/pipeline-context.md"
echo "- **Title**: $ARGUMENTS" >> ".claude/$FEATURE_NAME/pipeline-context.md"
echo "- **Created**: $(date)" >> ".claude/$FEATURE_NAME/pipeline-context.md"
echo "- **Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID" >> ".claude/$FEATURE_NAME/pipeline-context.md"
echo "- **Status**: Planning" >> ".claude/$FEATURE_NAME/pipeline-context.md"

# Create epic tracking file
cat > ".claude/$FEATURE_NAME/epic-$EPIC_ID/epic-tracking.md" << EOF
# Epic $EPIC_ID Tracking

## Epic Details
- **Feature**: $FEATURE_NAME
- **Epic ID**: $EPIC_ID
- **Title**: $ARGUMENTS
- **Created**: $(date)
- **Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID

## Sprint Status
- [ ] Sprint 1: Not created
- [ ] Sprint 2: Not created  
- [ ] Sprint 3: Not created

## Story Status
- [ ] No stories created yet

## Implementation Status
- [ ] Epic planning: In progress
- [ ] Sprint creation: Pending
- [ ] Story creation: Pending
- [ ] Implementation: Pending
- [ ] Testing: Pending
- [ ] Epic completion: Pending

## Next Actions
1. Create sprints for this epic
2. Define user stories based on feature personas
3. Begin implementation with proper branch workflow
EOF

echo "✅ Updated feature tracking and epic monitoring"
```

### Step 7: Commit and Merge Back
```bash
# Commit epic creation
git add .
git commit -m "feat($FEATURE_NAME): Create Epic $EPIC_ID - $ARGUMENTS

- Epic documentation with feature context integration
- Sprint structure planning
- Success criteria based on feature research
- Team assignments and dependencies mapped
- Ready for sprint and story creation

Part of feature: $FEATURE_NAME
Epic branch: feature-$FEATURE_NAME/epic-$EPIC_ID

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# Switch back to feature branch
git checkout "feature-$FEATURE_NAME" || {
    echo "❌ Error: Cannot switch back to feature branch. Manual intervention required."
    exit 1
}

# Merge epic branch
git merge "feature-$FEATURE_NAME/epic-$EPIC_ID" --no-ff -m "merge: Epic $EPIC_ID creation into feature $FEATURE_NAME" || {
    echo "❌ Error: Cannot merge epic branch. Fix conflicts and retry."
    exit 1
}

# Push changes
git push origin "feature-$FEATURE_NAME" || {
    echo "❌ Error: Cannot push to remote. Check network connection and try again."
    exit 1
}

# Clean up epic branch
git branch -d "feature-$FEATURE_NAME/epic-$EPIC_ID"

echo "✅ Epic committed, merged, and pushed successfully"
```

### Step 8: Output Results
```bash
echo ""
echo "🎉 EPIC CREATED SUCCESSFULLY!"
echo ""
echo "Epic Details:"
echo "- Feature: $FEATURE_NAME"
echo "- Epic ID: $EPIC_ID"
echo "- Title: $ARGUMENTS"
echo "- Documentation: docs/epics/$EPIC_ID/"
echo "- Tracking: .claude/$FEATURE_NAME/epic-$EPIC_ID/"
echo ""
echo "Feature Integration:"
echo "- Product research context integrated"
echo "- PM strategy alignment completed"
echo "- UX strategy considerations included"
echo "- User personas referenced"
echo ""
echo "Next Commands:"
echo "1. /sprint \"Sprint 1 - Foundation\" under $EPIC_ID"
echo "2. /story \"As [persona] I want...\" in [SPRINT-ID]"
echo ""
echo "Git Status:"
echo "- Current branch: $(git branch --show-current)"
echo "- Changes committed and pushed"
echo "- Epic integrated into feature $FEATURE_NAME"
```

**This v2.0 command:**
- ✅ Validates feature context before proceeding
- ✅ Creates epic with full feature integration
- ✅ Proper branch management (create → work → merge → push → cleanup)
- ✅ Incorporates market research and strategy context
- ✅ Error handling for git operations
- ✅ Comprehensive tracking and documentation
- ✅ Ready for hierarchical sprint/story creation

**No complex implementation needed - just enhanced bash commands with feature awareness!**