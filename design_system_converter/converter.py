"""
Design System Converter - Main orchestrator for Stage 2 conversion.

Coordinates token conversion, style generation, interface building, and validation
to convert Stage 1 outputs into production-ready design system configurations.
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from .schemas import (
    ConversionInput, ConversionOutput, DesignTokens, ComponentCatalog,
    ComponentDefinition, ComponentCategory
)
from .token_converter import TokenConverter
from .style_generator import StyleGenerator
from .interface_builder import InterfaceBuilder
from .platform_configs import PlatformConfigs
from .validators import ConversionValidator


class DesignSystemConverter:
    """Main orchestrator for the design system conversion process."""

    def __init__(self):
        self.token_converter = TokenConverter()
        self.style_generator = StyleGenerator()
        self.interface_builder = InterfaceBuilder()
        self.platform_configs = PlatformConfigs()
        self.validator = ConversionValidator()

    def convert_design_system(self, stage1_output: Dict[str, Any]) -> ConversionOutput:
        """
        Convert Stage 1 outputs to Stage 2 design system configurations.

        Args:
            stage1_output: Complete output from Stage 1 (design tokens, components, layouts)

        Returns:
            ConversionOutput: Complete design system configuration for Stage 3
        """
        conversion_start_time = time.time()

        # Parse Stage 1 input
        conversion_input = self._parse_stage1_input(stage1_output)

        # Convert design tokens
        design_tokens = self.token_converter.convert_tokens(conversion_input.design_tokens)

        # Generate style configurations
        tailwind_config = self.style_generator.generate_tailwind_config(design_tokens)
        native_wind_config = self.style_generator.generate_native_wind_config(design_tokens)

        # Generate component interfaces
        component_interfaces = self.interface_builder.build_component_interfaces(
            conversion_input.component_catalog.components
        )

        # Generate design system CSS
        css_variables = self.style_generator.generate_css_variables(design_tokens)
        design_system_css = self.style_generator.generate_design_system_css(design_tokens, css_variables)

        # Generate platform configurations
        platform_configs = self.platform_configs.generate_platform_specific_configs(
            design_tokens, tailwind_config, native_wind_config
        )

        # Calculate conversion statistics
        conversion_stats = self._calculate_conversion_stats(
            conversion_input, design_tokens, component_interfaces, conversion_start_time
        )

        # Create conversion output
        output = ConversionOutput(
            metadata={
                'conversion_time': datetime.now().isoformat(),
                'source_file': conversion_input.metadata.get('figma_file', {}).get('name', 'Unknown'),
                'version': '1.0.0',
                'stage': '2',
                'converter_version': '1.0.0'
            },
            tailwind_config=tailwind_config,
            native_wind_config=native_wind_config,
            component_interfaces=component_interfaces,
            design_system_css=design_system_css,
            platform_configs=platform_configs,
            conversion_stats=conversion_stats
        )

        # Validate output
        validation_result = self.validator.validate_conversion_output(output)
        if not validation_result['valid']:
            print("⚠️  Validation issues found:")
            for error in validation_result['errors']:
                print(f"  ❌ {error}")
            for warning in validation_result['warnings']:
                print(f"  ⚠️  {warning}")

        return output

    def _parse_stage1_input(self, stage1_output: Dict[str, Any]) -> ConversionInput:
        """Parse Stage 1 output into ConversionInput format."""
        # Extract design tokens
        design_tokens_data = stage1_output.get('design_tokens', {})

        # Extract component catalog
        component_catalog_data = stage1_output.get('component_catalog', {})
        component_catalog = self._parse_component_catalog(component_catalog_data)

        # Extract screen layouts
        screen_layouts = stage1_output.get('screen_layouts', {})

        # Extract metadata
        metadata = stage1_output.get('metadata', {})

        return ConversionInput(
            design_tokens=design_tokens_data,
            component_catalog=component_catalog,
            screen_layouts=screen_layouts,
            metadata=metadata
        )

    def _parse_component_catalog(self, catalog_data: Dict[str, Any]) -> ComponentCatalog:
        """Parse component catalog data."""
        components = []

        if 'components' in catalog_data:
            for component_data in catalog_data['components']:
                component = self._parse_component_definition(component_data)
                if component:
                    components.append(component)

        return ComponentCatalog(components=components)

    def _parse_component_definition(self, component_data: Dict[str, Any]) -> Optional[ComponentDefinition]:
        """Parse a single component definition."""
        if not component_data.get('name'):
            return None

        # Parse category
        category_str = component_data.get('category', 'display')
        try:
            category = ComponentCategory(category_str)
        except ValueError:
            category = ComponentCategory.DISPLAY

        # Parse variants
        variants = []
        if 'variants' in component_data:
            for variant_data in component_data['variants']:
                from .schemas import ComponentVariant
                variant = ComponentVariant(
                    name=variant_data.get('name', 'default'),
                    props=variant_data.get('props', {}),
                    example_usage=variant_data.get('example_usage', '')
                )
                variants.append(variant)

        return ComponentDefinition(
            name=component_data['name'],
            type=component_data.get('type', 'group'),
            category=category,
            props=component_data.get('props', {}),
            variants=variants,
            children=component_data.get('children', []),
            description=component_data.get('description', '')
        )

    def _calculate_conversion_stats(self, conversion_input: ConversionInput,
                                 design_tokens: DesignTokens,
                                 component_interfaces: List[Any],
                                 start_time: float) -> Dict[str, Any]:
        """Calculate conversion statistics."""
        conversion_duration = time.time() - start_time

        stats = {
            'conversion_duration_seconds': round(conversion_duration, 3),
            'input_tokens': {
                'colors': len(self._count_tokens(conversion_input.design_tokens.get('colors', {}))),
                'typography': len(self._count_tokens(conversion_input.design_tokens.get('typography', {}))),
                'spacing': len(self._count_tokens(conversion_input.design_tokens.get('spacing', {}))),
                'effects': len(self._count_tokens(conversion_input.design_tokens.get('effects', {})))
            },
            'output_tokens': {
                'colors': len(design_tokens.colors.semantic) + len(design_tokens.colors.neutral) + len(design_tokens.colors.brand),
                'typography_font_sizes': len(design_tokens.typography.font_sizes),
                'typography_font_weights': len(design_tokens.typography.font_weights),
                'spacing_values': len(design_tokens.spacing.scale),
                'effects_shadows': len(design_tokens.effects.shadows)
            },
            'components': {
                'input_count': len(conversion_input.component_catalog.components),
                'output_interfaces': len(component_interfaces),
                'categories': self._count_component_categories(conversion_input.component_catalog.components)
            },
            'platforms': {
                'web_config': True,
                'mobile_config': True,
                'css_variables': True
            },
            'quality_metrics': {
                'conversion_success_rate': 1.0,  # Will be updated after validation
                'token_coverage': 0.0,  # Will be calculated
                'interface_coverage': 0.0  # Will be calculated
            }
        }

        # Calculate quality metrics
        stats['quality_metrics']['token_coverage'] = self._calculate_token_coverage(stats)
        stats['quality_metrics']['interface_coverage'] = (
            stats['components']['output_interfaces'] / max(1, stats['components']['input_count'])
        )

        return stats

    def _count_tokens(self, token_dict: Dict[str, Any]) -> Dict[str, int]:
        """Count tokens in a nested dictionary."""
        count = 0

        def count_recursive(data):
            nonlocal count
            if isinstance(data, dict):
                for value in data.values():
                    count_recursive(value)
            elif isinstance(data, list):
                for item in data:
                    count_recursive(item)
            else:
                count += 1

        count_recursive(token_dict)
        return {'count': count}

    def _count_component_categories(self, components: List[ComponentDefinition]) -> Dict[str, int]:
        """Count components by category."""
        categories = {}
        for component in components:
            category_name = component.category.value
            categories[category_name] = categories.get(category_name, 0) + 1
        return categories

    def _calculate_token_coverage(self, stats: Dict[str, Any]) -> float:
        """Calculate token coverage percentage."""
        input_tokens = sum(stats['input_tokens'].values())
        output_tokens = sum(stats['output_tokens'].values())

        if input_tokens == 0:
            return 0.0

        return min(1.0, output_tokens / input_tokens)

    def save_output(self, output: ConversionOutput, output_path: str) -> Dict[str, str]:
        """
        Save conversion output to files.

        Args:
            output: ConversionOutput to save
            output_path: Directory path to save files

        Returns:
            Dict mapping file types to their saved paths
        """
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        saved_files = {}

        # Save complete output
        complete_output_path = f"{output_path}/conversion_output.json"
        with open(complete_output_path, 'w') as f:
            json.dump(output.to_dict(), f, indent=2)
        saved_files['complete'] = complete_output_path

        # Save Tailwind config
        tailwind_config_path = f"{output_path}/tailwind.config.json"
        with open(tailwind_config_path, 'w') as f:
            json.dump(output.tailwind_config.to_dict(), f, indent=2)
        saved_files['tailwind_config'] = tailwind_config_path

        # Save NativeWind config
        native_wind_config_path = f"{output_path}/nativewind.config.json"
        with open(native_wind_config_path, 'w') as f:
            json.dump(output.native_wind_config.to_dict(), f, indent=2)
        saved_files['nativewind_config'] = native_wind_config_path

        # Save component interfaces
        interfaces_config_path = f"{output_path}/component_interfaces.json"
        with open(interfaces_config_path, 'w') as f:
            json.dump([iface.to_dict() for iface in output.component_interfaces], f, indent=2)
        saved_files['component_interfaces'] = interfaces_config_path

        # Save TypeScript definitions
        typescript_definitions = self.interface_builder.generate_type_definitions_file(
            output.component_interfaces,
            DesignTokens()  # Empty tokens for now
        )
        typescript_definitions_path = f"{output_path}/design-system-types.ts"
        with open(typescript_definitions_path, 'w') as f:
            f.write(typescript_definitions)
        saved_files['typescript_definitions'] = typescript_definitions_path

        # Save CSS variables
        css_variables_path = f"{output_path}/design-system.css"
        with open(css_variables_path, 'w') as f:
            self._write_css_file(f, output.design_system_css)
        saved_files['css_variables'] = css_variables_path

        # Save platform configs
        for platform_config in output.platform_configs:
            platform_name = platform_config.platform.value
            platform_config_path = f"{output_path}/{platform_name}_config.json"
            with open(platform_config_path, 'w') as f:
                json.dump(platform_config.to_dict(), f, indent=2)
            saved_files[f'{platform_name}_config'] = platform_config_path

        # Save conversion report
        validation_result = self.validator.validate_conversion_output(output)
        report = self.validator.generate_validation_report(validation_result)
        report_path = f"{output_path}/conversion_report.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        saved_files['conversion_report'] = report_path

        return saved_files

    def _write_css_file(self, file, design_system_css) -> None:
        """Write design system CSS to file."""
        file.write("/* Design System CSS Variables */\n\n")

        # Write CSS variables
        file.write(":root {\n")
        for category, variables in design_system_css.variables.to_dict().items():
            file.write(f"  /* {category.title()} Variables */\n")
            for name, value in variables.items():
                file.write(f"  {name}: {value};\n")
            file.write("\n")
        file.write("}\n\n")

        # Write utility classes
        if design_system_css.utilities:
            file.write("/* Utility Classes */\n\n")
            for selector, styles in design_system_css.utilities.items():
                file.write(f"{selector} {{\n")
                file.write(f"  {styles}\n")
                file.write("}\n\n")

        # Write component classes
        if design_system_css.component_classes:
            file.write("/* Component Classes */\n\n")
            for selector, styles in design_system_css.component_classes.items():
                file.write(f"{selector} {{\n")
                # Properly format CSS styles
                for line in styles.strip().split('\n'):
                    if line.strip():
                        file.write(f"  {line.strip()}\n")
                file.write("}\n\n")

    def run_conversion(self, input_path: str, output_path: str) -> Dict[str, Any]:
        """
        Run complete conversion process from input file to output files.

        Args:
            input_path: Path to Stage 1 output JSON file
            output_path: Directory path for Stage 2 outputs

        Returns:
            Dict containing conversion results and saved file paths
        """
        print("🚀 Starting Stage 2: Design System Converter")
        print(f"📁 Input: {input_path}")
        print(f"📁 Output: {output_path}")
        print()

        # Load Stage 1 input
        print("📖 Loading Stage 1 output...")
        try:
            with open(input_path, 'r') as f:
                stage1_output = json.load(f)
            print("✅ Stage 1 output loaded successfully")
        except Exception as e:
            print(f"❌ Error loading Stage 1 output: {e}")
            raise

        # Run conversion
        print("🔄 Converting design system...")
        try:
            output = self.convert_design_system(stage1_output)
            print("✅ Design system conversion completed")
        except Exception as e:
            print(f"❌ Error during conversion: {e}")
            raise

        # Save outputs
        print("💾 Saving conversion outputs...")
        try:
            saved_files = self.save_output(output, output_path)
            print("✅ All outputs saved successfully")
        except Exception as e:
            print(f"❌ Error saving outputs: {e}")
            raise

        # Generate summary
        print()
        print("=" * 60)
        print("STAGE 2 CONVERSION SUMMARY")
        print("=" * 60)
        print(f"✅ Conversion completed in {output.conversion_stats['conversion_duration_seconds']}s")
        print(f"🎨 Colors: {output.conversion_stats['output_tokens']['colors']}")
        print(f"📝 Typography sizes: {output.conversion_stats['output_tokens']['typography_font_sizes']}")
        print(f"📏 Spacing values: {output.conversion_stats['output_tokens']['spacing_values']}")
        print(f"🧩 Component interfaces: {output.conversion_stats['components']['output_interfaces']}")
        print()
        print("📁 Generated files:")
        for file_type, file_path in saved_files.items():
            print(f"  📄 {file_type}: {file_path}")

        # Run validation
        validation_result = self.validator.validate_conversion_output(output)
        print()
        if validation_result['valid']:
            print("✅ All validations passed!")
        else:
            print(f"⚠️  Found {len(validation_result['errors'])} errors and {len(validation_result['warnings'])} warnings")
            print(f"📄 See conversion_report.txt for details")

        return {
            'success': True,
            'output': output,
            'saved_files': saved_files,
            'validation_result': validation_result
        }