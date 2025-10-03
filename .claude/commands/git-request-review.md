---
description: "Request review from specific team member with context and guidance"
allowed_tools: ["Bash", "Write", "Read", "Grep"]
---

Request code review from team member: **$ARGUMENTS**

## 👥 Review Request Process

**Usage**: `/git-request-review [@reviewer] [context]`
**Examples**: 
- `/git-request-review @sarthak EPIC-001`
- `/git-request-review @trimabk authentication-implementation`
- `/git-request-review @team critical-security-fix`

### Phase 1: Context Analysis
1. **Parse Request**
   - Extract reviewer identifier (@username or @team)
   - Identify review context (epic/sprint/story or description)
   - Determine current branch and changes
   - Check if PR exists or needs creation

2. **Reviewer Validation**
   - Map reviewer to GitHub username
   - Verify reviewer access to repository
   - Check reviewer availability/workload
   - Identify reviewer expertise area

### Phase 2: Change Preparation
1. **Change Summary**
   - Run `git status` and `git diff` analysis
   - Categorize changes by type and impact
   - Calculate change statistics
   - Identify critical changes needing attention

2. **Context Documentation**
   - Current epic/sprint/story objectives
   - Implementation decisions made
   - Trade-offs and alternatives considered
   - Dependencies and blockers

### Phase 3: Review Request Creation
1. **Pull Request Setup** (if not exists)
   ```bash
   # Create PR if needed
   gh pr create \
     --title "[Context] - Brief description" \
     --body "Generated review request content" \
     --reviewer "username"
   ```

2. **Existing PR Update**
   ```bash
   # Add reviewer to existing PR
   gh pr edit [PR] --add-reviewer "username"
   ```

### Phase 4: Review Guidance Generation
1. **Reviewer-Specific Focus Areas**
   
   **For Architect Review (trimabk)**
   ```markdown
   ## 🏗️ Architecture Review Request
   
   ### Review Focus Areas
   - System design alignment and patterns
   - Scalability and performance implications
   - Integration points and dependencies
   - Security architecture considerations
   - Future maintainability and extensibility
   
   ### Specific Questions
   1. Does the authentication flow align with our security architecture?
   2. Are there scalability concerns with the session management approach?
   3. Should we consider microservice extraction for auth module?
   ```
   
   **For Developer Review (sarthak)**
   ```markdown
   ## 💻 Implementation Review Request
   
   ### Review Focus Areas
   - Code quality and readability
   - Best practices and patterns
   - Test coverage and quality
   - Performance optimizations
   - Error handling completeness
   
   ### Specific Questions
   1. Is the React component structure optimal?
   2. Are MongoDB queries efficiently indexed?
   3. Should we add more unit tests for edge cases?
   ```

2. **Context-Aware Guidance**
   - Link to epic/sprint/story documentation
   - Highlight areas of uncertainty
   - Point out experimental approaches
   - Note time-sensitive elements

### Phase 5: Review Request Documentation
1. **Request Template**
   ```markdown
   ## 📋 Review Request: [Title]
   
   ### Request Details
   - **Requester**: [Current profile/user]
   - **Reviewer**: @[reviewer]
   - **Priority**: 🔴 Critical / 🟡 Normal / 🟢 Low
   - **Context**: [EPIC-001: Authentication System]
   - **Deadline**: [If applicable]
   
   ### Change Summary
   - **Type**: ✨ Feature / 🐛 Fix / ♻️ Refactor / 📚 Docs
   - **Impact**: High/Medium/Low
   - **Files Changed**: 15 files (+500 -200)
   - **Test Coverage**: 85%
   
   ### What I've Done
   - Implemented JWT authentication flow
   - Added email/password validation
   - Created login/logout endpoints
   - Added comprehensive test suite
   
   ### What I Need Reviewed
   1. **Security**: JWT implementation and session handling
   2. **Architecture**: Service layer structure
   3. **Performance**: Database query optimization
   4. **Testing**: Edge case coverage
   
   ### Specific Questions
   1. Is the JWT refresh token strategy secure?
   2. Should we cache user sessions in Redis?
   3. Are the error messages too detailed?
   
   ### Context & Decisions
   - Chose JWT over sessions for stateless auth
   - Implemented refresh tokens for security
   - Added rate limiting on login endpoint
   - Used bcrypt with 12 rounds for passwords
   
   ### Testing Instructions
   1. Run `npm install` to update dependencies
   2. Set up `.env` with test credentials
   3. Run `npm test` for unit tests
   4. Run `npm run test:e2e` for integration tests
   
   ### Related Documentation
   - [Epic Planning](docs/epics/EPIC-001/overview.md)
   - [API Specification](docs/api/authentication.md)
   - [Security Architecture](docs/architecture/security.md)
   ```

2. **Reviewer Checklist**
   - Code quality and standards
   - Security implications
   - Performance considerations
   - Test coverage adequacy
   - Documentation completeness

### Phase 6: Communication
1. **GitHub Integration**
   ```bash
   # Post review request comment
   gh pr comment [PR] --body "Review request content"
   
   # Assign reviewer
   gh pr edit [PR] --add-reviewer "[username]"
   
   # Add labels
   gh pr edit [PR] --add-label "needs-review,[priority]"
   ```

2. **Team Notification**
   - Update project database with review request
   - Set review status tracking
   - Schedule follow-up reminder
   - Log request in team activity

### Phase 7: Review Tracking
1. **Status Monitoring**
   - Track review request age
   - Monitor reviewer response time
   - Set escalation triggers
   - Update team dashboards

2. **Follow-up Actions**
   - Remind after 24 hours if no response
   - Escalate if critical and delayed
   - Reassign if reviewer unavailable
   - Thank reviewer upon completion

### Phase 8: Knowledge Capture
1. **Review Insights**
   - Document review feedback
   - Capture architectural decisions
   - Record best practices identified
   - Update team knowledge base

2. **Pattern Recognition**
   - Identify recurring review themes
   - Document common issues
   - Create review guidelines
   - Update coding standards

### Expected Deliverables
- [ ] Review request created with clear context
- [ ] Reviewer-specific guidance and focus areas
- [ ] Comprehensive change documentation
- [ ] Specific questions for reviewer attention
- [ ] Testing instructions and setup guide
- [ ] GitHub PR updated with reviewer assignment
- [ ] Review tracking and follow-up scheduled
- [ ] Knowledge capture mechanism in place

**Review requests are tailored to reviewer expertise and provide comprehensive context for efficient, focused code reviews.**