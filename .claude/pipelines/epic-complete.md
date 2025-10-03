# Complete Epic Pipeline with Implementation

## Task 1: Create Epic
**Prompt**: 
```
Create epic EPIC-TEST-001 "User Authentication System":
1. Create branch: epic/EPIC-TEST-001/planning
2. Create docs/epics/EPIC-TEST-001/
3. Write epic overview
Write results to pipeline-context.md
```

## Task 2-4: Create 3 Sprints
**Prompt**: 
```
Create 3 sprints under EPIC-TEST-001:
- Sprint 1: Core Auth (login/logout)
- Sprint 2: Advanced Auth (2FA, SSO)  
- Sprint 3: Security & Polish
Create branches and documentation.
Append to pipeline-context.md
```

## Task 5-13: Create Stories (3 per sprint)
**Prompt**:
```
Create 9 stories total:

Sprint 1 Stories:
- AUTH-001: "As user I want to login with email/password"
- AUTH-002: "As user I want to logout securely"
- AUTH-003: "As user I want password validation"

Sprint 2 Stories:
- AUTH-004: "As user I want 2FA authentication"
- AUTH-005: "As user I want SSO login"
- AUTH-006: "As user I want session management"

Sprint 3 Stories:
- AUTH-007: "As user I want password reset"
- AUTH-008: "As user I want account lockout protection"
- AUTH-009: "As user I want audit logs"

Create story directories and files.
Append to pipeline-context.md
```

## Task 14: Planning Handoff
**Prompt**:
```
Create handoff from planning to implementation:
1. Create handoff documentation
2. Technical specifications
3. API contracts
4. Ready for development
Append to pipeline-context.md
```

## Task 15-23: IMPLEMENTATION - Story AUTH-001 (Login)
**Prompt**:
```
IMPLEMENT AUTH-001: User login with email/password

Break down into tasks:
1. Create user model (User.js)
2. Create auth controller (authController.js)
3. Create login endpoint (POST /api/auth/login)
4. Create password hashing service
5. Create JWT token service
6. Create login form component (React)
7. Create auth state management
8. Write unit tests for auth
9. Write integration tests

Actually implement each file with real code.
Document progress in pipeline-context.md
```

## Task 24-32: IMPLEMENTATION - Story AUTH-002 (Logout)
**Prompt**:
```
IMPLEMENT AUTH-002: User logout securely

Break down into tasks:
1. Create logout endpoint (POST /api/auth/logout)
2. Create token blacklist service
3. Create logout component
4. Update auth state on logout
5. Clear local storage/cookies
6. Redirect after logout
7. Write logout tests
8. Test token invalidation
9. Security testing

Actually implement each component.
Document in pipeline-context.md
```

## Task 33-41: IMPLEMENTATION - Story AUTH-003 (Password Validation)
**Prompt**:
```
IMPLEMENT AUTH-003: Password validation

Break down into tasks:
1. Create password validation rules
2. Create validation middleware
3. Create password strength meter
4. Create validation error handling
5. Frontend validation component
6. Backend validation service
7. Password complexity tests
8. Error message handling
9. UX improvements

Implement all validation logic.
Document in pipeline-context.md
```

## Task 42-50: IMPLEMENTATION - Story AUTH-004 (2FA)
**Prompt**:
```
IMPLEMENT AUTH-004: 2FA authentication

Break down into tasks:
1. Create TOTP service
2. Create QR code generation
3. Create 2FA setup flow
4. Create 2FA verification
5. Create backup codes
6. Update login flow for 2FA
7. Create 2FA UI components
8. Write 2FA tests
9. Security validation

Implement complete 2FA system.
Document in pipeline-context.md
```

## Task 51-59: IMPLEMENTATION - Story AUTH-005 (SSO)
**Prompt**:
```
IMPLEMENT AUTH-005: SSO login

Break down into tasks:
1. OAuth2 integration setup
2. Google OAuth provider
3. Microsoft OAuth provider
4. User account linking
5. SSO login flow
6. Profile synchronization
7. SSO UI components
8. OAuth tests
9. Security review

Implement SSO authentication.
Document in pipeline-context.md
```

## Task 60-68: IMPLEMENTATION - Story AUTH-006 (Session Management)
**Prompt**:
```
IMPLEMENT AUTH-006: Session management

Break down into tasks:
1. Session store (Redis)
2. Session middleware
3. Session timeout handling
4. Concurrent session limits
5. Session monitoring
6. Session cleanup
7. Session UI indicators
8. Session tests
9. Performance optimization

Implement session management.
Document in pipeline-context.md
```

## Task 69-77: IMPLEMENTATION - Story AUTH-007 (Password Reset)
**Prompt**:
```
IMPLEMENT AUTH-007: Password reset

Break down into tasks:
1. Password reset request endpoint
2. Email service integration
3. Reset token generation
4. Reset token validation
5. Password update endpoint
6. Reset form components
7. Email templates
8. Reset flow tests
9. Security validation

Implement password reset flow.
Document in pipeline-context.md
```

## Task 78-86: IMPLEMENTATION - Story AUTH-008 (Account Lockout)
**Prompt**:
```
IMPLEMENT AUTH-008: Account lockout protection

Break down into tasks:
1. Failed attempt tracking
2. Account lockout logic
3. Lockout notification
4. Admin unlock feature
5. Lockout UI messaging
6. Rate limiting
7. Brute force protection
8. Lockout tests
9. Admin tools

Implement account protection.
Document in pipeline-context.md
```

## Task 87-95: IMPLEMENTATION - Story AUTH-009 (Audit Logs)
**Prompt**:
```
IMPLEMENT AUTH-009: Authentication audit logs

Break down into tasks:
1. Audit log schema
2. Log capture middleware
3. Login/logout logging
4. Failed attempt logging
5. Admin access logging
6. Log storage service
7. Log viewing interface
8. Log retention policy
9. Security monitoring

Implement audit logging.
Document in pipeline-context.md
```

## Task 96: Integration Testing
**Prompt**:
```
Run complete integration tests:
1. End-to-end auth flows
2. Cross-browser testing
3. Mobile responsiveness
4. Performance testing
5. Security penetration testing
Document results in pipeline-context.md
```

## Task 97: Code Review
**Prompt**:
```
Comprehensive code review:
1. Architecture review
2. Security audit
3. Performance analysis
4. Code quality check
5. Documentation review
Add review results to pipeline-context.md
```

## Task 98: Deployment Preparation
**Prompt**:
```
Prepare for deployment:
1. Build production assets
2. Environment configuration
3. Database migrations
4. Security checklist
5. Deployment scripts
Document deployment plan in pipeline-context.md
```

## Task 99: Staging Deployment
**Prompt**:
```
Deploy to staging:
1. Deploy application
2. Run smoke tests
3. Verify all auth flows
4. Performance validation
5. Security validation
Document staging results in pipeline-context.md
```

## Task 100: Production Deployment
**Prompt**:
```
Deploy to production:
1. Final pre-deployment checks
2. Production deployment
3. Post-deployment validation
4. Monitor system health
5. User acceptance testing
Document production deployment in pipeline-context.md
```

## Task 101: Final Summary
**Prompt**:
```
Generate complete pipeline summary:
- Epic: 1 (EPIC-TEST-001)
- Sprints: 3
- Stories: 9 (all implemented)
- Tasks: 100+ individual implementation tasks
- Lines of code written
- Tests created
- Documentation generated
- Deployment completed

Save as pipeline-result.md with full metrics.
```