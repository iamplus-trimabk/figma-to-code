"""
Figma SDK - Clean, minimal Python client for Figma REST API.

A professional SDK for accessing Figma designs with proper caching,
error handling, and clean architecture.
"""

from .client import FigmaClient
from .files import FigmaFile
from .exceptions import FigmaAPIError, FigmaAuthError, FigmaCacheError

__version__ = "1.0.0"
__all__ = [
    "FigmaClient",
    "FigmaFile",
    "FigmaAPIError",
    "FigmaAuthError",
    "FigmaCacheError"
]