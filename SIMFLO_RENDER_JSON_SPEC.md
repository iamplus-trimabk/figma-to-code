# SimFlo Render JSON Specification V1.0

## 🎯 Purpose
Defines the pixel-perfect drawing instruction format for the SimFlo rendering pipeline. This format contains absolute coordinates and pre-resolved values - no layout calculations needed.

## 🏗️ Architecture Position
```
Design JSON (semantic) → Layout Converter → Render JSON (pixel-perfect) → Canvas Renderer (draw)
```

## 📋 Render JSON Structure

### Root Schema
```json
{
  "version": "1.0.0",
  "viewport": {
    "width": 390,
    "height": 844,
    "scale": 1.0
  },
  "metadata": {
    "screenName": "Login",
    "theme": "light",
    "generatedAt": "2024-01-15T10:30:00Z"
  },
  "elements": [
    {
      "id": "element-uuid",
      "type": "rectangle | text | rounded-rectangle | image",
      "bounds": {
        "x": 45,
        "y": 280,
        "width": 300,
        "height": 48
      },
      "styles": {
        "backgroundColor": "#ffffff",
        "borderColor": "#d1d5db",
        "borderWidth": 1,
        "borderRadius": 8,
        "shadowColor": "rgba(0, 0, 0, 0.1)",
        "shadowOffsetX": 0,
        "shadowOffsetY": 4,
        "shadowBlur": 6,
        "opacity": 1.0
      },
      "content": {
        "type": "text | image | none",
        "properties": {
          /* Content-specific properties */
        }
      }
    }
  ]
}
```

## 🎨 Element Types

### 1. Rectangle (Simple Background)
```json
{
  "type": "rectangle",
  "bounds": {
    "x": 0,
    "y": 0,
    "width": 390,
    "height": 844
  },
  "styles": {
    "backgroundColor": "#f9fafb"
  }
}
```

### 2. Rounded Rectangle (Cards, Buttons)
```json
{
  "type": "rounded-rectangle",
  "bounds": {
    "x": 45,
    "y": 280,
    "width": 300,
    "height": 48
  },
  "styles": {
    "backgroundColor": "#6257db",
    "borderRadius": 8,
    "shadowColor": "rgba(0, 0, 0, 0.1)",
    "shadowOffsetX": 0,
    "shadowOffsetY": 4,
    "shadowBlur": 6
  }
}
```

### 3. Text Element
```json
{
  "type": "text",
  "bounds": {
    "x": 45,
    "y": 150,
    "width": 300,
    "height": 30
  },
  "styles": {
    "color": "#111827",
    "fontFamily": "Inter, system-ui, sans-serif",
    "fontSize": 24,
    "fontWeight": "700",
    "textAlign": "center",
    "lineHeight": 1.2
  },
  "content": {
    "type": "text",
    "properties": {
      "text": "Welcome Back",
      "maxLines": 1
    }
  }
}
```

### 4. Input Field (Background + Text + Border)
```json
{
  "type": "input-field",
  "bounds": {
    "x": 45,
    "y": 200,
    "width": 300,
    "height": 48
  },
  "styles": {
    "backgroundColor": "#ffffff",
    "borderColor": "#d1d5db",
    "borderWidth": 1,
    "borderRadius": 8
  },
  "content": {
    "type": "text",
    "properties": {
      "text": "",
      "placeholder": "Email address",
      "placeholderColor": "#6b7280",
      "fontFamily": "Inter, system-ui, sans-serif",
      "fontSize": 16,
      "textAlign": "left"
    }
  }
}
```

### 5. Button Element
```json
{
  "type": "button",
  "bounds": {
    "x": 45,
    "y": 350,
    "width": 300,
    "height": 48
  },
  "styles": {
    "backgroundColor": "#6257db",
    "borderRadius": 8,
    "shadowColor": "rgba(0, 0, 0, 0.1)",
    "shadowOffsetX": 0,
    "shadowOffsetY": 4,
    "shadowBlur": 6
  },
  "content": {
    "type": "text",
    "properties": {
      "text": "Sign In",
      "color": "#ffffff",
      "fontFamily": "Inter, system-ui, sans-serif",
      "fontSize": 16,
      "fontWeight": "500",
      "textAlign": "center"
    }
  }
}
```

### 6. Image Element
```json
{
  "type": "image",
  "bounds": {
    "x": 45,
    "y": 100,
    "width": 80,
    "height": 80
  },
  "styles": {
    "borderRadius": 40,
    "fit": "cover"
  },
  "content": {
    "type": "image",
    "properties": {
      "src": "data:image/png;base64,...",
      "alt": "User avatar"
    }
  }
}
```

## 📐 Bounds System

### Absolute Positioning
All elements use absolute pixel coordinates:
- **x**: Horizontal position from left edge (px)
- **y**: Vertical position from top edge (px)
- **width**: Element width (px)
- **height**: Element height (px)

### No Layout Math in Renderer
The renderer should never calculate positions - only draw at specified coordinates.

### Text Bounds
Text bounds define the **text container area**:
- Text is positioned within these bounds
- `textAlign` determines horizontal positioning within bounds
- Vertical positioning is handled by the renderer (centered vertically)

## 🎨 Style Properties

### Colors
- **backgroundColor**: Hex color string (`#ffffff`)
- **borderColor**: Hex color string (`#d1d5db`)
- **color**: Text color (`#111827`)
- **shadowColor**: RGBA string (`rgba(0, 0, 0, 0.1)`)

### Typography
- **fontFamily**: Complete font stack (`"Inter, system-ui, sans-serif"`)
- **fontSize**: Pixel value (`16`)
- **fontWeight**: Numeric weight (`400 | 500 | 700`)
- **textAlign**: `left | center | right`
- **lineHeight**: Multiplier (`1.2 | 1.5`)

### Layout
- **borderRadius**: Pixel radius (`8`)
- **borderWidth**: Pixel width (`1`)
- **opacity**: Alpha value (`0.0 - 1.0`)

### Shadows
- **shadowOffsetX**: Horizontal offset (`0`)
- **shadowOffsetY**: Vertical offset (`4`)
- **shadowBlur**: Blur radius (`6`)

## 🔄 Content System

### Text Content
```json
{
  "type": "text",
  "properties": {
    "text": "Actual text content",
    "placeholder": "Placeholder text (for inputs)",
    "placeholderColor": "#6b7280",
    "maxLines": 1
  }
}
```

### Image Content
```json
{
  "type": "image",
  "properties": {
    "src": "data:image/png;base64,... or URL",
    "alt": "Alternative text",
    "fit": "cover | contain | fill"
  }
}
```

## 📱 Complete Example: Login Screen

```json
{
  "version": "1.0.0",
  "viewport": {
    "width": 390,
    "height": 844,
    "scale": 1.0
  },
  "metadata": {
    "screenName": "Login",
    "theme": "light",
    "generatedAt": "2024-01-15T10:30:00Z"
  },
  "elements": [
    {
      "id": "background",
      "type": "rectangle",
      "bounds": { "x": 0, "y": 0, "width": 390, "height": 844 },
      "styles": { "backgroundColor": "#f9fafb" }
    },
    {
      "id": "card-background",
      "type": "rounded-rectangle",
      "bounds": { "x": 45, "y": 100, "width": 300, "height": 400 },
      "styles": {
        "backgroundColor": "#ffffff",
        "borderRadius": 12,
        "shadowColor": "rgba(0, 0, 0, 0.1)",
        "shadowOffsetX": 0,
        "shadowOffsetY": 4,
        "shadowBlur": 6
      }
    },
    {
      "id": "title",
      "type": "text",
      "bounds": { "x": 45, "y": 130, "width": 300, "height": 30 },
      "styles": {
        "color": "#111827",
        "fontFamily": "Inter, system-ui, sans-serif",
        "fontSize": 24,
        "fontWeight": "700",
        "textAlign": "center"
      },
      "content": {
        "type": "text",
        "properties": { "text": "Welcome Back" }
      }
    },
    {
      "id": "email-input",
      "type": "input-field",
      "bounds": { "x": 45, "y": 200, "width": 300, "height": 48 },
      "styles": {
        "backgroundColor": "#ffffff",
        "borderColor": "#d1d5db",
        "borderWidth": 1,
        "borderRadius": 8
      },
      "content": {
        "type": "text",
        "properties": {
          "placeholder": "Email address",
          "placeholderColor": "#6b7280",
          "fontFamily": "Inter, system-ui, sans-serif",
          "fontSize": 16
        }
      }
    },
    {
      "id": "password-input",
      "type": "input-field",
      "bounds": { "x": 45, "y": 264, "width": 300, "height": 48 },
      "styles": {
        "backgroundColor": "#ffffff",
        "borderColor": "#d1d5db",
        "borderWidth": 1,
        "borderRadius": 8
      },
      "content": {
        "type": "text",
        "properties": {
          "placeholder": "Password",
          "placeholderColor": "#6b7280",
          "fontFamily": "Inter, system-ui, sans-serif",
          "fontSize": 16
        }
      }
    },
    {
      "id": "login-button",
      "type": "button",
      "bounds": { "x": 45, "y": 332, "width": 300, "height": 48 },
      "styles": {
        "backgroundColor": "#6257db",
        "borderRadius": 8,
        "shadowColor": "rgba(0, 0, 0, 0.1)",
        "shadowOffsetX": 0,
        "shadowOffsetY": 4,
        "shadowBlur": 6
      },
      "content": {
        "type": "text",
        "properties": {
          "text": "Sign In",
          "color": "#ffffff",
          "fontFamily": "Inter, system-ui, sans-serif",
          "fontSize": 16,
          "fontWeight": "500",
          "textAlign": "center"
        }
      }
    }
  ]
}
```

## 🎯 Benefits of Render JSON

### 1. **Simple Renderer**
- No layout calculations needed
- Just draw at specified coordinates
- Fast and predictable

### 2. **Easy Debugging**
- Can inspect exact positions and styles
- Clear what will be rendered where
- Pixel-perfect validation

### 3. **Reusable Output**
- Same format can feed Canvas, WebGL, or other renderers
- Layout calculations done once, reused multiple times
- Consistent output across platforms

### 4. **Testable**
- Can validate render output visually
- Can test layout conversion separately
- Clear separation of concerns

---

*This format provides pixel-perfect drawing instructions that make the renderer extremely simple and fast, while ensuring visual consistency across all output formats.*