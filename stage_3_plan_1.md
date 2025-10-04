# Stage 3: Universal Component Generator Tool

## 🎯 **Vision: Build shadcn/ui + unified-ui Inspired Component Generator**

Create a universal, design-token-driven component generation tool that can work with any React app (mobile or web). This tool will generate production-ready components following the proven patterns from shadcn/ui blocks, components, hooks, and unified-ui architecture.

## 🏗️ **Core Architecture Inspiration**

### **From shadcn/ui Ecosystem:**
- **40+ Components**: Button, Card, Input, Select, Table, Dialog, etc.
- **Blocks System**: Pre-built compositions like dashboards, login pages, forms
- **Hooks Pattern**: Copy-paste, production-tested hooks with TypeScript
- **Variants System**: Using CVA (Class Variance Authority) for component variants

### **From unified-ui Architecture:**
- **StandardHookReturn<T, Actions>**: Standardized pattern eliminating 67% complexity
- **JSON-Driven Components**: Configuration-driven component architecture
- **Generic CRUD Patterns**: Reusable data operations with TanStack Query
- **Entity-Aware Architecture**: Dynamic entity management and configuration

## 🎨 **Component Generation Categories**

### **1. Form Components** (shadcn/ui inspired)
- Input, Select, Checkbox, Radio, Textarea, Switch
- Form validation with react-hook-form integration
- Accessible labels, error states, and helper text

### **2. Display Components**
- Card, Badge, Avatar, Skeleton, Divider
- Data visualization: Chart, Progress, Metrics
- Layout: Grid, Container, Stack, Spacer

### **3. Navigation Components**
- Button, Tabs, Pagination, Breadcrumb, Sidebar
- Header, Footer, Navigation menus
- Responsive navigation patterns

### **4. Feedback Components**
- Alert, Toast, Modal, Dialog, Drawer
- Loading states, Error boundaries
- Tooltips, Popovers, Dropdowns

### **5. Data Components**
- Table, DataTable with sorting/filtering
- List, Tree, Accordion, Timeline
- Search and filter components

### **6. Block-Level Compositions** (shadcn blocks inspired)
- Dashboard layouts, Authentication forms
- Settings pages, Profile pages, Billing pages
- Landing page sections, Marketing components

## 🔧 **Generation Engine Architecture**

### **Input Processing:**
```json
{
  "componentType": "form-input",
  "platform": "web|mobile",
  "designTokens": {
    "colors": "from Stage 2 outputs",
    "typography": "from Stage 2 outputs",
    "spacing": "from Stage 2 outputs",
    "effects": "from Stage 2 outputs"
  },
  "features": {
    "validation": true,
    "accessibility": true,
    "variants": ["primary", "secondary", "error"],
    "sizes": ["sm", "md", "lg"]
  },
  "integrations": {
    "tanstack-query": true,
    "react-hook-form": true,
    "zod": true,
    "storybook": true
  }
}
```

### **Template System:**
- **Jinja2 Templates** for each component category
- **Pattern-based Generation** (Display, Interactive, Form, Data)
- **Platform-specific Adaptation** (Web Tailwind vs Mobile NativeWind)
- **Integration-aware Generation** (adds required imports and dependencies)

### **Hook Generation (unified-ui patterns):**
```typescript
// StandardHookReturn pattern for all generated hooks
export function useComponentData<T>(config: ComponentConfig): StandardHookReturn<T, ComponentActions> {
  // TanStack Query integration
  // Generic CRUD operations
  // Optimistic updates
  // Error handling
}
```

## 📁 **Tool Structure**

```
component_generator/
├── generators/
│   ├── component_generator.py      # Main orchestrator
│   ├── hook_generator.py          # Hook generation engine
│   ├── template_engine.py         # Jinja2 template processor
│   └── config_processor.py        # Design token integration
├── templates/
│   ├── components/                # Component templates by category
│   │   ├── forms/                 # Input, Select, Checkbox...
│   │   ├── display/               # Card, Badge, Avatar...
│   │   ├── navigation/            # Button, Tabs, Pagination...
│   │   ├── feedback/              # Alert, Modal, Toast...
│   │   ├── data/                  # Table, List, Tree...
│   │   └── blocks/                # Dashboard, Auth, Settings...
│   ├── hooks/                     # Hook templates following unified-ui patterns
│   │   ├── use-async-data.j2
│   │   ├── use-component-state.j2
│   │   ├── use-generic-crud.j2
│   │   └── use-data-pipeline.j2
│   ├── stories/                   # Storybook story templates
│   └── tests/                     # Unit test templates
├── patterns/
│   ├── display_component.py       # Static presentation patterns
│   ├── interactive_component.py   # State management patterns
│   ├── form_component.py          # Form validation patterns
│   └── data_component.py          # Data fetching patterns
└── integrations/
    ├── shadcn_integration.py      # shadcn/ui component mapping
    ├── unified_ui_patterns.py     # unified-ui architecture patterns
    └── platform_adapters.py       # Web/Mobile platform adapters
```

## 🔄 **Generation Pipeline**

### **Phase 1: Analysis & Configuration**
1. **Component Type Detection**: Analyze requested component type and category
2. **Platform Adaptation**: Configure for web (Tailwind) or mobile (NativeWind)
3. **Design Token Integration**: Apply Stage 2 design tokens (colors, typography, spacing)
4. **Feature Selection**: Determine validation, accessibility, variants, integrations

### **Phase 2: Code Generation**
1. **Hook Generation**: Create data management hooks using unified-ui patterns
2. **Component Generation**: Generate main component using shadcn/ui as foundation
3. **Variant Generation**: Create component variants using CVA
4. **Type Generation**: Generate comprehensive TypeScript interfaces

### **Phase 3: Enhancement & Integration**
1. **Storybook Generation**: Create interactive component documentation
2. **Test Generation**: Generate comprehensive unit tests
3. **Documentation Generation**: Create usage examples and API docs
4. **Export Generation**: Generate clean component exports and indexes

## 🎨 **Design Token Integration**

### **Color System:**
```typescript
// Generated from Stage 2 outputs
const colors = {
  primary: {
    50: '#f7f6fd',
    500: '#6257db',
    900: '#3a3483'
  },
  // ... full color palette from Stage 2
}
```

### **Typography System:**
```typescript
// Generated from Stage 2 outputs
const typography = {
  fontFamily: { Poppins: ['Poppins', 'sans-serif'] },
  fontSize: { caption: ['12px', { lineHeight: 1.4 }] },
  // ... complete typography scale
}
```

### **Component Variants:**
```typescript
// Generated CVA variants using design tokens
const buttonVariants = cva(
  "inline-flex items-center justify-center",
  {
    variants: {
      variant: {
        primary: "bg-primary text-white hover:bg-primary-600",
        secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
        // ... variants using Stage 2 colors
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base"
        // ... sizes using Stage 2 spacing
      }
    }
  }
)
```

## 🚀 **Success Criteria**

### **Universal Compatibility:**
1. **Platform Agnostic**: Generate for both web (React + Tailwind) and mobile (React Native + NativeWind)
2. **Framework Integration**: Works with any React app setup
3. **Bundler Compatible**: Compatible with Vite, Webpack, Metro
4. **Type Safety**: Full TypeScript support with comprehensive interfaces

### **Developer Experience:**
1. **shadcn/ui Compatible**: Generated components work seamlessly with shadcn/ui
2. **Consistent Patterns**: Follow unified-ui StandardHookReturn pattern
3. **Production Ready**: Include accessibility, testing, documentation
4. **Easy Customization**: Generated code is clean, readable, and customizable

### **Feature Completeness:**
1. **40+ Component Types**: Cover all major UI component categories
2. **Block-Level Compositions**: Generate complete page layouts and patterns
3. **Hook Integration**: Include data management, state, and CRUD operations
4. **Storybook Integration**: All components include interactive documentation

## 🎯 **Expected Impact**

This tool will enable:
- **Rapid Development**: Generate production-ready components in seconds
- **Design Consistency**: Apply design tokens across any React application
- **Architecture Standardization**: Use proven patterns from shadcn/ui and unified-ui
- **Cross-Platform Compatibility**: One configuration for both web and mobile
- **Developer Productivity**: Eliminate repetitive component boilerplate

The tool will transform how React applications are built by providing a universal, design-token-driven component generation system that works across platforms and frameworks.

## 📋 **Implementation Checklist**

### **Phase 1: Foundation**
- [ ] Set up component generator module structure
- [ ] Implement Jinja2 template engine
- [ ] Create design token processor from Stage 2 outputs
- [ ] Build component classification system

### **Phase 2: Core Generation Engine**
- [ ] Implement main component generator orchestrator
- [ ] Create template-based component generation
- [ ] Build hook generator following unified-ui patterns
- [ ] Add platform-specific adaptation (web/mobile)

### **Phase 3: Template Library**
- [ ] Create form component templates (Input, Select, etc.)
- [ ] Create display component templates (Card, Badge, etc.)
- [ ] Create navigation component templates (Button, Tabs, etc.)
- [ ] Create feedback component templates (Alert, Modal, etc.)
- [ ] Create data component templates (Table, List, etc.)
- [ ] Create block-level composition templates

### **Phase 4: Advanced Features**
- [ ] Add Storybook generation
- [ ] Implement test generation
- [ ] Create documentation generation
- [ ] Add accessibility validation

### **Phase 5: Integration & Testing**
- [ ] Test with Stage 2 design token outputs
- [ ] Validate generated components with shadcn/ui
- [ ] Test cross-platform compatibility
- [ ] Performance optimization and validation

This plan provides a comprehensive roadmap for building a universal component generation tool that leverages the best patterns from shadcn/ui and unified-ui to create production-ready React components for any application.