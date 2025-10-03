---
description: "Initiate structured handoff between team members with complete context preservation"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Grep", "Glob"]
---

Initiate team handoff: **$ARGUMENTS**

## 🔄 Team Handoff Process

**Expected format**: `/handoff [from-phase]-to-[to-phase] [EPIC/SPRINT/STORY-ID]`
**Examples**: 
- `/handoff planning-to-implementation EPIC-001`
- `/handoff implementation-to-testing STORY-003`
- `/handoff testing-to-production SPRINT-002`

### Phase 1: Context Analysis
1. **Parse Handoff Request**
   - Identify source phase (planning, implementation, testing, review, production)
   - Identify target phase and team member responsibilities
   - Locate epic/sprint/story documentation
   - Understand current work status and deliverables

2. **Current State Assessment**
   - Read all relevant documentation and decisions
   - Check git branches and commit history
   - Review current epic/sprint/story progress
   - Identify completed work and remaining tasks

### Phase 2: Handoff Documentation Creation
1. **Handoff Package Structure**
   ```
   docs/handoffs/[DATE]-[FROM]-to-[TO]-[ID]/
   ├── handoff-summary.md
   ├── context-preservation.md
   ├── decisions-made.md
   ├── deliverables.md
   ├── next-steps.md
   ├── technical-context.md
   └── qa-checklist.md
   ```

2. **Context Preservation**
   - Document all architectural decisions and rationale
   - Capture technical trade-offs and considerations
   - Preserve user requirements and acceptance criteria
   - Record any blockers or dependencies identified

### Phase 3: Git Branch Handoff
1. **Branch Management**
   - Create handoff branch: `[epic/sprint/story]/handoff-[from]-to-[to]`
   - Commit all handoff documentation
   - Create pull request for formal handoff review
   - Tag appropriate team member for review

2. **Code Context**
   - Document current code structure and patterns
   - Explain any temporary solutions or TODOs
   - Highlight areas needing special attention
   - Provide setup and testing instructions

### Phase 4: Phase-Specific Handoffs

#### **Planning → Implementation**
1. **From Architect/PM to Developer**
   - Complete requirements and acceptance criteria
   - Architecture decisions and system design
   - API contracts and data models
   - Testing strategy and quality gates

2. **Implementation Setup**
   - Create implementation branch structure
   - Set up development environment instructions
   - Provide starter templates and boilerplate
   - Define coding standards and patterns

#### **Implementation → Testing/Review**
1. **From Developer to QA/Reviewer**
   - Complete implementation with unit tests
   - Deployment and setup instructions
   - Test data and scenarios
   - Known issues or limitations

2. **Testing Setup**
   - Testing environment configuration
   - Test case execution instructions
   - Performance and security considerations
   - User acceptance criteria validation

#### **Testing → Production**
1. **From QA to DevOps/Production**
   - Complete test results and validation
   - Performance and security audit results
   - Deployment checklist and rollback procedures
   - Monitoring and alerting requirements

### Phase 5: Team Notification
1. **Handoff Notification**
   - Update project database with handoff status
   - Notify receiving team member (based on profiles)
   - Create action items and next steps
   - Set up follow-up checkpoints

2. **Profile-Specific Approach**
   - **From Trimabk (Architect)**: Strategic context, system implications, future considerations
   - **To Sarthak (Developer)**: Practical implementation guide, code patterns, testing approach
   - **Reverse Direction**: Implementation details, practical considerations, optimization opportunities

### Phase 6: Handoff Verification
1. **Completeness Check**
   - Verify all documentation is complete
   - Ensure all decisions are captured
   - Confirm deliverables meet handoff criteria
   - Validate receiving team can proceed

2. **Knowledge Transfer**
   - Schedule handoff meeting if needed
   - Provide demo or walkthrough
   - Answer questions and clarify context
   - Confirm understanding and next steps

### Expected Deliverables
- [ ] Complete handoff documentation package
- [ ] Git branch with all context preserved
- [ ] Pull request for formal handoff review
- [ ] Next steps and action items defined
- [ ] Team member notification and assignment
- [ ] Database updated with handoff status
- [ ] Follow-up checkpoints scheduled

**Handoff ensures zero context loss and smooth transition between team members while preserving all architectural decisions and implementation details.**