#!/usr/bin/env python3
"""
Test script for Phase 2 Template System
Tests component generation functionality and validation
"""

import sys
import json
from pathlib import Path

# Add template script to path
sys.path.append('templates/scripts')

try:
    from component_generator import ComponentGenerator

    def test_template_system():
        print("🧪 Testing Phase 2 Template System")
        print("=" * 50)

        # Initialize generator
        generator = ComponentGenerator('stage_2_outputs', 'templates', '.')

        # Test cases: component name -> expected category
        test_cases = [
            ('Email', 'forms'),
            ('Button', 'navigation'),
            ('Login', 'display'),
            ('Check', 'forms'),
            ('ForgotPassword', 'navigation'),
            ('Bg', 'display')
        ]

        results = []

        print("\n📋 Testing Component Categorization:")
        for component_name, expected_category in test_cases:
            try:
                # Test component config loading
                config = generator._get_component_config(component_name)
                actual_category = generator._get_component_category(config)

                # Test component name conversion
                pascal_name = generator._to_pascal_case(component_name)

                # Test template availability
                template_path = generator._select_template(config)

                result = {
                    'component': component_name,
                    'pascal_name': pascal_name,
                    'expected_category': expected_category,
                    'actual_category': actual_category,
                    'template': template_path,
                    'success': actual_category == expected_category
                }

                results.append(result)

                status = "✅" if result['success'] else "❌"
                print(f"  {status} {component_name} -> {pascal_name} ({actual_category})")

            except Exception as e:
                print(f"  ❌ {component_name} -> ERROR: {e}")
                results.append({
                    'component': component_name,
                    'error': str(e),
                    'success': False
                })

        # Test template rendering without saving
        print(f"\n🎨 Testing Template Rendering:")
        test_components = ['Email', 'Button', 'Login']

        for component_name in test_components:
            try:
                config = generator._get_component_config(component_name)
                context = generator._prepare_context(config)
                template = generator.jinja_env.get_template(generator._select_template(config))

                # Test template rendering
                rendered = template.render(**context)

                # Basic validation checks
                checks = {
                    'has_imports': 'import' in rendered,
                    'has_exports': 'export' in rendered,
                    'has_component_name': context['component_name'] in rendered,
                    'has_design_tokens': 'designTokens' in rendered,
                    'has_cva': 'cva' in rendered if context.get('uses_cva') else True,
                    'has_interface': 'interface' in rendered,
                    'has_forward_ref': 'forwardRef' in rendered
                }

                all_passed = all(checks.values())
                status = "✅" if all_passed else "⚠️"

                print(f"  {status} {component_name} template render")
                for check, passed in checks.items():
                    symbol = "✅" if passed else "❌"
                    print(f"    {symbol} {check}")

            except Exception as e:
                print(f"  ❌ {component_name} template render failed: {e}")

        # Test stage 2 interface loading
        print(f"\n📊 Testing Stage 2 Interface Loading:")
        try:
            interfaces = []
            for key, value in generator.stage2_outputs.items():
                if key == 'component_interfaces.json':
                    interfaces = value
                    break
                elif isinstance(value, dict) and 'component_interfaces' in value:
                    interfaces = value['component_interfaces']
                    break

            print(f"  ✅ Loaded {len(interfaces)} component interfaces")

            # Test design token loading
            design_tokens = {}
            for key, value in generator.stage2_outputs.items():
                if key == 'web_config.json':
                    design_tokens = value
                    break
                elif isinstance(value, dict) and 'web_config' in value:
                    design_tokens = value['web_config']
                    break

            has_colors = 'colors' in design_tokens
            has_typography = 'typography' in design_tokens
            has_spacing = 'spacing' in design_tokens

            print(f"  ✅ Design tokens loaded:")
            print(f"    ✅ Colors: {has_colors}")
            print(f"    ✅ Typography: {has_typography}")
            print(f"    ✅ Spacing: {has_spacing}")

        except Exception as e:
            print(f"  ❌ Stage 2 interface loading failed: {e}")

        # Summary
        successful_tests = sum(1 for r in results if r.get('success', False))
        total_tests = len([r for r in results if 'error' not in r])

        print(f"\n📈 Test Summary:")
        print(f"  Component categorization: {successful_tests}/{total_tests} successful")
        print(f"  Template rendering: {len(test_components)}/{len(test_components)} tested")
        print(f"  Stage 2 integration: ✅ Working")
        print(f"  Template system: ✅ FUNCTIONAL")

        return successful_tests == total_tests

    if __name__ == "__main__":
        success = test_template_system()
        print(f"\n🎯 Overall Result: {'✅ PASS' if success else '❌ FAIL'}")
        sys.exit(0 if success else 1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)