# SimFlo Design Format - Minimal V1.0 Specification

## 🎯 Design Philosophy & Constraints

### Core Principles
1. **Responsive by Default** - All layouts use flex/grid systems
2. **No Absolute Positioning** - Never use fixed pixel coordinates
3. **Percentage-Based Sizing** - All dimensions relative to parent containers
4. **Component-Centric** - Focus on visual components, not complex logic
5. **Zero-Code Components** - Components contain minimal code, data in hooks

### Design Scope
- **Design Tokens**: Colors, typography, spacing, shadows
- **Components**: Reusable UI elements with variants
- **Pages/Mobile**: Screen layouts adapted for mobile or desktop

### Explicitly Excluded (for now)
- ❌ Animations and transitions
- ❌ Prototype interactions
- ❌ Scroll behaviors
- ❌ Complex state management
- ❌ Props-based data passing
- ❌ Absolute positioning

## 🏗️ Layout System Philosophy

### Universal Layout Approach
- **Single Layout System**: Define one approach that works for all target platforms
- **Converter Responsibility**: Each converter handles platform-specific layout implementation
- **Layout Options**:
  - **Auto-Layout**: Smart responsive layout (like Figma Auto-Layout)
  - **Stack**: Vertical or horizontal stacking
  - **Grid**: Regular grid system

### Container Hierarchy
- **Parent-Relative Sizing**: All elements size relative to their immediate parent
- **Responsive Flow**: Natural responsive behavior through flex/grid
- **Viewport Adaptation**: Same JSON works across different screen sizes

## 📱 Screen Size Reference

### Default: iPhone 12
- **Dimensions**: 390px × 844px
- **Purpose**: Fixed reference for design and canvas rendering
- **Responsiveness**: Same JSON should adapt to any screen size when re-rendered

## 📋 JSON Format Structure V1.0

### Root Schema
```json
{
  "version": "1.0.0",
  "screenType": "mobile" | "desktop" | "responsive",
  "designTokens": { /* See SIMFLO_DESIGN_TOKENS_SPEC.md */ },
  "components": { /* See SIMFLO_COMPONENTS_SPEC.md */ },
  "screens": { /* See SIMFLO_SCREENS_SPEC.md */ }
}
```

### Module Specifications
- **📖 Design Tokens**: `SIMFLO_DESIGN_TOKENS_SPEC.md` - Colors, typography, spacing, borders, shadows
- **🧩 Components**: `SIMFLO_COMPONENTS_SPEC.md` - Reusable UI components with variants and content types
- **📱 Screens**: `SIMFLO_SCREENS_SPEC.md` - Complete screen layouts and responsive patterns

### 1. Design Tokens (Referenced)
```json
{
  "designTokens": {
    "colors": {
      "primary": "#6257db",
      "secondary": "#f0f0f0",
      "text": {
        "primary": "#2e2e2e",
        "secondary": "#6b7280"
      },
      "background": {
        "primary": "#ffffff",
        "secondary": "#f4f4f4"
      }
    },
    "typography": {
      "fontFamily": {
        "primary": "Inter",
        "secondary": "SF Pro"
      },
      "fontSize": {
        "xs": "12px",
        "sm": "14px",
        "base": "16px",
        "lg": "18px",
        "xl": "24px",
        "2xl": "32px"
      },
      "fontWeight": {
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700"
      }
    },
    "spacing": {
      "xs": "4px",
      "sm": "8px",
      "md": "16px",
      "lg": "24px",
      "xl": "32px"
    },
    "borderRadius": {
      "sm": "4px",
      "md": "8px",
      "lg": "12px",
      "xl": "16px"
    },
    "shadows": {
      "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
      "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
      "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)"
    }
  }
}
```

### 2. Components (Referenced)
See `SIMFLO_COMPONENTS_SPEC.md` for complete component definitions including:
- **Form Components**: Input, Button, Select, Checkbox
- **Display Components**: Card, Badge, Avatar, Image
- **Layout Components**: Container, Stack, Grid
- **Navigation Components**: Header, Footer, Sidebar

### 3. Screens (Referenced)
See `SIMFLO_SCREENS_SPEC.md` for complete screen definitions including:
- **Authentication Screens**: Login, Register, Forgot Password
- **Main Navigation**: Home, Dashboard, Profile
- **Content Screens**: Lists, Details, Forms
- **Layout Patterns**: Full screen, Navigation, Overlay

## 🔧 Key Design Decisions

### 1. Reference-Based Styling
- All style values reference design tokens (e.g., `"colors.primary"`)
- No hardcoded values in component definitions
- Enables easy theming and consistency

### 2. Layout System Types
- **auto-layout**: Smart responsive layout with constraints
- **stack**: Simple vertical/horizontal stacking
- **grid**: Regular grid arrangement (future)

### 3. Content Types
- **text**: Static text display
- **input**: User input field
- **component**: Reusable component instance
- **container**: Layout container with children

### 4. Responsive Behavior
- Width/height as percentages of parent
- Flexible padding and spacing
- Automatic adaptation to different screen sizes

## 🎯 Implementation Strategy

### Phase 1: Core Format
1. Define JSON schema validation
2. Create sample Login screen JSON
3. Build HTML canvas renderer for iPhone 12 (390×844)
4. Test responsive resizing

### Phase 2: Component Library
1. Expand component definitions
2. Add more layout patterns
3. Test different screen compositions

### Phase 3: Converter Integration
1. Figma → SimFlo format parser
2. React/React Native generators
3. End-to-end conversion testing

---

*This format is intentionally minimal and will evolve as we add support for more features.*