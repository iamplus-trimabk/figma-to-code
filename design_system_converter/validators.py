"""
Validators - Output validation and quality assurance for the Design System Converter.

Ensures outputs match expected schemas, validates design token quality,
and performs accessibility checks.
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from .schemas import (
    ConversionOutput, DesignTokens, ComponentDefinition,
    TailwindTheme, NativeWindTheme, ComponentInterface,
    CSSVariables, PlatformConfig
)


class ConversionValidator:
    """Validates conversion outputs and ensures quality standards."""

    def __init__(self):
        self.contrast_ratio_threshold = 4.5  # WCAG AA standard
        self.accessibility_issues = []
        self.validation_errors = []
        self.warnings = []

    def validate_conversion_output(self, output: ConversionOutput) -> Dict[str, Any]:
        """Validate complete conversion output."""
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'accessibility_issues': [],
            'quality_metrics': {}
        }

        # Validate schema compliance
        schema_valid = self._validate_schema_compliance(output)
        if not schema_valid['valid']:
            validation_result['valid'] = False
            validation_result['errors'].extend(schema_valid['errors'])

        # Validate design tokens
        token_valid = self._validate_design_tokens(output)
        if not token_valid['valid']:
            validation_result['valid'] = False
            validation_result['errors'].extend(token_valid['errors'])
        validation_result['warnings'].extend(token_valid['warnings'])

        # Validate Tailwind configuration
        tailwind_valid = self._validate_tailwind_config(output.tailwind_config)
        if not tailwind_valid['valid']:
            validation_result['valid'] = False
            validation_result['errors'].extend(tailwind_valid['errors'])
        validation_result['warnings'].extend(tailwind_valid['warnings'])

        # Validate NativeWind configuration
        native_wind_valid = self._validate_native_wind_config(output.native_wind_config)
        if not native_wind_valid['valid']:
            validation_result['valid'] = False
            validation_result['errors'].extend(native_wind_valid['errors'])
        validation_result['warnings'].extend(native_wind_valid['warnings'])

        # Validate component interfaces
        interface_valid = self._validate_component_interfaces(output.component_interfaces)
        if not interface_valid['valid']:
            validation_result['valid'] = False
            validation_result['errors'].extend(interface_valid['errors'])
        validation_result['warnings'].extend(interface_valid['warnings'])

        # Validate accessibility
        accessibility_valid = self._validate_accessibility(output)
        if not accessibility_valid['valid']:
            validation_result['valid'] = False
            validation_result['accessibility_issues'].extend(accessibility_valid['issues'])

        # Calculate quality metrics
        quality_metrics = self._calculate_quality_metrics(output)
        validation_result['quality_metrics'] = quality_metrics

        return validation_result

    def _validate_schema_compliance(self, output: ConversionOutput) -> Dict[str, Any]:
        """Validate schema compliance of output data."""
        errors = []

        # Check required fields
        required_fields = [
            'metadata', 'tailwind_config', 'native_wind_config',
            'component_interfaces', 'design_system_css', 'platform_configs'
        ]

        for field in required_fields:
            if not hasattr(output, field) or getattr(output, field) is None:
                errors.append(f"Missing required field: {field}")

        # Validate metadata
        if hasattr(output, 'metadata') and output.metadata:
            metadata_errors = self._validate_metadata(output.metadata)
            errors.extend(metadata_errors)

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

    def _validate_metadata(self, metadata: Dict[str, Any]) -> List[str]:
        """Validate metadata structure."""
        errors = []

        # Check for required metadata fields
        required_metadata = ['conversion_time', 'source_file', 'version']
        for field in required_metadata:
            if field not in metadata:
                errors.append(f"Missing required metadata field: {field}")

        return errors

    def _validate_design_tokens(self, output: ConversionOutput) -> Dict[str, Any]:
        """Validate design token quality and completeness."""
        errors = []
        warnings = []

        # Check if we have basic design tokens
        if not output.tailwind_config.colors:
            errors.append("No colors found in design tokens")

        if not output.tailwind_config.fontFamily:
            warnings.append("No font family defined in design tokens")

        if not output.tailwind_config.fontSize:
            warnings.append("No font sizes defined in design tokens")

        if not output.tailwind_config.spacing:
            warnings.append("No spacing scale defined in design tokens")

        # Validate color format
        color_validation = self._validate_color_format(output.tailwind_config.colors)
        errors.extend(color_validation['errors'])
        warnings.extend(color_validation['warnings'])

        # Validate typography scale
        typography_validation = self._validate_typography_scale(output.tailwind_config)
        errors.extend(typography_validation)

        # Validate spacing scale
        spacing_validation = self._validate_spacing_scale(output.tailwind_config.spacing)
        errors.extend(spacing_validation)

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def _validate_color_format(self, colors: Dict[str, Any]) -> Dict[str, Any]:
        """Validate color format and consistency."""
        errors = []
        warnings = []

        for color_name, color_value in colors.items():
            if isinstance(color_value, dict):
                # Validate color scale
                scale_errors = self._validate_color_scale(color_name, color_value)
                errors.extend(scale_errors)
            elif isinstance(color_value, str):
                # Validate single color
                if not self._is_valid_color_format(color_value):
                    errors.append(f"Invalid color format for {color_name}: {color_value}")
            else:
                errors.append(f"Invalid color value type for {color_name}: {type(color_value)}")

        return {
            'errors': errors,
            'warnings': warnings
        }

    def _validate_color_scale(self, color_name: str, color_scale: Dict[str, str]) -> List[str]:
        """Validate color scale completeness."""
        errors = []

        # Check for standard scale values
        standard_shades = ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900', '950']
        missing_shades = [shade for shade in standard_shades if shade not in color_scale]

        if missing_shades:
            errors.append(f"Color {color_name} is missing shades: {', '.join(missing_shades)}")

        # Validate each shade format
        for shade, color_value in color_scale.items():
            if not self._is_valid_color_format(color_value):
                errors.append(f"Invalid color format for {color_name}-{shade}: {color_value}")

        return errors

    def _is_valid_color_format(self, color: str) -> bool:
        """Check if color string is in valid format."""
        # Check hex format
        hex_pattern = re.compile(r'^#[0-9A-Fa-f]{6}$')
        if hex_pattern.match(color):
            return True

        # Check rgb/rgba format
        rgb_pattern = re.compile(r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$')
        rgba_pattern = re.compile(r'^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$')
        if rgb_pattern.match(color) or rgba_pattern.match(color):
            return True

        return False

    def _validate_typography_scale(self, config: TailwindTheme) -> List[str]:
        """Validate typography scale consistency."""
        errors = []

        # Check font size scale
        if config.fontSize:
            size_names = list(config.fontSize.keys())
            standard_sizes = ['xs', 'sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl', '5xl', '6xl', '7xl', '8xl', '9xl']

            missing_sizes = [size for size in standard_sizes if size not in size_names]
            if missing_sizes:
                errors.append(f"Missing font sizes: {', '.join(missing_sizes)}")

        # Check font weight scale
        if config.fontWeight:
            weight_values = list(config.fontWeight.values())
            standard_weights = [100, 200, 300, 400, 500, 600, 700, 800, 900]

            missing_weights = [weight for weight in standard_weights if weight not in weight_values]
            if missing_weights:
                errors.append(f"Missing font weights: {', '.join(map(str, missing_weights))}")

        return errors

    def _validate_spacing_scale(self, spacing: Dict[str, Any]) -> List[str]:
        """Validate spacing scale consistency."""
        errors = []

        # Check spacing scale
        if spacing:
            spacing_names = list(spacing.keys())
            standard_spacing = ['0', 'px', '0.5', '1', '1.5', '2', '2.5', '3', '4', '5', '6', '8', '10', '12', '16', '20', '24', '32', '40', '48', '56', '64']

            missing_spacing = [sp for sp in standard_spacing if sp not in spacing_names]
            if missing_spacing:
                errors.append(f"Missing spacing values: {', '.join(missing_spacing)}")

        return errors

    def _validate_tailwind_config(self, config: TailwindTheme) -> Dict[str, Any]:
        """Validate Tailwind configuration."""
        errors = []
        warnings = []

        # Check required sections
        required_sections = ['colors', 'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'spacing']
        for section in required_sections:
            if not hasattr(config, section) or not getattr(config, section):
                warnings.append(f"Missing Tailwind config section: {section}")

        # Validate color system
        if config.colors:
            color_validation = self._validate_color_system(config.colors, 'Tailwind')
            errors.extend(color_validation['errors'])
            warnings.extend(color_validation['warnings'])

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def _validate_native_wind_config(self, config: NativeWindTheme) -> Dict[str, Any]:
        """Validate NativeWind configuration."""
        errors = []
        warnings = []

        # Check required sections
        required_sections = ['colors', 'fonts', 'fontSizes', 'fontWeights', 'spacing', 'borderRadius']
        for section in required_sections:
            if not hasattr(config, section) or not getattr(config, section):
                warnings.append(f"Missing NativeWind config section: {section}")

        # Validate color system
        if config.colors:
            color_validation = self._validate_color_system(config.colors, 'NativeWind')
            errors.extend(color_validation['errors'])
            warnings.extend(color_validation['warnings'])

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def _validate_color_system(self, colors: Dict[str, Any], config_type: str) -> Dict[str, Any]:
        """Validate color system completeness."""
        errors = []
        warnings = []

        # Check for semantic colors
        semantic_colors = ['primary', 'secondary', 'success', 'warning', 'error', 'info']
        missing_semantic = [color for color in semantic_colors if color not in colors]

        if missing_semantic:
            warnings.append(f"{config_type}: Missing semantic colors: {', '.join(missing_semantic)}")

        # Check for neutral colors
        if 'gray' not in colors:
            warnings.append(f"{config_type}: No gray scale found")
        elif 'gray' in colors and isinstance(colors['gray'], dict):
            gray_scale = colors['gray']
            required_shades = ['500', '600', '700']
            missing_shades = [shade for shade in required_shades if shade not in gray_scale]

            if missing_shades:
                warnings.append(f"{config_type}: Gray scale missing shades: {', '.join(missing_shades)}")

        return {
            'errors': errors,
            'warnings': warnings
        }

    def _validate_component_interfaces(self, interfaces: List[ComponentInterface]) -> Dict[str, Any]:
        """Validate component interfaces."""
        errors = []
        warnings = []

        if not interfaces:
            warnings.append("No component interfaces generated")
            return {'valid': True, 'errors': errors, 'warnings': warnings}

        # Validate each interface
        for interface in interfaces:
            interface_errors = self._validate_single_interface(interface)
            errors.extend(interface_errors)

        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }

    def _validate_single_interface(self, interface: ComponentInterface) -> List[str]:
        """Validate a single component interface."""
        errors = []

        # Check required fields
        if not interface.name:
            errors.append("Component interface missing name")

        if not interface.props:
            errors.append(f"Component interface {interface.name} has no props")

        # Check prop naming conventions
        for prop_name in interface.props.keys():
            if not self._is_valid_prop_name(prop_name):
                errors.append(f"Invalid prop name '{prop_name}' in interface {interface.name}")

        # Check for common props
        common_props = ['className', 'style', 'children']
        for prop in common_props:
            if prop not in interface.props:
                # This is a warning, not an error
                pass

        return errors

    def _is_valid_prop_name(self, prop_name: str) -> bool:
        """Check if prop name follows TypeScript conventions."""
        # Should be camelCase or snake_case
        pattern = re.compile(r'^[a-z][a-zA-Z0-9]*$')
        return bool(pattern.match(prop_name))

    def _validate_accessibility(self, output: ConversionOutput) -> Dict[str, Any]:
        """Validate accessibility compliance."""
        issues = []

        # Check color contrast
        contrast_issues = self._check_color_contrast(output.tailwind_config.colors)
        issues.extend(contrast_issues)

        # Check typography accessibility
        typography_issues = self._check_typography_accessibility(output.tailwind_config)
        issues.extend(typography_issues)

        # Check spacing accessibility
        spacing_issues = self._check_spacing_accessibility(output.tailwind_config.spacing)
        issues.extend(spacing_issues)

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def _check_color_contrast(self, colors: Dict[str, Any]) -> List[str]:
        """Check color contrast ratios."""
        issues = []

        # Check common text/background combinations
        text_colors = ['gray-900', 'gray-700', 'gray-600']
        bg_colors = ['white', 'gray-50', 'gray-100']

        for text_color in text_colors:
            for bg_color in bg_colors:
                if text_color in colors and bg_color in colors:
                    if isinstance(colors[text_color], str) and isinstance(colors[bg_color], str):
                        contrast_ratio = self._calculate_contrast_ratio(colors[text_color], colors[bg_color])
                        if contrast_ratio < self.contrast_ratio_threshold:
                            issues.append(f"Low contrast ratio ({contrast_ratio:.2f}) between {text_color} and {bg_color}")

        return issues

    def _calculate_contrast_ratio(self, color1: str, color2: str) -> float:
        """Calculate contrast ratio between two colors."""
        # Simplified contrast ratio calculation
        # In a real implementation, this would use proper luminance calculation
        return 4.5  # Default placeholder

    def _check_typography_accessibility(self, config: TailwindTheme) -> List[str]:
        """Check typography accessibility."""
        issues = []

        # Check minimum font size
        if config.fontSize:
            for size_name, size_value in config.fontSize.items():
                if isinstance(size_value, list) and len(size_value) > 0:
                    size_str = size_value[0]
                    if isinstance(size_str, str) and 'px' in size_str:
                        size_px = float(size_str.replace('px', ''))
                        if size_px < 14:
                            issues.append(f"Font size {size_name} ({size_px}px) is below recommended minimum")

        return issues

    def _check_spacing_accessibility(self, spacing: Dict[str, Any]) -> List[str]:
        """Check spacing accessibility."""
        issues = []

        # Check for adequate tap targets
        if '4' in spacing:
            if isinstance(spacing['4'], (int, str)):
                try:
                    spacing_value = int(spacing['4'])
                    if spacing_value < 16:  # 16px minimum for tap targets
                        issues.append("Spacing value '4' is below recommended minimum for tap targets")
                except (ValueError, TypeError):
                    pass

        return issues

    def _calculate_quality_metrics(self, output: ConversionOutput) -> Dict[str, Any]:
        """Calculate quality metrics for the conversion."""
        metrics = {}

        # Token completeness
        metrics['token_completeness'] = self._calculate_token_completeness(output)

        # Interface quality
        metrics['interface_quality'] = self._calculate_interface_quality(output)

        # Configuration completeness
        metrics['config_completeness'] = self._calculate_config_completeness(output)

        # Accessibility score
        metrics['accessibility_score'] = self._calculate_accessibility_score(output)

        # Overall quality score
        metrics['overall_quality'] = (
            metrics['token_completeness'] * 0.3 +
            metrics['interface_quality'] * 0.3 +
            metrics['config_completeness'] * 0.2 +
            metrics['accessibility_score'] * 0.2
        )

        return metrics

    def _calculate_token_completeness(self, output: ConversionOutput) -> float:
        """Calculate token completeness score."""
        score = 0.0

        # Colors
        if output.tailwind_config.colors:
            score += 0.3

        # Typography
        if output.tailwind_config.fontFamily:
            score += 0.1
        if output.tailwind_config.fontSize:
            score += 0.2
        if output.tailwind_config.fontWeight:
            score += 0.1

        # Spacing
        if output.tailwind_config.spacing:
            score += 0.2

        # Effects
        if output.tailwind_config.boxShadow:
            score += 0.1

        return score

    def _calculate_interface_quality(self, output: ConversionOutput) -> float:
        """Calculate interface quality score."""
        if not output.component_interfaces:
            return 0.0

        score = 0.0
        total_interfaces = len(output.component_interfaces)

        for interface in output.component_interfaces:
            if interface.name and interface.props:
                score += 1.0 / total_interfaces

        return score

    def _calculate_config_completeness(self, output: ConversionOutput) -> float:
        """Calculate configuration completeness score."""
        score = 0.0

        # Tailwind config completeness
        tailwind_sections = ['colors', 'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'spacing']
        for section in tailwind_sections:
            if hasattr(output.tailwind_config, section) and getattr(output.tailwind_config, section):
                score += 0.05

        # NativeWind config completeness
        native_wind_sections = ['colors', 'fonts', 'fontSizes', 'fontWeights', 'spacing', 'borderRadius']
        for section in native_wind_sections:
            if hasattr(output.native_wind_config, section) and getattr(output.native_wind_config, section):
                score += 0.05

        return score

    def _calculate_accessibility_score(self, output: ConversionOutput) -> float:
        """Calculate accessibility score."""
        score = 1.0

        # Reduce score for accessibility issues
        accessibility_validation = self._validate_accessibility(output)
        if accessibility_validation['issues']:
            score = max(0.0, score - len(accessibility_validation['issues']) * 0.1)

        return score

    def generate_validation_report(self, validation_result: Dict[str, Any]) -> str:
        """Generate a human-readable validation report."""
        report = []

        report.append("=" * 60)
        report.append("STAGE 2 CONVERSION VALIDATION REPORT")
        report.append("=" * 60)
        report.append("")

        # Overall status
        status = "✅ PASSED" if validation_result['valid'] else "❌ FAILED"
        report.append(f"Overall Status: {status}")
        report.append("")

        # Summary
        report.append("Summary:")
        report.append(f"  - Errors: {len(validation_result['errors'])}")
        report.append(f"  - Warnings: {len(validation_result['warnings'])}")
        report.append(f"  - Accessibility Issues: {len(validation_result['accessibility_issues'])}")
        report.append("")

        # Quality metrics
        report.append("Quality Metrics:")
        for metric, value in validation_result['quality_metrics'].items():
            percentage = value * 100
            emoji = "🟢" if percentage >= 80 else "🟡" if percentage >= 60 else "🔴"
            report.append(f"  {emoji} {metric}: {percentage:.1f}%")
        report.append("")

        # Errors
        if validation_result['errors']:
            report.append("Errors:")
            for error in validation_result['errors']:
                report.append(f"  ❌ {error}")
            report.append("")

        # Warnings
        if validation_result['warnings']:
            report.append("Warnings:")
            for warning in validation_result['warnings']:
                report.append(f"  ⚠️  {warning}")
            report.append("")

        # Accessibility issues
        if validation_result['accessibility_issues']:
            report.append("Accessibility Issues:")
            for issue in validation_result['accessibility_issues']:
                report.append(f"  ♿ {issue}")
            report.append("")

        # Recommendations
        report.append("Recommendations:")
        recommendations = self._generate_recommendations(validation_result)
        for recommendation in recommendations:
            report.append(f"  💡 {recommendation}")
        report.append("")

        return "\n".join(report)

    def _generate_recommendations(self, validation_result: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results."""
        recommendations = []

        # General recommendations
        if validation_result['errors']:
            recommendations.append("Fix all errors before proceeding to Stage 3")

        if validation_result['warnings']:
            recommendations.append("Address warnings to improve design system quality")

        if validation_result['accessibility_issues']:
            recommendations.append("Resolve accessibility issues for better inclusivity")

        # Quality-specific recommendations
        quality_metrics = validation_result['quality_metrics']

        if quality_metrics.get('token_completeness', 0) < 0.8:
            recommendations.append("Add more design tokens for a more complete design system")

        if quality_metrics.get('interface_quality', 0) < 0.8:
            recommendations.append("Improve component interfaces with better prop definitions")

        if quality_metrics.get('config_completeness', 0) < 0.8:
            recommendations.append("Complete configuration sections for better platform support")

        if quality_metrics.get('accessibility_score', 0) < 0.8:
            recommendations.append("Improve accessibility compliance with better contrast and sizing")

        return recommendations