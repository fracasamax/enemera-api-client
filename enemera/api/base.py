
from datetime import datetime, date
from typing import Dict, Any, Optional, Union, Type, TYPE_CHECKING, TypeVar

import pandas as pd
import requests

from enemera.response import APIResponse

# Define the generic type variable T
T = TypeVar('T')

if TYPE_CHECKING:
    import polars as pl

class BaseCurveClient:
    """Base class for all curve-specific clients with common functionality"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    @staticmethod
    def _format_date(date_obj: Union[str, datetime, date]) -> str:
        """Format date for API request"""
        if isinstance(date_obj, str):
            return date_obj
        elif isinstance(date_obj, datetime):
            return date_obj.strftime('%Y-%m-%d')
        elif isinstance(date_obj, date):
            return date_obj.strftime('%Y-%m-%d')
        else:
            return str(date_obj)

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> requests.Response:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"

        # Format dates in params
        formatted_params = {}
        date_from = None
        date_to = None

        for key, value in params.items():
            if value is not None:
                if key in ['date_from', 'date_to']:
                    try:
                        # Attempt to format the date value
                        formatted_value = self._format_date(value)
                        # Validate that the date string can be parsed as a valid date
                        datetime.strptime(formatted_value, '%Y-%m-%d')
                        formatted_params[key] = formatted_value

                        if key == 'date_from':
                            date_from = formatted_value
                        elif key == 'date_to':
                            date_to = formatted_value

                    except ValueError:
                        raise ValueError(f"Invalid date format for {key}: {value}. Expected 'YYYY-MM-DD', datetime, or date.")

                else:
                    formatted_params[key] = value

        # Validate date range if both dates are present
        if date_from and date_to:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()

            if to_date < from_date:
                raise ValueError(f"Invalid date range: date_to ({date_to}) cannot be before date_from ({date_from})")

        # Make the request
        response = self.session.get(url, params=formatted_params)
        response.raise_for_status()

        return response

    @staticmethod
    def _parse_response(response: requests.Response, model_class: Type[T]) -> APIResponse[T]:
        """Parse response into model objects"""
        data = response.json()
        items = [model_class(**item) for item in data]
        return APIResponse(items)

    def get_pandas(self, **kwargs) -> pd.DataFrame:
        """Get data as pandas DataFrame"""
        return self.get(**kwargs).to_pandas()

    def get_polars(self, **kwargs) -> 'pl.DataFrame':
        """Get data as polars DataFrame"""
        return self.get(**kwargs).to_polars()
