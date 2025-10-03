---
description: "Smart cherry-pick with conflict resolution guidance and impact analysis"
allowed_tools: ["Bash", "Read", "Write", "Grep", "Edit"]
---

Smart cherry-pick commits: **$ARGUMENTS**

## 🍒 Cherry-Pick Process

**Usage**: `/git-cherry-pick [commit-hash] [target-branch]`
**Examples**: 
- `/git-cherry-pick abc123 release/v2.0`
- `/git-cherry-pick fix-auth-bug main`
- `/git-cherry-pick abc123..def456 hotfix/security`

### Phase 1: Cherry-Pick Analysis
1. **Parse Arguments**
   - Extract commit hash(es) or range
   - Identify target branch
   - Validate commit existence
   - Check branch accessibility

2. **Commit Investigation**
   ```bash
   # Get commit details
   git show [commit] --stat
   
   # Check commit history
   git log --oneline -n 10 [commit]
   
   # Analyze changed files
   git diff-tree --no-commit-id --name-only -r [commit]
   ```

### Phase 2: Impact Assessment
1. **Change Analysis**
   - Files modified by commit(s)
   - Dependencies affected
   - Related commits that might be needed
   - Potential conflict areas

2. **Target Branch Compatibility**
   - Check target branch state
   - Identify divergence from source
   - Assess merge conflicts likelihood
   - Validate dependencies exist

### Phase 3: Pre-Cherry-Pick Validation
1. **Safety Checks**
   - Ensure clean working directory
   - Verify target branch is up-to-date
   - Check for uncommitted changes
   - Create backup branch

2. **Dependency Analysis**
   ```bash
   # Check if commit depends on other commits
   git log --oneline [commit]^..[commit]
   
   # Analyze file history
   git log --follow --oneline [files-from-commit]
   ```

### Phase 4: Cherry-Pick Execution
1. **Standard Cherry-Pick**
   ```bash
   # Switch to target branch
   git checkout [target-branch]
   
   # Create feature branch for cherry-pick
   git checkout -b cherry-pick/[description]
   
   # Execute cherry-pick
   git cherry-pick [commit]
   ```

2. **Range Cherry-Pick**
   ```bash
   # Cherry-pick commit range
   git cherry-pick [start-commit]..[end-commit]
   
   # Or with inclusive range
   git cherry-pick [start-commit]^..[end-commit]
   ```

### Phase 5: Conflict Resolution
1. **Conflict Detection**
   ```bash
   # Check conflict status
   git status
   
   # Show conflict details
   git diff --name-only --diff-filter=U
   ```

2. **Intelligent Resolution Guidance**
   ```markdown
   ## ⚠️ Merge Conflicts Detected
   
   ### Conflicted Files
   1. src/auth/login.js
      - Line 45-52: Authentication logic
      - Recommendation: Keep target branch version, apply security fix manually
   
   2. tests/auth.test.js
      - Line 120-135: Test assertions
      - Recommendation: Merge both changes, update test for new behavior
   
   ### Resolution Steps
   1. Review each conflict carefully
   2. Consider the context of both branches
   3. Test thoroughly after resolution
   4. Document any behavioral changes
   ```

3. **Automated Resolution Assistance**
   - Analyze conflict patterns
   - Suggest resolution strategies
   - Provide code snippets for common fixes
   - Offer to apply safe resolutions

### Phase 6: Post-Cherry-Pick Validation
1. **Build & Test**
   ```bash
   # Run build
   npm run build
   
   # Run affected tests
   npm test -- [affected-test-files]
   
   # Run integration tests
   npm run test:integration
   ```

2. **Change Verification**
   - Verify intended changes applied
   - Check for unintended side effects
   - Validate functionality works
   - Ensure no regressions

### Phase 7: Documentation
1. **Cherry-Pick Record**
   ```markdown
   ## Cherry-Pick Record
   
   ### Operation Details
   - **Date**: 2025-08-15
   - **Commits**: abc123 (Fix authentication bug)
   - **Source**: feature/auth
   - **Target**: release/v2.0
   - **Performer**: [current-profile]
   
   ### Reason
   Critical security fix needed in release branch
   
   ### Changes Applied
   - Fixed JWT validation vulnerability
   - Updated password hashing algorithm
   - Added rate limiting to login endpoint
   
   ### Conflicts Resolved
   - src/auth/login.js: Merged security fix with release changes
   
   ### Testing Performed
   - ✅ Unit tests pass
   - ✅ Integration tests pass
   - ✅ Security scan clean
   
   ### Notes
   - Requires config update in production
   - Monitor for performance impact
   ```

2. **Commit Message**
   ```
   cherry-pick: [original commit message]
   
   Cherry-picked from: [original-commit-hash]
   Original author: [author]
   Target context: [why needed in target branch]
   
   Conflicts resolved:
   - [file]: [resolution strategy]
   
   Testing: [what was tested]
   Impact: [any behavioral changes]
   ```

### Phase 8: Related Commits Analysis
1. **Dependency Check**
   - Identify related commits needed
   - Check for fix chains
   - Validate complete feature set
   - Ensure consistency

2. **Recommendation Generation**
   ```markdown
   ## 📋 Related Commits Recommended
   
   ### Should Also Cherry-Pick
   1. def456 - "Add tests for auth fix"
      - Adds test coverage for the fix
      - Ensures regression prevention
   
   2. ghi789 - "Update documentation"
      - Documents the security fix
      - Important for API users
   
   ### Optional Considerations
   1. jkl012 - "Performance optimization"
      - Improves auth performance
      - Not critical but beneficial
   ```

### Phase 9: Pull Request Creation
1. **PR for Cherry-Pick**
   ```bash
   # Push cherry-pick branch
   git push -u origin cherry-pick/[description]
   
   # Create pull request
   gh pr create \
     --title "Cherry-pick: [description]" \
     --body "Cherry-pick report content" \
     --base [target-branch]
   ```

2. **PR Documentation**
   - Link to original commit/PR
   - Explain why cherry-pick needed
   - Document any modifications
   - Request expedited review if critical

### Expected Deliverables
- [ ] Commit analysis and impact assessment
- [ ] Safe cherry-pick execution with backup
- [ ] Intelligent conflict resolution guidance
- [ ] Comprehensive testing validation
- [ ] Complete documentation of operation
- [ ] Related commits recommendation
- [ ] Pull request for review if needed
- [ ] Knowledge capture for future reference

**Cherry-pick operations include intelligent analysis, safe execution, and comprehensive documentation for traceability.**