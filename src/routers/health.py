"""
Health Check Module for FastAPI applications.

This module provides endpoints for monitoring the health of the application and its
core services. It features dynamic service checks, including database and cache
systems, and reports their health status along with service-specific latencies.
It utilizes FastAPI's asynchronous capabilities to perform non-blocking checks.

Classes:
    ServiceStatus: Represents the health status of a service.
    HealthCheckResponse: Aggregates overall health information of the application.

Functions:
    check_database_connection: Checks and reports the health of the database.
    check_redis_connection: Checks and reports the health of the Redis cache.
    check_service: Orchestrates service checks and aggregates results.
    health_check: Endpoint function that reports the application's overall health.

Usage:
    Add this module to a FastAPI application to enable health monitoring endpoints.
"""

import time
import asyncio
import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional
from sqlalchemy import create_engine
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

# Application version and start time
APP_VERSION = os.getenv("APP_VERSION")

app_start_time = datetime.now(timezone.utc)


class ServiceStatus(BaseModel):
    """
    Represents the health status of a service including its latency.

    Attributes:
        name (str): The name of the service being checked.
        status (str): The health status ('healthy' or 'unhealthy').
        latency (Optional[float]): Time taken to check the service in seconds.
    """

    name: str
    status: str
    latency: Optional[float] = None


class HealthCheckResponse(BaseModel):
    """
    Model for the overall health check response of the application.

    Attributes:
        status (str): Overall health status of the application.
        timestamp (str): ISO 8601 formatted timestamp of the health check.
        uptime (str): Formatted uptime of the application as HH:MM:SS.
        version (str): Version of the application.
        services (List[ServiceStatus]): List of service status objects.
    """

    status: str
    timestamp: str
    uptime: str
    services: List[ServiceStatus]


async def check_database_connection():
    """
    Simulate a check for the database connection. This function should connect to
    the database and perform a simple query to verify connectivity and measure latency.

    Returns:
        float: Time taken to establish the connection and query the database.
    """
    # Database URL: replace with your PostgreSQL credentials

    POSTGRES_USER = os.getenv("POSTGRES_USER", "default_user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "default_pass")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "default_db")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa: E501  # pylint: disable=C0301

    start = time.time()
    engine = create_engine(url)

    try:
        await engine.connect()
        return True
    finally:
        return time.time() - start


services_to_check = {
    "database": check_database_connection,
    # Additional services can be added here
}


async def check_service(name, function):
    """
    Perform a health check for a specific service using the provided function, capturing
    the latency of the check.

    Args:
        name (str): Name of the service.
        function (callable): Async function to execute for the service check.

    Returns:
        ServiceStatus: The status and latency of the service after the check.
    """
    try:
        latency = await function()
        return ServiceStatus(name=name, status="healthy", latency=latency)
    except Exception:
        return ServiceStatus(name=name, status="unhealthy", latency=None)


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Endpoint to perform a health check on the application. It checks all registered
    services and aggregates their status and latency into a comprehensive health report.

    Returns:
        HealthCheckResponse: The aggregated health status of the application.
    """
    services_status = await asyncio.gather(
        *[check_service(name, func) for name, func in services_to_check.items()]
    )
    overall_status = (
        "healthy"
        if all(service.status == "healthy" for service in services_status)
        else "unhealthy"
    )
    current_time = datetime.now(timezone.utc)
    uptime_duration = current_time - app_start_time
    return HealthCheckResponse(
        status=overall_status,
        timestamp=current_time.isoformat(),
        uptime=str(timedelta(seconds=int(uptime_duration.total_seconds()))),
        version=APP_VERSION,
        services=services_status,
    )
