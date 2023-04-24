from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from settings import settings
from .base import AbstractORMBaseModel


class User(AbstractORMBaseModel):
    __tablename__ = 'user'

    tg_id = Column(BigInteger(), unique=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True, index=True)
    first_name = Column(String(255), nullable=False, unique=True)
    last_name = Column(String(255), nullable=True, unique=True)
    phone_number = Column(BigInteger(), nullable=True)
    is_bot = Column(Boolean, nullable=False, default=False)
    language_code = Column(String(255), nullable=False)
    added_to_attachment_menu = Column(Boolean, nullable=True, default=False)
    can_join_groups = Column(Boolean, nullable=True, default=False)
    can_read_all_group_messages = Column(Boolean, nullable=True, default=False)
    supports_inline_queries = Column(Boolean, nullable=True, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)
    last_activity = Column(DateTime(timezone=settings.USE_TIMEZONE), onupdate=func.now(), nullable=False)
    registration_date = Column(DateTime(timezone=settings.USE_TIMEZONE), server_default=func.now(), nullable=False)

    crypto = relationship('Crypto', back_populates='user')
