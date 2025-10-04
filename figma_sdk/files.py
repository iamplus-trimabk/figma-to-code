"""
File operations for the Figma SDK.

Handles file retrieval, metadata, and file-level operations.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from .types import FigmaFile, DocumentNode
from .exceptions import FigmaValidationError


class FileOperations:
    """Operations for Figma file management."""

    def __init__(self, client):
        """Initialize with FigmaClient instance."""
        self.client = client

    def get(
        self,
        file_key: str,
        depth: Optional[int] = None,
        geometry: Optional[str] = None,
        ids: Optional[list] = None,
        version: Optional[int] = None,
        use_cache: bool = True
    ) -> FigmaFile:
        """
        Get file data from Figma API.

        Args:
            file_key: Figma file key
            depth: Node traversal depth (0-2)
            geometry: Include vector data ('paths')
            ids: Specific node IDs to include
            version: Specific file version
            use_cache: Whether to use cached data

        Returns:
            Figma file data
        """
        if not file_key:
            raise FigmaValidationError("File key is required")

        params = {}
        if depth is not None:
            params["depth"] = depth
        if geometry is not None:
            params["geometry"] = geometry
        if ids is not None:
            params["ids"] = ",".join(ids)
        if version is not None:
            params["version"] = version

        return self.client.get(f"/files/{file_key}", params=params, use_cache=use_cache)

    def get_metadata(self, file_key: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get file metadata only (lightweight request).

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            File metadata including name, last modified, thumbnail URL
        """
        file_data = self.get(file_key, depth=0, use_cache=use_cache)

        return {
            "name": file_data.get("name"),
            "lastModified": file_data.get("lastModified"),
            "thumbnailUrl": file_data.get("thumbnailUrl"),
            "version": file_data.get("version"),
            "editorType": file_data.get("editorType")
        }

    def get_pages(self, file_key: str, use_cache: bool = True) -> list:
        """
        Get all pages in a file.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            List of page information
        """
        file_data = self.get(file_key, depth=1, use_cache=use_cache)
        document = file_data.get("document", {})

        return [
            {
                "id": page.get("id"),
                "name": page.get("name"),
                "type": page.get("type"),
                "children_count": len(page.get("children", []))
            }
            for page in document.get("children", [])
            if page.get("type") == "CANVAS"
        ]

    def get_components(self, file_key: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get all components in a file.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            Component information
        """
        return self.client.get(f"/files/{file_key}/components", use_cache=use_cache)

    def get_styles(self, file_key: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get all styles in a file.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            Style information
        """
        return self.client.get(f"/files/{file_key}/styles", use_cache=use_cache)

    def get_comments(self, file_key: str, use_cache: bool = False) -> list:
        """
        Get comments for a file.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data (disabled by default for freshness)

        Returns:
            List of comments
        """
        result = self.client.get(f"/files/{file_key}/comments", use_cache=use_cache)
        return result.get("comments", [])


class FigmaFile:
    """High-level abstraction for Figma files with caching and convenience methods."""

    def __init__(
        self,
        file_key: str,
        project_name: str,
        client=None,
        data: Optional[FigmaFile] = None,
        use_cache: bool = True
    ):
        """
        Initialize FigmaFile.

        Args:
            file_key: Figma file key
            project_name: Project name for caching
            client: FigmaClient instance (optional)
            data: Pre-loaded file data (optional)
            use_cache: Whether to use caching
        """
        self.file_key = file_key
        self.project_name = project_name
        self.client = client
        self._data = data
        self.use_cache = use_cache

        if self.client is None and self._data is None:
            raise ValueError("Either client or data must be provided")

    @property
    def data(self) -> FigmaFile:
        """Get file data, loading if necessary."""
        if self._data is None:
            self._data = self.client.files.get(
                self.file_key,
                use_cache=self.use_cache
            )
        return self._data

    @property
    def name(self) -> str:
        """Get file name."""
        return self.data.get("name", "Untitled")

    @property
    def version(self) -> int:
        """Get file version."""
        return self.data.get("version", 0)

    @property
    def last_modified(self) -> str:
        """Get last modified timestamp."""
        return self.data.get("lastModified", "")

    @property
    def thumbnail_url(self) -> str:
        """Get thumbnail URL."""
        return self.data.get("thumbnailUrl", "")

    @property
    def document(self) -> DocumentNode:
        """Get document root node."""
        return self.data.get("document", {})

    @property
    def components_count(self) -> int:
        """Get count of components."""
        return len(self.data.get("components", {}))

    @property
    def styles_count(self) -> int:
        """Get count of styles."""
        return len(self.data.get("styles", {}))

    def get_pages(self) -> List[Dict[str, Any]]:
        """Get all pages in the file."""
        return self.client.files.get_pages(self.file_key, use_cache=self.use_cache)

    def get_components(self) -> Dict[str, Any]:
        """Get all components in the file."""
        if self.client:
            return self.client.files.get_components(self.file_key, use_cache=self.use_cache)

        # Fallback to extracting from cached data
        return self.data.get("components", {})

    def get_styles(self) -> Dict[str, Any]:
        """Get all styles in the file."""
        if self.client:
            return self.client.files.get_styles(self.file_key, use_cache=self.use_cache)

        # Fallback to extracting from cached data
        return self.data.get("styles", {})

    def _search_nodes_in_document(self, node_type: Optional[str] = None, node_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search nodes in the cached document by type and/or name."""
        matching_nodes = []

        def search_nodes(nodes):
            for node in nodes:
                # Check type match
                type_match = node_type is None or node.get("type") == node_type

                # Check name match (case-insensitive)
                name_match = node_name is None or node.get("name", "").lower() == node_name.lower()

                if type_match and name_match:
                    matching_nodes.append(node)

                # Recursively search children
                if "children" in node:
                    search_nodes(node["children"])

        document = self.document
        if "children" in document:
            search_nodes(document["children"])

        return matching_nodes

    def find_node_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Find nodes by name."""
        if self.client:
            return self.client.nodes.find_by_name(
                self.file_key,
                name,
                use_cache=self.use_cache
            )

        # Fallback to searching in cached data
        return self._search_nodes_in_document(node_name=name)

    def find_node_by_type(self, node_type: str) -> List[Dict[str, Any]]:
        """Find nodes by type."""
        if self.client:
            return self.client.nodes.find_by_type(
                self.file_key,
                node_type,
                use_cache=self.use_cache
            )

        # Fallback to searching in cached data
        return self._search_nodes_in_document(node_type=node_type)

    def get_color_styles(self) -> List[Dict[str, Any]]:
        """Get all color styles."""
        if self.client:
            return self.client.styles.get_color_styles(self.file_key, use_cache=self.use_cache)

        # Fallback to extracting from cached data
        styles = self.data.get("styles", {})
        color_styles = []
        for style_id, style in styles.items():
            if style.get("style_type") == "FILL":
                color_styles.append({
                    "id": style_id,
                    "name": style.get("name"),
                    "description": style.get("description", ""),
                    "style_type": style.get("style_type"),
                    "thumbnail_url": style.get("thumbnail_url"),
                    "remote": style.get("remote", False)
                })
        return color_styles

    def get_text_styles(self) -> List[Dict[str, Any]]:
        """Get all text styles."""
        if self.client:
            return self.client.styles.get_text_styles(self.file_key, use_cache=self.use_cache)

        # Fallback to extracting from cached data
        styles = self.data.get("styles", {})
        text_styles = []
        for style_id, style in styles.items():
            if style.get("style_type") == "TEXT":
                text_styles.append({
                    "id": style_id,
                    "name": style.get("name"),
                    "description": style.get("description", ""),
                    "style_type": style.get("style_type"),
                    "thumbnail_url": style.get("thumbnail_url"),
                    "remote": style.get("remote", False)
                })
        return text_styles

    def export_to_cache(self, cache_dir: str = "figma_cache") -> Path:
        """Export file data to cache directory."""
        cache_path = Path(cache_dir) / self.project_name / f"figma_{self.file_key}.json"
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

        return cache_path

    @classmethod
    def from_cache(
        cls,
        file_key: str,
        project_name: str,
        cache_dir: str = "figma_cache"
    ) -> "FigmaFile":
        """Load FigmaFile from cache."""
        cache_path = Path(cache_dir) / project_name / f"figma_{file_key}.json"

        if not cache_path.exists():
            raise FileNotFoundError(f"Cached file not found: {cache_path}")

        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return cls(file_key, project_name, client=None, data=data)

    def refresh(self) -> None:
        """Refresh file data from API."""
        if self.client is None:
            raise RuntimeError("Cannot refresh: no client available")

        self._data = self.client.files.get(self.file_key, use_cache=False)

    def __str__(self) -> str:
        """String representation."""
        return f"FigmaFile(name='{self.name}', file_key='{self.file_key}')"

    def __repr__(self) -> str:
        """Detailed string representation."""
        return (
            f"FigmaFile(name='{self.name}', file_key='{self.file_key}', "
            f"version={self.version}, components={self.components_count}, "
            f"styles={self.styles_count})"
        )