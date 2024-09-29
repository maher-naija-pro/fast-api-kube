"""
Health check endpoint for FastAPI.

This module defines a simple health check endpoint
that returns the status of the application. It uses
FastAPI's `APIRouter` for routing and Pydantic models
for structuring the response.

Classes:
    HealthCheckResponse: Pydantic model representing
    the health check response.

Routes:
    /health: A GET endpoint that returns the health status
    of the application.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="")


# Pydantic response model for health check
class HealthCheckResponse(BaseModel):
    """
    Pydantic model for the health check response.

    Attributes:
        status (str): A string representing the health status.
    """

    status: str


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    """
    Health check endpoint.

    This endpoint returns the health status of the application. It can be
    used by external systems to monitor the application's status.

    Returns:
        dict: A dictionary with the health status of the application.
    """
    return {"status": "healthy"}
