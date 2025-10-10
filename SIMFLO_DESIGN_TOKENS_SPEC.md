# SimFlo Design Tokens Specification V1.0

## 🎯 Purpose
Defines the design token system for consistent styling across all SimFlo components and screens.

## 📋 Token Categories

### 1. Colors
```json
{
  "designTokens": {
    "colors": {
      "primary": "#6257db",
      "secondary": "#8b5cf6",
      "accent": "#ec4899",
      "success": "#10b981",
      "warning": "#f59e0b",
      "error": "#ef4444",
      "neutral": {
        "50": "#f9fafb",
        "100": "#f3f4f6",
        "200": "#e5e7eb",
        "300": "#d1d5db",
        "400": "#9ca3af",
        "500": "#6b7280",
        "600": "#4b5563",
        "700": "#374151",
        "800": "#1f2937",
        "900": "#111827"
      },
      "text": {
        "primary": "#111827",
        "secondary": "#4b5563",
        "tertiary": "#6b7280",
        "inverse": "#ffffff",
        "link": "#6257db"
      },
      "background": {
        "primary": "#ffffff",
        "secondary": "#f9fafb",
        "tertiary": "#f3f4f6",
        "inverse": "#111827",
        "overlay": "rgba(0, 0, 0, 0.5)"
      },
      "border": {
        "light": "#e5e7eb",
        "medium": "#d1d5db",
        "dark": "#9ca3af",
        "focus": "#6257db"
      }
    }
  }
}
```

### 2. Typography
```json
{
  "typography": {
    "fontFamily": {
      "primary": "Inter, system-ui, sans-serif",
      "secondary": "SF Pro Display, system-ui, sans-serif",
      "monospace": "SF Mono, Monaco, monospace"
    },
    "fontSize": {
      "xs": "12px",
      "sm": "14px",
      "base": "16px",
      "lg": "18px",
      "xl": "20px",
      "2xl": "24px",
      "3xl": "30px",
      "4xl": "36px",
      "5xl": "48px"
    },
    "fontWeight": {
      "light": "300",
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700",
      "extrabold": "800"
    },
    "lineHeight": {
      "tight": "1.25",
      "normal": "1.5",
      "relaxed": "1.75",
      "loose": "2"
    },
    "letterSpacing": {
      "tight": "-0.025em",
      "normal": "0",
      "wide": "0.025em",
      "wider": "0.05em"
    }
  }
}
```

### 3. Spacing & Sizing
```json
{
  "spacing": {
    "0": "0px",
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px"
  },
  "sizing": {
    "xs": "20px",
    "sm": "32px",
    "md": "48px",
    "lg": "64px",
    "xl": "96px",
    "2xl": "128px",
    "3xl": "192px"
  }
}
```

### 4. Border Radius
```json
{
  "borderRadius": {
    "none": "0px",
    "sm": "4px",
    "md": "8px",
    "lg": "12px",
    "xl": "16px",
    "2xl": "24px",
    "3xl": "32px",
    "full": "9999px"
  }
}
```

### 5. Shadows
```json
{
  "shadows": {
    "none": "none",
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    "inner": "inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)"
  }
}
```

### 6. Z-Index Scale
```json
{
  "zIndex": {
    "hide": "-1",
    "auto": "auto",
    "base": "0",
    "raised": "10",
    "dropdown": "1000",
    "sticky": "1100",
    "modal": "1200",
    "popover": "1300",
    "tooltip": "1400",
    "max": "9999"
  }
}
```

## 🎨 Token Usage Rules

### Reference Syntax
- **Direct Reference**: `"colors.primary"`
- **Nested Reference**: `"colors.text.primary"`
- **Scale Reference**: `"spacing.4"` (maps to 16px)

### Fallback Values
- Tokens can have fallbacks: `"colors.primary | #6257db"`
- Missing tokens resolve to fallback value
- Required tokens must be defined

### Responsive Tokens
- Tokens can be responsive: `"fontSize.16px | fontSize.18px"`
- First value: mobile (base)
- Second value: tablet and above

### Dark Mode Support
- Dark mode tokens: `"colors.background.primary | colors.background.inverse"`
- Format: `lightValue | darkValue`
- Automatic theme switching

## 🔧 Implementation Guidelines

### 1. Token Resolution
```javascript
// Resolve token reference to actual value
function resolveToken(tokenPath, theme = 'light') {
  const [token, fallback] = tokenPath.split('|').map(t => t.trim());
  const value = getTokenValue(token, theme);
  return value || fallback || token;
}

// Example usage
resolveToken("colors.primary") // "#6257db"
resolveToken("colors.text.primary | #000") // "#111827"
resolveToken("spacing.4 | 16px") // "16px"
```

### 2. Canvas Rendering
```javascript
// Convert token to canvas-compatible value
function tokenToCanvas(tokenPath, context = {}) {
  const value = resolveToken(tokenPath, context.theme);

  // Handle color values
  if (tokenPath.includes('colors')) {
    return value; // Canvas accepts hex colors
  }

  // Handle spacing/sizing values
  if (tokenPath.includes('spacing') || tokenPath.includes('sizing')) {
    return parseFloat(value) * context.scale; // Scale for responsive
  }

  return value;
}
```

### 3. Validation Rules
- All referenced tokens must exist in design tokens
- Fallback values must be valid for the token type
- Responsive tokens must follow format: `value | responsiveValue`
- Circular references are not allowed

## 📱 Screen Size Adaptation

### Breakpoint System
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+

### Token Scaling
```json
{
  "typography": {
    "fontSize": {
      "base": "16px | 18px", // 16px mobile, 18px tablet+
      "lg": "18px | 20px",   // 18px mobile, 20px tablet+
      "xl": "20px | 24px"    // 20px mobile, 24px tablet+
    }
  },
  "spacing": {
    "4": "16px | 20px",      // 16px mobile, 20px tablet+
    "6": "24px | 32px"       // 24px mobile, 32px tablet+
  }
}
```

## 🎯 Best Practices

### Token Naming
- Use semantic names: `"text.primary"` not `"gray.900"`
- Be consistent with naming patterns
- Group related tokens together

### Token Organization
- Start with essentials (colors, typography, spacing)
- Add complexity as needed
- Document token usage and intent

### Future Extensibility
- Easy to add new token categories
- Supports custom token sets
- Version compatibility maintained

---

*This spec provides the foundation for consistent design across all SimFlo outputs.*