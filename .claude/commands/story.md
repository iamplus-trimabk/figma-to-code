---
description: "Create detailed user story with acceptance criteria, tasks, and testing requirements"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Grep"]
---

Create user story: **$ARGUMENTS**

## 📖 User Story Creation Process

**Expected format**: `/story [User Story Description] in [SPRINT-ID]`
**Example**: `/story As user I want to login with email in SPRINT-001`

### Phase 1: Story Analysis
1. **Parse Story Context**
   - Extract user persona, goal, and benefit from description
   - Read parent sprint and epic documentation
   - Understand story position in sprint backlog
   - Identify dependencies on other stories

2. **Story Refinement**
   - Ensure proper user story format: "As a [user], I want [goal] so that [benefit]"
   - Define story scope and boundaries
   - Estimate complexity and story points
   - Identify technical requirements

### Phase 2: Git Branch Setup
1. **Create Story Branch**
   - Format: `epic/EPIC-XXX/sprint-YYY/story-ZZZ/planning`
   - Branch from sprint planning branch
   - Create development branch: `epic/EPIC-XXX/sprint-YYY/story-ZZZ/implementation`

2. **Story Documentation**
   ```
   docs/epics/EPIC-XXX/sprints/SPRINT-YYY/stories/STORY-ZZZ/
   ├── story-definition.md
   ├── acceptance-criteria.md
   ├── technical-requirements.md
   ├── testing-strategy.md
   ├── implementation-tasks.md
   └── handoff-checklist.md
   ```

### Phase 3: Detailed Planning
1. **Acceptance Criteria (Given-When-Then)**
   ```
   Given [initial context]
   When [user action]
   Then [expected outcome]
   ```
   - Define 3-5 clear acceptance criteria
   - Include edge cases and error scenarios
   - Specify UI/UX requirements
   - Define API contracts if applicable

2. **Technical Requirements**
   - Frontend components needed (React/etc based on project.json)
   - Backend API endpoints and data models
   - Database schema changes
   - Third-party integrations
   - Security and validation requirements

### Phase 4: Implementation Breakdown
1. **Task Decomposition**
   - Break story into 4-8 hour development tasks
   - Include setup, development, testing, and review tasks
   - Consider frontend and backend work separately
   - Plan integration points

2. **Testing Strategy**
   - Unit tests (Jest/Vitest based on project.json)
   - Integration tests
   - End-to-end tests (Playwright/Cypress)
   - Manual testing scenarios

### Phase 5: Team Coordination
1. **Handoff Planning**
   - Define handoff points (planning → implementation → testing)
   - Create context transfer templates
   - Set up review checkpoints
   - Plan demonstration scenarios

2. **Profile-Specific Approach**
   - **Architect (trimabk)**: Focus on system integration and architectural decisions
   - **Developer (sarthak)**: Focus on implementation details and code structure

### Phase 6: Database Registration
1. **Story Entry**
   - Add story to SQLite database
   - Link to parent sprint and epic
   - Set initial story points and priority
   - Assign to appropriate team member

2. **Task Tracking**
   - Create task breakdown structure
   - Set up progress tracking
   - Define completion criteria

### Expected Deliverables
- [ ] Complete user story definition with acceptance criteria
- [ ] Technical requirements and API specifications
- [ ] Implementation task breakdown
- [ ] Testing strategy and test cases
- [ ] Git branch structure for development
- [ ] Database entry for tracking
- [ ] Handoff templates for team coordination

**Story should align with current sprint goals and epic objectives, using the project's technology stack from .claude/project.json**