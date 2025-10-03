---
description: "Switch between team member profiles with automatic git configuration"
allowed_tools: ["Bash", "Read", "Write", "Edit"]
---

Switch to profile: **$ARGUMENTS**

## 👤 Profile Management System

### Phase 1: Profile Validation
1. **Available Profiles**
   - `trimabk` - Trimbak Bardale (Technical Architect)
   - `sarthak` - Sarthak (Lead Developer)
   - Check if requested profile exists in `/Users/tbardale/.config/claude/profiles/`

2. **Current Status Check**
   - Read current active profile from `.claude/project.json`
   - Show current git configuration
   - Display current working context

### Phase 2: Profile Loading
1. **Load Profile Script**
   - Execute `/Users/tbardale/.config/claude/load-profile.sh $ARGUMENTS`
   - Verify profile loaded successfully
   - Confirm git configuration updated

2. **Local Git Configuration** 
   - Set repository-specific git user.name and user.email
   - Preserve global git configuration unchanged
   - Verify commit attribution will be correct

### Phase 3: Project Context Update
1. **Update Project Metadata**
   - Update `active_profile` in `.claude/project.json`
   - Set timestamp of profile switch
   - Log profile change for audit trail

2. **Context Preservation**
   - Maintain current epic/sprint/story context
   - Preserve development history and decisions
   - Update team assignment for current work

### Phase 4: Profile-Specific Configuration
1. **Trimabk Profile (Architect)**
   - Focus: System design, scalability, cross-team coordination
   - Response Style: Comprehensive, architecture-level, future considerations
   - Templates: Architecture-first epic templates
   - Git Context: Strategic commits with system-wide impact analysis

2. **Sarthak Profile (Developer)**
   - Focus: Implementation, code quality, practical solutions
   - Response Style: Concise-actionable, step-by-step, practical examples
   - Templates: User-story-driven implementation breakdown
   - Git Context: Implementation-focused commits with code details

### Phase 5: Verification & Feedback
1. **Profile Status Display**
   ```
   ✅ Profile switched successfully
   
   Current Profile: sarthak (Lead Developer)
   Git User: Sarthak <sarthak@iamplus.in>
   GitHub: iamplus-sarthak
   Focus: Implementation, code quality, practical solutions
   
   Active Context:
   - Project: claude-faq
   - Epic: EPIC-001 (if active)
   - Sprint: SPRINT-001 (if active)
   - Story: STORY-001 (if active)
   ```

2. **Next Steps Guidance**
   - Suggest appropriate commands for current profile
   - Show relevant epic/sprint/story context
   - Recommend workflow actions based on profile expertise

### Special Commands
- `/profile current` - Show current active profile and context
- `/profile list` - List all available profiles
- `/profile status` - Show detailed profile and git status

### Expected Deliverables
- [ ] Profile successfully loaded and activated
- [ ] Git configuration updated for repository
- [ ] Project metadata updated with new active profile
- [ ] Profile-specific behavior and templates activated
- [ ] Clear feedback on profile switch status

**Profile switching preserves all project context while adapting AI behavior and git attribution to the selected team member.**