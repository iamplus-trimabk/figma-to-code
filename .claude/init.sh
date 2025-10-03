#!/bin/bash
# Claude Orchestration Hub Initialization Script
# Executed automatically when Claude Code starts in this directory

set -e

# Detect context (hub vs project)
CURRENT_DIR=$(basename "$PWD")
if [[ -d "projects" && -f "CLAUDE.md" ]]; then
    CONTEXT="hub"
    PROJECT_NAME="claude-orchestration-hub"
    echo "✅ Hub context detected"
elif [[ -f "../CLAUDE.md" && -d "../projects" ]]; then
    CONTEXT="project"
    PROJECT_NAME=$(basename "$PWD")
    echo "✅ Project context detected: $PROJECT_NAME"
else
    CONTEXT="unknown"
    PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
    echo "⚠️  Unknown context, treating as legacy project: $PROJECT_NAME"
fi

# Git configuration detection
GIT_ORIGIN=$(git config --get remote.origin.url 2>/dev/null || echo "")
GIT_USER_EMAIL=$(git config user.email 2>/dev/null || echo "")
GIT_USER_NAME=$(git config user.name 2>/dev/null || echo "")

echo "🔍 Auto-detecting profile..."

# Profile detection function
detect_profile() {
    # Priority 1: Check existing git user email
    if [[ "$GIT_USER_EMAIL" == "trimbak@iamplus.in" ]]; then
        echo "trimabk"
        return 0
    elif [[ "$GIT_USER_EMAIL" == "sarthak@iamplus.in" ]]; then
        echo "sarthak"
        return 0
    fi
    
    # Priority 2: Check @iamplus.in domain
    if [[ "$GIT_USER_EMAIL" == *"@iamplus.in"* ]]; then
        local username=$(echo "$GIT_USER_EMAIL" | cut -d'@' -f1)
        if [[ -f "/Users/tbardale/.config/claude/profiles/$username.json" ]]; then
            echo "$username"
            return 0
        fi
    fi
    
    # Priority 3: Check git origin for project context
    if [[ "$GIT_ORIGIN" == *"iamplus-trimabk"* ]] || [[ "$GIT_ORIGIN" == *"trimbak"* ]]; then
        echo "trimabk"
        return 0
    elif [[ "$GIT_ORIGIN" == *"sarthak"* ]] || [[ "$GIT_ORIGIN" == *"iamplus-sarthak"* ]]; then
        echo "sarthak"
        return 0
    fi
    
    # Priority 4: Check if current system user matches profile
    local current_user=$(whoami)
    if [[ -f "/Users/tbardale/.config/claude/profiles/$current_user.json" ]]; then
        echo "$current_user"
        return 0
    fi
    
    # No profile detected
    echo ""
    return 1
}

# Attempt profile detection
DETECTED_PROFILE=$(detect_profile)

if [[ -n "$DETECTED_PROFILE" ]]; then
    echo "✅ Auto-detected profile: $DETECTED_PROFILE"
    
    # Check if profile loader exists
    if [[ -f "/Users/tbardale/.config/claude/load-profile.sh" ]]; then
        /Users/tbardale/.config/claude/load-profile.sh "$DETECTED_PROFILE"
    else
        echo "❌ Profile loader not found at /Users/tbardale/.config/claude/load-profile.sh"
        echo "Please ensure Claude configuration is properly installed."
        exit 1
    fi
else
    echo "❓ Could not auto-detect profile"
    echo ""
    echo "🔍 Context information:"
    echo "  Project: $PROJECT_NAME"
    echo "  Git origin: ${GIT_ORIGIN:-'(not set)'}"
    echo "  Git user: ${GIT_USER_NAME:-'(not set)'} <${GIT_USER_EMAIL:-'(not set)'}>"
    echo ""
    echo "📋 Available profiles:"
    if [[ -d "/Users/tbardale/.config/claude/profiles" ]]; then
        ls -1 /Users/tbardale/.config/claude/profiles/*.json 2>/dev/null | xargs -n 1 basename | sed 's/.json$//' | sed 's/^/  /' || echo "  (no profiles found)"
    else
        echo "  (profiles directory not found)"
    fi
    echo ""
    echo "🔧 Manual setup:"
    echo "  /Users/tbardale/.config/claude/load-profile.sh [profile-name]"
    echo ""
    echo "⚠️  Continuing without profile - Claude Code will use default settings"
fi

# Context-specific initialization
echo ""
if [[ "$CONTEXT" == "hub" ]]; then
    echo "🔧 Initializing Orchestration Hub..."
    
    # Ensure hub directory structure exists
    mkdir -p projects research automation notes
    mkdir -p .claude/{profiles,templates,mcp-config,cache,logs}
    mkdir -p docs/{architecture,requirements,testing,api}
    
    # Set hub environment variables
    export CLAUDE_CONTEXT="orchestration-hub"
    export CLAUDE_ROLE="multi-project-coordinator" 
    export CLAUDE_CAPABILITIES="research,analysis,automation,coordination,project-management"
    export CLAUDE_PROJECT_NAME="$PROJECT_NAME"
    export CLAUDE_PROJECT_TYPE="orchestration-hub"
    export CLAUDE_PROJECT_ROOT="$(pwd)"
    
    echo "✅ Claude Orchestration Hub initialized!"
    echo "🎯 Ready for multi-project coordination and research tasks"
    
elif [[ "$CONTEXT" == "project" ]]; then
    echo "🔧 Initializing Project Context: $PROJECT_NAME..."
    
    # Load project-specific configuration
    if [[ -f "CLAUDE.md" ]]; then
        echo "✅ Project configuration found"
    fi
    
    if [[ -f "repos.json" ]]; then
        echo "✅ Repository configuration found"
    fi
    
    if [[ -f "team.json" ]]; then
        echo "✅ Team configuration found"
    fi
    
    # Set project environment variables
    export CLAUDE_CONTEXT="project"
    export CLAUDE_PROJECT_NAME="$PROJECT_NAME"
    export CLAUDE_PROJECT_ROOT="$(pwd)"
    
    # Project-specific settings for Simflo
    if [[ "$PROJECT_NAME" == "simflo" ]]; then
        export CLAUDE_PROJECT_TYPE="real-time-messaging-platform"
        export CLAUDE_TECH_STACK="Express.js,Socket.IO,TypeScript,MongoDB,Commander.js"
        export CLAUDE_TESTING_FRAMEWORK="Vitest,node-pty,E2E-CLI"
        export CLAUDE_ARCHITECTURE="Backend,SDK,CLI,Testing"
        
        echo "✅ Simflo project context loaded"
        echo "🚀 Ready for real-time messaging development!"
    fi
    
else
    echo "🔧 Initializing Legacy Project: $PROJECT_NAME..."
    
    # Legacy initialization for backward compatibility
    mkdir -p .claude/{templates,workflows,cache,logs}
    mkdir -p docs/{architecture,requirements,testing,api}
    mkdir -p scripts
    mkdir -p data/sqlite
    
    # Set legacy environment variables
    export CLAUDE_CONTEXT="legacy-project"
    export CLAUDE_PROJECT_NAME="$PROJECT_NAME"
    export CLAUDE_PROJECT_TYPE="web-application"
    export CLAUDE_TECH_STACK="React,Node.js,TypeScript,MongoDB"
    export CLAUDE_TESTING_FRAMEWORK="Jest,Playwright,Cypress"
    export CLAUDE_PROJECT_ROOT="$(pwd)"
    
    echo "✅ Legacy project environment initialized"
fi

# Initialize SQLite database for project metadata
if command -v sqlite3 >/dev/null 2>&1; then
    sqlite3 data/sqlite/project.db << 'EOF'
CREATE TABLE IF NOT EXISTS epics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    epic_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'planning',
    created_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sprint_id TEXT UNIQUE NOT NULL,
    epic_id TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'planning',
    created_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (epic_id) REFERENCES epics(epic_id)
);

CREATE TABLE IF NOT EXISTS stories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    story_id TEXT UNIQUE NOT NULL,
    sprint_id TEXT NOT NULL,
    title TEXT NOT NULL,
    status TEXT DEFAULT 'planning',
    story_points INTEGER,
    assignee TEXT,
    created_by TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sprint_id) REFERENCES sprints(sprint_id)
);
EOF
    echo "✅ Project database initialized"
else
    echo "⚠️  SQLite not available - project database not initialized"
fi

# Log initialization
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Project initialized with profile: ${DETECTED_PROFILE:-'none'}" >> .claude/logs/init.log

# Update git configuration for Trimbak profile
git config user.name "Trimbak Bardale" 2>/dev/null || true
git config user.email "trimbak@iamplus.in" 2>/dev/null || true

# Log initialization
echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Context: $CONTEXT, Profile: ${DETECTED_PROFILE:-'none'}" >> .claude/logs/init.log

echo ""
echo "✅ Initialization completed successfully!"
echo ""
echo "🎯 Environment Summary:"
echo "  - Context: $CONTEXT"
echo "  - Profile: ${DETECTED_PROFILE:-'default'}"
echo "  - Project: $PROJECT_NAME"
echo "  - Git User: $(git config user.name) <$(git config user.email)>"
echo ""

if [[ "$CONTEXT" == "hub" ]]; then
    echo "🏗️  Hub capabilities:"
    echo "  • Multi-project management and coordination"
    echo "  • Research and analysis across domains"
    echo "  • Team and repository management"
    echo "  • Administrative task automation"
    echo ""
    echo "📋 Quick commands:"
    echo "  • cd projects/simflo && claude  - Switch to Simflo project"
    echo "  • claude research [topic]  - Perform research analysis"
    echo "  • claude team status  - Show team and project status"
elif [[ "$CONTEXT" == "project" && "$PROJECT_NAME" == "simflo" ]]; then
    echo "📋 Simflo repositories:"
    echo "  • simflo-core: Shared types and schemas"
    echo "  • simflo-backend: Express.js + Socket.IO server"
    echo "  • simflo-sdk: TypeScript client library"  
    echo "  • simflo-cli: Interactive command-line interface"
    echo ""
    echo "🔧 Development commands:"
    echo "  • claude work  - Enter development mode"
    echo "  • claude test  - Run project tests"
    echo "  • claude deploy  - Deploy to production"
else
    echo "🚀 You can now create epics, stories, and collaborate!"
    echo "   Example: claude github-agent \"Create epic: User Authentication System\""
fi

echo ""
echo "🌟 Claude Orchestration Hub ready for action!"