"""
Design Asset Extractor - Stage 1 of Figma-to-Code Pipeline

Extracts structured design assets from Figma designs:
- Design tokens (colors, typography, spacing, effects)
- Component catalog with variants and properties
- Screen layouts and hierarchy information

Builds on the existing figma_sdk for Figma API integration.
"""

from .extractor import DesignAssetExtractor, extract_from_figma_file, extract_from_file_key
from .token_extractor import TokenExtractor
from .component_parser import ComponentParser
from .layout_analyzer import LayoutAnalyzer

__version__ = "1.0.0"
__all__ = [
    "DesignAssetExtractor",
    "extract_from_figma_file",
    "extract_from_file_key",
    "TokenExtractor",
    "ComponentParser",
    "LayoutAnalyzer"
]