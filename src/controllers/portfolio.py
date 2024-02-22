import datetime
from typing import List, Sequence, Optional

from sqlalchemy.sql.expression import select

from src.models import Portfolio, PortfolioAction
from src.shared.schemas import TickerStat, TotalStats
from src.shared.features import get_current_price
from .base import BaseController
from ..shared.constants import ActionType


class PortfolioController(BaseController):
    async def get_total_portfolio_stats(
        self,
        tg_id: int
    ) -> TotalStats:
        stmt = select(
            PortfolioAction,
            Portfolio.crypto_ticker.label('ticker')
        ).outerjoin(
            Portfolio,
            PortfolioAction.portfolio_id == Portfolio.id
        ).where(Portfolio.tg_id == tg_id)

        all_portfolio_action_list = (await self.async_session.execute(stmt)).all()

        all_tickers = set([record[1] for record in all_portfolio_action_list])

        current_prices: dict = await get_current_price(all_tickers)

        tickers_stats = []

        for ticker in all_tickers:
            current_price = current_prices[ticker]

            action_list = [record[0] for record in all_portfolio_action_list if record[1] == ticker]

            total_value: float = 0
            total_invested_usd_sum: float = 0

            for action in action_list:
                if action.action_type.value == 0:
                    total_value += action.value
                    total_invested_usd_sum += action.value * action.by_price
                else:
                    total_value -= action.value
                    total_invested_usd_sum -= action.value * action.by_price
            print('total_invested_usd_sum', total_invested_usd_sum)
            print('total_value', total_value)
            try:
                average_price = total_invested_usd_sum / total_value
            except ZeroDivisionError:
                average_price = 0

            total_current_usd_sum = current_price * total_value

            pnl_value = total_current_usd_sum - total_invested_usd_sum
            pnl_percent = (pnl_value * 100) / total_invested_usd_sum

            ticker_stat = TickerStat(
                tg_id=tg_id,
                crypto=ticker,
                total_value=round(total_value, 2),
                average_price=round(average_price, 2),
                current_price=round(current_price, 2),
                total_invested_usd_sum=round(total_invested_usd_sum, 2),
                total_current_usd_sum=round(total_current_usd_sum, 2),
                pnl_value=round(pnl_value, 2),
                pnl_percent=round(pnl_percent, 2)
            )

            tickers_stats.append(ticker_stat)

        total_invested_usd_sum: float = 0
        total_current_usd_sum: float = 0

        for detailed_portfolio in tickers_stats:
            total_invested_usd_sum += detailed_portfolio.total_invested_usd_sum
            total_current_usd_sum += detailed_portfolio.total_current_usd_sum

        pnl_value = total_current_usd_sum - total_invested_usd_sum
        pnl_percent = (pnl_value * 100) / total_invested_usd_sum

        total_stats = TotalStats(
            total_invested_usd_sum=round(total_invested_usd_sum, 2),
            total_current_usd_sum=round(total_current_usd_sum, 2),
            pnl_value=round(pnl_value, 2),
            pnl_percent=round(pnl_percent, 2),
            tickers_stats=tickers_stats
        )

        return total_stats

    async def get_user_portfolio_tickers(
        self,
        tg_id: int
    ) -> Sequence[List[str]]:
        stmt = select(Portfolio.crypto_ticker).where(Portfolio.tg_id == tg_id)

        return (await self.async_session.scalars(stmt)).all()

    async def create_portfolio_record(
        self,
        tg_id: int,
        crypto_ticker: str,
        action_date: Optional[datetime.datetime],
        action_type: ActionType,
        by_price: float,
        value: float
    ) -> PortfolioAction:
        if not action_date:
            action_date = datetime.datetime.now()

        portfolio_stmt = select(
            Portfolio
        ).where(
            Portfolio.tg_id == tg_id,
            Portfolio.crypto_ticker == crypto_ticker
        )

        portfolio = (await self.async_session.execute(portfolio_stmt)).scalar()

        if not portfolio:
            portfolio = Portfolio(
                tg_id=tg_id,
                crypto_ticker=crypto_ticker
            )

            self.async_session.add(portfolio)
            await self.async_session.flush()

        new_portfolio_action = PortfolioAction(
            portfolio_id=portfolio.id,
            action_date=action_date,
            action_type=action_type,
            by_price=by_price,
            value=value
        )

        self.async_session.add(new_portfolio_action)

        await self.async_session.commit()

        return new_portfolio_action
