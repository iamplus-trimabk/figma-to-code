---
description: "Debug issues with step-by-step analysis, root cause identification, and solutions"
allowed_tools: ["Bash", "Read", "Write", "Grep", "Edit", "TodoWrite"]
---

Debug issue: **$ARGUMENTS**

## 🐛 Intelligent Debugging Process

**Usage**: `/debug [error-description]` or `/debug [error-message]`
**Examples**: 
- `/debug login-timeout-error`
- `/debug "Cannot read property 'id' of undefined"`
- `/debug users-api-returning-500`
- `/debug memory-leak-in-production`

### Phase 1: Issue Analysis
1. **Parse Error Context**
   - Extract error message/description
   - Identify affected components
   - Determine error frequency/pattern
   - Check if production or development

2. **Initial Information Gathering**
   ```bash
   # Check recent commits
   git log --oneline -10
   
   # Check error logs
   grep -r "$ARGUMENTS" logs/
   
   # Check recent changes
   git diff HEAD~5
   ```

### Phase 2: Error Reproduction
1. **Reproduction Strategy**
   ```markdown
   ## 🔍 Reproduction Attempt
   
   ### Environment Setup
   - Node version: 18.17.0
   - Environment: development
   - Database: Connected
   - Services: All running
   
   ### Steps to Reproduce
   1. Start development server
   2. Navigate to /login
   3. Enter credentials
   4. Submit form
   5. Observe error
   
   ### Result
   ✅ Reproduced / ❌ Cannot reproduce
   ```

2. **Reproduction Variations**
   - Try different inputs
   - Test various environments
   - Check different browsers/clients
   - Vary network conditions

### Phase 3: Stack Trace Analysis
1. **Error Trace Parsing**
   ```markdown
   ## 📋 Stack Trace Analysis
   
   ### Error: Cannot read property 'id' of undefined
   
   **Location**: src/services/auth.js:45
   ```javascript
   // Line 45
   const userId = user.id; // 💥 Error here
   ```
   
   **Call Stack**:
   1. auth.js:45 - getUserId()
   2. middleware.js:23 - authenticate()
   3. router.js:67 - POST /api/login
   
   **Root Cause**: 
   - `user` object is undefined
   - Likely from failed database query
   - Or missing error handling
   ```

2. **Code Path Tracing**
   - Follow execution flow
   - Identify failure point
   - Map data transformations
   - Find where undefined originates

### Phase 4: Root Cause Analysis
1. **5-Why Analysis**
   ```markdown
   ## 🎯 Root Cause Analysis
   
   ### Problem: Login fails with undefined error
   
   **Why 1**: user.id is undefined
   → Because user object is undefined
   
   **Why 2**: user object is undefined
   → Because database query returned null
   
   **Why 3**: database query returned null
   → Because email parameter was empty
   
   **Why 4**: email parameter was empty
   → Because frontend validation was bypassed
   
   **Why 5**: frontend validation was bypassed
   → Because API lacks server-side validation
   
   **Root Cause**: Missing server-side input validation
   ```

2. **Contributing Factors**
   - Recent code changes
   - Configuration issues
   - Environmental factors
   - Dependency updates

### Phase 5: Diagnostic Steps
1. **Add Debug Logging**
   ```javascript
   // Temporary debug code
   console.log('Debug: Email received:', email);
   console.log('Debug: User query result:', user);
   console.log('Debug: User object:', JSON.stringify(user));
   
   // Better: Use debug module
   const debug = require('debug')('app:auth');
   debug('Login attempt for email: %s', email);
   debug('User found: %O', user);
   ```

2. **Breakpoint Strategy**
   ```markdown
   ## 🔴 Breakpoint Placement
   
   ### Key Debug Points
   1. **Entry Point**: Route handler start
   2. **Data Validation**: After input parsing
   3. **Database Query**: Before and after
   4. **Data Transform**: Each modification
   5. **Error Handler**: Catch blocks
   
   ### Watch Variables
   - email
   - user
   - query parameters
   - database connection
   ```

### Phase 6: Solution Development
1. **Fix Implementation**
   ```markdown
   ## 💡 Solution Options
   
   ### Option 1: Add Validation (Recommended)
   ```javascript
   // Add input validation
   if (!email || !email.trim()) {
     return res.status(400).json({
       error: 'Email is required'
     });
   }
   ```
   
   ### Option 2: Add Null Check
   ```javascript
   // Safe property access
   const userId = user?.id;
   if (!userId) {
     return res.status(404).json({
       error: 'User not found'
     });
   }
   ```
   
   ### Option 3: Improve Error Handling
   ```javascript
   try {
     const user = await User.findByEmail(email);
     if (!user) throw new NotFoundError('User not found');
     const userId = user.id;
   } catch (error) {
     logger.error('Login failed:', error);
     return res.status(error.status || 500).json({
       error: error.message
     });
   }
   ```
   ```

2. **Testing the Fix**
   - Apply fix locally
   - Test error scenario
   - Test normal flow
   - Test edge cases

### Phase 7: Performance Debugging
1. **Performance Analysis**
   ```markdown
   ## ⚡ Performance Debugging
   
   ### Symptom: Slow API response (>3s)
   
   ### Profiling Results
   1. **Database Query**: 2.5s 🔴
      - Issue: Missing index on email field
      - Fix: Add index to users.email
   
   2. **JSON Parsing**: 0.3s 🟡
      - Issue: Large payload
      - Fix: Paginate results
   
   3. **Authentication**: 0.1s ✅
      - No issues
   
   ### Optimization Plan
   ```sql
   -- Add missing index
   CREATE INDEX idx_users_email ON users(email);
   ```
   ```

2. **Memory Leak Detection**
   ```markdown
   ## 💾 Memory Leak Analysis
   
   ### Heap Snapshots
   - Initial: 50MB
   - After 1 hour: 250MB
   - Growth rate: 200MB/hour
   
   ### Leak Source
   - Event listeners not removed
   - Closures retaining references
   - Cache growing unbounded
   
   ### Fix
   ```javascript
   // Remove listeners
   componentWillUnmount() {
     this.subscription.unsubscribe();
     window.removeEventListener('resize', this.handler);
   }
   ```
   ```

### Phase 8: Advanced Debugging
1. **Race Condition Detection**
   ```markdown
   ## 🏁 Race Condition Debugging
   
   ### Symptom: Intermittent failures
   
   ### Analysis
   - Two async operations competing
   - State updates in wrong order
   - Missing await statements
   
   ### Fix
   ```javascript
   // Before: Race condition
   updateUser(data);
   sendEmail(user.email);
   
   // After: Sequential
   await updateUser(data);
   await sendEmail(user.email);
   ```
   ```

2. **Deadlock Resolution**
   - Identify locked resources
   - Analyze wait chains
   - Implement timeout strategies
   - Add retry logic

### Phase 9: Debug Documentation
1. **Debug Report**
   ```markdown
   ## 📝 Debug Session Report
   
   ### Issue
   - **Description**: Login fails with undefined error
   - **Severity**: High
   - **Affected Users**: All
   - **First Occurred**: 2025-08-15 10:30
   
   ### Investigation
   - **Time Spent**: 45 minutes
   - **Root Cause**: Missing input validation
   - **Contributing**: Recent refactor removed validation
   
   ### Solution Applied
   - Added server-side validation
   - Improved error handling
   - Added logging for monitoring
   
   ### Prevention
   - Add integration tests for validation
   - Code review checklist update
   - Input validation middleware
   
   ### Verification
   - ✅ Error no longer occurs
   - ✅ Tests added and passing
   - ✅ Deployed to staging
   ```

2. **Knowledge Base Entry**
   - Document error pattern
   - Record solution
   - Add to troubleshooting guide
   - Update runbook

### Phase 10: Monitoring Setup
1. **Error Tracking**
   ```javascript
   // Add error tracking
   app.use((err, req, res, next) => {
     // Log to monitoring service
     logger.error({
       error: err.message,
       stack: err.stack,
       url: req.url,
       method: req.method,
       user: req.user?.id
     });
     
     // Alert if critical
     if (err.severity === 'critical') {
       alerting.send('Critical error in production');
     }
   });
   ```

2. **Debug Instrumentation**
   - Add performance metrics
   - Set up error alerting
   - Create debug dashboards
   - Configure log aggregation

### Expected Deliverables
- [ ] Issue reproduced and understood
- [ ] Stack trace analyzed with root cause
- [ ] Multiple solution options provided
- [ ] Fix implemented and tested
- [ ] Performance issues identified if any
- [ ] Debug documentation created
- [ ] Monitoring/alerting configured
- [ ] Knowledge base updated for future reference

**Debugging provides systematic issue resolution with root cause analysis and preventive measures.**