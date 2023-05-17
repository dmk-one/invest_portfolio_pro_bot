from datetime import datetime

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession

from src.sessions import async_engine
from src.controllers import BaseController, UserController


class ResourceMiddleware(BaseMiddleware):
    """
    Middleware for providing db-connection resource
    """

    # async def _cleanup(self, data: dict):
    #     if "async_session" in data:
    #         session: AsyncSession = data["async_session"]
    #         await session.commit()
    #         await session.close()

    async def _update_last_activity_or_create(self, from_user_data: types.User):
        user_controller = UserController()
        user = await user_controller.get(tg_id=from_user_data.id)

        if user is None:
            new_user = await user_controller.create(
                tg_id=from_user_data.id,
                username=from_user_data.username,
                first_name=from_user_data.first_name,
                language_code=from_user_data.language_code,
                last_name=from_user_data.last_name,
                added_to_attachment_menu=from_user_data.added_to_attachment_menu,
                can_join_groups=from_user_data.can_join_groups,
                can_read_all_group_messages=from_user_data.can_read_all_group_messages,
                supports_inline_queries=from_user_data.supports_inline_queries,
                last_activity=datetime.now()
            )

            return new_user

        updated_user = await user_controller.update(
            where={'tg_id': from_user_data.id},
            last_activity=datetime.now()
        )

        return updated_user

    async def _cleanup(self):
        session: AsyncSession = BaseController.async_session
        await session.commit()
        await session.close()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        async_session = AsyncSession(async_engine)
        BaseController.async_session = async_session

        user = await self._update_last_activity_or_create(from_user_data=message.from_user)
        data['user'] = user

        # data['async_session'] = async_session
        return data

    # async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
    #     resources = await self._provide_resources()
    #     data.update(resources)
    #
    #     return data

    # async def on_post_process_callback_query(self, query: types.CallbackQuery, data_from_handler: list, data: dict):
    #     await self._cleanup(data)

    async def on_post_process_message(self, message: types.Message, data_from_handler: list, data: dict):
        await self._cleanup()
