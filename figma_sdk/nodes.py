"""
Node operations for the Figma SDK.

Handles individual node access and batch operations.
"""

from typing import Dict, Any, List, Optional
from .exceptions import FigmaValidationError


class NodeOperations:
    """Operations for Figma node management."""

    def __init__(self, client):
        """Initialize with FigmaClient instance."""
        self.client = client

    def get(
        self,
        file_key: str,
        node_ids: List[str],
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Get specific nodes from a file.

        Args:
            file_key: Figma file key
            node_ids: List of node IDs to retrieve
            use_cache: Whether to use cached data

        Returns:
            Dictionary mapping node IDs to node data
        """
        if not file_key:
            raise FigmaValidationError("File key is required")
        if not node_ids:
            raise FigmaValidationError("Node IDs are required")

        # Figma API limits to 100 nodes per request
        if len(node_ids) > 100:
            # Split into batches and combine results
            all_nodes = {}
            for i in range(0, len(node_ids), 100):
                batch_ids = node_ids[i:i+100]
                batch_result = self._get_batch(file_key, batch_ids, use_cache)
                all_nodes.update(batch_result.get("nodes", {}))
            return {"nodes": all_nodes}

        return self._get_batch(file_key, node_ids, use_cache)

    def _get_batch(
        self,
        file_key: str,
        node_ids: List[str],
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """Get a batch of nodes (up to 100)."""
        params = {"ids": ",".join(node_ids)}
        return self.client.get(f"/files/{file_key}/nodes", params=params, use_cache=use_cache)

    def find_by_name(
        self,
        file_key: str,
        node_name: str,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find nodes by name within a file.

        Args:
            file_key: Figma file key
            node_name: Name to search for (case-insensitive)
            use_cache: Whether to use cached data

        Returns:
            List of matching nodes
        """
        file_data = self.client.files.get(file_key, depth=2, use_cache=use_cache)
        matching_nodes = []

        def search_nodes(nodes):
            for node in nodes:
                if node.get("name", "").lower() == node_name.lower():
                    matching_nodes.append(node)

                # Recursively search children
                if "children" in node:
                    search_nodes(node["children"])

        document = file_data.get("document", {})
        if "children" in document:
            search_nodes(document["children"])

        return matching_nodes

    def find_by_type(
        self,
        file_key: str,
        node_type: str,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find nodes by type within a file.

        Args:
            file_key: Figma file key
            node_type: Node type to search for
            use_cache: Whether to use cached data

        Returns:
            List of matching nodes
        """
        file_data = self.client.files.get(file_key, depth=2, use_cache=use_cache)
        matching_nodes = []

        def search_nodes(nodes):
            for node in nodes:
                if node.get("type") == node_type:
                    matching_nodes.append(node)

                # Recursively search children
                if "children" in node:
                    search_nodes(node["children"])

        document = file_data.get("document", {})
        if "children" in document:
            search_nodes(document["children"])

        return matching_nodes

    def get_component_instances(
        self,
        file_key: str,
        component_id: str,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find all instances of a specific component.

        Args:
            file_key: Figma file key
            component_id: Component ID to find instances of
            use_cache: Whether to use cached data

        Returns:
            List of component instances
        """
        file_data = self.client.files.get(file_key, depth=2, use_cache=use_cache)
        instances = []

        def search_nodes(nodes):
            for node in nodes:
                if (
                    node.get("type") == "INSTANCE"
                    and node.get("componentId") == component_id
                ):
                    instances.append(node)

                # Recursively search children
                if "children" in node:
                    search_nodes(node["children"])

        document = file_data.get("document", {})
        if "children" in document:
            search_nodes(document["children"])

        return instances