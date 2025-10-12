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

## Multi-Device Platform Switching Best Practices

### 🚨 Critical Learnings

#### Race Condition Prevention in Device Switching
**Problem**: When switching screens that require different platforms (e.g., Dashboard needs desktop), multiple render calls execute simultaneously, causing component artifacts from previous screens.

**Solution**: Implement async device switching with proper state management:
```javascript
async autoSwitchDeviceForScreen(designJson, screenName) {
    const screen = designJson.screens[screenName];
    if (!screen?.platform) return;

    // Map platform to device
    const targetDevice = screen.platform === 'desktop' ? 'desktop' :
                        screen.platform === 'tablet' ? 'tablet' : 'mobile';

    if (targetDevice !== this.state.currentDevice) {
        // Wait for existing device switching if in progress
        if (this.state.isDeviceSwitching && this.state.deviceSwitchPromise) {
            await this.state.deviceSwitchPromise;
        }

        // Perform async device switch
        await this.setDeviceAsync(targetDevice);
    }
}

async setDeviceAsync(device) {
    const switchPromise = new Promise((resolve) => {
        // Update UI and state
        this.updateDeviceUI(device);
        this.state.update({ currentDevice: device });

        // Wait for CSS transitions
        setTimeout(() => {
            this.state.update({ isDeviceSwitching: false, deviceSwitchPromise: null });
            resolve();
        }, 100);
    });

    this.state.update({ isDeviceSwitching: true, deviceSwitchPromise: switchPromise });
    return switchPromise;
}
```

#### Canvas Container Sizing for Different Devices
**Problem**: Desktop frames (1440x900) don't fit properly in containers designed for mobile layouts, causing tiny canvas rendering.

**Solution**: Implement responsive container sizing with CSS classes:
```css
/* Default mobile container */
.canvas-container {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    padding: 32px;
}

/* Desktop mode needs more space */
.canvas-container.desktop-mode {
    padding: 16px;
}

/* Allow device frame to scale down if needed but maintain aspect ratio */
.device-frame.desktop {
    max-width: calc(100vw - var(--sidebar-width) - var(--right-panel-width) - 32px);
    max-height: calc(100vh - var(--header-height) - 32px);
    width: var(--desktop-width);
    height: var(--desktop-height);
}
```

#### JavaScript Class Management
```javascript
setDevice(device, shouldReload = true) {
    // Update device frame
    const deviceFrame = this.components.deviceFrame;
    deviceFrame.className = `device-frame ${device} ${this.state.currentOrientation}`;

    // Update canvas container for desktop mode
    const canvasContainer = this.components.canvasWrapper;
    if (device === 'desktop') {
        canvasContainer.classList.add('desktop-mode');
    } else {
        canvasContainer.classList.remove('desktop-mode');
    }

    // Update state and reload
    this.state.update({ currentDevice: device });
    if (shouldReload) {
        setTimeout(() => this.loadScreen(this.state.currentScreen), 50);
    }
}
```

#### Token Resolution Error Handling
**Problem**: Undefined token paths cause `TypeError: undefined is not an object (evaluating 'tokenPath.split')`.

**Solution**: Add input validation in token resolver:
```javascript
resolve(tokenPath) {
    // Handle undefined or null token paths
    if (!tokenPath) {
        console.warn('Token path is undefined or null, returning fallback value');
        return '16px'; // Default fallback value
    }

    // Check cache first
    if (this.cache.has(tokenPath)) {
        return this.cache.get(tokenPath);
    }

    const resolved = this.resolveTokenPath(tokenPath);
    this.cache.set(tokenPath, resolved);
    return resolved;
}

resolveTokenPath(tokenPath) {
    // Additional safety check
    if (!tokenPath) {
        console.warn('Token path is undefined in resolveTokenPath, returning fallback');
        return '16px';
    }

    const parts = tokenPath.split('.');
    // ... rest of resolution logic
}
```

#### Enhanced Canvas Rendering Validation
**Problem**: Canvas rendering fails silently when dimensions are invalid or JSON structure is malformed.

**Solution**: Add comprehensive validation:
```javascript
async renderToCanvas(renderJson) {
    // Enhanced dimension validation
    const containerRect = canvas.parentElement.getBoundingClientRect();
    if (containerRect.width <= 0 || containerRect.height <= 0) {
        throw new Error(`Container too small: ${containerRect.width}x${containerRect.height}`);
    }

    // Validate render JSON and viewport
    if (!renderJson || !renderJson.viewport) {
        throw new Error('Invalid render JSON: missing viewport information');
    }

    const designWidth = renderJson.viewport.width;
    const designHeight = renderJson.viewport.height;
    if (designWidth <= 0 || designHeight <= 0) {
        throw new Error(`Invalid design viewport: ${designWidth}x${designHeight}`);
    }

    // ... continue with rendering
}
```

#### NEVER DO These Things
1. **Never allow concurrent device switches** - always prevent race conditions with proper state management
2. **Never use fixed container padding** - adapt padding based on device requirements (16px for desktop vs 32px for mobile)
3. **Never ignore undefined token paths** - always validate inputs and provide sensible fallbacks
4. **Never skip JSON structure validation** - always validate render JSON before processing
5. **Never use synchronous device switching** - always wait for transitions to complete before rendering

#### ALWAYS DO These Things
1. **Always use async device switching** with Promise-based state management
2. **Always add CSS classes dynamically** based on device type (desktop-mode, mobile-mode, etc.)
3. **Always validate token paths** before attempting to split or process them
4. **Always implement comprehensive dimension validation** before canvas rendering
5. **Always use cache-busting version updates** when fixing race conditions or device switching logic
6. **Always update both JavaScript and CSS** when fixing device-specific rendering issues
7. **Always provide fallback values** for undefined or invalid design tokens

### Debugging Multi-Device Issues

#### Symptoms of Device Switching Problems
- Components from previous screen persist after switching
- Canvas appears tiny in desktop mode
- JavaScript errors with undefined token paths
- Invalid container dimension errors
- Race conditions between concurrent render calls

#### Debugging Checklist
1. **Check Race Conditions**: Are device switches properly serialized with async/await?
2. **Check Container CSS**: Does desktop mode have appropriate container sizing?
3. **Check Token Resolution**: Are undefined token paths handled gracefully?
4. **Check Canvas Validation**: Are dimensions and JSON structure validated before rendering?
5. **Check CSS Classes**: Are device-specific classes (desktop-mode) being applied correctly?

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