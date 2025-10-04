"""
Design System Converter - Stage 2 of Figma-to-Code Pipeline

Converts raw design assets from Stage 1 into production-ready design system
configurations for multiple platforms (Web with Tailwind CSS, Mobile with NativeWind).
"""

from .converter import DesignSystemConverter
from .token_converter import TokenConverter
from .style_generator import StyleGenerator
from .interface_builder import InterfaceBuilder
from .platform_configs import PlatformConfigs
from .schemas import ConversionOutput, DesignTokens
from .validators import ConversionValidator

__version__ = "1.0.0"
__all__ = [
    "DesignSystemConverter",
    "TokenConverter",
    "StyleGenerator",
    "InterfaceBuilder",
    "PlatformConfigs",
    "ConversionOutput",
    "DesignTokens",
    "ConversionValidator"
]