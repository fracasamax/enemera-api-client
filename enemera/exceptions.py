"""
Custom exceptions for the Enemera API client.
"""
from typing import Optional, Dict, Any, Union


class EnemeraError(Exception):
    """Base exception for all Enemera API client errors."""

    def __init__(self, message: str, **kwargs):
        self.message = message
        self.extra_data = kwargs
        super().__init__(message)


class AuthenticationError(EnemeraError):
    """Raised when authentication with the API fails."""

    def __init__(self, message: str = "Authentication failed. Check your API key.", **kwargs):
        super().__init__(message, **kwargs)


class RateLimitError(EnemeraError):
    """Raised when the API rate limit is exceeded."""

    def __init__(
        self,
        message: str = "API rate limit exceeded. Please slow down your requests.",
        retry_after: Optional[int] = None,
        **kwargs
    ):
        self.retry_after = retry_after
        super().__init__(message, retry_after=retry_after, **kwargs)


class APIError(EnemeraError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        response_body: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        **kwargs
    ):
        self.status_code = status_code
        self.detail = detail
        self.response_body = response_body
        self.request_id = request_id
        message = f"API Error {status_code}: {detail}"
        if request_id:
            message += f" (Request ID: {request_id})"
        super().__init__(
            message,
            status_code=status_code,
            detail=detail,
            response_body=response_body,
            request_id=request_id,
            **kwargs
        )


class ValidationError(EnemeraError):
    """Raised when input validation fails."""

    def __init__(
        self,
        message: str = "Validation error",
        errors: Optional[Dict[str, Any]] = None,
        **kwargs
    ):
        self.errors = errors or {}
        super().__init__(message, errors=errors, **kwargs)


class ConnectionError(EnemeraError):
    """Raised when connection to the API fails."""

    def __init__(
        self,
        message: str = "Connection to API failed",
        original_exception: Optional[Exception] = None,
        **kwargs
    ):
        self.original_exception = original_exception
        super().__init__(
            message,
            original_exception=str(
                original_exception) if original_exception else None,
            **kwargs
        )


class TimeoutError(ConnectionError):
    """Raised when a request times out."""

    def __init__(
        self,
        message: str = "Request timed out",
        timeout_value: Optional[Union[int, float]] = None,
        **kwargs
    ):
        self.timeout_value = timeout_value
        super().__init__(message, timeout_value=timeout_value, **kwargs)


class RetryError(EnemeraError):
    """Raised when all retry attempts fail."""

    def __init__(
        self,
        message: str = "All retry attempts failed",
        attempts: int = 0,
        last_exception: Optional[Exception] = None,
        **kwargs
    ):
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(
            message,
            attempts=attempts,
            last_exception=str(last_exception) if last_exception else None,
            **kwargs
        )


class DependencyError(EnemeraError):
    """
    Raised when a required optional dependency is not installed.
    Provides clear information about which package is missing and how to install it.
    """

    def __init__(self, package_name: str, feature_description: str, install_command: str):
        self.package_name = package_name
        self.feature_description = feature_description
        self.install_command = install_command
        message = (
            f"The '{package_name}' package is required to {feature_description}. "
            f"Please install it using: {install_command}"
        )
        super().__init__(
            message,
            package_name=package_name,
            feature_description=feature_description,
            install_command=install_command
        )


class ConfigurationError(EnemeraError):
    """Raised when there's an issue with the client configuration."""

    def __init__(self, message: str = "Invalid client configuration", **kwargs):
        super().__init__(message, **kwargs)
