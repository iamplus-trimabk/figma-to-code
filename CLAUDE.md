# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains the **SimFlo Design Format** - a centralized JSON-based design system specification for converting between multiple design formats and outputs. The project focuses on providing a clean, well-documented specification and reference implementation for design format conversion.

## Core Components

### Design Format Specifications
- **SIMFLO_DESIGN_FORMAT.md** - Main format overview and philosophy
- **SIMFLO_DESIGN_TOKENS_SPEC.md** - Complete design tokens specification
- **SIMFLO_COMPONENTS_SPEC.md** - Component structure and variant definitions
- **SIMFLO_SCREENS_SPEC.md** - Screen layout patterns and composition
- **SIMFLO_LAYOUT_CONVERTER.md** - Layout conversion engine architecture
- **SIMFLO_RENDER_JSON_SPEC.md** - Pixel-perfect rendering instruction format

### Reference Implementation
- **simflo-canvas-renderer.html** - Complete working canvas renderer implementation
- **login-screen-example.json** - Example design following SimFlo format

### Architecture Pipeline
```
Design JSON (semantic) → Layout Converter → Render JSON (pixel-perfect) → Canvas Renderer
```

## Key Features

### Design Format Conversion
- **Input Formats**: Figma JSON, HTML/CSS DOM, React Native, ReactJS/TSX
- **Output Formats**: ReactJS/React Native code, Figma generation, DOM creation, HTML canvas rendering
- **Centralized Schema**: Single JSON format for all design conversions

### Layout System
- **Token Resolution**: Reference-based styling system
- **Flexbox Layout**: Automatic layout calculations
- **Component Variants**: Multiple component states and styles
- **Responsive Design**: Percentage-based sizing and positioning

### Reference Implementation
The canvas renderer demonstrates:
- Clean architecture separation
- Token resolution system
- Layout calculation engine
- Pixel-perfect rendering

## Development Workflow

### Testing the Reference Implementation
```bash
# Serve the canvas renderer locally
npx serve -s . -p 8080

# Open in browser
open http://localhost:8080/simflo-canvas-renderer.html
```

### Validation
- Use the canvas renderer to validate design format specifications
- Test with login-screen-example.json to verify format compliance
- Validate layout calculations and token resolution

## Architecture Principles

### Clean Separation
- **Layout Calculation**: Separate from rendering concerns
- **Token Resolution**: Centralized design token management
- **Component System**: Variant-based component architecture

### Format First
- Specifications drive implementation
- Working examples validate specifications
- Clear documentation for all components

### Extensibility
- Plugin architecture for new input/output formats
- Flexible component variant system
- Scalable token resolution

## File Structure

```
├── SIMFLO_DESIGN_FORMAT.md          # Main format overview
├── SIMFLO_DESIGN_TOKENS_SPEC.md     # Design tokens specification
├── SIMFLO_COMPONENTS_SPEC.md        # Component structure definitions
├── SIMFLO_SCREENS_SPEC.md           # Screen layout patterns
├── SIMFLO_LAYOUT_CONVERTER.md       # Layout conversion engine
├── SIMFLO_RENDER_JSON_SPEC.md       # Rendering instruction format
├── simflo-canvas-renderer.html      # Reference implementation
├── login-screen-example.json        # Example design format
└── README.md                        # Project overview
```

## Quality Standards

### Documentation
- Clear, comprehensive specifications
- Working examples for all concepts
- Consistent formatting and terminology

### Implementation
- Clean architecture with separation of concerns
- Type-safe interfaces and definitions
- Comprehensive error handling

### Testing
- Reference implementation validates specifications
- Real-world examples demonstrate functionality
- Visual verification of output quality

## Future Development

This repository serves as the foundation for:
- Multi-format design conversion tools
- Component generation systems
- Design token management platforms
- Visual design validation tools

The clean architecture and comprehensive specifications provide a solid base for building sophisticated design system conversion tools.