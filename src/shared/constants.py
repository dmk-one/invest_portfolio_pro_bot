from enum import IntEnum
from typing import List

from pydantic import BaseModel

from src.models import Portfolio


class ROLE(IntEnum):
    CUSTOMER = 1
    ADMIN = 2
    MODERATOR = 3


class ActionType(IntEnum):
    BUY = 0
    SELL = 1


class DetailedPortfolio(BaseModel):
    portfolio: Portfolio
    total_value: float
    average_price: float
    current_price: float
    total_invested_usd_sum: float
    total_current_asset_value: float
    pnl_value: float
    pnl_percent: float


class TotalStats(BaseModel):
    total_invested_usd_sum: float
    total_current_assets_value: float
    pnl_value: float
    pnl_percent: float
    detailed_portfolio_list: List[DetailedPortfolio]
