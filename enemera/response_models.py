"""
Enemera API Client v2 - Simplified client with proper inheritance to avoid repetition
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Base models
class BaseTimeSeriesResponse(BaseModel):
    utc: datetime = Field(..., description="UTC timestamp")


class PriceData(BaseTimeSeriesResponse):
    market: str = Field(..., description="Market identifier")
    zone: str = Field(..., description="Zone identifier")
    price: float = Field(..., description="Price in EUR/MWh")


class IPEXXbidRecapResponse(BaseTimeSeriesResponse):
    zone: str = Field(..., description="Zone identifier")
    time_resolution: str = Field(..., description="Time resolution (e.g., PT60M, PT15M)")
    first_price: Optional[float] = Field(..., description="First price in EUR/MWh")
    last_price: Optional[float] = Field(..., description="Last price in EUR/MWh")
    min_price: Optional[float] = Field(..., description="Minimum price in EUR/MWh")
    max_price: Optional[float] = Field(..., description="Maximum price in EUR/MWh")
    ref_price: Optional[float] = Field(..., description="Reference price in EUR/MWh")
    last_hour_price: Optional[float] = Field(..., description="Last hour price in EUR/MWh")
    buy_volume: Optional[float] = Field(..., description="Buy volume in MWh")
    sell_volume: Optional[float] = Field(..., description="Sell volume in MWh")


class IpexQuantityResponse(BaseTimeSeriesResponse):
    market: str = Field(..., description="Market identifier")
    zone: str = Field(..., description="Zone identifier")
    purpose: str = Field(..., description="BUY or SELL")
    quantity: float = Field(..., description="Quantity in MWh")


class IPEXAncillaryServicesResponse(BaseTimeSeriesResponse):
    zone: str = Field(..., description="Zone identifier")
    market: str = Field(..., description="Market identifier (e.g., MSD, MB)")
    segment: str = Field(..., description="Market segment (e.g., MSD, MBs, MBa, MB)")
    buy_volume: Optional[float] = Field(None, description="Buy volume in MWh")
    sell_volume: Optional[float] = Field(None, description="Sell volume in MWh")
    buy_volume_no_rev: Optional[float] = Field(None, description="Buy volume without revision in MWh")
    sell_volume_no_rev: Optional[float] = Field(None, description="Sell volume without revision in MWh")
    avg_buy_price: Optional[float] = Field(None, description="Average buy price in EUR/MWh")
    avg_sell_price: Optional[float] = Field(None, description="Average sell price in EUR/MWh")
    max_sell_price: Optional[float] = Field(None, description="Maximum sell price in EUR/MWh")
    min_buy_price: Optional[float] = Field(None, description="Minimum buy price in EUR/MWh")


class IPEXFlowResponse(BaseTimeSeriesResponse):
    market: str = Field(..., description="Market identifier (e.g., MGP, MI1, MI2)")
    zone_from: str = Field(..., description="Zone FROM identifier")
    zone_to: str = Field(..., description="Zone TO identifier")
    flow: float = Field(..., description="Flow value in MW")


class IPEXFlowLimitResponse(BaseTimeSeriesResponse):
    market: str = Field(..., description="Market identifier (e.g., MGP, MI1, MI2)")
    zone_from: str = Field(..., description="Zone FROM identifier")
    zone_to: str = Field(..., description="Zone TO identifier")
    flow_limit: float = Field(..., description="Flow value in MW")
    coefficient: float = Field(..., description="Coefficient value")


class IPEXEstimatedDemandResponse(BaseTimeSeriesResponse):
    zone: str = Field(..., description="Zone identifier")
    demand: float = Field(..., description="Estimated demand value in MW")


class IPEXActualDemandResponse(BaseTimeSeriesResponse):
    zone: str = Field(..., description="Zone identifier")
    demand: float = Field(..., description="Actual demand value in MW")


class ItalyImbalanceDataResponse(BaseTimeSeriesResponse):
    macrozone: str = Field(..., description="Macrozone identifier (NORD or SUD)")
    imb_volume: Optional[float] = Field(None, description="Imbalance volume in MWh")
    imb_sign: Optional[int] = Field(None, description="Imbalance sign (-1, 0, or 1)")
    imb_price: Optional[float] = Field(None, description="Imbalance price in EUR/MWh")
    imb_base_price: Optional[float] = Field(None, description="Imbalance base price in EUR/MWh")
    pnamz: Optional[float] = Field(None, description="Non-arbitrage price (PNAMZ) in EUR/MWh")
    scambi: Optional[float] = Field(None, description="Scambi value in MW")
    estero: Optional[float] = Field(None, description="Estero value in MW")
    is_final_sign: Optional[bool] = Field(None,
                                          description="Indicates if the data is final (True) or provisional (False)")
    is_final_price: Optional[bool] = Field(None,
                                           description="Indicates if the price is final (True) or provisional (False)")
    is_final_pnamz: Optional[bool] = Field(None,
                                           description="Indicates if the non-arbitrage price is final (True) or provisional (False)")


class TernaImbalancePriceResponse(BaseTimeSeriesResponse):
    macrozone: str = Field(..., description="Macrozone identifier (NORD or SUD)")
    imb_price: Optional[float] = Field(None, description="Imbalance price in EUR/MWh")
    imb_base_price: Optional[float] = Field(None, description="Imbalance base price in EUR/MWh")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the price is final (True) or provisional (False)")


class TernaImbalanceVolumeResponse(BaseTimeSeriesResponse):
    macrozone: str = Field(..., description="Macrozone identifier (NORD or SUD)")
    imb_volume: Optional[float] = Field(None, description="Imbalance volume in MW")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the data is final (True) or provisional (False)")


class TernaImbalanceSignResponse(BaseTimeSeriesResponse):
    macrozone: str = Field(..., description="Macrozone identifier (NORD or SUD)")
    imb_sign: Optional[int] = Field(None, description="Imbalance sign (-1, 0, or 1)")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the data is final (True) or provisional (False)")


class TernaNonArbitragePriceResponse(BaseTimeSeriesResponse):
    macrozone: str = Field(..., description="Macrozone identifier (NORD or SUD)")
    pnamz: Optional[float] = Field(None, description="Non-arbitrage price (PNAMZ) in EUR/MWh")
    time_resolution: str = Field(..., description="Time resolution (PT60M or PT15M)")
    is_final: Optional[bool] = Field(None,
                                     description="Indicates if the non-arbitrage price is final (True) or provisional (False)")


class GenerationData(BaseTimeSeriesResponse):
    area: str = Field(..., description="Area code")
    gen_type: str = Field(..., description="Generation type")
    data_value: Optional[float] = Field(None, description="Generation value in MW")


class LoadData(BaseTimeSeriesResponse):
    area: str = Field(..., description="Area code")
    data_value: Optional[float] = Field(None, description="Load value in MW")


class SpainPriceResponse(BaseTimeSeriesResponse):
    market: str = Field(..., description="Market identifier (e.g., MD, MI1, MI2)")
    zone: str = Field(..., description="Zone identifier")
    price: float = Field(..., description="Price value in EUR/MWh")


class SpainXbidResultsResponse(BaseTimeSeriesResponse):
    zone: str = Field(..., description="Zone identifier")
    wavg_price: Optional[float] = Field(None, description="Weighted average price value in EUR/MWh")
    min_price: Optional[float] = Field(None, description="Minimum price value in EUR/MWh")
    max_price: Optional[float] = Field(None, description="Maximum price value in EUR/MWh")
