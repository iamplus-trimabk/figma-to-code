---
description: "Create custom pipeline definition with steps, conditions, and error handling"
allowed_tools: ["Write", "Read", "Edit", "Bash"]
---

Create custom pipeline: **$ARGUMENTS**

## 🏗️ Pipeline Creation Wizard

**Usage**: `/pipeline-create [pipeline-name]`
**Examples**: 
- `/pipeline-create feature-deployment`
- `/pipeline-create data-migration`
- `/pipeline-create security-audit`
- `/pipeline-create ml-training`

### Phase 1: Pipeline Design
1. **Interactive Pipeline Builder**
   ```markdown
   ## 🎨 Pipeline Creation: $ARGUMENTS
   
   ### Basic Information
   - **Name**: feature-deployment
   - **Description**: Deploy feature from development to production
   - **Author**: [current-profile]
   - **Created**: 2025-08-15
   
   ### Pipeline Type
   1. ✅ **Sequential**: Steps run one after another
   2. ⬜ **Parallel**: Steps run simultaneously
   3. ⬜ **Hybrid**: Mix of sequential and parallel
   4. ⬜ **Conditional**: Steps based on conditions
   
   ### Estimated Duration
   - Minimum: 15 minutes
   - Average: 30 minutes
   - Maximum: 1 hour
   ```

2. **Step Definition Wizard**
   ```markdown
   ## 📝 Define Pipeline Steps
   
   ### Step 1
   - **Name**: validate_code
   - **Command**: /review
   - **Description**: Review code quality and standards
   - **Required**: Yes
   - **Continue on Failure**: No
   - **Timeout**: 5 minutes
   
   ### Step 2
   - **Name**: run_tests
   - **Command**: /test --all
   - **Description**: Execute complete test suite
   - **Required**: Yes
   - **Continue on Failure**: No
   - **Success Criteria**: coverage > 80%
   
   ### Add More Steps?
   [Yes] [No] [Import from template]
   ```

### Phase 2: Pipeline Structure
1. **YAML Generation**
   ```yaml
   # Generated pipeline: feature-deployment.yml
   name: feature-deployment
   description: Deploy feature from development to production
   author: [current-profile]
   version: 1.0.0
   created: 2025-08-15
   
   # Input parameters
   parameters:
     feature_branch:
       type: string
       required: true
       description: Feature branch to deploy
     
     environment:
       type: string
       required: false
       default: staging
       enum: [development, staging, production]
     
     skip_tests:
       type: boolean
       required: false
       default: false
   
   # Environment variables
   env:
     NODE_ENV: ${environment}
     DEPLOY_KEY: ${secrets.DEPLOY_KEY}
     SLACK_WEBHOOK: ${secrets.SLACK_WEBHOOK}
   
   # Pipeline steps
   steps:
     # Validation phase
     - id: validate
       name: Code Validation
       command: /review ${feature_branch}
       required: true
       continue_on_error: false
     
     # Testing phase
     - id: test
       name: Run Tests
       command: /test --all
       condition: ${skip_tests} == false
       success_criteria:
         - test_coverage: ">= 80"
         - test_failures: "== 0"
     
     # Build phase
     - id: build
       name: Build Application
       command: |
         npm run build:${environment}
       artifacts:
         - dist/
         - build/
     
     # Deploy phase
     - id: deploy
       name: Deploy to ${environment}
       command: |
         /deploy ${environment} ${feature_branch}
       requires:
         - validate
         - test
         - build
     
     # Verify phase
     - id: verify
       name: Verify Deployment
       command: |
         /health-check ${environment}
       retry:
         attempts: 3
         delay: 30s
   
   # Error handling
   on_failure:
     - command: /rollback ${environment}
     - notify: slack
     - create_issue: true
   
   # Success actions
   on_success:
     - notify: slack
     - merge_pr: true
     - tag_release: true
   ```

2. **Visual Pipeline Builder**
   ```markdown
   ## 🔗 Pipeline Flow Visualization
   
   ```mermaid
   graph LR
     Start([Start]) --> Validate[Code Validation]
     Validate --> Test{Skip Tests?}
     Test -->|No| RunTests[Run Tests]
     Test -->|Yes| Build[Build]
     RunTests --> Build
     Build --> Deploy[Deploy]
     Deploy --> Verify[Verify]
     Verify --> Success([Success])
     
     Validate -->|Fail| Rollback[Rollback]
     RunTests -->|Fail| Rollback
     Build -->|Fail| Rollback
     Deploy -->|Fail| Rollback
     Verify -->|Fail| Rollback
     Rollback --> Failed([Failed])
   ```
   ```

### Phase 3: Advanced Features
1. **Parallel Execution Groups**
   ```yaml
   # Parallel step definition
   parallel_groups:
     - group_name: quality_checks
       max_parallel: 4
       steps:
         - id: lint
           command: /lint
         - id: security
           command: /security-scan
         - id: performance
           command: /performance-test
         - id: accessibility
           command: /a11y-check
     
     - group_name: multi_env_test
       strategy: matrix
       matrix:
         environment: [dev, staging, prod]
         region: [us-east, eu-west, ap-south]
       steps:
         - command: /test-env ${environment} ${region}
   ```

2. **Conditional Logic**
   ```yaml
   # Complex conditions
   steps:
     - id: check_branch
       command: git branch --show-current
       output: current_branch
     
     - id: production_checks
       condition: |
         ${current_branch} == "main" && 
         ${environment} == "production"
       steps:
         - command: /security-audit --deep
         - command: /performance-baseline
         - command: /backup-production
     
     - id: feature_checks
       condition: ${current_branch} =~ "feature/*"
       steps:
         - command: /test --feature
         - command: /review --light
   ```

### Phase 4: Pipeline Templates
1. **Template Library**
   ```markdown
   ## 📚 Available Templates
   
   ### CI/CD Templates
   1. **node-deployment**: Node.js app deployment
   2. **react-spa**: React SPA build and deploy
   3. **python-api**: Python API deployment
   4. **docker-compose**: Multi-container deployment
   
   ### Data Templates
   1. **etl-pipeline**: Extract-Transform-Load
   2. **database-migration**: Safe DB migrations
   3. **backup-restore**: Backup and restore flow
   
   ### ML Templates
   1. **model-training**: ML model training pipeline
   2. **model-deployment**: Deploy ML model
   3. **data-preprocessing**: Data prep pipeline
   
   ### Select Template
   - Using template: node-deployment
   - Customizing for your needs...
   ```

2. **Template Customization**
   ```yaml
   # Extending template
   extends: templates/node-deployment
   
   # Override specific steps
   overrides:
     steps:
       test:
         command: /test --coverage --watch=false
         timeout: 10m
     
     deploy:
         pre_deploy:
           - command: /database-migrate
           - command: /cache-clear
   
   # Add custom steps
   additional_steps:
     - id: notify_team
       command: /slack-notify "Deployment complete"
       when: always
   ```

### Phase 5: Validation & Testing
1. **Pipeline Validation**
   ```markdown
   ## ✅ Pipeline Validation
   
   ### Syntax Check
   - ✅ Valid YAML structure
   - ✅ All required fields present
   - ✅ Commands are valid
   - ✅ No circular dependencies
   
   ### Logic Validation
   - ✅ All referenced variables defined
   - ✅ Conditions are valid expressions
   - ✅ Artifacts paths exist
   - ⚠️ Warning: Long timeout on step 'deploy'
   
   ### Simulation
   - Running dry-run simulation...
   - Estimated duration: 25-35 minutes
   - Resource requirements: 2 CPU, 4GB RAM
   - Potential bottlenecks: test phase (15m)
   ```

2. **Test Pipeline**
   ```markdown
   ## 🧪 Test Pipeline Execution
   
   ### Dry Run Mode
   - Executing pipeline in simulation mode
   - No actual commands executed
   - Validating flow and conditions
   
   ### Step Simulation
   1. validate: Would run /review (est. 2m)
   2. test: Would run /test --all (est. 15m)
   3. build: Would run npm build (est. 5m)
   4. deploy: Would run /deploy (est. 3m)
   5. verify: Would run /health-check (est. 1m)
   
   ### Simulation Results
   - ✅ Pipeline flow valid
   - ✅ All conditions resolvable
   - ✅ Resources available
   - ✅ No conflicts detected
   ```

### Phase 6: Pipeline Storage
1. **Save Pipeline**
   ```markdown
   ## 💾 Save Pipeline Configuration
   
   ### Storage Locations
   1. **Project**: .claude/pipelines/feature-deployment.yml
   2. **Personal**: ~/.claude/pipelines/feature-deployment.yml
   3. **Shared**: team/pipelines/feature-deployment.yml
   
   ### Versioning
   - Version: 1.0.0
   - Previous versions backed up
   - Change history tracked
   
   ### Access Control
   - Owner: [current-profile]
   - Permissions: team-readable
   - Approval required for changes: Yes
   ```

2. **Pipeline Registry**
   ```json
   {
     "pipeline": "feature-deployment",
     "version": "1.0.0",
     "location": ".claude/pipelines/feature-deployment.yml",
     "author": "[current-profile]",
     "created": "2025-08-15T14:30:00Z",
     "last_modified": "2025-08-15T14:45:00Z",
     "tags": ["deployment", "ci-cd", "node"],
     "usage_count": 0,
     "success_rate": null,
     "average_duration": null
   }
   ```

### Phase 7: Pipeline Documentation
1. **Auto-Generated Docs**
   ```markdown
   # Pipeline: feature-deployment
   
   ## Overview
   Deploy feature from development to production with comprehensive validation, testing, and rollback capabilities.
   
   ## Parameters
   | Name | Type | Required | Default | Description |
   |------|------|----------|---------|-------------|
   | feature_branch | string | Yes | - | Feature branch to deploy |
   | environment | string | No | staging | Target environment |
   | skip_tests | boolean | No | false | Skip test execution |
   
   ## Steps
   1. **validate**: Code quality validation
   2. **test**: Complete test suite execution
   3. **build**: Application build process
   4. **deploy**: Deploy to target environment
   5. **verify**: Post-deployment verification
   
   ## Usage
   ```bash
   /pipeline-run feature-deployment feature_branch=feature/auth environment=staging
   ```
   
   ## Error Handling
   - Automatic rollback on failure
   - Slack notifications
   - Issue creation for tracking
   ```

### Phase 8: Pipeline Sharing
1. **Export Pipeline**
   ```markdown
   ## 📤 Export Pipeline
   
   ### Export Format
   - ✅ YAML (native)
   - ⬜ JSON
   - ⬜ GitHub Actions
   - ⬜ Jenkins Pipeline
   - ⬜ CircleCI Config
   
   ### Export Complete
   - File: feature-deployment.yml
   - Size: 4.2 KB
   - Checksum: sha256:abc123...
   
   ### Sharing Options
   - Copy to clipboard
   - Upload to GitHub Gist
   - Share via team repository
   - Email to team
   ```

2. **Import Pipeline**
   ```markdown
   ## 📥 Import Pipeline
   
   ### Import Source
   - From file: pipeline.yml
   - From URL: https://gist.github.com/...
   - From template: company-standard
   
   ### Import Validation
   - ✅ Valid pipeline format
   - ✅ Compatible version
   - ⚠️ Warning: Uses different test framework
   - ✅ All commands available
   
   ### Import Options
   - [ ] Keep original name
   - [x] Rename to: my-feature-deployment
   - [x] Adapt to current project
   - [ ] Import as template
   ```

### Phase 9: Pipeline Optimization
1. **Performance Analysis**
   ```markdown
   ## ⚡ Pipeline Optimization Suggestions
   
   ### Parallelization Opportunities
   - Steps 2, 3, 4 can run in parallel
   - Estimated time saving: 10 minutes
   
   ### Caching Opportunities
   - Cache node_modules: -3 minutes
   - Cache build artifacts: -2 minutes
   - Cache test results: -1 minute
   
   ### Resource Optimization
   - Current: Sequential, 1 worker
   - Optimized: Parallel, 3 workers
   - Time reduction: 40% (30m → 18m)
   
   ### Apply Optimizations?
   [Yes - Auto-optimize] [No - Keep as is] [Customize]
   ```

### Phase 10: Pipeline Activation
1. **Enable Pipeline**
   ```markdown
   ## 🚀 Pipeline Ready
   
   ### Pipeline Created Successfully
   - Name: feature-deployment
   - Location: .claude/pipelines/
   - Status: Active
   - Ready for use
   
   ### Quick Start Commands
   ```bash
   # Run pipeline
   /pipeline-run feature-deployment feature_branch=feature/auth
   
   # View pipeline
   /pipeline-info feature-deployment
   
   # Edit pipeline
   /pipeline-edit feature-deployment
   ```
   
   ### Next Steps
   1. Test with dry run
   2. Execute first real run
   3. Monitor performance
   4. Iterate and improve
   
   ### Integration Options
   - [ ] Add to CI/CD system
   - [ ] Create GitHub Action
   - [ ] Schedule automated runs
   - [ ] Add to team workflows
   ```

### Expected Deliverables
- [ ] Interactive pipeline creation wizard
- [ ] Complete YAML pipeline definition
- [ ] Visual flow representation
- [ ] Template integration and customization
- [ ] Validation and testing capabilities
- [ ] Pipeline storage and versioning
- [ ] Auto-generated documentation
- [ ] Export/import functionality
- [ ] Optimization suggestions
- [ ] Ready-to-use pipeline with commands

**Pipeline creation provides comprehensive wizard for building custom automation workflows with validation and optimization.**