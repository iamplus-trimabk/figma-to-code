"""
Authentication handling for the Figma SDK.

Manages Personal Access Token authentication with proper security practices.
"""

from typing import Dict
import requests
from .exceptions import FigmaAuthError, FigmaAPIError


class FigmaAuth:
    """Handles Personal Access Token authentication for Figma API."""

    def __init__(self, access_token: str):
        """Initialize with Personal Access Token."""
        if not access_token:
            raise FigmaAuthError("Access token is required")
        self._access_token = access_token

    @property
    def headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        return {
            "X-Figma-Token": self._access_token,
            "Content-Type": "application/json"
        }

    async def validate_token(self) -> bool:
        """Validate the access token by making a test API call."""
        try:
            response = requests.get(
                "https://api.figma.com/v1/me",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def authenticate_request(self, request_func):
        """Add authentication to a request function."""
        def wrapper(*args, **kwargs):
            # Ensure headers are set
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            kwargs['headers'].update(self.headers)

            response = request_func(*args, **kwargs)

            # Handle auth errors
            if response.status_code == 401:
                raise FigmaAuthError("Invalid or expired access token")

            return response

        return wrapper