---
description: "Checkout PR locally, run comprehensive tests, and generate test report"
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

Test pull request locally: **$ARGUMENTS**

## 🧪 Pull Request Testing Process

**Usage**: `/git-test-pr [PR-number]` or `/git-test-pr [PR-URL]`
**Examples**: 
- `/git-test-pr 123`
- `/git-test-pr https://github.com/org/repo/pull/123`

### Phase 1: PR Setup
1. **Fetch PR Code**
   ```bash
   # Get PR information
   gh pr view $ARGUMENTS --json number,headRefName,baseRefName
   
   # Checkout PR locally
   gh pr checkout $ARGUMENTS
   
   # Or manually:
   git fetch origin pull/[PR]/head:test-pr-[PR]
   git checkout test-pr-[PR]
   ```

2. **Environment Preparation**
   - Stash any local changes
   - Install/update dependencies
   - Set up test databases
   - Configure test environment variables

### Phase 2: Dependency & Build Verification
1. **Dependency Installation**
   ```bash
   # Based on project.json tech stack
   npm ci           # Node.js projects
   pip install -r requirements.txt  # Python
   bundle install   # Ruby
   go mod download  # Go
   ```

2. **Build Verification**
   - Compile TypeScript/build assets
   - Verify build succeeds
   - Check for build warnings
   - Validate bundle size

### Phase 3: Test Suite Execution
1. **Unit Tests**
   ```bash
   # Run unit tests with coverage
   npm test -- --coverage
   # or
   jest --coverage --verbose
   vitest run --coverage
   ```
   - Track test count and duration
   - Monitor coverage percentage
   - Identify failing tests
   - Check coverage thresholds

2. **Integration Tests**
   ```bash
   # Run integration tests
   npm run test:integration
   ```
   - Test API endpoints
   - Database operations
   - Service integrations
   - External API mocking

3. **End-to-End Tests**
   ```bash
   # Based on project.json frameworks
   npm run test:e2e     # Playwright/Cypress
   playwright test      # Playwright
   cypress run          # Cypress
   ```
   - UI workflow testing
   - Critical path validation
   - Cross-browser testing
   - Performance metrics

### Phase 4: Specialized Testing
1. **Performance Testing**
   - Load time analysis
   - Memory usage profiling
   - API response times
   - Database query performance
   - Frontend rendering metrics

2. **Security Testing**
   ```bash
   # Security audit
   npm audit
   
   # Dependency scanning
   npm audit --production
   
   # OWASP dependency check
   dependency-check --scan .
   ```

3. **Accessibility Testing**
   - WCAG compliance
   - Screen reader compatibility
   - Keyboard navigation
   - Color contrast validation

### Phase 5: Regression Testing
1. **Baseline Comparison**
   - Compare with main branch tests
   - Identify new failures
   - Check performance regression
   - Validate backwards compatibility

2. **Critical Path Validation**
   - User authentication flow
   - Core business operations
   - Payment processing
   - Data integrity checks

### Phase 6: Test Failure Analysis
1. **Failure Investigation**
   - Categorize failures: new, flaky, environmental
   - Analyze error messages and stack traces
   - Check test logs and screenshots
   - Identify root causes

2. **Flaky Test Detection**
   - Re-run failed tests 3 times
   - Identify intermittent failures
   - Check timing dependencies
   - Environmental factors

### Phase 7: Code Quality Checks
1. **Linting & Formatting**
   ```bash
   npm run lint
   npm run format:check
   ```
   - Code style violations
   - Best practice violations
   - Security issues
   - Complexity warnings

2. **Type Checking**
   ```bash
   npm run typecheck
   tsc --noEmit
   ```
   - Type errors
   - Missing types
   - Type coverage

### Phase 8: Test Report Generation
1. **Comprehensive Test Report**
   ```markdown
   ## 🧪 PR Test Report: #123
   
   ### Test Summary
   - **PR**: #123 - [Title]
   - **Branch**: feature/auth → main
   - **Test Date**: 2025-08-15 14:30 UTC
   - **Duration**: 5m 23s
   
   ### Overall Status: ✅ PASS / ❌ FAIL / ⚠️ PARTIAL
   
   ### Test Results
   
   #### Unit Tests: ✅ PASSED
   - **Tests**: 245 passed, 0 failed
   - **Coverage**: 87% (threshold: 80%)
   - **Duration**: 45s
   
   #### Integration Tests: ✅ PASSED
   - **Tests**: 42 passed, 0 failed
   - **Duration**: 1m 20s
   
   #### E2E Tests: ❌ FAILED
   - **Tests**: 18 passed, 2 failed
   - **Failed**: 
     - Login flow with 2FA
     - Password reset email
   - **Duration**: 3m 15s
   
   ### Code Quality
   - **Linting**: ✅ No issues
   - **Type Check**: ⚠️ 2 warnings
   - **Security Audit**: ✅ No vulnerabilities
   
   ### Performance Metrics
   - **Build Time**: 35s (baseline: 32s) ⚠️ +3s
   - **Bundle Size**: 2.1MB (baseline: 2.0MB) ⚠️ +100KB
   - **Test Speed**: Normal
   
   ### Failed Test Details
   1. **Login with 2FA**
      - File: tests/e2e/auth.spec.ts:45
      - Error: Timeout waiting for 2FA input
      - Likely Cause: UI change in 2FA modal
   
   2. **Password Reset Email**
      - File: tests/integration/email.test.js:78
      - Error: Email template not found
      - Likely Cause: Missing email template file
   
   ### Recommendations
   1. 🔴 Fix failing E2E tests before merge
   2. 🟡 Investigate bundle size increase
   3. 🟡 Address TypeScript warnings
   4. 🟢 Consider adding tests for new features
   
   ### Environment
   - Node: v18.17.0
   - npm: 9.6.7
   - OS: macOS 14.0
   ```

2. **CI/CD Integration**
   - Format report for CI systems
   - Update PR status checks
   - Post results to PR comments
   - Trigger notifications

### Phase 9: Test Artifacts
1. **Artifact Collection**
   - Test coverage reports
   - Failed test screenshots
   - Performance profiles
   - Error logs and traces

2. **Artifact Storage**
   ```bash
   # Create test artifacts directory
   mkdir -p .test-artifacts/pr-$PR_NUMBER/
   
   # Copy artifacts
   cp -r coverage/ .test-artifacts/pr-$PR_NUMBER/
   cp -r test-results/ .test-artifacts/pr-$PR_NUMBER/
   ```

### Phase 10: Cleanup & Restoration
1. **Environment Cleanup**
   - Stop test servers
   - Clean test databases
   - Remove test files
   - Clear test caches

2. **Git Restoration**
   ```bash
   # Return to original branch
   git checkout -
   
   # Clean up test branch (optional)
   git branch -D test-pr-[PR]
   
   # Restore stashed changes
   git stash pop
   ```

### Expected Deliverables
- [ ] PR code checked out and environment prepared
- [ ] Complete test suite execution (unit, integration, E2E)
- [ ] Performance and security testing completed
- [ ] Code quality checks performed
- [ ] Comprehensive test report with failure analysis
- [ ] Test artifacts collected and stored
- [ ] PR status updated with test results
- [ ] Environment cleaned up and restored

**Test execution adapts to project technology stack and provides detailed, actionable results for PR validation.**