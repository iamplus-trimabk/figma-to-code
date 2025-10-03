# Idea to Production Pipeline

## Pipeline: idea-to-production
**Description**: Complete product lifecycle from human idea to production deployment  
**Context File**: ./pipeline-context.md (accumulates as we go)

---

## PHASE 1: RESEARCH & VALIDATION (Tasks 1-6)

## Task 1: Structure Product Idea
**Agent**: Task  
**Description**: Convert human idea into structured format  
**Context**: None (first task)  
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

---

## Task 2: Market Research - Competitors
**Agent**: Task  
**Description**: Research market and competitors  
**Context**: ./pipeline-context.md (from Task 1)  
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

---

## Task 3: Competitive Analysis Deep Dive
**Agent**: Task  
**Description**: Analyze top competitors in detail  
**Context**: ./pipeline-context.md  
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

---

## Task 4: User Research Validation
**Agent**: Task  
**Description**: Research target user needs and behaviors  
**Context**: ./pipeline-context.md  
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

---

## Task 5: Technical Landscape Research
**Agent**: Task  
**Description**: Research technical implementation landscape  
**Context**: ./pipeline-context.md  
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

---

## Task 6: Opportunity Assessment
**Agent**: Task  
**Description**: Synthesize research into opportunity assessment  
**Context**: ./pipeline-context.md  
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

---

## PHASE 2: STRATEGY & PLANNING (Tasks 7-12)

## Task 7: PM Strategy Session
**Agent**: Task  
**Description**: Create comprehensive product strategy  
**Context**: ./pipeline-context.md  
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

---

## Task 8: UX Strategy Session
**Agent**: Task  
**Description**: Create user experience strategy and design approach  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Acting as a UX Strategist, create comprehensive UX strategy:

Based on user research and PM strategy:
1. **User Journey Mapping**: Key user flows and touchpoints
2. **Information Architecture**: Content organization and navigation
3. **Design System Strategy**: UI components and style guidelines
4. **Interaction Design**: Key interactions and micro-interactions
5. **Accessibility Requirements**: WCAG compliance and inclusive design
6. **Testing Strategy**: Usability testing and validation approach

Create ux-strategy.md
Update pipeline-context.md with UX strategy summary
```

---

## Task 9: Epic Planning
**Agent**: Task  
**Description**: Create Phase 1 epic structure  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Based on PM and UX strategies, create Phase 1 epic structure:

From pm-product-strategy.md and ux-strategy.md, identify Phase 1 scope:
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

---

## PHASE 3: IMPLEMENTATION (Tasks 10-18)

## Task 10: Create Epics
**Agent**: Task  
**Description**: Execute epic creation using epic command  
**Context**: ./pipeline-context.md  
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

---

## Task 11: Create Sprints
**Agent**: Task  
**Description**: Create sprints for each epic  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Create sprints for each epic:

For each epic created:

/sprint-simple "[Sprint Name]" under [EPIC-ID]

Based on pm-product-strategy.md and ux-strategy.md:
- Sprint 1: Foundation & Core Features
- Sprint 2: User Experience & Polish
- Sprint 3: Integration & Launch Prep

Document all sprint IDs in pipeline-context.md
```

---

## Task 12: Create Core Stories
**Agent**: Task  
**Description**: Create initial user stories for Sprint 1 of each epic  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Create initial user stories for Sprint 1 of each epic:

Based on user research and UX strategy:

/story-simple "As [persona] I want [core need] so that [value]" in [SPRINT-ID]

Focus on MVP features that deliver core value proposition.
Create 3-5 stories per sprint to start.

Document all story IDs in pipeline-context.md
```

---

## Task 13: Implementation Setup
**Agent**: Task  
**Description**: Set up development environment and structure  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Set up development environment for first epic:

Based on technical-landscape.md:
1. Create implementation branches for first epic
2. Set up project structure and scaffolding
3. Initialize technology stack (package.json, dependencies)
4. Create base configuration files
5. Set up development database/services

Document setup in pipeline-context.md
```

---

## Task 14: Core Implementation
**Agent**: Task  
**Description**: Implement first sprint stories  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Implement core functionality for first sprint:

Based on story definitions and technical requirements:
1. Implement core backend API endpoints
2. Create frontend components and pages
3. Set up authentication and security
4. Implement database schema and operations
5. Create basic error handling and validation

Focus on working MVP functionality.
Document implementation progress in pipeline-context.md
```

---

## PHASE 4: TESTING & QUALITY (Tasks 15-16)

## Task 15: Testing Implementation
**Agent**: Task  
**Description**: Implement comprehensive testing  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Implement comprehensive testing suite:

Based on technical requirements:
1. **Unit Tests**: Test individual functions and components
2. **Integration Tests**: Test API endpoints and data flow
3. **E2E Tests**: Test complete user workflows
4. **Performance Tests**: Load testing and optimization
5. **Security Tests**: Vulnerability scanning and validation

Run all tests and document results in pipeline-context.md
```

---

## Task 16: Code Review & Quality
**Agent**: Task  
**Description**: Perform comprehensive code review  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Perform comprehensive code review and quality assessment:

Review areas:
1. **Architecture Alignment**: Follows technical design
2. **Code Quality**: Clean, maintainable, documented
3. **Security Assessment**: Secure coding practices
4. **Performance Analysis**: Optimization opportunities
5. **UX Implementation**: Matches design requirements

Document review findings and fixes in pipeline-context.md
```

---

## PHASE 5: DEPLOYMENT & LAUNCH (Tasks 17-20)

## Task 17: Staging Deployment
**Agent**: Task  
**Description**: Deploy to staging environment  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Deploy application to staging environment:

Based on technical-landscape.md infrastructure plan:
1. Set up staging environment (database, services)
2. Deploy application to staging servers
3. Run smoke tests and validation
4. Test all user workflows in staging
5. Verify performance and security

Document staging deployment and URLs in pipeline-context.md
```

---

## Task 18: User Acceptance Testing
**Agent**: Task  
**Description**: Conduct user acceptance testing  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Conduct user acceptance testing:

Based on user personas and success metrics:
1. Create UAT test plans and scenarios
2. Execute testing with target user representatives
3. Collect feedback on usability and functionality
4. Document issues and improvement suggestions
5. Prioritize fixes and enhancements

Document UAT results and action items in pipeline-context.md
```

---

## Task 19: Production Deployment
**Agent**: Task  
**Description**: Deploy to production environment  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Deploy to production environment:

Final production deployment:
1. Set up production infrastructure and monitoring
2. Deploy application with zero-downtime strategy
3. Verify all services are running correctly
4. Set up monitoring and alerting
5. Create production runbook and documentation

Document production URLs and monitoring in pipeline-context.md
```

---

## Task 20: Final Summary & Handoff
**Agent**: Task  
**Description**: Generate comprehensive project summary  
**Context**: ./pipeline-context.md  
**Prompt**:
```
Generate comprehensive project summary:

From pipeline-context.md, create final report:

1. **Product Concept**: Original idea + research validation
2. **Market Opportunity**: Research findings and opportunity size
3. **Competitive Landscape**: Key insights and differentiation
4. **User Validation**: Confirmed user needs and personas
5. **Technical Implementation**: Architecture and tech stack
6. **Development Artifacts**: Epics, sprints, stories created
7. **Production Deployment**: URLs, monitoring, documentation
8. **Success Metrics**: How to measure progress
9. **Next Steps**: Roadmap for Phase 2
10. **Lessons Learned**: Key insights and improvements

Create final-product-plan.md with complete project documentation
Include all epic/sprint/story IDs and production information
```

---

## Usage

To run this complete pipeline:

```bash
# Transform any idea into production-ready product
/pipe idea-to-production "Your product idea here"

# Example:
/pipe idea-to-production "AI-powered task management for remote teams"
```

This pipeline will:
1. **Research Phase**: Market validation, competitive analysis, user research (Tasks 1-6)
2. **Strategy Phase**: PM strategy, UX strategy, epic planning (Tasks 7-9)
3. **Implementation Phase**: Create epics/sprints/stories, build MVP (Tasks 10-14)
4. **Quality Phase**: Testing and code review (Tasks 15-16)
5. **Launch Phase**: Staging, UAT, production deployment (Tasks 17-20)

**Total Timeline**: Idea to production in 20 comprehensive tasks with full context preservation.