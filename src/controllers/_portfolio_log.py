from datetime import datetime

from src.database.provider.portfolio_log import PortfolioLogProvider
from src.database.serializer import domain


class PortfolioLogService:

    _provider: PortfolioLogProvider

    def __init__(self):
        self._provider = PortfolioLogProvider()

    async def get(
        self,
        id: int
    ) -> domain.PortfolioLog:

        return await self._provider.get(
            filters={
                'id__e': id
            }
        )

    async def select(
        self,
        filters: dict = {},
        order_by: str = ...,
        order_reversed: bool = ...,
        limit: int = None,
        offset: int = 0,
    ) -> domain.PortfolioLogList:

        return await self._provider.select(
            order_by=order_by,
            order_reversed=order_reversed,
            limit=limit,
            offset=offset,
            filters=filters
        )

    async def create(
        self,
        portfolio_id: int,
        action_type: int,
        by_price: float,
        value: float
    ) -> domain.PortfolioLog:

        action_date = datetime.now()

        portfolio_log = await self._provider.insert(
            portfolio_id=portfolio_id,
            action_type=action_type,
            by_price=by_price,
            value=value,
            action_date=action_date
        )

        return portfolio_log

    async def update(
        self,
        id: int,
        portfolio_id: int,
        action_type: int,
        by_price: float,
        value: float
    ) -> domain.PortfolioLog:

        return await self._provider.update(
            portfolio_id=portfolio_id,
            action_type=action_type,
            by_price=by_price,
            value=value,
            id__e=id
        )

    async def delete(
        self,
        id: int
    ):

        return await self._provider.delete(
            filters={
                'id__e': id
            }
        )
