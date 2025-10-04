"""
Style Generator - Generates platform-specific style configurations.

Creates Tailwind CSS theme configuration, NativeWind configuration for React Native,
CSS custom properties, and utility classes.
"""

from typing import Dict, List, Any, Optional, Union
from .schemas import (
    DesignTokens, TailwindTheme, NativeWindTheme, CSSVariables, DesignSystemCSS,
    ColorPalette, TypographyTokens, SpacingTokens, EffectTokens
)


class StyleGenerator:
    """Generates platform-specific style configurations from design tokens."""

    def __init__(self):
        self.accessibility_contrast_ratio = 4.5  # WCAG AA standard

    def generate_tailwind_config(self, design_tokens: DesignTokens) -> TailwindTheme:
        """Generate complete Tailwind CSS theme configuration."""
        theme = TailwindTheme()

        # Generate color system
        theme.colors = self._generate_tailwind_colors(design_tokens.colors)

        # Generate typography system
        theme.fontFamily = self._generate_tailwind_fonts(design_tokens.typography)
        theme.fontSize = self._generate_tailwind_font_sizes(design_tokens.typography)
        theme.fontWeight = self._generate_tailwind_font_weights(design_tokens.typography)
        theme.lineHeight = self._generate_tailwind_line_heights(design_tokens.typography)

        # Generate spacing system
        theme.spacing = self._generate_tailwind_spacing(design_tokens.spacing)

        # Generate border radius from effects
        theme.borderRadius = self._generate_tailwind_border_radius(design_tokens.effects)

        # Generate effects
        theme.boxShadow = self._generate_tailwind_shadows(design_tokens.effects)
        theme.blur = self._generate_tailwind_blurs(design_tokens.effects)

        return theme

    def generate_native_wind_config(self, design_tokens: DesignTokens) -> NativeWindTheme:
        """Generate NativeWind configuration for React Native."""
        theme = NativeWindTheme()

        # Generate color system
        theme.colors = self._generate_native_wind_colors(design_tokens.colors)

        # Generate typography system
        theme.fonts = self._generate_native_wind_fonts(design_tokens.typography)
        theme.fontSizes = self._generate_native_wind_font_sizes(design_tokens.typography)
        theme.fontWeights = self._generate_native_wind_font_weights(design_tokens.typography)

        # Generate spacing system
        theme.spacing = self._generate_native_wind_spacing(design_tokens.spacing)

        # Generate border radius
        theme.borderRadius = self._generate_native_wind_border_radius(design_tokens.effects)

        # Generate shadows
        theme.shadows = self._generate_native_wind_shadows(design_tokens.effects)

        return theme

    def generate_css_variables(self, design_tokens: DesignTokens) -> CSSVariables:
        """Generate CSS custom properties for theming."""
        variables = CSSVariables()

        # Generate color variables
        variables.colors = self._generate_css_color_variables(design_tokens.colors)

        # Generate typography variables
        variables.typography = self._generate_css_typography_variables(design_tokens.typography)

        # Generate spacing variables
        variables.spacing = self._generate_css_spacing_variables(design_tokens.spacing)

        # Generate effect variables
        variables.effects = self._generate_css_effect_variables(design_tokens.effects)

        return variables

    def generate_design_system_css(self, design_tokens: DesignTokens, css_variables: CSSVariables) -> DesignSystemCSS:
        """Generate complete design system CSS with variables and utilities."""
        css = DesignSystemCSS()
        css.variables = css_variables

        # Generate utility classes
        css.utilities = self._generate_utility_classes(design_tokens)

        # Generate component classes
        css.component_classes = self._generate_component_classes(design_tokens)

        return css

    def _generate_tailwind_colors(self, colors: ColorPalette) -> Dict[str, Any]:
        """Generate Tailwind color configuration."""
        tailwind_colors = {}

        # Semantic colors
        if colors.semantic:
            for name, color in colors.semantic.items():
                tailwind_colors[name] = self._create_color_scale(color, name)

        # Neutral colors
        if colors.neutral:
            for name, color in colors.neutral.items():
                if name == 'white':
                    tailwind_colors['white'] = color
                elif name == 'black':
                    tailwind_colors['black'] = color
                elif name.startswith('gray-'):
                    # Ensure we have a complete gray scale
                    gray_base = color
                    tailwind_colors['gray'] = self._create_color_scale(gray_base, 'gray')

        # Brand colors
        if colors.brand:
            for name, color in colors.brand.items():
                # Generate scale for brand colors
                tailwind_colors[name] = self._create_color_scale(color, name)

        return tailwind_colors

    def _create_color_scale(self, base_color: str, name: str) -> Dict[str, str]:
        """Create a complete color scale from base color."""
        scale = {}

        # For semantic colors, create variations
        if name in ['primary', 'secondary', 'success', 'warning', 'error', 'info']:
            scale['50'] = self._lighten_color(base_color, 0.95)
            scale['100'] = self._lighten_color(base_color, 0.9)
            scale['200'] = self._lighten_color(base_color, 0.8)
            scale['300'] = self._lighten_color(base_color, 0.7)
            scale['400'] = self._lighten_color(base_color, 0.6)
            scale['500'] = base_color  # Base color
            scale['600'] = self._darken_color(base_color, 0.9)
            scale['700'] = self._darken_color(base_color, 0.8)
            scale['800'] = self._darken_color(base_color, 0.7)
            scale['900'] = self._darken_color(base_color, 0.6)
            scale['950'] = self._darken_color(base_color, 0.5)
        else:
            # For brand colors, use the base color as 500
            scale['500'] = base_color

        return scale

    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Lighten a hex color by a factor."""
        # Remove # and convert to RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        # Lighten by moving towards white
        lighter_rgb = tuple(int(255 - (255 - val) * (1 - factor)) for val in rgb)

        return f"#{lighter_rgb[0]:02x}{lighter_rgb[1]:02x}{lighter_rgb[2]:02x}"

    def _darken_color(self, hex_color: str, factor: float) -> str:
        """Darken a hex color by a factor."""
        # Remove # and convert to RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

        # Darken by moving towards black
        darker_rgb = tuple(int(val * factor) for val in rgb)

        return f"#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}"

    def _generate_tailwind_fonts(self, typography: TypographyTokens) -> Dict[str, List[str]]:
        """Generate Tailwind font family configuration."""
        fonts = {}

        # Main font family
        if typography.font_family:
            fonts['sans'] = [typography.font_family, 'system-ui', 'sans-serif']
            fonts['serif'] = ['Georgia', 'Cambria', 'Times New Roman', 'Times', 'serif']
            fonts['mono'] = ['Menlo', 'Monaco', 'Consolas', 'Liberation Mono', 'Courier New', 'monospace']

        return fonts

    def _generate_tailwind_font_sizes(self, typography: TypographyTokens) -> Dict[str, List[Union[str, float]]]:
        """Generate Tailwind font size configuration."""
        font_sizes = {}

        for name, size in typography.font_sizes.items():
            line_height = typography.line_heights.get(name, 1.5)
            font_sizes[name] = [f"{size}px", {"lineHeight": line_height}]

        return font_sizes

    def _generate_tailwind_font_weights(self, typography: TypographyTokens) -> Dict[str, int]:
        """Generate Tailwind font weight configuration."""
        return typography.font_weights

    def _generate_tailwind_line_heights(self, typography: TypographyTokens) -> Dict[str, Union[str, float]]:
        """Generate Tailwind line height configuration."""
        line_heights = {}

        for name, height in typography.line_heights.items():
            line_heights[name] = height

        return line_heights

    def _generate_tailwind_spacing(self, spacing: SpacingTokens) -> Dict[str, Union[str, int]]:
        """Generate Tailwind spacing configuration."""
        return spacing.scale

    def _generate_tailwind_border_radius(self, effects: EffectTokens) -> Dict[str, str]:
        """Generate Tailwind border radius configuration."""
        border_radius = {}

        # Standard border radius values
        border_radius['none'] = '0px'
        border_radius['sm'] = '0.125rem'
        border_radius['DEFAULT'] = '0.25rem'
        border_radius['md'] = '0.375rem'
        border_radius['lg'] = '0.5rem'
        border_radius['xl'] = '0.75rem'
        border_radius['2xl'] = '1rem'
        border_radius['3xl'] = '1.5rem'
        border_radius['full'] = '9999px'

        return border_radius

    def _generate_tailwind_shadows(self, effects: EffectTokens) -> Dict[str, str]:
        """Generate Tailwind shadow configuration."""
        shadows = {}

        # Default shadows
        shadows['sm'] = '0 1px 2px 0 rgb(0 0 0 / 0.05)'
        shadows['DEFAULT'] = '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)'
        shadows['md'] = '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)'
        shadows['lg'] = '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)'
        shadows['xl'] = '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)'
        shadows['2xl'] = '0 25px 50px -12px rgb(0 0 0 / 0.25)'

        # Custom shadows from design
        for i, shadow in enumerate(effects.shadows):
            shadow_name = f'custom-{i + 1}'
            shadow_value = f"{shadow['offsetX']}px {shadow['offsetY']}px {shadow['blur']}px {shadow['spread']}px {shadow['color']}"
            if shadow.get('inset'):
                shadow_value = f"inset {shadow_value}"
            shadows[shadow_name] = shadow_value

        return shadows

    def _generate_tailwind_blurs(self, effects: EffectTokens) -> Dict[str, str]:
        """Generate Tailwind blur configuration."""
        blurs = {}

        # Default blur values
        blurs['none'] = '0'
        blurs['sm'] = '4px'
        blurs['DEFAULT'] = '8px'
        blurs['md'] = '12px'
        blurs['lg'] = '16px'
        blurs['xl'] = '24px'
        blurs['2xl'] = '40px'
        blurs['3xl'] = '64px'

        # Custom blur values from design
        for blur in effects.blurs:
            blur_name = blur.get('name', f"blur-{blur['value']}")
            blurs[blur_name] = f"{blur['value']}px"

        return blurs

    def _generate_native_wind_colors(self, colors: ColorPalette) -> Dict[str, Any]:
        """Generate NativeWind color configuration."""
        # NativeWind uses similar structure to Tailwind but with some differences
        return self._generate_tailwind_colors(colors)

    def _generate_native_wind_fonts(self, typography: TypographyTokens) -> Dict[str, Any]:
        """Generate NativeWind font configuration."""
        fonts = {}

        if typography.font_family:
            fonts['body'] = typography.font_family
            fonts['heading'] = typography.font_family

        return fonts

    def _generate_native_wind_font_sizes(self, typography: TypographyTokens) -> Dict[str, Union[int, float]]:
        """Generate NativeWind font size configuration."""
        font_sizes = {}

        for name, size in typography.font_sizes.items():
            # Convert px to numbers for React Native
            font_sizes[name] = int(size)

        return font_sizes

    def _generate_native_wind_font_weights(self, typography: TypographyTokens) -> Dict[str, str]:
        """Generate NativeWind font weight configuration."""
        # React Native supports: 'normal', 'bold', '100', '200', ..., '900'
        weights = {}

        for name, weight in typography.font_weights.items():
            weights[name] = str(weight)

        return weights

    def _generate_native_wind_spacing(self, spacing: SpacingTokens) -> Dict[str, int]:
        """Generate NativeWind spacing configuration."""
        # Convert all spacing to integers for React Native
        native_spacing = {}

        for name, value in spacing.scale.items():
            native_spacing[name] = int(value)

        return native_spacing

    def _generate_native_wind_border_radius(self, effects: EffectTokens) -> Dict[str, int]:
        """Generate NativeWind border radius configuration."""
        border_radius = {}

        # Convert to integers for React Native
        border_radius['sm'] = 2
        border_radius['md'] = 4
        border_radius['lg'] = 8
        border_radius['xl'] = 12
        border_radius['2xl'] = 16
        border_radius['full'] = 9999

        return border_radius

    def _generate_native_wind_shadows(self, effects: EffectTokens) -> Dict[str, Any]:
        """Generate NativeWind shadow configuration."""
        shadows = {}

        # React Native shadow configuration
        shadows['sm'] = {
            'shadowOffset': {'width': 0, 'height': 1},
            'shadowOpacity': 0.05,
            'shadowRadius': 2,
            'elevation': 1
        }

        shadows['md'] = {
            'shadowOffset': {'width': 0, 'height': 4},
            'shadowOpacity': 0.1,
            'shadowRadius': 6,
            'elevation': 4
        }

        shadows['lg'] = {
            'shadowOffset': {'width': 0, 'height': 10},
            'shadowOpacity': 0.15,
            'shadowRadius': 15,
            'elevation': 10
        }

        return shadows

    def _generate_css_color_variables(self, colors: ColorPalette) -> Dict[str, str]:
        """Generate CSS custom properties for colors."""
        variables = {}

        # Semantic colors
        if colors.semantic:
            for name, color in colors.semantic.items():
                variables[f'--color-{name}'] = color
                # Generate light/dark variants
                variables[f'--color-{name}-light'] = self._lighten_color(color, 0.8)
                variables[f'--color-{name}-dark'] = self._darken_color(color, 0.8)

        # Neutral colors
        if colors.neutral:
            for name, color in colors.neutral.items():
                variables[f'--color-{name}'] = color

        # Brand colors
        if colors.brand:
            for name, color in colors.brand.items():
                variables[f'--color-{name}'] = color

        return variables

    def _generate_css_typography_variables(self, typography: TypographyTokens) -> Dict[str, str]:
        """Generate CSS custom properties for typography."""
        variables = {}

        # Font family
        variables['--font-family-base'] = typography.font_family

        # Font sizes
        for name, size in typography.font_sizes.items():
            variables[f'--font-size-{name}'] = f"{size}px"

        # Line heights
        for name, height in typography.line_heights.items():
            variables[f'--line-height-{name}'] = str(height)

        return variables

    def _generate_css_spacing_variables(self, spacing: SpacingTokens) -> Dict[str, str]:
        """Generate CSS custom properties for spacing."""
        variables = {}

        for name, value in spacing.scale.items():
            variables[f'--spacing-{name}'] = f"{value}px"

        return variables

    def _generate_css_effect_variables(self, effects: EffectTokens) -> Dict[str, str]:
        """Generate CSS custom properties for effects."""
        variables = {}

        # Shadows
        for i, shadow in enumerate(effects.shadows):
            variables[f'--shadow-{i + 1}'] = f"{shadow['offsetX']}px {shadow['offsetY']}px {shadow['blur']}px {shadow['color']}"

        return variables

    def _generate_utility_classes(self, design_tokens: DesignTokens) -> Dict[str, str]:
        """Generate custom utility classes."""
        utilities = {}

        # Color utilities
        utilities.update(self._generate_color_utilities(design_tokens.colors))

        # Spacing utilities
        utilities.update(self._generate_spacing_utilities(design_tokens.spacing))

        return utilities

    def _generate_color_utilities(self, colors: ColorPalette) -> Dict[str, str]:
        """Generate color-related utility classes."""
        utilities = {}

        # Semantic color utilities
        if colors.semantic:
            for name in colors.semantic.keys():
                utilities[f".text-{name}"] = f"color: var(--color-{name});"
                utilities[f".bg-{name}"] = f"background-color: var(--color-{name});"
                utilities[f".border-{name}"] = f"border-color: var(--color-{name});"

        return utilities

    def _generate_spacing_utilities(self, spacing: SpacingTokens) -> Dict[str, str]:
        """Generate spacing-related utility classes."""
        utilities = {}

        # Semantic spacing utilities
        if spacing.semantic:
            for name, scale_name in spacing.semantic.items():
                utilities[f".p-{name}"] = f"padding: var(--spacing-{scale_name});"
                utilities[f".m-{name}"] = f"margin: var(--spacing-{scale_name});"

        return utilities

    def _generate_component_classes(self, design_tokens: DesignTokens) -> Dict[str, str]:
        """Generate component-specific CSS classes."""
        classes = {}

        # Common component patterns
        classes.update(self._generate_button_classes(design_tokens.colors))
        classes.update(self._generate_input_classes(design_tokens.colors, design_tokens.spacing))

        return classes

    def _generate_button_classes(self, colors: ColorPalette) -> Dict[str, str]:
        """Generate button component classes."""
        classes = {}

        if colors.semantic and 'primary' in colors.semantic:
            classes['.btn-primary'] = f"""
                background-color: var(--color-primary);
                color: white;
                padding: var(--spacing-4) var(--spacing-6);
                border-radius: var(--border-radius-md);
                border: none;
                cursor: pointer;
                transition: all 0.2s ease;
            """

            classes['.btn-primary:hover'] = f"""
                background-color: var(--color-primary-dark);
                transform: translateY(-1px);
            """

        return classes

    def _generate_input_classes(self, colors: ColorPalette, spacing: SpacingTokens) -> Dict[str, str]:
        """Generate input component classes."""
        classes = {}

        classes['.input'] = f"""
            padding: var(--spacing-3) var(--spacing-4);
            border: 1px solid #e5e7eb;
            border-radius: var(--border-radius-md);
            font-size: var(--font-size-base);
            transition: border-color 0.2s ease;
        """

        classes['.input:focus'] = f"""
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px var(--color-primary-light);
        """

        return classes