from sqlalchemy.ext.asyncio import AsyncSession


class BaseController:
    async_session: AsyncSession = None
