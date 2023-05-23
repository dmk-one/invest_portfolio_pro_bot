from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select, update, delete

from src.exceptions.shared import OperatorRequiredException
from src.models import ORMBaseModel


class BaseController:
    async_session: AsyncSession = None
    model: ORMBaseModel = None

    async def _make_where_clause(
        self,
        **where
    ):
        where_clause_list = []

        for column_with_operator, value in where.items():
            try:
                column, operator = column_with_operator.split('__')

                where_clause = None
                if operator == 'e':
                    where_clause = getattr(self.model, column) == value
                if operator == 'not_e':
                    where_clause = getattr(self.model, column) != value
                if operator == 'in':
                    where_clause = getattr(self.model, column).in_(value)
                if operator == 'not_in':
                    where_clause = getattr(self.model, column).not_in(value)

                where_clause_list.append(where_clause)
            except ValueError:
                OperatorRequiredException()

        return where_clause_list

    async def make_get_stmt(
        self,
        **where
    ):
        where_clause_list = await self._make_where_clause(**where)

        return select(self.model).where(*where_clause_list)

    async def get_first(
        self,
        **where
    ):
        get_stmt = await self.make_get_stmt(**where)

        return (await self.async_session.execute(get_stmt)).first()

    async def get_all(
        self,
        **where
    ):
        get_stmt = await self.make_get_stmt(**where)

        return (await self.async_session.execute(get_stmt)).all()

    async def create(
        self,
        **kwargs
    ):
        new_obj = self.model(
            **kwargs
        )

        self.async_session.add(new_obj)
        await self.async_session.flush()

        return await self.get_first(id__e=new_obj.id)

    async def update(
        self,
        where: dict,
        **values
    ):
        where_clause_list = await self._make_where_clause(**where)

        stmt = update(self.model).where(*where_clause_list).values(**values)

        await self.async_session.execute(stmt)

        return await self.get_all(**where)

    async def delete(
        self,
        **where
    ):
        where_clause_list = await self._make_where_clause(**where)
        stmt = delete(self.model).where(*where_clause_list)

        await self.async_session.execute(stmt)
