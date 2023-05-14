from uuid import uuid4

from sqlalchemy import Column, BigInteger, UUID
from sqlalchemy.orm import declarative_base


ORMBaseModel = declarative_base()


class AbstractORMBaseModel(ORMBaseModel):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
