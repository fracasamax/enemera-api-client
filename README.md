# Enemera API Client

[![PyPI version](https://badge.fury.io/py/enemera.svg)](https://badge.fury.io/py/enemera)
[![Python](https://img.shields.io/pypi/pyversions/enemera.svg)](https://pypi.org/project/enemera/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Python client for the Enemera energy data API, providing access to European electricity market data with
enhanced functionality and type-safe enums.

## Features

- **Multiple Output Formats**: Native support for pandas DataFrames, Polars DataFrames, CSV, and Excel exports
- **Type Safety**: Comprehensive enums for markets, areas, and trading purposes
- **Timezone Handling**: Automatic UTC to CET timezone conversion for European energy markets
- **Robust Error Handling**: Detailed exception hierarchy with retry logic and rate limiting
- **Flexible Data Access**: Generic curve access via unified client or specialized country-specific clients
- **Optional Dependencies**: Install only what you need for your specific use case

## Supported Markets

### Italy

- **Prices**: Day-ahead (MGP) and intraday markets (MI1-MI7)
- **XBID Results**: Cross-border intraday trading data
- **Exchange Volumes**: Trading volumes by market and purpose
- **Ancillary Services**: MSD, MB, MBa, MBs market data
- **Load Data**: Actual and forecast consumption
- **Generation**: Actual and forecast generation by technology
- **Commercial Flows**: Inter-zonal power flows and limits
- **Imbalance Data**: System imbalance volumes and prices

### Spain

- **Prices**: Day-ahead and intraday market prices
- **XBID Results**: Cross-border intraday trading data

## Installation

### Basic Installation

```bash
pip install enemera
```

### With Optional Dependencies

```bash
# For pandas support
pip install enemera[pandas]

# For polars support  
pip install enemera[polars]

# For Excel export
pip install enemera[excel]

# For Excel export with xlsxwriter
pip install enemera[excel-xlsxwriter]

# Install everything
pip install enemera[all]
```

## Quick Start

### Authentication

```python
from enemera import EnemeraClient

# Initialize with API key
client = EnemeraClient(api_key="your-api-key")

# Or set via environment variable ENEMERA_API_KEY
client = EnemeraClient()
```

### Basic Usage

```python
from enemera import EnemeraClient, Curve
from datetime import date

client = EnemeraClient(api_key="your-api-key")

# Get Italian day-ahead prices
response = client.get(
    curve=Curve.ITALY_PRICES,
    market="MGP",
    date_from=date(2024, 1, 1),
    date_to=date(2024, 1, 7),
    area="NORD"
)

# Convert to pandas DataFrame
df = response.to_pandas()
print(df.head())
```

### Using Type-Safe Enums

```python
from enemera import EnemeraClient, Curve, Market, Area, Purpose

client = EnemeraClient(api_key="your-api-key")

# Type-safe market and area specification
response = client.get(
    curve=Curve.ITALY_PRICES,
    market=Market.MGP,
    area=Area.NORD,
    date_from="2024-01-01",
    date_to="2024-01-07"
)
```

### Direct DataFrame Access

```python
# Get data directly as pandas DataFrame
df = client.get_pandas(
    curve=Curve.ITALY_PRICES,
    market=Market.MGP,
    area=Area.NORD,
    date_from="2024-01-01",
    date_to="2024-01-07"
)

# Get data with CET timezone
df_cet = client.get_pandas_cet(
    curve=Curve.ITALY_LOAD_ACTUAL,
    date_from="2024-01-01",
    date_to="2024-01-07",
    area=Area.NORD
)
```

## Data Export

### CSV Export

```python
response = client.get(curve=Curve.ITALY_PRICES, ...)
response.to_csv("prices.csv", index=True)
```

### Excel Export

```python
response = client.get(curve=Curve.ITALY_PRICES, ...)
response.to_excel("prices.xlsx", sheet_name="Prices", index=True)
```

### Polars DataFrame

```python
response = client.get(curve=Curve.ITALY_PRICES, ...)
df_polars = response.to_polars()
```

## Country-Specific Clients

For more specialized access, you can use country-specific clients:

### Italy

```python
from enemera.api import ItalyPricesClient, ItalyLoadActualClient

# Specialized Italy prices client
italy_prices = ItalyPricesClient(api_key="your-api-key")
response = italy_prices.get(
    market="MGP",
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)

# Load data client
italy_load = ItalyLoadActualClient(api_key="your-api-key")
load_response = italy_load.get(
    date_from="2024-01-01",
    date_to="2024-01-07",
    area="NORD"
)
```

### Spain

```python
from enemera.api import SpainPricesClient

spain_prices = SpainPricesClient(api_key="your-api-key")
response = spain_prices.get(
    market="MD",
    date_from="2024-01-01",
    date_to="2024-01-07"
)
```

## Available Curves

| Curve                       | Description                      | Countries |
|-----------------------------|----------------------------------|-----------|
| `ITALY_PRICES`              | Electricity prices by market     | Italy     |
| `ITALY_XBID_RESULTS`        | XBID trading results             | Italy     |
| `ITALY_EXCHANGE_VOLUMES`    | Trading volumes                  | Italy     |
| `ITALY_ANCILLARY_SERVICES`  | Ancillary services data          | Italy     |
| `ITALY_LOAD_ACTUAL`         | Actual electricity consumption   | Italy     |
| `ITALY_LOAD_FORECAST`       | Forecast electricity consumption | Italy     |
| `ITALY_GENERATION`          | Actual generation by technology  | Italy     |
| `ITALY_GENERATION_FORECAST` | Forecast generation              | Italy     |
| `ITALY_COMMERCIAL_FLOWS`    | Inter-zonal power flows          | Italy     |
| `ITALY_IMBALANCE_DATA`      | System imbalance data            | Italy     |
| `SPAIN_PRICES`              | Electricity prices               | Spain     |
| `SPAIN_XBID_RESULTS`        | XBID trading results             | Spain     |

## Enums Reference

### Markets

```python
from enemera import Market

# Italian markets
Market.MGP    # Day-Ahead Market
Market.MI1    # Intraday Market 1
Market.MI2    # Intraday Market 2
# ... MI3 through MI7
Market.MSD    # Ancillary Services Market
Market.MB     # Balancing Market
```

### Areas (Italy)

```python
from enemera import Area

# Bidding zones
Area.NORD     # North
Area.CNOR     # Center-North  
Area.CSUD     # Center-South
Area.SUD      # South
Area.SICI     # Sicily
Area.SARD     # Sardinia
Area.CALA     # Calabria

# Virtual zones
Area.BRNN     # Brindisi
Area.FOGN     # Foggia
# ... and more
```

### Trading Purpose

```python
from enemera import Purpose

Purpose.BUY   # Buy orders
Purpose.SELL  # Sell orders
```

## Error Handling

The client provides comprehensive error handling:

```python
from enemera import (
    EnemeraClient,
    AuthenticationError,
    RateLimitError,
    APIError,
    ValidationError
)

client = EnemeraClient(api_key="your-api-key")

try:
    response = client.get(curve=Curve.ITALY_PRICES, ...)
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid parameters: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e.detail}")
```

## Configuration

### Environment Variables

```bash
export ENEMERA_API_KEY="your-api-key"
export ENEMERA_BASE_URL="https://api.enemera.com"  # Optional
```

### Logging

```python
from enemera.utils.logging import configure_logging

# Configure logging level
configure_logging(level="debug")

# Or get a custom logger
from enemera.utils.logging import get_logger

logger = get_logger("my_app")
```

## Advanced Usage

### Date Handling

```python
from datetime import datetime, date

# Multiple date formats supported
client.get(
    curve=Curve.ITALY_PRICES,
    date_from="2024-01-01",  # String
    date_to=date(2024, 1, 7),  # Date object
    # date_to=datetime(2024, 1, 7), # Datetime object
)
```

### Timezone Conversion

```python
# Get data with UTC timestamps (default)
df_utc = response.to_pandas()

# Get data with CET timestamps  
df_cet = response.to_pandas_cet()

# Get naive datetime (no timezone info)
df_naive = response.to_pandas(naive_datetime=True)
```

## Requirements

- Python ≥ 3.7
- requests ≥ 2.25.0
- pydantic ≥ 2.0.0
- python-dateutil ≥ 2.8.0

### Optional Dependencies

- pandas ≥ 1.0.0 (for DataFrame support)
- polars ≥ 0.7.0 (for Polars DataFrame support)
- openpyxl ≥ 3.0.0 (for Excel export)
- xlsxwriter ≥ 3.0.0 (alternative Excel writer)
- pytz ≥ 2023.3 (for timezone handling)

## API Documentation

For detailed API documentation and available endpoints, visit
the [Enemera API documentation](https://api.enemera.com/docs).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to
discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/fracasamax/enemera-api-client/issues)
- **Email**: [dev@elnc.eu](mailto:dev@elnc.eu)

## Changelog

### v0.2.0

- Enhanced functionality with type-safe enums
- Multiple output format support (pandas, polars, CSV, Excel)
- Improved error handling and validation
- Timezone conversion utilities
- Optional dependencies for flexible installation

---

**Disclaimer**: This is an unofficial client library. Enemera is a trademark of its respective owners.