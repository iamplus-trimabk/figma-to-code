# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Stage 3 Component Generator** - a sophisticated Figma-driven component generation system that creates production-ready React components through a hybrid approach of prompt-driven precision and template-based automation. The project transforms Figma designs into fully functional, responsive React components using Next.js, TypeScript, and Tailwind CSS.

**Current Development State**: The project has successfully implemented Phase 2 template system and is currently in Stage 3 implementation, focusing on responsive layout generation and component integration.

## Architecture

### Component Generation Pipeline
The project follows a multi-stage architecture:

1. **Stage 1**: Manual component pattern establishment and design token integration
2. **Stage 2**: Automated template system using Jinja2 for batch component generation from Figma interfaces
3. **Stage 3**: Hybrid approach combining prompt-driven precision for complex components with template-based automation for scale

### Core System Components
- **Figma Asset Extractor**: Extracts design assets, layouts, and component definitions from Figma API
- **Design System Converter**: Transforms Figma designs to Stage 2 interfaces with comprehensive component metadata
- **Template Engine**: Jinja2-based system for automated component generation
- **Page Assembler**: Layout parsing engine for assembling complete responsive pages from Figma screen layouts
- **Component Registry**: Manages component categorization and registration (navigation, forms, display categories)

### Component Architecture
Generated components follow consistent patterns:
- **JSON-driven configuration** via Stage 2 interfaces
- **Class Variance Authority (CVA)** for variant management
- **TypeScript interfaces** extending React HTML attributes
- **Figma design properties** integration (width, height, position, backgroundColor, etc.)
- **Responsive design** with absolute positioning converted to flexbox/grid layouts

## Development Commands

### Core Development Workflow
```bash
# Start development server
npm run dev              # Next.js dev server on http://localhost:3000

# Build and deployment
npm run build            # Production build
npm run start            # Start production server
npm run lint             # ESLint checking
```

### Component Generation (Template System)
```bash
# Generate components using automated template system
python3 templates/scripts/component_generator.py --stage2 stage_2_outputs --templates templates --output . --component [ComponentName]

# Examples:
python3 templates/scripts/component_generator.py --stage2 stage_2_outputs --templates templates --output . --component Button
python3 templates/scripts/component_generator.py --stage2 stage_2_outputs --templates templates --output . --component Email
python3 templates/scripts/component_generator.py --stage2 stage_2_outputs --templates templates --output . --component Bg
```

### Design Asset Processing
```bash
# Extract design assets from Figma
python3 design_asset_extractor/extract_assets.py

# Convert designs to Stage 2 interfaces
python3 design_system_converter/convert_designs.py

# Analyze Figma data for component patterns
python3 analyze_figma_data.py
```

### Testing and Validation
```bash
# Test template system functionality
python3 test-template-system.py

# Test design asset extraction
python3 test_design_asset_extractor.py

# Validate generated components
python3 test_stage_2_conversion.py
```

## Code Structure & Architecture

### Directory Organization
```
├── src/
│   ├── app/                    # Next.js app router pages
│   │   ├── button-test/       # Component testing pages
│   │   ├── card-test/
│   │   ├── alert-test/
│   │   ├── input-test/
│   │   ├── login/             # Login page with Figma-generated components
│   │   ├── components/        # Component showcase page
│   │   └── layout.tsx         # Root layout
│   ├── components/            # Generated React components
│   │   ├── display/           # Card, Alert, etc.
│   │   ├── forms/             # Input, Password, Search, etc.
│   │   ├── navigation/        # Button components
│   │   └── email.tsx          # Generated from Figma Email interface
│   └── lib/
│       └── page-assembler/    # Layout assembly engine
│           ├── page-assembler.tsx    # Main page assembly logic
│           ├── layout-parser.tsx     # Figma layout parsing
│           ├── component-registry.tsx # Component registration
│           └── types.ts              # TypeScript definitions
├── templates/                 # Jinja2 template system
│   ├── components/
│   │   └── component.j2       # Main component template
│   ├── partials/              # Template partials
│   │   ├── variants.j2
│   │   ├── component-props.j2
│   │   └── component-render.j2
│   └── scripts/
│       └── component_generator.py    # Template generation script
├── design_asset_extractor/    # Figma API integration
├── design_system_converter/   # Design-to-interface conversion
├── stage_2_outputs/          # Generated component interfaces
├── extracted_login_assets_api/ # Figma design data
└── figma_cache/              # Cached Figma API responses
```

### Component Categories
The system automatically categorizes components based on their functionality:
- **navigation**: Button, links, navigation elements
- **forms**: Input, Password, Search, form controls
- **display**: Card, Alert, display components

### Stage 2 Interface Pattern
Components generated from Stage 2 interfaces include Figma design properties:
```typescript
export interface ComponentProps extends React.HTMLAttributes<HTMLElement> {
  // Figma design properties
  width?: string | number
  height?: string | number
  position?: { x?: number; y?: number }
  backgroundColor?: string
  backgroundOpacity?: number
  borderRadius?: string | number
  display?: "block" | "inline" | "flex" | "grid" | "none"
  overflow?: "visible" | "hidden" | "scroll" | "auto"
  style?: React.CSSProperties
  testId?: string
  // Component-specific props
  [key: string]: any
}
```

## Development Workflow

### Figma Integration Setup
1. **Configure Environment**: Copy `.env.example` to `.env` and add Figma credentials
2. **Set API Access**: Add `FILE_KEY` and `ACCESS_TOKEN` for Figma API access
3. **Cache Management**: Figma responses cached in `figma_cache/` directory

### Component Development Process
1. **Design Extraction**: Extract assets from Figma using design asset extractor
2. **Interface Generation**: Convert designs to Stage 2 interfaces
3. **Component Generation**: Use template system or prompt-driven approach
4. **Layout Integration**: Assemble components into pages using page assembler
5. **Responsive Design**: Convert absolute positioning to responsive layouts

### Template System Usage
The template system uses established patterns from Phase 1:
- **Jinja2 Templates**: Modular template system with partials
- **Component Categorization**: Automatic pattern application based on component type
- **Design Token Integration**: Consistent styling across generated components
- **TypeScript Generation**: Complete interface definitions with React attribute extensions

### Page Assembly System
The page assembler converts Figma screen layouts to responsive React pages:
- **Layout Parser**: Parses Figma screen layouts from JSON
- **Component Registry**: Maps component types to React implementations
- **Responsive Conversion**: Transforms absolute positioning to flexbox/grid
- **Style Integration**: Maintains Figma design properties in responsive format

## Figma Configuration

### Required Environment Variables
```bash
# Figma API Configuration
FILE_KEY=your_figma_file_key_here
ACCESS_TOKEN=figd_your_personal_access_token_here
PROJECT_NAME=your_project_name_here

# Optional Configuration
BASE_URL=https://api.figma.com/v1
CACHE_TTL=3000
CACHE_DIR=figma_cache
```

### Design Asset Structure
Figma designs are extracted and converted to:
- **Component Interfaces**: TypeScript definitions in `stage_2_outputs/`
- **Screen Layouts**: JSON layout definitions in `extracted_login_assets_api/`
- **Design Tokens**: Color, typography, spacing definitions
- **Component Catalog**: Complete component metadata

## Quality Standards

### Component Requirements
- **TypeScript Strict Mode**: All components must use strict TypeScript
- **Responsive Design**: Components must work across screen sizes
- **Accessibility**: Proper ARIA attributes and keyboard navigation
- **Figma Compliance**: Maintain visual fidelity to original designs
- **Stage 2 Interface**: Include all Figma design properties

### Code Organization
- **Component Categorization**: Proper placement in navigation/forms/display directories
- **Interface Extensions**: Extend React HTML attributes and Stage 2 interfaces
- **Variant Systems**: Use Class Variance Authority for component variants
- **Style Integration**: Combine Tailwind classes with inline styles for Figma properties

## Testing and Validation

### Component Testing
Each component has dedicated test pages:
- `/button-test` - Button component variants and functionality
- `/card-test` - Card component layouts and interactions
- `/alert-test` - Alert component states and variations
- `/input-test` - Input component validation and states
- `/login` - Complete page using Figma-generated components

### Template System Testing
```bash
# Validate template generation with specific components
python3 test-template-system.py

# Test individual component generation
python3 templates/scripts/component_generator.py --stage2 stage_2_outputs --templates templates --output . --component [ComponentName]
```

## Development Best Practices

### Working with Figma Components
1. **Always use Stage 2 interfaces** for component props definition
2. **Maintain responsive design** by converting absolute positioning
3. **Preserve design properties** like width, height, backgroundColor
4. **Use proper TypeScript interfaces** extending React attributes
5. **Test component variations** across different screen sizes

### Template System Usage
1. **Component categorization** ensures correct pattern application
2. **Template fixes** benefit all future components
3. **Design token integration** maintains consistency
4. **Automated generation** reduces manual errors

### Page Assembly
1. **Layout parsing** converts Figma layouts to React components
2. **Responsive conversion** ensures mobile compatibility
3. **Component registration** maps types to implementations
4. **Style preservation** maintains design fidelity

## Architecture Summary

This project implements a **Figma-driven component generation architecture** with:
- **Hybrid Generation Strategy**: Combining prompt-driven precision with template automation
- **Design System Integration**: Direct Figma-to-component conversion with design properties
- **Responsive Layout System**: Automatic conversion of absolute positioning to responsive design
- **Template-Based Automation**: Jinja2 templates for consistent component generation
- **Complete Type Safety**: Comprehensive TypeScript interfaces with Stage 2 compliance

The architecture prioritizes **design fidelity**, **developer productivity**, and **responsive design** over manual component creation, focusing on automated generation from Figma designs while maintaining production-ready quality standards.