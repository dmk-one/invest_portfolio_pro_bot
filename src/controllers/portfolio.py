from typing import List, Optional

from sqlalchemy.orm import join
from sqlalchemy.sql.expression import select, update, delete

from src.models import Portfolio, PortfolioLog
from src.shared.constants import DetailedPortfolio, TotalStats
from src.shared.features import get_current_price
from .base import BaseController
from .portfolio_log import PortfolioLogController


class PortfolioController(BaseController):
    model = Portfolio

    # _portfolio_log_controller = PortfolioLogController()

    async def make_get_stmt(
        self,
        **where
    ):
        where_clause_list = await self._make_where_clause(**where)

        stmt = select(
            self.model,
            PortfolioLog
        ).outerjoin(
            PortfolioLog, PortfolioLog.portfolio_id == self.model.id
        ).where(*where_clause_list)

        return stmt

    async def _detailed_portfolio_generator(
        self,
        portfolio: Portfolio,
        portfolio_log_list: List[PortfolioLog],
    ) -> DetailedPortfolio:
        current_price = get_current_price()

        total_value: float = 0
        total_invested_usd_sum: float = 0

        for portfolio_log in portfolio_log_list:
            if portfolio_log.action_type.value == 0:
                total_value += portfolio_log.value
                total_invested_usd_sum += portfolio_log.value * portfolio_log.by_price
            else:
                total_value -= portfolio_log.value
                total_invested_usd_sum -= portfolio_log.value * portfolio_log.by_price

        average_price = total_invested_usd_sum / total_value

        total_current_crypto_value = current_price * total_value

        pnl_value = total_current_crypto_value - total_invested_usd_sum
        pnl_percent = (pnl_value * 100) / total_invested_usd_sum

        detailed_portfolio = DetailedPortfolio(
            portfolio=portfolio,
            total_value=total_value,
            average_price=average_price,
            current_price=current_price,
            total_invested_usd_sum=total_invested_usd_sum,
            total_current_crypto_value=total_current_crypto_value,
            pnl_value=pnl_value,
            pnl_percent=pnl_percent
        )

        return detailed_portfolio

    async def get_detailed_portfolio(
        self,
        portfolio_id_list: List[int] = None
    ) -> List[DetailedPortfolio]:
        if portfolio_id_list is None:
            portfolio_records = await self.get_all()
        else:
            portfolio_records = await self.get_all(
                id__in=portfolio_id_list
            )

        detailed_portfolio_list = []

        for portfolio_record in portfolio_records:
            portfolio, portfolio_log_list = portfolio_record[0], portfolio_record[1:]

            detailed_portfolio = await self._detailed_portfolio_generator(
                portfolio=portfolio,
                portfolio_log_list=portfolio_log_list
            )

            detailed_portfolio_list.append(detailed_portfolio)

        return detailed_portfolio_list

    async def get_total_stats(
        self,
        portfolio_id_list: List[int] = None
    ) -> TotalStats:
        detailed_portfolio_list = await self.get_detailed_portfolio(portfolio_id_list)

        total_invested_usd_sum: float = 0
        total_current_cryptos_value: float = 0

        for detailed_portfolio in detailed_portfolio_list:
            total_invested_usd_sum += detailed_portfolio.total_invested_usd_sum
            total_current_cryptos_value += detailed_portfolio.total_invested_usd_sum

        pnl_value = total_current_cryptos_value - total_invested_usd_sum
        pnl_percent = (pnl_value * 100) / total_invested_usd_sum

        total_stats = TotalStats(
            total_invested_usd_sum=total_invested_usd_sum,
            total_current_cryptos_value=total_current_cryptos_value,
            pnl_value=pnl_value,
            pnl_percent=pnl_percent,
            detailed_portfolio_list=detailed_portfolio_list
        )

        return total_stats
