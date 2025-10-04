"""
Interface Builder - Generates TypeScript interfaces for components.

Creates component prop interfaces, variant types, style-related type definitions,
and helper type utilities for the design system.
"""

from typing import Dict, List, Any, Optional, Set, Union
from .schemas import (
    ComponentDefinition, ComponentVariant, ComponentInterface, ComponentCategory,
    DesignTokens, ConversionOutput
)


class InterfaceBuilder:
    """Builds TypeScript interfaces for components from design definitions."""

    def __init__(self):
        self.type_mappings = {
            'string': 'string',
            'number': 'number',
            'boolean': 'boolean',
            'text': 'string',
            'rectangle': 'React.HTMLAttributes<HTMLElement>',
            'group': 'React.HTMLAttributes<HTMLDivElement>',
            'frame': 'React.HTMLAttributes<HTMLDivElement>',
            'vector': 'React.SVGProps<SVGSVGElement>'
        }

    def build_component_interfaces(self, component_catalog: List[ComponentDefinition]) -> List[ComponentInterface]:
        """Build TypeScript interfaces for all components."""
        interfaces = []

        for component in component_catalog:
            interface = self._build_component_interface(component)
            if interface:
                interfaces.append(interface)

        return interfaces

    def _build_component_interface(self, component: ComponentDefinition) -> Optional[ComponentInterface]:
        """Build a TypeScript interface for a single component."""
        if not component.name:
            return None

        # Generate interface name
        interface_name = self._generate_interface_name(component.name)

        # Extract props
        props = self._extract_component_props(component)

        # Generate variants
        variants = self._generate_variant_types(component.variants)

        # Determine base interfaces
        extends = self._determine_base_interfaces(component)

        return ComponentInterface(
            name=interface_name,
            description=component.description or f"{component.name} component interface",
            props=props,
            variants=variants,
            extends=extends,
            generics=[]
        )

    def _generate_interface_name(self, component_name: str) -> str:
        """Generate TypeScript interface name from component name."""
        # Convert kebab-case to PascalCase
        name_parts = component_name.split('-')
        pascal_case = ''.join(part.capitalize() for part in name_parts)

        # Remove invalid characters and ensure it starts with a letter
        clean_name = ''.join(c for c in pascal_case if c.isalnum() or c == '_')

        if clean_name and clean_name[0].isdigit():
            clean_name = f'Component{clean_name}'

        return clean_name or 'Component'

    def _extract_component_props(self, component: ComponentDefinition) -> Dict[str, Any]:
        """Extract and type component props from component definition."""
        props = {}

        # Common props for all components
        common_props = {
            'className': 'string',
            'style': 'React.CSSProperties',
            'children': 'React.ReactNode',
            'id': 'string',
            'testId': 'string'
        }

        # Extract props from component data
        if component.props:
            extracted_props = self._extract_props_from_data(component.props)
            props.update(extracted_props)

        # Add common props
        props.update(common_props)

        # Add category-specific props
        category_props = self._get_category_specific_props(component.category)
        props.update(category_props)

        return props

    def _extract_props_from_data(self, props_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract prop definitions from raw component data."""
        props = {}

        # Extract dimension props
        if 'width' in props_data:
            props['width'] = 'string | number'
        if 'height' in props_data:
            props['height'] = 'string | number'

        # Extract position props
        if 'x' in props_data or 'y' in props_data:
            props['position'] = '{ x?: number; y?: number }'

        # Extract style props
        if 'fills' in props_data:
            props['backgroundColor'] = 'string'
            props['backgroundOpacity'] = 'number'

        if 'strokes' in props_data:
            props['borderColor'] = 'string'
            props['borderWidth'] = 'number'

        if 'cornerRadius' in props_data:
            props['borderRadius'] = 'string | number'

        # Extract text props
        if 'font_family' in props_data or 'fontFamily' in props_data:
            props['fontFamily'] = 'string'
        if 'font_size' in props_data or 'fontSize' in props_data:
            props['fontSize'] = 'string | number'
        if 'font_weight' in props_data or 'fontWeight' in props_data:
            props['fontWeight'] = 'string | number'
        if 'text' in props_data:
            props['text'] = 'string'
        if 'text_align' in props_data or 'textAlign' in props_data:
            props['textAlign'] = 'left | center | right | justify'

        # Extract visibility
        if 'visible' in props_data:
            props['visible'] = 'boolean'

        return props

    def _get_category_specific_props(self, category: ComponentCategory) -> Dict[str, str]:
        """Get props specific to component category."""
        if category == ComponentCategory.BUTTONS:
            return {
                'variant': 'primary | secondary | outline | ghost',
                'size': 'sm | md | lg',
                'disabled': 'boolean',
                'loading': 'boolean',
                'onClick': '(event: React.MouseEvent) => void',
                'type': "'button' | 'submit' | 'reset'"
            }
        elif category == ComponentCategory.INTERACTIVE:
            return {
                'interactive': 'boolean',
                'hover': 'boolean',
                'focus': 'boolean',
                'active': 'boolean',
                'onPress': '() => void',
                'onHover': '(hovering: boolean) => void'
            }
        elif category == ComponentCategory.DISPLAY:
            return {
                'display': 'block | inline | inline-block | flex | grid | none',
                'overflow': 'visible | hidden | scroll | auto',
                'opacity': 'number'
            }

        return {}

    def _generate_variant_types(self, variants: List[ComponentVariant]) -> List[Dict[str, Any]]:
        """Generate TypeScript types for component variants."""
        variant_types = []

        if not variants:
            return variant_types

        # Extract variant properties
        variant_props = set()
        for variant in variants:
            variant_props.update(variant.props.keys())

        # Generate variant type definitions
        for prop_name in variant_props:
            prop_values = []
            for variant in variants:
                if prop_name in variant.props:
                    value = variant.props[prop_name]
                    if isinstance(value, str):
                        prop_values.append(f"'{value}'")
                    elif isinstance(value, bool):
                        prop_values.append(str(value).lower())
                    elif isinstance(value, (int, float)):
                        prop_values.append(str(value))

            if prop_values:
                variant_types.append({
                    'name': prop_name,
                    'type': f"{prop_name}: {' | '.join(prop_values)}",
                    'description': f"Variant property for {prop_name}"
                })

        return variant_types

    def _determine_base_interfaces(self, component: ComponentDefinition) -> List[str]:
        """Determine base interfaces for component interface."""
        extends = []

        # Always extend HTML attributes
        extends.append('React.HTMLAttributes<HTMLElement>')

        # Category-specific interfaces
        if component.category == ComponentCategory.BUTTONS:
            extends.append('ButtonProps')
        elif component.category == ComponentCategory.INTERACTIVE:
            extends.append('InteractiveProps')

        # Type-specific interfaces
        if component.type == 'text':
            extends.append('TextProps')
        elif component.type in ['rectangle', 'frame']:
            extends.append('LayoutProps')

        return extends

    def generate_style_types(self, design_tokens: DesignTokens) -> Dict[str, Any]:
        """Generate style-related type definitions."""
        style_types = {}

        # Color types
        style_types['colors'] = self._generate_color_types(design_tokens.colors)

        # Typography types
        style_types['typography'] = self._generate_typography_types(design_tokens.typography)

        # Spacing types
        style_types['spacing'] = self._generate_spacing_types(design_tokens.spacing)

        # Effect types
        style_types['effects'] = self._generate_effect_types(design_tokens.effects)

        return style_types

    def _generate_color_types(self, colors) -> Dict[str, Any]:
        """Generate color type definitions."""
        color_types = {}

        # Semantic color types
        if colors.semantic:
            semantic_colors = []
            for name in colors.semantic.keys():
                semantic_colors.append(f"'{name}'")

            if semantic_colors:
                color_types['semantic'] = f"SemanticColor = {' | '.join(semantic_colors)}"

        # Neutral color types
        if colors.neutral:
            neutral_colors = []
            for name in colors.neutral.keys():
                neutral_colors.append(f"'{name}'")

            if neutral_colors:
                color_types['neutral'] = f"NeutralColor = {' | '.join(neutral_colors)}"

        # Brand color types
        if colors.brand:
            brand_colors = []
            for name in colors.brand.keys():
                brand_colors.append(f"'{name}'")

            if brand_colors:
                color_types['brand'] = f"BrandColor = {' | '.join(brand_colors)}"

        return color_types

    def _generate_typography_types(self, typography) -> Dict[str, Any]:
        """Generate typography type definitions."""
        typography_types = {}

        # Font size types
        if typography.font_sizes:
            font_sizes = []
            for name in typography.font_sizes.keys():
                font_sizes.append(f"'{name}'")

            if font_sizes:
                typography_types['fontSize'] = f"FontSize = {' | '.join(font_sizes)}"

        # Font weight types
        if typography.font_weights:
            font_weights = []
            for name in typography.font_weights.keys():
                font_weights.append(f"'{name}'")

            if font_weights:
                typography_types['fontWeight'] = f"FontWeight = {' | '.join(font_weights)}"

        return typography_types

    def _generate_spacing_types(self, spacing) -> Dict[str, Any]:
        """Generate spacing type definitions."""
        spacing_types = {}

        # Spacing scale types
        if spacing.scale:
            spacing_values = []
            for name in spacing.scale.keys():
                spacing_values.append(f"'{name}'")

            if spacing_values:
                spacing_types['scale'] = f"SpacingScale = {' | '.join(spacing_values)}"

        # Semantic spacing types
        if spacing.semantic:
            semantic_spacing = []
            for name in spacing.semantic.keys():
                semantic_spacing.append(f"'{name}'")

            if semantic_spacing:
                spacing_types['semantic'] = f"SemanticSpacing = {' | '.join(semantic_spacing)}"

        return spacing_types

    def _generate_effect_types(self, effects) -> Dict[str, Any]:
        """Generate effect type definitions."""
        effect_types = {}

        # Shadow types
        if effects.shadows:
            shadow_names = []
            for i in range(len(effects.shadows)):
                shadow_names.append(f"'shadow-{i + 1}'")

            if shadow_names:
                effect_types['shadows'] = f"Shadow = {' | '.join(shadow_names)}"

        return effect_types

    def generate_utility_types(self) -> Dict[str, str]:
        """Generate helper type utilities."""
        utilities = {}

        # Common utility types
        utilities['ComponentSize'] = "'xs' | 'sm' | 'md' | 'lg' | 'xl'"
        utilities['ComponentVariant'] = "'default' | 'primary' | 'secondary' | 'outline'"
        utilities['AnimationState'] = "'idle' | 'loading' | 'success' | 'error'"
        utilities['InteractionState'] = "'none' | 'hover' | 'focus' | 'active' | 'disabled'"

        # Responsive types
        utilities['ResponsiveValue'] = "T | T[] | { sm?: T; md?: T; lg?: T; xl?: T }"
        utilities['Breakpoint'] = "'sm' | 'md' | 'lg' | 'xl' | '2xl'"

        return utilities

    def generate_type_definitions_file(self, component_interfaces: List[ComponentInterface],
                                     design_tokens: DesignTokens) -> str:
        """Generate complete TypeScript definitions file."""
        lines = []

        # File header
        lines.extend([
            "/*",
            " * Design System Component Types",
            " * Generated from Stage 2: Design System Converter",
            " */",
            "",
            "import React from 'react';",
            "",
            "// ===========================================",
            "// Base Component Interfaces",
            "// ===========================================",
            ""
        ])

        # Base interfaces
        lines.extend(self._generate_base_interfaces())

        # Style types
        style_types = self.generate_style_types(design_tokens)
        lines.extend([
            "// ===========================================",
            "// Style Type Definitions",
            "// ===========================================",
            ""
        ])

        for category, types in style_types.items():
            lines.append(f"// {category.title()} Types")
            for type_name, type_def in types.items():
                lines.append(f"export type {type_def};")
            lines.append("")

        # Utility types
        utility_types = self.generate_utility_types()
        lines.extend([
            "// ===========================================",
            "// Utility Types",
            "// ===========================================",
            ""
        ])

        for type_name, type_def in utility_types.items():
            lines.append(f"export type {type_name} = {type_def};")
        lines.append("")

        # Component interfaces
        lines.extend([
            "// ===========================================",
            "// Component Interfaces",
            "// ===========================================",
            ""
        ])

        for interface in component_interfaces:
            lines.extend(self._generate_interface_definition(interface))
            lines.append("")

        return "\n".join(lines)

    def _generate_base_interfaces(self) -> List[str]:
        """Generate base component interfaces."""
        return [
            "// Base component props",
            "export interface BaseComponentProps {",
            "  className?: string;",
            "  style?: React.CSSProperties;",
            "  children?: React.ReactNode;",
            "  id?: string;",
            "  testId?: string;",
            "}",
            "",
            "// Interactive component props",
            "export interface InteractiveProps extends BaseComponentProps {",
            "  interactive?: boolean;",
            "  disabled?: boolean;",
            "  onClick?: (event: React.MouseEvent) => void;",
            "  onFocus?: (event: React.FocusEvent) => void;",
            "  onBlur?: (event: React.FocusEvent) => void;",
            "}",
            "",
            "// Button component props",
            "export interface ButtonProps extends InteractiveProps {",
            "  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';",
            "  size?: 'sm' | 'md' | 'lg';",
            "  loading?: boolean;",
            "  type?: 'button' | 'submit' | 'reset';",
            "}",
            "",
            "// Text component props",
            "export interface TextProps extends BaseComponentProps {",
            "  as?: keyof React.ReactHTML;",
            "  variant?: string;",
            "  weight?: string;",
            "  size?: string;",
            "  color?: string;",
            "  align?: 'left' | 'center' | 'right' | 'justify';",
            "}",
            "",
            "// Layout component props",
            "export interface LayoutProps extends BaseComponentProps {",
            "  display?: React.CSSProperties['display'];",
            "  position?: React.CSSProperties['position'];",
            "  overflow?: React.CSSProperties['overflow'];",
            "  width?: string | number;",
            "  height?: string | number;",
            "  minWidth?: string | number;",
            "  minHeight?: string | number;",
            "  maxWidth?: string | number;",
            "  maxHeight?: string | number;",
            "}",
            ""
        ]

    def _generate_interface_definition(self, interface: ComponentInterface) -> List[str]:
        """Generate TypeScript interface definition."""
        lines = []

        # Interface declaration
        extends_clause = f" extends {', '.join(interface.extends)}" if interface.extends else ""
        lines.append(f"export interface {interface.name}{extends_clause} {{")

        # JSDoc comment
        if interface.description:
            lines.append(f"  /** {interface.description} */")

        # Props
        for prop_name, prop_type in interface.props.items():
            lines.append(f"  {prop_name}?: {prop_type};")

        lines.append("}")

        # Variant types (if any)
        if interface.variants:
            lines.append("")
            lines.append(f"// {interface.name} Variant Types")
            for variant in interface.variants:
                lines.append(f"export type {interface.name}{variant['name'].title()} = {variant['type']};")

        return lines