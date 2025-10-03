---
description: "Initialize new project from baseline template with complete setup and configuration"
allowed_tools: ["Bash", "Write", "Read", "Edit", "Glob", "LS"]
---

Initialize new project: **$ARGUMENTS**

## 🚀 Project Initialization Process

**Usage**: `/init-project [project-name] [tech-stack] [team-size]`
**Examples**: 
- `/init-project my-ecommerce-app React,Node.js,MongoDB 3`
- `/init-project mobile-app Flutter,Firebase 2`
- `/init-project api-service Python,FastAPI,PostgreSQL 5`

### Phase 1: Project Planning
1. **Parse Arguments**
   - Extract project name (required)
   - Parse technology stack (default: React,Node.js,TypeScript,MongoDB)
   - Determine team size (default: 2, range: 2-7)
   - Validate project name format and availability

2. **Technology Stack Validation**
   - Verify requested technologies are supported
   - Suggest complementary tools and frameworks
   - Identify testing frameworks based on stack
   - Configure build tools and development environment

### Phase 2: Baseline Template Setup
1. **Template Replication**
   - Copy baseline template structure from current directory
   - Remove project-specific content and history
   - Preserve framework structure and configurations
   - Update all references to new project name

2. **Directory Structure Creation**
   ```
   [project-name]/
   ├── .claude/
   │   ├── init.sh                    # Auto-initialization
   │   ├── project.json               # Project metadata
   │   ├── commands/                  # All Phase 1 slash commands
   │   └── templates/                 # Project templates
   ├── ~/.config/claude/              # Preserve global config
   │   ├── profiles/                  # Team member profiles
   │   ├── agents/                    # Agent definitions
   │   └── mcp_settings.json          # MCP configuration
   ├── docs/
   │   ├── architecture/              # System design docs
   │   ├── requirements/              # Project requirements
   │   ├── testing/                   # Testing strategy
   │   └── api/                       # API documentation
   ├── data/sqlite/                   # Project database
   ├── scripts/                       # Build and deployment
   └── [tech-stack-specific structure]
   ```

### Phase 3: Technology-Specific Setup
1. **Frontend Setup** (React/Vue/Angular/Flutter)
   - Initialize frontend framework
   - Configure TypeScript if specified
   - Set up testing framework (Jest/Vitest/Cypress)
   - Configure build tools and bundlers
   - Set up linting and formatting

2. **Backend Setup** (Node.js/Python/Java/Go)
   - Initialize backend framework
   - Configure database connections
   - Set up API framework and routing
   - Configure authentication and security
   - Set up logging and monitoring

3. **Database Setup** (MongoDB/PostgreSQL/MySQL)
   - Initialize database configuration
   - Set up connection strings and pools
   - Configure migrations and seeders
   - Set up development and test databases
   - Configure backup and recovery

### Phase 4: Project Configuration
1. **Project Metadata Creation**
   ```json
   {
     "name": "[project-name]",
     "type": "web-application|mobile-app|api-service|desktop-app",
     "tech_stack": ["React", "Node.js", "TypeScript", "MongoDB"],
     "testing_frameworks": ["Jest", "Playwright", "Cypress"],
     "team_size": 3,
     "created": "2025-08-15T12:00:00Z",
     "mcp_servers": [...],
     "agents": [...],
     "profiles": ["trimabk", "sarthak", ...],
     "git_origin": ""
   }
   ```

2. **Team Configuration**
   - Configure team member profiles based on team size
   - Assign roles and responsibilities
   - Set up epic/sprint/story templates
   - Configure handoff workflows

### Phase 5: Development Environment
1. **Tool Configuration**
   - Set up package.json/requirements.txt/etc.
   - Configure development scripts and commands
   - Set up environment variables and secrets
   - Configure CI/CD pipeline templates
   - Set up code quality tools

2. **MCP Server Integration**
   - Copy MCP server configuration
   - Verify all servers are accessible
   - Test integration with development tools
   - Configure project-specific MCP settings

### Phase 6: Git Repository Setup
1. **Repository Initialization**
   - Initialize git repository
   - Create initial commit with baseline
   - Set up branch protection rules
   - Configure git hooks and automation
   - Create repository on GitHub (if requested)

2. **Branch Strategy Setup**
   - Create main/develop branch structure
   - Set up epic/sprint/story branch patterns
   - Configure merge policies and reviews
   - Set up automated testing on branches

### Phase 7: Documentation Generation
1. **Project Documentation**
   - Generate project-specific README.md
   - Create getting started guide
   - Set up API documentation templates
   - Create development workflow guide
   - Generate team collaboration guide

2. **Architecture Documentation**
   - Create architecture decision records (ADRs)
   - Document technology choices and rationale
   - Set up system design templates
   - Create integration and deployment guides

### Phase 8: Quality Assurance Setup
1. **Testing Framework**
   - Configure unit testing setup
   - Set up integration testing
   - Configure end-to-end testing
   - Set up performance testing
   - Configure security testing

2. **Code Quality Tools**
   - Set up linting and formatting
   - Configure code coverage reporting
   - Set up static analysis tools
   - Configure dependency scanning
   - Set up automated code review

### Phase 9: Deployment Configuration
1. **Environment Setup**
   - Configure development environment
   - Set up staging environment templates
   - Configure production deployment
   - Set up monitoring and logging
   - Configure backup and recovery

2. **DevOps Integration**
   - Set up CI/CD pipeline configuration
   - Configure automated testing and deployment
   - Set up monitoring and alerting
   - Configure infrastructure as code
   - Set up security scanning and compliance

### Phase 10: Project Validation
1. **Setup Verification**
   - Verify all tools and frameworks work
   - Test slash commands functionality
   - Validate profile switching and git config
   - Test epic/sprint/story creation
   - Verify MCP server integration

2. **Team Onboarding**
   - Generate team setup instructions
   - Create development environment guide
   - Set up first epic for project kickoff
   - Configure team communication channels
   - Schedule project initialization meeting

### Expected Deliverables
- [ ] Complete project setup with chosen technology stack
- [ ] All Phase 1 slash commands configured and working
- [ ] Team profiles and git configuration ready
- [ ] Documentation and development guides created
- [ ] Testing and quality assurance tools configured
- [ ] Git repository with initial structure committed
- [ ] Team onboarding materials and workflows ready
- [ ] First epic template created for project kickoff

**Project initialization creates a production-ready development environment with all baseline template benefits adapted to the specific technology stack and team size.**