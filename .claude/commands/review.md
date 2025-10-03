---
description: "Deep code review with architecture, security, performance, and maintainability analysis"
allowed_tools: ["Read", "Grep", "Glob", "Bash", "Write"]
---

Perform comprehensive code review for: **$ARGUMENTS**

## 🔬 Deep Code Review Process

**Usage**: `/review [file/directory/PR]` or `/review` for current changes
**Examples**: 
- `/review src/auth/` - Review auth module
- `/review components/UserLogin.tsx` - Review specific file
- `/review` - Review current git changes

### Phase 1: Scope Analysis
1. **Target Identification**
   - Parse arguments to determine review scope
   - If no arguments, analyze current git changes (`git diff`, `git status`)
   - If directory, recursively analyze relevant files
   - If specific file, focus on that file and dependencies

2. **Context Gathering**
   - Read current epic/sprint/story context from .claude/project.json
   - Understand project technology stack and conventions
   - Identify active profile for perspective (architect vs developer)
   - Check for related test files and documentation

### Phase 2: Architecture Review
1. **System Design Analysis** (Trimabk Architect Focus)
   - Overall architecture alignment and patterns
   - Integration points and dependencies
   - Scalability and performance implications
   - Cross-cutting concerns (security, logging, monitoring)
   - Future maintenance and extensibility

2. **Component Design**
   - Single responsibility principle adherence
   - Proper abstraction levels
   - Interface design and contracts
   - Dependency injection and coupling
   - Reusability and modularity

### Phase 3: Code Quality Assessment
1. **Implementation Quality** (Sarthak Developer Focus)
   - Code readability and clarity
   - Naming conventions and consistency
   - Function/method size and complexity
   - Error handling and edge cases
   - Resource management and cleanup

2. **Technology-Specific Analysis**
   - **React/TypeScript**: Component patterns, hooks usage, type safety
   - **Node.js**: Async patterns, error handling, performance
   - **MongoDB**: Query optimization, data modeling
   - **Testing**: Coverage, quality, maintainability

### Phase 4: Security Analysis
1. **Security Vulnerabilities**
   - Input validation and sanitization
   - Authentication and authorization
   - Data exposure and privacy
   - Injection attacks (SQL, XSS, etc.)
   - Dependency vulnerabilities

2. **Best Practices**
   - Secrets management
   - Secure coding patterns
   - Error message disclosure
   - Rate limiting and DoS protection
   - HTTPS and encryption usage

### Phase 5: Performance Review
1. **Performance Analysis**
   - Algorithm efficiency and complexity
   - Database query optimization
   - Memory usage and leaks
   - Network requests and caching
   - Bundle size and loading performance

2. **Optimization Opportunities**
   - Code splitting and lazy loading
   - Memoization and caching strategies
   - Database indexing and queries
   - API response optimization
   - Frontend rendering performance

### Phase 6: Testing & Quality Assurance
1. **Test Coverage Analysis**
   - Unit test coverage and quality
   - Integration test scenarios
   - End-to-end test coverage
   - Edge cases and error scenarios
   - Performance and load testing

2. **Testing Quality**
   - Test readability and maintainability
   - Test data management
   - Mock usage and isolation
   - Test performance and reliability
   - Continuous integration compatibility

### Phase 7: Documentation & Maintainability
1. **Documentation Review**
   - Code comments quality and necessity
   - API documentation completeness
   - README and setup instructions
   - Architecture decision records
   - Inline documentation accuracy

2. **Maintainability Assessment**
   - Code complexity and readability
   - Dependency management
   - Configuration management
   - Debugging and troubleshooting ease
   - Future change impact analysis

### Phase 8: Standards & Conventions
1. **Project Standards Compliance**
   - Coding style and formatting
   - File organization and structure
   - Naming conventions consistency
   - Import/export patterns
   - Configuration and environment handling

2. **Technology Stack Alignment**
   - Framework usage patterns
   - Library integration best practices
   - TypeScript type usage
   - React patterns and hooks
   - Node.js and MongoDB patterns

### Phase 9: Review Report Generation
1. **Comprehensive Report**
   ```markdown
   ## 🔬 Code Review Report: [Target]
   
   ### Overview
   - Scope: [files/directories reviewed]
   - Context: [epic/sprint/story]
   - Reviewer Profile: [trimabk/sarthak perspective]
   
   ### Summary Score: 🟢 EXCELLENT / 🟡 GOOD / 🟠 NEEDS IMPROVEMENT / 🔴 ISSUES FOUND
   
   ### Architecture Assessment
   ✅ **Strengths**
   - [Specific architectural strengths]
   
   ⚠️ **Concerns**
   - [Architectural concerns or improvements]
   
   ### Code Quality: [Score/10]
   ✅ **Strengths**
   - [Code quality strengths]
   
   ❌ **Issues**
   - [Specific issues to address]
   
   ### Security: [Score/10]
   - [Security assessment and findings]
   
   ### Performance: [Score/10]
   - [Performance analysis and recommendations]
   
   ### Testing: [Score/10]
   - [Test coverage and quality assessment]
   
   ### Maintainability: [Score/10]
   - [Maintainability and documentation review]
   ```

2. **Actionable Recommendations**
   - **High Priority**: Critical issues requiring immediate attention
   - **Medium Priority**: Important improvements for next iteration
   - **Low Priority**: Nice-to-have optimizations
   - **Future Considerations**: Architectural improvements for roadmap

### Expected Deliverables
- [ ] Comprehensive multi-dimensional code review
- [ ] Architecture and design assessment
- [ ] Security vulnerability analysis
- [ ] Performance optimization recommendations
- [ ] Testing coverage and quality evaluation
- [ ] Maintainability and documentation review
- [ ] Prioritized action items with specific guidance
- [ ] Standards compliance verification

**Review perspective adapts to active profile (architect vs developer focus) and provides technology-stack-specific insights aligned with project requirements.**