"""
Style operations for the Figma SDK.

Handles style retrieval and analysis for design tokens.
"""

from typing import Dict, Any, List, Optional
from .exceptions import FigmaValidationError


class StyleOperations:
    """Operations for Figma style management."""

    def __init__(self, client):
        """Initialize with FigmaClient instance."""
        self.client = client

    def get_file_styles(self, file_key: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Get all styles in a file.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            Dictionary of style data
        """
        if not file_key:
            raise FigmaValidationError("File key is required")

        return self.client.get(f"/files/{file_key}/styles", use_cache=use_cache)

    def get_styles_by_type(
        self,
        file_key: str,
        style_type: str,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get styles filtered by type.

        Args:
            file_key: Figma file key
            style_type: Style type ('FILL', 'TEXT', 'EFFECT', 'GRID')
            use_cache: Whether to use cached data

        Returns:
            List of styles of specified type
        """
        if not style_type:
            raise FigmaValidationError("Style type is required")

        valid_types = ["FILL", "TEXT", "EFFECT", "GRID"]
        if style_type.upper() not in valid_types:
            raise FigmaValidationError(f"Style type must be one of: {valid_types}")

        styles_data = self.get_file_styles(file_key, use_cache)
        matching_styles = []

        for style_id, style in styles_data.get("styles", {}).items():
            if style.get("style_type") == style_type.upper():
                matching_styles.append({
                    "id": style_id,
                    "name": style.get("name"),
                    "description": style.get("description", ""),
                    "style_type": style.get("style_type"),
                    "thumbnail_url": style.get("thumbnail_url"),
                    "remote": style.get("remote", False)
                })

        return matching_styles

    def get_color_styles(self, file_key: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get all color (fill) styles.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            List of color styles
        """
        return self.get_styles_by_type(file_key, "FILL", use_cache)

    def get_text_styles(self, file_key: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get all text styles.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            List of text styles
        """
        return self.get_styles_by_type(file_key, "TEXT", use_cache)

    def get_effect_styles(self, file_key: str, use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        Get all effect styles.

        Args:
            file_key: Figma file key
            use_cache: Whether to use cached data

        Returns:
            List of effect styles
        """
        return self.get_styles_by_type(file_key, "EFFECT", use_cache)

    def find_styles_by_name(
        self,
        file_key: str,
        name_pattern: str,
        style_type: Optional[str] = None,
        use_cache: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Find styles by name pattern.

        Args:
            file_key: Figma file key
            name_pattern: Name pattern to match (supports wildcards)
            style_type: Optional filter by style type
            use_cache: Whether to use cached data

        Returns:
            List of matching styles
        """
        import fnmatch

        if style_type:
            styles = self.get_styles_by_type(file_key, style_type, use_cache)
        else:
            styles_data = self.get_file_styles(file_key, use_cache)
            styles = []
            for style_id, style in styles_data.get("styles", {}).items():
                styles.append({
                    "id": style_id,
                    "name": style.get("name"),
                    "description": style.get("description", ""),
                    "style_type": style.get("style_type"),
                    "thumbnail_url": style.get("thumbnail_url"),
                    "remote": style.get("remote", False)
                })

        matching_styles = []
        for style in styles:
            if fnmatch.fnmatch(style["name"].lower(), name_pattern.lower()):
                matching_styles.append(style)

        return matching_styles

    def analyze_style_usage(
        self,
        file_key: str,
        style_id: str,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze usage of a specific style.

        Args:
            file_key: Figma file key
            style_id: Style ID to analyze
            use_cache: Whether to use cached data

        Returns:
            Usage analysis information
        """
        # This would require additional API calls to determine style usage
        # For now, return basic style information
        styles_data = self.get_file_styles(file_key, use_cache)
        style = styles_data.get("styles", {}).get(style_id)

        if not style:
            return {"error": "Style not found"}

        return {
            "style_id": style_id,
            "name": style.get("name"),
            "description": style.get("description", ""),
            "style_type": style.get("style_type"),
            "remote": style.get("remote", False),
            "thumbnail_url": style.get("thumbnail_url")
        }