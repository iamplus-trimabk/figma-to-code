#!/usr/bin/env python3
"""
Design System Extractor - Parse Figma JSON and generate design tokens + components

Usage:
    python extract_design_system.py figma_BNYofc4IssIvloPwNRyJh4.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import re


class DesignSystemExtractor:
    """Extract design tokens and components from Figma JSON"""

    def __init__(self, figma_json_path: str):
        self.figma_json_path = Path(figma_json_path)
        self.output_dir = Path("design_system_output")
        self.output_dir.mkdir(exist_ok=True)

        # Load Figma data
        with open(figma_json_path) as f:
            self.data = json.load(f)

        self.colors = set()
        self.typography = []
        self.components = []

    def extract_colors(self) -> Dict[str, str]:
        """Extract all colors from the design"""
        print("🎨 Extracting colors...")

        def extract_from_node(node):
            # Extract from fills
            if 'fills' in node:
                for fill in node['fills']:
                    if fill.get('type') == 'SOLID' and 'color' in fill:
                        color = fill['color']
                        hex_color = '#{:02x}{:02x}{:02x}'.format(
                            int(color['r'] * 255),
                            int(color['g'] * 255),
                            int(color['b'] * 255)
                        )
                        self.colors.add(hex_color)

            # Extract from strokes
            if 'strokes' in node:
                for stroke in node['strokes']:
                    if stroke.get('type') == 'SOLID' and 'color' in stroke:
                        color = stroke['color']
                        hex_color = '#{:02x}{:02x}{:02x}'.format(
                            int(color['r'] * 255),
                            int(color['g'] * 255),
                            int(color['b'] * 255)
                        )
                        self.colors.add(hex_color)

            # Recursively check children
            if 'children' in node:
                for child in node['children']:
                    extract_from_node(child)

        extract_from_node(self.data['document'])

        # Categorize colors
        color_palette = self._categorize_colors(sorted(self.colors))
        print(f"   Found {len(self.colors)} colors")
        return color_palette

    def _categorize_colors(self, colors: List[str]) -> Dict[str, str]:
        """Categorize colors into semantic names"""
        palette = {}

        for color in colors:
            if color == '#ffffff':
                palette['white'] = color
            elif color == '#000000':
                palette['black'] = color
            elif color in ['#f4f4f4', '#f4f7fa', '#ebebeb', '#d8dee8']:
                palette[f'gray-{self._get_gray_shade(color)}'] = color
            elif color in ['#518ef8', '#6257db']:
                palette['primary'] = color
            elif color in ['#28b446']:
                palette['success'] = color
            elif color in ['#f14336']:
                palette['danger'] = color
            elif color in ['#fbbb00']:
                palette['warning'] = color
            elif color == '#3b5999':
                palette['facebook'] = color
            else:
                palette[f'color-{len(palette)}'] = color

        return palette

    def _get_gray_shade(self, color: str) -> str:
        """Get gray shade number from hex color"""
        # Convert hex to RGB to determine brightness
        hex_color = color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        brightness = (r + g + b) / 3

        if brightness > 240:
            return '50'
        elif brightness > 200:
            return '100'
        elif brightness > 150:
            return '200'
        elif brightness > 100:
            return '300'
        else:
            return '900'

    def extract_typography(self) -> List[Dict[str, Any]]:
        """Extract typography information"""
        print("📝 Extracting typography...")

        def extract_from_node(node):
            if node.get('type') == 'TEXT' and 'style' in node:
                style = node['style']
                font_size = style.get('fontSize', 16)
                font_weight = style.get('fontWeight', 400)

                # Determine semantic type
                if font_size >= 32:
                    type_name = 'heading'
                elif font_size >= 20:
                    type_name = 'subheading'
                elif font_size >= 16:
                    type_name = 'body'
                else:
                    type_name = 'caption'

                self.typography.append({
                    'name': f"{type_name}-{font_size}",
                    'fontSize': font_size,
                    'fontWeight': font_weight,
                    'fontFamily': style.get('fontFamily', 'Inter'),
                    'lineHeight': style.get('lineHeight', {}).get('value', 1.4)
                })

            if 'children' in node:
                for child in node['children']:
                    extract_from_node(child)

        extract_from_node(self.data['document'])

        # Remove duplicates
        unique_typography = []
        seen = set()
        for typo in self.typography:
            key = (typo['fontSize'], typo['fontWeight'])
            if key not in seen:
                seen.add(key)
                unique_typography.append(typo)

        print(f"   Found {len(unique_typography)} unique text styles")
        return unique_typography

    def extract_components(self) -> List[Dict[str, Any]]:
        """Extract component information"""
        print("🧩 Extracting components...")

        def extract_from_node(node, parent_name=""):
            if node.get('type') in ['RECTANGLE', 'GROUP', 'FRAME']:
                # Determine component type based on name and properties
                name = node.get('name', '').lower()
                comp_type = self._identify_component_type(node, name)

                component = {
                    'name': node.get('name'),
                    'type': comp_type,
                    'width': node.get('absoluteBoundingBox', {}).get('width', 0),
                    'height': node.get('absoluteBoundingBox', {}).get('height', 0),
                    'fills': node.get('fills', []),
                    'strokes': node.get('strokes', []),
                    'cornerRadius': node.get('cornerRadius', 0)
                }

                if comp_type != 'unknown':
                    self.components.append(component)

            if 'children' in node:
                for child in node['children']:
                    extract_from_node(child, node.get('name', ''))

        extract_from_node(self.data['document'])

        print(f"   Found {len(self.components)} components")
        return self.components

    def _identify_component_type(self, node: Dict[str, Any], name: str) -> str:
        """Identify component type based on properties"""
        if 'button' in name:
            return 'button'
        elif 'input' in name or 'field' in name:
            return 'input'
        elif 'bg' in name or 'background' in name:
            return 'background'
        elif node.get('type') == 'RECTANGLE' and node.get('cornerRadius', 0) > 0:
            return 'card'
        elif node.get('type') == 'TEXT':
            return 'text'
        else:
            return 'unknown'

    def generate_css_variables(self, colors: Dict[str, str]) -> str:
        """Generate CSS variables for colors"""
        css = ":root {\n"
        css += "  /* Colors */\n"
        for name, color in colors.items():
            css += f"  --color-{name}: {color};\n"
        css += "}\n"
        return css

    def generate_tailwind_config(self, colors: Dict[str, str], typography: List[Dict[str, Any]]) -> str:
        """Generate Tailwind configuration"""
        config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './src/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {"""

        # Add colors
        for name, color in colors.items():
            if name != 'white' and name != 'black':
                config += f"\n        {name}: '{{color}}',"

        config += """
      },
      fontFamily: {"""

        # Add font families
        fonts = set()
        for typo in typography:
            fonts.add(typo['fontFamily'])

        for font in sorted(fonts):
            config += f"\n        '{font.lower().replace(' ', '-')}': ['{font}'],"

        config += """
      },
      fontSize: {"""

        # Add font sizes
        for typo in typography:
            size_name = typo['name'].split('-')[0]
            config += f"\n        '{size_name}': ['{typo["fontSize"]}px'],"

        config += """
      }
    }
  },
  plugins: [],
}"""

        return config

    def generate_react_components(self) -> str:
        """Generate basic React components"""
        components_dir = self.output_dir / "components"
        components_dir.mkdir(exist_ok=True)

        # Generate Button component
        button_code = '''import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
}

export const Button: React.FC<ButtonProps> = ({
  className,
  variant = 'primary',
  size = 'md',
  children,
  ...props
}) => {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
        'disabled:pointer-events-none disabled:opacity-50',
        {
          'bg-primary text-primary-foreground hover:bg-primary/90': variant === 'primary',
          'bg-secondary text-secondary-foreground hover:bg-secondary/80': variant === 'secondary',
        },
        {
          'h-9 px-3 text-sm': size === 'sm',
          'h-10 px-4 py-2': size === 'md',
          'h-11 px-8': size === 'lg',
        },
        className
      )}
      {...props}
    >
      {children}
    </button>
  );
};
'''

        button_file = components_dir / "Button.tsx"
        button_file.write_text(button_code)

        # Generate Input component
        input_code = '''import React from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export const Input: React.FC<InputProps> = ({ className, ...props }) => {
  return (
    <input
      className={cn(
        'flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm',
        'ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium',
        'placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2',
        'focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    />
  );
};
'''

        input_file = components_dir / "Input.tsx"
        input_file.write_text(input_code)

        return str(components_dir)

    def run_extraction(self):
        """Run the complete extraction process"""
        print("🚀 Starting design system extraction...")

        # Extract design tokens
        colors = self.extract_colors()
        typography = self.extract_typography()
        components = self.extract_components()

        # Generate output files
        print("\n📁 Generating output files...")

        # CSS variables
        css_file = self.output_dir / "design-tokens.css"
        css_file.write_text(self.generate_css_variables(colors))
        print(f"   ✅ CSS variables: {css_file}")

        # Tailwind config
        tailwind_file = self.output_dir / "tailwind.config.js"
        tailwind_file.write_text(self.generate_tailwind_config(colors, typography))
        print(f"   ✅ Tailwind config: {tailwind_file}")

        # React components
        components_dir = self.generate_react_components()
        print(f"   ✅ React components: {components_dir}")

        # Design tokens JSON
        tokens_file = self.output_dir / "design-tokens.json"
        tokens_data = {
            'colors': colors,
            'typography': typography,
            'components': components
        }
        tokens_file.write_text(json.dumps(tokens_data, indent=2))
        print(f"   ✅ Design tokens JSON: {tokens_file}")

        # Summary
        print(f"\n📊 Extraction Summary:")
        print(f"   Colors: {len(colors)}")
        print(f"   Typography styles: {len(typography)}")
        print(f"   Components identified: {len(components)}")
        print(f"   Output directory: {self.output_dir}")

        print(f"\n✅ Design system extraction complete!")
        return self.output_dir


def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_design_system.py <figma_json_file>")
        sys.exit(1)

    figma_json_path = sys.argv[1]
    if not Path(figma_json_path).exists():
        print(f"❌ File not found: {figma_json_path}")
        sys.exit(1)

    extractor = DesignSystemExtractor(figma_json_path)
    extractor.run_extraction()


if __name__ == "__main__":
    main()