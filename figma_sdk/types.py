"""
Type definitions for the Figma SDK.

Provides type hints for common Figma API data structures.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum


class NodeType(Enum):
    """Figma node types."""
    DOCUMENT = "DOCUMENT"
    CANVAS = "CANVAS"
    FRAME = "FRAME"
    GROUP = "GROUP"
    COMPONENT = "COMPONENT"
    INSTANCE = "INSTANCE"
    TEXT = "TEXT"
    RECTANGLE = "RECTANGLE"
    ELLIPSE = "ELLIPSE"
    LINE = "LINE"
    VECTOR = "VECTOR"
    STAR = "STAR"
    IMAGE = "IMAGE"


class BlendMode(Enum):
    """Blend mode options."""
    PASS_THROUGH = "PASS_THROUGH"
    NORMAL = "NORMAL"
    DARKEN = "DARKEN"
    MULTIPLY = "MULTPLY"
    LINEAR_BURN = "LINEAR_BURN"
    COLOR_BURN = "COLOR_BURN"
    LIGHTEN = "LIGHTEN"
    SCREEN = "SCREEN"
    LINEAR_DODGE = "LINEAR_DODGE"
    COLOR_DODGE = "COLOR_DODGE"
    OVERLAY = "OVERLAY"
    SOFT_LIGHT = "SOFT_LIGHT"
    HARD_LIGHT = "HARD_LIGHT"
    DIFFERENCE = "DIFFERENCE"
    EXCLUSION = "EXCLUSION"
    HUE = "HUE"
    SATURATION = "SATURATION"
    COLOR = "COLOR"
    LUMINOSITY = "LUMINOSITY"


@dataclass
class Color:
    """RGB color representation."""
    r: float  # 0-1
    g: float  # 0-1
    b: float  # 0-1
    a: float = 1.0  # 0-1

    def to_hex(self) -> str:
        """Convert to hex color string."""
        return f"#{int(self.r*255):02x}{int(self.g*255):02x}{int(self.b*255):02x}"


@dataclass
class Vector2D:
    """2D vector/point representation."""
    x: float
    y: float


@dataclass
class BoundingBox:
    """Bounding box dimensions and position."""
    x: float
    y: float
    width: float
    height: float


@dataclass
class Style:
    """Base style information."""
    key: str
    name: str
    description: str
    style_type: str
    thumbnail_url: str
    remote: bool = False


@dataclass
class Component:
    """Component information."""
    key: str
    name: str
    description: str
    node_id: str
    thumbnail_url: str
    component_set_id: Optional[str] = None


# Raw API types (matching Figma's JSON structure)
DocumentNode = Dict[str, Any]
SceneNode = Dict[str, Any]
FigmaFile = Dict[str, Any]
StyleMap = Dict[str, Style]
ComponentMap = Dict[str, Component]