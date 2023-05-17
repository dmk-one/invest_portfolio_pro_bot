from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, update, delete

from src.models import ORMBaseModel


class BaseController:
    async_session: AsyncSession = None
    model: ORMBaseModel = None

    async def get(
        self,
        **where
    ) -> model:
        where_clause = [getattr(self.model, key) == value for key, value in where.items()]
        stmt = select(self.model).where(*where_clause)

        return (await self.async_session.execute(stmt)).scalar()

    async def create(
        self,
        **kwargs
    ) -> model:
        new_obj = self.model(
            **kwargs
        )

        self.async_session.add(new_obj)
        await self.async_session.flush()

        return await self.get(id=new_obj.id)

    async def update(
        self,
        where: dict,
        **values
    ) -> model:
        where_clause = [getattr(self.model, key) == value for key, value in where.items()]

        stmt = update(self.model).where(*where_clause).values(**values)

        await self.async_session.execute(stmt)

        return await self.get(**where)

    async def delete(
        self,
        **where
    ):
        where_clause = [getattr(self.model, key) == value for key, value in where.items()]
        stmt = delete(self.model).where(*where_clause)

        await self.async_session.execute(stmt)
