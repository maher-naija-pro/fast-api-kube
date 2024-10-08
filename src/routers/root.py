"""
Root endpoint for FastAPI.

This module defines the root ("/") endpoint for the FastAPI application.
 It logs
the incoming requests, tracks request metrics using Prometheus, and
returns basic application information including version and Kubernetes
 environment detection.

Metrics:
    REQUEST_COUNTER_ROOT: A counter for the total number of requests to the
    root endpoint.
    ERROR_COUNTER_ROOT: A counter for the total number of errors encountered
    in the root endpoint.
    REQUEST_LATENCY_ROOT: A histogram for tracking request latency in seconds
     for the root endpoint.

Routes:
    /: A GET endpoint that returns basic app information and environment details.
"""

import os
from time import time

from fastapi import APIRouter, Request
from prometheus_client import Counter, Histogram

from helpers.log.logger import init_log

router = APIRouter()

# init logger
logger = init_log()

# Define Prometheus root
REQUEST_COUNTER_ROOT = Counter(
    "root_app_requests_total", "Total number of requests of endpoint root"
)
ERROR_COUNTER_ROOT = Counter(
    "root_app_request_errors_total", "Total number of request errors of endpoint root"
)
REQUEST_LATENCY_ROOT = Histogram(
    "root_app_request_latency_seconds", "Request latency in seconds of endpoint root"
)


@router.get("/")
async def root(request: Request):
    """
    Root endpoint for the FastAPI application.

    This endpoint returns metadata about the application including the version,
    current time, and whether the application is running in a Kubernetes
    environment. Metrics for request latency and request count are also recorded.

    Args:
        request (Request): The incoming HTTP request object.

    Returns:
        dict: A dictionary with the version, current time (in Unix epoch),
        and a flag indicating if the app is in a Kubernetes environment.
    """
    start_time = time()

    logger.info(f"Root / requested from {request.client.host}")

    is_k8s = "KUBERNETES_SERVICE_HOST" in os.environ
    duration = time() - start_time
    REQUEST_LATENCY_ROOT.observe(duration)
    REQUEST_COUNTER_ROOT.inc()

    logger.info(f"Request completed in {duration:.4f} seconds")
    return {"version": "0.1.0", "date": int(time()), "kubernetes": is_k8s}
    # Measure request latency
