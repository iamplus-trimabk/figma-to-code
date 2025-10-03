---
description: "Execute predefined multi-step workflows with checkpoints and validation"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Grep", "TodoWrite"]
---

Execute workflow: **$ARGUMENTS**

## 🔄 Workflow Execution System

**Usage**: `/workflow [workflow-name] [parameters]`
**Examples**: 
- `/workflow epic-to-production EPIC-001`
- `/workflow daily-standup`
- `/workflow release-preparation v2.0.0`
- `/workflow sprint-planning SPRINT-005`

### Phase 1: Workflow Discovery
1. **Available Workflows**
   ```markdown
   ## 📚 Workflow Library
   
   ### Development Workflows
   - **epic-to-production**: Complete epic lifecycle
   - **feature-development**: Feature branch workflow
   - **bug-fix**: Bug investigation and fix
   - **technical-debt**: Refactoring workflow
   
   ### Team Workflows
   - **daily-standup**: Generate standup report
   - **sprint-planning**: Sprint setup and planning
   - **sprint-review**: Sprint retrospective
   - **release-preparation**: Release checklist
   
   ### Maintenance Workflows
   - **dependency-update**: Update dependencies safely
   - **security-audit**: Security assessment
   - **performance-tuning**: Performance optimization
   - **database-migration**: Database updates
   ```

2. **Workflow Selection**
   - Parse workflow name
   - Load workflow definition
   - Validate parameters
   - Check prerequisites

### Phase 2: Workflow Definition
1. **Epic-to-Production Workflow**
   ```yaml
   name: epic-to-production
   description: Complete epic from planning to production
   parameters:
     - epic_id: Epic identifier (required)
     - priority: high|medium|low (optional)
   
   phases:
     planning:
       steps:
         - create_epic: /epic $epic_id
         - break_down: /sprint planning under $epic_id
         - create_stories: /story from sprint backlog
         - estimate: Estimate story points
       checkpoint: Epic planning complete
       approval_required: true
     
     development:
       steps:
         - setup_branches: Create feature branches
         - implement: Development work
         - unit_tests: /test --unit
         - integration_tests: /test --integration
       checkpoint: Development complete
       validation: All tests passing
     
     review:
       steps:
         - code_review: /review feature branch
         - security_review: /security-scan
         - performance_check: /performance-test
       checkpoint: Reviews complete
       approval_required: true
     
     deployment:
       steps:
         - staging_deploy: Deploy to staging
         - e2e_tests: /test --e2e staging
         - production_deploy: Deploy to production
         - smoke_tests: Verify production
       checkpoint: Deployment complete
       rollback_plan: required
   ```

2. **Sprint Planning Workflow**
   ```yaml
   name: sprint-planning
   description: Set up and plan a new sprint
   
   steps:
     preparation:
       - review_backlog: Review product backlog
       - prioritize: Prioritize stories
       - estimate: Story point estimation
     
     planning:
       - capacity: Calculate team capacity
       - commit: Commit to sprint goals
       - assign: Assign stories to team
     
     setup:
       - create_board: Set up sprint board
       - schedule: Schedule ceremonies
       - communicate: Notify team
   ```

### Phase 3: Workflow Execution
1. **Phase-Based Execution**
   ```markdown
   ## 🎯 Executing Workflow: epic-to-production
   
   ### Current Phase: Planning (1/4)
   
   #### Steps Completed
   ✅ Create epic structure
   ✅ Break down into sprints
   ✅ Generate user stories
   🔄 Estimating story points...
   
   #### Phase Progress: 75%
   
   ### Checkpoint Approaching
   - Approval needed from: Tech Lead
   - Documents to review: Epic plan, Sprint breakdown
   - Deadline: End of day
   ```

2. **Step Execution with Validation**
   ```markdown
   ## ✅ Step Validation
   
   ### Step: unit_tests
   **Expected**: All tests passing
   **Actual**: 245/250 passing
   **Status**: ❌ FAILED
   
   ### Failure Handling
   - Attempting auto-fix...
   - Running /debug failing tests
   - Retrying tests...
   - Success! All tests now passing ✅
   ```

### Phase 4: Checkpoint Management
1. **Checkpoint Validation**
   ```markdown
   ## 🚩 Checkpoint: Planning Complete
   
   ### Validation Criteria
   - ✅ Epic documentation complete
   - ✅ All sprints defined
   - ✅ Stories estimated
   - ✅ Resources allocated
   - ✅ Risks identified
   
   ### Approval Status
   - Technical Lead: ✅ Approved
   - Product Owner: ⏳ Pending
   - QA Lead: ✅ Approved
   
   ### Next Phase Blocked Until
   - Product Owner approval received
   ```

2. **Checkpoint Artifacts**
   ```markdown
   ## 📦 Checkpoint Artifacts
   
   ### Planning Phase Deliverables
   - Epic overview document
   - Sprint breakdown (2 sprints)
   - User stories (15 stories)
   - Technical design document
   - Risk assessment matrix
   - Resource allocation plan
   
   ### Review Package
   - Location: ./workflows/EPIC-001/planning/
   - Size: 125 KB
   - Format: Markdown + Diagrams
   ```

### Phase 5: Workflow State Management
1. **State Persistence**
   ```json
   {
     "workflow": "epic-to-production",
     "id": "wf-20250815-143000",
     "parameters": {
       "epic_id": "EPIC-001",
       "priority": "high"
     },
     "current_phase": "development",
     "current_step": 3,
     "status": "in_progress",
     "started": "2025-08-15T14:30:00Z",
     "checkpoints_passed": ["planning"],
     "context": {
       "branches_created": ["feature/auth"],
       "tests_written": 45,
       "coverage": 85
     }
   }
   ```

2. **Resume Capability**
   ```markdown
   ## 🔄 Resuming Workflow
   
   ### Found Incomplete Workflow
   - ID: wf-20250815-143000
   - Type: epic-to-production
   - Last Active: 2 hours ago
   - Progress: Development phase (60%)
   
   ### Resume Options
   1. **Continue**: Pick up where left off
   2. **Restart Phase**: Restart current phase
   3. **Skip to Next**: Move to next phase
   4. **Abort**: Cancel workflow
   
   Resuming from: integration_tests step...
   ```

### Phase 6: Workflow Automation
1. **Daily Standup Workflow**
   ```markdown
   ## 📅 Daily Standup Report
   
   ### Team Member: [current-profile]
   ### Date: 2025-08-15
   
   #### Yesterday's Accomplishments
   ```bash
   git log --author="[user]" --since="yesterday" --oneline
   ```
   - ✅ Completed user authentication API
   - ✅ Fixed bug in password reset
   - ✅ Reviewed PR #123
   
   #### Today's Plan
   ```bash
   # Check assigned issues
   gh issue list --assignee="[user]"
   ```
   - 🎯 Implement 2FA support
   - 🎯 Write tests for auth module
   - 🎯 Deploy to staging
   
   #### Blockers
   - ⚠️ Waiting for API key from DevOps
   - ⚠️ Need review on PR #125
   
   #### Metrics
   - Commits: 8
   - Lines changed: +450 -125
   - PRs merged: 2
   - Issues closed: 3
   ```

2. **Release Preparation Workflow**
   ```markdown
   ## 🚀 Release Preparation: v2.0.0
   
   ### Pre-Release Checklist
   - ✅ All features complete
   - ✅ All tests passing
   - ✅ Security audit clean
   - ✅ Performance benchmarks met
   - ✅ Documentation updated
   - 🔄 Release notes drafted
   - ⏸️ Changelog updated
   - ⏸️ Version bumped
   - ⏸️ Tags created
   - ⏸️ Deployment plan ready
   
   ### Automated Steps
   1. Running final test suite...
   2. Building release artifacts...
   3. Generating changelog...
   4. Creating release branch...
   5. Preparing deployment scripts...
   ```

### Phase 7: Workflow Orchestration
1. **Parallel Workflow Execution**
   ```markdown
   ## ⚡ Parallel Execution
   
   ### Running in Parallel
   
   #### Track 1: Backend Development
   - API implementation
   - Database setup
   - Unit tests
   
   #### Track 2: Frontend Development
   - UI components
   - State management
   - Component tests
   
   #### Track 3: Infrastructure
   - Docker setup
   - CI/CD pipeline
   - Monitoring setup
   
   ### Synchronization Point
   - All tracks must complete before integration
   - ETA: Track 1 (45m), Track 2 (30m), Track 3 (60m)
   ```

2. **Conditional Workflow Paths**
   ```yaml
   # Conditional workflow execution
   steps:
     - analyze_changes: Detect what changed
     
     - if: changes.includes('database')
       then:
         - run_migrations
         - validate_schema
         - update_seeds
     
     - if: changes.includes('api')
       then:
         - regenerate_docs
         - update_postman
         - test_endpoints
     
     - if: is_hotfix
       then:
         - expedited_review
         - direct_to_production
       else:
         - standard_review
         - staging_first
   ```

### Phase 8: Workflow Metrics
1. **Performance Tracking**
   ```markdown
   ## 📊 Workflow Metrics
   
   ### Execution Statistics
   - Workflow: epic-to-production
   - Total Runs: 15
   - Success Rate: 87%
   - Average Duration: 2h 15m
   - Fastest Run: 1h 45m
   - Slowest Run: 3h 30m
   
   ### Bottleneck Analysis
   1. **Test Phase**: 45m average (30% of time)
   2. **Review Phase**: 35m average (25% of time)
   3. **Deployment**: 30m average (22% of time)
   
   ### Optimization Opportunities
   - Parallelize test execution: -15m
   - Automate review checks: -10m
   - Cache build artifacts: -8m
   ```

2. **Success Patterns**
   ```markdown
   ## ✨ Success Patterns Identified
   
   ### Successful Workflows Share
   - Early morning execution (less contention)
   - Smaller epic scope (<20 stories)
   - Automated test coverage >80%
   - Pre-workflow dependency check
   
   ### Failure Patterns
   - Missing prerequisites (40% of failures)
   - Test failures (30% of failures)
   - Approval delays (20% of failures)
   - Environment issues (10% of failures)
   ```

### Phase 9: Workflow Templates
1. **Custom Workflow Creation**
   ```yaml
   # Template for custom workflow
   name: custom-deployment
   description: Custom deployment workflow
   
   template_variables:
     - environment: ${ENV}
     - version: ${VERSION}
     - region: ${REGION}
   
   steps:
     - validate: /test --smoke
     - backup: Create backup of ${ENV}
     - deploy: Deploy ${VERSION} to ${ENV}
     - verify: Health check ${ENV}
     - notify: Send deployment notification
   
   rollback:
     trigger: Health check fails
     steps:
       - restore: Restore from backup
       - alert: Page on-call engineer
   ```

### Phase 10: Workflow Reporting
1. **Execution Report**
   ```markdown
   ## 📄 Workflow Execution Report
   
   ### Summary
   - **Workflow**: epic-to-production
   - **Epic**: EPIC-001 - User Authentication
   - **Duration**: 2h 34m
   - **Status**: ✅ COMPLETED
   
   ### Phase Results
   | Phase | Duration | Status | Notes |
   |-------|----------|--------|-------|
   | Planning | 45m | ✅ | All stories estimated |
   | Development | 1h 15m | ✅ | 98% test coverage |
   | Review | 25m | ✅ | 2 minor issues fixed |
   | Deployment | 9m | ✅ | Zero downtime |
   
   ### Key Achievements
   - Zero production issues
   - 15% performance improvement
   - 100% backward compatible
   - Full documentation coverage
   
   ### Lessons Learned
   - Parallel testing saved 20m
   - Early reviews prevented rework
   - Automated checks caught 5 issues
   
   ### Recommendations
   - Implement more parallel steps
   - Add performance benchmarks
   - Increase automation coverage
   ```

### Expected Deliverables
- [ ] Workflow selected and parameters validated
- [ ] Phase-based execution with checkpoints
- [ ] State management and resume capability
- [ ] Parallel and conditional execution support
- [ ] Comprehensive metrics and reporting
- [ ] Checkpoint artifacts and approvals
- [ ] Success/failure pattern analysis
- [ ] Complete execution report with insights

**Workflow system provides structured, repeatable processes with checkpoints, validation, and comprehensive tracking.**