from uuid import uuid4
from datetime import datetime

from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, SmallInteger, UUID, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

from src.shared.constants import ROLE


ORMBaseModel = declarative_base()


class AbstractORMBaseModel(ORMBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)


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


class Portfolio(AbstractORMBaseModel):
    __tablename__ = 'portfolio'

    tg_id = Column(BigInteger, ForeignKey(f'{User.__tablename__}.tg_id', ondelete='CASCADE'))
    crypto_ticker = Column(String(), nullable=False)


class PortfolioAction(AbstractORMBaseModel):
    __tablename__ = 'portfolio_action'

    portfolio_id = Column(BigInteger, ForeignKey(f'{Portfolio.__tablename__}.id', ondelete='CASCADE'))
    action_date = Column(DateTime(), server_default=func.now(), nullable=False)
    action_type = Column(SmallInteger(), nullable=False)
    by_price = Column(Float(), nullable=False)
    value = Column(Float(), nullable=False)



