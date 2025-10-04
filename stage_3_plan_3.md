# Stage 3 Option 3: Prompt-Driven Component Generation with Claude Code

## 🎯 **Vision: Precision-Guided Component Implementation**

Create a systematic approach using carefully crafted prompts to guide Claude Code in implementing individual components with precision. This approach combines human oversight with Claude's powerful code generation capabilities.

## 🏗️ **Core Strategy: Prompt-Engineering + Claude Code**

### **How It Works:**
1. **Component-Specific Prompts** - Detailed prompts for each component with exact requirements
2. **Design Token Integration** - Prompts include specific design token references from Stage 2
3. **Existing Component Utilization** - Prompts guide Claude to leverage shadcn/ui and unified-ui patterns
4. **Precision Implementation** - Each prompt focuses Claude on implementing ONLY the specific component
5. **Progressive Building** - Build components systematically with validation at each step

## 📝 **Prompt Engineering Framework**

### **Standard Prompt Structure:**
```
COMPONENT IMPLEMENTATION REQUEST

## Component Details
- Name: [Component Name]
- Type: [Form/Display/Navigation/Data/Feedback/Block]
- Category: [Specific category]
- Platform: [Web/Mobile/Both]

## Requirements
### Core Functionality
- [Specific functional requirements]
- [User interaction patterns]
- [State management needs]

### Design Integration
- Use these design tokens from Stage 2: [specific tokens]
- Follow this visual specification: [detailed visual requirements]
- Integrate with existing components: [component dependencies]

### Technical Implementation
- File location: [exact file path]
- Use existing components: [shadcn/ui components to leverage]
- Follow patterns: [unified-ui patterns to apply]
- Implement these interfaces: [TypeScript interfaces]

### Constraints
- ONLY implement this component - no extra features
- Use exact prop interface from Stage 2: [interface details]
- Follow existing code patterns in: [reference files]
- Ensure accessibility compliance
- Include comprehensive TypeScript types

### Validation
- Component renders without errors
- All props work as specified
- Design tokens applied correctly
- Integration with existing components works
```

## 🎨 **Component-Specific Prompt Templates**

### **1. Form Component Prompts**
**Example: Input Component**
```
COMPONENT IMPLEMENTATION REQUEST - Input Component

## Component Details
- Name: Input
- Type: Form Component
- Category: Text Input
- Platform: Web & Mobile

## Requirements
### Core Functionality
- Text input with validation states
- Support for different input types (text, email, password, etc.)
- Error state display with accessible error messages
- Loading state for async validation
- Helper text support

### Design Integration
Use these design tokens from Stage 2 mobile_config.json:
- Colors: primary (500: #6257db), success (500: #28b446), warning (500: #fbbb00)
- Typography: font family Poppins, sizes sm (14px), base (16px)
- Spacing: use spacing scale from Stage 2 (1: 4px, 2: 8px, 3: 13px, 4: 16px)
- Border radius: md (4px), lg (8px)

### Technical Implementation
- File location: src/components/forms/input.tsx
- Base on shadcn/ui Input component
- Follow unified-ui useComponentState pattern for state management
- Implement this interface from Stage 2: [exact Input interface]

### Constraints
- ONLY implement the Input component exactly as specified
- Use existing shadcn/ui Input as foundation
- Apply unified-ui StandardHookReturn pattern for any state management
- Must work with both web (Tailwind) and mobile (NativeWind)

### Validation Checklist
- [ ] Component renders without errors
- [ ] All input types work correctly
- [ ] Error states display properly
- [ ] Design tokens applied correctly
- [ ] Accessibility features working
```

### **2. Display Component Prompts**
**Example: Card Component**
```
COMPONENT IMPLEMENTATION REQUEST - Card Component

## Component Details
- Name: Card
- Type: Display Component
- Category: Container
- Platform: Web & Mobile

## Requirements
### Core Functionality
- Container component with header, content, and footer sections
- Support for different variants (default, elevated, outlined)
- Responsive layout with proper spacing
- Optional hover effects and transitions

### Design Integration
Use design tokens from Stage 2:
- Shadows: sm, md, lg variants
- Colors: white (#ffffff), gray shades
- Border radius: md (4px), lg (8px), xl (12px)
- Spacing: internal padding using Stage 2 spacing scale

### Technical Implementation
- File location: src/components/display/card.tsx
- Base on shadcn/ui Card component
- Implement props interface from Stage 2 component_interfaces.json
- Use CVA for variant management

### Constraints
- ONLY implement Card component - no extra features
- Must accept children prop correctly
- Variants must use design tokens for styling
- Maintain accessibility standards

### Validation
- Renders children correctly
- All variants display properly
- Design tokens applied correctly
- Responsive behavior works
```

### **3. Button Component Prompt**
```
COMPONENT IMPLEMENTATION REQUEST - Button Component

## Component Details
- Name: Button
- Type: Navigation Component
- Category: Action Button
- Platform: Web & Mobile

## Requirements
### Core Functionality
- Clickable button with multiple variants (primary, secondary, outline, ghost)
- Different sizes (sm, md, lg, xl)
- Loading state with spinner
- Disabled state with proper styling
- Support for icons and text content

### Design Integration
Use design tokens from Stage 2:
- Colors: primary (500: #6257db), success (500: #28b446), warning (500: #fbbb00)
- Typography: Poppins font family, proper font weights
- Spacing: Stage 2 spacing scale for padding (2: 8px, 3: 13px, 4: 16px, 6: 22px)
- Border radius: md (4px), lg (8px)
- Effects: shadow variants for depth

### Technical Implementation
- File location: src/components/navigation/button.tsx
- Base on shadcn/ui Button component
- Implement Button interface from Stage 2 component_interfaces.json
- Use CVA (Class Variance Authority) for variant management
- Follow unified-ui patterns for component structure

### Constraints
- ONLY implement Button component exactly as specified
- Must integrate seamlessly with existing shadcn/ui Button
- Apply design tokens for all styling
- Ensure accessibility with proper ARIA attributes
- Support both web (Tailwind) and mobile (NativeWind)

### Validation Checklist
- [ ] All variants render correctly
- [ ] Click handlers work properly
- [ ] Loading state displays spinner
- [ ] Disabled state is properly styled
- [ ] Design tokens applied correctly
- [ ] Accessibility attributes present
```

### **4. Data Component Prompt**
```
COMPONENT IMPLEMENTATION REQUEST - DataTable Component

## Component Details
- Name: DataTable
- Type: Data Component
- Category: Table Display
- Platform: Web & Mobile

## Requirements
### Core Functionality
- Sortable columns with visual indicators
- Filterable data with search functionality
- Paginated results with navigation controls
- Responsive design for mobile devices
- Loading and error states
- Row selection capabilities

### Design Integration
Use design tokens from Stage 2:
- Colors: primary for headers, gray shades for borders, success/warning for states
- Typography: proper font sizes and weights from Stage 2 typography scale
- Spacing: consistent padding and margins using Stage 2 spacing scale
- Border radius: subtle rounded corners for modern look
- Effects: hover states and transitions

### Technical Implementation
- File location: src/components/data/data-table.tsx
- Base on unified-ui DataTable pattern (reference: /Users/tbardale/projects/unified-ui/src/iamplus/components/table/data-table.tsx)
- Use TanStack Table for advanced table functionality
- Implement DataTable interface from Stage 2 component_interfaces.json
- Follow unified-ui useTableState pattern for state management

### Constraints
- ONLY implement DataTable component - no extra features
- Must leverage existing unified-ui patterns for consistency
- Apply design tokens for all visual styling
- Ensure accessibility with proper table semantics
- Support both web and mobile platforms

### Validation Checklist
- [ ] Data renders correctly in table format
- [ ] Sorting works on all sortable columns
- [ ] Filtering functionality works
- [ ] Pagination controls function properly
- [ ] Mobile responsive design works
- [ ] Loading and error states display
- [ ] Design tokens applied correctly
```

## 🔄 **Implementation Workflow**

### **Phase 1: Prompt Preparation**
1. **Extract Component Data** - Get interface from Stage 2 component_interfaces.json
2. **Identify Design Tokens** - Extract relevant tokens from mobile_config.json and web_config.json
3. **Map Dependencies** - Identify shadcn/ui components to leverage
4. **Craft Specific Prompt** - Create detailed prompt using the template

### **Phase 2: Claude Code Implementation**
1. **Execute Prompt** - Run Claude Code with the prepared prompt
2. **Monitor Implementation** - Ensure Claude follows constraints exactly
3. **Validate Output** - Check against validation checklist
4. **Iterate if Needed** - Refine prompt and re-run if issues

### **Phase 3: Integration Testing**
1. **Component Testing** - Test component in isolation
2. **Integration Testing** - Test with other components
3. **Design Validation** - Verify design token application
4. **Accessibility Testing** - Ensure WCAG compliance

## 📁 **File Organization Strategy**

```
stage_3_prompt_driven/
├── prompts/
│   ├── forms/
│   │   ├── input-prompt.md
│   │   ├── select-prompt.md
│   │   ├── checkbox-prompt.md
│   │   ├── textarea-prompt.md
│   │   └── form-prompt.md
│   ├── display/
│   │   ├── card-prompt.md
│   │   ├── badge-prompt.md
│   │   ├── avatar-prompt.md
│   │   ├── skeleton-prompt.md
│   │   └── divider-prompt.md
│   ├── navigation/
│   │   ├── button-prompt.md
│   │   ├── tabs-prompt.md
│   │   ├── pagination-prompt.md
│   │   └── breadcrumb-prompt.md
│   ├── feedback/
│   │   ├── alert-prompt.md
│   │   ├── modal-prompt.md
│   │   ├── toast-prompt.md
│   │   └── tooltip-prompt.md
│   ├── data/
│   │   ├── table-prompt.md
│   │   ├── list-prompt.md
│   │   └── chart-prompt.md
│   └── blocks/
│       ├── dashboard-prompt.md
│       ├── auth-form-prompt.md
│       └── settings-page-prompt.md
├── implementation_tracker.md
├── validation_checklist.md
└── prompt_templates.md
```

## 🎯 **Component Implementation Order**

### **Priority 1: Foundation Components**
1. **Button** - Core interaction component used everywhere
2. **Input** - Essential form component for data entry
3. **Card** - Fundamental display component for content grouping
4. **Alert** - Critical feedback component for user notifications

### **Priority 2: Form Components**
5. **Select** - Dropdown selection for choices
6. **Checkbox** - Toggle selection for multiple options
7. **Textarea** - Multi-line input for longer text
8. **Form** - Form container with validation integration

### **Priority 3: Display Components**
9. **Badge** - Status indicators and labels
10. **Avatar** - User images and profile pictures
11. **Skeleton** - Loading states for better UX
12. **Divider** - Visual separation between content

### **Priority 4: Navigation Components**
13. **Tabs** - Content organization and switching
14. **Pagination** - Data navigation controls
15. **Breadcrumb** - Navigation hierarchy display

### **Priority 5: Advanced Components**
16. **DataTable** - Complex data display with sorting/filtering
17. **Modal** - Overlay dialogs and popups
18. **Toast** - Notification system
19. **Tooltip** - Contextual help and information

## 📊 **Design Token Reference Guide**

### **Color System (from Stage 2)**
```json
{
  "primary": {
    "50": "#f7f6fd", "100": "#efeefb", "200": "#dfddf7",
    "300": "#cfccf4", "400": "#c0bbf0", "500": "#6257db",
    "600": "#584ec5", "700": "#4e45af", "800": "#443c99",
    "900": "#3a3483", "950": "#312b6d"
  },
  "success": {
    "50": "#f4fbf5", "100": "#e9f7ec", "200": "#d4f0da",
    "300": "#bee8c7", "400": "#a9e1b5", "500": "#28b446",
    "600": "#24a23f", "700": "#209038", "800": "#1c7d31",
    "900": "#186c2a", "950": "#145a23"
  },
  "warning": {
    "50": "#fefbf2", "100": "#fef8e5", "200": "#fef1cc",
    "300": "#fdeab2", "400": "#fde399", "500": "#fbbb00",
    "600": "#e1a800", "700": "#c89500", "800": "#af8200",
    "900": "#967000", "950": "#7d5d00"
  }
}
```

### **Typography System (from Stage 2)**
```json
{
  "fontFamily": { "Poppins": ["Poppins", "sans-serif"] },
  "fontSize": {
    "caption": [12, { "lineHeight": 1.4 }],
    "body": [16, { "lineHeight": 1.5 }],
    "heading-2": [36, { "lineHeight": 1.7 }],
    "heading-1": [40, { "lineHeight": 1.7 }],
    "xs": [12, { "lineHeight": 1.4 }],
    "sm": [14, { "lineHeight": 1.5 }],
    "base": [16, { "lineHeight": 1.5 }],
    "lg": [18, { "lineHeight": 1.6 }],
    "xl": [20, { "lineHeight": 1.6 }],
    "2xl": [24, { "lineHeight": 1.7 }],
    "3xl": [30, { "lineHeight": 1.7 }],
    "4xl": [36, { "lineHeight": 1.7 }]
  },
  "fontWeight": { "regular": 400, "black": 900 }
}
```

### **Spacing System (from Stage 2)**
```json
{
  "0": 0, "px": 1, "0.5": 2, "1": 4, "1.5": 6, "2": 8,
  "2.5": 10, "3": 13, "3.5": 14, "4": 16, "5": 19,
  "6": 22, "7": 28, "8": 32, "9": 36, "10": 40,
  "11": 44, "12": 47, "14": 56, "16": 63, "20": 80,
  "24": 95, "28": 112, "32": 128, "36": 144, "40": 160
}
```

### **Border Radius System (from Stage 2)**
```json
{
  "sm": 2, "md": 4, "lg": 8, "xl": 12, "2xl": 16, "full": 9999
}
```

## 🚀 **Success Criteria**

### **Implementation Quality:**
1. **Precision Implementation** - Each component implements exactly what's requested
2. **Design Token Compliance** - All components use Stage 2 design tokens correctly
3. **Pattern Consistency** - All components follow unified-ui patterns
4. **Type Safety** - Full TypeScript coverage with proper interfaces

### **Integration Success:**
1. **shadcn/ui Compatibility** - Components work seamlessly with existing shadcn components
2. **Cross-Platform Support** - Components work on both web and mobile
3. **Accessibility Compliance** - WCAG 2.1 AA compliance
4. **Performance Optimization** - Efficient rendering and state management

### **Development Efficiency:**
1. **Rapid Implementation** - Each component implemented in single Claude Code session
2. **Minimal Iteration** - Well-crafted prompts reduce back-and-forth
3. **Consistent Quality** - Standardized prompts ensure consistent output
4. **Progressive Building** - Components build on each other successfully

## 📊 **Comparison with Other Options**

| Aspect | Option 1 (Template Generator) | Option 2 (Unified UI Copy) | **Option 3 (Prompt-Driven)** |
|--------|-------------------------------|----------------------------|------------------------------|
| **Control** | Medium | Low | **High** |
| **Quality** | Good | Excellent | **Excellent** |
| **Speed** | Fast | Medium | **Fast** |
| **Flexibility** | Medium | Low | **High** |
| **Maintenance** | High | Low | **Medium** |
| **Learning** | High | Low | **Medium** |
| **Precision** | Medium | Low | **High** |
| **Iterative** | Difficult | Difficult | **Easy** |

## 🎯 **Why Option 3 is Powerful**

1. **Human Oversight** - You control exactly what gets implemented
2. **Claude's Strength** - Leverages Claude's code generation capabilities
3. **Precision Focus** - Each prompt focuses on one specific component
4. **Iterative Refinement** - Prompts can be refined based on results
5. **Quality Assurance** - Each component validated before moving to next
6. **Learning Opportunity** - You learn component patterns through the process

## 📋 **Implementation Checklist**

### **Phase 1: Foundation Setup**
- [ ] Create prompt directory structure
- [ ] Develop standard prompt template
- [ ] Create component-specific prompt templates
- [ ] Set up validation checklist system

### **Phase 2: Core Components**
- [ ] Implement Button component with prompt-driven approach
- [ ] Implement Input component with design token integration
- [ ] Implement Card component with variant support
- [ ] Implement Alert component with state management

### **Phase 3: Component Library**
- [ ] Implement all form components using prompts
- [ ] Implement all display components using prompts
- [ ] Implement all navigation components using prompts
- [ ] Implement feedback and data components

### **Phase 4: Validation & Integration**
- [ ] Test all components with design tokens
- [ ] Validate cross-platform compatibility
- [ ] Ensure accessibility compliance
- [ ] Create component documentation

### **Phase 5: Advanced Features**
- [ ] Implement block-level compositions
- [ ] Create storybook integration
- [ ] Add comprehensive testing
- [ ] Optimize for performance

## 🔄 **Prompt Refinement Process**

### **Initial Prompt Creation:**
1. **Extract Requirements** - From Stage 2 component interfaces
2. **Map Design Tokens** - Identify specific tokens needed
3. **Identify Dependencies** - List existing components to leverage
4. **Write Initial Prompt** - Using standard template structure

### **Testing & Refinement:**
1. **Execute Prompt** - Run Claude Code with initial prompt
2. **Analyze Output** - Compare against requirements and constraints
3. **Identify Gaps** - Note missing features or incorrect implementations
4. **Refine Prompt** - Add specific instructions for identified issues
5. **Re-test** - Execute refined prompt and validate improvements

### **Prompt Optimization:**
1. **Document Patterns** - Record successful prompt patterns
2. **Create Templates** - Build reusable prompt templates
3. **Standardize Language** - Use consistent terminology across prompts
4. **Validate Consistency** - Ensure similar components follow similar patterns

This approach combines the best of both worlds: precise human control with Claude's powerful implementation capabilities, resulting in high-quality components that exactly match your requirements while maintaining flexibility for iterative improvement.