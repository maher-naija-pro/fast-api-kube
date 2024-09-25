from sqlalchemy import Column, Integer, String,  ForeignKey
from .base import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False)
    queryID = Column(Integer, ForeignKey('query_log.queryID'))