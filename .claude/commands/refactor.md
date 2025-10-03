---
description: "Guided refactoring with impact analysis, safe execution, and validation"
allowed_tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "TodoWrite"]
---

Refactor code: **$ARGUMENTS**

## ♻️ Intelligent Refactoring Process

**Usage**: `/refactor [refactoring-type] [target]`
**Examples**: 
- `/refactor extract-service user-authentication`
- `/refactor rename-variable getUserData to fetchUserProfile`
- `/refactor split-component UserDashboard`
- `/refactor optimize-query database/queries.js`

### Phase 1: Refactoring Analysis
1. **Parse Refactoring Request**
   - Identify refactoring type
   - Locate target code/component
   - Determine scope of changes
   - Assess complexity and risk

2. **Refactoring Types**
   ```markdown
   ## 📋 Refactoring Catalog
   
   ### Extraction
   - Extract Method/Function
   - Extract Service/Module
   - Extract Component
   - Extract Interface
   
   ### Restructuring
   - Split Component/Module
   - Merge Duplicates
   - Move Method/Function
   - Inline Method
   
   ### Renaming
   - Rename Variable/Function
   - Rename Class/Component
   - Rename File/Module
   
   ### Optimization
   - Optimize Loops
   - Simplify Conditionals
   - Remove Dead Code
   - Consolidate Duplicates
   ```

### Phase 2: Impact Assessment
1. **Dependency Analysis**
   ```markdown
   ## 🔍 Impact Analysis
   
   ### Target: auth.service.js
   
   ### Direct Dependencies (5 files)
   - controllers/user.js: Lines 23, 45, 67
   - middleware/auth.js: Lines 12, 34
   - routes/api.js: Line 89
   - tests/auth.test.js: Lines 15-120
   - utils/jwt.js: Line 5
   
   ### Indirect Impact (12 files)
   - Components using auth service
   - API endpoints requiring auth
   - Test files with auth mocks
   
   ### Risk Assessment: 🟡 Medium
   - Core functionality affected
   - Multiple consumer updates needed
   - Test updates required
   ```

2. **Breaking Change Detection**
   - API signature changes
   - Export modifications
   - Type/interface changes
   - Configuration impacts

### Phase 3: Refactoring Plan
1. **Step-by-Step Plan**
   ```markdown
   ## 📝 Refactoring Plan: Extract Auth Service
   
   ### Phase 1: Preparation
   - [ ] Create feature branch
   - [ ] Run existing tests (baseline)
   - [ ] Document current behavior
   - [ ] Set up refactoring tests
   
   ### Phase 2: Extraction
   - [ ] Create new service file
   - [ ] Move authentication logic
   - [ ] Create service interface
   - [ ] Update imports/exports
   
   ### Phase 3: Integration
   - [ ] Update consumers (5 files)
   - [ ] Fix import statements
   - [ ] Update dependency injection
   - [ ] Maintain backward compatibility
   
   ### Phase 4: Validation
   - [ ] Run unit tests
   - [ ] Run integration tests
   - [ ] Manual testing
   - [ ] Performance comparison
   
   ### Phase 5: Cleanup
   - [ ] Remove old code
   - [ ] Update documentation
   - [ ] Clean up imports
   - [ ] Update type definitions
   ```

2. **Safety Checks**
   - Create backup branch
   - Ensure tests pass before starting
   - Set up rollback plan
   - Monitor for regressions

### Phase 4: Automated Refactoring
1. **Extract Method/Function**
   ```markdown
   ## 🔧 Extract Method Refactoring
   
   ### Original Code
   ```javascript
   // Before: Long function with multiple responsibilities
   async function processUser(data) {
     // Validation logic (15 lines)
     if (!data.email) throw new Error('Email required');
     if (!data.password) throw new Error('Password required');
     // ... more validation
     
     // Hash password (10 lines)
     const salt = await bcrypt.genSalt(10);
     const hashedPassword = await bcrypt.hash(data.password, salt);
     // ... more hashing logic
     
     // Save to database (8 lines)
     const user = new User(data);
     await user.save();
     // ... more database logic
   }
   ```
   
   ### Refactored Code
   ```javascript
   // After: Extracted methods with single responsibility
   async function processUser(data) {
     validateUserData(data);
     const hashedData = await hashPassword(data);
     return await saveUser(hashedData);
   }
   
   function validateUserData(data) {
     if (!data.email) throw new Error('Email required');
     if (!data.password) throw new Error('Password required');
     // ... validation logic
   }
   
   async function hashPassword(data) {
     const salt = await bcrypt.genSalt(10);
     data.password = await bcrypt.hash(data.password, salt);
     return data;
   }
   
   async function saveUser(data) {
     const user = new User(data);
     return await user.save();
   }
   ```
   ```

2. **Rename Variable/Function**
   ```bash
   # Automated rename across codebase
   # Find all occurrences
   grep -r "getUserData" --include="*.js"
   
   # Perform rename with confirmation
   find . -name "*.js" -exec sed -i.bak 's/getUserData/fetchUserProfile/g' {} \;
   ```

### Phase 5: Component Refactoring
1. **Split Component**
   ```markdown
   ## 🎨 Component Split Refactoring
   
   ### Original: Monolithic Component
   ```jsx
   // Before: Large component with multiple concerns
   function UserDashboard() {
     // 500+ lines of mixed logic
     // - User profile display
     // - Settings management
     // - Activity feed
     // - Notifications
   }
   ```
   
   ### Refactored: Separated Concerns
   ```jsx
   // After: Focused components
   function UserDashboard() {
     return (
       <div>
         <UserProfile user={user} />
         <UserSettings settings={settings} />
         <ActivityFeed activities={activities} />
         <NotificationPanel notifications={notifications} />
       </div>
     );
   }
   
   // Extracted components
   function UserProfile({ user }) { /* ... */ }
   function UserSettings({ settings }) { /* ... */ }
   function ActivityFeed({ activities }) { /* ... */ }
   function NotificationPanel({ notifications }) { /* ... */ }
   ```
   ```

2. **Extract Service Layer**
   - Separate business logic
   - Create service interfaces
   - Implement dependency injection
   - Update consumers

### Phase 6: Code Optimization
1. **Performance Refactoring**
   ```markdown
   ## ⚡ Performance Optimization
   
   ### Query Optimization
   ```javascript
   // Before: N+1 query problem
   const users = await User.find();
   for (const user of users) {
     user.posts = await Post.find({ userId: user.id });
   }
   
   // After: Optimized with join
   const users = await User.aggregate([
     {
       $lookup: {
         from: 'posts',
         localField: '_id',
         foreignField: 'userId',
         as: 'posts'
       }
     }
   ]);
   ```
   
   ### React Optimization
   ```javascript
   // Before: Unnecessary re-renders
   function Component({ data }) {
     const processedData = data.map(complexTransform);
     return <List items={processedData} />;
   }
   
   // After: Memoized computation
   function Component({ data }) {
     const processedData = useMemo(
       () => data.map(complexTransform),
       [data]
     );
     return <List items={processedData} />;
   }
   ```
   ```

2. **Algorithm Optimization**
   - Identify inefficient algorithms
   - Suggest better approaches
   - Implement optimizations
   - Benchmark improvements

### Phase 7: Type Safety Refactoring
1. **Add TypeScript Types**
   ```typescript
   // Before: JavaScript without types
   function processUser(data) {
     return {
       id: data.id,
       name: data.name,
       email: data.email
     };
   }
   
   // After: TypeScript with full type safety
   interface UserData {
     id: string;
     name: string;
     email: string;
     createdAt?: Date;
   }
   
   interface ProcessedUser {
     id: string;
     name: string;
     email: string;
   }
   
   function processUser(data: UserData): ProcessedUser {
     return {
       id: data.id,
       name: data.name,
       email: data.email
     };
   }
   ```

### Phase 8: Testing During Refactoring
1. **Refactoring Test Suite**
   ```javascript
   // Characterization tests
   describe('Refactoring Safety Tests', () => {
     let originalBehavior;
     
     beforeAll(() => {
       // Capture original behavior
       originalBehavior = captureCurrentBehavior();
     });
     
     test('behavior unchanged after refactoring', () => {
       const newBehavior = captureCurrentBehavior();
       expect(newBehavior).toEqual(originalBehavior);
     });
   });
   ```

2. **Regression Prevention**
   - Run tests before each step
   - Add tests for new structure
   - Verify performance metrics
   - Check for breaking changes

### Phase 9: Documentation Updates
1. **Update Documentation**
   ```markdown
   ## 📚 Documentation Updates
   
   ### API Changes
   - ❌ Deprecated: `getUserData(id)`
   - ✅ New: `fetchUserProfile(id, options)`
   
   ### Migration Guide
   ```javascript
   // Old way
   const data = getUserData(userId);
   
   // New way
   const profile = await fetchUserProfile(userId, {
     includeMetadata: true
   });
   ```
   
   ### Breaking Changes
   - Return type changed from object to Promise
   - Added required options parameter
   - Renamed response properties
   ```

### Phase 10: Validation & Rollback
1. **Validation Checklist**
   ```markdown
   ## ✅ Refactoring Validation
   
   ### Functional Validation
   - [ ] All tests passing
   - [ ] No new warnings/errors
   - [ ] Feature parity maintained
   - [ ] Performance unchanged/improved
   
   ### Code Quality
   - [ ] Improved readability
   - [ ] Better structure
   - [ ] Reduced complexity
   - [ ] DRY principle applied
   
   ### Documentation
   - [ ] Code comments updated
   - [ ] API docs updated
   - [ ] README updated
   - [ ] Migration guide created
   ```

2. **Rollback Plan**
   ```bash
   # If issues detected
   git stash  # Save current work
   git checkout main
   git branch -D refactor-branch
   git checkout -b refactor-branch
   git stash pop  # Restore work
   ```

### Expected Deliverables
- [ ] Complete impact analysis with dependency map
- [ ] Step-by-step refactoring plan
- [ ] Automated refactoring execution where possible
- [ ] Comprehensive testing throughout process
- [ ] Performance comparison before/after
- [ ] Updated documentation and migration guides
- [ ] Validation checklist completed
- [ ] Rollback plan ready if needed

**Refactoring provides safe, systematic code improvement with comprehensive impact analysis and validation.**