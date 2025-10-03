---
description: "Chain multiple commands with context passing between stages for complex workflows"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Grep", "Glob", "TodoWrite"]
---

Execute pipeline: **$ARGUMENTS**

## 🔄 Pipeline Execution System

**Usage**: `/pipe [pipeline-name] [initial-context]`
**Examples**: 
- `/pipe feature-development auth-epic`
- `/pipe hotfix-deployment critical-bug`
- `/pipe quality-check src/`
- `/pipe epic-to-production EPIC-001`

### Phase 1: Pipeline Initialization
1. **Parse Pipeline Request**
   - Extract pipeline name
   - Identify initial context/parameters
   - Locate pipeline definition
   - Validate pipeline exists

2. **Pipeline Setup**
   ```bash
   # Create pipeline workspace
   PIPELINE_ID="pipe-$(date +%Y%m%d-%H%M%S)"
   PIPELINE_DIR="./pipe/$ARGUMENTS-$PIPELINE_ID"
   mkdir -p "$PIPELINE_DIR"
   
   # Initialize pipeline log
   echo "Pipeline: $ARGUMENTS" > "$PIPELINE_DIR/pipeline.log"
   echo "Started: $(date)" >> "$PIPELINE_DIR/pipeline.log"
   ```

### Phase 2: Pipeline Definition Loading
1. **Built-in Pipelines**
   ```yaml
   # Feature Development Pipeline
   name: feature-development
   description: Complete feature from epic to implementation
   steps:
     - epic: Create comprehensive epic
     - sprint: Break down into sprints
     - story: Create user stories
     - git-commit: Commit planning docs
     - handoff: Handoff to implementation
     - test: Run tests
     - review: Code review
     - git-commit: Final commit
   
   # Hotfix Pipeline
   name: hotfix-deployment
   steps:
     - git-hotfix: Create hotfix branch
     - debug: Debug the issue
     - test: Test the fix
     - git-commit: Commit fix
     - git-review-pr: Review changes
     - deploy: Deploy to production
   
   # Quality Pipeline
   name: quality-check
   steps:
     - review: Deep code review
     - test: Run all tests
     - refactor: Suggest improvements
     - git-self-review: Self review
   ```

2. **Custom Pipeline Loading**
   ```markdown
   ## 📁 Loading Pipeline: $ARGUMENTS
   
   ### Pipeline Location Priority
   1. .claude/pipelines/[name].yml
   2. ~/.claude/pipelines/[name].yml
   3. Built-in pipelines
   
   ### Pipeline Loaded
   - Name: feature-development
   - Steps: 8
   - Estimated Duration: 15-30 minutes
   ```

### Phase 3: Context Management
1. **Initial Context Creation**
   ```markdown
   # File: 00-input.md
   ## Pipeline Context
   
   ### Initial Parameters
   - Pipeline: feature-development
   - Context: auth-epic
   - User: [current-profile]
   - Timestamp: 2025-08-15T14:30:00Z
   
   ### Objectives
   - Create authentication epic
   - Plan implementation
   - Set up development environment
   
   ### Constraints
   - Technology: React, Node.js, MongoDB
   - Timeline: 2 sprints
   - Team: 3 developers
   ```

2. **Context Passing Strategy**
   ```markdown
   ## 🔄 Context Flow
   
   Step 1 (epic) → Output: 01-epic-output.md
      ↓ (becomes input for next step)
   Step 2 (sprint) → Output: 02-sprint-output.md
      ↓ (accumulates context)
   Step 3 (story) → Output: 03-story-output.md
      ↓ (enriched context)
   Final Output: pipeline-result.md
   ```

### Phase 4: Step Execution
1. **Step Processing**
   ```markdown
   ## 🎯 Executing Step 1/8: Epic Creation
   
   ### Input Context
   - Previous outputs: None (first step)
   - Parameters: auth-epic
   - Accumulated knowledge: Initial context
   
   ### Executing Command
   `/epic User Authentication System`
   
   ### Capturing Output
   - Documentation created
   - Branches created
   - Database updated
   - Context enriched
   
   ### Output Saved
   - File: 01-epic-output.md
   - Size: 15KB
   - Key Decisions: JWT auth, 2-sprint plan
   ```

2. **Dynamic Step Adaptation**
   ```javascript
   // Each step reads previous context
   const previousContext = readPreviousOutputs();
   const enrichedPrompt = `
     Given the previous context:
     ${previousContext}
     
     Now execute: ${currentStep.command}
     
     Ensure continuity and build upon previous decisions.
   `;
   ```

### Phase 5: Pipeline Orchestration
1. **Execution Flow Control**
   ```markdown
   ## 🎮 Pipeline Control
   
   ### Execution Modes
   - **Sequential**: Each step waits for previous
   - **Parallel**: Independent steps run together
   - **Conditional**: Steps based on conditions
   - **Interactive**: Pause for user input
   
   ### Current Mode: Sequential
   ```

2. **Error Handling**
   ```markdown
   ## ⚠️ Step 4 Failed
   
   ### Error Details
   - Step: git-commit
   - Error: Merge conflict detected
   - Severity: Recoverable
   
   ### Recovery Options
   1. **Retry**: Try step again
   2. **Skip**: Continue without this step
   3. **Fix**: Manual intervention
   4. **Abort**: Stop pipeline
   
   ### Auto-Recovery Attempt
   - Resolving conflict automatically...
   - Conflict resolved ✅
   - Continuing pipeline...
   ```

### Phase 6: Progress Tracking
1. **Real-time Status**
   ```markdown
   ## 📊 Pipeline Progress
   
   ╔════════════════════════════════════════╗
   ║ Feature Development Pipeline           ║
   ╠════════════════════════════════════════╣
   ║ ✅ Step 1: Epic Creation      [2m 15s] ║
   ║ ✅ Step 2: Sprint Breakdown   [1m 30s] ║
   ║ ✅ Step 3: Story Creation     [3m 45s] ║
   ║ 🔄 Step 4: Git Commit         [0m 30s] ║
   ║ ⏸️ Step 5: Handoff                     ║
   ║ ⏸️ Step 6: Testing                     ║
   ║ ⏸️ Step 7: Review                      ║
   ║ ⏸️ Step 8: Final Commit                ║
   ╠════════════════════════════════════════╣
   ║ Progress: ████████░░░░░░░ 45%          ║
   ║ Time Elapsed: 7m 50s                   ║
   ║ Est. Remaining: 9m 10s                 ║
   ╚════════════════════════════════════════╝
   ```

2. **Step Artifacts**
   ```
   ./pipe/auth-epic-20250815-143000/
   ├── 00-input.md                 # Initial context
   ├── 01-epic-output.md           # Epic creation results
   ├── 02-sprint-output.md         # Sprint breakdown
   ├── 03-story-output.md          # User stories
   ├── 04-commit-output.md         # Commit details
   ├── artifacts/
   │   ├── epic-plan.pdf           # Generated documents
   │   ├── sprint-board.json       # Sprint data
   │   └── test-results.xml        # Test outputs
   ├── pipeline.log                # Execution log
   └── pipeline-result.md          # Final summary
   ```

### Phase 7: Advanced Pipeline Features
1. **Conditional Execution**
   ```yaml
   # Conditional pipeline steps
   steps:
     - name: test
       command: /test
       continue_on_failure: false
     
     - name: deploy_staging
       command: /deploy staging
       condition: "test.passed == true"
     
     - name: deploy_production
       command: /deploy production
       condition: "deploy_staging.passed && approval.received"
   ```

2. **Parallel Execution**
   ```yaml
   # Parallel step groups
   parallel_groups:
     - group: quality_checks
       steps:
         - /test --unit
         - /test --integration
         - /review
         - /security-scan
     
     - group: documentation
       steps:
         - /docs api
         - /docs user-guide
   ```

### Phase 8: Pipeline Composition
1. **Sub-Pipelines**
   ```yaml
   # Main pipeline calling sub-pipelines
   name: release-pipeline
   steps:
     - pipeline: quality-check
     - pipeline: security-audit  
     - pipeline: deployment
     - pipeline: monitoring-setup
   ```

2. **Dynamic Pipeline Generation**
   ```markdown
   ## 🧬 Dynamic Pipeline Created
   
   Based on project analysis:
   - Detected: React + Node.js project
   - Test framework: Jest + Playwright
   - CI/CD: GitHub Actions
   
   Generated Pipeline:
   1. /test --unit
   2. /test --integration
   3. /test --e2e
   4. /build
   5. /security-scan
   6. /deploy staging
   7. /smoke-test
   8. /deploy production
   ```

### Phase 9: Pipeline Results
1. **Summary Report**
   ```markdown
   ## ✅ Pipeline Complete: feature-development
   
   ### Execution Summary
   - **Duration**: 18m 32s
   - **Steps Completed**: 8/8
   - **Status**: SUCCESS
   
   ### Key Deliverables
   1. **Epic Created**: EPIC-001 - User Authentication
   2. **Sprints Planned**: 2 sprints, 15 stories
   3. **Branches Created**: 
      - epic/EPIC-001/planning
      - epic/EPIC-001/sprint-001
   4. **Documentation**: 25 files created
   5. **Tests Written**: 45 new tests
   6. **Code Reviewed**: 15 files analyzed
   
   ### Metrics
   - Code Coverage: 85%
   - Test Pass Rate: 100%
   - Performance: No regression
   - Security: No vulnerabilities
   
   ### Next Steps
   1. Review epic documentation
   2. Assign team members
   3. Start sprint 1 development
   4. Schedule planning meeting
   
   ### Artifacts Location
   `./pipe/auth-epic-20250815-143000/`
   ```

2. **Knowledge Accumulation**
   ```markdown
   ## 🧠 Accumulated Knowledge
   
   ### Decisions Made
   - Authentication: JWT with refresh tokens
   - Database: MongoDB with user collection
   - Testing: Jest for unit, Playwright for E2E
   - Deployment: Docker containers on AWS
   
   ### Patterns Identified
   - Service layer architecture
   - Repository pattern for data access
   - Middleware for authentication
   - Error handling standards
   
   ### Risks Identified
   - Session management complexity
   - Token refresh edge cases
   - Rate limiting requirements
   - GDPR compliance needs
   ```

### Phase 10: Pipeline Management
1. **Pipeline Commands**
   ```bash
   # List available pipelines
   /pipe --list
   
   # Show pipeline details
   /pipe --info feature-development
   
   # Resume interrupted pipeline
   /pipe --resume pipe-20250815-143000
   
   # Clean old pipeline runs
   /pipe --clean --older-than 7d
   ```

2. **Pipeline Monitoring**
   ```markdown
   ## 📈 Pipeline Analytics
   
   ### Recent Executions
   - feature-development: 5 runs, 80% success
   - hotfix-deployment: 3 runs, 100% success
   - quality-check: 12 runs, 92% success
   
   ### Performance Trends
   - Average duration: 15m (↓ 2m from last week)
   - Success rate: 87% (↑ 5% from last week)
   - Most failed step: test (3 failures)
   
   ### Optimization Suggestions
   - Parallelize test execution (-5m)
   - Cache dependencies (-2m)
   - Skip unchanged modules (-3m)
   ```

### Expected Deliverables
- [ ] Pipeline workspace created with full tracking
- [ ] Context passed and enriched between steps
- [ ] Each step executed with accumulated knowledge
- [ ] Progress tracked with real-time updates
- [ ] Artifacts collected and organized
- [ ] Error handling and recovery implemented
- [ ] Comprehensive summary report generated
- [ ] Knowledge accumulated for future use

**Pipeline system enables complex multi-step workflows with intelligent context management and comprehensive tracking.**