# SimFlo Components Specification V1.0

## 🎯 Purpose
Defines the structure and behavior of reusable UI components in the SimFlo format.

## 📋 Component Structure

### Basic Component Definition
```json
{
  "components": {
    "ComponentName": {
      "type": "component",
      "category": "forms | display | navigation | layout",
      "layout": {
        "type": "auto-layout | stack | grid",
        "direction": "row | column",
        "width": "percentage | auto | fit-content",
        "height": "percentage | auto | fit-content",
        "minWidth": "percentage | pixel",
        "maxWidth": "percentage | pixel",
        "minHeight": "percentage | pixel",
        "maxHeight": "percentage | pixel",
        "padding": "token-reference | pixel-value",
        "margin": "token-reference | pixel-value",
        "gap": "token-reference | pixel-value"
      },
      "styles": {
        "backgroundColor": "token-reference",
        "borderColor": "token-reference",
        "borderWidth": "token-reference",
        "borderRadius": "token-reference",
        "shadow": "token-reference",
        "opacity": "0-1"
      },
      "variants": [
        {
          "name": "variant-name",
          "styles": { /* variant-specific styles */ },
          "layout": { /* variant-specific layout */ }
        }
      ],
      "content": {
        "type": "text | input | image | icon | component | container",
        "properties": {
          /* content-specific properties */
        }
      },
      "children": [
        /* nested components if needed */
      ],
      "interactions": {
        "clickable": true | false,
        "disabled": true | false,
        "hoverable": true | false
      }
    }
  }
}
```

## 🎨 Component Categories

### 1. Form Components
#### Input Field
```json
{
  "Input": {
    "type": "component",
    "category": "forms",
    "layout": {
      "type": "auto-layout",
      "width": "100%",
      "height": "48px",
      "padding": { "horizontal": "spacing.4", "vertical": "spacing.3" }
    },
    "styles": {
      "backgroundColor": "colors.background.primary",
      "borderColor": "colors.border.medium",
      "borderWidth": "1px",
      "borderRadius": "borderRadius.md",
      "fontSize": "fontSize.base"
    },
    "variants": [
      {
        "name": "default",
        "styles": {
          "borderColor": "colors.border.medium"
        }
      },
      {
        "name": "focus",
        "styles": {
          "borderColor": "colors.border.focus",
          "shadow": "shadows.sm"
        }
      },
      {
        "name": "error",
        "styles": {
          "borderColor": "colors.error"
        }
      }
    ],
    "content": {
      "type": "input",
      "properties": {
        "placeholder": "Enter text...",
        "value": "",
        "type": "text | email | password"
      }
    }
  }
}
```

#### Button
```json
{
  "Button": {
    "type": "component",
    "category": "navigation",
    "layout": {
      "type": "auto-layout",
      "width": "auto",
      "height": "48px",
      "padding": { "horizontal": "spacing.6", "vertical": "spacing.3" },
      "justifyContent": "center",
      "alignItems": "center"
    },
    "styles": {
      "borderRadius": "borderRadius.md",
      "fontSize": "fontSize.base",
      "fontWeight": "fontWeight.medium",
      "cursor": "pointer"
    },
    "variants": [
      {
        "name": "primary",
        "styles": {
          "backgroundColor": "colors.primary",
          "color": "colors.text.inverse"
        }
      },
      {
        "name": "secondary",
        "styles": {
          "backgroundColor": "colors.background.tertiary",
          "color": "colors.text.primary",
          "borderColor": "colors.border.medium",
          "borderWidth": "1px"
        }
      },
      {
        "name": "ghost",
        "styles": {
          "backgroundColor": "transparent",
          "color": "colors.text.primary"
        }
      }
    ],
    "content": {
      "type": "text",
      "properties": {
        "value": "Button Text",
        "align": "center"
      }
    },
    "interactions": {
      "clickable": true,
      "hoverable": true
    }
  }
}
```

### 2. Display Components
#### Card
```json
{
  "Card": {
    "type": "component",
    "category": "display",
    "layout": {
      "type": "auto-layout",
      "direction": "column",
      "width": "100%",
      "padding": "spacing.6",
      "gap": "spacing.4"
    },
    "styles": {
      "backgroundColor": "colors.background.primary",
      "borderRadius": "borderRadius.lg",
      "shadow": "shadows.md"
    },
    "variants": [
      {
        "name": "default",
        "styles": {
          "shadow": "shadows.md"
        }
      },
      {
        "name": "elevated",
        "styles": {
          "shadow": "shadows.lg"
        }
      },
      {
        "name": "bordered",
        "styles": {
          "borderColor": "colors.border.light",
          "borderWidth": "1px",
          "shadow": "none"
        }
      }
    ],
    "content": {
      "type": "container",
      "children": [
        {
          "type": "text",
          "properties": {
            "value": "Card Title",
            "fontSize": "fontSize.lg",
            "fontWeight": "fontWeight.semibold"
          }
        },
        {
          "type": "text",
          "properties": {
            "value": "Card description text goes here.",
            "fontSize": "fontSize.sm",
            "color": "colors.text.secondary"
          }
        }
      ]
    }
  }
}
```

#### Badge
```json
{
  "Badge": {
    "type": "component",
    "category": "display",
    "layout": {
      "type": "auto-layout",
      "width": "fit-content",
      "height": "24px",
      "padding": { "horizontal": "spacing.2", "vertical": "spacing.1" },
      "justifyContent": "center",
      "alignItems": "center"
    },
    "styles": {
      "borderRadius": "borderRadius.full",
      "fontSize": "fontSize.xs",
      "fontWeight": "fontWeight.medium"
    },
    "variants": [
      {
        "name": "success",
        "styles": {
          "backgroundColor": "colors.success",
          "color": "colors.text.inverse"
        }
      },
      {
        "name": "warning",
        "styles": {
          "backgroundColor": "colors.warning",
          "color": "colors.text.inverse"
        }
      },
      {
        "name": "error",
        "styles": {
          "backgroundColor": "colors.error",
          "color": "colors.text.inverse"
        }
      }
    ],
    "content": {
      "type": "text",
      "properties": {
        "value": "Badge",
        "align": "center"
      }
    }
  }
}
```

### 3. Layout Components
#### Container
```json
{
  "Container": {
    "type": "component",
    "category": "layout",
    "layout": {
      "type": "auto-layout",
      "direction": "column",
      "width": "100%",
      "height": "auto"
    },
    "styles": {},
    "variants": [
      {
        "name": "center",
        "layout": {
          "justifyContent": "center",
          "alignItems": "center"
        }
      },
      {
        "name": "start",
        "layout": {
          "justifyContent": "flex-start",
          "alignItems": "flex-start"
        }
      },
      {
        "name": "between",
        "layout": {
          "justifyContent": "space-between",
          "alignItems": "center"
        }
      }
    ],
    "content": {
      "type": "container",
      "children": []
    }
  }
}
```

#### Stack
```json
{
  "Stack": {
    "type": "component",
    "category": "layout",
    "layout": {
      "type": "stack",
      "direction": "column | row",
      "width": "100%",
      "height": "auto",
      "gap": "spacing.4"
    },
    "styles": {},
    "variants": [
      {
        "name": "vertical",
        "layout": {
          "direction": "column"
        }
      },
      {
        "name": "horizontal",
        "layout": {
          "direction": "row"
        }
      },
      {
        "name": "wrap",
        "layout": {
          "direction": "row",
          "flexWrap": "wrap"
        }
      }
    ],
    "content": {
      "type": "container",
      "children": []
    }
  }
}
```

## 🔧 Content Types

### 1. Text Content
```json
{
  "type": "text",
  "properties": {
    "value": "Text content",
    "fontSize": "token-reference",
    "fontWeight": "token-reference",
    "color": "token-reference",
    "align": "left | center | right",
    "lineHeight": "token-reference",
    "letterSpacing": "token-reference",
    "maxLines": "number"
  }
}
```

### 2. Input Content
```json
{
  "type": "input",
  "properties": {
    "placeholder": "Placeholder text",
    "value": "Current value",
    "type": "text | email | password | number",
    "maxLength": "number",
    "required": true | false
  }
}
```

### 3. Image Content
```json
{
  "type": "image",
  "properties": {
    "src": "image-url or base64",
    "alt": "Alternative text",
    "fit": "cover | contain | fill",
    "width": "percentage | pixel",
    "height": "percentage | pixel"
  }
}
```

### 4. Icon Content
```json
{
  "type": "icon",
  "properties": {
    "name": "icon-name",
    "size": "token-reference",
    "color": "token-reference"
  }
}
```

### 5. Component Content
```json
{
  "type": "component",
  "name": "ComponentName",
  "variant": "variant-name",
  "properties": {
    "component-specific": "properties"
  }
}
```

### 6. Container Content
```json
{
  "type": "container",
  "layout": {
    "layout-configuration"
  },
  "children": [
    "array of child components"
  ]
}
```

## 🎯 Layout System Details

### Auto-Layout
```json
{
  "type": "auto-layout",
  "direction": "row | column",
  "wrap": "nowrap | wrap",
  "justifyContent": "flex-start | flex-end | center | space-between | space-around | space-evenly",
  "alignItems": "flex-start | flex-end | center | stretch | baseline",
  "alignContent": "flex-start | flex-end | center | stretch | space-between | space-around"
}
```

### Stack Layout
```json
{
  "type": "stack",
  "direction": "column | row",
  "gap": "spacing-value"
}
```

### Grid Layout
```json
{
  "type": "grid",
  "columns": "number | repeat(auto-fit, minmax(min, max))",
  "rows": "number | auto",
  "gap": "spacing-value"
}
```

## 🔄 Responsive Behavior

### Responsive Layout
```json
{
  "layout": {
    "width": "100% | 80%",
    "direction": "column | row",
    "responsive": {
      "tablet": {
        "width": "80% | 60%",
        "direction": "row"
      },
      "desktop": {
        "width": "60% | 50%",
        "direction": "row"
      }
    }
  }
}
```

### Responsive Styles
```json
{
  "styles": {
    "fontSize": "fontSize.base | fontSize.lg",
    "padding": "spacing.4 | spacing.6",
    "responsive": {
      "tablet": {
        "fontSize": "fontSize.lg",
        "padding": "spacing.6"
      },
      "desktop": {
        "fontSize": "fontSize.xl",
        "padding": "spacing.8"
      }
    }
  }
}
```

## 🎨 Component Composition

### Nested Components
```json
{
  "components": {
    "ComplexCard": {
      "type": "component",
      "category": "display",
      "layout": {
        "type": "auto-layout",
        "direction": "column",
        "gap": "spacing.4"
      },
      "content": {
        "type": "container",
        "children": [
          {
            "type": "component",
            "name": "Badge",
            "variant": "success"
          },
          {
            "type": "text",
            "properties": {
              "value": "Card Title",
              "fontSize": "fontSize.lg"
            }
          },
          {
            "type": "component",
            "name": "Input",
            "properties": {
              "placeholder": "Enter value"
            }
          },
          {
            "type": "component",
            "name": "Button",
            "variant": "primary",
            "properties": {
              "value": "Submit"
            }
          }
        ]
      }
    }
  }
}
```

## 📋 Implementation Guidelines

### 1. Component Naming
- Use PascalCase for component names
- Be descriptive and consistent
- Group related components together

### 2. Variant System
- Each variant should be visually distinct
- Variants inherit base styles and override
- Use semantic names (primary, secondary, ghost)

### 3. Layout Consistency
- All components use same layout system
- Percentage-based sizing for responsiveness
- Consistent spacing using design tokens

### 4. Content Flexibility
- Components should work with different content types
- Support both direct content and nested components
- Handle content overflow gracefully

---

*This spec provides a comprehensive component system that can represent most common UI patterns while maintaining consistency and flexibility.*