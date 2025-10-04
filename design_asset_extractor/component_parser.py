"""
Component Parser - Identify and parse components from Figma designs.

Detects repeating patterns, categorizes components, and extracts
component properties with variants and states.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Dict, Any, List, Set, Optional, Tuple
from collections import defaultdict, Counter
import hashlib
import figma_sdk
from .schemas import ComponentSpec, ComponentVariant
from .utils import (
    clean_component_name, extract_text_properties, rgb_to_hex,
    rgba_to_hex, find_common_values
)


class ComponentParser:
    """Parse and categorize components from Figma document."""

    def __init__(self, figma_file: 'figma_sdk.files.FigmaFile'):
        """Initialize with FigmaFile instance."""
        self.figma_file = figma_file
        self.document = figma_file.document

        # Storage for components
        self.components: Dict[str, ComponentSpec] = {}
        self.component_patterns: Dict[str, List[Dict[str, Any]]] = defaultdict(list)

        # Component identification patterns
        self.interactive_patterns = {
            "button", "btn", "submit", "cancel", "close", "add", "delete",
            "edit", "save", "search", "filter", "menu", "toggle", "switch"
        }
        self.input_patterns = {
            "input", "field", "textfield", "textarea", "searchbox",
            "email", "password", "name", "username"
        }
        self.display_patterns = {
            "card", "badge", "avatar", "icon", "image", "photo",
            "banner", "header", "footer", "sidebar", "navbar"
        }

    def parse_all_components(self) -> Dict[str, Any]:
        """Parse all components from the document."""
        print("🧩 Parsing components...")

        # First pass: identify potential components
        self._identify_components(self.document)

        # Second pass: analyze component patterns and variants
        self._analyze_component_patterns()

        # Third pass: create component specifications
        self._create_component_specs()

        return self._build_component_output()

    def _identify_components(self, node: Dict[str, Any], parent_path: str = "") -> None:
        """Identify potential components in the document tree."""
        if not isinstance(node, dict):
            return

        node_type = node.get("type", "").upper()
        node_name = node.get("name", "").lower()
        current_path = f"{parent_path}/{node_name}" if parent_path else node_name

        # Check if this node could be a component
        if self._is_component_node(node):
            component_id = self._generate_component_id(node)
            self.component_patterns[component_id].append({
                "node": node,
                "path": current_path,
                "id": component_id
            })

        # Traverse children
        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                self._identify_components(child, current_path)

    def _is_component_node(self, node: Dict[str, Any]) -> bool:
        """Determine if a node represents a component."""
        node_type = node.get("type", "").upper()
        node_name = node.get("name", "").lower()

        # Exclude certain node types
        if node_type in ["DOCUMENT", "PAGE"]:
            return False

        # Check for explicit component markers
        if node_type in ["COMPONENT", "INSTANCE"]:
            return True

        # Check naming patterns
        if any(pattern in node_name for pattern in self.interactive_patterns):
            return True

        if any(pattern in node_name for pattern in self.input_patterns):
            return True

        if any(pattern in node_name for pattern in self.display_patterns):
            return True

        # Check for visual patterns that suggest components
        if node_type == "RECTANGLE" and self._has_component_properties(node):
            return True

        if node_type == "GROUP" and self._has_component_structure(node):
            return True

        return False

    def _has_component_properties(self, node: Dict[str, Any]) -> bool:
        """Check if node has properties typical of components."""
        # Has corner radius (not just a simple rectangle)
        if node.get("cornerRadius", 0) > 0:
            return True

        # Has fills or strokes
        if node.get("fills") or node.get("strokes"):
            return True

        # Has reasonable dimensions
        if "absoluteBoundingBox" in node:
            bbox = node["absoluteBoundingBox"]
            width = bbox.get("width", 0)
            height = bbox.get("height", 0)
            # Reasonable component sizes (between 20px and 500px)
            if 20 <= width <= 500 and 20 <= height <= 500:
                return True

        return False

    def _has_component_structure(self, node: Dict[str, Any]) -> bool:
        """Check if group has structure typical of components."""
        if "children" not in node or not node["children"]:
            return False

        # Group with multiple children that work together
        children = node["children"]
        if len(children) >= 2:
            # Check for common component patterns
            has_background = any(
                child.get("type", "").upper() == "RECTANGLE"
                for child in children
            )
            has_text = any(
                child.get("type", "").upper() == "TEXT"
                for child in children
            )
            has_icon = any(
                "icon" in child.get("name", "").lower()
                for child in children
            )

            # If it has background + text/icon, it's likely a component
            if has_background and (has_text or has_icon):
                return True

        return False

    def _generate_component_id(self, node: Dict[str, Any]) -> str:
        """Generate a unique ID for component based on its properties."""
        # Use key visual properties to identify similar components
        props = []

        # Node type
        props.append(node.get("type", ""))

        # Node name (cleaned)
        clean_name = clean_component_name(node.get("name", ""))
        props.append(clean_name)

        # Bounding box dimensions
        if "absoluteBoundingBox" in node:
            bbox = node["absoluteBoundingBox"]
            props.append(f"{bbox.get('width', 0)}x{bbox.get('height', 0)}")

        # Visual properties
        if "fills" in node:
            fill_types = [f.get("type", "") for f in node["fills"]]
            props.append(",".join(fill_types))

        if "cornerRadius" in node:
            props.append(f"r{node['cornerRadius']}")

        # Create hash from properties
        prop_string = "|".join(props)
        return hashlib.md5(prop_string.encode()).hexdigest()[:8]

    def _analyze_component_patterns(self) -> None:
        """Analyze component patterns to identify variants and families."""
        for component_id, instances in self.component_patterns.items():
            if len(instances) > 1:
                # Multiple instances - analyze for variants
                self._analyze_component_variants(component_id, instances)

    def _analyze_component_variants(self, component_id: str, instances: List[Dict[str, Any]]) -> None:
        """Analyze variants of the same component."""
        if len(instances) < 2:
            return

        # Extract properties that vary between instances
        varying_properties = self._find_varying_properties(instances)

        # Group instances by variant properties
        variant_groups = self._group_by_variants(instances, varying_properties)

        # Store variant information
        for variant_name, variant_instances in variant_groups.items():
            if len(variant_instances) > 0:
                # Use the first instance as the variant example
                example = variant_instances[0]["node"]
                example["variant_info"] = {
                    "name": variant_name,
                    "count": len(variant_instances),
                    "properties": varying_properties
                }

    def _find_varying_properties(self, instances: List[Dict[str, Any]]) -> List[str]:
        """Find properties that vary between component instances."""
        if len(instances) < 2:
            return []

        varying_props = []
        first_instance = instances[0]["node"]

        # Check common properties for variation
        properties_to_check = [
            "name", "fills", "strokes", "cornerRadius", "opacity"
        ]

        for prop in properties_to_check:
            values = []
            for instance in instances:
                value = instance["node"].get(prop)
                if isinstance(value, list):
                    # For lists (like fills), convert to string for comparison
                    value = str([f.get("type", "") for f in value])
                values.append(value)

            # Check if this property varies
            if len(set(values)) > 1:
                varying_props.append(prop)

        return varying_props

    def _group_by_variants(self, instances: List[Dict[str, Any]], varying_properties: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Group instances by their variant properties."""
        variant_groups = defaultdict(list)

        for instance in instances:
            node = instance["node"]
            variant_key = self._create_variant_key(node, varying_properties)

            # Create a semantic variant name
            variant_name = self._create_variant_name(node, varying_properties)
            variant_groups[variant_name].append(instance)

        return dict(variant_groups)

    def _create_variant_key(self, node: Dict[str, Any], varying_properties: List[str]) -> str:
        """Create a key for grouping variants."""
        key_parts = []
        for prop in varying_properties:
            value = node.get(prop)
            if isinstance(value, list):
                value = str([f.get("type", "") for f in value])
            key_parts.append(f"{prop}:{value}")
        return "|".join(key_parts)

    def _create_variant_name(self, node: Dict[str, Any], varying_properties: List[str]) -> str:
        """Create a semantic name for a variant."""
        node_name = node.get("name", "").lower()

        # Try to extract variant information from the name
        if "primary" in node_name or "main" in node_name:
            return "primary"
        elif "secondary" in node_name or "alt" in node_name:
            return "secondary"
        elif "outline" in node_name or "ghost" in node_name:
            return "outline"
        elif "small" in node_name or "sm" in node_name:
            return "small"
        elif "large" in node_name or "lg" in node_name:
            return "large"
        elif "hover" in node_name:
            return "hover"
        elif "active" in node_name or "pressed" in node_name:
            return "active"
        elif "disabled" in node_name:
            return "disabled"
        else:
            return "default"

    def _create_component_specs(self) -> None:
        """Create component specifications from identified patterns."""
        for component_id, instances in self.component_patterns.items():
            if not instances:
                continue

            # Use the first instance as the base
            base_instance = instances[0]
            base_node = base_instance["node"]

            # Determine component type
            component_type = self._determine_component_type(base_node)
            component_name = self._generate_component_name(base_node, component_id)

            # Extract component properties
            props = self._extract_component_properties(base_node)

            # Extract children
            children = self._extract_component_children(base_node)

            # Find variants
            variants = self._extract_component_variants(instances)

            # Create component specification
            component_spec = ComponentSpec(
                name=component_name,
                type=component_type,
                props=props,
                variants=variants,
                children=children,
                description=self._generate_component_description(component_name, component_type)
            )

            self.components[component_name] = component_spec

    def _determine_component_type(self, node: Dict[str, Any]) -> str:
        """Determine the type of component."""
        node_name = node.get("name", "").lower()
        node_type = node.get("type", "").upper()

        # Check for interactive components
        if any(pattern in node_name for pattern in self.interactive_patterns):
            return "interactive"

        # Check for input components
        if any(pattern in node_name for pattern in self.input_patterns):
            return "interactive"  # Inputs are also interactive

        # Check for display components
        if any(pattern in node_name for pattern in self.display_patterns):
            return "display"

        # Check for text components
        if node_type == "TEXT":
            return "text"

        # Check for layout components
        if node_type in ["FRAME", "GROUP"] and "children" in node:
            # If it has many children, it's likely a layout component
            if len(node["children"]) > 2:
                return "layout"

        # Default to display
        return "display"

    def _generate_component_name(self, node: Dict[str, Any], component_id: str) -> str:
        """Generate a clean component name."""
        node_name = node.get("name", "")

        # Clean the name
        clean_name = clean_component_name(node_name)

        # If cleaning removed everything, generate a name based on type
        if not clean_name or clean_name == "rect" or clean_name == "frame":
            component_type = self._determine_component_type(node)
            return f"{component_type}-{component_id}"

        return clean_name

    def _extract_component_properties(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Extract component properties."""
        props = {}

        # Basic properties
        props["type"] = node.get("type", "").lower()
        props["name"] = node.get("name", "")

        # Bounding box
        if "absoluteBoundingBox" in node:
            bbox = node["absoluteBoundingBox"]
            props["width"] = bbox.get("width", 0)
            props["height"] = bbox.get("height", 0)
            props["x"] = bbox.get("x", 0)
            props["y"] = bbox.get("y", 0)

        # Visual properties
        if "fills" in node and node["fills"]:
            fills = []
            for fill in node["fills"]:
                if fill.get("type") == "SOLID" and "color" in fill:
                    color = fill["color"]
                    hex_color = rgb_to_hex(color["r"], color["g"], color["b"])
                    fills.append({
                        "type": "solid",
                        "color": hex_color,
                        "opacity": fill.get("opacity", 1.0)
                    })
            props["fills"] = fills

        if "strokes" in node and node["strokes"]:
            strokes = []
            for stroke in node["strokes"]:
                if stroke.get("type") == "SOLID" and "color" in stroke:
                    color = stroke["color"]
                    hex_color = rgb_to_hex(color["r"], color["g"], color["b"])
                    strokes.append({
                        "type": "solid",
                        "color": hex_color,
                        "weight": stroke.get("weight", 1)
                    })
            props["strokes"] = strokes

        if "cornerRadius" in node:
            props["cornerRadius"] = node["cornerRadius"]

        if "opacity" in node:
            props["opacity"] = node["opacity"]

        # Text properties for text nodes
        if node.get("type", "").upper() == "TEXT" and "style" in node:
            props.update(extract_text_properties(node["style"]))
            if "characters" in node:
                props["text"] = node["characters"]

        return props

    def _extract_component_children(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract component children information."""
        children = []

        if "children" in node and isinstance(node["children"], list):
            for child in node["children"]:
                child_info = {
                    "name": child.get("name", ""),
                    "type": child.get("type", "").lower(),
                    "visible": child.get("visible", True)
                }

                # Add basic properties
                if "absoluteBoundingBox" in child:
                    bbox = child["absoluteBoundingBox"]
                    child_info["width"] = bbox.get("width", 0)
                    child_info["height"] = bbox.get("height", 0)

                # Add text content for text nodes
                if child.get("type", "").upper() == "TEXT" and "characters" in child:
                    child_info["text"] = child["characters"]

                children.append(child_info)

        return children

    def _extract_component_variants(self, instances: List[Dict[str, Any]]) -> List[ComponentVariant]:
        """Extract component variants from instances."""
        variants = []

        # Group instances by variant
        variant_groups = defaultdict(list)
        for instance in instances:
            node = instance["node"]
            variant_name = self._create_variant_name(node, [])
            variant_groups[variant_name].append(instance)

        # Create variant specifications
        for variant_name, variant_instances in variant_groups.items():
            if variant_instances:
                example_instance = variant_instances[0]
                props = self._extract_component_properties(example_instance["node"])

                variant = ComponentVariant(
                    name=variant_name,
                    props=props,
                    example_usage=f"<{self._generate_component_name(example_instance['node'], '')} variant='{variant_name}' />"
                )
                variants.append(variant)

        return variants

    def _generate_component_description(self, name: str, component_type: str) -> str:
        """Generate component description."""
        type_descriptions = {
            "interactive": "Interactive UI component with user interactions",
            "display": "Visual component for displaying content",
            "layout": "Layout component for organizing content",
            "text": "Typography component for text display"
        }

        base_desc = type_descriptions.get(component_type, "UI component")
        return f"{name} - {base_desc}"

    def _build_component_output(self) -> Dict[str, Any]:
        """Build the final component output structure."""
        component_list = []

        for component_name, component_spec in self.components.items():
            component_dict = {
                "name": component_spec.name,
                "type": component_spec.type,
                "category": self._get_component_category(component_spec),
                "props": component_spec.props,
                "variants": [
                    {
                        "name": variant.name,
                        "props": variant.props,
                        "example_usage": variant.example_usage
                    }
                    for variant in component_spec.variants
                ],
                "children": component_spec.children,
                "description": component_spec.description
            }
            component_list.append(component_dict)

        return {
            "components": component_list
        }

    def _get_component_category(self, component_spec: ComponentSpec) -> str:
        """Get category for component based on type and properties."""
        if component_spec.type == "interactive":
            if "input" in component_spec.name.lower() or "field" in component_spec.name.lower():
                return "forms"
            elif "button" in component_spec.name.lower() or "btn" in component_spec.name.lower():
                return "buttons"
            else:
                return "interactive"
        elif component_spec.type == "display":
            if "card" in component_spec.name.lower():
                return "cards"
            elif "badge" in component_spec.name.lower():
                return "badges"
            else:
                return "display"
        elif component_spec.type == "layout":
            return "layout"
        elif component_spec.type == "text":
            return "typography"
        else:
            return "general"

    def get_component_summary(self) -> Dict[str, int]:
        """Get summary statistics of parsed components."""
        category_counts = Counter()
        type_counts = Counter()

        for component_spec in self.components.values():
            category_counts[self._get_component_category(component_spec)] += 1
            type_counts[component_spec.type] += 1

        return {
            "total_components": len(self.components),
            "by_category": dict(category_counts),
            "by_type": dict(type_counts),
            "with_variants": sum(1 for spec in self.components.values() if len(spec.variants) > 1)
        }