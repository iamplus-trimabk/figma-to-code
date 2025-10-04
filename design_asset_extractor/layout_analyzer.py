"""
Layout Analyzer - Analyze screen layouts and structure.

Extracts layout information, positioning data, and hierarchical
structure from Figma frames and pages.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List, Optional, Tuple
from collections import defaultdict
import figma_sdk
from .schemas import ScreenLayout
from .utils import calculate_distance, find_common_values


class LayoutAnalyzer:
    """Analyze layout structure and positioning from Figma document."""

    def __init__(self, figma_file: 'figma_sdk.files.FigmaFile'):
        """Initialize with FigmaFile instance."""
        self.figma_file = figma_file
        self.document = figma_file.document

        # Storage for layout information
        self.screens: List[ScreenLayout] = []
        self.layout_patterns: Dict[str, Any] = defaultdict(list)
        self.spacing_patterns: List[float] = []
        self.grid_systems: List[Dict[str, Any]] = []

    def analyze_all_layouts(self) -> Dict[str, Any]:
        """Analyze all layouts in the document."""
        print("📐 Analyzing layouts...")

        # Extract screen information
        self._extract_screens(self.document)

        # Analyze layout patterns
        self._analyze_layout_patterns()

        # Detect grid systems
        self._detect_grid_systems()

        # Build final layout output
        return self._build_layout_output()

    def _extract_screens(self, node: Dict[str, Any], depth: int = 0) -> None:
        """Extract screen information from document hierarchy."""
        if not isinstance(node, dict):
            return

        node_type = node.get("type", "").upper()
        node_name = node.get("name", "")

        # Consider frames as screens
        if node_type == "FRAME" and depth > 0:
            screen_layout = self._create_screen_layout(node)
            if screen_layout:
                self.screens.append(screen_layout)

        # Also consider top-level CANVAS nodes as screens
        elif node_type == "CANVAS" and depth == 1:
            screen_layout = self._create_screen_layout(node)
            if screen_layout:
                self.screens.append(screen_layout)

        # Traverse children
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                self._extract_screens(child, depth + 1)

    def _create_screen_layout(self, node: Dict[str, Any]) -> Optional[ScreenLayout]:
        """Create a screen layout from a frame or canvas node."""
        if not isinstance(node, dict):
            return None

        node_type = node.get("type", "").upper()
        node_name = node.get("name", "")

        # Get size information
        size = self._extract_size_info(node)
        if not size:
            return None

        # Get background color
        background_color = self._extract_background_color(node)

        # Extract children information
        children = self._extract_children_layouts(node)

        # Analyze layout properties
        layout_info = self._analyze_layout_properties(node)

        return ScreenLayout(
            name=node_name,
            type=node_type.lower(),
            size=size,
            background_color=background_color,
            children=children,
            layout=layout_info,
            description=f"{node_type} screen: {node_name}"
        )

    def _extract_size_info(self, node: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """Extract size information from node."""
        # Try absolute bounding box first
        if "absoluteBoundingBox" in node:
            bbox = node["absoluteBoundingBox"]
            return {
                "width": bbox.get("width", 0),
                "height": bbox.get("height", 0),
                "x": bbox.get("x", 0),
                "y": bbox.get("y", 0)
            }

        # Try regular bounding box
        if "boundingBox" in node:
            bbox = node["boundingBox"]
            return {
                "width": bbox.get("width", 0),
                "height": bbox.get("height", 0),
                "x": bbox.get("x", 0),
                "y": bbox.get("y", 0)
            }

        # Try size properties
        width = node.get("width", 0)
        height = node.get("height", 0)
        if width > 0 and height > 0:
            return {
                "width": width,
                "height": height,
                "x": 0,
                "y": 0
            }

        return None

    def _extract_background_color(self, node: Dict[str, Any]) -> Optional[str]:
        """Extract background color from node."""
        if "fills" not in node or not node["fills"]:
            return None

        for fill in node["fills"]:
            if fill.get("type") == "SOLID" and "color" in fill and fill.get("visible", True):
                color = fill["color"]
                # Convert RGB to hex
                r = int(color["r"] * 255)
                g = int(color["g"] * 255)
                b = int(color["b"] * 255)
                return f"#{r:02x}{g:02x}{b:02x}"

        return None

    def _extract_children_layouts(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract layout information for children."""
        children = []

        if "children" not in node or not isinstance(node["children"], list):
            return children

        for i, child in enumerate(node["children"]):
            child_info = self._extract_child_layout_info(child, i)
            if child_info:
                children.append(child_info)

        return children

    def _extract_child_layout_info(self, node: Dict[str, Any], index: int) -> Optional[Dict[str, Any]]:
        """Extract layout information for a single child."""
        if not isinstance(node, dict):
            return None

        child_type = node.get("type", "").lower()
        child_name = node.get("name", "")

        # Get positioning information
        size_info = self._extract_size_info(node)
        if not size_info:
            return None

        child_info = {
            "name": child_name,
            "type": child_type,
            "index": index,
            "size": {
                "width": size_info["width"],
                "height": size_info["height"]
            },
            "position": {
                "x": size_info["x"],
                "y": size_info["y"]
            },
            "visible": node.get("visible", True)
        }

        # Add component reference if this is a known component
        # This would be populated by the component parser
        child_info["component_ref"] = None

        # Add styling information
        child_info["style"] = self._extract_child_style_info(node)

        # Add constraints if available
        if "constraints" in node:
            child_info["constraints"] = node["constraints"]

        return child_info

    def _extract_child_style_info(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract style information for a child node."""
        style_info = {}

        # Background colors
        if "fills" in node and node["fills"]:
            fills = []
            for fill in node["fills"]:
                if fill.get("type") == "SOLID" and "color" in fill:
                    color = fill["color"]
                    r = int(color["r"] * 255)
                    g = int(color["g"] * 255)
                    b = int(color["b"] * 255)
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    fills.append(hex_color)
            if fills:
                style_info["background_colors"] = fills

        # Border radius
        if "cornerRadius" in node:
            style_info["border_radius"] = node["cornerRadius"]

        # Opacity
        if "opacity" in node:
            style_info["opacity"] = node["opacity"]

        return style_info

    def _analyze_layout_properties(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze layout properties of a node."""
        layout_info = {}

        # Auto layout information
        if "layoutMode" in node:
            layout_info["type"] = "auto-layout"
            layout_info["direction"] = node.get("layoutMode", "NONE").lower()
            layout_info["alignment"] = node.get("layoutAlign", "STRETCH").lower()

            # Spacing
            if "itemSpacing" in node:
                spacing = node["itemSpacing"]
                layout_info["spacing"] = spacing
                if spacing > 0:
                    self.spacing_patterns.append(float(spacing))

            # Padding
            padding = {}
            if "paddingLeft" in node:
                padding["left"] = node["paddingLeft"]
            if "paddingRight" in node:
                padding["right"] = node["paddingRight"]
            if "paddingTop" in node:
                padding["top"] = node["paddingTop"]
            if "paddingBottom" in node:
                padding["bottom"] = node["paddingBottom"]

            if padding:
                layout_info["padding"] = padding

        else:
            # Manual layout analysis
            layout_info["type"] = "manual"
            if "children" in node and len(node["children"]) > 1:
                layout_info.update(self._analyze_manual_layout(node))

        return layout_info

    def _analyze_manual_layout(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze manual layout to infer layout patterns."""
        if "children" not in node or len(node["children"]) < 2:
            return {}

        children = node["children"]
        layout_info = {}

        # Get positions of children
        positions = []
        for child in children:
            if "absoluteBoundingBox" in child:
                bbox = child["absoluteBoundingBox"]
                positions.append({
                    "x": bbox.get("x", 0),
                    "y": bbox.get("y", 0),
                    "width": bbox.get("width", 0),
                    "height": bbox.get("height", 0)
                })

        if len(positions) < 2:
            return {}

        # Determine layout direction
        x_positions = [p["x"] for p in positions]
        y_positions = [p["y"] for p in positions]

        x_variance = max(x_positions) - min(x_positions)
        y_variance = max(y_positions) - min(y_positions)

        if x_variance > y_variance:
            layout_info["direction"] = "horizontal"
        else:
            layout_info["direction"] = "vertical"

        # Calculate spacing
        if layout_info["direction"] == "horizontal":
            # Sort by x position and calculate horizontal spacing
            sorted_positions = sorted(positions, key=lambda p: p["x"])
            spacings = []
            for i in range(len(sorted_positions) - 1):
                spacing = sorted_positions[i + 1]["x"] - (sorted_positions[i]["x"] + sorted_positions[i]["width"])
                if spacing > 0:
                    spacings.append(spacing)
                    self.spacing_patterns.append(float(spacing))

            if spacings:
                layout_info["spacing"] = sum(spacings) / len(spacings)
        else:
            # Sort by y position and calculate vertical spacing
            sorted_positions = sorted(positions, key=lambda p: p["y"])
            spacings = []
            for i in range(len(sorted_positions) - 1):
                spacing = sorted_positions[i + 1]["y"] - (sorted_positions[i]["y"] + sorted_positions[i]["height"])
                if spacing > 0:
                    spacings.append(spacing)
                    self.spacing_patterns.append(float(spacing))

            if spacings:
                layout_info["spacing"] = sum(spacings) / len(spacings)

        # Analyze alignment
        if layout_info["direction"] == "horizontal":
            y_positions = [p["y"] for p in positions]
            if len(set(y_positions)) == 1:
                layout_info["alignment"] = "center"
        else:
            x_positions = [p["x"] for p in positions]
            if len(set(x_positions)) == 1:
                layout_info["alignment"] = "center"

        return layout_info

    def _analyze_layout_patterns(self) -> None:
        """Analyze common layout patterns across all screens."""
        # Analyze spacing patterns
        if self.spacing_patterns:
            common_spacing = find_common_values(self.spacing_patterns, tolerance=2)
            self.layout_patterns["common_spacing"] = common_spacing

        # Analyze screen sizes
        screen_sizes = [(screen.size["width"], screen.size["height"]) for screen in self.screens]
        unique_sizes = list(set(screen_sizes))
        self.layout_patterns["screen_sizes"] = [
            {"width": w, "height": h} for w, h in unique_sizes
        ]

        # Analyze layout directions
        directions = []
        for screen in self.screens:
            if screen.layout and "direction" in screen.layout:
                directions.append(screen.layout["direction"])

        if directions:
            direction_counts = {}
            for direction in directions:
                direction_counts[direction] = direction_counts.get(direction, 0) + 1
            self.layout_patterns["layout_directions"] = direction_counts

    def _detect_grid_systems(self) -> None:
        """Detect grid systems used in the layouts."""
        for screen in self.screens:
            grid_info = self._analyze_screen_grid(screen)
            if grid_info:
                self.grid_systems.append(grid_info)

    def _analyze_screen_grid(self, screen: ScreenLayout) -> Optional[Dict[str, Any]]:
        """Analyze grid system for a single screen."""
        if not screen.children or len(screen.children) < 2:
            return None

        # Get all x and y positions
        x_positions = [child["position"]["x"] for child in screen.children]
        y_positions = [child["position"]["y"] for child in screen.children]

        # Look for regular grid patterns
        x_spacing = self._find_regular_spacing(x_positions)
        y_spacing = self._find_regular_spacing(y_positions)

        if x_spacing or y_spacing:
            return {
                "screen": screen.name,
                "x_spacing": x_spacing,
                "y_spacing": y_spacing,
                "columns": len(set([round(x / x_spacing) for x in x_positions])) if x_spacing else None,
                "rows": len(set([round(y / y_spacing) for y in y_positions])) if y_spacing else None
            }

        return None

    def _find_regular_spacing(self, positions: List[float], tolerance: float = 2.0) -> Optional[float]:
        """Find regular spacing in a list of positions."""
        if len(positions) < 3:
            return None

        # Calculate all spacing differences
        spacings = []
        sorted_positions = sorted(positions)
        for i in range(len(sorted_positions) - 1):
            spacing = sorted_positions[i + 1] - sorted_positions[i]
            if spacing > tolerance:  # Ignore very small differences
                spacings.append(spacing)

        if len(spacings) < 2:
            return None

        # Find most common spacing
        spacing_counts = {}
        for spacing in spacings:
            # Group similar spacings
            found = False
            for key_spacing in spacing_counts:
                if abs(spacing - key_spacing) < tolerance:
                    spacing_counts[key_spacing] += 1
                    found = True
                    break
            if not found:
                spacing_counts[spacing] = 1

        if spacing_counts:
            # Return the spacing with the highest count
            best_spacing = max(spacing_counts, key=spacing_counts.get)
            if spacing_counts[best_spacing] >= 2:  # Must appear at least twice
                return best_spacing

        return None

    def _build_layout_output(self) -> Dict[str, Any]:
        """Build the final layout output structure."""
        screens_data = []

        for screen in self.screens:
            screen_dict = {
                "name": screen.name,
                "type": screen.type,
                "size": screen.size,
                "children": screen.children,
                "layout": screen.layout,
                "description": screen.description
            }

            if screen.background_color:
                screen_dict["background_color"] = screen.background_color

            screens_data.append(screen_dict)

        output = {
            "screens": screens_data
        }

        # Add layout patterns if any were found
        if self.layout_patterns:
            output["layout_patterns"] = dict(self.layout_patterns)

        # Add grid systems if any were found
        if self.grid_systems:
            output["grid_systems"] = self.grid_systems

        return output

    def get_layout_summary(self) -> Dict[str, Any]:
        """Get summary statistics of layout analysis."""
        if not self.screens:
            return {"screens": 0}

        # Screen size analysis
        widths = [screen.size["width"] for screen in self.screens]
        heights = [screen.size["height"] for screen in self.screens]

        # Layout type analysis
        layout_types = {}
        for screen in self.screens:
            if screen.layout:
                layout_type = screen.layout.get("type", "unknown")
                layout_types[layout_type] = layout_types.get(layout_type, 0) + 1

        # Children count analysis
        children_counts = [len(screen.children) for screen in self.screens]

        return {
            "total_screens": len(self.screens),
            "screen_sizes": {
                "width_range": [min(widths), max(widths)] if widths else [0, 0],
                "height_range": [min(heights), max(heights)] if heights else [0, 0],
                "unique_sizes": len(set((w, h) for w, h in zip(widths, heights)))
            },
            "layout_types": layout_types,
            "children_counts": {
                "total": sum(children_counts),
                "average": sum(children_counts) / len(children_counts) if children_counts else 0,
                "max": max(children_counts) if children_counts else 0
            },
            "spacing_patterns_found": len(self.spacing_patterns),
            "grid_systems_detected": len(self.grid_systems)
        }