from typing import List
from pydantic import BaseModel


class DetailedPortfolio(BaseModel):
    tg_id: int
    crypto: str
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
