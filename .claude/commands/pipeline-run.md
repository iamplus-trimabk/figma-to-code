---
description: "Execute saved pipeline with monitoring, logging, and error recovery"
allowed_tools: ["Bash", "Read", "Write", "Grep", "TodoWrite"]
---

Run pipeline: **$ARGUMENTS**

## ▶️ Pipeline Execution Manager

**Usage**: `/pipeline-run [pipeline-name] [parameters]`
**Examples**: 
- `/pipeline-run feature-deployment feature_branch=feature/auth`
- `/pipeline-run data-migration source=prod target=staging`
- `/pipeline-run security-audit --deep-scan`
- `/pipeline-run ml-training dataset=training-v2`

### Phase 1: Pipeline Loading
1. **Pipeline Discovery**
   ```markdown
   ## 🔍 Loading Pipeline: $ARGUMENTS
   
   ### Pipeline Search
   - Checking: .claude/pipelines/feature-deployment.yml ✅
   - Found: feature-deployment v1.0.0
   - Author: [current-profile]
   - Last modified: 2 hours ago
   
   ### Pipeline Details
   - Steps: 5 sequential
   - Estimated duration: 25-35 minutes
   - Required parameters: feature_branch
   - Optional parameters: environment, skip_tests
   ```

2. **Parameter Validation**
   ```markdown
   ## ⚙️ Parameter Validation
   
   ### Provided Parameters
   - feature_branch: feature/auth ✅
   - environment: staging (default) ✅
   - skip_tests: false (default) ✅
   
   ### Environment Variables
   - NODE_ENV: staging ✅
   - DEPLOY_KEY: ****** (from secrets) ✅
   - SLACK_WEBHOOK: ****** (from secrets) ✅
   
   ### Validation Status: ✅ READY
   All required parameters provided and valid
   ```

### Phase 2: Pre-Execution Setup
1. **Environment Preparation**
   ```markdown
   ## 🛠️ Execution Environment
   
   ### System Check
   - CPU Available: 4 cores ✅
   - Memory Available: 8GB ✅
   - Disk Space: 25GB free ✅
   - Network: Connected ✅
   
   ### Dependencies Check
   - Node.js: v18.17.0 ✅
   - Git: 2.40.0 ✅
   - Docker: 24.0.2 ✅
   - Required tools: All available ✅
   
   ### Workspace Setup
   - Pipeline ID: run-20250815-145500
   - Workspace: ./pipelines/runs/run-20250815-145500/
   - Log file: pipeline.log
   - Artifacts dir: ./artifacts/
   ```

2. **State Initialization**
   ```json
   {
     "pipeline_id": "run-20250815-145500",
     "pipeline_name": "feature-deployment",
     "started_at": "2025-08-15T14:55:00Z",
     "status": "initializing",
     "parameters": {
       "feature_branch": "feature/auth",
       "environment": "staging",
       "skip_tests": false
     },
     "current_step": null,
     "steps_completed": [],
     "artifacts": [],
     "metrics": {
       "start_time": 1234567890,
       "cpu_usage": [],
       "memory_usage": []
     }
   }
   ```

### Phase 3: Execution Monitor
1. **Real-Time Dashboard**
   ```markdown
   ## 📊 Pipeline Execution Dashboard
   
   ╔══════════════════════════════════════════════════╗
   ║ Pipeline: feature-deployment                     ║
   ║ Run ID: run-20250815-145500                     ║
   ╠══════════════════════════════════════════════════╣
   ║                                                  ║
   ║ Progress: ████████████░░░░░░░░░ 60%             ║
   ║                                                  ║
   ║ Steps:                                           ║
   ║ ✅ validate      [2m 15s]  Code review passed   ║
   ║ ✅ test         [15m 30s]  245/245 tests pass  ║
   ║ 🔄 build         [3m 45s]  Building assets...   ║
   ║ ⏸️ deploy                   Waiting...          ║
   ║ ⏸️ verify                   Waiting...          ║
   ║                                                  ║
   ║ Time Elapsed: 21m 30s                           ║
   ║ Est. Remaining: 8m 30s                          ║
   ║                                                  ║
   ║ Resources:                                       ║
   ║ CPU: ████░░░░░░ 42%  Memory: ███░░░░░░░ 31%   ║
   ║                                                  ║
   ║ Logs: tail -f pipeline.log                      ║
   ╚══════════════════════════════════════════════════╝
   ```

2. **Step Execution Tracking**
   ```markdown
   ## 🎯 Current Step: build
   
   ### Execution Details
   - Command: npm run build:staging
   - Started: 14:58:45
   - Duration: 3m 45s (ongoing)
   - Status: In Progress
   
   ### Live Output
   ```
   > feature-app@1.0.0 build:staging
   > webpack --mode production --env staging
   
   webpack 5.89.0 compiled successfully
   ✓ Client build complete (2.1 MB)
   ✓ Server build complete (450 KB)
   ⠋ Optimizing assets...
   ```
   
   ### Metrics
   - CPU Usage: 85%
   - Memory: 1.2GB
   - Disk I/O: 45 MB/s
   ```

### Phase 4: Error Handling
1. **Failure Detection**
   ```markdown
   ## ❌ Step Failed: test
   
   ### Error Details
   - Step: test
   - Command: /test --all
   - Exit Code: 1
   - Duration: 15m 30s
   
   ### Failure Reason
   ```
   FAIL src/auth/login.test.js
     ● Login Component › should handle 2FA
   
     Expected: 200
     Received: 401
   
     45 |   const response = await login(credentials);
   > 46 |   expect(response.status).toBe(200);
        |                           ^
   ```
   
   ### Recovery Options
   1. **Retry Step** - Run failed step again
   2. **Skip Step** - Continue without this step
   3. **Fix & Retry** - Open debugger, fix, retry
   4. **Abort Pipeline** - Stop execution
   5. **Rollback** - Undo changes and stop
   
   Selecting: Fix & Retry...
   ```

2. **Auto-Recovery**
   ```markdown
   ## 🔧 Auto-Recovery Attempting
   
   ### Analyzing Failure
   - Type: Test failure
   - Component: Authentication
   - Likely cause: Missing mock data
   
   ### Applying Fix
   ```javascript
   // Adding missing mock
   jest.mock('./api', () => ({
     login: jest.fn().mockResolvedValue({
       status: 200,
       data: { token: 'mock-token' }
     })
   }));
   ```
   
   ### Retrying Step
   - Running: /test --all
   - Status: Tests passing... ✅
   - Recovery: Successful
   - Continuing pipeline...
   ```

### Phase 5: Artifact Management
1. **Artifact Collection**
   ```markdown
   ## 📦 Pipeline Artifacts
   
   ### Generated Artifacts
   
   #### Build Artifacts
   - dist/client.bundle.js (2.1 MB)
   - dist/server.bundle.js (450 KB)
   - dist/assets/ (15 files, 3.2 MB)
   
   #### Test Reports
   - coverage/lcov-report/index.html
   - test-results.xml
   - performance-report.json
   
   #### Deployment Artifacts
   - deployment-manifest.yml
   - rollback-script.sh
   - health-check-results.json
   
   ### Artifact Storage
   - Location: ./artifacts/run-20250815-145500/
   - Total Size: 25.3 MB
   - Retention: 30 days
   ```

2. **Artifact Publishing**
   ```markdown
   ## 📤 Publishing Artifacts
   
   ### Upload Destinations
   - ✅ S3 Bucket: s3://artifacts/run-20250815-145500/
   - ✅ Docker Registry: registry.company.com/app:staging
   - ✅ NPM Registry: @company/app@1.0.0-staging.1
   
   ### Published URLs
   - Build: https://artifacts.company.com/builds/run-20250815-145500
   - Coverage: https://coverage.company.com/run-20250815-145500
   - Logs: https://logs.company.com/pipelines/run-20250815-145500
   ```

### Phase 6: Parallel Execution
1. **Parallel Step Management**
   ```markdown
   ## ⚡ Parallel Execution Active
   
   ### Running in Parallel (4 workers)
   
   ╔══════════════╦══════════════╦══════════════╦══════════════╗
   ║   Worker 1   ║   Worker 2   ║   Worker 3   ║   Worker 4   ║
   ╠══════════════╬══════════════╬══════════════╬══════════════╣
   ║ lint         ║ security     ║ performance  ║ a11y         ║
   ║ ████████ 85% ║ ██████ 60%   ║ ████████ 90% ║ ████ 40%     ║
   ║ 2m 15s       ║ 3m 30s       ║ 1m 45s       ║ 4m 10s       ║
   ╚══════════════╩══════════════╩══════════════╩══════════════╝
   
   ### Synchronization Point
   - All parallel steps must complete
   - Estimated completion: 4m 10s (slowest)
   - Then continue to: deployment phase
   ```

### Phase 7: Conditional Execution
1. **Condition Evaluation**
   ```markdown
   ## 🔀 Conditional Step Evaluation
   
   ### Evaluating: production_checks
   
   ### Conditions
   ```javascript
   current_branch == "main" && 
   environment == "production"
   ```
   
   ### Values
   - current_branch: "feature/auth"
   - environment: "staging"
   
   ### Result: FALSE ❌
   - Skipping: production_checks
   - Reason: Not a production deployment
   - Continue to: next step
   ```

2. **Dynamic Path Selection**
   ```markdown
   ## 🗺️ Dynamic Path Selection
   
   ### Branch Detection
   - Current: feature/auth
   - Type: Feature branch
   
   ### Selected Path: feature_workflow
   - Steps: light_review → feature_tests → staging_deploy
   - Skipping: full_review, production_tests, prod_deploy
   
   ### Adjusted Timeline
   - Original estimate: 35 minutes
   - New estimate: 22 minutes
   - Time saved: 13 minutes
   ```

### Phase 8: Monitoring & Metrics
1. **Performance Metrics**
   ```markdown
   ## 📈 Pipeline Performance Metrics
   
   ### Step Performance
   | Step | Duration | CPU Peak | Memory Peak | Status |
   |------|----------|----------|-------------|--------|
   | validate | 2m 15s | 25% | 512MB | ✅ |
   | test | 15m 30s | 95% | 2.1GB | ✅ |
   | build | 5m 20s | 88% | 1.8GB | ✅ |
   | deploy | 3m 10s | 15% | 256MB | 🔄 |
   
   ### Resource Usage Timeline
   ```
   CPU:  ▁▂▃▄█████▅▃▂▁▁▂▃████▇▅▃▂▁
   MEM:  ▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▃▄▅▆▇█▇▆▅▄
   I/O:  ▁▁▁▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▁▁▁▁▁▁▁
   ```
   
   ### Bottleneck Analysis
   - Slowest step: test (15m 30s)
   - Highest CPU: test phase (95%)
   - Highest Memory: build phase (2.1GB)
   - Optimization potential: Parallelize tests
   ```

2. **Quality Metrics**
   ```markdown
   ## 🎯 Quality Metrics
   
   ### Code Quality
   - Linting Issues: 0 errors, 3 warnings
   - Code Coverage: 87.5% (+2.3%)
   - Complexity: Average 3.2 (Good)
   - Duplication: 2.1% (Low)
   
   ### Security Metrics
   - Vulnerabilities: 0 critical, 1 medium
   - Dependencies: All up-to-date
   - OWASP Compliance: 98%
   
   ### Performance Metrics
   - Build Size: 2.1MB (-150KB)
   - Load Time: 1.2s (Target: <2s)
   - API Response: 145ms avg
   ```

### Phase 9: Notifications
1. **Progress Notifications**
   ```markdown
   ## 📢 Notification Sent
   
   ### Slack Notification
   ```
   🚀 Pipeline Update: feature-deployment
   
   Status: In Progress (60%)
   Branch: feature/auth
   Environment: staging
   
   ✅ validate - Complete (2m 15s)
   ✅ test - Complete (15m 30s)
   🔄 build - Running (3m 45s)
   ⏸️ deploy - Waiting
   ⏸️ verify - Waiting
   
   View Details: https://pipelines.company.com/run-20250815-145500
   ```
   
   ### Email Notification
   - Recipients: team@company.com
   - Subject: Pipeline 60% Complete
   - Status: Sent ✅
   ```

### Phase 10: Completion Report
1. **Final Report**
   ```markdown
   ## ✅ Pipeline Complete
   
   ### Execution Summary
   ╔════════════════════════════════════════════════╗
   ║ Pipeline: feature-deployment                   ║
   ║ Status: SUCCESS ✅                             ║
   ║ Duration: 28m 35s                              ║
   ╠════════════════════════════════════════════════╣
   ║ Parameters:                                    ║
   ║ - feature_branch: feature/auth                 ║
   ║ - environment: staging                         ║
   ║ - skip_tests: false                           ║
   ╠════════════════════════════════════════════════╣
   ║ Steps Summary:                                 ║
   ║ ✅ validate     2m 15s   Code review passed   ║
   ║ ✅ test        15m 30s   245/245 tests       ║
   ║ ✅ build        5m 20s   Assets built        ║
   ║ ✅ deploy       3m 10s   Deployed to staging ║
   ║ ✅ verify       2m 20s   Health checks pass  ║
   ╠════════════════════════════════════════════════╣
   ║ Artifacts:                                     ║
   ║ - Build: 2.1MB client, 450KB server           ║
   ║ - Coverage: 87.5%                              ║
   ║ - Deployment: staging.company.com             ║
   ╚════════════════════════════════════════════════╝
   
   ### Key Achievements
   - Zero failures (after 1 auto-recovery)
   - Performance improved by 15%
   - All quality gates passed
   - Successfully deployed to staging
   
   ### Next Actions
   1. Review staging deployment
   2. Run acceptance tests
   3. Prepare production deployment
   4. Schedule go-live meeting
   
   ### Resources
   - Full Logs: ./pipelines/runs/run-20250815-145500/
   - Artifacts: https://artifacts.company.com/run-20250815-145500
   - Deployment: https://staging.company.com
   - Rollback: /pipeline-run rollback run-20250815-145500
   ```

2. **Analytics Update**
   ```json
   {
     "pipeline": "feature-deployment",
     "run_id": "run-20250815-145500",
     "status": "success",
     "duration_seconds": 1715,
     "steps_total": 5,
     "steps_passed": 5,
     "steps_failed": 0,
     "steps_skipped": 0,
     "auto_recoveries": 1,
     "resource_usage": {
       "cpu_average": 45,
       "memory_peak_mb": 2150,
       "disk_usage_mb": 253
     },
     "quality_metrics": {
       "test_coverage": 87.5,
       "linting_score": 98,
       "security_score": 95
     },
     "artifacts_generated": 12,
     "notifications_sent": 3
   }
   ```

### Expected Deliverables
- [ ] Pipeline loaded and parameters validated
- [ ] Real-time execution dashboard with progress
- [ ] Step-by-step execution with live output
- [ ] Error detection and auto-recovery
- [ ] Artifact collection and publishing
- [ ] Parallel execution management
- [ ] Conditional step evaluation
- [ ] Comprehensive metrics and monitoring
- [ ] Progress notifications to team
- [ ] Complete execution report with analytics

**Pipeline execution provides comprehensive management, monitoring, and recovery for automated workflows with full visibility.**