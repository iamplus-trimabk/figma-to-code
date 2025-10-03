---
description: "Create hotfix branch with automated testing, deployment prep, and rollback plan"
allowed_tools: ["Bash", "Write", "Read", "Grep", "TodoWrite"]
---

Create and manage hotfix: **$ARGUMENTS**

## 🚨 Hotfix Process

**Usage**: `/git-hotfix [issue-description]`
**Examples**: 
- `/git-hotfix critical-auth-vulnerability`
- `/git-hotfix payment-processing-error`
- `/git-hotfix data-corruption-bug`

### Phase 1: Hotfix Initialization
1. **Issue Analysis**
   - Parse issue description
   - Determine severity level (P0/P1/P2)
   - Identify affected components
   - Assess production impact

2. **Environment Assessment**
   ```bash
   # Check current production version
   git describe --tags --abbrev=0
   
   # Verify clean working state
   git status
   
   # Fetch latest from remote
   git fetch origin
   ```

### Phase 2: Hotfix Branch Creation
1. **Branch Setup**
   ```bash
   # Create hotfix from production/main
   git checkout -b hotfix/[issue-name] origin/main
   
   # Or from last release tag
   git checkout -b hotfix/[issue-name] [last-release-tag]
   ```

2. **Hotfix Metadata**
   ```json
   {
     "hotfix_id": "HOTFIX-001",
     "severity": "P0",
     "issue": "Authentication bypass vulnerability",
     "affected_versions": ["v2.0.0", "v2.0.1"],
     "created": "2025-08-15T14:30:00Z",
     "owner": "[current-profile]"
   }
   ```

### Phase 3: Rapid Development Setup
1. **Fast Feedback Loop**
   - Set up watch mode for tests
   - Configure hot reload
   - Enable debug logging
   - Set up monitoring dashboard

2. **Focused Testing**
   ```bash
   # Run only affected tests
   npm test -- --watch [affected-modules]
   
   # Set up continuous testing
   npm run test:watch
   ```

### Phase 4: Implementation Tracking
1. **Hotfix Checklist**
   ```markdown
   ## 🚨 Hotfix Checklist: [Issue]
   
   ### Immediate Actions
   - [ ] Reproduce issue locally
   - [ ] Identify root cause
   - [ ] Implement minimal fix
   - [ ] Add regression test
   - [ ] Verify fix works
   
   ### Validation
   - [ ] Unit tests pass
   - [ ] Integration tests pass
   - [ ] Security scan clean
   - [ ] Performance impact assessed
   - [ ] No new issues introduced
   
   ### Deployment Prep
   - [ ] Update changelog
   - [ ] Document configuration changes
   - [ ] Prepare rollback procedure
   - [ ] Alert operations team
   - [ ] Schedule deployment window
   ```

2. **Real-time Status Updates**
   - Update issue tracker
   - Notify stakeholders
   - Log progress milestones
   - Track time to resolution

### Phase 5: Fix Implementation
1. **Minimal Change Principle**
   - Make smallest possible fix
   - Avoid refactoring
   - Focus on issue resolution
   - Defer improvements

2. **Code Documentation**
   ```javascript
   // HOTFIX: HOTFIX-001 - Critical auth vulnerability
   // Issue: JWT validation bypass allowed unauthorized access
   // Fix: Added proper signature verification
   // Impact: All authenticated endpoints now properly secured
   // Rollback: Revert this commit and deploy previous version
   ```

### Phase 6: Comprehensive Testing
1. **Regression Testing**
   ```bash
   # Run full test suite
   npm test
   
   # Run security tests
   npm run test:security
   
   # Run performance tests
   npm run test:performance
   ```

2. **Production Simulation**
   - Test with production data copy
   - Simulate production load
   - Test edge cases
   - Verify monitoring/alerts work

### Phase 7: Rollback Planning
1. **Rollback Procedure**
   ```markdown
   ## 🔄 Rollback Plan
   
   ### Triggers
   - Error rate > 5% after deployment
   - Critical functionality broken
   - Performance degradation > 20%
   
   ### Steps
   1. Immediately revert deployment
      ```bash
      kubectl rollout undo deployment/api
      ```
   2. Restore previous version
      ```bash
      git revert [hotfix-commit]
      git push origin main
      ```
   3. Clear caches
   4. Notify team
   5. Post-mortem meeting
   
   ### Validation
   - Verify services healthy
   - Check error rates normal
   - Confirm functionality restored
   ```

2. **Backup Creation**
   - Database backup before deployment
   - Configuration backup
   - Current version artifacts
   - State snapshots

### Phase 8: Deployment Preparation
1. **Release Package**
   ```markdown
   ## 📦 Hotfix Release: v2.0.2-hotfix
   
   ### Changes
   - Fixed critical authentication vulnerability
   - Patched JWT validation bypass
   - Added security regression tests
   
   ### Deployment Requirements
   - **Downtime**: None expected
   - **Config Changes**: JWT_STRICT_MODE=true
   - **Database**: No changes
   - **Dependencies**: No changes
   
   ### Deployment Steps
   1. Enable maintenance mode (optional)
   2. Deploy to staging
   3. Run smoke tests
   4. Deploy to production (rolling)
   5. Monitor for 30 minutes
   6. Disable maintenance mode
   ```

2. **Communication Plan**
   - Stakeholder notification
   - Customer communication (if needed)
   - Internal team alerts
   - Status page updates

### Phase 9: Merge Strategy
1. **Multi-Branch Integration**
   ```bash
   # Merge to main/production
   git checkout main
   git merge --no-ff hotfix/[issue-name]
   
   # Merge to develop
   git checkout develop
   git merge --no-ff hotfix/[issue-name]
   
   # Tag release
   git tag -a v2.0.2-hotfix -m "Hotfix: [issue]"
   git push origin --tags
   ```

2. **PR Creation**
   ```bash
   # Create PR for review (even if expedited)
   gh pr create \
     --title "🚨 HOTFIX: [issue]" \
     --body "Hotfix documentation" \
     --label "hotfix,priority:critical" \
     --reviewer "[senior-reviewer]"
   ```

### Phase 10: Post-Deployment
1. **Monitoring**
   ```markdown
   ## 📊 Post-Deployment Monitoring
   
   ### Key Metrics (30 min window)
   - Error rate: Monitor for spikes
   - Response time: Check for degradation
   - CPU/Memory: Watch for leaks
   - User reports: Track support tickets
   
   ### Alert Thresholds
   - Error rate > 1% → Investigate
   - Response time > 2x baseline → Alert
   - Memory usage increasing → Monitor
   - User complaints > 5 → Escalate
   ```

2. **Validation & Verification**
   - Run production smoke tests
   - Verify fix is working
   - Check for side effects
   - Confirm metrics normal

### Phase 11: Documentation & Learning
1. **Post-Mortem**
   ```markdown
   ## 📝 Hotfix Post-Mortem
   
   ### Timeline
   - Issue detected: [time]
   - Hotfix started: [time]
   - Fix deployed: [time]
   - Issue resolved: [time]
   - Total duration: [duration]
   
   ### Root Cause
   [Detailed explanation]
   
   ### Fix Applied
   [What was changed]
   
   ### Lessons Learned
   - What went well
   - What could improve
   - Action items
   
   ### Prevention
   - Add automated tests
   - Improve code review
   - Update monitoring
   ```

2. **Knowledge Base Update**
   - Document issue and fix
   - Update runbooks
   - Improve monitoring
   - Share learnings

### Expected Deliverables
- [ ] Hotfix branch created and tracked
- [ ] Minimal fix implemented with tests
- [ ] Comprehensive testing completed
- [ ] Rollback plan documented and ready
- [ ] Deployment package prepared
- [ ] Multi-branch integration completed
- [ ] Production deployment successful
- [ ] Post-deployment monitoring active
- [ ] Post-mortem and learnings captured

**Hotfix process ensures rapid, safe resolution of critical issues with proper testing, deployment, and rollback procedures.**