"""
Data schemas and type definitions for the Design System Converter.

Defines the structure of input data from Stage 1 and output data for Stage 3.
"""

from typing import Dict, List, Optional, Any, Union, Literal
from dataclasses import dataclass, field
from enum import Enum


class PlatformType(Enum):
    """Supported target platforms."""
    WEB = "web"
    MOBILE = "mobile"


class ComponentCategory(Enum):
    """Component categories from design extraction."""
    DISPLAY = "display"
    INTERACTIVE = "interactive"
    BUTTONS = "buttons"


@dataclass
class ColorPalette:
    """Color palette definition."""
    semantic: Dict[str, str] = field(default_factory=dict)
    neutral: Dict[str, str] = field(default_factory=dict)
    brand: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "semantic": self.semantic,
            "neutral": self.neutral,
            "brand": self.brand
        }


@dataclass
class TypographyTokens:
    """Typography token definitions."""
    font_family: str = "Poppins"
    font_sizes: Dict[str, Union[int, float]] = field(default_factory=dict)
    font_weights: Dict[str, int] = field(default_factory=dict)
    line_heights: Dict[str, Union[int, float]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fontFamily": self.font_family,
            "fontSizes": self.font_sizes,
            "fontWeights": self.font_weights,
            "lineHeights": self.line_heights
        }


@dataclass
class SpacingTokens:
    """Spacing token definitions."""
    scale: Dict[str, int] = field(default_factory=dict)
    semantic: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scale": self.scale,
            "semantic": self.semantic
        }


@dataclass
class EffectTokens:
    """Effect tokens for shadows, blurs, etc."""
    shadows: List[Dict[str, Any]] = field(default_factory=list)
    blurs: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "shadows": self.shadows,
            "blurs": self.blurs
        }


@dataclass
class DesignTokens:
    """Complete design tokens from Stage 1."""
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: TypographyTokens = field(default_factory=TypographyTokens)
    spacing: SpacingTokens = field(default_factory=SpacingTokens)
    effects: EffectTokens = field(default_factory=EffectTokens)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "colors": self.colors.to_dict(),
            "typography": self.typography.to_dict(),
            "spacing": self.spacing.to_dict(),
            "effects": self.effects.to_dict()
        }


@dataclass
class ComponentVariant:
    """Component variant definition."""
    name: str
    props: Dict[str, Any]
    example_usage: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "props": self.props,
            "exampleUsage": self.example_usage
        }


@dataclass
class ComponentDefinition:
    """Component definition from extraction."""
    name: str
    type: str
    category: ComponentCategory
    props: Dict[str, Any]
    variants: List[ComponentVariant] = field(default_factory=list)
    children: List[Dict[str, Any]] = field(default_factory=list)
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "category": self.category.value,
            "props": self.props,
            "variants": [v.to_dict() for v in self.variants],
            "children": self.children,
            "description": self.description
        }


@dataclass
class ComponentCatalog:
    """Complete component catalog from Stage 1."""
    components: List[ComponentDefinition] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "components": [c.to_dict() for c in self.components]
        }


@dataclass
class TailwindTheme:
    """Tailwind CSS theme configuration."""
    colors: Dict[str, Any] = field(default_factory=dict)
    fontFamily: Dict[str, Any] = field(default_factory=dict)
    fontSize: Dict[str, Any] = field(default_factory=dict)
    fontWeight: Dict[str, Any] = field(default_factory=dict)
    lineHeight: Dict[str, Any] = field(default_factory=dict)
    spacing: Dict[str, Any] = field(default_factory=dict)
    borderRadius: Dict[str, Any] = field(default_factory=dict)
    boxShadow: Dict[str, Any] = field(default_factory=dict)
    blur: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "colors": self.colors,
            "fontFamily": self.fontFamily,
            "fontSize": self.fontSize,
            "fontWeight": self.fontWeight,
            "lineHeight": self.lineHeight,
            "spacing": self.spacing,
            "borderRadius": self.borderRadius,
            "boxShadow": self.boxShadow,
            "blur": self.blur
        }


@dataclass
class NativeWindTheme:
    """NativeWind theme configuration for React Native."""
    colors: Dict[str, Any] = field(default_factory=dict)
    fonts: Dict[str, Any] = field(default_factory=dict)
    fontSizes: Dict[str, Any] = field(default_factory=dict)
    fontWeights: Dict[str, Any] = field(default_factory=dict)
    spacing: Dict[str, Any] = field(default_factory=dict)
    borderRadius: Dict[str, Any] = field(default_factory=dict)
    shadows: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "colors": self.colors,
            "fonts": self.fonts,
            "fontSizes": self.fontSizes,
            "fontWeights": self.fontWeights,
            "spacing": self.spacing,
            "borderRadius": self.borderRadius,
            "shadows": self.shadows
        }


@dataclass
class ComponentInterface:
    """TypeScript interface for a component."""
    name: str
    description: str
    props: Dict[str, Any]
    variants: List[Dict[str, Any]] = field(default_factory=list)
    extends: List[str] = field(default_factory=list)
    generics: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "props": self.props,
            "variants": self.variants,
            "extends": self.extends,
            "generics": self.generics
        }


@dataclass
class CSSVariables:
    """CSS custom properties definition."""
    colors: Dict[str, str] = field(default_factory=dict)
    typography: Dict[str, str] = field(default_factory=dict)
    spacing: Dict[str, str] = field(default_factory=dict)
    effects: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "colors": self.colors,
            "typography": self.typography,
            "spacing": self.spacing,
            "effects": self.effects
        }


@dataclass
class DesignSystemCSS:
    """Complete design system CSS definition."""
    variables: CSSVariables = field(default_factory=CSSVariables)
    utilities: Dict[str, str] = field(default_factory=dict)
    component_classes: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "variables": self.variables.to_dict(),
            "utilities": self.utilities,
            "componentClasses": self.component_classes
        }


@dataclass
class PlatformConfig:
    """Platform-specific configuration."""
    platform: PlatformType
    config: Dict[str, Any]
    optimizations: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform": self.platform.value,
            "config": self.config,
            "optimizations": self.optimizations
        }


@dataclass
class ConversionOutput:
    """Complete output from Stage 2 conversion."""
    metadata: Dict[str, Any]
    tailwind_config: TailwindTheme = field(default_factory=TailwindTheme)
    native_wind_config: NativeWindTheme = field(default_factory=NativeWindTheme)
    component_interfaces: List[ComponentInterface] = field(default_factory=list)
    design_system_css: DesignSystemCSS = field(default_factory=DesignSystemCSS)
    platform_configs: List[PlatformConfig] = field(default_factory=list)
    conversion_stats: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata,
            "tailwind_config": self.tailwind_config.to_dict(),
            "native_wind_config": self.native_wind_config.to_dict(),
            "component_interfaces": [c.to_dict() for c in self.component_interfaces],
            "design_system_css": self.design_system_css.to_dict(),
            "platform_configs": [c.to_dict() for c in self.platform_configs],
            "conversion_stats": self.conversion_stats
        }


@dataclass
class ConversionInput:
    """Input data for Stage 2 conversion."""
    design_tokens: DesignTokens
    component_catalog: ComponentCatalog
    screen_layouts: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "design_tokens": self.design_tokens.to_dict(),
            "component_catalog": self.component_catalog.to_dict(),
            "screen_layouts": self.screen_layouts,
            "metadata": self.metadata
        }