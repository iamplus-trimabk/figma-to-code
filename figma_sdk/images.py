"""
Image export operations for the Figma SDK.

Handles image generation and export functionality.
"""

from typing import Dict, Any, List, Optional, Union
from .exceptions import FigmaValidationError


class ImageOperations:
    """Operations for Figma image export."""

    def __init__(self, client):
        """Initialize with FigmaClient instance."""
        self.client = client

    def get_urls(
        self,
        file_key: str,
        node_ids: List[str],
        format: str = "PNG",
        scale: Union[int, float] = 1,
        use_cache: bool = False  # Images typically shouldn't be cached
    ) -> Dict[str, str]:
        """
        Get image URLs for specified nodes.

        Args:
            file_key: Figma file key
            node_ids: List of node IDs to export
            format: Image format ('PNG', 'JPG', 'SVG', 'PDF')
            scale: Export scale factor
            use_cache: Whether to use cached data

        Returns:
            Dictionary mapping node IDs to image URLs
        """
        if not file_key:
            raise FigmaValidationError("File key is required")
        if not node_ids:
            raise FigmaValidationError("Node IDs are required")
        if not format:
            raise FigmaValidationError("Format is required")

        valid_formats = ["PNG", "JPG", "SVG", "PDF"]
        if format.upper() not in valid_formats:
            raise FigmaValidationError(f"Format must be one of: {valid_formats}")

        if scale <= 0:
            raise FigmaValidationError("Scale must be positive")

        params = {
            "ids": ",".join(node_ids),
            "format": format.upper(),
            "scale": scale
        }

        result = self.client.get(f"/images/{file_key}", params=params, use_cache=use_cache)
        return result.get("images", {})

    def get_single_url(
        self,
        file_key: str,
        node_id: str,
        format: str = "PNG",
        scale: Union[int, float] = 1,
        use_cache: bool = False
    ) -> Optional[str]:
        """
        Get image URL for a single node.

        Args:
            file_key: Figma file key
            node_id: Node ID to export
            format: Image format ('PNG', 'JPG', 'SVG', 'PDF')
            scale: Export scale factor
            use_cache: Whether to use cached data

        Returns:
            Image URL or None if not found
        """
        urls = self.get_urls(file_key, [node_id], format, scale, use_cache)
        return urls.get(node_id)

    def download_image(
        self,
        url: str,
        output_path: str,
        timeout: int = 30
    ) -> bool:
        """
        Download image from URL to local file.

        Args:
            url: Image URL to download
            output_path: Local file path to save image
            timeout: Download timeout in seconds

        Returns:
            True if download was successful
        """
        try:
            import requests
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(response.content)

            return True
        except Exception:
            return False

    def export_frame(
        self,
        file_key: str,
        frame_id: str,
        output_path: str,
        format: str = "PNG",
        scale: Union[int, float] = 1
    ) -> bool:
        """
        Export a frame as an image file.

        Args:
            file_key: Figma file key
            frame_id: Frame node ID
            output_path: Local file path to save image
            format: Image format ('PNG', 'JPG', 'SVG', 'PDF')
            scale: Export scale factor

        Returns:
            True if export was successful
        """
        url = self.get_single_url(file_key, frame_id, format, scale)

        if not url:
            return False

        return self.download_image(url, output_path)