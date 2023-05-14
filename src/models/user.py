from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, SmallInteger
from sqlalchemy.sql import func

from .base import AbstractORMBaseModel
from src.shared.constants import ROLE


class User(AbstractORMBaseModel):
    __tablename__ = 'user'

    tg_id = Column(BigInteger(), unique=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True, index=True)
    role = Column(SmallInteger(), nullable=False, default=ROLE.CUSTOMER.value)
    first_name = Column(String(255), nullable=False, unique=False)
    last_name = Column(String(255), nullable=True, unique=False)
    phone_number = Column(BigInteger(), nullable=True)
    language_code = Column(String(255), nullable=False)
    added_to_attachment_menu = Column(Boolean, nullable=True, default=False)
    can_join_groups = Column(Boolean, nullable=True, default=False)
    can_read_all_group_messages = Column(Boolean, nullable=True, default=False)
    supports_inline_queries = Column(Boolean, nullable=True, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_activity = Column(DateTime(), onupdate=func.now(), nullable=False)
    updated_at = Column(DateTime(), default=datetime.now(), nullable=True)
    created_at = Column(DateTime(), server_default=func.now(), nullable=False)
