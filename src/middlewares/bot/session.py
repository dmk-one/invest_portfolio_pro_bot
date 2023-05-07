from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.sessions import async_engine


class ResourceMiddleware(BaseMiddleware):
    """
    Middleware for providing db-connection resource
    """

    async def _cleanup(self, data: dict):
        if "async_session" in data:
            session: AsyncSession = data["async_session"]
            await session.commit()
            await session.close()

    async def on_pre_process_message(self, update: types.Message, data: dict):
        async_session = AsyncSession(async_engine)
        data['async_session'] = async_session

        return data

    # async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
    #     resources = await self._provide_resources()
    #     data.update(resources)
    #
    #     return data

    # async def on_post_process_callback_query(self, query: types.CallbackQuery, data_from_handler: list, data: dict):
    #     await self._cleanup(data)

    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        await self._cleanup(data)




