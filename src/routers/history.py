"""
History endpoint for FastAPI.

This module defines an endpoint for retrieving the query
history from the database.It also integrates with Prometheus
for tracking request metrics and logs activity
using a custom logger.

Classes:
    QueryLogResponse: Pydantic model representing a query log entry.

Routes:
    /history: A GET endpoint that returns the last 20 query log entries.
"""

import sys
from datetime import datetime
from time import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from prometheus_client import Counter, Histogram
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from db.database import get_db
from helpers.log.logger import init_log
from models.log import QueryLog

sys.path = ["", ".."] + sys.path[1:]
sys.path.append("src")

router = APIRouter()
logger = init_log()

# Define Prometheus metrics
REQUEST_COUNTER_HISTORY = Counter(
    "history_app_requests_total", "Total number of requests on history endpoint"
)
ERROR_COUNTER_HISTORY = Counter(
    "history_app_request_errors_total",
    "Total number of request errors on history endpoint",
)
REQUEST_LATENCY_HISTORY = Histogram(
    "history_app_request_latency_seconds",
    "Request latency in seconds on history endpoint",
)


# Pydantic model for each query log entry
class QueryLogResponse(BaseModel):
    """
    Pydantic model for a query log entry.

    Attributes:
        queryID (int): The unique ID of the query.
        domain (str): The domain that was queried.
        client_ip (str): The IP address of the client making the query.
        created_time (datetime): Timestamp when the query was created.
    """

    queryID: int = Field(..., description="The unique ID of the query")
    domain: str = Field(..., description="The domain queried")
    client_ip: str = Field(
        ..., description="The IP address of the client making the query"
    )
    created_time: datetime = Field(
        ..., description="Timestamp when the query was created"
    )

    class Config:
        """
        Configuration for the Pydantic model.

        Allows the model to be populated from SQLAlchemy ORM model attributes.
        """

        from_attributes = True  # Enable compatibility with SQLAlchemy models


@router.get("/history", response_model=List[QueryLogResponse])
def get_history(db: Session = Depends(get_db)):
    """
    Retrieves the latest 20 query logs from the database.

    This endpoint queries the database for the most recent 20 query logs
    and returns them. It also tracks request latency and errors using Prometheus.

    Args:
        db (Session): The SQLAlchemy session used to interact with the database.

    Returns:
        List[QueryLogResponse]: A list of the latest 20 query logs.

    Raises:
        HTTPException: If no records are found (404) or in case of a server error (500).
    """
    start_time = time()  # Track the start time for latency measurement
    # Increment the Prometheus counter
    REQUEST_COUNTER_HISTORY.inc()

    # Log the request
    logger.info("/history requested")

    try:
        # Fetch the history and handle potential errors
        history = (
            db.query(QueryLog).order_by(QueryLog.created_time.desc()).limit(20).all()
        )

        if not history:
            logger.warning("No history found")
            raise HTTPException(status_code=404, detail="No history records found")
        # Log success with latency
        request_latency = time() - start_time
        REQUEST_LATENCY_HISTORY.observe(request_latency)
        logger.info(f"History served in {request_latency:.4f} seconds")
        return history

    except Exception as e:
        # Log the error and increment error counter
        ERROR_COUNTER_HISTORY.inc()
        # Log the error and return an appropriate response
        logger.error(f"Failed to fetch history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error") from e
