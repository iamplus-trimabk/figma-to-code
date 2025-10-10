# SimFlo Layout Converter Engine

## 🎯 Purpose
Converts high-level Design JSON to pixel-perfect Render JSON by calculating absolute positions, resolving design tokens, and handling flexbox layout logic.

## 🏗️ Architecture Position
```
Design JSON (semantic) → Layout Converter → Render JSON (pixel-perfect) → Canvas Renderer (draw)
```

## 🔄 Conversion Pipeline

### Input: Design JSON
- Component-based, semantic structure
- Design token references (`colors.primary`)
- Relative positioning and layout constraints
- Flexbox-like layout system

### Output: Render JSON
- Absolute pixel coordinates
- Pre-resolved colors, fonts, sizes
- Simple drawing instructions
- No layout calculations needed

## 🧮 Layout Calculation Engine

### 1. Token Resolution
```javascript
class TokenResolver {
  constructor(designTokens, theme = 'light') {
    this.tokens = designTokens;
    this.theme = theme;
    this.cache = new Map();
  }

  resolve(tokenPath) {
    // Resolve token paths like "colors.primary", "fontSize.base"
    // Handle responsive values "16px | 18px"
    // Cache resolved values for performance
  }

  parseDimension(value) {
    // Convert "16px", "spacing.4", "100%" to pixel values
    // Handle percentage calculations relative to parent
  }
}
```

### 2. Flexbox Layout Engine
```javascript
class FlexboxLayoutEngine {
  calculateLayout(container, children) {
    const {
      direction = 'column',
      justifyContent = 'flex-start',
      alignItems = 'flex-start',
      gap = 0,
      padding = 0
    } = container.layout;

    // 1. Calculate container bounds
    const containerBounds = this.calculateContainerBounds(container);

    // 2. Resolve padding
    const paddingResolved = this.resolvePadding(padding);

    // 3. Calculate children layout
    const childLayouts = this.layoutChildren(
      children,
      containerBounds,
      paddingResolved,
      { direction, justifyContent, alignItems, gap }
    );

    return { containerBounds, childLayouts };
  }

  layoutChildren(children, containerBounds, padding, layoutProps) {
    const { direction, justifyContent, alignItems, gap } = layoutProps;

    // Calculate available space
    const availableWidth = containerBounds.width - padding.left - padding.right;
    const availableHeight = containerBounds.height - padding.top - padding.bottom;

    // Measure children dimensions
    const measuredChildren = children.map(child => ({
      ...child,
      measuredSize: this.measureChild(child, direction === 'row' ? availableWidth : availableHeight)
    }));

    // Calculate main axis positioning
    const mainAxisLayout = this.calculateMainAxis(
      measuredChildren,
      direction === 'row' ? availableWidth : availableHeight,
      justifyContent,
      gap
    );

    // Calculate cross axis positioning
    const crossAxisLayout = this.calculateCrossAxis(
      measuredChildren,
      direction === 'row' ? availableHeight : availableWidth,
      alignItems
    );

    // Convert to absolute positions
    return this.convertToAbsolutePositions(
      measuredChildren,
      mainAxisLayout,
      crossAxisLayout,
      containerBounds,
      padding,
      direction
    );
  }
}
```

### 3. Component Layout Calculator
```javascript
class ComponentLayoutCalculator {
  calculateComponentLayout(component, parentBounds, variant = null) {
    // 1. Get component definition
    const componentDef = this.getComponentDefinition(component.name);

    // 2. Apply variant styles
    const styles = this.applyVariant(componentDef, variant);

    // 3. Calculate dimensions
    const dimensions = this.calculateDimensions(component, componentDef, parentBounds);

    // 4. Calculate position within parent
    const position = this.calculatePosition(component, componentDef, parentBounds, dimensions);

    // 5. Calculate content layout
    const contentLayout = this.calculateContentLayout(component, componentDef, dimensions);

    return {
      bounds: { ...position, ...dimensions },
      styles: this.resolveStyles(styles),
      content: contentLayout
    };
  }

  calculateDimensions(component, componentDef, parentBounds) {
    const layout = { ...componentDef.layout, ...component.layout };

    let width = this.resolveDimension(layout.width, parentBounds.width);
    let height = this.resolveDimension(layout.height, parentBounds.height);

    // Apply constraints
    width = this.applyConstraints(width, layout.minWidth, layout.maxWidth, parentBounds.width);
    height = this.applyConstraints(height, layout.minHeight, layout.maxHeight, parentBounds.height);

    return { width, height };
  }

  calculatePosition(component, componentDef, parentBounds, dimensions) {
    const layout = { ...componentDef.layout, ...component.layout };
    const { justifyContent = 'flex-start', alignItems = 'flex-start' } = layout;

    let x = parentBounds.x;
    let y = parentBounds.y;

    // Handle main axis positioning
    switch (justifyContent) {
      case 'center':
        if (layout.direction === 'row') {
          x = parentBounds.x + (parentBounds.width - dimensions.width) / 2;
        } else {
          y = parentBounds.y + (parentBounds.height - dimensions.height) / 2;
        }
        break;
      case 'flex-end':
        if (layout.direction === 'row') {
          x = parentBounds.x + parentBounds.width - dimensions.width;
        } else {
          y = parentBounds.y + parentBounds.height - dimensions.height;
        }
        break;
    }

    // Add margins
    const margin = this.resolveMargin(layout.margin);
    x += margin.left;
    y += margin.top;

    return { x, y };
  }
}
```

## 🎯 Conversion Process

### Step 1: Screen Layout Calculation
```javascript
convertScreen(screen, viewport, tokenResolver) {
  // 1. Calculate screen bounds
  const screenBounds = {
    x: 0,
    y: 0,
    width: viewport.width,
    height: viewport.height
  };

  // 2. Apply screen styles
  const backgroundElement = this.createBackgroundElement(screen, screenBounds);

  // 3. Layout screen children
  const childElements = this.layoutChildren(screen.children, screenBounds, tokenResolver);

  return {
    version: "1.0.0",
    viewport,
    metadata: {
      screenName: screen.name,
      theme: tokenResolver.theme,
      generatedAt: new Date().toISOString()
    },
    elements: [backgroundElement, ...childElements]
  };
}
```

### Step 2: Component Element Conversion
```javascript
convertComponent(component, parentBounds, tokenResolver) {
  // 1. Get component definition
  const componentDef = this.getComponentDefinition(component.name);

  // 2. Apply variant
  const variant = component.variant || 'default';
  const variantStyles = this.getVariantStyles(componentDef, variant);

  // 3. Calculate layout
  const layout = this.calculateComponentLayout(component, parentBounds, variant);

  // 4. Resolve styles to pixel values
  const resolvedStyles = this.resolveStylesToPixels(layout.styles, tokenResolver);

  // 5. Convert content
  const content = this.convertContent(layout.content, layout.bounds, tokenResolver);

  // 6. Create render elements
  const elements = this.createRenderElements(component.name, layout.bounds, resolvedStyles, content);

  return elements;
}
```

### Step 3: Content Conversion
```javascript
convertContent(content, parentBounds, tokenResolver) {
  switch (content.type) {
    case 'text':
      return this.convertTextContent(content, parentBounds, tokenResolver);

    case 'input':
      return this.convertInputContent(content, parentBounds, tokenResolver);

    case 'image':
      return this.convertImageContent(content, parentBounds, tokenResolver);

    case 'container':
      return this.convertContainerContent(content, parentBounds, tokenResolver);

    default:
      return null;
  }
}

convertTextContent(content, parentBounds, tokenResolver) {
  return {
    type: 'text',
    bounds: parentBounds,
    styles: {
      color: tokenResolver.resolve(content.properties.color || 'colors.text.primary'),
      fontFamily: tokenResolver.resolve('fontFamily.primary'),
      fontSize: tokenResolver.parseDimension(content.properties.fontSize || 'fontSize.base'),
      fontWeight: tokenResolver.resolve(content.properties.fontWeight || 'fontWeight.normal'),
      textAlign: content.properties.align || 'left',
      lineHeight: tokenResolver.resolve(content.properties.lineHeight || 'lineHeight.normal')
    },
    content: {
      type: 'text',
      properties: {
        text: content.properties.value || '',
        maxLines: content.properties.maxLines || 1
      }
    }
  };
}

convertInputContent(content, parentBounds, tokenResolver) {
  return {
    type: 'input-field',
    bounds: parentBounds,
    styles: {
      backgroundColor: tokenResolver.resolve('colors.background.primary'),
      borderColor: tokenResolver.resolve('colors.border.medium'),
      borderWidth: 1,
      borderRadius: tokenResolver.parseDimension('borderRadius.md')
    },
    content: {
      type: 'text',
      properties: {
        placeholder: content.properties.placeholder || '',
        placeholderColor: tokenResolver.resolve('colors.text.tertiary'),
        fontFamily: tokenResolver.resolve('fontFamily.primary'),
        fontSize: tokenResolver.parseDimension('fontSize.base'),
        textAlign: 'left'
      }
    }
  };
}
```

### Step 4: Element Creation
```javascript
createRenderElements(componentName, bounds, styles, content) {
  const elements = [];

  // Create background/shape element
  const shapeElement = this.createShapeElement(componentName, bounds, styles);
  elements.push(shapeElement);

  // Create content element if exists
  if (content) {
    const contentElement = this.createContentElement(content, bounds, styles);
    if (contentElement) {
      elements.push(contentElement);
    }
  }

  return elements;
}

createShapeElement(componentName, bounds, styles) {
  const elementType = this.determineElementType(componentName, styles);

  return {
    id: this.generateId(componentName, 'background'),
    type: elementType,
    bounds,
    styles: {
      backgroundColor: styles.backgroundColor,
      borderColor: styles.borderColor,
      borderWidth: styles.borderWidth,
      borderRadius: styles.borderRadius,
      shadowColor: styles.shadowColor,
      shadowOffsetX: styles.shadowOffsetX,
      shadowOffsetY: styles.shadowOffsetY,
      shadowBlur: styles.shadowBlur,
      opacity: styles.opacity || 1
    }
  };
}

determineElementType(componentName, styles) {
  if (componentName === 'Button') return 'button';
  if (componentName === 'Input') return 'input-field';
  if (styles.borderRadius > 0) return 'rounded-rectangle';
  return 'rectangle';
}
```

## 🎯 Layout Features Supported

### 1. Flexbox Layout
- **Direction**: row, column
- **Justify Content**: flex-start, center, flex-end, space-between, space-around
- **Align Items**: flex-start, center, flex-end, stretch
- **Gap**: Uniform spacing between children

### 2. Sizing and Positioning
- **Width/Height**: pixels, percentages, auto
- **Min/Max Constraints**: min-width, max-width, min-height, max-height
- **Margins and Padding**: token-based or pixel values
- **Absolute Positioning**: within parent containers

### 3. Responsive Behavior
- **Token Resolution**: handles responsive token values
- **Viewport Scaling**: maintains aspect ratios
- **Content Adaptation**: text wrapping, scaling

### 4. Component Variants
- **Style Overrides**: variant-specific styles
- **Layout Variations**: different layouts per variant
- **Content Changes**: variant content differences

## 🧪 Conversion Validation

### Input Validation
- Component definitions exist
- Token references are valid
- Layout constraints are solvable
- No circular dependencies

### Output Validation
- All elements have valid bounds
- Styles are resolved to pixel values
- No overlapping elements (unless intended)
- Layout fits within viewport

### Error Handling
- Missing components: create fallback elements
- Invalid tokens: use default values
- Layout conflicts: apply reasonable defaults
- Overflow: handle gracefully with clipping or scrolling

---

*This layout converter provides the bridge between high-level design intent and pixel-perfect rendering instructions, enabling complex layouts while maintaining clean separation of concerns.*