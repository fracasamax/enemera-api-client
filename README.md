# Enemera API Client

A Python client for the Enemera energy data API. This package provides a simple interface to access energy market and grid data from Italian and European markets.

## Installation

```bash
pip install enemera
```

### Optional Dependencies

For data conversion features, you can install optional dependencies:

```bash
# For pandas DataFrame conversion
pip install enemera[pandas]

# For polars DataFrame conversion
pip install enemera[polars]

# For Excel export with openpyxl
pip install enemera[excel]

# For Excel export with xlsxwriter
pip install enemera[excel-xlsxwriter]

# For all data conversion features
pip install enemera[all]
```

## Usage

```python
from enemera import EnemeraClient, Market, Area, Curve
from datetime import datetime, timedelta

# Initialize the client with your API key
client = EnemeraClient(api_key="your_api_key_here")

# Get prices for the MGP market in the NORD zone for the last week
yesterday = datetime.now() - timedelta(days=1)
week_ago = datetime.now() - timedelta(days=7)

# Get market prices - using Market enum
prices = client.data.get(
    curve=Curve.ITALY_PRICES,
    market=Market.MGP,
    date_from=week_ago.strftime("%Y-%m-%d"),
    date_to=yesterday.strftime("%Y-%m-%d"),
    area=Area.NORD
)

# The response behaves like a list of price objects
print(f"Retrieved {len(prices)} price records")

# Print the prices
for price in prices:
    print(f"Time: {price.utc}, Market: {price.market}, Zone: {price.zone}, Price: {price.price} EUR/MWh")
```

## Data Conversion

The client provides direct methods on API responses to convert data to various formats:

### Converting to pandas DataFrame

```python
from datetime import datetime, date
from enemera import Curve

# Shorthand: get pandas DataFrame directly via unified interface
df_cet1 = client.data.get_pandas(
    curve=Curve.ITALY_PRICES,
    use_cet_index=True,  # Default True: CET index named 'cet'
    market="MGP",
    date_from="2023-01-01",
    date_to="2023-01-07",
    area="NORD"
)

# Using datetime/date objects
df_cet2 = client.data.get_pandas(
    curve=Curve.ITALY_PRICES,
    use_cet_index=True,
    market=Market.MGP,
    date_from=datetime(2023, 1, 1),
    date_to=date(2023, 1, 7),
    area=Area.NORD
)

# Partial date strings (first day used)
df_cet3 = client.data.get_pandas(
    curve=Curve.ITALY_PRICES,
    use_cet_index=True,
    market=Market.MGP,
    date_from="2023-01",
    date_to="2023-01-07",
    area=Area.NORD
)
```

### Converting to polars DataFrame

```python
# Convert to polars DataFrame directly
pl_df = prices.to_polars()

# Analyze data
import polars as pl
print(pl_df.head())
print(f"Average price: {pl_df.select(pl.mean('price')).item():.2f} EUR/MWh")
```

### Exporting to CSV

```python
# Save to CSV file directly
prices.to_csv("prices_data.csv", index=False)
```

### Exporting to Excel

```python
# Save to Excel file directly
prices.to_excel(
    "prices_data.xlsx", 
    sheet_name="MGP Prices", 
    index=False
)

# With additional formatting (requires pandas)
import pandas as pd
df = prices.to_pandas()

with pd.ExcelWriter("prices_analysis.xlsx", engine="openpyxl") as writer:
    # Raw data
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    
    # Daily statistics
    daily_stats = df.groupby(df["utc"].dt.date)["price"].agg(["mean", "min", "max"])
    daily_stats.to_excel(writer, sheet_name="Daily Stats")
```

## Multi-sheet Excel Export Example

```python
# Get both prices and volumes
prices = client.prices.get(market="MGP", date_from="2023-01-01", date_to="2023-01-07", area="NORD")
volumes = client.italy.exchange_volumes.get(market="MGP", date_from="2023-01-01", date_to="2023-01-07", area="NORD")

# Create a multi-sheet Excel file
import pandas as pd

with pd.ExcelWriter("market_analysis.xlsx", engine="openpyxl") as writer:
    # Prices sheet
    prices.to_pandas().to_excel(writer, sheet_name="Prices", index=False)
    
    # Volumes sheet
    volumes.to_pandas().to_excel(writer, sheet_name="Volumes", index=False)
    
    # Analysis sheet (custom calculations)
    prices_df = prices.to_pandas()
    prices_df["hour"] = prices_df["utc"].dt.hour
    hourly_avg = prices_df.groupby("hour")["price"].mean().reset_index()
    hourly_avg.to_excel(writer, sheet_name="Hourly Analysis", index=False)
```

## Available Endpoints

The client is organized using a namespace structure:

### Italy Namespace (`client.italy`)

- `italy.prices.get()`: Access to the `/italy/prices/{market}/` endpoint for market prices
- `italy.exchange_volumes.get()`: Access to the `/italy/exchange_volumes/{market}/` endpoint for market volumes
- `italy.commercial_flows.get()`: Access to the `/italy/commercial_flows/` endpoint for cross-zonal flows

For backward compatibility, prices are also available directly via `client.prices.get()`.

## Enums

The client provides enums for common parameters:

- `Market`: Enum for Italian energy market identifiers (MGP, MI1, MI2, etc.)
- `Area`: Enum for Italian bidding zones and macrozones (NORD, CNOR, CSUD, etc.)

These enums can be used interchangeably with string values:

```python
# Using enums
client.italy.prices.get(market=Market.MGP, area=Area.NORD, ...)

# Using strings
client.italy.prices.get(market="MGP", area="NORD", ...)
```

## Authentication

The client uses API key authentication with Bearer tokens. You can obtain an API key by subscribing to the Enemera API service.

## Features

- Organized namespace structure for intuitive API navigation
- Enum support for market and area identifiers
- Handles authentication automatically
- Converts API responses to Python objects
- Direct conversion methods on API responses (to_pandas, to_polars, to_csv, to_excel)
- Comprehensive error handling
- Date formatting helpers
- Type hints for better IDE support

## License

MIT

# Error Handling and Logging

The Enemera API client includes comprehensive error handling and logging capabilities to help you debug issues and build robust applications.

## Error Handling

The client provides a hierarchy of exception classes:

- `EnemeraError`: Base exception for all client errors
  - `AuthenticationError`: Raised when authentication fails
  - `RateLimitError`: Raised when API rate limits are exceeded
  - `APIError`: Raised when the API returns an error response
  - `ValidationError`: Raised when input validation fails
  - `ConnectionError`: Raised when connection to the API fails
  - `TimeoutError`: Raised when a request times out
  - `RetryError`: Raised when all retry attempts fail
  - `DependencyError`: Raised when a required optional dependency is missing
  - `ConfigurationError`: Raised when there's an issue with the client configuration

Example of handling errors:

```python
from enemera import EnemeraClient
from enemera.exceptions import AuthenticationError, RateLimitError, APIError, ConnectionError

client = EnemeraClient(api_key="your_api_key_here")

try:
    prices = client.italy.prices.get(market="MGP", date="2023-05-01")
    print(f"Retrieved {len(prices)} price records")
except AuthenticationError:
    print("Authentication failed. Check your API key.")
except RateLimitError as e:
    retry_after = e.retry_after  # Seconds to wait before retry
    print(f"Rate limit exceeded. Retry after {retry_after} seconds")
except APIError as e:
    print(f"API error {e.status_code}: {e.detail}")
    if e.request_id:
        print(f"Request ID: {e.request_id}")
except ConnectionError:
    print("Connection failed. Check your internet connection.")
```

## Logging

The client includes a structured logging system that provides detailed information about API requests and errors.

### Configuring Logging

```python
from enemera import EnemeraClient
from enemera.logging import configure_logging
import logging

# Configure global client logging
configure_logging(
    level="debug",  # Available levels: debug, info, warning, error, critical
    handler=logging.FileHandler("enemera.log"),
    formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

# Or set logging level per client instance
client = EnemeraClient(api_key="your_api_key_here", log_level="debug")

# Change logging level at runtime
client.set_log_level("info")
```

## Rate Limiting and Retries

The client includes built-in protection against rate limiting and automatic retries for failed requests.

### Configuring Rate Limiting

```python
from enemera import EnemeraClient

# Configure rate limiting (max 10 requests per second)
client = EnemeraClient(
    api_key="your_api_key_here",
    rate_limit_max_requests=10,
    rate_limit_period=1.0  # seconds
)
```

### Configuring Retries

```python
from enemera import EnemeraClient
from enemera.retry import ExponentialBackoffStrategy

# Configure retry with exponential backoff
client = EnemeraClient(
    api_key="your_api_key_here",
    max_retries=3,  # Maximum number of retry attempts
    retry_strategy=ExponentialBackoffStrategy(
        base_delay=1.0,    # Initial delay in seconds
        max_delay=60.0,    # Maximum delay in seconds
        exponent=2.0,      # Exponent for backoff calculation
        jitter=True        # Add randomness to prevent thundering herd
    )
)

# You can also specify retry attempts per request
data = client.get("/some/endpoint", retry_attempts=5)
```

### Request IDs for Tracing

Each request gets a unique ID for tracing across logs and API responses:

```python
# Generate a custom request ID
import uuid
request_id = str(uuid.uuid4())

# Use the ID with a request
data = client.get("/some/endpoint", request_id=request_id)

# The ID will be included in all logs for this request
# and can be useful for debugging with the API provider
```

## Timezone Conversion

The client provides methods to convert UTC times to local timezones, such as Central European Time (CET), or any specified timezone.

### Converting UTC to local timezone (CET)

```python
# Get prices data
prices = client.italy.prices.get(
    market=Market.MGP,
    date_from="2023-01-01",
    date_to="2023-01-07"
)

# Convert to pandas with time in Central European Time (CET)
df_cet = prices.to_pandas_cet()

# The 'utc' column is now in CET timezone
print(df_cet.head())
print(f"Data timestamps are in CET timezone: {df_cet['utc'].dt.tz}")

# You can also specify a different datetime column if needed
df_cet_custom = prices.to_pandas_cet(datetime_col='my_time_column')
```

### Converting UTC to any timezone

```python
# Convert to any specific timezone
df_ny = prices.to_pandas_with_tz(tz='America/New_York')

# The 'utc' column is now in New York timezone
print(df_ny.head())

# Access the timezone information
print(f"Data timezone: {df_ny['utc'].dt.tz}")

# Compare UTC and local time values
df_multi_tz = prices.to_pandas()  # Original UTC data
df_cet = prices.to_pandas_cet()   # Data in CET

# Combine for comparison
comparison = pd.DataFrame({
    'UTC': df_multi_tz['utc'],
    'CET': df_cet['utc'],
    'Price (EUR/MWh)': df_multi_tz['price']
})
print(comparison.head())
```

### Using timezone conversion with existing DataFrame

If you already have a DataFrame with UTC timestamps, you can use the timezone conversion functions directly:

```python
from enemera.data_utils import convert_timezone, to_cet

# Convert an existing DataFrame from UTC to CET
df_utc = prices.to_pandas()
df_cet = to_cet(df_utc)

# Or convert to any timezone
df_tokyo = convert_timezone(df_utc, tz='Asia/Tokyo')
```

## Timezone Handling and Date Input Formats

The client provides flexible timezone handling and supports multiple date input formats for easier data analysis.

### Date Input Formats

You can specify dates in any of these formats:

```python
from datetime import datetime, date

# 1. Using datetime objects
df1 = client.prices.get_pandas(
    market=Market.MGP,
    date_from=datetime(2023, 1, 1),  # Full datetime object
    date_to=datetime(2023, 1, 7, 23, 59, 59),
    area=Area.NORD
)

# 2. Using date objects (midnight is assumed)
df2 = client.prices.get_pandas(
    market=Market.MGP,
    date_from=date(2023, 1, 1),     # Date object
    date_to=date(2023, 1, 7),       # Date object
    area=Area.NORD
)

# 3. Using string formats
# Full ISO format
df3 = client.prices.get_pandas(
    market=Market.MGP,
    date_from="2023-01-01T00:00:00",  # Full ISO format
    date_to="2023-01-07T23:59:59",
    area=Area.NORD
)

# Simple date strings
df4 = client.prices.get_pandas(
    market=Market.MGP,
    date_from="2023-01-01",   # Simple YYYY-MM-DD format
    date_to="2023-01-07",
    area=Area.NORD
)

# Partial date strings (first day of period is used)
df5 = client.prices.get_pandas(
    market=Market.MGP,
    date_from="2023-01",      # First day of January 2023
    date_to="2023-02",        # First day of February 2023
    area=Area.NORD
)
```

### Timezone Handling

The client supports various timezone features for convenient data analysis:

```python
# 1. Get data in CET timezone (default)
df_cet = client.prices.get_pandas(
    use_cet_index=True,  # This is the default
    market=Market.MGP,
    date_from="2023-01-01",
    date_to="2023-01-07",
    area=Area.NORD
)
print(f"Data with CET timezone: {df_cet['utc'].dt.tz}")

# 2. Keep UTC timezone
df_utc = client.prices.get_pandas(
    use_cet_index=False,  # Keep UTC timezone
    market=Market.MGP,
    date_from="2023-01-01",
    date_to="2023-01-07",
    area=Area.NORD
)
print(f"Data with UTC timezone: {df_utc['utc'].dt.tz}")

# 3. Convert existing data to any timezone
df_ny = prices.to_pandas_with_tz(tz='America/New_York')
print(f"Data in New York timezone: {df_ny['utc'].dt.tz}")

# 4. Use custom datetime column and index
df_custom = client.prices.get_pandas(
    use_cet_index=True,
    datetime_col='utc',      # Column containing datetime info
    index_col='utc',         # Column to use as index
    market=Market.MGP,
    date_from="2023-01-01",
    date_to="2023-01-07",
    area=Area.NORD
)

# 5. Compare timezones
comparison = pd.DataFrame({
    'UTC': df_utc['utc'],
    'CET': df_cet['utc'],
    'NY': df_ny['utc'],
    'Price (EUR/MWh)': df_utc['price']
})
print(comparison.head())
```
