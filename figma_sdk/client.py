"""
Main Figma API client.

Coordinates all SDK operations and provides the primary interface.
"""

import time
from typing import Dict, Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .auth import FigmaAuth
from .cache import FigmaCache
from .config import FigmaConfig
from .exceptions import (
    FigmaAPIError, FigmaAuthError, FigmaRateLimitError,
    FigmaNotFoundError, FigmaValidationError
)
from .files import FileOperations
from .nodes import NodeOperations
from .images import ImageOperations
from .components import ComponentOperations
from .styles import StyleOperations


class FigmaClient:
    """Main Figma API client with clean, professional interface."""

    def __init__(self, token: str = None, config: FigmaConfig = None):
        """Initialize client with token or config."""
        if config:
            self.config = config
        elif token:
            self.config = FigmaConfig(access_token=token)
        else:
            self.config = FigmaConfig.from_env()

        self.config.validate()

        # Initialize components
        self.auth = FigmaAuth(self.config.access_token)
        self.cache = FigmaCache(self.config.cache_dir)
        self.session = self._create_session()

        # Initialize operation modules
        self.files = FileOperations(self)
        self.nodes = NodeOperations(self)
        self.images = ImageOperations(self)
        self.components = ComponentOperations(self)
        self.styles = StyleOperations(self)

    def _create_session(self) -> requests.Session:
        """Create HTTP session with retry configuration."""
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=self.config.max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update(self.auth.headers)

        return session

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Dict[str, Any] = None,
        data: Dict[str, Any] = None,
        use_cache: bool = True,
        cache_ttl: int = None
    ) -> Dict[str, Any]:
        """Make HTTP request with caching and error handling."""
        url = f"{self.config.base_url}{endpoint}"

        # Check cache first for GET requests
        if method.upper() == "GET" and use_cache:
            cache_key = f"{method}:{endpoint}:{str(params or {})}"
            cached_result = self.cache.get(cache_key)
            if cached_result:
                return cached_result

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.config.timeout
            )

            # Handle specific HTTP errors
            if response.status_code == 401:
                raise FigmaAuthError("Invalid or expired access token")
            elif response.status_code == 404:
                raise FigmaNotFoundError(f"Resource not found: {endpoint}")
            elif response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                raise FigmaRateLimitError(
                    "Rate limit exceeded",
                    retry_after=int(retry_after) if retry_after else None
                )
            elif not response.ok:
                raise FigmaAPIError(
                    f"API request failed: {response.text}",
                    status_code=response.status_code,
                    response_data=response.json() if response.content else {}
                )

            result = response.json()

            # Cache successful GET requests
            if method.upper() == "GET" and use_cache:
                ttl = cache_ttl or self.config.cache_ttl
                self.cache.set(cache_key, result, ttl)

            return result

        except requests.exceptions.Timeout:
            raise FigmaAPIError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise FigmaAPIError("Connection error")
        except requests.exceptions.RequestException as e:
            raise FigmaAPIError(f"Request failed: {e}")

    def get(self, endpoint: str, params: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make GET request."""
        return self._make_request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, data: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """Make POST request."""
        return self._make_request("POST", endpoint, data=data, **kwargs)

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def health_check(self) -> bool:
        """Check if the API is accessible."""
        try:
            self.get("/me")
            return True
        except FigmaAPIError:
            return False

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get client usage statistics."""
        return {
            "cache_stats": self.cache.get_stats(),
            "health_check": self.health_check()
        }