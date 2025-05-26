from datetime import datetime, date
from typing import Union, Optional

from enemera.api.base import BaseCurveClient
from enemera.constants import BASE_URL
from enemera.response import APIResponse
from enemera.response_models import PriceData


class ItalyPricesClient(BaseCurveClient):
    """Client for Italian electricity prices"""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(base_url=BASE_URL, api_key=api_key)

    def get(self,
            market: str,
            date_from: Union[str, datetime, date],
            date_to: Union[str, datetime, date],
            area: Optional[str] = None) -> APIResponse[PriceData]:
        """Get Italian electricity prices"""
        params = {
            'market': market,
            'date_from': date_from,
            'date_to': date_to,
            'area': area
        }
        endpoint = '/italy/prices'
        response = self._make_request(endpoint, params)
        return self._parse_response(response, PriceData)
