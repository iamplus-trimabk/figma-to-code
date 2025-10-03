# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Unified UI** is a sophisticated component library providing unified APIs for Web (React) development with JSON-driven components and shadcn/ui integration. The project focuses on creating reusable, type-safe components that follow consistent architectural patterns.

**Current Project State**: Active implementation phase with mature JSON-based component architecture, standardized hook patterns, and comprehensive development workflows.

**Current Development Focus**: Building JSON-driven components using established patterns, maintaining type safety, and ensuring consistent developer experience across all components.

## Architecture

### Component Architecture
The project follows a JSON-driven component architecture with standardized patterns:

1. **JSON Configuration Layer** - Components configured via JSON with type-safe interfaces
2. **Hook Layer** - Data loading and state management using `StandardHookReturn<T, Actions>` pattern
3. **Context Layer** - React contexts that delegate completely to hooks
4. **Component Layer** - Self-contained components using context for data and actions
5. **shadcn/ui Foundation** - Read-only component library treated as dependency

### Key Principles
- **JSON-Driven**: All components configured through JSON with TypeScript interfaces
- **Standardized Patterns**: Consistent `StandardHookReturn<T, Actions>` across all hooks
- **Self-Contained**: Components manage their own state and loading/error handling
- **Type Safety**: Strict TypeScript with comprehensive interfaces

## Development Commands

### Core Development Workflow
```bash
# Required before any development
npm run lint:all          # Type checking + linting

# Development server (web platform)
npm run dev              # Starts on port 5173 with demo application

# Build commands
npm run build            # Web platform build
npm run clean             # Clean build artifacts
```

### shadcn/ui Management
```bash
# Install shadcn components (READ-ONLY - treated like node_modules)
python install_shadcn.py --components
python install_shadcn.py --hooks
python install_shadcn.py --blocks
python install_shadcn.py --all

# Install with automatic package dependency management
python install_shadcn.py --all --install-packages
```

### Quality Assurance
```bash
npm run check:no-js        # Enforce TypeScript-only sources
npm run lint:all          # Type checking + linting (must pass before commits)
```

## Code Structure & Architecture

### Directory Organization
```
src/
├── iamplus/                    # 🚦 CUSTOM COMPONENT DEVELOPMENT (MODIFY HERE)
│   ├── components/             # JSON-driven components
│   │   ├── nav-user.tsx       # Example JSON component
│   │   ├── dynamic-app-sidebar.tsx
│   │   └── dashboard/         # Dashboard-specific components
│   ├── hooks/                 # Data loading hooks
│   │   ├── use-standard-hook.tsx
│   │   ├── use-nav-user-data.tsx
│   │   └── use-base-context.tsx
│   ├── contexts/              # React context providers
│   │   ├── navigation-context.tsx
│   │   └── nav-user-context.tsx
│   ├── types/                 # TypeScript interfaces
│   │   ├── prop-interfaces.ts
│   │   ├── nav-user-types.ts
│   │   └── entity-types.ts
│   └── lib/                   # Utilities and error handling
│       ├── error-utils.ts
│       └── navigation-service.ts
└── shadcn/                    # 🔒 READ-ONLY (MANAGED BY install_shadcn.py)
    ├── components/            # shadcn/ui components (29 installed)
    ├── hooks/                 # shadcn/ui hooks
    ├── blocks/                # shadcn/ui blocks
    └── lib/                   # shadcn/ui utilities
```

### Namespace Rules (CRITICAL)
🚦 **ONLY MODIFY CODE IN `src/iamplus/`**
- `@iamplus/*` - Custom company components (built in-house)
- `@shadcn/*` - Third-party shadcn components (read-only, like node_modules)

🚫 **FORBIDDEN IMPORTS**:
```typescript
// ❌ BANNED - No ambiguous aliases
import { Something } from "@/components/something"
import { Something } from "@/lib/utils"

// ❌ BANNED - No relative imports in component files
import { Something } from "./something"
```

✅ **ALLOWED IMPORTS**:
```typescript
// ✅ Custom company components
import { NavUser } from "@iamplus/components/nav-user"
import { useNavUserData } from "@iamplus/hooks/use-nav-user-data"

// ✅ Third-party shadcn components (read-only)
import { Button } from "@shadcn/components/button"
import { Card } from "@shadcn/components/card"
```

### TypeScript Configuration
- `tsconfig.json` - Main TypeScript configuration
- Path aliases defined for proper namespace separation

## JSON-Component Development

### 🚨 MANDATORY: Read These Guides First
**Before working on any JSON-based component, you MUST read:**
1. **[JSON-COMPONENT-DEVELOPMENT-GUIDE.md](./JSON-COMPONENT-DEVELOPMENT-GUIDE.md)** - Complete architectural blueprint
2. **[JSON-COMPONENT-TEMPLATE.md](./JSON-COMPONENT-TEMPLATE.md)** - Ready-to-use templates
3. **[JSON-COMPONENT-EXAMPLE.md](./JSON-COMPONENT-EXAMPLE.md)** - Complete working example

### Standard Hook Pattern (MANDATORY)
All hooks MUST follow the `StandardHookReturn<T, Actions>` pattern:
```typescript
export interface StandardHookReturn<T, Actions extends Record<string, any>> {
  data: T | null
  loading: boolean
  error: string | null
  refresh: () => void
  actions: Actions
}
```

### Component Architecture Pattern
```typescript
// 1. Hook loads JSON data and provides actions
const { data, loading, error, actions } = useComponentData(config)

// 2. Context delegates to hook completely
export function ComponentProvider({ children, ...config }) {
  const hookReturn = useComponentData(config)
  return <ComponentContext.Provider value={hookReturn}>
    {children}
  </ComponentContext.Provider>
}

// 3. Component uses context for data and actions
export function JsonComponent() {
  const { data, loading, error, actions } = useComponent()

  if (loading) return <LoadingState />
  if (error) return <ErrorState error={error} onRetry={actions.refresh} />

  return <ComponentUI data={data} actions={actions} />
}
```

### JSON Configuration Structure
All JSON components follow this configuration pattern:
```json
{
  "id": "component-id",
  "type": "data-table",
  "version": "1.0.0",
  "jsonUrl": "/api/v1/data.json",
  "refreshInterval": 30000,
  "enableAutoRefresh": true,
  "filters": [...],
  "display": {...}
}
```

## Development Workflow

### Standard Development Process
For direct development without agents:
1. **Run Quality Checks**: `npm run lint:all` (must pass before commits)
2. **Start Development Server**: `npm run dev` (port 5173)
3. **Read JSON Component Guides**: Mandatory before any component work
4. **Follow Established Patterns**: Use `StandardHookReturn<T, Actions>` pattern
5. **Implement Components**: Work only in `src/iamplus/` directory

### Quality Standards
- **Strict TypeScript**: No `any` types, comprehensive interfaces
- **TypeScript Only**: No JavaScript files (enforced by `check:no-js`)
- **Standard Patterns**: All hooks must follow `StandardHookReturn<T, Actions>`
- **Error Handling**: Use `standardizeError` from `@iamplus/lib/error-utils`
- **Self-Contained**: Components manage own loading/error/empty states

### Critical Development Rules

#### 🚦 ONLY WORK IN `src/iamplus/`
- ✅ **Modify**: `src/iamplus/components/`, `src/iamplus/hooks/`, `src/iamplus/contexts/`, `src/iamplus/types/`, `src/iamplus/lib/`
- 🔒 **READ-ONLY**: `src/shadcn/` (managed by `install_shadcn.py`)

#### Namespace Enforcement
- ✅ **Use**: `@iamplus/*` for custom components
- ✅ **Use**: `@shadcn/*` for shadcn components
- ❌ **Forbidden**: `@/components/*`, `@/lib/*`, relative imports

#### Component Development Standards
1. **Read Guides First**: Always read JSON component guides before starting
2. **Follow Patterns**: Use established `StandardHookReturn<T, Actions>` pattern
3. **Type Safety**: Comprehensive TypeScript interfaces
4. **Error Handling**: Proper error states with retry functionality
5. **Loading States**: Meaningful loading indicators
6. **Self-Contained**: Components should work without external props

## Demo Application

### Location: `demo/src/App.tsx`
Active demonstration of JSON-based components:
- **JSON Components**: Live examples of `nav-user`, dynamic components
- **shadcn Integration**: Proper usage of read-only shadcn components
- **Theme Switching**: Light/dark themes with brand colors
- **Real Development**: Shows actual working patterns, not mockups

## Quick Reference

### Essential Commands
```bash
# Development (run in this order)
npm run lint:all          # Type checking + linting (must pass)
npm run dev              # Start dev server on port 5173

# shadcn Management (when adding new components)
python install_shadcn.py --all --install-packages
```

### Component Development Checklist
- [ ] Read JSON-COMPONENT-DEVELOPMENT-GUIDE.md
- [ ] Follow StandardHookReturn<T, Actions> pattern
- [ ] Work only in src/iamplus/ directory
- [ ] Use proper @iamplus/* imports
- [ ] Handle loading/error/empty states
- [ ] Ensure TypeScript compilation
- [ ] Test component functionality

### Common Issues & Solutions
- **Build Issues**: Run `npm run lint:all` first
- **Import Errors**: Check namespace rules (@iamplus/* vs @shadcn/*)
- **Component Issues**: Verify JSON configuration is correct
- **Type Errors**: Ensure all interfaces are properly defined

## Architecture Summary

This project implements a **JSON-driven component architecture** with:
- **Standardized Patterns**: Consistent hook and context patterns
- **Type Safety**: Comprehensive TypeScript interfaces
- **Self-Contained Components**: Components manage their own state
- **Read-Only Dependencies**: shadcn components managed via installation script
- **Quality Focus**: Strict linting, type checking, and established patterns

The architecture prioritizes **developer experience** and **consistency** over complex abstractions, focusing on what works for the current implementation rather than theoretical future capabilities.