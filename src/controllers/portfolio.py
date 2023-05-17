from sqlalchemy.sql.expression import select, update, delete

from src.models import Portfolio
from .base import BaseController


class PortfolioController(BaseController):
    model = Portfolio

    async def _detailed_portfolio_generator(
        self,
        portfolio: domain.Portfolio,
        portfolio_log_list: List[domain.PortfolioLog],
        current_price: float
    ) -> domain.DetailedPortfolio:

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

        detailed_portfolio = domain.DetailedPortfolio(
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
        portfolio: Portfolio,
        current_price: float
    ) -> domain.DetailedPortfolio:

        portfolio_log_list = await self._s_portfolio_log.select(
            filters={
                'portfolio_id__e': portfolio.id
            }
        )

        detailed_portfolio = await self._detailed_portfolio_generator(
            portfolio=portfolio,
            portfolio_log_list=[portfolio_log for portfolio_log in portfolio_log_list.items],
            current_price=current_price
        )

        return detailed_portfolio

    async def select_detailed_portfolio(
        self,
        portfolio_list_with_current_price: Dict[domain.Portfolio, float]
    ) -> domain.DetailedPortfolioList:

        portfolio_log_list = await self._s_portfolio_log.select(
            filters={
                'portfolio_id__in': [portfolio.id for portfolio in portfolio_list_with_current_price.keys()]
            }
        )

        detailed_portfolio_list = domain.DetailedPortfolioList()

        for portfolio, current_price in portfolio_list_with_current_price.items():
            detailed_portfolio = await self._detailed_portfolio_generator(
                portfolio=portfolio,
                portfolio_log_list=[portfolio_log for portfolio_log in portfolio_log_list.items
                                    if portfolio_log.portfolio.id == portfolio.id],
                current_price=current_price
            )

            detailed_portfolio_list.items.append(detailed_portfolio)

        return detailed_portfolio_list

    async def get_total_stats(
        self,
        portfolio_list_with_current_price: Dict[domain.Portfolio, float]
    ) -> domain.TotalStats:

        detailed_portfolio_list = await self.select_detailed_portfolio(portfolio_list_with_current_price)

        total_invested_usd_sum: float = 0
        total_current_cryptos_value: float = 0

        for detailed_portfolio in detailed_portfolio_list.items:
            total_invested_usd_sum += detailed_portfolio.total_invested_usd_sum
            total_current_cryptos_value += detailed_portfolio.total_invested_usd_sum

        pnl_value = total_current_cryptos_value - total_invested_usd_sum
        pnl_percent = (pnl_value * 100) / total_invested_usd_sum

        total_stats = domain.TotalStats(
            total_invested_usd_sum=total_invested_usd_sum,
            total_current_cryptos_value=total_current_cryptos_value,
            pnl_value=pnl_value,
            pnl_percent=pnl_percent,
            detailed_portfolio_list=detailed_portfolio_list
        )

        return total_stats
