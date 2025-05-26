"""
Constants used throughout the Enemera API client.
"""

# Base API URL - set a default but allow override
BASE_URL = "https://api.enemera.com"


# Default request timeout in seconds
DEFAULT_TIMEOUT = 30

# Default max retries for failed requests
DEFAULT_MAX_RETRIES = 3

# Default rate limits
DEFAULT_RATE_LIMIT_MAX_REQUESTS = 10
DEFAULT_RATE_LIMIT_PERIOD = 1.0  # seconds

# Date format for API requests (ISO 8601 date format)
DATE_FORMAT = "%Y-%m-%d"
