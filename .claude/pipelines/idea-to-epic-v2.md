# Idea to Epic Pipeline v2.0
*Enhanced with feature naming and proper branch management*

## Initial Setup: Feature Naming and Branch Creation
**Prompt**: 
```
Get feature name from user for the following product idea:

"$ARGUMENTS"

Step 1: Ask user to provide feature name:
1. **Custom Feature Name** (if they want to specify)
2. **Suggested Names** (provide 3-5 options based on the idea)

Step 2: Once feature name is confirmed (e.g., "mcp-simflo"):
- Set FEATURE_NAME environment variable
- Create feature branch: feature-{FEATURE_NAME} (e.g., feature-mcp-simflo)
- Switch to feature branch
- Create feature directory: .claude/{FEATURE_NAME}/
- Initialize pipeline-context.md in feature directory

Branch Management:
```bash
# Create and switch to feature branch
git checkout -b feature-{FEATURE_NAME} || git checkout feature-{FEATURE_NAME}
echo "✅ On feature branch: feature-{FEATURE_NAME}"

# Create feature directory
mkdir -p .claude/{FEATURE_NAME}
echo "✅ Created feature directory: .claude/{FEATURE_NAME}"
```

All subsequent tasks will use this feature name and directory structure.
```

## Task 1: Structure Product Idea
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-001-product-structure
**Prompt**: 
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-001-product-structure
3. If branch switching fails, error out with message: "Cannot switch to branch. Please fix git conflicts and retry."

Convert the following human product idea into a structured format:

"$ARGUMENTS"

Create structured analysis covering:
1. **Product Concept**: Core value proposition
2. **Target Audience**: Primary and secondary users
3. **Key Features**: Main functionality needed
4. **Business Model**: How it generates value
5. **Success Metrics**: How to measure success
6. **Technical Requirements**: High-level tech needs

Output files:
- .claude/$FEATURE_NAME/structured-product-brief.md
- .claude/$FEATURE_NAME/pipeline-context.md (initialize with summary)

Completion Steps:
1. Commit changes with message: "feat($FEATURE_NAME): Task 1 - Structure product idea"
2. Switch back to: feature-$FEATURE_NAME
3. Merge task branch: git merge feature-$FEATURE_NAME/task-001-product-structure
4. Push changes: git push origin feature-$FEATURE_NAME
5. Delete task branch: git branch -d feature-$FEATURE_NAME/task-001-product-structure
```

## Task 2: Market Research - Competitors
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-002-market-research
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-002-market-research
3. If branch switching fails, error out and stop execution

Using WebSearch and WebFetch tools, research the market for this product idea:

Read context from: .claude/$FEATURE_NAME/structured-product-brief.md

Research:
1. **Direct Competitors**: Top 5 similar products/services
2. **Market Size**: Industry size and growth trends
3. **User Pain Points**: What problems exist in current solutions
4. **Pricing Models**: How competitors monetize
5. **Market Gaps**: Opportunities for differentiation

Use WebSearch to find:
- "Top [product category] apps 2024"
- "[product category] market size trends"
- "[target audience] pain points [product category]"

Output files:
- .claude/$FEATURE_NAME/market-research.md
- Update .claude/$FEATURE_NAME/pipeline-context.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 2 - Market research and competitor analysis"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-002-market-research
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 3: Competitive Analysis Deep Dive
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-003-competitive-analysis
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-003-competitive-analysis

Using WebFetch, analyze top 3 competitors from market research:

Read context from: .claude/$FEATURE_NAME/market-research.md

For each competitor:
1. Visit their website/product pages
2. Analyze features, pricing, user experience
3. Read user reviews and feedback
4. Identify strengths and weaknesses
5. Find differentiation opportunities

Output files:
- .claude/$FEATURE_NAME/competitive-analysis.md
- Update .claude/$FEATURE_NAME/pipeline-context.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 3 - Deep competitive analysis"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-003-competitive-analysis
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 4: User Research Validation
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-004-user-research
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-004-user-research

Research target user needs and behaviors:

Read context from: .claude/$FEATURE_NAME/pipeline-context.md

Use WebSearch to find:
- User surveys and studies about [target audience]
- Forum discussions and pain points
- Industry reports on user behavior
- Best practices and user expectations

Output files:
- .claude/$FEATURE_NAME/user-research.md
- Update .claude/$FEATURE_NAME/pipeline-context.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 4 - User research validation"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-004-user-research
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 5: Technical Landscape Research
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-005-technical-landscape
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-005-technical-landscape

Research technical implementation landscape:

Read context from: .claude/$FEATURE_NAME/pipeline-context.md

Use WebSearch for:
- Popular technology stacks for similar products
- API integrations commonly used
- Scalability considerations and best practices
- Security requirements for this domain
- Cost estimates for infrastructure

Output files:
- .claude/$FEATURE_NAME/technical-landscape.md
- Update .claude/$FEATURE_NAME/pipeline-context.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 5 - Technical landscape research"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-005-technical-landscape
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 6: Opportunity Assessment
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-006-opportunity-assessment
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-006-opportunity-assessment

Synthesize all research into opportunity assessment:

Read context from: .claude/$FEATURE_NAME/pipeline-context.md

Create comprehensive assessment:
1. **Market Opportunity**: Size, growth, timing
2. **Competitive Advantage**: How to differentiate
3. **User Value Proposition**: Clear value to users
4. **Technical Feasibility**: Complexity and requirements
5. **Business Viability**: Revenue potential and costs
6. **Risk Assessment**: Technical, market, and business risks
7. **GO/NO-GO Decision**: Recommendation with score (1-10)

Output files:
- .claude/$FEATURE_NAME/opportunity-assessment.md
- Update .claude/$FEATURE_NAME/pipeline-context.md with final analysis

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 6 - Opportunity assessment and GO/NO-GO decision"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-006-opportunity-assessment
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 7: PM Strategy Session
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-007-pm-strategy
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-007-pm-strategy

Acting as a Product Manager, create comprehensive product strategy:

Read context from: .claude/$FEATURE_NAME/pipeline-context.md

Create detailed strategy:
1. **Product Vision**: Clear 1-year vision
2. **Success Metrics**: KPIs and measurement plan
3. **User Personas**: Detailed target user profiles (3-4 personas)
4. **Feature Priority Matrix**: Must-have vs nice-to-have
5. **Go-to-Market Strategy**: Launch and growth plan
6. **Epic Structure**: 3-4 epics for Phase 1 MVP
7. **Roadmap Outline**: Phase 1, 2, 3 breakdown with timelines

Output files:
- .claude/$FEATURE_NAME/pm-product-strategy.md
- Update .claude/$FEATURE_NAME/pipeline-context.md with strategy summary

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 7 - PM strategy and product roadmap"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-007-pm-strategy
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 8: UX Strategy Session
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-008-ux-strategy
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-008-ux-strategy

Acting as a UX Strategist, create user experience strategy:

Read context from: .claude/$FEATURE_NAME/pm-product-strategy.md

Create UX strategy:
1. **User Journey Maps**: Key user flows for each persona
2. **Information Architecture**: App structure and navigation
3. **Design System Requirements**: UI/UX principles and patterns
4. **Accessibility Requirements**: WCAG compliance and inclusive design
5. **Mobile/Desktop Strategy**: Platform-specific considerations
6. **Prototype Priorities**: Key screens to prototype first
7. **Usability Testing Plan**: How to validate design decisions

Output files:
- .claude/$FEATURE_NAME/ux-strategy.md
- Update .claude/$FEATURE_NAME/pipeline-context.md with UX insights

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 8 - UX strategy and user journey design"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-008-ux-strategy
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 9: Epic Structure Planning
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-009-epic-planning
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-009-epic-planning

Based on PM and UX strategy, create detailed epic structure:

Read context from: .claude/$FEATURE_NAME/pm-product-strategy.md and .claude/$FEATURE_NAME/ux-strategy.md

Plan epic structure for Phase 1 MVP:
1. **Epic Breakdown**: 3-4 epics maximum
2. **Sprint Organization**: 2-3 sprints per epic (6-8 weeks total)
3. **Story Themes**: High-level story categories per epic
4. **Dependencies**: Epic and sprint dependencies
5. **Success Criteria**: Measurable outcomes per epic
6. **Team Assignment**: Which team profiles work on each epic

Each Epic should include:
- Clear business objective
- User value delivered
- Technical scope
- Acceptance criteria
- Estimated effort (person-weeks)

Output files:
- .claude/$FEATURE_NAME/epic-planning.md
- Update .claude/$FEATURE_NAME/pipeline-context.md with epic structure

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 9 - Epic structure and sprint planning"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-009-epic-planning
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 10: Create Epic 1
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-001
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-001

Execute epic creation for Epic 1:

Read epic details from: .claude/$FEATURE_NAME/epic-planning.md

Create Epic 1 using command:
/epic-simple "[Epic 1 Name from planning]"

Include context from research:
- Market research and competitive analysis
- User personas and journey maps
- Technical requirements and constraints
- Success metrics and acceptance criteria

Set environment variable: EPIC_001_ID=[generated epic ID]

Output files:
- Epic documentation in proper git branch structure
- Update .claude/$FEATURE_NAME/pipeline-context.md with Epic 1 ID

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 10 - Create Epic 1 [Epic Name]"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/epic-001
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 11: Create Epic 2
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-002
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-002

Execute epic creation for Epic 2:

Read epic details from: .claude/$FEATURE_NAME/epic-planning.md

Create Epic 2 using command:
/epic-simple "[Epic 2 Name from planning]"

Include full context and dependencies on Epic 1.

Set environment variable: EPIC_002_ID=[generated epic ID]

Output files:
- Epic documentation in proper git branch structure
- Update .claude/$FEATURE_NAME/pipeline-context.md with Epic 2 ID

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 11 - Create Epic 2 [Epic Name]"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/epic-002
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 12: Create Epic 3
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-003
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-003

Execute epic creation for Epic 3:

Read epic details from: .claude/$FEATURE_NAME/epic-planning.md

Create Epic 3 using command:
/epic-simple "[Epic 3 Name from planning]"

Include full context and dependencies on previous epics.

Set environment variable: EPIC_003_ID=[generated epic ID]

Output files:
- Epic documentation in proper git branch structure
- Update .claude/$FEATURE_NAME/pipeline-context.md with Epic 3 ID

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 12 - Create Epic 3 [Epic Name]"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/epic-003
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch
```

## Task 13: Final Product Plan
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/task-013-final-plan
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/task-013-final-plan

Generate comprehensive pipeline summary:

Read all context from: .claude/$FEATURE_NAME/pipeline-context.md

Create final report including:

1. **Product Concept**: Original idea + research validation
2. **Market Opportunity**: Research findings and opportunity size ($TAM, growth %)
3. **Competitive Landscape**: Key insights and differentiation strategy
4. **User Validation**: Confirmed user needs and detailed personas
5. **Technical Approach**: Recommended tech stack and architecture
6. **UX Strategy**: User journeys and design system requirements
7. **Phase 1 Plan**: All epics created with IDs and sprint breakdown
8. **Success Metrics**: KPIs and measurement plan
9. **Go-to-Market Strategy**: Launch plan and marketing approach
10. **Next Steps**: Ready for implementation with epic → sprint → story pipeline

Include all epic/sprint/story IDs for execution tracking.

Output files:
- .claude/$FEATURE_NAME/final-product-plan.md
- .claude/$FEATURE_NAME/README.md (feature overview)

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Task 13 - Final product plan and feature summary"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/task-013-final-plan
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch

Note: Feature ready for Epic → Sprint → Story implementation pipeline
```

## Pipeline Notes:
- **Feature Name**: Established at start, used throughout
- **Directory Structure**: .claude/$FEATURE_NAME/ for all files
- **Branch Strategy**: feature-$FEATURE_NAME with task branches
- **Git Flow**: Create task branch → work → commit → merge → push → delete task branch
- **Error Handling**: Stop execution if branch switching fails
- **Next Phase**: Use epic → sprint → story pipeline for implementation