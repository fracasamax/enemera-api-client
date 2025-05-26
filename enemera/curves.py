from enum import Enum


class Curve(Enum):
    """Data curves available in the API"""
    ITALY_PRICES = "italy_prices"
    ITALY_XBID_RESULTS = "italy_xbid_results"
    ITALY_EXCHANGE_VOLUMES = "italy_exchange_volumes"
    ITALY_ANCILLARY_SERVICES = "italy_ancillary_services"
    ITALY_DAM_DEMAND_ACT = "italy_dam_demand_act"
    ITALY_DAM_DEMAND_FCS = "italy_dam_demand_fcs"
    ITALY_COMMERCIAL_FLOWS = "italy_commercial_flows"
    ITALY_COMMERCIAL_FLOW_LIMITS = "italy_commercial_flow_limits"
    ITALY_DEMAND_FORECAST = "italy_demand_forecast"
    ITALY_DEMAND_ACTUAL = "italy_demand_actual"
    ITALY_LOAD_ACTUAL = "italy_load_actual"
    ITALY_LOAD_FORECAST = "italy_load_forecast"
    ITALY_GENERATION = "italy_generation"
    ITALY_GENERATION_FORECAST = "italy_generation_forecast"
    ITALY_IMBALANCE_DATA = "italy_imbalance_data"
    ITALY_IMBALANCE_PRICES = "italy_imbalance_prices"
    ITALY_IMBALANCE_VOLUMES = "italy_imbalance_volumes"
    SPAIN_PRICES = "spain_prices"
    SPAIN_XBID_RESULTS = "spain_xbid_results"
