# Dummy Test Pipeline

## Task 1: Create Dummy Epic
**Prompt**: 
```
Create dummy epic:
- Epic ID: DUMMY-001
- Name: "Test Feature System"
- Status: Planning
- Output: "Epic DUMMY-001 created"

Write to pipeline-context.md
```

## Task 2: Create Dummy Sprint 1
**Prompt**:
```
Create dummy Sprint 1:
- Sprint ID: SPRINT-001
- Name: "Core Features"  
- Epic: DUMMY-001
- Status: Planning
- Output: "Sprint 1 created under DUMMY-001"

Append to pipeline-context.md
```

## Task 3: Create Dummy Sprint 2
**Prompt**:
```
Create dummy Sprint 2:
- Sprint ID: SPRINT-002
- Name: "Advanced Features"
- Epic: DUMMY-001
- Status: Planning
- Output: "Sprint 2 created under DUMMY-001"

Append to pipeline-context.md
```

## Task 4: Create Stories for Sprint 1
**Prompt**:
```
Create 3 dummy stories for Sprint 1:
- STORY-001: "As user I want feature A"
- STORY-002: "As user I want feature B"
- STORY-003: "As user I want feature C"
- Output: "3 stories created for Sprint 1"

Append to pipeline-context.md
```

## Task 5: Create Stories for Sprint 2
**Prompt**:
```
Create 3 dummy stories for Sprint 2:
- STORY-004: "As user I want advanced feature X"
- STORY-005: "As user I want advanced feature Y"
- STORY-006: "As user I want advanced feature Z"
- Output: "3 stories created for Sprint 2"

Append to pipeline-context.md
```

## Task 6: Implement Story STORY-001 (Dummy)
**Prompt**:
```
Dummy implementation of STORY-001:
1. Create file: feature-a.js (dummy content)
2. Create test: feature-a.test.js (dummy test)
3. Update documentation
4. Output: "STORY-001 implemented"

Append to pipeline-context.md
```

## Task 7: Implement Story STORY-002 (Dummy)
**Prompt**:
```
Dummy implementation of STORY-002:
1. Create file: feature-b.js (dummy content)
2. Create test: feature-b.test.js (dummy test)
3. Update documentation
4. Output: "STORY-002 implemented"

Append to pipeline-context.md
```

## Task 8: Test All Stories (Dummy)
**Prompt**:
```
Dummy test execution:
1. Run unit tests: PASSED (dummy)
2. Run integration tests: PASSED (dummy)
3. Coverage: 85% (dummy)
4. Output: "All tests passing"

Append to pipeline-context.md
```

## Task 9: Code Review (Dummy)
**Prompt**:
```
Dummy code review:
1. Architecture: APPROVED (dummy)
2. Security: APPROVED (dummy)
3. Performance: APPROVED (dummy)
4. Output: "Code review completed"

Append to pipeline-context.md
```

## Task 10: Deploy (Dummy)
**Prompt**:
```
Dummy deployment:
1. Build: SUCCESS (dummy)
2. Deploy to staging: SUCCESS (dummy)
3. Deploy to production: SUCCESS (dummy)
4. Output: "Deployment completed"

Append to pipeline-context.md
```

## Task 11: Final Summary
**Prompt**:
```
Generate summary from pipeline-context.md:
- Count epics created: 1
- Count sprints created: 2
- Count stories created: 6
- Count stories implemented: 2
- Tests status: All passing
- Deployment status: Completed
- Output: "Pipeline test completed successfully!"

Save summary as pipeline-result.md
```