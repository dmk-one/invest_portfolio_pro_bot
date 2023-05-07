from typing import Dict, List
from uuid import uuid4

from sqlalchemy import Column, BigInteger, UUID, select
from sqlalchemy.orm import declarative_base

# from src.sessions import a_session


ORMBaseModel = declarative_base()


class AbstractORMBaseModel(ORMBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)

    # @classmethod
    # async def get_record(
    #     cls,
    #     equal_list: List[Dict],
    #     not_equal_list: List[Dict],
    #     in_list: List[Dict]
    # ):
    #     stmt = select(cls)
    #     res = await a_session.execute(stmt)
    #     print(res.fetchall())
