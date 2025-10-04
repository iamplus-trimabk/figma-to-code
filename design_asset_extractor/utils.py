"""
Utility functions for design asset extraction.

Helper functions for color conversion, naming, and data processing.
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from .schemas import ColorToken, TypographyToken, SpacingToken


def rgb_to_hex(r: float, g: float, b: float) -> str:
    """Convert RGB values (0-1) to hex color string."""
    return f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"


def rgba_to_hex(r: float, g: float, b: float, a: float) -> str:
    """Convert RGBA values (0-1) to hex color string with alpha."""
    hex_color = f"#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}"
    if a < 1.0:
        # For now, return solid color - could add alpha support later
        pass
    return hex_color


def categorize_color(hex_color: str) -> str:
    """Categorize color into semantic categories."""
    # Basic color categorization
    hex_color = hex_color.lower()

    # Pure colors
    if hex_color == "#ffffff":
        return "white"
    elif hex_color == "#000000":
        return "black"

    # Extract RGB values for analysis
    r = int(hex_color[1:3], 16)
    g = int(hex_color[3:5], 16)
    b = int(hex_color[5:7], 16)

    # Brightness calculation
    brightness = (r + g + b) / 3

    # Determine if it's a gray scale
    max_diff = max(abs(r - g), abs(g - b), abs(r - b))

    if max_diff < 30:  # Gray scale
        if brightness > 240:
            return "gray-50"
        elif brightness > 200:
            return "gray-100"
        elif brightness > 150:
            return "gray-200"
        elif brightness > 100:
            return "gray-300"
        elif brightness > 50:
            return "gray-600"
        else:
            return "gray-900"

    # Color categorization
    if r > g and r > b:
        if g > 150 and b < 100:
            return "yellow" if brightness > 150 else "orange"
        elif b > 100:
            return "purple"
        else:
            return "red"
    elif g > r and g > b:
        if r > 150:
            return "lime" if brightness > 150 else "green"
        else:
            return "green"
    elif b > r and b > g:
        if r > 150:
            return "pink"
        elif g > 150:
            return "cyan"
        else:
            return "blue"

    return "unknown"


def create_semantic_name(base_name: str, category: str, index: int = 0) -> str:
    """Create semantic names for design tokens."""
    if category == "semantic":
        return base_name
    elif category == "neutral":
        return f"{base_name}-{index}" if index > 0 else base_name
    else:
        return f"{category}-{base_name}"


def normalize_font_weight(weight: Any) -> int:
    """Normalize font weight to standard values."""
    if isinstance(weight, str):
        weight_map = {
            "thin": 100, "extralight": 200, "light": 300,
            "normal": 400, "regular": 400, "medium": 500,
            "semibold": 600, "demibold": 600, "bold": 700,
            "extrabold": 800, "black": 900, "heavy": 900
        }
        return weight_map.get(weight.lower(), 400)

    # Ensure it's within valid range
    weight = int(weight) if weight else 400
    return max(100, min(900, weight))


def detect_spacing_pattern(spacings: List[float]) -> Dict[str, float]:
    """Detect consistent spacing patterns from a list of spacing values."""
    if not spacings:
        return {}

    # Remove duplicates and sort
    unique_spacings = sorted(list(set(spacings)))

    # Find base unit (smallest non-zero spacing)
    base_unit = min([s for s in unique_spacings if s > 0], default=8)

    # Generate semantic spacing scale
    spacing_scale = {}

    # Common spacing patterns
    common_scales = [4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]

    for i, expected_value in enumerate(common_scales):
        # Find closest actual spacing value
        closest = min(unique_spacings, key=lambda x: abs(x - expected_value))

        # If it's reasonably close, use it
        if abs(closest - expected_value) < 4:  # Within 4px tolerance
            if i == 0:
                spacing_scale["xs"] = closest
            elif i == 1:
                spacing_scale["sm"] = closest
            elif i == 2:
                spacing_scale["md"] = closest
            elif i == 3:
                spacing_scale["lg"] = closest
            elif i == 4:
                spacing_scale["xl"] = closest
            elif i == 5:
                spacing_scale["2xl"] = closest
            elif i == 6:
                spacing_scale["3xl"] = closest
            elif i == 7:
                spacing_scale["4xl"] = closest
            elif i == 8:
                spacing_scale["5xl"] = closest
            elif i == 9:
                spacing_scale["6xl"] = closest
            elif i == 10:
                spacing_scale["7xl"] = closest
            elif i == 11:
                spacing_scale["8xl"] = closest

    return spacing_scale


def clean_component_name(name: str) -> str:
    """Clean and normalize component names."""
    # Remove common prefixes and suffixes
    prefixes_to_remove = ["rect", "ellipse", "frame", "group"]
    suffixes_to_remove = [" copy", " 1", " 2", " 3"]

    clean_name = name.lower().strip()

    # Remove prefixes
    for prefix in prefixes_to_remove:
        if clean_name.startswith(prefix):
            clean_name = clean_name[len(prefix):].strip()

    # Remove suffixes
    for suffix in suffixes_to_remove:
        if clean_name.endswith(suffix):
            clean_name = clean_name[:-len(suffix)].strip()

    # Convert to proper case
    if clean_name:
        return clean_name.replace(" ", "-").replace("_", "-")

    return name


def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def camel_to_snake(camel_str: str) -> str:
    """Convert camelCase to snake_case."""
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def extract_text_properties(style: Dict[str, Any]) -> Dict[str, Any]:
    """Extract and normalize text properties from Figma style."""
    properties = {}

    # Font family
    if "fontFamily" in style:
        properties["font_family"] = style["fontFamily"]

    # Font size
    if "fontSize" in style:
        properties["font_size"] = float(style["fontSize"])

    # Font weight
    if "fontWeight" in style:
        properties["font_weight"] = normalize_font_weight(style["fontWeight"])

    # Line height
    if "lineHeight" in style:
        lh = style["lineHeight"]
        if isinstance(lh, dict) and "value" in lh:
            properties["line_height"] = float(lh["value"])
        else:
            properties["line_height"] = float(lh) if lh else 1.4

    # Letter spacing
    if "letterSpacing" in style:
        ls = style["letterSpacing"]
        if isinstance(ls, dict) and "value" in ls:
            properties["letter_spacing"] = float(ls["value"])
        else:
            properties["letter_spacing"] = float(ls) if ls else 0

    # Text alignment
    if "textAlignHorizontal" in style:
        properties["text_align"] = style["textAlignHorizontal"].lower()

    # Text case
    if "textCase" in style and style["textCase"] != "ORIGINAL":
        properties["text_transform"] = style["textCase"].lower()

    return properties


def calculate_distance(pos1: Dict[str, float], pos2: Dict[str, float]) -> float:
    """Calculate distance between two positions."""
    if "x" in pos1 and "x" in pos2 and "y" in pos1 and "y" in pos2:
        dx = pos2["x"] - pos1["x"]
        dy = pos2["y"] - pos1["y"]
        return abs(dx) if abs(dx) > abs(dy) else abs(dy)
    return 0


def find_common_values(values: List[Any], tolerance: float = 0.1) -> List[Any]:
    """Find common values within a tolerance range."""
    if not values:
        return []

    # Group values by similarity
    groups = []
    for value in values:
        if isinstance(value, (int, float)):
            added = False
            for group in groups:
                if abs(group[0] - value) <= tolerance * max(abs(group[0]), abs(value)):
                    group.append(value)
                    added = True
                    break
            if not added:
                groups.append([value])
        else:
            # For non-numeric values, just group identical ones
            found = False
            for group in groups:
                if group[0] == value:
                    group.append(value)
                    found = True
                    break
            if not found:
                groups.append([value])

    # Return the most common value from each group
    common_values = []
    for group in groups:
        if len(group) > 1:  # Only return values that appear multiple times
            if isinstance(group[0], (int, float)):
                # Use average for numeric values
                avg_value = sum(group) / len(group)
                common_values.append(round(avg_value, 2))
            else:
                common_values.append(group[0])

    return common_values