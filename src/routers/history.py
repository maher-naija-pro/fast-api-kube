from fastapi import APIRouter,Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from helpers.log.logger import init_log
from db.database import get_db
from src.models.log import QueryLog
from prometheus_client import Counter

import sys

sys.path = ["", ".."] + sys.path[1:]
sys.path.append("src")

router = APIRouter()
logger=init_log()

# Define Prometheus metrics
REQUEST_COUNTER_HISTORY = Counter('history_app_requests_total', 'Total number of requests on history endpoint')

# Pydantic model for each query log entry
class QueryLogResponse(BaseModel):
    queryID: int = Field(..., description="The unique ID of the query")
    domain: str = Field(..., description="The domain queried")
    client_ip: str = Field(..., description="The IP address of the client making the query")
    created_time: datetime = Field(..., description="Timestamp when the query was created")

    class Config:
        from_attributes = True  # Enable compatibility with SQLAlchemy models

@router.get("/history",response_model=List[QueryLogResponse])
def get_history(db: Session = Depends(get_db)):
    # Increment the Prometheus counter
    REQUEST_COUNTER_HISTORY.inc()

    # Log the request
    logger.info("/history requested")

    try:
        # Fetch the history and handle potential errors
        history = db.query(QueryLog).order_by(QueryLog.created_time.desc()).limit(20).all()

        if not history:
            logger.warning("No history found")
            raise HTTPException(status_code=404, detail="No history records found")

        return history

    except Exception as e:
        # Log the error and return an appropriate response
        logger.error(f"Failed to fetch history: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")





