# Test Epic Pipeline (NO-OP)

## Task 1: Create Dummy Epic
**Prompt**: 
```
Create dummy epic EPIC-TEST-001 "Test Feature System":

1. Create branch: epic/EPIC-TEST-001/planning
2. Create directory: docs/epics/EPIC-TEST-001/
3. Write epic overview file
4. Output: "Epic EPIC-TEST-001 created successfully"

Write results to pipeline-context.md
```

## Task 2: Create Sprint 1
**Context**: ./pipeline-context.md
**Prompt**:
```
Create dummy Sprint 1 under EPIC-TEST-001:

1. Create branch: epic/EPIC-TEST-001/sprint-001/planning
2. Create directory: docs/epics/EPIC-TEST-001/sprints/sprint-001/
3. Write sprint overview
4. Output: "Sprint 1 created - Core Features"

Append to pipeline-context.md
```

## Task 3: Create Sprint 2
**Context**: ./pipeline-context.md
**Prompt**:
```
Create dummy Sprint 2 under EPIC-TEST-001:

1. Create branch: epic/EPIC-TEST-001/sprint-002/planning
2. Create directory: docs/epics/EPIC-TEST-001/sprints/sprint-002/
3. Write sprint overview
4. Output: "Sprint 2 created - Advanced Features"

Append to pipeline-context.md
```

## Task 4: Create Sprint 3
**Context**: ./pipeline-context.md
**Prompt**:
```
Create dummy Sprint 3 under EPIC-TEST-001:

1. Create branch: epic/EPIC-TEST-001/sprint-003/planning
2. Create directory: docs/epics/EPIC-TEST-001/sprints/sprint-003/
3. Write sprint overview
4. Output: "Sprint 3 created - Polish & Testing"

Append to pipeline-context.md
```

## Task 5: Create Stories for Sprint 1
**Context**: ./pipeline-context.md
**Prompt**:
```
Create 3 dummy stories for Sprint 1:

1. Story TEST-001: "As user I want feature A"
2. Story TEST-002: "As user I want feature B" 
3. Story TEST-003: "As user I want feature C"

Create directories and files for each.
Output: "3 stories created for Sprint 1"

Append to pipeline-context.md
```

## Task 6: Create Stories for Sprint 2
**Context**: ./pipeline-context.md
**Prompt**:
```
Create 3 dummy stories for Sprint 2:

1. Story TEST-004: "As user I want advanced feature A"
2. Story TEST-005: "As user I want advanced feature B"
3. Story TEST-006: "As user I want advanced feature C"

Create directories and files for each.
Output: "3 stories created for Sprint 2"

Append to pipeline-context.md
```

## Task 7: Create Stories for Sprint 3
**Context**: ./pipeline-context.md
**Prompt**:
```
Create 3 dummy stories for Sprint 3:

1. Story TEST-007: "As user I want polished feature A"
2. Story TEST-008: "As user I want polished feature B"
3. Story TEST-009: "As user I want polished feature C"

Create directories and files for each.
Output: "3 stories created for Sprint 3"

Append to pipeline-context.md
```

## Task 8: Create Handoff Documentation
**Context**: ./pipeline-context.md
**Prompt**:
```
Create dummy handoff from planning to implementation:

1. Create handoff directory: docs/handoffs/planning-to-impl-$(date +%Y%m%d)/
2. Write handoff summary with all epic/sprint/story info
3. Output: "Handoff documentation created"

Append to pipeline-context.md
```

## Task 9: Setup Implementation Branches
**Context**: ./pipeline-context.md
**Prompt**:
```
Setup implementation branches (NO-OP):

1. List what implementation branches would be created
2. List what worktrees would be setup
3. Output: "Implementation environment ready (simulated)"

Append to pipeline-context.md
```

## Task 10: Run Tests (NO-OP)
**Context**: ./pipeline-context.md
**Prompt**:
```
Simulate running tests:

1. Output: "Running unit tests... PASSED (simulated)"
2. Output: "Running integration tests... PASSED (simulated)"
3. Output: "Running e2e tests... PASSED (simulated)"

Append to pipeline-context.md
```

## Task 11: Code Review (NO-OP)
**Context**: ./pipeline-context.md
**Prompt**:
```
Simulate code review:

1. Output: "Code review completed"
2. Output: "Architecture: APPROVED"
3. Output: "Security: APPROVED"
4. Output: "Performance: APPROVED"

Append to pipeline-context.md
```

## Task 12: Final Summary
**Context**: ./pipeline-context.md
**Prompt**:
```
Generate final pipeline summary from pipeline-context.md:

1. Count total epics created: 1
2. Count total sprints created: 3
3. Count total stories created: 9
4. List all branches that were created
5. Show final directory structure
6. Output: "Pipeline test completed successfully!"

Save complete summary as pipeline-result.md
```