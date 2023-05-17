from sqlalchemy.sql.expression import select, update, delete

from src.models import PortfolioLog
from .base import BaseController


class PortfolioController(BaseController):
    async def get(
            self,
            tg_id: int
    ) -> PortfolioLog:
        stmt = select(PortfolioLog).where(Portfolio.tg_id == tg_id)

        return (await self.async_session.execute(stmt)).scalar()

    async def create(
            self,
            tg_id: int,
            crypto: str
    ) -> Portfolio:
        new_portfolio_obj = Portfolio(
            tg_id=tg_id,
            crypto=crypto
        )

        self.async_session.add(new_portfolio_obj)

        return await self.get(tg_id)

    async def update(
            self,
            tg_id: int,
            crypto: str
    ) -> Portfolio:
        stmt = update(Portfolio).where(Portfolio.tg_id == tg_id).values(crypto=crypto)

        await self.async_session.execute(stmt)

        return await self.get(tg_id)

    async def delete(
            self,
            tg_id: int
    ):
        stmt = delete(Portfolio).where(Portfolio.tg_id == tg_id)

        await self.async_session.execute(stmt)