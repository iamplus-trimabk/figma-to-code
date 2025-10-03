---
description: "Comprehensive PR review with security, performance, and architecture analysis"
allowed_tools: ["Bash", "Read", "Grep", "Glob", "Write", "WebFetch"]
---

Perform comprehensive PR review: **$ARGUMENTS**

## 🔍 Pull Request Review Process

**Usage**: `/git-review-pr [PR-number]` or `/git-review-pr [PR-URL]`
**Examples**: 
- `/git-review-pr 123`
- `/git-review-pr https://github.com/org/repo/pull/123`

### Phase 1: PR Context Retrieval
1. **Fetch PR Information**
   - Use `gh pr view $ARGUMENTS --json` to get PR metadata
   - Retrieve title, description, author, and target branch
   - Fetch list of changed files and diff statistics
   - Get existing comments and review status

2. **Local Checkout**
   - Create review branch: `review/pr-[number]`
   - Fetch and checkout PR code locally
   - Ensure clean working directory
   - Preserve current branch for later restoration

### Phase 2: Change Analysis
1. **File Change Overview**
   - Categorize changes: features, fixes, refactoring, tests, docs
   - Calculate change impact: lines added/removed/modified
   - Identify critical path changes
   - Map changes to epic/sprint/story context

2. **Diff Deep Dive**
   - Review each file change systematically
   - Analyze code additions and deletions
   - Identify patterns and architectural changes
   - Check for consistency across changes

### Phase 3: Multi-Dimensional Review

#### **Architecture Review** (Trimabk Focus)
1. **System Design Impact**
   - Architectural pattern compliance
   - Scalability implications
   - Integration point changes
   - Cross-cutting concerns
   - Future maintainability

2. **Design Patterns**
   - SOLID principles adherence
   - Design pattern usage
   - Abstraction appropriateness
   - Coupling and cohesion analysis

#### **Code Quality Review** (Sarthak Focus)
1. **Implementation Quality**
   - Code readability and clarity
   - Naming conventions
   - Function complexity
   - Error handling completeness
   - Resource management

2. **Best Practices**
   - Framework-specific patterns
   - Language idioms
   - Performance optimizations
   - Code duplication analysis

### Phase 4: Security Analysis
1. **Vulnerability Scanning**
   - Input validation and sanitization
   - Authentication/authorization changes
   - Secrets and credential exposure
   - Dependency vulnerabilities
   - OWASP Top 10 compliance

2. **Security Best Practices**
   - Secure coding patterns
   - Data encryption usage
   - Session management
   - API security measures
   - Error message disclosure

### Phase 5: Performance Review
1. **Performance Impact**
   - Algorithm complexity analysis
   - Database query optimization
   - Memory usage patterns
   - Network request efficiency
   - Frontend rendering performance

2. **Optimization Opportunities**
   - Caching strategies
   - Query optimization
   - Bundle size impact
   - Lazy loading opportunities
   - Performance bottlenecks

### Phase 6: Testing Validation
1. **Test Coverage Analysis**
   - New code test coverage
   - Modified code test updates
   - Edge case coverage
   - Integration test adequacy
   - E2E test scenarios

2. **Test Quality Review**
   - Test readability and maintenance
   - Proper mocking and isolation
   - Test data management
   - CI/CD compatibility
   - Test performance

### Phase 7: Documentation & Standards
1. **Documentation Updates**
   - API documentation changes
   - README updates
   - Code comment quality
   - Architecture decision records
   - Migration guides

2. **Standards Compliance**
   - Coding style consistency
   - Linting rule compliance
   - Commit message format
   - PR description quality
   - Branch naming conventions

### Phase 8: Automated Checks
1. **Run Automated Tests**
   ```bash
   # Based on project.json tech stack
   npm test          # Unit tests
   npm run test:e2e  # E2E tests
   npm run lint      # Linting
   npm run typecheck # TypeScript
   ```

2. **Security & Dependency Scan**
   - Run security audit
   - Check dependency updates
   - Scan for vulnerabilities
   - License compliance check

### Phase 9: Review Report Generation
1. **Comprehensive PR Review Report**
   ```markdown
   ## 📋 PR Review: #123 - [Title]
   
   ### Summary
   - **Author**: @username
   - **Target**: main ← feature/branch
   - **Changes**: +500 -200 across 15 files
   - **Risk Level**: 🟢 Low / 🟡 Medium / 🔴 High
   
   ### Review Decision: ✅ APPROVE / 🔄 REQUEST CHANGES / 💬 COMMENT
   
   ### Architecture & Design: [8/10]
   ✅ **Strengths**
   - Good separation of concerns
   - Scalable approach to authentication
   
   ⚠️ **Suggestions**
   - Consider extracting auth logic to service
   
   ### Code Quality: [9/10]
   ✅ Clean, readable implementation
   ⚠️ Minor: Variable naming in auth.js:45
   
   ### Security: [7/10]
   ❌ **Must Fix**
   - Add input validation for email field
   - Rate limiting needed on login endpoint
   
   ### Performance: [8/10]
   ✅ Efficient database queries
   ⚠️ Consider caching user sessions
   
   ### Testing: [9/10]
   ✅ Good test coverage (85%)
   ⚠️ Add edge case for expired tokens
   
   ### Required Changes
   1. 🔴 Add email validation (security)
   2. 🔴 Implement rate limiting (security)
   3. 🟡 Add token expiry test (testing)
   
   ### Suggestions
   1. Extract auth service (architecture)
   2. Add session caching (performance)
   3. Update API docs (documentation)
   ```

2. **GitHub Comment Generation**
   - Post review summary as PR comment
   - Add inline comments for specific issues
   - Suggest specific code improvements
   - Request changes if needed

### Phase 10: Follow-up Actions
1. **Review Submission**
   ```bash
   gh pr review $ARGUMENTS \
     --approve|--request-changes|--comment \
     --body "Review report content"
   ```

2. **Track Review Items**
   - Create issues for major findings
   - Update project database with review status
   - Schedule follow-up if changes requested
   - Notify team of review completion

### Expected Deliverables
- [ ] Complete PR analysis with local checkout
- [ ] Multi-dimensional review (architecture, quality, security, performance)
- [ ] Automated test execution and validation
- [ ] Comprehensive review report with risk assessment
- [ ] Specific required changes and suggestions
- [ ] GitHub PR review submission with comments
- [ ] Follow-up action items and tracking

**PR review adapts to active profile perspective and provides actionable, specific feedback aligned with project standards and requirements.**