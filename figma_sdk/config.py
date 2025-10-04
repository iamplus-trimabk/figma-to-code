"""
Configuration management for the Figma SDK.

Handles environment variables, validation, and default settings.
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class FigmaConfig:
    """Configuration settings for Figma SDK."""

    access_token: str
    base_url: str = "https://api.figma.com/v1"
    timeout: int = 30
    max_retries: int = 3
    cache_ttl: int = 3000  # 50 minutes
    cache_dir: str = "figma_cache"

    @classmethod
    def from_env(cls) -> "FigmaConfig":
        """Create configuration from environment variables."""
        access_token = os.getenv("ACCESS_TOKEN")
        if not access_token:
            raise ValueError("ACCESS_TOKEN environment variable is required")

        return cls(
            access_token=access_token,
            base_url=os.getenv("FIGMA_BASE_URL", cls.base_url),
            timeout=int(os.getenv("FIGMA_TIMEOUT", str(cls.timeout))),
            max_retries=int(os.getenv("FIGMA_MAX_RETRIES", str(cls.max_retries))),
            cache_ttl=int(os.getenv("FIGMA_CACHE_TTL", str(cls.cache_ttl))),
            cache_dir=os.getenv("FIGMA_CACHE_DIR", cls.cache_dir)
        )

    def validate(self) -> None:
        """Validate configuration settings."""
        if not self.access_token:
            raise FigmaValidationError("Access token is required")
        if not self.base_url:
            raise FigmaValidationError("Base URL is required")
        if self.timeout <= 0:
            raise FigmaValidationError("Timeout must be positive")
        if self.max_retries < 0:
            raise FigmaValidationError("Max retries must be non-negative")


# Import here to avoid circular imports
try:
    from .exceptions import FigmaValidationError
except ImportError:
    # For standalone usage
    class FigmaValidationError(Exception):
        pass