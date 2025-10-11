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

## Canvas Coordinate System Best Practices

### 🚨 Critical Learnings

#### Canvas API Coordinate Transformation
**Problem**: Canvas doesn't have automatic nested coordinate systems like DOM. All coordinates are global unless you manually manage them.

**Solution**: Use proper Canvas API coordinate transformation:
```javascript
// Parent container rendering
ctx.save();
ctx.translate(parentBounds.x, parentBounds.y);  // Move origin to parent position
ctx.rect(0, 0, parentBounds.width, parentBounds.height);
ctx.clip();  // Create clipping region

// Nested elements now use parent-relative coordinates (0,0 = top-left of parent)
for (const nestedElement of nestedElements) {
    this.renderElement(nestedElement);  // Coordinates are relative to parent
}

ctx.restore();  // Return to global coordinate system
```

#### Container Height Calculation
**Problem**: Fixed spacing calculations don't account for actual margin properties from JSON design.

**Solution**: Calculate height based on actual element properties:
```javascript
calculateContainerHeight(children, containerWidth) {
    const cardPadding = this.tokenResolver.parseDimension('spacing.6');
    const totalPadding = cardPadding * 2; // Top and bottom padding
    let totalHeight = totalPadding;

    for (let i = 0; i < children.length; i++) {
        const child = children[i];
        totalHeight += this.calculateElementHeight(child);

        // Add spacing based on child properties, but not after last element
        if (i < children.length - 1) {
            if (child.properties?.marginBottom) {
                const marginBottom = this.tokenResolver.parseDimension(child.properties.marginBottom);
                totalHeight += marginBottom;
            } else {
                const defaultGap = this.tokenResolver.parseDimension('spacing.4');
                totalHeight += defaultGap;
            }
        }
    }
    return Math.max(totalHeight, 48);
}
```

#### NEVER DO These Things
1. **Never use global coordinates for nested elements** - always transform to parent-relative coordinate system
2. **Never use fixed spacing calculations** - always read actual margin/padding properties from design JSON
3. **Never forget to apply clipping** - without `ctx.clip()`, nested elements can escape parent boundaries
4. **Never forget context state management** - always `ctx.save()` before transformation and `ctx.restore()` after
5. **Never cache-bump only one file** - when fixing coordinate systems, update both LayoutConverter and CanvasRenderer

#### ALWAYS DO These Things
1. **Always use `ctx.save()`/`ctx.restore()`** when applying coordinate transformations
2. **Always read design token values from JSON** instead of hardcoding spacing values
3. **Always calculate container height based on actual content** including margins and gaps
4. **Always apply clipping regions** to constrain nested elements to parent bounds
5. **Always use parent-relative coordinates** (0,0 = top-left of parent) for nested elements
6. **Always update cache-busting versions** when fixing coordinate calculation bugs

### Debugging Canvas Coordinate Issues

#### Symptoms of Coordinate System Problems
- Elements appearing outside their parent containers
- Button or text going beyond rectangle borders
- Elements aligned to screen instead of container
- Inconsistent positioning across different screen sizes

#### Debugging Checklist
1. **Check LayoutConverter**: Are nested elements getting parent-relative coordinates?
2. **Check CanvasRenderer**: Is `ctx.translate()` and `ctx.clip()` applied correctly?
3. **Check Height Calculation**: Is container height calculated based on actual content + margins?
4. **Check Context State**: Are you properly saving/restoring context state?
5. **Check Cache-Busting**: Are you using updated versions of both files?

#### Reference Implementation Pattern
The working implementation demonstrates:
- Proper parent coordinate system with `ctx.translate()`
- Correct container height calculation based on JSON properties
- Proper clipping with `ctx.clip()` to enforce boundaries
- Clean separation between layout calculation and rendering

## Future Development

This repository serves as the foundation for:
- Multi-format design conversion tools
- Component generation systems
- Design token management platforms
- Visual design validation tools

The clean architecture and comprehensive specifications provide a solid base for building sophisticated design system conversion tools.