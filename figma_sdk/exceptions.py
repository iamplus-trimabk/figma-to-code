"""
Custom exceptions for the Figma SDK.

Provides clear, specific error types for different failure scenarios.
"""


class FigmaAPIError(Exception):
    """Base exception for Figma API errors."""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.status_code:
            return f"Figma API Error {self.status_code}: {self.message}"
        return f"Figma API Error: {self.message}"


class FigmaAuthError(FigmaAPIError):
    """Authentication related errors."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class FigmaRateLimitError(FigmaAPIError):
    """Rate limiting errors."""

    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        self.retry_after = retry_after
        super().__init__(message, status_code=429)


class FigmaNotFoundError(FigmaAPIError):
    """Resource not found errors."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class FigmaCacheError(Exception):
    """Cache related errors."""

    def __init__(self, message: str = "Cache operation failed"):
        self.message = message
        super().__init__(self.message)


class FigmaValidationError(Exception):
    """Input validation errors."""

    def __init__(self, message: str = "Validation failed"):
        self.message = message
        super().__init__(self.message)