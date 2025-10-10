# SimFlo Canvas Renderer - Design & Implementation

## 🎯 Purpose
Defines the approach for rendering SimFlo JSON format to HTML Canvas for visual validation.

## 🏗️ Canvas Rendering Strategy

### Why Canvas is Superior for Validation
- **Deterministic Output**: Same JSON = exact same visual result
- **Pixel-Perfect Control**: No CSS browser variations or quirks
- **Complete Format Validation**: Every JSON property must be explicitly implemented
- **Immediate Visual Feedback**: Errors in JSON format are immediately visible
- **Platform Independence**: Canvas behavior is consistent across all browsers

### Rendering Pipeline
```
SimFlo JSON → Token Resolution → Layout Calculation → Canvas Drawing → Visual Output
```

## 📐 Viewport & Scaling

### Fixed Reference Viewport
- **iPhone 12**: 390px × 844px (standard mobile reference)
- **Device Pixel Ratio**: 2x (retina displays)
- **Canvas Size**: 780px × 1688px (for crisp rendering)
- **CSS Display Size**: 390px × 844px

### Responsive Scaling
```javascript
// Scale factor for different screen sizes
function getScaleFactor(targetWidth, targetHeight) {
  const baseWidth = 390;
  const baseHeight = 844;
  const scaleX = targetWidth / baseWidth;
  const scaleY = targetHeight / baseHeight;
  return Math.min(scaleX, scaleY); // Maintain aspect ratio
}

// Apply scaling to canvas
function scaleCanvas(canvas, scaleFactor) {
  canvas.style.width = `${390 * scaleFactor}px`;
  canvas.style.height = `${844 * scaleFactor}px`;
}
```

## 🎨 Rendering Architecture

### 1. Token Resolver
```javascript
class TokenResolver {
  constructor(designTokens) {
    this.tokens = designTokens;
    this.cache = new Map();
  }

  resolve(tokenPath, theme = 'light') {
    // Check cache first
    const cacheKey = `${tokenPath}-${theme}`;
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    // Resolve token path (e.g., "colors.primary")
    const value = this.getNestedValue(this.tokens, tokenPath);

    // Handle responsive values (e.g., "16px | 20px")
    const resolvedValue = this.parseResponsiveValue(value, theme);

    // Cache and return
    this.cache.set(cacheKey, resolvedValue);
    return resolvedValue;
  }

  parseResponsiveValue(value, theme) {
    if (typeof value === 'string' && value.includes('|')) {
      const [light, dark] = value.split('|').map(v => v.trim());
      return theme === 'dark' ? dark : light;
    }
    return value;
  }

  toCanvasValue(tokenPath, context = {}) {
    const value = this.resolve(tokenPath, context.theme);

    // Convert for canvas usage
    if (tokenPath.includes('spacing') || tokenPath.includes('sizing')) {
      return parseFloat(value) * (context.scale || 1);
    }

    return value;
  }
}
```

### 2. Layout Engine
```javascript
class LayoutEngine {
  constructor(tokenResolver) {
    this.tokenResolver = tokenResolver;
  }

  calculateBounds(element, parentBounds) {
    const layout = element.layout || {};
    const styles = element.styles || {};

    // Resolve width/height
    let width = this.resolveDimension(layout.width, parentBounds.width);
    let height = this.resolveDimension(layout.height, parentBounds.height);

    // Apply min/max constraints
    width = this.applyConstraints(width, layout.minWidth, layout.maxWidth, parentBounds.width);
    height = this.applyConstraints(height, layout.minHeight, layout.maxHeight, parentBounds.height);

    // Resolve position
    const position = this.resolvePosition(layout, parentBounds, width, height);

    // Resolve padding and margin
    const padding = this.resolveBoxModel(layout.padding, parentBounds.width);
    const margin = this.resolveBoxModel(layout.margin, parentBounds.width);

    return {
      x: position.x + margin.left,
      y: position.y + margin.top,
      width: width - margin.left - margin.right,
      height: height - margin.top - margin.bottom,
      padding,
      margin
    };
  }

  resolveDimension(value, parentDimension) {
    if (!value) return parentDimension;

    if (typeof value === 'string' && value.includes('%')) {
      const percentage = parseFloat(value) / 100;
      return parentDimension * percentage;
    }

    return this.tokenResolver.toCanvasValue(value, { scale: 1 });
  }

  resolvePosition(layout, parentBounds, elementWidth, elementHeight) {
    const { justifyContent = 'flex-start', alignItems = 'flex-start' } = layout;

    let x = parentBounds.x;
    let y = parentBounds.y;

    // Horizontal alignment
    switch (justifyContent) {
      case 'center':
        x = parentBounds.x + (parentBounds.width - elementWidth) / 2;
        break;
      case 'flex-end':
        x = parentBounds.x + parentBounds.width - elementWidth;
        break;
      case 'space-between':
        // Handle for multiple children
        break;
    }

    // Vertical alignment
    switch (alignItems) {
      case 'center':
        y = parentBounds.y + (parentBounds.height - elementHeight) / 2;
        break;
      case 'flex-end':
        y = parentBounds.y + parentBounds.height - elementHeight;
        break;
    }

    return { x, y };
  }
}
```

### 3. Canvas Renderer
```javascript
class CanvasRenderer {
  constructor(canvas, tokenResolver) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.tokenResolver = tokenResolver;
    this.layoutEngine = new LayoutEngine(tokenResolver);

    // Set up high-DPI support
    this.setupHighDPI();
  }

  setupHighDPI() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();

    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;

    this.ctx.scale(dpr, dpr);
    this.canvas.style.width = rect.width + 'px';
    this.canvas.style.height = rect.height + 'px';
  }

  render(screen, viewport = { width: 390, height: 844 }) {
    // Clear canvas
    this.ctx.clearRect(0, 0, viewport.width, viewport.height);

    // Apply background
    this.renderBackground(screen, viewport);

    // Render screen children
    if (screen.children) {
      this.renderChildren(screen.children, viewport, screen);
    }
  }

  renderBackground(screen, viewport) {
    const backgroundColor = this.tokenResolver.resolve(
      screen.styles?.backgroundColor || 'colors.background.secondary'
    );

    this.ctx.fillStyle = backgroundColor;
    this.ctx.fillRect(0, 0, viewport.width, viewport.height);
  }

  renderChildren(children, parentBounds, parent) {
    children.forEach((child, index) => {
      this.renderElement(child, parentBounds, parent, index);
    });
  }

  renderElement(element, parentBounds, parent, index) {
    // Skip if element is not visible
    if (element.styles?.opacity === 0) return;

    // Calculate element bounds
    const bounds = this.layoutEngine.calculateBounds(element, parentBounds);

    // Save context state
    this.ctx.save();

    // Apply styles
    this.applyStyles(element, bounds);

    // Render based on type
    switch (element.type) {
      case 'component':
        this.renderComponent(element, bounds);
        break;
      case 'text':
        this.renderText(element, bounds);
        break;
      case 'input':
        this.renderInput(element, bounds);
        break;
      case 'image':
        this.renderImage(element, bounds);
        break;
      case 'container':
        this.renderContainer(element, bounds);
        break;
    }

    // Restore context state
    this.ctx.restore();
  }

  applyStyles(element, bounds) {
    const styles = element.styles || {};

    // Background
    if (styles.backgroundColor) {
      const bgColor = this.tokenResolver.resolve(styles.backgroundColor);
      this.ctx.fillStyle = bgColor;
      this.ctx.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);
    }

    // Border
    if (styles.borderColor && styles.borderWidth) {
      const borderColor = this.tokenResolver.resolve(styles.borderColor);
      const borderWidth = this.tokenResolver.toCanvasValue(styles.borderWidth);

      this.ctx.strokeStyle = borderColor;
      this.ctx.lineWidth = borderWidth;
      this.ctx.strokeRect(bounds.x, bounds.y, bounds.width, bounds.height);
    }

    // Border Radius
    if (styles.borderRadius) {
      const radius = this.tokenResolver.toCanvasValue(styles.borderRadius);
      this.drawRoundedRect(bounds.x, bounds.y, bounds.width, bounds.height, radius);
    }

    // Shadow
    if (styles.shadow) {
      const shadow = this.tokenResolver.resolve(styles.shadow);
      this.applyShadow(shadow);
    }

    // Opacity
    if (styles.opacity !== undefined) {
      this.ctx.globalAlpha = styles.opacity;
    }
  }

  renderText(element, bounds) {
    const props = element.properties || {};
    const text = props.value || '';

    if (!text) return;

    // Set text styles
    this.ctx.fillStyle = this.tokenResolver.resolve(props.color || 'colors.text.primary');
    this.ctx.font = this.getFontString(props);
    this.ctx.textAlign = props.align || 'left';
    this.ctx.textBaseline = 'top';

    // Calculate text position
    const textX = this.getTextX(bounds, props.align);
    const textY = bounds.y + bounds.padding.top;

    // Handle text wrapping
    const lines = this.wrapText(text, bounds.width - bounds.padding.left - bounds.padding.right);
    lines.forEach((line, index) => {
      this.ctx.fillText(line, textX, textY + (index * this.getLineHeight(props)));
    });
  }

  renderComponent(element, bounds) {
    // Get component definition from registry
    const componentDef = this.getComponentDefinition(element.name);
    if (!componentDef) return;

    // Apply component layout and styles
    const mergedElement = this.mergeWithComponentDefinition(element, componentDef);

    // Render component content
    if (mergedElement.content) {
      this.renderElement(mergedElement.content, bounds, mergedElement, 0);
    }

    // Render component children
    if (mergedElement.children) {
      this.renderChildren(mergedElement.children, bounds, mergedElement);
    }
  }

  renderInput(element, bounds) {
    const props = element.properties || {};

    // Draw input background
    this.ctx.fillStyle = this.tokenResolver.resolve('colors.background.primary');
    this.ctx.fillRect(bounds.x, bounds.y, bounds.width, bounds.height);

    // Draw border
    this.ctx.strokeStyle = this.tokenResolver.resolve('colors.border.medium');
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(bounds.x, bounds.y, bounds.width, bounds.height);

    // Draw placeholder text if no value
    if (!props.value && props.placeholder) {
      this.ctx.fillStyle = this.tokenResolver.resolve('colors.text.tertiary');
      this.ctx.font = this.getFontString({ fontSize: 'fontSize.base' });
      this.ctx.textAlign = 'left';
      this.ctx.textBaseline = 'middle';
      this.ctx.fillText(props.placeholder, bounds.x + bounds.padding.left, bounds.y + bounds.height / 2);
    }
  }

  renderContainer(element, bounds) {
    // Container is mainly for layout, just render children
    if (element.children) {
      this.renderChildren(element.children, bounds, element);
    }
  }

  // Helper methods
  getFontString(props) {
    const fontSize = this.tokenResolver.toCanvasValue(props.fontSize || 'fontSize.base');
    const fontWeight = this.tokenResolver.resolve(props.fontWeight || 'fontWeight.normal');
    const fontFamily = this.tokenResolver.resolve('fontFamily.primary');
    return `${fontWeight} ${fontSize}px ${fontFamily}`;
  }

  getTextX(bounds, align) {
    switch (align) {
      case 'center':
        return bounds.x + bounds.width / 2;
      case 'right':
        return bounds.x + bounds.width - bounds.padding.right;
      default:
        return bounds.x + bounds.padding.left;
    }
  }

  wrapText(text, maxWidth) {
    const words = text.split(' ');
    const lines = [];
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
      const word = words[i];
      const width = this.ctx.measureText(currentLine + ' ' + word).width;

      if (width < maxWidth) {
        currentLine += ' ' + word;
      } else {
        lines.push(currentLine);
        currentLine = word;
      }
    }

    lines.push(currentLine);
    return lines;
  }

  getLineHeight(props) {
    const fontSize = this.tokenResolver.toCanvasValue(props.fontSize || 'fontSize.base');
    const lineHeight = this.tokenResolver.resolve(props.lineHeight || 'lineHeight.normal');
    return fontSize * parseFloat(lineHeight);
  }

  drawRoundedRect(x, y, width, height, radius) {
    this.ctx.beginPath();
    this.ctx.moveTo(x + radius, y);
    this.ctx.lineTo(x + width - radius, y);
    this.ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    this.ctx.lineTo(x + width, y + height - radius);
    this.ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    this.ctx.lineTo(x + radius, y + height);
    this.ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    this.ctx.lineTo(x, y + radius);
    this.ctx.quadraticCurveTo(x, y, x + radius, y);
    this.ctx.closePath();
    this.ctx.fill();
  }

  applyShadow(shadowString) {
    // Parse shadow string like "0 4px 6px rgba(0, 0, 0, 0.1)"
    const parts = shadowString.match(/(-?\d+px)\s+(-?\d+px)\s+(-?\d+px)\s+(.+)/);
    if (parts) {
      this.ctx.shadowOffsetX = parseInt(parts[1]);
      this.ctx.shadowOffsetY = parseInt(parts[2]);
      this.ctx.shadowBlur = parseInt(parts[3]);
      this.ctx.shadowColor = parts[4];
    }
  }
}
```

## 🎯 Implementation Steps

### Step 1: Core Infrastructure
1. **Token Resolver** - Parse and resolve design token references
2. **Layout Engine** - Calculate bounds and positioning
3. **Base Canvas Renderer** - Set up canvas and basic rendering

### Step 2: Component Rendering
1. **Text Rendering** - Typography, alignment, wrapping
2. **Input Fields** - Form inputs with placeholders
3. **Containers** - Layout containers with children
4. **Component System** - Reusable component instances

### Step 3: Visual Polish
1. **Borders & Shadows** - Visual styling
2. **Border Radius** - Rounded corners
3. **Backgrounds** - Colors and gradients
4. **Opacity & Blending** - Visual effects

### Step 4: Testing & Validation
1. **Example Screens** - Test with sample JSON
2. **Responsive Scaling** - Test different viewport sizes
3. **Error Handling** - Graceful degradation
4. **Performance** - Optimization for complex screens

## 🧪 Validation Strategy

### What Canvas Rendering Validates
- **JSON Schema Compliance** - All required properties must exist
- **Token Resolution** - All token references must be valid
- **Layout Logic** - Positioning and sizing calculations
- **Component Structure** - Component definitions and variants
- **Visual Fidelity** - Does the output match expectations?

### Error Detection
- **Missing Tokens** - Undefined token references
- **Invalid Layout** - Overlapping elements, overflow issues
- **Missing Components** - Undefined component references
- **Syntax Errors** - Malformed JSON or property values

### Success Criteria
- **Clean Render** - No console errors or warnings
- **Visual Accuracy** - Output matches design expectations
- **Responsive Behavior** - Scales correctly at different sizes
- **Performance** - Renders in acceptable time

---

*This canvas renderer provides the most reliable validation method for the SimFlo JSON format, ensuring that every aspect of the format is properly implemented and tested.*