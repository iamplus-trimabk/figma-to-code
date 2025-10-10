# SimFlo Design Format

A centralized JSON-based design system specification for converting between multiple design formats and outputs.

## Overview

The SimFlo Design Format provides a unified schema for design system conversion, supporting:

- **Input Formats**: Figma JSON, HTML/CSS DOM, React Native, ReactJS/TSX
- **Output Formats**: ReactJS/React Native code, Figma generation, DOM creation, HTML canvas rendering

## Architecture

```
Design JSON (semantic) ’ Layout Converter ’ Render JSON (pixel-perfect) ’ Canvas Renderer
```

## Files

### Specifications
- `SIMFLO_DESIGN_FORMAT.md` - Main format overview and philosophy
- `SIMFLO_DESIGN_TOKENS_SPEC.md` - Design tokens specification
- `SIMFLO_COMPONENTS_SPEC.md` - Component structure definitions
- `SIMFLO_SCREENS_SPEC.md` - Screen layout patterns
- `SIMFLO_LAYOUT_CONVERTER.md` - Layout conversion engine
- `SIMFLO_RENDER_JSON_SPEC.md` - Rendering instruction format

### Reference Implementation
- `simflo-canvas-renderer.html` - Working canvas renderer demo
- `login-screen-example.json` - Example design format

## Quick Start

1. View the specifications to understand the format
2. Test the reference implementation:
   ```bash
   npx serve -s . -p 8080
   open http://localhost:8080/simflo-canvas-renderer.html
   ```

## Features

- Clean architecture separation
- Token resolution system
- Component variant support
- Responsive design capabilities
- Pixel-perfect rendering