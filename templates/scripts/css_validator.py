#!/usr/bin/env python3
"""
CSS Validation and Generation System for Component Templates

Ensures all design tokens used in templates have corresponding CSS classes.
Automatically generates fallback CSS classes when needed.
"""

import re
import json
from pathlib import Path
from typing import Dict, Set, List, Tuple
from collections import defaultdict


class CSSValidator:
    """Validates and generates CSS classes for design tokens"""

    def __init__(self):
        # Standard Tailwind classes that always exist
        self.standard_classes = {
            'grayscale', 'border', 'shadow', 'text', 'bg', 'flex', 'grid',
            'items', 'justify', 'self', 'place', 'content', 'gap', 'space',
            'divide', 'place', 'inset', 'z', 'order', 'col', 'row', 'auto',
            'grid', 'flow', 'start', 'end', 'center', 'between', 'around',
            'evenly', 'stretch', 'normal', 'basis', 'grow', 'shrink',
            'p', 'px', 'py', 'pt', 'pr', 'pb', 'pl', 'm', 'mx', 'my',
            'mt', 'mr', 'mb', 'ml', 'space', 'w', 'min', 'max', 'h',
            'display', 'hidden', 'visible', 'overflow', 'inline', 'block',
            'table', 'relative', 'absolute', 'fixed', 'sticky', 'top',
            'right', 'bottom', 'left', 'inset', 'rounded', 'border',
            'divide', 'ring', 'shadow', 'opacity', 'text', 'font',
            'leading', 'tracking', 'decoration', 'transform', 'scale',
            'rotate', 'translate', 'skew', 'object', 'table', 'caption',
            'align', 'list', 'float', 'clear', 'isolate', 'z', 'isolation',
            'content', 'items', 'justify', 'self', 'place', 'whitespace',
            'break', 'truncate', 'overflow', 'underline', 'line', 'text',
            'align', 'normal', 'list', 'grid', 'col', 'row', 'auto',
            'flow', 'start', 'end', 'center', 'between', 'around',
            'evenly', 'stretch', 'basis', 'grow', 'shrink', 'gap',
            'space', 'w', 'min', 'max', 'h', 'display', 'hidden',
            'visible', 'overflow', 'inline', 'block', 'table',
            'relative', 'absolute', 'fixed', 'sticky', 'top',
            'right', 'bottom', 'left', 'inset', 'rounded', 'border',
            'divide', 'ring', 'shadow', 'opacity', 'text', 'font',
            'leading', 'tracking', 'decoration', 'transform', 'scale',
            'rotate', 'translate', 'skew', 'object', 'table', 'caption',
            'align', 'list', 'float', 'clear', 'isolate', 'z', 'isolation',
            'hover', 'focus', 'active', 'visited', 'disabled', 'checked',
            'read-only', 'first', 'last', 'odd', 'even', 'group', 'peer',
            'motion', 'dark', 'sm', 'md', 'lg', 'xl', '2xl', '3xl',
            '4xl', '5xl', '6xl', '7xl', '8xl', '9xl', 'screen',
            'portrait', 'landscape', 'print', 'forced', 'reduced',
            'motion', 'contrast', 'orientation', 'prefers', 'media',
            'supports', 'aria', 'data', 'lang', 'dir', 'ltr', 'rtl',
            'before', 'after', 'first-letter', 'first-line', 'selection',
            'marker', 'file', 'placeholder', 'backdrop', 'from', 'via',
            'to', 'gradient', 'linear', 'radial', 'conic', 'repeating',
            'ring', 'shadow', 'blur', 'brightness', 'contrast',
            'grayscale', 'hue', 'invert', 'saturate', 'sepia',
            'filter', 'filter', 'backdrop', 'blur', 'brightness',
            'contrast', 'grayscale', 'hue', 'invert', 'saturate',
            'sepia', 'filter', 'drop', 'shadow'
        }

        # Design token categories with their color values
        self.design_tokens = {
            'primary': {
                50: '#f7f6fd', 100: '#efeefb', 200: '#dfddf7', 300: '#cfccf4',
                400: '#c0bbf0', 500: '#6257db', 600: '#584ec5', 700: '#4e45af',
                800: '#443c99', 900: '#3a3483', 950: '#312b6d'
            },
            'success': {
                50: '#f4fbf5', 100: '#e9f7ec', 200: '#d4f0da', 300: '#bee8c7',
                400: '#a9e1b5', 500: '#28b446', 600: '#24a23f', 700: '#209038',
                800: '#1c7d31', 900: '#186c2a', 950: '#145a23'
            },
            'warning': {
                50: '#fefbf2', 100: '#fef8e5', 200: '#fef1cc', 300: '#fdeab2',
                400: '#fde399', 500: '#fbbb00', 600: '#e1a800', 700: '#c89500',
                800: '#af8200', 900: '#967000', 950: '#7d5d00'
            },
            'error': {
                50: '#fef2f2', 100: '#fee2e2', 200: '#fecaca', 300: '#fca5a5',
                400: '#f87171', 500: '#ef4444', 600: '#dc2626', 700: '#b91c1c',
                800: '#991b1b', 900: '#7f1d1d', 950: '#450a0a'
            }
        }

    def extract_classes_from_component(self, component_content: str) -> Set[str]:
        """Extract all CSS classes from a component file"""
        # Pattern to match className content
        class_pattern = r'className\s*=\s*["\']([^"\']*)["\']'
        class_matches = re.findall(class_pattern, component_content)

        # Pattern to match cva() calls
        cva_pattern = r'cva\([^,]*,\s*\{[^}]*variant:\s*\{([^}]*)\}'
        cva_matches = re.findall(cva_pattern, component_content, re.MULTILINE | re.DOTALL)

        all_classes = set()

        for match in class_matches:
            classes = match.split()
            all_classes.update(classes)

        for match in cva_matches:
            # Parse CVA variant definitions
            variant_pairs = re.findall(r'"([^"]+)"', match)
            all_classes.update(variant_pairs)

        return all_classes

    def validate_design_token_classes(self, classes: Set[str]) -> Tuple[Set[str], Set[str]]:
        """
        Validate design token classes and return:
        - Set of missing classes that need CSS generation
        - Set of invalid classes
        """
        missing_classes = set()
        invalid_classes = set()

        for class_name in classes:
            # Skip if it's a standard Tailwind class
            if self._is_standard_tailwind_class(class_name):
                continue

            # Check if it's a design token class
            if self._is_design_token_class(class_name):
                # Check if we have the definition for this token
                if not self._design_token_exists(class_name):
                    missing_classes.add(class_name)
            else:
                # It's not a standard class and not a recognized design token
                invalid_classes.add(class_name)

        return missing_classes, invalid_classes

    def _is_standard_tailwind_class(self, class_name: str) -> bool:
        """Check if a class is a standard Tailwind class"""
        # Remove modifiers and prefixes
        clean_name = re.sub(r'^(hover|focus|active|disabled|group|peer|first|last|odd|even|before|after|dark|sm|md|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl|screen|portrait|landscape|print|media|supports|aria|data|lang|dir|ltr|rtl|file|placeholder|backdrop|from|via|to|gradient|repeating|ring|shadow|blur|brightness|contrast|grayscale|hue|invert|saturate|sepia|filter|drop)([:-])?', '', class_name)

        # Split into parts and check each
        parts = clean_name.split('-')
        return any(part in self.standard_classes for part in parts)

    def _is_design_token_class(self, class_name: str) -> bool:
        """Check if a class is a design token class"""
        # Pattern: bg-primary-600, text-success-500, border-error-200, ring-warning-600
        pattern = r'^(bg|text|border|ring)-(primary|success|warning|error)-\d+$'
        return re.match(pattern, class_name) is not None

    def _design_token_exists(self, class_name: str) -> bool:
        """Check if a design token class exists in our token definitions"""
        match = re.match(r'^(bg|text|border|ring)-(primary|success|warning|error)-(\d+)$', class_name)
        if not match:
            return False

        prefix, color_name, shade = match.groups()
        return color_name in self.design_tokens and int(shade) in self.design_tokens[color_name]

    def generate_css_for_classes(self, classes: Set[str]) -> str:
        """Generate CSS rules for the given classes"""
        css_rules = []

        for class_name in sorted(classes):
            css_rule = self._generate_css_rule(class_name)
            if css_rule:
                css_rules.append(css_rule)

        return '\n'.join(css_rules)

    def _generate_css_rule(self, class_name: str) -> str:
        """Generate a CSS rule for a specific class"""
        match = re.match(r'^(bg|text|border|ring)-(primary|success|warning|error)-(\d+)$', class_name)
        if not match:
            return ""

        prefix, color_name, shade = match.groups()

        if color_name not in self.design_tokens or int(shade) not in self.design_tokens[color_name]:
            return ""

        color_value = self.design_tokens[color_name][int(shade)]

        if prefix == 'bg':
            return f'.bg-{color_name}-{shade} {{ background-color: {color_value}; }}'
        elif prefix == 'text':
            return f'.text-{color_name}-{shade} {{ color: {color_value}; }}'
        elif prefix == 'border':
            return f'.border-{color_name}-{shade} {{ border-color: {color_value}; }}'
        elif prefix == 'ring':
            return f'.ring-{color_name}-{shade} {{ --tw-ring-color: {color_value}; }}'

        return ""

    def validate_components(self, component_dir: Path) -> Dict[str, any]:
        """Validate all components in a directory"""
        results = {
            'components_checked': 0,
            'classes_found': set(),
            'missing_classes': set(),
            'invalid_classes': set(),
            'component_details': []
        }

        if not component_dir.exists():
            return results

        for component_file in component_dir.glob('**/*.tsx'):
            try:
                with open(component_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                classes = self.extract_classes_from_component(content)
                missing, invalid = self.validate_design_token_classes(classes)

                results['components_checked'] += 1
                results['classes_found'].update(classes)
                results['missing_classes'].update(missing)
                results['invalid_classes'].update(invalid)

                if missing or invalid:
                    results['component_details'].append({
                        'file': str(component_file),
                        'missing': list(missing),
                        'invalid': list(invalid)
                    })

            except Exception as e:
                print(f"Error processing {component_file}: {e}")

        return results

    def generate_css_file(self, missing_classes: Set[str]) -> str:
        """Generate a complete CSS file for missing classes"""
        css_content = [
            "/* Auto-generated CSS classes for design tokens */",
            "/* Generated by CSS Validator - Do not edit manually */",
            "",
            self.generate_css_for_classes(missing_classes)
        ]

        return '\n'.join(css_content)


def main():
    """Main function for CSS validation"""
    import argparse

    parser = argparse.ArgumentParser(description='Validate and generate CSS for component templates')
    parser.add_argument('--component-dir', required=True, help='Directory containing component files')
    parser.add_argument('--output-css', help='Output CSS file for missing classes')
    parser.add_argument('--validate-only', action='store_true', help='Only validate, do not generate CSS')

    args = parser.parse_args()

    validator = CSSValidator()

    print("🔍 CSS Validation for Component Templates")
    print("=" * 50)

    # Validate components
    component_dir = Path(args.component_dir)
    results = validator.validate_components(component_dir)

    print(f"📊 Results:")
    print(f"  Components checked: {results['components_checked']}")
    print(f"  Total classes found: {len(results['classes_found'])}")
    print(f"  Missing design token classes: {len(results['missing_classes'])}")
    print(f"  Invalid classes: {len(results['invalid_classes'])}")

    if results['missing_classes']:
        print(f"\n❌ Missing Design Token Classes:")
        for cls in sorted(results['missing_classes']):
            print(f"  - {cls}")

    if results['invalid_classes']:
        print(f"\n⚠️  Invalid Classes:")
        for cls in sorted(results['invalid_classes']):
            print(f"  - {cls}")

    if results['component_details']:
        print(f"\n📋 Component Details:")
        for detail in results['component_details']:
            print(f"  {detail['file']}:")
            if detail['missing']:
                print(f"    Missing: {', '.join(detail['missing'])}")
            if detail['invalid']:
                print(f"    Invalid: {', '.join(detail['invalid'])}")

    # Generate CSS file if requested
    if not args.validate_only and results['missing_classes'] and args.output_css:
        css_content = validator.generate_css_file(results['missing_classes'])

        output_path = Path(args.output_css)
        with open(output_path, 'w') as f:
            f.write(css_content)

        print(f"\n✅ Generated CSS file: {output_path}")
        print(f"   Contains {len(results['missing_classes'])} CSS rules")

    return len(results['missing_classes']) == 0


if __name__ == '__main__':
    exit(0 if main() else 1)