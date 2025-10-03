# Claude Code Pipeline System v2.0
*Feature-driven development with proper git workflow*

## 🎯 **Key Improvements**

### 1. **Feature Naming System**
- User provides custom feature name or selects from suggestions
- All files organized under `.claude/{FEATURE_NAME}/`
- Consistent naming across branches, directories, and documentation

### 2. **Proper Branch Management**
- Feature branch: `feature-{FEATURE_NAME}`
- Task branches: `feature-{FEATURE_NAME}/task-{NUMBER}-{DESCRIPTION}`
- Epic/Sprint/Story branches: `feature-{FEATURE_NAME}/{TYPE}-{ID}-{ACTION}`
- Automatic merge back to feature branch with push
- Error handling: Stop execution if branch switching fails

### 3. **Hierarchical Workflow**
- **Epic → Sprint → Story** sequential completion
- Complete all stories before finishing sprint
- Complete all sprints before finishing epic
- Complete all epics before finishing feature

## 📋 **Available Pipelines**

### **Idea to Epic Pipeline v2.0**
```bash
/pipe idea-to-epic-v2 "Your product idea here"
```

**Features:**
- ✅ Feature naming (custom or suggested)
- ✅ Branch management with error handling
- ✅ Market research and competitive analysis
- ✅ PM and UX strategy development
- ✅ Epic structure planning and creation
- ✅ Complete research validation

**Output Structure:**
```
.claude/{FEATURE_NAME}/
├── structured-product-brief.md
├── market-research.md
├── competitive-analysis.md
├── user-research.md
├── technical-landscape.md
├── opportunity-assessment.md
├── pm-product-strategy.md
├── ux-strategy.md
├── epic-planning.md
├── pipeline-context.md
└── final-product-plan.md
```

### **Epic to Production Pipeline**
```bash
/pipe epic-to-production "{FEATURE_NAME}" "{EPIC_ID}"
```

**Hierarchical Flow:**
1. **Epic Phase**: Initialize → Create Sprints
2. **Sprint Phase**: Create Stories → Implement Stories → Complete Sprint
3. **Epic Completion**: Integration testing → Success criteria validation
4. **Feature Completion**: End-to-end testing → Production readiness

**Branch Strategy Example:**
```
feature-ai-chat-system
├── feature-ai-chat-system/epic-EPIC-001-implementation
├── feature-ai-chat-system/epic-EPIC-001-sprint-001
├── feature-ai-chat-system/sprint-SPRINT-001-stories
├── feature-ai-chat-system/story-STORY-001-implementation
├── feature-ai-chat-system/story-STORY-002-implementation
├── feature-ai-chat-system/sprint-SPRINT-001-completion
└── feature-ai-chat-system/epic-EPIC-001-completion
```

## 🔧 **Git Workflow**

### **Every Task Follows:**
1. **Create task branch** from feature branch
2. **Implement changes** with proper commits
3. **Switch back** to feature branch
4. **Merge task branch** with no fast-forward
5. **Push changes** to remote
6. **Delete task branch** cleanup

### **Error Handling:**
- If branch switching fails → **STOP EXECUTION**
- Display error: "Cannot switch to branch. Please fix git conflicts and retry."
- User must resolve conflicts before continuing

### **Commit Standards:**
```bash
feat({FEATURE_NAME}): Task {NUMBER} - {DESCRIPTION}
feat({FEATURE_NAME}): Complete Story {STORY_ID} - {STORY_TITLE}
feat({FEATURE_NAME}): Complete Sprint {SPRINT_ID} with all stories
feat({FEATURE_NAME}): Complete Epic {EPIC_ID} - {EPIC_NAME}
feat({FEATURE_NAME}): Complete Feature {FEATURE_NAME} - Production Ready
```

## 🚀 **Usage Examples**

### **1. Start New Feature**
```bash
# Idea to Epic pipeline with feature naming
/pipe idea-to-epic-v2 "AI-powered chat system for customer support"

# System will ask for feature name:
# - Custom name: "ai-chat-system"
# - Or choose from suggestions: "smart-support-chat", "ai-customer-assistant", etc.
```

### **2. Implement Feature**
```bash
# After epic planning is complete
/pipe epic-to-production "ai-chat-system" "EPIC-001"

# Will create complete implementation:
# - Initialize epic implementation
# - Create Sprint 1, 2, 3
# - For each sprint: create stories → implement → complete
# - Complete epic with integration testing
# - Ready for production deployment
```

### **3. Continue with Additional Epics**
```bash
# After Epic 1 is complete
/pipe epic-to-production "ai-chat-system" "EPIC-002"
/pipe epic-to-production "ai-chat-system" "EPIC-003"

# Finally complete the feature
/pipe epic-to-production "ai-chat-system" "FEATURE_COMPLETION"
```

## 📁 **Directory Structure**

```
.claude/
├── {FEATURE_NAME}/
│   ├── pipeline-context.md              # Central context tracking
│   ├── structured-product-brief.md      # Initial product structure
│   ├── market-research.md               # Competitive analysis
│   ├── user-research.md                 # User validation
│   ├── pm-product-strategy.md           # Product strategy
│   ├── ux-strategy.md                   # User experience strategy
│   ├── epic-planning.md                 # Epic structure
│   ├── final-product-plan.md            # Complete roadmap
│   ├── epic-{EPIC_ID}/
│   │   ├── implementation-plan.md       # Epic implementation plan
│   │   ├── sprint-breakdown.md          # Sprint organization
│   │   ├── completion-report.md         # Epic completion validation
│   │   └── success-criteria-validation.md
│   ├── sprint-{SPRINT_ID}/
│   │   ├── story-list.md                # Stories in sprint
│   │   ├── completion-report.md         # Sprint completion
│   │   └── demo-guide.md                # Sprint demo materials
│   ├── story-{STORY_ID}/
│   │   └── implementation-report.md     # Story implementation details
│   ├── FEATURE-COMPLETION-REPORT.md     # Final feature report
│   ├── PRODUCTION-READINESS-CHECKLIST.md
│   └── LAUNCH-PLAN.md                   # Go-to-market plan
├── commands/                            # Slash command definitions
├── pipelines/                           # Pipeline definitions
│   ├── idea-to-epic-v2.md              # Enhanced idea to epic
│   └── epic-to-production.md           # Implementation pipeline
└── templates/                           # Reusable templates
```

## ⚠️ **Breaking Changes from v1.0**

### **Required Changes:**
1. **Feature naming is now mandatory** - no more generic pipeline execution
2. **Branch switching must succeed** - pipeline stops on git conflicts
3. **Sequential completion required** - can't skip stories/sprints/epics
4. **Directory structure changed** - all files under feature directories

### **Migration from v1.0:**
- Existing pipelines will need feature name assignment
- Git branches may need restructuring
- File organization will need updates to new directory structure

## 🎯 **Benefits of v2.0**

1. **Better Organization**: Feature-based file structure
2. **Proper Git Workflow**: Branch per task with proper merging
3. **Error Prevention**: Branch conflicts stop execution
4. **Sequential Workflow**: Natural epic → sprint → story progression
5. **Production Ready**: Complete implementation with testing
6. **Scalable**: Multiple features can be developed in parallel

The v2.0 pipeline system ensures professional-grade development workflow with proper git practices and complete traceability from idea to production! 🚀