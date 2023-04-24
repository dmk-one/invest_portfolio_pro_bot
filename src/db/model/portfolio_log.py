from sqlalchemy import Column, BigInteger, ForeignKey, DateTime, SmallInteger, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from settings import settings
from .base import AbstractORMBaseModel
from .crypto import Portfolio


class PortfolioLog(AbstractORMBaseModel):
    __tablename__ = 'portfolio_log'

    portfolio_id = Column(BigInteger, ForeignKey(f'{Portfolio.__tablename__}.id', ondelete='CASCADE'))
    action_date = Column(DateTime(timezone=settings.USE_TIMEZONE), server_default=func.now(), nullable=False)
    action_type = Column(SmallInteger(), nullable=False)
    by_price = Column(Float(), nullable=False)
    value = Column(Float(), nullable=False)

    portfolio = relationship('Portfolio', back_populates='portfolio_log')
