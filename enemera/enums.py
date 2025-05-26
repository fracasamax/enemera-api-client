"""
Enums for the Enemera API client.
"""

from enum import Enum


class Purpose(Enum):
    """Enum for the purpose of exchange volumes."""
    SELL = "SELL"  # Sell purpose
    BUY = "BUY"  # Buy purpose

    def __str__(self):
        return self.value


class Market(Enum):
    """Enum for Italian energy market identifiers."""
    MGP = "MGP"  # Day-Ahead Market
    MI1 = "MI1"  # Intraday Market 1
    MI2 = "MI2"  # Intraday Market 2
    MI3 = "MI3"  # Intraday Market 3
    MI4 = "MI4"  # Intraday Market 4
    MI5 = "MI5"  # Intraday Market 5
    MI6 = "MI6"  # Intraday Market 6
    MI7 = "MI7"  # Intraday Market 7
    MSD = "MSD"  # Ancillary Services Market
    MB = "MB"    # Balancing Market
    MBa = "MBa"  # Balancing Market - altri servizi (other services)
    MBs = "MBs"  # Balancing Market - secondary reserve

    def __str__(self):
        return self.value


class Area(Enum):
    """Enum for Italian bidding zones and macrozones."""
    # Standard bidding zones
    NORD = "NORD"  # North
    CNOR = "CNOR"  # Center-North
    CSUD = "CSUD"  # Center-South
    SUD = "SUD"  # South
    SICI = "SICI"  # Sicily
    SARD = "SARD"  # Sardinia
    CALA = "CALA"  # Calabria

    # Macro zones
    NORTH = "NORD"  # North macrozone (alias for NORD)
    SOUTH = "SUD"  # South macrozone

    # Virtual zones
    BRNN = "BRNN"  # Brindisi
    FOGN = "FOGN"  # Foggia
    MONT = "MONT"  # Montalto
    PRGP = "PRGP"  # Priolo Gargallo
    ROSN = "ROSN"  # Rossano

    # Foreign virtual zones
    AUST = "AUST"  # Austria
    CORS = "CORS"  # Corsica
    COAC = "COAC"  # Corsica AC
    COAD = "COAD"  # Corsica DC
    FRAN = "FRAN"  # France
    GREC = "GREC"  # Greece
    SLOV = "SLOV"  # Slovenia
    SVIZ = "SVIZ"  # Switzerland
    MALT = "MALT"  # Malta

    def __str__(self):
        return self.value



