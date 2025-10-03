# Idea to Epic Pipeline

## Task 1: Structure Product Idea
**Prompt**: 
```
Convert the following human product idea into a structured format:

"$ARGUMENTS"

Create structured analysis covering:
1. **Product Concept**: Core value proposition
2. **Target Audience**: Primary and secondary users
3. **Key Features**: Main functionality needed
4. **Business Model**: How it generates value
5. **Success Metrics**: How to measure success
6. **Technical Requirements**: High-level tech needs

Output structured product brief as structured-product-brief.md
Write summary to pipeline-context.md
```

## Task 2: Market Research - Competitors
**Prompt**:
```
Using WebSearch and WebFetch tools, research the market for this product idea:

Based on structured-product-brief.md, research:
1. **Direct Competitors**: Top 5 similar products/services
2. **Market Size**: Industry size and growth trends
3. **User Pain Points**: What problems exist in current solutions
4. **Pricing Models**: How competitors monetize
5. **Market Gaps**: Opportunities for differentiation

Use WebSearch to find:
- "Top [product category] apps 2024"
- "[product category] market size trends"
- "[target audience] pain points [product category]"

Create market-research.md with findings
Append summary to pipeline-context.md
```

## Task 3: Competitive Analysis Deep Dive
**Prompt**:
```
Using WebFetch, analyze top 3 competitors found in market research:

For each competitor:
1. Visit their website/product pages
2. Analyze features, pricing, user experience
3. Read user reviews and feedback
4. Identify strengths and weaknesses
5. Find differentiation opportunities

Create competitive-analysis.md
Append insights to pipeline-context.md
```

## Task 4: User Research Validation
**Prompt**:
```
Research target user needs and behaviors:

Use WebSearch to find:
- User surveys and studies about [target audience]
- Forum discussions and pain points
- Industry reports on user behavior
- Best practices and user expectations

Create user-research.md with validated assumptions
Append to pipeline-context.md
```

## Task 5: Technical Landscape Research
**Prompt**:
```
Research technical implementation landscape:

Use WebSearch for:
- Popular technology stacks for similar products
- API integrations commonly used
- Scalability considerations and best practices
- Security requirements for this domain
- Cost estimates for infrastructure

Create technical-landscape.md
Append to pipeline-context.md
```

## Task 6: Opportunity Assessment
**Prompt**:
```
Synthesize all research into opportunity assessment:

Based on pipeline-context.md contents:
1. **Market Opportunity**: Size, growth, timing
2. **Competitive Advantage**: How to differentiate
3. **User Value Proposition**: Clear value to users
4. **Technical Feasibility**: Complexity and requirements
5. **Business Viability**: Revenue potential and costs
6. **Risk Assessment**: Technical, market, and business risks

Create opportunity-assessment.md
Update pipeline-context.md with final analysis
```

## Task 7: PM Strategy Session
**Prompt**:
```
Acting as a Product Manager, create comprehensive product strategy:

Using all research from pipeline-context.md:
1. **Product Vision**: Clear 1-year vision
2. **Success Metrics**: KPIs and measurement plan
3. **User Personas**: Detailed target user profiles
4. **Feature Priority Matrix**: Must-have vs nice-to-have
5. **Go-to-Market Strategy**: Launch and growth plan
6. **Roadmap Outline**: Phase 1, 2, 3 breakdown

Create pm-product-strategy.md
Update pipeline-context.md with strategy summary
```

## Task 8: Epic Planning
**Prompt**:
```
Based on PM strategy, create Phase 1 epic structure:

From pm-product-strategy.md, identify Phase 1 scope:
1. **MVP Features**: Core functionality for launch
2. **User Flows**: Key user journeys to enable
3. **Technical Foundation**: Architecture needed
4. **Success Criteria**: Measurable outcomes

Plan epic structure:
- Epic breakdown (2-3 epics max for Phase 1)
- Sprint organization (2-3 sprints per epic)
- Story themes and priorities

Create epic-planning.md
Update pipeline-context.md with epic structure
```

## Task 9: Create Epics
**Prompt**:
```
Execute epic creation using our epic command:

For each epic identified in epic-planning.md:

/epic-simple [Epic Name based on research]

Create all Phase 1 epics with proper:
- Market research context
- User personas and needs
- Competitive differentiation
- Technical requirements
- Success metrics

Document all epic IDs in pipeline-context.md
```

## Task 10: Create Sprints
**Prompt**:
```
Create sprints for each epic:

For each epic created:

/sprint-simple "[Sprint Name]" under [EPIC-ID]

Based on pm-product-strategy.md:
- Sprint 1: Foundation & Core Features
- Sprint 2: User Experience & Polish
- Sprint 3: Integration & Launch Prep

Document all sprint IDs in pipeline-context.md
```

## Task 11: Create Core Stories
**Prompt**:
```
Create initial user stories for Sprint 1 of each epic:

Based on user research and PM strategy:

/story-simple "As [persona] I want [core need] so that [value]" in [SPRINT-ID]

Focus on MVP features that deliver core value proposition.
Create 3-5 stories per sprint to start.

Document all story IDs in pipeline-context.md
```

## Task 12: Final Summary
**Prompt**:
```
Generate comprehensive pipeline summary:

From pipeline-context.md, create final report:

1. **Product Concept**: Original idea + research validation
2. **Market Opportunity**: Research findings and opportunity size
3. **Competitive Landscape**: Key insights and differentiation
4. **User Validation**: Confirmed user needs and personas
5. **Technical Approach**: Recommended tech stack and architecture
6. **Phase 1 Plan**: Epics, sprints, and stories created
7. **Success Metrics**: How to measure progress
8. **Next Steps**: Ready for implementation with idea-to-production pipeline

Create final-product-plan.md with complete Phase 1 roadmap
Include all epic/sprint/story IDs for execution
Note: Continue with /pipe idea-to-production for full implementation
```