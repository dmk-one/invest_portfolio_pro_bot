from datetime import datetime

from sqlalchemy import select, update

from .base import BaseController
from src.models import User
from ..shared.constants import ROLE


class UserController(BaseController):
    async def get_user(self, tg_id) -> User:
        stmt = select(User).where(User.tg_id == tg_id)

        return (await self.async_session.execute(stmt)).scalar()

    async def create_user(
        self,
        tg_id: int,
        username: str,
        first_name: str,
        language_code: str,
        role: int = ROLE.CUSTOMER.value,
        last_name: str = None,
        added_to_attachment_menu: bool = False,
        can_join_groups: bool = False,
        can_read_all_group_messages: bool = False,
        supports_inline_queries: bool = False,
        is_superuser: bool = False,
        phone_number: int = None
    ) -> User:
        new_user = User(
            tg_id=tg_id,
            username=username,
            role=role,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            added_to_attachment_menu=added_to_attachment_menu,
            can_join_groups=can_join_groups,
            can_read_all_group_messages=can_read_all_group_messages,
            supports_inline_queries=supports_inline_queries,
            is_superuser=is_superuser,
            phone_number=phone_number,
            last_activity=datetime.now()
        )

        self.async_session.add(new_user)

        return await self.get_user(tg_id)

    async def update_user(
        self,
        tg_id: int,
        **kwargs
    ) -> User:
        stmt = update(User).where(User.tg_id == tg_id).values(**kwargs)

        await self.async_session.execute(stmt)

        return await self.get_user(tg_id)

