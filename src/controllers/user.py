from datetime import datetime
from aiogram import types

from .portfolio import PortfolioService


class User:
    async def create(
        self,
        tg_id: int,
        username: str,
        first_name: str,
        last_name: str,
        is_bot: bool,
        language_code: str,
        added_to_attachment_menu: bool,
        can_join_groups: bool,
        can_read_all_group_messages: bool,
        supports_inline_queries: bool,
        is_superuser: bool,
        last_activity: datetime,
        registration_date: datetime,
        phone_number: int = ...
    ) -> domain.User:

        user = await self._provider.insert(
            tg_id=tg_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_bot=is_bot,
            language_code=language_code,
            added_to_attachment_menu=added_to_attachment_menu,
            can_join_groups=can_join_groups,
            can_read_all_group_messages=can_read_all_group_messages,
            supports_inline_queries=supports_inline_queries,
            is_superuser=is_superuser,
            last_activity=last_activity,
            registration_date=registration_date,
            phone_number=phone_number
        )

        return user

    async def get(
        self,
        tg_id: int = ...,
        phone_number: int = ...
    ) -> domain.User:

        return await self._provider.get(
            filters={
                'tg_id': tg_id,
                'phone_number': phone_number
            }
        )

    async def add_user_phone(
        self,
        tg_id: int,
        phone_number: int
    ):
        await self._provider.update(
            phone_number=phone_number,
            filters={
                'tg_id': tg_id
            }
        )

    async def update_last_activity(
        self,
        tg_id: int
    ) -> domain.User:
        updated_user = await self._provider.update(
            last_activity=datetime.now(),
            filters={
                'tg_id': tg_id
            }
        )
        return updated_user

    async def update_last_activity_or_create(
        self,
        mess: types.Message
    ):
        try:
            updated_user = await self.update_last_activity(
                tg_id=mess.from_user.id
            )
            updated_user.is_new_user = False

            return updated_user
        except:
            new_user = await self.create(
                tg_id=mess.from_user.id,
                username=mess.from_user.username,
                first_name=mess.from_user.first_name,
                last_name=mess.from_user.last_name,
                is_bot=mess.from_user.is_bot,
                language_code=mess.from_user.language_code,
                added_to_attachment_menu=mess.from_user.added_to_attachment_menu,
                can_join_groups=mess.from_user.can_join_groups,
                can_read_all_group_messages=mess.from_user.can_read_all_group_messages,
                supports_inline_queries=mess.from_user.supports_inline_queries,
                is_superuser=False,
                last_activity=datetime.now(),
                registration_date=datetime.now()
            )
            new_user.is_new_user = True

            return new_user
