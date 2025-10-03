---
description: "Create epic with market research integration and competitive analysis"
allowed_tools: ["Bash", "Write", "Read", "Edit", "WebSearch", "WebFetch"]
---

Create research-backed epic: **$ARGUMENTS**

## 🔍 Market Research Epic Creation

### Step 1: Quick Market Validation
```bash
echo "🔍 Conducting market research for: $ARGUMENTS"

# Use WebSearch to validate market opportunity
echo "Searching for market data and competitors..."
```

**Market Research Queries:**
1. Search for: "[$ARGUMENTS] market size 2024"
2. Search for: "top [$ARGUMENTS] competitors" 
3. Search for: "[$ARGUMENTS] user pain points"
4. Search for: "[$ARGUMENTS] industry trends"

### Step 2: Competitive Analysis
```bash
echo "📊 Analyzing competitive landscape..."
```

**Competitive Research:**
1. WebFetch top 3 competitor websites
2. Analyze their features and pricing
3. Identify market gaps and opportunities
4. Document competitive advantages

### Step 3: Generate Epic ID with Research Context
```bash
# Generate epic ID
EPIC_COUNT=$(find docs/epics -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
EPIC_ID="EPIC-$(printf "%03d" $((EPIC_COUNT + 1)))"
echo "Creating Research-Backed Epic: $EPIC_ID - $ARGUMENTS"
```

### Step 4: Create Git Structure
```bash
# Create epic planning branch
git checkout -b "epic/$EPIC_ID/planning"
git checkout -b "epic/$EPIC_ID/research"
git checkout -b "epic/$EPIC_ID/sprint-001/planning"
git checkout -b "epic/$EPIC_ID/sprint-002/planning"
git checkout "epic/$EPIC_ID/planning"

echo "✅ Created branch structure with research branch"
```

### Step 5: Create Research-Enhanced Documentation
```bash
# Create epic directories including research
mkdir -p "docs/epics/$EPIC_ID"/{research,sprints,stories,handoffs}
mkdir -p "docs/epics/$EPIC_ID/research"/{market,competitors,users,technical}

# Create market research summary
cat > "docs/epics/$EPIC_ID/research/market-research.md" << EOF
# Market Research: $EPIC_ID

## Market Opportunity
- **Market Size**: [From WebSearch results]
- **Growth Rate**: [Industry trends]
- **Target Segments**: [User demographics]

## Competitive Landscape
- **Direct Competitors**: [List from research]
- **Indirect Competitors**: [Adjacent solutions]
- **Market Gaps**: [Opportunities identified]

## User Pain Points
- **Primary Issues**: [From research]
- **Unmet Needs**: [Opportunities]
- **User Behavior**: [Patterns identified]

## Validation Status
- [x] Market size validated
- [x] Competitors analyzed  
- [x] User needs confirmed
- [x] Technical feasibility assessed
EOF

# Create main epic README with research context
cat > "docs/epics/$EPIC_ID/README.md" << EOF
# $EPIC_ID: $ARGUMENTS

## Overview
Epic for implementing: $ARGUMENTS

**Market-Validated Opportunity**
This epic is backed by comprehensive market research showing [opportunity summary].

## Market Context
- **Market Size**: [Validated size]
- **Key Competitors**: [Top 3 competitors]
- **Differentiation**: [Our competitive advantage]
- **Target Users**: [Validated personas]

## Details
- **Epic ID**: $EPIC_ID
- **Title**: $ARGUMENTS  
- **Status**: Planning (Research-Backed)
- **Created**: $(date)
- **Branch**: epic/$EPIC_ID/planning
- **Research**: docs/epics/$EPIC_ID/research/

## Research-Backed Objectives
Based on market research:
- [Objective 1 based on user pain points]
- [Objective 2 based on market gaps]
- [Objective 3 based on competitive analysis]

## User Personas (Research-Validated)
### Primary Persona
- **Who**: [From user research]
- **Pain Points**: [Validated problems]
- **Goals**: [What they want to achieve]
- **Current Solutions**: [What they use now]

### Secondary Persona
- **Who**: [Secondary user type]
- **Needs**: [Their specific requirements]

## Competitive Advantage
- **Unique Value**: [What makes us different]
- **Market Gap**: [Opportunity we're filling]
- **User Benefit**: [Why users will switch]

## Sprint Breakdown (Research-Informed)
- [ ] **Sprint 1**: Core Value Proposition (addresses main pain point)
- [ ] **Sprint 2**: Competitive Differentiation (unique features)
- [ ] **Sprint 3**: User Experience Excellence (better than competitors)

## Success Metrics (Market-Validated)
- **Adoption**: [Target user acquisition]
- **Engagement**: [Usage patterns from research]
- **Revenue**: [Business model validation]
- **Satisfaction**: [User satisfaction targets]

## Technical Approach (Research-Informed)
- **Tech Stack**: [Based on competitive analysis]
- **Scalability**: [Market size considerations]
- **Integration**: [User workflow requirements]

## Go-to-Market Strategy
- **Launch Approach**: [Based on competitive landscape]
- **Pricing**: [Competitive pricing analysis]
- **Channels**: [Where target users are found]

## Risk Mitigation
- **Market Risk**: [Competition response]
- **Technical Risk**: [Implementation challenges]
- **User Risk**: [Adoption barriers]

## Next Steps
1. Complete competitive feature analysis
2. Validate technical approach with research
3. Create user personas from research data
4. Begin Sprint 1 planning with market context

## Research Sources
- Market size: [WebSearch sources]
- Competitors: [WebFetch analysis]  
- User needs: [Research sources]
- Technical: [Industry analysis]
EOF

echo "✅ Created research-enhanced epic documentation"
```

### Step 6: Create Research-Informed Sprint Templates
```bash
# Create sprint templates with research context
cat > "docs/epics/$EPIC_ID/sprints/sprint-template-research.md" << EOF
# Sprint Template: Research-Informed

## Market Context for Sprint
- **User Pain Point**: [Specific problem this sprint addresses]
- **Competitive Gap**: [How this sprint creates advantage]
- **User Value**: [Measurable value delivered]

## Research-Backed Acceptance Criteria
- [ ] Addresses validated user pain point
- [ ] Delivers competitive differentiation
- [ ] Meets market expectations for quality
- [ ] Supports go-to-market strategy

## User Validation Plan
- [ ] Test with target persona segments
- [ ] Measure against competitor benchmarks
- [ ] Validate business model assumptions
- [ ] Confirm technical scalability
EOF

echo "✅ Created research-informed templates"
```

### Step 7: Project Tracking with Research
```bash
# Enhanced project tracking with research context
echo "RESEARCH-BACKED EPIC CREATED" >> .claude/project-log.txt
echo "Epic $EPIC_ID: $ARGUMENTS" >> .claude/project-log.txt
echo "Market Research: Completed" >> .claude/project-log.txt
echo "Competitive Analysis: Completed" >> .claude/project-log.txt
echo "User Validation: Completed" >> .claude/project-log.txt
echo "Branch: epic/$EPIC_ID/planning" >> .claude/project-log.txt
echo "Created: $(date)" >> .claude/project-log.txt
echo "---" >> .claude/project-log.txt

echo "✅ Updated project tracking with research context"
```

### Step 8: Output Research-Enhanced Results
```bash
echo ""
echo "🎉 RESEARCH-BACKED EPIC CREATED!"
echo ""
echo "Epic Details:"
echo "- ID: $EPIC_ID"
echo "- Title: $ARGUMENTS"
echo "- Type: Market Research Validated"
echo "- Branch: epic/$EPIC_ID/planning"
echo "- Documentation: docs/epics/$EPIC_ID/"
echo "- Research: docs/epics/$EPIC_ID/research/"
echo ""
echo "Research Completed:"
echo "✅ Market size and opportunity validated"
echo "✅ Competitive landscape analyzed"
echo "✅ User pain points identified"
echo "✅ Technical feasibility confirmed"
echo ""
echo "Next Commands:"
echo "1. /sprint-simple \"MVP Core Features\" under $EPIC_ID"
echo "2. /story-simple \"As validated-user I want researched-feature\" in SPRINT-001"
echo ""
echo "Research-Informed Branches:"
git branch | grep "$EPIC_ID"
```

**This epic command creates research-backed epics with:**
- Market validation
- Competitive analysis
- User research
- Research-informed documentation
- Market-driven success metrics