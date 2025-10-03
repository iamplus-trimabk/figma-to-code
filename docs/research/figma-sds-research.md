# Figma SDS (Shared Design System) Research
## Repository: https://github.com/figma/sds

## Overview
Figma SDS (Shared Design System) is Figma's internal design system that demonstrates best practices for bridging design and development through Figma Variables, Styles, Components, and Code Connect. It provides a real-world example of how to structure a comprehensive design system that integrates seamlessly with modern development workflows.

## Architecture & Structure

### Core Components
```typescript
src/ui/
├── primitives/          # Basic building blocks
│   ├── Button/
│   ├── Input/
│   ├── Avatar/
│   └── ...
├── compositions/        # Complex components
│   ├── Card/
│   ├── DataTable/
│   ├── Navigation/
│   └── ...
├── utilities/          # Helper utilities
│   ├── cn.ts           # Class name utility
│   ├── types.ts        # Type definitions
│   └── constants.ts    # Design constants
└── index.ts            # Main exports
```

### Key Technologies
- **Figma Variables**: Design token management
- **Figma Styles**: Consistent design properties
- **Figma Components**: Reusable design elements
- **Code Connect**: Design-to-code synchronization
- **React**: Component implementation framework
- **TypeScript**: Type safety and interfaces

## Design System Organization Patterns

### 1. **Component Taxonomy**
```typescript
// Clear hierarchical organization
export enum ComponentCategory {
  PRIMITIVE = 'primitive',      // Basic elements (Button, Input)
  COMPOSITION = 'composition',  // Complex assemblies (Card, Form)
  LAYOUT = 'layout',           // Structural components (Grid, Stack)
  UTILITY = 'utility'          // Helper components (Icon, Badge)
}

interface ComponentMetadata {
  category: ComponentCategory;
  tags: string[];
  status: 'stable' | 'beta' | 'deprecated';
  version: string;
}
```

### 2. **Design Token Structure**
```typescript
// Systematic token organization
interface DesignTokens {
  colors: {
    semantic: Record<string, ColorToken>;    // primary, secondary, accent
    neutral: Record<string, ColorToken>;     // gray scales
    feedback: Record<string, ColorToken>;    // success, warning, error
  };
  typography: {
    fontFamily: Record<string, string>;
    fontSize: Record<string, number>;
    fontWeight: Record<string, number>;
    lineHeight: Record<string, number>;
  };
  spacing: {
    scale: Record<string, number>;          // 4, 8, 12, 16, 24, 32...
    semantic: Record<string, string>;        // small, medium, large
  };
  effects: {
    shadows: Record<string, ShadowToken>;
    borderRadius: Record<string, number>;
  };
}
```

### 3. **Component Architecture**
```typescript
// Standardized component structure
interface ComponentProps {
  variant?: string;           // Component variants
  size?: ComponentSize;       // Size variations
  disabled?: boolean;         // State management
  children?: React.ReactNode; // Content composition
  className?: string;         // Custom styling
}

// Example: Button implementation
export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'medium',
  disabled = false,
  children,
  className,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center';
  const variantClasses = buttonVariants[variant];
  const sizeClasses = sizeVariants[size];

  return (
    <button
      className={cn(baseClasses, variantClasses, sizeClasses, className)}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  );
};
```

## Figma Integration Patterns

### 1. **Variable Mapping**
```typescript
// Direct mapping from Figma Variables to code
const colors = {
  'color-primary': 'var(--color-primary)',
  'color-secondary': 'var(--color-secondary)',
  'color-surface': 'var(--color-surface)',
  'color-text': 'var(--color-text)'
};

// Automatic token synchronization
export const getFigmaVariable = (tokenName: string): string => {
  return figmaVariables[tokenName] || tokenName;
};
```

### 2. **Style Consistency**
```typescript
// Consistent application of Figma Styles
const typographyStyles = {
  'text-heading-large': {
    fontSize: 'var(--font-size-heading-large)',
    fontWeight: 'var(--font-weight-bold)',
    lineHeight: 'var(--line-height-tight)'
  },
  'text-body-medium': {
    fontSize: 'var(--font-size-body-medium)',
    fontWeight: 'var(--font-weight-regular)',
    lineHeight: 'var(--line-height-normal)'
  }
};
```

### 3. **Component Variants**
```typescript
// Mapping Figma component variants to code
const buttonVariants = {
  primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
  outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
  ghost: 'hover:bg-accent hover:text-accent-foreground'
};

const sizeVariants = {
  small: 'h-8 px-3 text-sm',
  medium: 'h-10 px-4 py-2',
  large: 'h-12 px-6 text-lg'
};
```

## Advanced Patterns & Best Practices

### 1. **Composition Strategy**
```typescript
// Flexible composition patterns
interface CompositionProps {
  layout: 'horizontal' | 'vertical';
  spacing: ComponentSpacing;
  alignment: AlignmentOptions;
  children: React.ReactNode;
}

export const Stack: React.FC<CompositionProps> = ({
  layout = 'vertical',
  spacing = 'medium',
  alignment = 'start',
  children
}) => {
  const layoutClasses = layout === 'horizontal' ? 'flex-row' : 'flex-col';
  const spacingClasses = spacingClasses[spacing];
  const alignmentClasses = alignmentClasses[alignment];

  return (
    <div className={cn('flex', layoutClasses, spacingClasses, alignmentClasses)}>
      {children}
    </div>
  );
};
```

### 2. **State Management**
```typescript
// Consistent state handling across components
interface ComponentState {
  hover: boolean;
  focus: boolean;
  active: boolean;
  disabled: boolean;
  loading: boolean;
}

export const useStateStyles = (
  baseClasses: string,
  state: ComponentState
): string => {
  return cn(
    baseClasses,
    state.hover && 'hover:styles',
    state.focus && 'focus:styles',
    state.active && 'active:styles',
    state.disabled && 'disabled:styles',
    state.loading && 'loading:styles'
  );
};
```

### 3. **Accessibility Integration**
```typescript
// Built-in accessibility patterns
export const AccessibilityButton: React.FC<ButtonProps> = ({
  children,
  ariaLabel,
  ariaDescribedBy,
  ...props
}) => {
  return (
    <button
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedBy}
      role="button"
      tabIndex={props.disabled ? -1 : 0}
      {...props}
    >
      {children}
    </button>
  );
};
```

## Code Connect Integration

### 1. **Design-to-Code Sync**
```typescript
// Automatic synchronization patterns
interface FigmaComponent {
  id: string;
  name: string;
  type: 'COMPONENT' | 'COMPONENT_SET';
  properties: ComponentProperties;
  variants: ComponentVariant[];
}

export const syncFigmaComponent = (
  figmaComponent: FigmaComponent
): React.ComponentType => {
  // Generate React component from Figma component
  return generateReactComponent(figmaComponent);
};
```

### 2. **Variant Management**
```typescript
// Handle component variants systematically
interface ComponentVariantSet {
  primary: {
    variant: 'primary';
    size: 'small' | 'medium' | 'large';
    state: 'default' | 'hover' | 'pressed' | 'disabled';
  };
}

export const generateVariantClasses = (
  variants: ComponentVariantSet
): Record<string, string> => {
  // Generate CSS classes for all variant combinations
  return Object.entries(variants).reduce((acc, [key, value]) => {
    acc[key] = generateVariantClass(value);
    return acc;
  }, {});
};
```

## Component Examples

### 1. **Primitive Component**
```typescript
// Button - Basic building block
export const Button = {
  Root: ButtonRoot,
  Variant: ButtonVariant,
  Size: ButtonSize,
  Icon: ButtonIcon
};

// Usage
<Button.Root variant="primary" size="medium">
  <Button.Icon>
    <PlusIcon />
  </Button.Icon>
  Add Item
</Button.Root>
```

### 2. **Composition Component**
```typescript
// Card - Complex assembly
export const Card = {
  Root: CardRoot,
  Header: CardHeader,
  Title: CardTitle,
  Description: CardDescription,
  Content: CardContent,
  Footer: CardFooter
};

// Usage
<Card.Root>
  <Card.Header>
    <Card.Title>Card Title</Card.Title>
    <Card.Description>Card description</Card.Description>
  </Card.Header>
  <Card.Content>
    Card content goes here
  </Card.Content>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card.Root>
```

### 3. **Layout Component**
```typescript
// Grid - Structural component
export const Grid = {
  Root: GridRoot,
  Item: GridItem
};

// Usage
<Grid.Root cols={3} gap="medium">
  <Grid.Item span={2}>Wide item</Grid.Item>
  <Grid.Item>Narrow item</Grid.Item>
</Grid.Root>
```

## Key Insights for Our Project

### 1. **Component Taxonomy Strategy**
- Clear categorization (primitives, compositions, layouts)
- Consistent naming conventions
- Hierarchical organization
- Easy discovery and usage

### 2. **Design Token Integration**
- Systematic token organization
- Direct Figma Variable mapping
- Semantic naming conventions
- Scalable token system

### 3. **Component Architecture Patterns**
- Standardized prop interfaces
- Consistent variant handling
- Flexible composition strategies
- Built-in accessibility

### 4. **Development Workflow Integration**
- Code Connect for design synchronization
- Automatic variant generation
- Consistent styling patterns
- Type safety throughout

## Application to Our Design System Extraction

### 1. **Component Classification**
```typescript
// Apply SDS taxonomy to our extraction
export const classifyExtractedComponent = (
  component: ExtractedComponent
): ComponentCategory => {
  if (isPrimitive(component)) {
    return ComponentCategory.PRIMITIVE;
  } else if (isComposition(component)) {
    return ComponentCategory.COMPOSITION;
  } else if (isLayout(component)) {
    return ComponentCategory.LAYOUT;
  }
  return ComponentCategory.UTILITY;
};
```

### 2. **Token Structure Adoption**
```typescript
// Use SDS token organization
export const organizeExtractedTokens = (
  rawTokens: RawDesignTokens
): DesignTokens => {
  return {
    colors: categorizeColors(rawTokens.colors),
    typography: organizeTypography(rawTokens.typography),
    spacing: createSpacingScale(rawTokens.spacing),
    effects: extractEffects(rawTokens.effects)
  };
};
```

### 3. **Component Generation Patterns**
```typescript
// Generate components following SDS patterns
export const generateSDSComponent = (
  spec: ComponentSpecification
): React.ComponentType => {
  return {
    Root: generateRootComponent(spec),
    ...generateSubComponents(spec)
  };
};
```

### 4. **Variant System Implementation**
```typescript
// Implement comprehensive variant handling
export const createVariantSystem = (
  variants: ExtractedVariants
): VariantSystem => {
  return {
    variants: organizeVariants(variants),
    defaultVariant: determineDefault(variants),
    variantProps: generateVariantProps(variants)
  };
};
```

## Recommendations for Our Project

### 1. **Adopt SDS Taxonomy**
- Use primitive/composition/layout/utility categorization
- Implement consistent naming conventions
- Create clear component hierarchy

### 2. **Implement Design Token System**
- Organize tokens by semantic categories
- Create systematic spacing scales
- Establish color organization patterns

### 3. **Standardize Component Architecture**
- Use consistent prop interfaces
- Implement variant systems
- Build composition patterns

### 4. **Integration with Figma Features**
- Leverage Variables for token management
- Use Styles for consistency
- Implement Code Connect patterns

## Conclusion

Figma SDS provides an excellent blueprint for organizing and implementing a comprehensive design system. Its patterns for component taxonomy, design token management, and development integration offer valuable guidance for our automated extraction project.

**Key Takeaways**:
- Systematic organization is crucial for scalability
- Design token integration enables consistency
- Component composition patterns create flexibility
- Development workflow integration ensures adoption

**Recommendation**: Use SDS patterns as the foundation for our extracted design system structure, adapting them to our automated extraction requirements while maintaining the proven organizational principles.

---

*Research completed: Figma SDS analysis for design system organization patterns and best practices.*