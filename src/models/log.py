"""
models/log.py

This module defines the `QueryLog` model for storing domain query logs in the
database. Each log contains the queried domain, the client's IP address, and
the timestamp when the query was made.
"""

from sqlalchemy import Column, DateTime, Integer, String, func

from .base import Base


class QueryLog(Base):
    """
    SQLAlchemy model for the 'query_log' table.

    This model stores logs of domain queries, including the queried domain,
    client IP address (if available), and the time the query was made.

    Attributes:
        queryID (int): The primary key ID of the query log.
        domain (str): The domain that was queried.
        client_ip (str): The IP address of the client making the query.
        created_time (datetime): The timestamp when the query was made.
    """

    __tablename__ = "query_log"

    queryID = Column(Integer, primary_key=True, index=True)
    domain = Column(String, nullable=False)
    client_ip = Column(String, nullable=True)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
