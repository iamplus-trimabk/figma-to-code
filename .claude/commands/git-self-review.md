---
description: "Review your own changes before committing with intelligent suggestions and quality checks"
allowed_tools: ["Bash", "Read", "Grep", "Glob", "Write"]
---

Perform intelligent self-review of current changes before committing.

## 🔍 Git Self-Review Process

### Phase 1: Change Discovery
1. **Scan All Changes**
   - Run `git status` to identify all modified, added, deleted files
   - Run `git diff --staged` for staged changes
   - Run `git diff` for unstaged changes
   - Identify scope: features, fixes, refactoring, tests, docs

2. **File Classification**
   - **Source Code**: Components, services, utilities, models
   - **Tests**: Unit tests, integration tests, e2e tests
   - **Configuration**: Package.json, env files, build configs
   - **Documentation**: README, API docs, inline comments

### Phase 2: Code Quality Analysis
1. **Code Review Checklist**
   - **Functionality**: Does code do what it's supposed to do?
   - **Readability**: Is code clear and easy to understand?
   - **Performance**: Any obvious performance issues?
   - **Security**: No secrets, proper input validation?
   - **Error Handling**: Proper error handling and edge cases?

2. **Pattern Consistency**
   - Follows project coding standards (from .claude/project.json tech stack)
   - Uses established patterns and conventions
   - Proper naming conventions for variables and functions
   - Consistent formatting and style

### Phase 3: Technology-Specific Checks
1. **React/Frontend Changes**
   - Component structure and hooks usage
   - Props validation and TypeScript types
   - State management patterns
   - Accessibility and responsive design
   - Performance optimization (useMemo, useCallback)

2. **Node.js/Backend Changes**
   - API endpoint security and validation
   - Database query optimization
   - Error handling and logging
   - Authentication and authorization
   - Rate limiting and input sanitization

3. **TypeScript/JavaScript**
   - Type safety and proper typing
   - No `any` types without justification
   - Proper async/await usage
   - Memory leak prevention

### Phase 4: Testing Coverage Analysis
1. **Test Requirements**
   - New features have corresponding tests
   - Changed functionality has updated tests
   - Tests cover edge cases and error scenarios
   - Integration points are tested

2. **Test Quality Check**
   - Tests are readable and maintainable
   - Test names clearly describe what they test
   - Proper test data setup and cleanup
   - No flaky or unreliable tests

### Phase 5: Security & Best Practices
1. **Security Scan**
   - No hardcoded secrets or API keys
   - Proper input validation and sanitization
   - No SQL injection or XSS vulnerabilities
   - Secure authentication and session handling

2. **Best Practices**
   - No console.log or debugging code in production
   - Proper error messages (not exposing internal details)
   - Resource cleanup (event listeners, subscriptions)
   - Proper dependency management

### Phase 6: Architecture & Design Review
1. **Design Consistency** (Profile-Aware)
   - **Trimabk (Architect) Focus**: System design alignment, scalability implications, integration patterns
   - **Sarthak (Developer) Focus**: Implementation quality, code maintainability, practical patterns

2. **Architecture Considerations**
   - Changes align with overall system architecture
   - No tight coupling or circular dependencies
   - Proper separation of concerns
   - Scalability and performance implications

### Phase 7: Documentation & Comments
1. **Code Documentation**
   - Complex logic has clear comments
   - API changes have updated documentation
   - README updated for significant changes
   - Inline comments explain "why" not "what"

2. **Change Documentation**
   - Breaking changes are documented
   - Migration guides for API changes
   - Configuration changes documented
   - Dependencies and deployment notes

### Phase 8: Review Report Generation
1. **Findings Summary**
   ```markdown
   ## 🔍 Self-Review Report
   
   ### Changes Summary
   - 5 files modified (3 components, 2 tests)
   - Added user authentication feature
   - Updated API endpoints for security
   
   ### Quality Assessment: ✅ GOOD / ⚠️ NEEDS ATTENTION / ❌ ISSUES FOUND
   
   ### Findings:
   ✅ **Strengths**
   - Good test coverage for new features
   - Proper TypeScript typing
   - Security best practices followed
   
   ⚠️ **Improvements Needed**
   - Add error boundary for UserLogin component
   - Consider memoizing expensive calculations
   - Update API documentation
   
   ❌ **Issues to Fix**
   - Console.log statement in production code
   - Missing input validation for email field
   
   ### Recommendations:
   1. Remove debugging statements
   2. Add input validation
   3. Update documentation
   ```

2. **Action Items**
   - List specific items to fix before committing
   - Suggest improvements for future consideration
   - Highlight areas needing team discussion

### Expected Deliverables
- [ ] Comprehensive analysis of all changes
- [ ] Quality assessment with specific findings
- [ ] Security and best practices validation
- [ ] Testing coverage evaluation
- [ ] Architecture alignment verification
- [ ] Action items for improvements
- [ ] Ready-to-commit recommendation or fix-first guidance

**Self-review adapts to current profile expertise (architect vs developer focus) and project technology stack for relevant, actionable feedback.**