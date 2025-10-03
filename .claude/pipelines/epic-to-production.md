# Epic to Production Pipeline
*Hierarchical Epic → Sprint → Story workflow with proper branch management*

## Pipeline Flow:
1. **Epic Phase**: Create sprints for current epic
2. **Sprint Phase**: Create and complete all stories in current sprint  
3. **Story Phase**: Complete individual story with implementation
4. **Completion Flow**: Story → Sprint → Epic → Next Epic

## Epic Phase: Create Sprints

### Task E1: Initialize Epic Implementation
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID-implementation
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-$EPIC_ID-implementation
3. If branch switching fails, error out: "Cannot switch to epic implementation branch"

Initialize Epic $EPIC_ID for implementation:

Read epic details from: docs/epics/$EPIC_ID/README.md
Read feature context from: .claude/$FEATURE_NAME/pipeline-context.md

Tasks:
1. Create epic implementation directory: .claude/$FEATURE_NAME/epic-$EPIC_ID/
2. Review epic objectives and success criteria
3. Identify all sprints needed for this epic (typically 2-3 sprints)
4. Create sprint planning structure

Set environment variables:
- CURRENT_EPIC_ID=$EPIC_ID
- EPIC_SPRINT_COUNT=[number of sprints needed]

Output files:
- .claude/$FEATURE_NAME/epic-$EPIC_ID/implementation-plan.md
- .claude/$FEATURE_NAME/epic-$EPIC_ID/sprint-breakdown.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Initialize Epic $EPIC_ID implementation"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/epic-$EPIC_ID-implementation
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch

Next: Run Sprint Creation Pipeline for Sprint 1
```

### Task E2: Create Sprint 1
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID-sprint-001
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-$EPIC_ID-sprint-001

Create Sprint 1 for Epic $EPIC_ID:

Read context from: .claude/$FEATURE_NAME/epic-$EPIC_ID/sprint-breakdown.md

Execute sprint creation:
/sprint-simple "[Sprint 1 Name]" under $EPIC_ID

Sprint 1 Focus:
- Foundation and core architecture
- Essential infrastructure setup
- Basic functionality implementation
- Security and authentication basics

Set environment variables:
- CURRENT_SPRINT_ID=[generated sprint ID]
- SPRINT_NUMBER=001

Output files:
- Sprint documentation in git structure
- Update .claude/$FEATURE_NAME/epic-$EPIC_ID/implementation-plan.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Create Sprint 1 for Epic $EPIC_ID"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/epic-$EPIC_ID-sprint-001
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch

Next: Run Story Creation Pipeline for Sprint 1
```

### Task E3: Create Sprint 2
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID-sprint-002
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-$EPIC_ID-sprint-002

Create Sprint 2 for Epic $EPIC_ID:

Read context from: .claude/$FEATURE_NAME/epic-$EPIC_ID/sprint-breakdown.md

Execute sprint creation:
/sprint-simple "[Sprint 2 Name]" under $EPIC_ID

Sprint 2 Focus:
- User experience and interface
- Advanced features and integrations
- Performance optimization
- Testing and quality assurance

Set environment variables:
- CURRENT_SPRINT_ID=[generated sprint ID]  
- SPRINT_NUMBER=002

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Create Sprint 2 for Epic $EPIC_ID"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/epic-$EPIC_ID-sprint-002
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch

Next: Continue with Sprint 3 if needed, or proceed to Story Pipeline
```

## Sprint Phase: Create and Complete Stories

### Task S1: Create Stories for Current Sprint
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/sprint-$SPRINT_ID-stories
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/sprint-$SPRINT_ID-stories

Create user stories for Sprint $SPRINT_ID:

Read context from:
- docs/epics/$EPIC_ID/sprints/$SPRINT_ID/README.md
- .claude/$FEATURE_NAME/pm-product-strategy.md (for personas)

Create 3-5 user stories:
/story-simple "As [persona] I want [core need] so that [value]" in $SPRINT_ID

Stories should focus on:
- Core user value delivery
- Technical foundation needed
- Essential user journeys
- Measurable outcomes

Set environment variables:
- STORY_IDS=[comma-separated list of story IDs]
- STORY_COUNT=[number of stories created]

Output files:
- All story documentation in git structure
- .claude/$FEATURE_NAME/sprint-$SPRINT_ID/story-list.md

Completion Steps:
1. Commit: "feat($FEATURE_NAME): Create stories for Sprint $SPRINT_ID"
2. Switch to: feature-$FEATURE_NAME
3. Merge: git merge feature-$FEATURE_NAME/sprint-$SPRINT_ID-stories
4. Push: git push origin feature-$FEATURE_NAME
5. Delete task branch

Next: Run Story Implementation Pipeline for each story
```

### Task S2: Implement Story 1
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/story-$STORY_ID-implementation
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/story-$STORY_ID-implementation

Implement Story $STORY_ID:

Read requirements from: docs/epics/$EPIC_ID/sprints/$SPRINT_ID/stories/$STORY_ID/README.md

Implementation Tasks:
1. **Analysis**: Review acceptance criteria and technical requirements
2. **Design**: Create technical design and architecture approach
3. **Implementation**: Write production-ready code
4. **Testing**: Create comprehensive unit and integration tests
5. **Documentation**: Update API docs and implementation notes
6. **Validation**: Verify all acceptance criteria are met

Focus Areas:
- Follow existing code patterns and conventions
- Implement proper error handling and logging
- Add comprehensive test coverage
- Update documentation and README files
- Ensure security best practices

Create real, working code - not just documentation.

Output files:
- All implementation code in appropriate directories
- Test files with comprehensive coverage
- Updated documentation
- .claude/$FEATURE_NAME/story-$STORY_ID/implementation-report.md

Completion Steps:
1. Run tests: npm test (must pass)
2. Run linting: npm run lint (if available)
3. Commit: "feat($FEATURE_NAME): Complete Story $STORY_ID - [Story Title]"
4. Switch to: feature-$FEATURE_NAME
5. Merge: git merge feature-$FEATURE_NAME/story-$STORY_ID-implementation
6. Push: git push origin feature-$FEATURE_NAME
7. Delete task branch

Mark story as COMPLETED in pipeline tracking.
```

### Task S3: Implement Story 2
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/story-$STORY_ID-implementation
**Prompt**:
```
[Same pattern as S2 but for next story in sprint]

Continue implementing all stories in current sprint before proceeding to sprint completion.
```

### Task S4: Complete Sprint
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/sprint-$SPRINT_ID-completion
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/sprint-$SPRINT_ID-completion

Complete Sprint $SPRINT_ID:

Verify all stories in sprint are completed:
- Read .claude/$FEATURE_NAME/sprint-$SPRINT_ID/story-list.md
- Confirm all stories have been implemented and tested
- Run comprehensive test suite for sprint scope

Sprint Completion Tasks:
1. **Integration Testing**: Test all stories working together
2. **Performance Validation**: Ensure performance requirements met
3. **Security Review**: Validate security requirements
4. **Documentation Update**: Update sprint documentation
5. **Demo Preparation**: Create demo/showcase materials
6. **Sprint Retrospective**: Document lessons learned

Output files:
- .claude/$FEATURE_NAME/sprint-$SPRINT_ID/completion-report.md
- .claude/$FEATURE_NAME/sprint-$SPRINT_ID/demo-guide.md
- Test reports and coverage analysis

Completion Steps:
1. Run full test suite: npm test
2. Commit: "feat($FEATURE_NAME): Complete Sprint $SPRINT_ID with all stories"
3. Switch to: feature-$FEATURE_NAME
4. Merge: git merge feature-$FEATURE_NAME/sprint-$SPRINT_ID-completion
5. Push: git push origin feature-$FEATURE_NAME
6. Delete task branch

Mark sprint as COMPLETED.
Next: Move to next sprint in epic or complete epic if all sprints done.
```

## Epic Completion

### Task EC1: Complete Epic
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/epic-$EPIC_ID-completion
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/epic-$EPIC_ID-completion

Complete Epic $EPIC_ID:

Verify all sprints in epic are completed:
- Confirm all sprint completion reports exist
- Validate epic objectives have been met
- Run comprehensive testing across entire epic scope

Epic Completion Tasks:
1. **Epic Integration Testing**: Test complete epic functionality
2. **Performance Benchmarking**: Measure against epic success criteria
3. **Security Audit**: Complete security review for epic scope
4. **User Acceptance Testing**: Validate against user needs
5. **Documentation Finalization**: Complete epic documentation
6. **Epic Demo**: Create comprehensive demo of epic value

Success Criteria Validation:
- Review each success criterion from epic README
- Provide evidence of completion for each criterion
- Document any deviations or scope changes

Output files:
- .claude/$FEATURE_NAME/epic-$EPIC_ID/completion-report.md
- .claude/$FEATURE_NAME/epic-$EPIC_ID/success-criteria-validation.md
- .claude/$FEATURE_NAME/epic-$EPIC_ID/epic-demo-guide.md

Completion Steps:
1. Run full test suite for epic: npm test
2. Commit: "feat($FEATURE_NAME): Complete Epic $EPIC_ID - [Epic Name]"
3. Switch to: feature-$FEATURE_NAME
4. Merge: git merge feature-$FEATURE_NAME/epic-$EPIC_ID-completion
5. Push: git push origin feature-$FEATURE_NAME
6. Delete task branch

Mark epic as COMPLETED.
Next: Move to next epic in feature or complete epic if all epics done.
```

## Feature Completion

### Task FC1: Complete Feature
**Agent**: general-purpose
**Branch**: feature-$FEATURE_NAME/feature-completion
**Prompt**:
```
Branch Management:
1. Ensure on feature-$FEATURE_NAME branch
2. Create and switch to: feature-$FEATURE_NAME/feature-completion

Complete Feature $FEATURE_NAME:

Verify all epics in feature are completed:
- Confirm all epic completion reports exist
- Validate feature vision has been delivered
- Run comprehensive testing across entire feature

Feature Completion Tasks:
1. **End-to-End Testing**: Complete user journey validation
2. **Performance Benchmarking**: Final performance validation
3. **Security Audit**: Complete security review
4. **Production Readiness**: Deployment and operations validation
5. **User Documentation**: Complete user guides and documentation
6. **Feature Launch Plan**: Go-to-market readiness

Final Deliverables:
- Complete working feature implementation
- Comprehensive test suite with high coverage
- Production deployment configuration
- User documentation and guides
- Performance and security validation
- Go-to-market launch plan

Output files:
- .claude/$FEATURE_NAME/FEATURE-COMPLETION-REPORT.md
- .claude/$FEATURE_NAME/PRODUCTION-READINESS-CHECKLIST.md
- .claude/$FEATURE_NAME/LAUNCH-PLAN.md

Completion Steps:
1. Run complete test suite: npm test
2. Run production validation: npm run build
3. Commit: "feat($FEATURE_NAME): Complete Feature $FEATURE_NAME - Production Ready"
4. Switch to: feature-$FEATURE_NAME
5. Merge: git merge feature-$FEATURE_NAME/feature-completion
6. Push: git push origin feature-$FEATURE_NAME
7. Delete task branch

Feature $FEATURE_NAME is now PRODUCTION READY! 🚀
```

## Pipeline Usage:

1. **Start with Epic**: `Task E1: Initialize Epic Implementation`
2. **Create Sprints**: `Task E2, E3: Create Sprint 1, 2`
3. **For Each Sprint**: 
   - `Task S1: Create Stories`
   - `Task S2, S3: Implement each Story`
   - `Task S4: Complete Sprint`
4. **Complete Epic**: `Task EC1: Complete Epic`
5. **Repeat for all Epics in Feature**
6. **Complete Feature**: `Task FC1: Complete Feature`

**Branch Strategy**: Each task creates its own branch, implements, commits, merges back to feature branch, and pushes.

**Error Handling**: If any branch switching fails, stop execution and ask user to fix git conflicts.