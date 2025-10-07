#!/usr/bin/env python3
"""
Figma Design Data Analyzer

This script extracts real design properties from Figma export data
to enhance template intelligence with actual design values.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Set
from collections import defaultdict

def load_figma_data(file_path: str) -> Dict[str, Any]:
    """Load Figma export data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading Figma data: {e}")
        return {}

def extract_colors(tokens: Dict[str, Any]) -> Dict[str, str]:
    """Extract color values from design tokens"""
    colors = {}

    if 'colors' in tokens:
        color_data = tokens['colors']

        # Extract from nested structure (semantic, neutral, brand)
        for category, color_values in color_data.items():
            if isinstance(color_values, dict):
                for color_name, color_value in color_values.items():
                    if isinstance(color_value, str) and color_value.startswith('#'):
                        colors[f"{category}-{color_name}"] = color_value
                        colors[color_name] = color_value  # Also add without category

    return colors

def extract_spacing(tokens: Dict[str, Any]) -> Dict[str, float]:
    """Extract spacing values from design tokens"""
    spacing = {}

    if 'spacing' in tokens:
        for spacing_name, spacing_value in tokens['spacing'].items():
            if isinstance(spacing_value, (int, float)):
                spacing[spacing_name] = spacing_value

    return spacing

def extract_typography(tokens: Dict[str, Any]) -> Dict[str, Any]:
    """Extract typography tokens from design tokens"""
    typography = {}

    if 'typography' in tokens:
        typo_data = tokens['typography']

        # Font family
        if 'fontFamily' in typo_data:
            typography['fontFamily'] = typo_data['fontFamily']

        # Font sizes
        if 'fontSizes' in typo_data:
            typography['fontSizes'] = typo_data['fontSizes']

        # Font weights
        if 'fontWeights' in typo_data:
            typography['fontWeights'] = typo_data['fontWeights']

        # Line heights
        if 'lineHeights' in typo_data:
            typography['lineHeights'] = typo_data['lineHeights']

    return typography

def extract_effects(tokens: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract effect tokens from design tokens"""
    effects = []

    if 'effects' in tokens:
        if 'shadows' in tokens['effects']:
            effects = tokens['effects']['shadows']

    return effects

def analyze_component_properties(components: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze actual component properties from Figma components"""
    analysis = {
        'border_radius_values': set(),
        'border_widths': set(),
        'font_sizes': set(),
        'font_weights': set(),
        'line_heights': set(),
        'opacity_values': set(),
        'shadows': set(),
        'component_specific_colors': set(),
        'component_dimensions': set(),
        'component_types': set(),
        'component_categories': set()
    }

    for component in components:
        if not isinstance(component, dict):
            continue

        # Track component metadata
        if 'name' in component:
            analysis['component_types'].add(component['name'])
        if 'type' in component:
            analysis['component_types'].add(component['type'])
        if 'category' in component:
            analysis['component_categories'].add(component['category'])

        # Extract properties from component data
        if 'props' in component:
            props = component['props']

            # Dimensions
            if 'width' in props:
                analysis['component_dimensions'].add(f"width:{props['width']}")
            if 'height' in props:
                analysis['component_dimensions'].add(f"height:{props['height']}")

            # Border radius
            if 'borderRadius' in props:
                analysis['border_radius_values'].add(str(props['borderRadius']))

            # Border width
            if 'borderWidth' in props:
                analysis['border_widths'].add(str(props['borderWidth']))

            # Colors
            for color_key in ['backgroundColor', 'textColor', 'borderColor', 'fill']:
                if color_key in props and props[color_key]:
                    analysis['component_specific_colors'].add(str(props[color_key]))

            # Opacity
            if 'opacity' in props:
                analysis['opacity_values'].add(str(props['opacity']))

        # Check for styling properties in nested structures
        if 'styles' in component:
            styles = component['styles']
            if 'fontSize' in styles:
                analysis['font_sizes'].add(str(styles['fontSize']))
            if 'fontWeight' in styles:
                analysis['font_weights'].add(str(styles['fontWeight']))

    # Convert sets to sorted lists
    for key in analysis:
        if isinstance(analysis[key], set):
            analysis[key] = sorted(list(analysis[key]))

    return analysis

def generate_tailwind_mapping(design_analysis: Dict[str, Any]) -> Dict[str, str]:
    """Generate mapping from Figma values to Tailwind classes"""
    mapping = {
        'colors': {},
        'spacing': {},
        'border_radius': {},
        'font_sizes': {},
        'font_weights': {},
        'shadows': {}
    }

    # Map colors to Tailwind classes
    for color_name, color_value in design_analysis.get('colors', {}).items():
        # Generate Tailwind-style class name
        tailwind_class = f"text-{color_name}" if color_name else ""
        mapping['colors'][color_value] = tailwind_class

    # Map spacing to Tailwind classes
    for spacing_name, spacing_value in design_analysis.get('spacing', {}).items():
        tailwind_class = f"p-{spacing_name}" if spacing_name else ""
        mapping['spacing'][spacing_value] = tailwind_class

    # Map border radius to Tailwind classes
    for radius in design_analysis.get('border_radius_values', []):
        try:
            radius_num = float(radius)
            if radius_num <= 1:
                tailwind_class = "rounded-sm"
            elif radius_num <= 2:
                tailwind_class = "rounded"
            elif radius_num <= 4:
                tailwind_class = "rounded-md"
            elif radius_num <= 8:
                tailwind_class = "rounded-lg"
            else:
                tailwind_class = "rounded-xl"
            mapping['border_radius'][radius] = tailwind_class
        except ValueError:
            continue

    return mapping

def generate_template_variables(design_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """Generate template variables from Figma design data"""
    variables = {
        'design_tokens': {
            'colors': design_analysis.get('colors', {}),
            'spacing': design_analysis.get('spacing', {}),
            'typography': design_analysis.get('typography', {}),
            'effects': design_analysis.get('effects', {})
        },
        'component_patterns': {
            'border_radius': design_analysis.get('border_radius_values', []),
            'border_widths': design_analysis.get('border_widths', []),
            'font_sizes': design_analysis.get('font_sizes', []),
            'font_weights': design_analysis.get('font_weights', []),
            'line_heights': design_analysis.get('line_heights', []),
            'shadows': design_analysis.get('shadows', []),
            'opacity_values': design_analysis.get('opacity_values', [])
        },
        'tailwind_mapping': generate_tailwind_mapping(design_analysis)
    }

    return variables

def main():
    """Main analysis function"""
    print("🎨 Analyzing Figma Design Data for Template Intelligence")
    print("=" * 60)

    # Path to Figma export data
    figma_data_path = "extracted_login_assets_api/all_assets.json"

    if not Path(figma_data_path).exists():
        print(f"❌ Figma data file not found: {figma_data_path}")
        return False

    # Load Figma data
    print(f"📁 Loading Figma data from: {figma_data_path}")
    figma_data = load_figma_data(figma_data_path)

    if not figma_data:
        print("❌ Failed to load Figma data")
        return False

    print(f"✅ Loaded Figma data")

    # Extract design tokens
    design_tokens = figma_data.get('design_tokens', {})
    print(f"🎨 Extracting design tokens...")

    colors = extract_colors(design_tokens)
    spacing = extract_spacing(design_tokens)
    typography = extract_typography(design_tokens)
    effects = extract_effects(design_tokens)

    print(f"  Found {len(colors)} colors")
    print(f"  Found {len(spacing)} spacing tokens")
    print(f"  Found {len(typography)} typography tokens")
    print(f"  Found {len(effects)} effects")

    # Analyze components from component_catalog
    component_catalog = figma_data.get('component_catalog', {})
    components = component_catalog.get('components', [])
    print(f"🧩 Analyzing {len(components)} components...")

    component_analysis = analyze_component_properties(components)

    # Compile full analysis
    design_analysis = {
        'colors': colors,
        'spacing': spacing,
        'typography': typography,
        'effects': effects,
        **component_analysis
    }

    # Generate template variables
    print(f"🔧 Generating template variables...")
    template_variables = generate_template_variables(design_analysis)

    # Save analysis results
    output_path = "figma_design_analysis.json"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(template_variables, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved analysis to: {output_path}")
    except Exception as e:
        print(f"❌ Error saving analysis: {e}")
        return False

    # Print summary
    print("\n📊 Analysis Summary:")
    print(f"  Colors: {len(colors)}")
    print(f"  Spacing: {len(spacing)}")
    print(f"  Typography: {len(typography)}")
    print(f"  Effects: {len(effects)}")
    print(f"  Components Analyzed: {len(components)}")
    print(f"  Component Types: {len(component_analysis['component_types'])}")
    print(f"  Component Categories: {len(component_analysis['component_categories'])}")
    print(f"  Border Radius Values: {len(component_analysis['border_radius_values'])}")
    print(f"  Component Dimensions: {len(component_analysis['component_dimensions'])}")

    # Show sample data
    if colors:
        print(f"\n🎨 Sample Colors:")
        for i, (name, value) in enumerate(list(colors.items())[:8]):
            print(f"  {name}: {value}")

    if spacing:
        print(f"\n📏 Sample Spacing:")
        for i, (name, value) in enumerate(list(spacing.items())[:8]):
            print(f"  {name}: {value}px")

    if typography:
        print(f"\n📝 Typography:")
        if 'fontFamily' in typography:
            print(f"  Font Family: {typography['fontFamily']}")
        if 'fontSizes' in typography:
            print(f"  Font Sizes: {typography['fontSizes']}")
        if 'fontWeights' in typography:
            print(f"  Font Weights: {typography['fontWeights']}")

    if component_analysis['component_types']:
        print(f"\n🧩 Component Types Found:")
        for comp_type in component_analysis['component_types'][:8]:
            print(f"  - {comp_type}")

    if component_analysis['component_categories']:
        print(f"\n📂 Component Categories:")
        for category in component_analysis['component_categories']:
            print(f"  - {category}")

    print(f"\n✅ Template intelligence analysis completed!")
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)