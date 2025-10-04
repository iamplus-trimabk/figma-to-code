"""
Token Extractor - Extract design tokens from Figma nodes.

Handles extraction of colors, typography, spacing, and effects
from Figma design data and organizes them into semantic design tokens.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List, Set, Optional
from collections import defaultdict, Counter
import figma_sdk
from .schemas import ColorToken, TypographyToken, SpacingToken
from .utils import (
    rgb_to_hex, rgba_to_hex, categorize_color, create_semantic_name,
    normalize_font_weight, detect_spacing_pattern, extract_text_properties,
    find_common_values
)


class TokenExtractor:
    """Extract design tokens from Figma document."""

    def __init__(self, figma_file: 'figma_sdk.files.FigmaFile'):
        """Initialize with FigmaFile instance."""
        self.figma_file = figma_file
        self.document = figma_file.document

        # Storage for extracted tokens
        self.colors: Dict[str, ColorToken] = {}
        self.typography: Dict[str, TypographyToken] = {}
        self.spacing: Dict[str, SpacingToken] = {}
        self.effects: Dict[str, Any] = defaultdict(list)

        # Tracking for analysis
        self.all_color_values: Set[str] = set()
        self.all_font_sizes: List[float] = []
        self.all_spacing_values: List[float] = []
        self.all_font_families: Set[str] = set()

    def extract_all_tokens(self) -> Dict[str, Any]:
        """Extract all design tokens from the document."""
        print("🎨 Extracting design tokens...")

        # Traverse document and extract tokens
        self._traverse_document(self.document)

        # Process and organize tokens
        self._process_colors()
        self._process_typography()
        self._process_spacing()
        self._process_effects()

        # Build final token structure
        return self._build_token_output()

    def _traverse_document(self, node: Dict[str, Any]) -> None:
        """Recursively traverse document and extract tokens."""
        if not isinstance(node, dict):
            return

        # Extract tokens from current node
        self._extract_node_tokens(node)

        # Traverse children
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                self._traverse_document(child)

    def _extract_node_tokens(self, node: Dict[str, Any]) -> None:
        """Extract tokens from a single node."""
        node_type = node.get("type", "").upper()

        # Extract colors from fills and strokes
        if "fills" in node and node["fills"]:
            self._extract_colors_from_fills(node["fills"])

        if "strokes" in node and node["strokes"]:
            self._extract_colors_from_strokes(node["strokes"])

        # Extract typography from text nodes
        if node_type == "TEXT" and "style" in node:
            self._extract_typography_from_text(node)

        # Extract spacing from layout nodes
        if node_type in ["FRAME", "GROUP", "COMPONENT", "INSTANCE"]:
            self._extract_spacing_from_layout(node)

        # Extract effects
        if "effects" in node and node["effects"]:
            self._extract_effects_from_node(node["effects"])

    def _extract_colors_from_fills(self, fills: List[Dict[str, Any]]) -> None:
        """Extract colors from fill properties."""
        for fill in fills:
            if fill.get("type") == "SOLID" and "color" in fill:
                color = fill["color"]
                hex_color = rgb_to_hex(color["r"], color["g"], color["b"])
                self.all_color_values.add(hex_color)

            elif fill.get("type") == "GRADIENT_LINEAR" and "gradientStops" in fill:
                for stop in fill["gradientStops"]:
                    if "color" in stop:
                        color = stop["color"]
                        hex_color = rgb_to_hex(color["r"], color["g"], color["b"])
                        self.all_color_values.add(hex_color)

    def _extract_colors_from_strokes(self, strokes: List[Dict[str, Any]]) -> None:
        """Extract colors from stroke properties."""
        for stroke in strokes:
            if stroke.get("type") == "SOLID" and "color" in stroke:
                color = stroke["color"]
                hex_color = rgb_to_hex(color["r"], color["g"], color["b"])
                self.all_color_values.add(hex_color)

    def _extract_typography_from_text(self, node: Dict[str, Any]) -> None:
        """Extract typography from text nodes."""
        style = node.get("style", {})
        text_properties = extract_text_properties(style)

        # Track font size
        if "font_size" in text_properties:
            self.all_font_sizes.append(text_properties["font_size"])

        # Track font family
        if "font_family" in text_properties:
            self.all_font_families.add(text_properties["font_family"])

        # Create typography token
        font_size = text_properties.get("font_size", 16)
        font_weight = text_properties.get("font_weight", 400)
        font_family = text_properties.get("font_family", "Inter")

        # Create semantic name
        if font_size >= 32:
            size_category = "heading"
        elif font_size >= 20:
            size_category = "subheading"
        elif font_size >= 16:
            size_category = "body"
        else:
            size_category = "caption"

        token_name = f"{size_category}-{int(font_size)}"
        if token_name not in self.typography:
            self.typography[token_name] = TypographyToken(
                name=token_name,
                font_family=font_family,
                font_size=font_size,
                font_weight=font_weight,
                line_height=text_properties.get("line_height", 1.4),
                letter_spacing=text_properties.get("letter_spacing"),
                description=f"{size_category.replace('-', ' ').title()} text style"
            )

    def _extract_spacing_from_layout(self, node: Dict[str, Any]) -> None:
        """Extract spacing patterns from layout nodes."""
        # Extract from absolute positioning
        if "absoluteBoundingBox" in node:
            bbox = node["absoluteBoundingBox"]
            # Track width and height as potential spacing values
            if "width" in bbox:
                self.all_spacing_values.append(bbox["width"])
            if "height" in bbox:
                self.all_spacing_values.append(bbox["height"])

        # Extract from layout constraints
        if "constraints" in node:
            constraints = node["constraints"]
            # This could be useful for understanding layout patterns

        # Extract from auto layout
        if "layoutMode" in node:
            # Auto layout nodes often have consistent spacing
            if "itemSpacing" in node:
                spacing = node["itemSpacing"]
                if spacing > 0:
                    self.all_spacing_values.append(float(spacing))

            if "paddingLeft" in node:
                self.all_spacing_values.append(float(node["paddingLeft"]))
            if "paddingRight" in node:
                self.all_spacing_values.append(float(node["paddingRight"]))
            if "paddingTop" in node:
                self.all_spacing_values.append(float(node["paddingTop"]))
            if "paddingBottom" in node:
                self.all_spacing_values.append(float(node["paddingBottom"]))

    def _extract_effects_from_node(self, effects: List[Dict[str, Any]]) -> None:
        """Extract effects (shadows, blurs) from nodes."""
        for effect in effects:
            effect_type = effect.get("type", "").upper()
            effect_radius = effect.get("radius", 0)
            effect_color = effect.get("color", {})

            if effect_type == "DROP_SHADOW":
                if effect_color and "r" in effect_color:
                    color_hex = rgb_to_hex(effect_color["r"], effect_color["g"], effect_color["b"])
                    shadow_value = f"0px {effect.get('offset', {}).get('x', 0)}px {effect.get('offset', {}).get('y', 0)}px {effect_radius}px {color_hex}"
                    self.effects["shadows"].append({
                        "name": f"shadow-{len(self.effects['shadows']) + 1}",
                        "value": shadow_value
                    })

            elif effect_type == "LAYER_BLUR":
                self.effects["blurs"].append({
                    "name": f"blur-{len(self.effects['blurs']) + 1}",
                    "value": effect_radius
                })

    def _process_colors(self) -> None:
        """Process and categorize extracted colors."""
        color_list = list(self.all_color_values)

        # Separate into semantic, neutral, and brand colors
        semantic_colors = {}
        neutral_colors = {}
        brand_colors = {}

        # Common semantic colors (you could make this configurable)
        semantic_map = {
            "#ff0000": "danger",
            "#dc3545": "danger",
            "#28a745": "success",
            "#28b446": "success",
            "#ffc107": "warning",
            "#fbbb00": "warning",
            "#007bff": "info",
            "#6257db": "primary",
            "#6c757d": "secondary",
            "#3b5999": "facebook"
        }

        for color in color_list:
            # Check if it's a predefined semantic color
            if color.lower() in semantic_map:
                semantic_colors[semantic_map[color.lower()]] = color
            else:
                # Categorize based on color properties
                category = categorize_color(color)
                if category in ["white", "black"] or "gray" in category:
                    neutral_colors[category] = color
                else:
                    brand_colors[f"brand-{len(brand_colors) + 1}"] = color

        # Store processed colors
        self.colors = {
            "semantic": semantic_colors,
            "neutral": neutral_colors,
            "brand": brand_colors
        }

    def _process_typography(self) -> None:
        """Process and organize typography tokens."""
        if not self.typography:
            return

        # Find most common font family
        if self.all_font_families:
            most_common_family = Counter(list(self.all_font_families)).most_common(1)[0][0]
        else:
            most_common_family = "Inter"

        # Group typography by font size and weight
        processed_typography = {
            "fontFamily": most_common_family,
            "fontSizes": {},
            "fontWeights": {},
            "lineHeights": {}
        }

        # Extract unique values
        font_sizes = set()
        font_weights = set()
        line_heights = set()

        for token in self.typography.values():
            font_sizes.add(int(token.font_size))
            font_weights.add(token.font_weight)
            line_heights.add(round(token.line_height, 2))

        # Create semantic names for font sizes
        sorted_sizes = sorted(list(font_sizes))
        if len(sorted_sizes) == 1:
            processed_typography["fontSizes"]["body"] = sorted_sizes[0]
        else:
            # Assign semantic names based on size
            for size in sorted_sizes:
                if size >= 40:
                    processed_typography["fontSizes"]["heading-1"] = size
                elif size >= 32:
                    processed_typography["fontSizes"]["heading-2"] = size
                elif size >= 24:
                    processed_typography["fontSizes"]["heading-3"] = size
                elif size >= 20:
                    processed_typography["fontSizes"]["subheading"] = size
                elif size >= 16:
                    processed_typography["fontSizes"]["body"] = size
                else:
                    processed_typography["fontSizes"]["caption"] = size

        # Process font weights
        weight_names = {400: "regular", 600: "medium", 700: "bold", 900: "black"}
        for weight in sorted(font_weights):
            name = weight_names.get(weight, str(weight))
            processed_typography["fontWeights"][name] = weight

        # Process line heights
        sorted_heights = sorted(list(line_heights))
        for height in sorted_heights:
            processed_typography["fontSizes"][f"leading-{int(height * 100)}"] = height

        self.typography = processed_typography

    def _process_spacing(self) -> None:
        """Process and organize spacing tokens."""
        if not self.all_spacing_values:
            self.spacing = {}
            return

        # Detect spacing patterns
        spacing_scale = detect_spacing_pattern(self.all_spacing_values)
        self.spacing = spacing_scale

    def _process_effects(self) -> None:
        """Process and organize effects."""
        # Effects are already organized during extraction
        pass

    def _build_token_output(self) -> Dict[str, Any]:
        """Build the final token output structure."""
        output = {
            "colors": self.colors,
            "typography": self.typography,
            "spacing": self.spacing
        }

        # Add effects if any were found
        if self.effects["shadows"] or self.effects["blurs"]:
            output["effects"] = dict(self.effects)

        return output

    def get_token_summary(self) -> Dict[str, int]:
        """Get summary statistics of extracted tokens."""
        return {
            "colors": len(self.all_color_values),
            "typography_tokens": len(self.typography) if isinstance(self.typography, dict) else 0,
            "spacing_values": len(self.all_spacing_values),
            "effects_shadows": len(self.effects["shadows"]),
            "effects_blurs": len(self.effects["blurs"])
        }