# Phase 4: Implementation

## Phase Overview

**Duration**: Week 3-4
**Status**: 🟡 Planning
**Goal**: Convert design token specifications and component definitions into implementable React/shadcn components with comprehensive documentation and validation.

## Objectives

1. **Component Generation**: Create React component implementations based on specifications
2. **Style Implementation**: Generate Tailwind CSS classes and design token integration
3. **Documentation Creation**: Produce comprehensive component documentation and examples
4. **Quality Validation**: Ensure components match original designs and maintain consistency

## Success Criteria

- ✅ Generate 100% of specified components with React + TypeScript
- ✅ Implement all variants and states identified in Phase 3
- ✅ Create comprehensive documentation with live examples
- ✅ Validate visual fidelity to original Figma designs

## Detailed Implementation Plan

### 4.1 React Component Generation

#### 4.1.1 Component Template System
```typescript
// Base component template structure
interface ComponentTemplate {
  name: string;
  description: string;
  props: ComponentProps;
  variants: ComponentVariant[];
  states: ComponentState[];
  accessibility: AccessibilityFeatures;
  examples: ComponentExample[];
}

interface ComponentProps {
  [key: string]: {
    type: string;
    required: boolean;
    default?: any;
    description: string;
  };
}

// Generated Button component example
import React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input hover:bg-accent hover:text-accent-foreground',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'underline-offset-4 hover:underline text-primary',
      },
      size: {
        default: 'h-10 py-2 px-4',
        sm: 'h-9 px-3 rounded-md',
        lg: 'h-11 px-8 rounded-md',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, loading = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={loading || props.disabled}
        {...props}
      >
        {loading && <LoadingSpinner className="mr-2 h-4 w-4" />}
        {props.children}
      </Comp>
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
```

**Tasks**:
- [ ] Create React component template generator
- [ ] Implement TypeScript interface generation
- [ ] Build variant system with class-variance-authority
- [ ] Develop accessibility integration patterns

**Deliverables**:
- React component template system
- TypeScript interface generator
- Variant implementation framework
- Accessibility integration utilities

#### 4.1.2 Custom Hook Generation
```typescript
// JSON-driven component hook template
interface ComponentConfig {
  id: string;
  type: string;
  jsonUrl?: string;
  data?: any;
  autoRefresh?: boolean;
  refreshInterval?: number;
}

interface StandardHookReturn<T, Actions extends Record<string, any>> {
  data: T | null;
  loading: boolean;
  error: string | null;
  refresh: () => void;
  actions: Actions;
}

// Generated hook for Data Table component
export function useDataTable(config: ComponentConfig): StandardHookReturn<DataTableData, DataTableActions> {
  const [data, setData] = useState<DataTableData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      let responseData: DataTableData;

      if (config.jsonUrl) {
        const response = await fetch(config.jsonUrl);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        responseData = await response.json();
      } else if (config.data) {
        responseData = config.data;
      } else {
        throw new Error('No data source configured');
      }

      setData(responseData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [config.jsonUrl, config.data]);

  // Auto-refresh functionality
  useEffect(() => {
    fetchData();

    if (config.autoRefresh && config.refreshInterval) {
      const interval = setInterval(fetchData, config.refreshInterval);
      return () => clearInterval(interval);
    }
  }, [fetchData, config.autoRefresh, config.refreshInterval]);

  const actions: DataTableActions = {
    sort: (column: string, direction: 'asc' | 'desc') => {
      if (data) {
        const sortedData = { ...data };
        sortedData.rows = [...data.rows].sort((a, b) => {
          const aValue = a[column];
          const bValue = b[column];
          const modifier = direction === 'asc' ? 1 : -1;

          if (aValue < bValue) return -1 * modifier;
          if (aValue > bValue) return 1 * modifier;
          return 0;
        });
        setData(sortedData);
      }
    },
    filter: (filters: FilterCriteria) => {
      if (data) {
        const filteredData = { ...data };
        filteredData.rows = data.rows.filter(row => {
          return Object.entries(filters).every(([key, value]) => {
            return row[key] === value;
          });
        });
        setData(filteredData);
      }
    },
    select: (rowId: string) => {
      if (data) {
        const updatedData = { ...data };
        const rowIndex = updatedData.rows.findIndex(row => row.id === rowId);
        if (rowIndex !== -1) {
          updatedData.rows[rowIndex] = {
            ...updatedData.rows[rowIndex],
            selected: !updatedData.rows[rowIndex].selected
          };
        }
        setData(updatedData);
      }
    }
  };

  return {
    data,
    loading,
    error,
    refresh: fetchData,
    actions
  };
}
```

**Tasks**:
- [ ] Create hook template generator
- [ ] Implement StandardHookReturn pattern
- [ ] Build data loading and state management
- [ ] Develop action system generation

**Deliverables**:
- Hook generation system
- StandardHookReturn implementation
- Action pattern templates
- Data management utilities

### 4.2 Style Implementation

#### 4.2.1 Tailwind CSS Class Generation
```typescript
interface StyleMapping {
  colors: {
    [tokenName: string]: string;
  };
  spacing: {
    [tokenName: string]: string;
  };
  typography: {
    [tokenName: string]: string;
  };
  effects: {
    [tokenName: string]: string;
  };
}

// Generated Tailwind configuration extension
const designSystemConfig = {
  theme: {
    extend: {
      colors: {
        // Extracted from Figma design tokens
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6', // Primary blue from design
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
          950: '#172554',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
        accent: {
          50: '#fef2f2',
          100: '#fee2e2',
          200: '#fecaca',
          300: '#fca5a5',
          400: '#f87171',
          500: '#ef4444', // Accent color from design
          600: '#dc2626',
          700: '#b91c1c',
          800: '#991b1b',
          900: '#7f1d1d',
          950: '#450a0a',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        // Design system spacing scale
        '18': '4.5rem',    // 72px
        '88': '22rem',     // 352px
        '128': '32rem',    // 512px
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
};

// Generated CSS variables for design tokens
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;

  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;

  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;

  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;

  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;

  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;

  --accent: 0 84.2% 60.2%;
  --accent-foreground: 210 40% 98%;

  --destructive: 0 62.8% 30.6%;
  --destructive-foreground: 210 40% 98%;

  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 221.2 83.2% 53.3%;

  --radius: 0.5rem;
}
```

**Tasks**:
- [ ] Create Tailwind config generator from design tokens
- [ ] Implement CSS variable system
- [ ] Build custom spacing scale mapping
- [ ] Develop color palette generation

**Deliverables**:
- Tailwind configuration files
- CSS variable definitions
- Design token mapping utilities
- Style compilation pipeline

#### 4.2.2 Component Style Generation
```typescript
interface ComponentStyles {
  base: string;
  variants: {
    [variantName: string]: string;
  };
  sizes: {
    [sizeName: string]: string;
  };
  states: {
    [stateName: string]: string;
  };
}

// Generated styles for Card component
const cardStyles: ComponentStyles = {
  base: 'rounded-lg border bg-card text-card-foreground shadow-sm',
  variants: {
    default: 'border-border',
    elevated: 'border-0 shadow-lg',
    outlined: 'border-2 border-border shadow-none',
    ghost: 'border-0 bg-transparent shadow-none',
  },
  sizes: {
    sm: 'p-3',
    default: 'p-6',
    lg: 'p-8',
    xl: 'p-10',
  },
  states: {
    hover: 'hover:shadow-md transition-shadow',
    interactive: 'hover:shadow-md cursor-pointer transition-shadow',
    loading: 'opacity-70 pointer-events-none',
  }
};

// Generated CVA (class-variance-authority) configuration
export const cardVariants = cva(cardStyles.base, {
  variants: {
    variant: {
      default: cardStyles.variants.default,
      elevated: cardStyles.variants.elevated,
      outlined: cardStyles.variants.outlined,
      ghost: cardStyles.variants.ghost,
    },
    size: {
      sm: cardStyles.sizes.sm,
      default: cardStyles.sizes.default,
      lg: cardStyles.sizes.lg,
      xl: cardStyles.sizes.xl,
    },
    interactive: {
      true: cardStyles.states.interactive,
      false: '',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'default',
    interactive: false,
  },
});
```

**Tasks**:
- [ ] Create component style generator
- [ ] Implement CVA configuration builder
- [ ] Build responsive style variations
- [ ] Develop theme integration utilities

**Deliverables**:
- Component style generation system
- CVA configuration files
- Responsive style utilities
- Theme integration framework

### 4.3 Documentation Creation

#### 4.3.1 Component Documentation Generator
```markdown
# Button Component

## Overview
The Button component is a versatile interactive element used to trigger actions throughout the application. It supports multiple variants, sizes, and states to accommodate different use cases.

## Installation
```bash
npm install @iamplus/components
```

## Usage
```tsx
import { Button } from '@iamplus/components';

export default function Example() {
  return (
    <div className="flex gap-4">
      <Button variant="default">Default Button</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button size="sm">Small</Button>
      <Button size="lg">Large</Button>
    </div>
  );
}
```

## API Reference

### Props
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | `'default' \| 'destructive' \| 'outline' \| 'secondary' \| 'ghost' \| 'link'` | `'default'` | The visual style variant |
| size | `'default' \| 'sm' \| 'lg' \| 'icon'` | `'default'` | The button size |
| asChild | `boolean` | `false` | Whether to render as a different element |
| loading | `boolean` | `false` | Show loading state |
| disabled | `boolean` | `false` | Disable the button |
| onClick | `(event: MouseEvent) => void` | - | Click handler |

### Variants

#### Default
```tsx
<Button variant="default">Save Changes</Button>
```
Primary action button with solid background.

#### Destructive
```tsx
<Button variant="destructive">Delete Item</Button>
```
Used for destructive actions like delete, remove, etc.

#### Outline
```tsx
<Button variant="outline">Cancel</Button>
```
Secondary action with transparent background and border.

#### Ghost
```tsx
<Button variant="ghost">Edit</Button>
```
Subtle action with no background, only on hover.

#### Link
```tsx
<Button variant="link">Learn More</Button>
```
Styled as a link with underline on hover.

### Sizes

#### Small
```tsx
<Button size="sm">Small Button</Button>
```
Compact button for tight spaces.

#### Default
```tsx
<Button size="default">Default Button</Button>
```
Standard button size.

#### Large
```tsx
<Button size="lg">Large Button</Button>
```
Prominent button for primary actions.

#### Icon
```tsx
<Button size="icon">
  <PlusIcon />
</Button>
```
Square button for icons only.

## States

### Loading
```tsx
<Button loading disabled>Loading...</Button>
```
Shows loading spinner and disables interaction.

### Disabled
```tsx
<Button disabled>Disabled</Button>
```
Visually disabled and non-interactive.

## Accessibility

- Supports keyboard navigation with Tab and Enter/Space keys
- Provides appropriate ARIA attributes
- Includes focus states for keyboard users
- Semantic HTML button element by default

## Design Token Mapping

| Element | CSS Variable | Value |
|---------|--------------|-------|
| Background | `--primary` | `hsl(221.2 83.2% 53.3%)` |
| Text | `--primary-foreground` | `hsl(210 40% 98%)` |
| Border | `--border` | `hsl(214.3 31.8% 91.4%)` |
| Radius | `--radius` | `0.5rem` |

## Examples

### With Icons
```tsx
<Button>
  <DownloadIcon className="mr-2 h-4 w-4" />
  Download
</Button>
```

### Full Width
```tsx
<Button className="w-full">Full Width Button</Button>
```

### Button Group
```tsx
<div className="flex gap-2">
  <Button variant="outline">Cancel</Button>
  <Button>Submit</Button>
</div>
```
```

**Tasks**:
- [ ] Create documentation template generator
- [ ] Implement API reference generation
- [ ] Build example code generator
- [ ] Develop accessibility documentation

**Deliverables**:
- Component documentation system
- API reference generator
- Example code templates
- Accessibility guidelines

#### 4.3.2 Storybook Integration
```typescript
// Generated Storybook stories
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './button';

const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile button component with multiple variants and sizes.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link'],
      description: 'The visual style variant',
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'icon'],
      description: 'The button size',
    },
    children: {
      control: 'text',
      description: 'Button content',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable the button',
    },
    loading: {
      control: 'boolean',
      description: 'Show loading state',
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

// Default story
export const Default: Story = {
  args: {
    children: 'Button',
  },
};

// Variants stories
export const Variants: Story = {
  render: () => (
    <div className="flex gap-4">
      <Button variant="default">Default</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
};

// Sizes story
export const Sizes: Story = {
  render: () => (
    <div className="flex items-center gap-4">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
      <Button size="icon">
        <PlusIcon />
      </Button>
    </div>
  ),
};

// States story
export const States: Story = {
  render: () => (
    <div className="flex gap-4">
      <Button>Default</Button>
      <Button disabled>Disabled</Button>
      <Button loading>Loading</Button>
    </div>
  ),
};

// Interactive playground
export const Playground: Story = {
  args: {
    variant: 'default',
    size: 'default',
    children: 'Click me',
    disabled: false,
    loading: false,
  },
};
```

**Tasks**:
- [ ] Create Storybook story generator
- [ ] Implement interactive playground stories
- [ ] Build variant and size showcase stories
- [ ] Develop controls and argTypes configuration

**Deliverables**:
- Storybook configuration
- Component story files
- Interactive playground examples
- Documentation integration

### 4.4 Quality Validation

#### 4.4.1 Visual Validation System
```typescript
interface VisualValidation {
  componentId: string;
  originalScreenshot: string;
  implementationScreenshot: string;
  comparison: {
    pixelDifference: number;
    structuralSimilarity: number;
    colorAccuracy: number;
    layoutAccuracy: number;
  };
  passed: boolean;
  issues: ValidationIssue[];
}

async function validateComponentImplementation(
  componentSpec: ComponentSpecification,
  implementationPath: string
): Promise<VisualValidation> {
  // Generate screenshots of the implementation
  const implementationScreenshots = await generateComponentScreenshots(
    implementationPath,
    componentSpec.variants
  );

  // Compare with original Figma screenshots
  const comparisons = await Promise.all(
    componentSpec.variants.map(async (variant) => {
      const original = componentSpec.screenshots[variant.id];
      const implementation = implementationScreenshots[variant.id];

      return {
        variant: variant.id,
        comparison: await compareScreenshots(original, implementation)
      };
    })
  );

  return {
    componentId: componentSpec.id,
    originalScreenshot: componentSpec.screenshots.default,
    implementationScreenshot: implementationScreenshots.default,
    comparison: aggregateComparisons(comparisons),
    passed: comparisons.every(c => c.comparison.similarity > 0.95),
    issues: identifyValidationIssues(comparisons)
  };
}
```

**Tasks**:
- [ ] Create visual comparison utilities
- [ ] Implement screenshot generation for components
- [ ] Build similarity analysis algorithms
- [ ] Develop issue identification system

**Deliverables**:
- Visual validation framework
- Screenshot comparison tools
- Quality metrics system
- Issue reporting utilities

#### 4.4.2 Functional Testing
```typescript
interface ComponentTestSuite {
  componentId: string;
  tests: {
    rendering: TestResult[];
    interactions: TestResult[];
    accessibility: TestResult[];
    responsive: TestResult[];
  };
  coverage: TestCoverage;
}

// Generated test file for Button component
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './button';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

describe('Button', () => {
  // Rendering tests
  it('renders correctly with default props', () => {
    render(<Button>Click me</Button>);
    const button = screen.getByRole('button', { name: 'Click me' });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-primary');
  });

  it('renders with different variants', () => {
    const { rerender } = render(<Button variant="destructive">Delete</Button>);
    expect(screen.getByRole('button')).toHaveClass('bg-destructive');

    rerender(<Button variant="outline">Cancel</Button>);
    expect(screen.getByRole('button')).toHaveClass('border-input');
  });

  // Interaction tests
  it('handles click events', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('can be disabled', () => {
    const handleClick = jest.fn();
    render(<Button disabled onClick={handleClick}>Disabled</Button>);

    const button = screen.getByRole('button');
    expect(button).toBeDisabled();

    fireEvent.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  // Accessibility tests
  it('should not have accessibility violations', async () => {
    const { container } = render(<Button>Accessible button</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('supports keyboard navigation', () => {
    render(<Button>Keyboard button</Button>);
    const button = screen.getByRole('button');

    button.focus();
    expect(button).toHaveFocus();

    fireEvent.keyDown(button, { key: 'Enter' });
    // Should trigger click action
  });

  // Responsive tests
  it('adapts to different sizes', () => {
    const { rerender } = render(<Button size="sm">Small</Button>);
    expect(screen.getByRole('button')).toHaveClass('h-9');

    rerender(<Button size="lg">Large</Button>);
    expect(screen.getByRole('button')).toHaveClass('h-11');
  });
});
```

**Tasks**:
- [ ] Create automated test generation
- [ ] Implement accessibility testing with axe-core
- [ ] Build interaction testing utilities
- [ ] Develop responsive testing framework

**Deliverables**:
- Automated test suite
- Accessibility validation tools
- Interaction testing framework
- Quality coverage reports

## File Organization Structure

```
src/iamplus/
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── index.ts
│   ├── data-table/
│   │   ├── data-table.tsx
│   │   ├── data-table-columns.tsx
│   │   ├── data-table-context.tsx
│   │   └── index.ts
│   └── index.ts
├── hooks/
│   ├── use-data-table.tsx
│   ├── use-card.tsx
│   └── index.ts
├── contexts/
│   ├── data-table-context.tsx
│   └── index.ts
├── types/
│   ├── component-types.ts
│   ├── design-tokens.ts
│   └── index.ts
└── lib/
    ├── utils.ts
    ├── constants.ts
    └── design-tokens.ts

stories/
├── components/
│   ├── button.stories.tsx
│   ├── card.stories.tsx
│   └── data-table.stories.tsx
└── index.ts

tests/
├── components/
│   ├── button.test.tsx
│   ├── card.test.tsx
│   └── data-table.test.tsx
├── accessibility/
│   └── axe.test.tsx
└── visual/
    └── visual-regression.test.tsx

docs/
├── components/
│   ├── button.md
│   ├── card.md
│   └── data-table.md
├── design-tokens.md
├── getting-started.md
└── migration-guide.md
```

## Integration with Existing Project

### 4.5.1 Project Structure Integration
```typescript
// Update to existing components.json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "slate",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@iamplus/components",
    "utils": "@iamplus/lib/utils",
    "ui": "@iamplus/components/ui",
    "lib": "@iamplus/lib",
    "hooks": "@iamplus/hooks"
  },
  "iconLibrary": "lucide-react"
}
```

**Tasks**:
- [ ] Update project configuration for new components
- [ ] Integrate with existing build system
- [ ] Configure TypeScript path aliases
- [ ] Set up component exports and imports

### 4.5.2 Migration Strategy
```typescript
// Migration guide for existing components
interface MigrationPlan {
  oldComponent: string;
  newComponent: string;
  breakingChanges: BreakingChange[];
  migrationSteps: MigrationStep[];
  examples: CodeExample[];
}

const migrationPlan: MigrationPlan[] = [
  {
    oldComponent: 'CustomButton',
    newComponent: 'Button',
    breakingChanges: [
      {
        description: 'Prop name changed from "btnType" to "variant"',
        impact: 'medium',
        fix: 'Replace btnType prop with variant'
      }
    ],
    migrationSteps: [
      'Update import statement',
      'Replace btnType prop with variant',
      'Update size prop values if needed',
      'Test functionality and styling'
    ],
    examples: [
      {
        before: '<CustomButton btnType="primary" size="lg">Click</CustomButton>',
        after: '<Button variant="default" size="lg">Click</Button>'
      }
    ]
  }
];
```

**Tasks**:
- [ ] Create migration documentation
- [ ] Implement backward compatibility layer
- [ ] Build migration automation scripts
- [ ] Develop testing procedures for migrated components

## Risk Mitigation

### Technical Risks
- **Component Complexity**: Break down complex components into smaller pieces
- **Style Conflicts**: Use CSS specificity and scoped styles
- **Performance Issues**: Optimize component rendering and bundle size

### Quality Risks
- **Visual Inconsistency**: Comprehensive visual validation system
- **Accessibility Issues**: Automated and manual accessibility testing
- **Browser Compatibility**: Cross-browser testing and polyfills

## Deliverables Summary

### Primary Outputs
- Complete React component library with TypeScript
- Comprehensive styling system with Tailwind CSS
- Full documentation with examples and API references
- Quality validation and testing framework

### Secondary Outputs
- Storybook configuration and stories
- Migration guides and compatibility layer
- Build and development tooling
- Design token integration

### Tools & Utilities
- Component generation system
- Style compilation pipeline
- Documentation generator
- Quality validation framework

## Success Metrics

### Implementation Completeness
- ✅ Generate 100% of specified components
- ✅ Implement all variants and states
- ✅ Create comprehensive documentation
- ✅ Achieve 95%+ visual accuracy

### Quality Standards
- ✅ 100% accessibility compliance (WCAG 2.1 AA)
- ✅ 90%+ test coverage
- ✅ Zero console errors or warnings
- ✅ Consistent design system implementation

### Developer Experience
- ✅ Clear and comprehensive documentation
- ✅ Easy-to-use component APIs
- ✅ Seamless integration with existing codebase
- ✅ Robust error handling and validation

---

*This phase completes the Figma Design System Extraction project by transforming the analyzed design patterns into a production-ready component library that maintains visual fidelity while providing excellent developer experience.*