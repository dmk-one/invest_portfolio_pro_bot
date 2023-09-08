from typing import List

from sqlalchemy.sql.expression import select

from src.models import Portfolio, PortfolioAction
from src.shared.pydantic_models import DetailedPortfolio, TotalStats
from src.shared.features import get_current_price
from .base import BaseController


class PortfolioController(BaseController):
    async def make_get_stmt(
        self,
        **where
    ):
        where_clause_list = await self._make_where_clause(**where)

        stmt = select(
            Portfolio,
            PortfolioAction
        ).outerjoin(
            PortfolioAction, PortfolioAction.portfolio_id == Portfolio.id
        ).where(*where_clause_list)

        return stmt

    async def _detailed_portfolio_generator(
        self,
        portfolio: Portfolio,
        portfolio_action_list: List[PortfolioAction],
    ) -> DetailedPortfolio:
        current_price = await get_current_price()

        total_value: float = 0
        total_invested_usd_sum: float = 0

        for portfolio_action in portfolio_action_list:
            if portfolio_action.action_type.value == 0:
                total_value += portfolio_action.value
                total_invested_usd_sum += portfolio_action.value * portfolio_action.by_price
            else:
                total_value -= portfolio_action.value
                total_invested_usd_sum -= portfolio_action.value * portfolio_action.by_price

        average_price = total_invested_usd_sum / total_value

        total_current_crypto_value = current_price * total_value

        pnl_value = total_current_crypto_value - total_invested_usd_sum
        pnl_percent = (pnl_value * 100) / total_invested_usd_sum

        detailed_portfolio = DetailedPortfolio(
            tg_id=portfolio.tg_id,
            crypto=portfolio.crypto,
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
            portfolio, portfolio_action_list = portfolio_record[0], portfolio_record[1:]

            detailed_portfolio = await self._detailed_portfolio_generator(
                portfolio=portfolio,
                portfolio_action_list=portfolio_action_list
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
