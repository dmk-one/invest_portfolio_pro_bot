from typing import List
from pydantic import BaseModel


class TickerStat(BaseModel):
    tg_id: int
    crypto: str
    total_value: float
    average_price: float
    current_price: float
    total_invested_usd_sum: float
    total_current_usd_sum: float
    pnl_value: float
    pnl_percent: float


class TotalStats(BaseModel):
    total_invested_usd_sum: float
    total_current_usd_sum: float
    pnl_value: float
    pnl_percent: float
    tickers_stats: List[TickerStat]
