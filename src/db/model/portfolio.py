from sqlalchemy import Column, BigInteger, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import AbstractORMBaseModel
from .user import User


class Portfolio(AbstractORMBaseModel):
    __tablename__ = 'portfolio'

    tg_id = Column(BigInteger, ForeignKey(f'{User.__tablename__}.tg_id', ondelete='CASCADE'))
    crypto = Column(String(), nullable=False)

    user = relationship('User', back_populates='portfolio')
    portfolio_log = relationship('PortfolioLog', back_populates='portfolio')
