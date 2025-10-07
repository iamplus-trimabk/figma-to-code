#!/usr/bin/env python3
"""
Design Property Mapper

Converts Figma design properties to dynamic template variables
for intelligent component generation.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import re

class DesignPropertyMapper:
    """Maps Figma design properties to template variables"""

    def __init__(self, figma_analysis_path: str = "figma_design_analysis.json"):
        self.figma_analysis_path = figma_analysis_path
        self.figma_data = self._load_figma_analysis()
        self.tailwind_mappings = self._create_tailwind_mappings()

    def _load_figma_analysis(self) -> Dict[str, Any]:
        """Load Figma design analysis"""
        try:
            with open(self.figma_analysis_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading Figma analysis: {e}")
            return {}

    def _create_tailwind_mappings(self) -> Dict[str, Dict[str, str]]:
        """Create comprehensive Tailwind CSS mappings"""
        return {
            'colors': {
                # Semantic colors
                '#6257db': ['bg-primary', 'text-primary', 'border-primary', 'ring-primary'],
                '#28b446': ['bg-success', 'text-success', 'border-success', 'ring-success'],
                '#fbbb00': ['bg-warning', 'text-warning', 'border-warning', 'ring-warning'],
                '#ef4444': ['bg-error', 'text-error', 'border-error', 'ring-error'],

                # Neutral colors
                '#ffffff': ['bg-white', 'text-white', 'border-white'],
                '#000000': ['bg-black', 'text-black', 'border-black'],
                '#f4f7fa': ['bg-gray-50', 'text-gray-50', 'border-gray-50'],
                '#d9d9d9': ['bg-gray-100', 'text-gray-100', 'border-gray-100'],
                '#bfbfbf': ['bg-gray-200', 'text-gray-200', 'border-gray-200'],
                '#2e2e2e': ['bg-gray-900', 'text-gray-900', 'border-gray-900'],

                # Brand colors (mapped to standard colors)
                '#f36f56': ['bg-orange-500', 'text-orange-500', 'border-orange-500'],
                '#3e4177': ['bg-indigo-800', 'text-indigo-800', 'border-indigo-800'],
                '#518ef8': ['bg-blue-500', 'text-blue-500', 'border-blue-500'],
                '#311944': ['bg-purple-900', 'text-purple-900', 'border-purple-900'],
            },
            'spacing': {
                # Map Figma spacing to Tailwind classes
                4: ['p-1', 'm-1', 'space-y-1', 'gap-1'],
                8: ['p-2', 'm-2', 'space-y-2', 'gap-2'],
                12: ['p-3', 'm-3', 'space-y-3', 'gap-3'],
                16: ['p-4', 'm-4', 'space-y-4', 'gap-4'],
                20: ['p-5', 'm-5', 'space-y-5', 'gap-5'],
                24: ['p-6', 'm-6', 'space-y-6', 'gap-6'],
                32: ['p-8', 'm-8', 'space-y-8', 'gap-8'],
                48: ['p-12', 'm-12', 'space-y-12', 'gap-12'],
                64: ['p-16', 'm-16', 'space-y-16', 'gap-16'],

                # Figma-specific spacing (rounded to nearest Tailwind)
                13.93: ['p-3', 'm-3', 'space-y-3', 'gap-3'],  # ~14px -> p-3
                16.79: ['p-4', 'm-4', 'space-y-4', 'gap-4'],  # ~17px -> p-4
                19.19: ['p-5', 'm-5', 'space-y-5', 'gap-5'],  # ~19px -> p-5
                22.0: ['p-6', 'm-6', 'space-y-6', 'gap-6'],   # 22px -> p-6
                32.0: ['p-8', 'm-8', 'space-y-8', 'gap-8'],   # 32px -> p-8
                47.13: ['p-12', 'm-12', 'space-y-12', 'gap-12'], # ~47px -> p-12
            },
            'border_radius': {
                0: ['rounded-none'],
                2: ['rounded-sm'],
                4: ['rounded'],
                6: ['rounded-md'],
                8: ['rounded-lg'],
                12: ['rounded-xl'],
                16: ['rounded-2xl'],
                24: ['rounded-3xl'],
            },
            'font_sizes': {
                12: ['text-xs'],
                14: ['text-sm'],
                16: ['text-base'],
                18: ['text-lg'],
                20: ['text-xl'],
                24: ['text-2xl'],
                30: ['text-3xl'],
                36: ['text-4xl'],
                40: ['text-5xl'],
                48: ['text-6xl'],
            },
            'font_weights': {
                300: ['font-light'],
                400: ['font-normal'],
                500: ['font-medium'],
                600: ['font-semibold'],
                700: ['font-bold'],
                800: ['font-extrabold'],
                900: ['font-black'],
            },
            'shadows': {
                '0px 0.0px 0.0px 4.0px #000000': ['shadow-sm'],
                '0px 0.0px 4.0px 15.0px #000000': ['shadow-lg'],
                '0px 0.0px 0.0px 9.0px #000000': ['shadow-md'],
                '0px 4px 6px -1px rgba(0, 0, 0, 0.1)': ['shadow'],
                '0px 10px 15px -3px rgba(0, 0, 0, 0.1)': ['shadow-lg'],
                '0px 20px 25px -5px rgba(0, 0, 0, 0.1)': ['shadow-xl'],
            }
        }

    def map_color_to_tailwind(self, color_value: str, color_type: str = 'bg') -> List[str]:
        """Map a color value to Tailwind classes"""
        if not color_value or not color_value.startswith('#'):
            return []

        color_mappings = self.tailwind_mappings['colors'].get(color_value, [])

        # Filter by color type
        if color_type == 'bg':
            return [c for c in color_mappings if c.startswith('bg-')]
        elif color_type == 'text':
            return [c for c in color_mappings if c.startswith('text-')]
        elif color_type == 'border':
            return [c for c in color_mappings if c.startswith('border-')]
        elif color_type == 'ring':
            return [c for c in color_mappings if c.startswith('ring-')]

        return color_mappings

    def map_spacing_to_tailwind(self, spacing_value: float, spacing_type: str = 'p') -> List[str]:
        """Map spacing value to Tailwind classes"""
        # Find closest match in mappings
        spacing_mappings = self.tailwind_mappings['spacing']

        # Exact match
        if spacing_value in spacing_mappings:
            classes = spacing_mappings[spacing_value]
            return [c for c in classes if c.startswith(f'{spacing_type}-') or c.startswith('gap-') or c.startswith('space-')]

        # Closest match
        closest_spacing = min(spacing_mappings.keys(), key=lambda x: abs(x - spacing_value))
        classes = spacing_mappings[closest_spacing]
        return [c for c in classes if c.startswith(f'{spacing_type}-') or c.startswith('gap-') or c.startswith('space-')]

    def map_font_size_to_tailwind(self, font_size: float) -> List[str]:
        """Map font size to Tailwind classes"""
        font_mappings = self.tailwind_mappings['font_sizes']

        # Exact match
        if font_size in font_mappings:
            return font_mappings[font_size]

        # Closest match
        closest_size = min(font_mappings.keys(), key=lambda x: abs(x - font_size))
        return font_mappings[closest_size]

    def map_border_radius_to_tailwind(self, radius: float) -> List[str]:
        """Map border radius to Tailwind classes"""
        radius_mappings = self.tailwind_mappings['border_radius']

        # Exact match
        if radius in radius_mappings:
            return radius_mappings[radius]

        # Closest match
        closest_radius = min(radius_mappings.keys(), key=lambda x: abs(x - radius))
        return radius_mappings[closest_radius]

    def get_design_tokens_for_template(self) -> Dict[str, Any]:
        """Get design tokens formatted for template usage"""
        design_tokens = self.figma_data.get('design_tokens', {})

        # Process colors
        colors = design_tokens.get('colors', {})
        processed_colors = {
            'semantic': {},
            'neutral': {},
            'brand': {}
        }

        for color_key, color_value in colors.items():
            if '-' in color_key:
                category, name = color_key.split('-', 1)
                if category in processed_colors:
                    processed_colors[category][name] = {
                        'value': color_value,
                        'bg_classes': self.map_color_to_tailwind(color_value, 'bg'),
                        'text_classes': self.map_color_to_tailwind(color_value, 'text'),
                        'border_classes': self.map_color_to_tailwind(color_value, 'border'),
                        'ring_classes': self.map_color_to_tailwind(color_value, 'ring')
                    }

        # Process spacing
        spacing = design_tokens.get('spacing', {})
        processed_spacing = {}
        for spacing_key, spacing_value in spacing.items():
            processed_spacing[spacing_key] = {
                'value': spacing_value,
                'padding_classes': self.map_spacing_to_tailwind(spacing_value, 'p'),
                'margin_classes': self.map_spacing_to_tailwind(spacing_value, 'm'),
                'gap_classes': self.map_spacing_to_tailwind(spacing_value, 'gap'),
                'space_classes': self.map_spacing_to_tailwind(spacing_value, 'space')
            }

        # Process typography
        typography = design_tokens.get('typography', {})
        processed_typography = {}

        if 'fontSizes' in typography:
            processed_typography['font_sizes'] = {}
            for font_key, font_value in typography['fontSizes'].items():
                if isinstance(font_value, (int, float)):
                    processed_typography['font_sizes'][font_key] = {
                        'value': font_value,
                        'classes': self.map_font_size_to_tailwind(font_value)
                    }

        if 'fontWeights' in typography:
            processed_typography['font_weights'] = {}
            for weight_key, weight_value in typography['fontWeights'].items():
                if isinstance(weight_value, int):
                    weight_classes = self.tailwind_mappings['font_weights'].get(weight_value, ['font-normal'])
                    processed_typography['font_weights'][weight_key] = {
                        'value': weight_value,
                        'classes': weight_classes
                    }

        # Process effects
        effects = design_tokens.get('effects', [])
        processed_effects = {}
        for effect in effects:
            if isinstance(effect, dict) and 'name' in effect and 'value' in effect:
                shadow_classes = self.tailwind_mappings['shadows'].get(effect['value'], ['shadow'])
                processed_effects[effect['name']] = {
                    'value': effect['value'],
                    'classes': shadow_classes
                }

        return {
            'colors': processed_colors,
            'spacing': processed_spacing,
            'typography': processed_typography,
            'effects': processed_effects
        }

    def generate_template_variables(self) -> Dict[str, Any]:
        """Generate template variables for Jinja2 templates"""
        design_tokens = self.get_design_tokens_for_template()

        # Create template-specific variables
        template_vars = {
            'figma_design_tokens': design_tokens,
            'color_mappings': {
                'primary': design_tokens['colors']['semantic'].get('primary', {}),
                'success': design_tokens['colors']['semantic'].get('success', {}),
                'warning': design_tokens['colors']['semantic'].get('warning', {}),
                'error': design_tokens['colors']['semantic'].get('error', {}),
                'white': design_tokens['colors']['neutral'].get('white', {}),
                'black': design_tokens['colors']['neutral'].get('black', {}),
                'gray_50': design_tokens['colors']['neutral'].get('gray-50', {}),
                'gray_100': design_tokens['colors']['neutral'].get('gray-100', {}),
                'gray_200': design_tokens['colors']['neutral'].get('gray-200', {}),
                'gray_900': design_tokens['colors']['neutral'].get('gray-900', {}),
            },
            'spacing_mappings': design_tokens['spacing'],
            'typography_mappings': design_tokens['typography'],
            'effects_mappings': design_tokens['effects'],
            'component_defaults': {
                'button': {
                    'primary_bg': design_tokens['colors']['semantic'].get('primary', {}).get('bg_classes', ['bg-blue-600']),
                    'primary_text': design_tokens['colors']['semantic'].get('primary', {}).get('text_classes', ['text-white']),
                    'success_bg': design_tokens['colors']['semantic'].get('success', {}).get('bg_classes', ['bg-green-600']),
                    'success_text': design_tokens['colors']['semantic'].get('success', {}).get('text_classes', ['text-white']),
                    'warning_bg': design_tokens['colors']['semantic'].get('warning', {}).get('bg_classes', ['bg-yellow-500']),
                    'warning_text': design_tokens['colors']['semantic'].get('warning', {}).get('text_classes', ['text-white']),
                    'error_bg': design_tokens['colors']['semantic'].get('error', {}).get('bg_classes', ['bg-red-600']),
                    'error_text': design_tokens['colors']['semantic'].get('error', {}).get('text_classes', ['text-white']),
                    'border_radius': ['rounded-md'],
                    'padding': design_tokens['spacing'].get('md', {}).get('padding_classes', ['p-3']),
                    'font_size': design_tokens['typography'].get('font_sizes', {}).get('body', {}).get('classes', ['text-base']),
                },
                'input': {
                    'border_color': design_tokens['colors']['neutral'].get('gray-200', {}).get('border_classes', ['border-gray-300']),
                    'background': design_tokens['colors']['neutral'].get('white', {}).get('bg_classes', ['bg-white']),
                    'text_color': design_tokens['colors']['neutral'].get('gray-900', {}).get('text_classes', ['text-gray-900']),
                    'focus_ring': design_tokens['colors']['semantic'].get('primary', {}).get('ring_classes', ['ring-primary']),
                    'border_radius': ['rounded-md'],
                    'padding': design_tokens['spacing'].get('md', {}).get('padding_classes', ['p-3']),
                },
                'card': {
                    'background': design_tokens['colors']['neutral'].get('white', {}).get('bg_classes', ['bg-white']),
                    'border_color': design_tokens['colors']['neutral'].get('gray-200', {}).get('border_classes', ['border-gray-200']),
                    'shadow': design_tokens['effects'].get('shadow-1', {}).get('classes', ['shadow']),
                    'border_radius': ['rounded-lg'],
                    'padding': design_tokens['spacing'].get('lg', {}).get('padding_classes', ['p-4']),
                }
            }
        }

        return template_vars

    def save_template_variables(self, output_path: str = "template_design_variables.json"):
        """Save template variables to file"""
        template_vars = self.generate_template_variables()

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(template_vars, f, indent=2, ensure_ascii=False)
            print(f"✅ Saved template variables to: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving template variables: {e}")
            return False

def main():
    """Main function to generate template variables"""
    print("🎨 Creating Design Property Mapping System")
    print("=" * 50)

    mapper = DesignPropertyMapper()

    if not mapper.figma_data:
        print("❌ No Figma analysis data found")
        return False

    # Generate and save template variables
    print("🔧 Generating template variables from Figma design data...")
    success = mapper.save_template_variables()

    if success:
        # Print summary
        template_vars = mapper.generate_template_variables()
        print("\n📊 Template Variables Summary:")

        colors = template_vars.get('color_mappings', {})
        print(f"  Color Mappings: {len(colors)}")

        spacing = template_vars.get('spacing_mappings', {})
        print(f"  Spacing Mappings: {len(spacing)}")

        typography = template_vars.get('typography_mappings', {})
        print(f"  Typography Mappings: {len(typography)}")

        effects = template_vars.get('effects_mappings', {})
        print(f"  Effects Mappings: {len(effects)}")

        component_defaults = template_vars.get('component_defaults', {})
        print(f"  Component Defaults: {len(component_defaults)}")

        print(f"\n✅ Design property mapping system created!")
        return True

    return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)