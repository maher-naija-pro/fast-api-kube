from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from .base import Base

class QueryLog(Base):
    __tablename__ = "query_log"

    queryID = Column(Integer, primary_key=True, index=True)
    domain = Column(String, nullable=False)
    client_ip = Column(String, nullable=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    addresses = relationship("Address", back_populates="query")

