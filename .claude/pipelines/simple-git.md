# Simple Git Pipeline

## Task 1: Check Status
**Prompt**: 
```
git status
Write output to pipeline-context.md
```

## Task 2: Review Changes  
**Prompt**:
```
/git-self-review
Add review results to pipeline-context.md
```

## Task 3: Commit Changes
**Prompt**:
```
/git-commit
Add commit hash to pipeline-context.md
```

## Task 4: Push Changes
**Prompt**:
```
git push origin HEAD
Add result to pipeline-context.md
```

## Task 5: Summary
**Prompt**:
```
Read pipeline-context.md and generate summary of all operations completed.
```