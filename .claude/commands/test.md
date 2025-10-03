---
description: "Run tests with intelligent failure analysis and fix suggestions"
allowed_tools: ["Bash", "Read", "Write", "Grep", "Edit"]
---

Run tests with intelligent analysis: **$ARGUMENTS**

## 🧪 Intelligent Test Execution

**Usage**: `/test [options]` or `/test [specific-test-file]`
**Examples**: 
- `/test` - Run all tests
- `/test --watch` - Run tests in watch mode
- `/test auth.test.js` - Run specific test file
- `/test --coverage` - Run with coverage report
- `/test --failed` - Re-run only failed tests

### Phase 1: Test Environment Setup
1. **Environment Detection**
   - Read project.json for test frameworks
   - Detect test configuration files
   - Identify test directories
   - Check for test databases

2. **Pre-test Validation**
   ```bash
   # Install dependencies if needed
   npm ci
   
   # Build if required
   npm run build
   
   # Set up test environment
   export NODE_ENV=test
   ```

### Phase 2: Test Execution Strategy
1. **Smart Test Selection**
   ```bash
   # Detect changed files
   git diff --name-only
   
   # Run affected tests first
   npm test -- --findRelatedTests [changed-files]
   
   # Then run full suite
   npm test
   ```

2. **Test Categorization**
   - **Unit Tests**: Fast, isolated component tests
   - **Integration Tests**: API and service tests
   - **E2E Tests**: Full workflow tests
   - **Performance Tests**: Load and speed tests

### Phase 3: Test Execution
1. **Progressive Test Running**
   ```bash
   # 1. Run unit tests first (fast feedback)
   npm run test:unit
   
   # 2. Run integration tests
   npm run test:integration
   
   # 3. Run E2E tests if all pass
   npm run test:e2e
   ```

2. **Watch Mode Support**
   ```bash
   # Interactive watch mode
   npm test -- --watch
   
   # With coverage
   npm test -- --watch --coverage
   ```

### Phase 4: Failure Analysis
1. **Intelligent Failure Detection**
   ```markdown
   ## ❌ Test Failure Analysis
   
   ### Failed Test: auth.test.js
   **Test**: "should reject invalid JWT tokens"
   **Error**: Expected 401, received 200
   
   **Root Cause Analysis**:
   - JWT validation middleware not applied
   - Missing authentication check in route
   - Likely regression from commit abc123
   
   **Suggested Fix**:
   ```javascript
   // Add to routes/api.js line 45
   router.use('/protected', authMiddleware);
   ```
   
   **Related Tests at Risk**:
   - "should protect user endpoints"
   - "should validate token expiry"
   ```

2. **Pattern Recognition**
   - Identify common failure patterns
   - Group related failures
   - Detect flaky tests
   - Find root cause connections

### Phase 5: Fix Suggestions
1. **Automated Fix Generation**
   ```markdown
   ## 🔧 Suggested Fixes
   
   ### Test: "User login with email"
   **Failure**: Cannot read property 'email' of undefined
   
   **Fix Option 1**: Add null check
   ```javascript
   // Line 45 in auth.service.js
   if (!user || !user.email) {
     throw new Error('User email required');
   }
   ```
   
   **Fix Option 2**: Add default value
   ```javascript
   const email = user?.email || '';
   ```
   
   **Fix Option 3**: Update test setup
   ```javascript
   // In test file
   const mockUser = {
     email: 'test@example.com',
     password: 'hashedPassword'
   };
   ```
   ```

2. **Code Fix Application**
   - Offer to apply simple fixes
   - Create fix branches
   - Run tests after fixes
   - Validate fixes work

### Phase 6: Coverage Analysis
1. **Coverage Report**
   ```markdown
   ## 📊 Test Coverage Report
   
   ### Overall Coverage: 82.5%
   - Statements: 85.2% (1250/1467)
   - Branches: 78.3% (180/230)
   - Functions: 88.1% (250/284)
   - Lines: 82.5% (1200/1454)
   
   ### Uncovered Areas
   
   #### Critical Gaps 🔴
   - auth/jwt.js: Lines 45-52 (error handling)
   - payment/process.js: Lines 120-135 (retry logic)
   
   #### Should Cover 🟡
   - user/profile.js: Lines 78-85 (edge cases)
   - api/validation.js: Lines 23-30 (error paths)
   
   #### Nice to Have 🟢
   - utils/format.js: Lines 12-15 (formatting)
   ```

2. **Coverage Improvement Suggestions**
   ```markdown
   ## 📈 Coverage Improvement Plan
   
   ### Quick Wins (+5% coverage)
   1. Add error handling tests for auth module
   2. Test edge cases in user validation
   3. Add negative test cases for API
   
   ### Generated Test Examples
   ```javascript
   // Suggested test for uncovered auth error
   test('should handle JWT decode errors', () => {
     const invalidToken = 'malformed.jwt.token';
     expect(() => decodeJWT(invalidToken))
       .toThrow('Invalid token format');
   });
   ```
   ```

### Phase 7: Performance Analysis
1. **Test Performance Metrics**
   ```markdown
   ## ⏱️ Test Performance Analysis
   
   ### Slow Tests (>1s)
   1. **database.integration.test.js** - 3.2s
      - Issue: No connection pooling
      - Fix: Use shared test database connection
   
   2. **email.service.test.js** - 2.1s
      - Issue: Real SMTP calls
      - Fix: Mock email service
   
   ### Test Suite Timing
   - Unit Tests: 8.5s (245 tests)
   - Integration: 45.2s (42 tests)
   - E2E: 2m 15s (18 tests)
   - Total: 3m 8.7s
   
   ### Optimization Suggestions
   - Parallelize integration tests: -20s
   - Use test database snapshots: -15s
   - Mock external services: -10s
   ```

2. **Performance Improvements**
   - Identify slow tests
   - Suggest parallelization
   - Recommend mocking strategies
   - Optimize test data setup

### Phase 8: Flaky Test Detection
1. **Flaky Test Analysis**
   ```markdown
   ## 🎲 Flaky Test Detection
   
   ### Intermittent Failures (3 runs)
   
   1. **"should handle concurrent requests"**
      - Passed: 2/3 times
      - Issue: Race condition in test
      - Fix: Add proper async/await
   
   2. **"should timeout after 5 seconds"**
      - Passed: 1/3 times
      - Issue: Hardcoded timeout too tight
      - Fix: Increase timeout or mock timer
   ```

2. **Stabilization Recommendations**
   - Add retry logic for network tests
   - Use fixed timestamps
   - Mock external dependencies
   - Isolate test data

### Phase 9: Continuous Testing
1. **Watch Mode Enhancements**
   ```markdown
   ## 👀 Watch Mode Active
   
   ### Watching Files
   - src/**/*.js
   - tests/**/*.test.js
   
   ### Current Focus
   - Testing: auth.service.js
   - Related: auth.test.js, jwt.test.js
   
   ### Commands
   - Press 'a' to run all tests
   - Press 'f' to run failed tests
   - Press 'c' to clear console
   - Press 'q' to quit
   ```

2. **Test Feedback Loop**
   - Run tests on file save
   - Show inline test results
   - Highlight coverage changes
   - Track test history

### Phase 10: Report Generation
1. **Test Summary Report**
   ```markdown
   ## ✅ Test Execution Complete
   
   ### Results
   - **Total**: 305 tests
   - **Passed**: 298 ✅
   - **Failed**: 5 ❌
   - **Skipped**: 2 ⏭️
   - **Duration**: 45.3s
   
   ### Failed Tests
   1. auth › JWT validation › should reject expired tokens
   2. user › profile › should update email
   3. api › endpoints › should rate limit requests
   4. payment › stripe › should handle webhook
   5. email › templates › should render welcome email
   
   ### Next Steps
   1. Fix failing tests (5 issues)
   2. Improve coverage (target: 85%)
   3. Optimize slow tests (3 tests >1s)
   4. Stabilize flaky tests (2 identified)
   
   ### CI/CD Status
   - Would PASS/FAIL in CI
   - Blocking issues: 5
   - Warning issues: 3
   ```

### Expected Deliverables
- [ ] Smart test execution with affected tests first
- [ ] Comprehensive failure analysis with root causes
- [ ] Automated fix suggestions with code examples
- [ ] Coverage analysis with improvement plan
- [ ] Performance metrics and optimization suggestions
- [ ] Flaky test detection and stabilization
- [ ] Continuous testing with watch mode
- [ ] Detailed test report with actionable next steps

**Test execution provides intelligent analysis, automated fixes, and continuous feedback for rapid development.**