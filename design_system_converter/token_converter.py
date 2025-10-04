"""
Token Converter - Converts design tokens to platform-agnostic format.

Handles color token conversion, typography system generation, spacing scale creation,
and effect token processing.
"""

import re
import math
from typing import Dict, List, Any, Tuple, Optional, Union
from .schemas import (
    DesignTokens, ColorPalette, TypographyTokens, SpacingTokens, EffectTokens,
    ComponentDefinition, ComponentCategory
)


class TokenConverter:
    """Converts raw design tokens to platform-agnostic format."""

    def __init__(self):
        self.base_spacing = 4  # Base unit for modular scale
        self.typography_scale = [0.75, 0.875, 1, 1.125, 1.25, 1.5, 1.875, 2.25, 3]

    def convert_tokens(self, design_tokens: Dict[str, Any]) -> DesignTokens:
        """Convert all design tokens to standardized format."""
        return DesignTokens(
            colors=self.convert_color_tokens(design_tokens.get("colors", {})),
            typography=self.convert_typography_tokens(design_tokens.get("typography", {})),
            spacing=self.convert_spacing_tokens(design_tokens.get("spacing", {})),
            effects=self.convert_effect_tokens(design_tokens.get("effects", {}))
        )

    def convert_color_tokens(self, color_data: Dict[str, Any]) -> ColorPalette:
        """Convert color tokens to semantic, neutral, and brand palettes."""
        colors = ColorPalette()

        # Extract colors from the raw data
        all_colors = self._extract_all_colors(color_data)

        # Separate into semantic, neutral, and brand colors
        colors.semantic = self._categorize_semantic_colors(all_colors)
        colors.neutral = self._categorize_neutral_colors(all_colors)
        colors.brand = self._categorize_brand_colors(all_colors)

        return colors

    def _extract_all_colors(self, color_data: Dict[str, Any]) -> Dict[str, str]:
        """Extract all colors from various sources."""
        colors = {}

        # From color data structure
        if isinstance(color_data, dict):
            for key, value in color_data.items():
                if isinstance(value, dict):
                    colors.update(self._extract_all_colors(value))
                elif isinstance(value, str) and self._is_color_hex(value):
                    colors[key] = value

        return colors

    def _is_color_hex(self, value: str) -> bool:
        """Check if string is a hex color."""
        return bool(re.match(r'^#[0-9A-Fa-f]{6}$', value))

    def _categorize_semantic_colors(self, all_colors: Dict[str, str]) -> Dict[str, str]:
        """Categorize semantic colors (primary, secondary, success, error, etc.)."""
        semantic = {}

        # Common semantic color patterns
        semantic_patterns = {
            'primary': ['primary', 'main', 'brand', 'accent'],
            'secondary': ['secondary', 'subtle', 'muted'],
            'success': ['success', 'valid', 'positive', 'green'],
            'warning': ['warning', 'caution', 'yellow'],
            'error': ['error', 'danger', 'invalid', 'red'],
            'info': ['info', 'information', 'blue']
        }

        for semantic_name, patterns in semantic_patterns.items():
            for color_name, color_value in all_colors.items():
                if any(pattern in color_name.lower() for pattern in patterns):
                    semantic[semantic_name] = color_value
                    break

        return semantic

    def _categorize_neutral_colors(self, all_colors: Dict[str, str]) -> Dict[str, str]:
        """Categorize neutral colors (grays, whites, blacks)."""
        neutral = {}

        # Extract neutral colors based on common patterns
        neutral_colors = {}
        for name, value in all_colors.items():
            name_lower = name.lower()
            if any(keyword in name_lower for keyword in ['gray', 'grey', 'neutral', 'stone', 'slate']):
                neutral_colors[name] = value
            elif value.lower() in ['#ffffff', '#000000']:
                neutral_colors[name] = value

        # Create a scale if multiple neutrals exist
        if neutral_colors:
            neutral['white'] = '#ffffff'
            neutral['black'] = '#000000'

            # Add gray scale if available
            gray_scale = self._create_gray_scale(neutral_colors)
            neutral.update(gray_scale)

        return neutral

    def _create_gray_scale(self, neutral_colors: Dict[str, str]) -> Dict[str, str]:
        """Create a consistent gray scale from available neutral colors."""
        gray_scale = {}

        # Try to identify existing scale (50, 100, 200, etc.)
        scale_pattern = re.compile(r'(\d+)')
        for name, value in neutral_colors.items():
            match = scale_pattern.search(name)
            if match:
                shade = int(match.group(1))
                gray_scale[f'gray-{shade}'] = value

        return gray_scale

    def _categorize_brand_colors(self, all_colors: Dict[str, str]) -> Dict[str, str]:
        """Categorize brand-specific colors."""
        brand = {}

        # Colors that don't fit semantic or neutral categories
        semantic_neutral_keys = set()
        semantic_neutral_keys.update(self._categorize_semantic_colors(all_colors).keys())
        semantic_neutral_keys.update(self._categorize_neutral_colors(all_colors).keys())

        for name, value in all_colors.items():
            if name not in semantic_neutral_keys:
                brand[name] = value

        return brand

    def convert_typography_tokens(self, typo_data: Dict[str, Any]) -> TypographyTokens:
        """Convert typography tokens to standardized format."""
        typography = TypographyTokens()

        # Extract font family
        typography.font_family = typo_data.get('fontFamily', 'Poppins')

        # Extract and generate font sizes
        font_sizes = typo_data.get('fontSizes', {})
        typography.font_sizes = self._generate_font_scale(font_sizes)

        # Extract font weights
        font_weights = typo_data.get('fontWeights', {})
        typography.font_weights = self._normalize_font_weights(font_weights)

        # Generate line heights
        typography.line_heights = self._generate_line_heights(typography.font_sizes)

        return typography

    def _generate_font_scale(self, font_sizes: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        """Generate a complete font size scale from available sizes."""
        scale = {}

        # Standard font size names in Tailwind
        size_names = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl', '7xl', '8xl', '9xl']

        # Use provided sizes or generate from base
        if font_sizes:
            # Map provided sizes to scale
            for name, value in font_sizes.items():
                if isinstance(value, (int, float)):
                    scale[name] = value

            # Fill in missing sizes using scale
            base_size = scale.get('base', 16)
            for i, size_name in enumerate(size_names):
                if size_name not in scale:
                    scale[size_name] = base_size * self.typography_scale[min(i, len(self.typography_scale) - 1)]
        else:
            # Generate complete scale from base 16px
            base_size = 16
            for i, size_name in enumerate(size_names):
                scale[size_name] = base_size * self.typography_scale[min(i, len(self.typography_scale) - 1)]

        return scale

    def _normalize_font_weights(self, font_weights: Dict[str, int]) -> Dict[str, int]:
        """Normalize font weights to standard web weights."""
        normalized = {}

        # Standard web font weights
        standard_weights = {
            'thin': 100,
            'extralight': 200,
            'light': 300,
            'normal': 400,
            'medium': 500,
            'semibold': 600,
            'bold': 700,
            'extrabold': 800,
            'black': 900
        }

        # Use provided weights or generate standard scale
        if font_weights:
            for name, value in font_weights.items():
                # Normalize to nearest standard weight
                normalized_weight = min(standard_weights.values(), key=lambda x: abs(x - value))
                normalized[name] = normalized_weight
        else:
            # Generate standard scale
            normalized = standard_weights

        return normalized

    def _generate_line_heights(self, font_sizes: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        """Generate appropriate line heights for font sizes."""
        line_heights = {}

        for name, size in font_sizes.items():
            # Calculate optimal line height based on font size
            # Smaller fonts need tighter line heights, larger fonts need more space
            if size <= 12:
                line_height = 1.4
            elif size <= 16:
                line_height = 1.5
            elif size <= 20:
                line_height = 1.6
            else:
                line_height = 1.7

            # Convert to unitless value
            line_heights[name] = line_height

        return line_heights

    def convert_spacing_tokens(self, spacing_data: Dict[str, Any]) -> SpacingTokens:
        """Convert spacing tokens to modular scale."""
        spacing = SpacingTokens()

        # Extract spacing values and create scale
        all_spacing = self._extract_spacing_values(spacing_data)
        spacing.scale = self._create_spacing_scale(all_spacing)
        spacing.semantic = self._create_semantic_spacing(spacing.scale)

        return spacing

    def _extract_spacing_values(self, spacing_data: Dict[str, Any]) -> List[int]:
        """Extract all spacing values from various sources."""
        values = []

        def extract_recursive(data):
            if isinstance(data, dict):
                for value in data.values():
                    extract_recursive(value)
            elif isinstance(data, (int, float)) and data > 0:
                values.append(int(data))

        extract_recursive(spacing_data)
        return sorted(set(values))

    def _create_spacing_scale(self, values: List[int]) -> Dict[str, int]:
        """Create a modular spacing scale from available values."""
        scale = {}

        # Standard Tailwind spacing names
        spacing_names = ['0', 'px', '0.5', '1', '1.5', '2', '2.5', '3', '3.5', '4', '5', '6', '7', '8', '9', '10', '11', '12', '14', '16', '20', '24', '28', '32', '36', '40', '44', '48', '52', '56', '60', '64', '72', '80', '96']

        # Start with base unit and generate scale
        base_unit = self.base_spacing

        # Generate complete scale
        for i, name in enumerate(spacing_names):
            if name == '0':
                scale[name] = 0
            elif name == 'px':
                scale[name] = 1
            elif '.' in name:
                # Handle fractional values
                decimal = float(name)
                scale[name] = int(base_unit * decimal)
            else:
                # Handle integer values
                scale[name] = base_unit * int(name)

        # Override with actual values from design if they exist
        for value in values:
            # Find closest scale value
            closest_name = min(scale.keys(), key=lambda x: abs(scale[x] - value))
            if abs(scale[closest_name] - value) <= base_unit:  # Within one unit tolerance
                scale[closest_name] = value

        return scale

    def _create_semantic_spacing(self, scale: Dict[str, int]) -> Dict[str, str]:
        """Create semantic spacing tokens from scale."""
        semantic = {}

        # Common semantic spacing patterns
        semantic_patterns = {
            'xs': ['px', '0.5', '1'],
            'sm': ['1.5', '2'],
            'md': ['3', '4'],
            'lg': ['6', '8'],
            'xl': ['10', '12']
        }

        for semantic_name, scale_names in semantic_patterns.items():
            for scale_name in scale_names:
                if scale_name in scale:
                    semantic[semantic_name] = scale_name
                    break

        return semantic

    def convert_effect_tokens(self, effect_data: Dict[str, Any]) -> EffectTokens:
        """Convert effect tokens (shadows, blurs) to standardized format."""
        effects = EffectTokens()

        # Extract shadows
        shadows = effect_data.get('shadows', [])
        effects.shadows = self._normalize_shadows(shadows)

        # Extract blurs
        blurs = effect_data.get('blurs', [])
        effects.blurs = self._normalize_blurs(blurs)

        return effects

    def _normalize_shadows(self, shadows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize shadow definitions to Tailwind format."""
        normalized = []

        for i, shadow in enumerate(shadows):
            if isinstance(shadow, dict):
                # Convert to Tailwind shadow format
                normalized_shadow = {
                    'name': f'shadow-{i + 1}',
                    'offsetX': shadow.get('offsetX', 0),
                    'offsetY': shadow.get('offsetY', 0),
                    'blur': shadow.get('blur', 0),
                    'spread': shadow.get('spread', 0),
                    'color': shadow.get('color', 'rgba(0, 0, 0, 0.1)'),
                    'inset': shadow.get('inset', False)
                }
                normalized.append(normalized_shadow)

        return normalized

    def _normalize_blurs(self, blurs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize blur definitions to Tailwind format."""
        normalized = []

        # Standard blur values
        standard_blurs = [0, 4, 8, 12, 16, 24, 40]

        for i, blur in enumerate(blurs):
            if isinstance(blur, dict):
                blur_value = blur.get('value', 0)
                # Round to nearest standard blur value
                normalized_value = min(standard_blurs, key=lambda x: abs(x - blur_value))

                normalized_blur = {
                    'name': f'blur-{i + 1}',
                    'value': normalized_value
                }
                normalized.append(normalized_blur)

        return normalized