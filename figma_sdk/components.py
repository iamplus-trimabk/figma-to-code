"""
Component operations for the Figma SDK.

Handles component retrieval, analysis, and management.
"""

from typing import Dict, Any, List, Optional
from .exceptions import FigmaValidationError


class ComponentOperations:
    """Operations for Figma component management."""

    def __init__(self, client):
        """Initialize with FigmaClient instance."""
        self.client = client

    def get_file_components(self, file_key: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get all components in a file.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            Dictionary of component data
        """
        if not file_key:
            raise FigmaValidationError("File key is required")

        return self.client.get(f"/files/{file_key}/components", use_cache=use_cache)

    def get_component_set(self, component_set_id: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get component set details.

        Args:
            component_set_id: Component set ID
            use_cache: Whether to use cached data

        Returns:
            Component set information
        """
        if not component_set_id:
            raise FigmaValidationError("Component set ID is required")

        return self.client.get(f"/component_sets/{component_set_id}", use_cache=use_cache)

    def get_component(
        self,
        file_key: str,
        node_id: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get specific component data.

        Args:
            file_key: Figma file key
            node_id: Component node ID
            use_cache: Whether to use cached data

        Returns:
            Component data
        """
        nodes_result = self.client.nodes.get([node_id], use_cache=use_cache)
        return nodes_result.get("nodes", {}).get(node_id)

    def find_components_by_name(
        self,
        file_key: str,
        name_pattern: str,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find components by name pattern.

        Args:
            file_key: Figma file key
            name_pattern: Name pattern to match (supports wildcards)
            use_cache: Whether to use cached data

        Returns:
            List of matching components
        """
        components_data = self.get_file_components(file_key, use_cache)
        matching_components = []

        import fnmatch

        for component_id, component in components_data.get("components", {}).items():
            component_name = component.get("name", "")
            if fnmatch.fnmatch(component_name.lower(), name_pattern.lower()):
                matching_components.append({
                    "id": component_id,
                    "name": component_name,
                    "description": component.get("description", ""),
                    "node_id": component.get("node_id")
                })

        return matching_components

    def get_component_variants(
        self,
        file_key: str,
        component_set_id: str,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get all variants in a component set.

        Args:
            file_key: Figma file key
            component_set_id: Component set ID
            use_cache: Whether to use cached data

        Returns:
            List of component variants
        """
        component_set = self.get_component_set(component_set_id, use_cache)
        variants = []

        for component in component_set.get("components", []):
            variant_info = {
                "id": component.get("node_id"),
                "name": component.get("name"),
                "description": component.get("description", ""),
                "component_set_id": component_set_id
            }

            # Try to get more detailed node information
            try:
                node_data = self.get_component(file_key, component.get("node_id"), use_cache)
                if node_data:
                    variant_info.update({
                        "width": node_data.get("absoluteBoundingBox", {}).get("width"),
                        "height": node_data.get("absoluteBoundingBox", {}).get("height"),
                        "type": node_data.get("type")
                    })
            except Exception:
                pass

            variants.append(variant_info)

        return variants

    def analyze_component_usage(
        self,
        file_key: str,
        component_id: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze usage of a specific component.

        Args:
            file_key: Figma file key
            component_id: Component ID to analyze
            use_cache: Whether to use cached data

        Returns:
            Usage analysis information
        """
        instances = self.client.nodes.get_component_instances(file_key, component_id, use_cache)

        return {
            "component_id": component_id,
            "instance_count": len(instances),
            "instances": instances,
            "pages": list(set(instance.get("pageId") for instance in instances if "pageId" in instance))
        }