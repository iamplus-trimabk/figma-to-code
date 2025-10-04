#!/usr/bin/env python3
"""
Stage 3 Component Generator - Phase 2 Template System

Template-based component generation using established patterns from Phase 1.
Generates React components from Stage 2 interfaces using Jinja2 templates.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import argparse

try:
    import jinja2
except ImportError:
    print("Error: jinja2 is required. Install with: pip install jinja2")
    sys.exit(1)


class ComponentGenerator:
    """Template-based component generator using Phase 1 patterns"""

    def __init__(self, stage2_outputs_path: str, templates_dir: str, output_dir: str):
        self.stage2_outputs_path = Path(stage2_outputs_path)
        self.templates_dir = Path(templates_dir)
        self.output_dir = Path(output_dir)
        self.stage2_outputs = self._load_stage2_outputs()
        self.jinja_env = self._setup_jinja_environment()

    def _load_stage2_outputs(self) -> Dict[str, Any]:
        """Load Stage 2 outputs from JSON files"""
        if not self.stage2_outputs_path.exists():
            raise FileNotFoundError(f"Stage 2 outputs not found: {self.stage2_outputs_path}")

        # If it's a directory, load all JSON files
        if self.stage2_outputs_path.is_dir():
            outputs = {}
            for json_file in self.stage2_outputs_path.glob("*.json"):
                with open(json_file, 'r') as f:
                    outputs[json_file.name] = json.load(f)
            return outputs
        else:
            # If it's a file, load it directly
            with open(self.stage2_outputs_path, 'r') as f:
                return json.load(f)

    def _setup_jinja_environment(self) -> jinja2.Environment:
        """Configure Jinja2 environment with custom filters"""
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        # Custom filters for component generation
        env.filters['pascal_case'] = self._to_pascal_case
        env.filters['camel_case'] = self._to_camel_case
        env.filters['lower'] = str.lower
        env.filters['component_category'] = self._get_component_category
        env.filters['base_classes'] = self._get_base_classes

        return env

    def _to_pascal_case(self, text: str) -> str:
        """Convert text to PascalCase"""
        # Handle special cases
        special_cases = {
            'Bg': 'Card',
            'Angle': 'Card',
            'Email': 'Input',
            'Password': 'Input',
            'Search': 'Input',
            'ForgotPassword': 'Button',
            'Button': 'Button',
            'Check': 'Input',
            'Image': 'Image',
            'Login': 'Card',
            'RememberMe': 'Input',
            'Angle4': 'Card',
            'Angle5': 'Card',
            'Angle6': 'Card',
            'Angle7': 'Card'
        }

        if text in special_cases:
            return special_cases[text]

        # Default PascalCase conversion
        return ''.join(word.capitalize() for word in text.replace('-', '_').split('_'))

    def _to_camel_case(self, text: str) -> str:
        """Convert text to camelCase"""
        pascal = self._to_pascal_case(text)
        return pascal[0].lower() + pascal[1:] if len(pascal) > 0 else pascal

    def _get_component_category(self, component_config: Dict) -> str:
        """Determine component category based on Stage 2 interface"""
        name = component_config.get('name', '')
        description = component_config.get('description', '').lower()

        # Navigation components
        if name in ['Button', 'ForgotPassword'] or 'button' in description:
            return 'navigation'

        # Form components
        elif name in ['Email', 'Password', 'Search', 'Check'] or any(x in description for x in ['input', 'form', 'field']):
            return 'forms'

        # Feedback components
        elif 'alert' in description or 'notification' in description or 'feedback' in description:
            return 'feedback'

        # Display components (default)
        else:
            return 'display'

    def _get_base_classes(self, component_config: Dict) -> str:
        """Get base classes for component"""
        category = self._get_component_category(component_config)
        name = component_config.get('name', '')

        if name == 'Button':
            return 'React.ButtonHTMLAttributes<HTMLButtonElement>'
        elif name in ['Email', 'Password', 'Search']:
            return 'Omit<React.InputHTMLAttributes<HTMLInputElement>, \'size\' | \'onChange\'>'
        else:
            return 'React.HTMLAttributes<HTMLDivElement>'

    def _get_component_config(self, component_name: str) -> Dict[str, Any]:
        """Get component configuration from Stage 2 interfaces"""
        # Get component interfaces from loaded outputs
        interfaces = []
        for key, value in self.stage2_outputs.items():
            if key == 'component_interfaces.json':
                interfaces = value
                break
            elif isinstance(value, dict) and 'component_interfaces' in value:
                interfaces = value['component_interfaces']
                break

        # Find component by name (case-insensitive)
        for interface in interfaces:
            if interface.get('name', '').lower() == component_name.lower():
                return interface

        raise ValueError(f"Component '{component_name}' not found in Stage 2 interfaces")

    def _select_template(self, component_config: Dict) -> str:
        """Select appropriate template based on component type"""
        category = self._get_component_category(component_config)
        return "components/component.j2"

    def _prepare_context(self, component_config: Dict, platform: str = 'web') -> Dict[str, Any]:
        """Prepare template context with component data"""
        component_name = self._to_pascal_case(component_config['name'])

        # Determine if component uses variants
        uses_cva = self._get_component_category(component_config) in ['navigation', 'forms', 'display', 'feedback']

        # Get base classes
        base_classes = self._get_base_classes(component_config)

        # Determine extends_from
        extends_from = component_config.get('name', 'Bg')
        if component_config.get('name') in ['Email', 'Password', 'Search']:
            extends_from = component_config.get('name')
        elif component_config.get('name') == 'Button':
            extends_from = 'Button'

        # Get design tokens
        design_tokens = {}
        for key, value in self.stage2_outputs.items():
            if key == 'web_config.json':
                design_tokens = value
                break
            elif isinstance(value, dict) and 'web_config' in value:
                design_tokens = value['web_config']
                break

        return {
            'component_name': component_name,
            'component_config': {
                **component_config,
                'category': self._get_component_category(component_config),
                'extends_from': extends_from,
                'base_classes': base_classes,
                'base_classes_value': self._get_base_classes(component_config)
            },
            'uses_cva': uses_cva,
            'platform': platform,
            'design_tokens': design_tokens,
            'accessibility': True
        }

    def _format_code(self, code: str) -> str:
        """Basic code formatting"""
        # Remove excessive blank lines
        lines = code.split('\n')
        formatted_lines = []
        prev_empty = False

        for line in lines:
            is_empty = not line.strip()
            if not (is_empty and prev_empty):
                formatted_lines.append(line)
            prev_empty = is_empty

        return '\n'.join(formatted_lines)

    def _validate_component(self, code: str) -> bool:
        """Basic validation of generated component"""
        # Check for essential patterns
        essential_patterns = [
            'export interface',
            'React.forwardRef',
            '.displayName',
            'export {'
        ]

        for pattern in essential_patterns:
            if pattern not in code:
                print(f"Warning: Missing essential pattern '{pattern}' in generated code")
                return False

        return True

    def generate_component(self, component_name: str, platform: str = 'web') -> str:
        """Generate a component using templates"""
        print(f"Generating component: {component_name}")

        try:
            # 1. Load component configuration from Stage 2
            component_config = self._get_component_config(component_name)
            print(f"  Found config: {component_config['name']}")

            # 2. Select appropriate template
            template_path = self._select_template(component_config)
            print(f"  Using template: {template_path}")
            template = self.jinja_env.get_template(template_path)

            # 3. Prepare template context
            context = self._prepare_context(component_config, platform)
            print(f"  Component category: {context['component_config']['category']}")

            # 4. Generate component code
            generated_code = template.render(**context)

            # 5. Format and validate
            formatted_code = self._format_code(generated_code)

            if not self._validate_component(formatted_code):
                print("  Warning: Generated code may have issues")

            print(f"  Successfully generated {component_name} component")
            return formatted_code

        except Exception as e:
            print(f"Error generating component {component_name}: {e}")
            raise

    def save_component(self, component_name: str, code: str, category: str):
        """Save generated component to appropriate directory"""
        # Create output directory
        output_category_dir = self.output_dir / "src" / "components" / category
        output_category_dir.mkdir(parents=True, exist_ok=True)

        # Determine filename
        if category == 'navigation' and component_name == 'Button':
            filename = 'button.tsx'
        elif category == 'forms' and component_name in ['Input', 'Email', 'Password', 'Search']:
            if component_name == 'Input':
                filename = 'input.tsx'
            else:
                filename = f"{component_name.lower()}.tsx"
        elif category == 'display' and component_name in ['Card', 'Bg']:
            filename = 'card.tsx'
        elif category == 'feedback':
            filename = 'alert.tsx'
        else:
            filename = f"{component_name.lower()}.tsx"

        output_path = output_category_dir / filename

        # Save component
        with open(output_path, 'w') as f:
            f.write(code)

        print(f"  Saved to: {output_path}")

    def generate_all_components(self, platform: str = 'web'):
        """Generate all available components"""
        print("Generating all components from Stage 2 interfaces...")

        # Get component interfaces from loaded outputs
        interfaces = []
        for key, value in self.stage2_outputs.items():
            if key == 'component_interfaces.json':
                interfaces = value
                break
            elif isinstance(value, dict) and 'component_interfaces' in value:
                interfaces = value['component_interfaces']
                break

        generated_components = []

        for interface in interfaces:
            component_name = interface.get('name')
            if not component_name:
                continue

            try:
                # Skip components we already have from Phase 1
                phase_1_components = ['Button', 'Input', 'Card', 'Alert']
                pascal_name = self._to_pascal_case(component_name)

                if pascal_name in phase_1_components:
                    print(f"Skipping {component_name} (already implemented in Phase 1)")
                    continue

                # Generate component
                code = self.generate_component(component_name, platform)

                # Determine category and save
                component_config = self._get_component_config(component_name)
                category = self._get_component_category(component_config)

                self.save_component(pascal_name, code, category)

                generated_components.append({
                    'name': pascal_name,
                    'category': category,
                    'source': component_name
                })

            except Exception as e:
                print(f"Failed to generate {component_name}: {e}")
                continue

        print(f"\nGenerated {len(generated_components)} components:")
        for comp in generated_components:
            print(f"  - {comp['name']} ({comp['category']})")

        return generated_components


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Generate components from Stage 2 interfaces')
    parser.add_argument('--stage2', required=True, help='Path to Stage 2 outputs directory')
    parser.add_argument('--templates', default='templates', help='Path to templates directory')
    parser.add_argument('--output', default='.', help='Output directory')
    parser.add_argument('--component', help='Generate specific component (name from Stage 2)')
    parser.add_argument('--all', action='store_true', help='Generate all available components')
    parser.add_argument('--platform', default='web', choices=['web', 'mobile'], help='Target platform')

    args = parser.parse_args()

    # Initialize generator
    try:
        generator = ComponentGenerator(args.stage2, args.templates, args.output)
    except Exception as e:
        print(f"Error initializing generator: {e}")
        sys.exit(1)

    # Generate components
    if args.all:
        generator.generate_all_components(args.platform)
    elif args.component:
        try:
            code = generator.generate_component(args.component, args.platform)
            component_config = generator._get_component_config(args.component)
            category = generator._get_component_category(component_config)
            component_name = generator._to_pascal_case(args.component)

            generator.save_component(component_name, code, category)
            print(f"Generated {component_name} successfully!")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print("Please specify either --component or --all")
        parser.print_help()


if __name__ == '__main__':
    main()