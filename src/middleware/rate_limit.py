"""
rate_limit_middleware.py

This module defines a global rate-limiting middleware for FastAPI applications.

The middleware limits the number of requests that can be made globally to the
application within a defined time window. If the number of requests exceeds the
configured limit, the middleware returns an HTTP 429 (Too Many Requests) error.

Environment Variables:
    RATE_LIMIT_REQUESTS (int): The maximum number of requests allowed in the
        rate limit window. Defaults to 10.
    RATE_LIMIT_WINDOW (int): The length of the time window (in seconds) for
        which the rate limit applies. Defaults to 60 seconds.

Classes:
    GlobalRateLimitMiddleware: Implements the global rate-limiting logic using
    an in-memory counter to track requests and enforce limits.
"""

# rate_limit_middleware.py
import os
import time

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware

# Load rate-limiting settings from environment variables
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "1000"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "200"))


# Middleware for global rate-limiting
class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    """
    A middleware to enforce global rate-limiting for all incoming requests.

    This middleware counts the number of incoming requests and ensures that
    the requests do not exceed the specified rate limit (requests per time window).
    If the limit is exceeded, an HTTP 429 (Too Many Requests) error is raised.

    Attributes:
        global_request_count (int): The number of requests
        window_start_time (float): The start time of the current time window
        rate_limit_requests (int): The maximum number of requests allowed
        rate_limit_window (int): The length of the time window in seconds.
    """

    def __init__(self, app):
        """
        Initializes the GlobalRateLimitMiddleware.

        Args:
            app (ASGI app): The FastAPI
        """
        super().__init__(app)
        # Time window in seconds
        self.global_request_count = 0  # Global request count (in-memory)
        self.window_start_time = time.time()  # When the current window started
        self.rate_limit_requests = RATE_LIMIT_REQUESTS
        self.rate_limit_window = RATE_LIMIT_WINDOW

    async def dispatch(self, request: Request, call_next):
        """
        Processes incoming requests and applies rate-limiting.

        If the number of requests within the current time window exceeds the
        rate limit, an HTTPException with status 429 is raised. Otherwise, the
        request is processed as usual.

        Args:
            request (Request): The incoming HTTP request.
            call_next (function): A function that processes the request returns a resp.

        Returns:
            Response: The HTTP response after the request has been processed.

        Raises:
            HTTPException: If the global rate limit has been exceeded, an exception
            with status code 429 is raised.
        """
        current_time = time.time()

        # Check if the current window has expired
        if current_time - self.window_start_time > self.rate_limit_window:
            # Reset the counter and window start time
            self.global_request_count = 0
            self.window_start_time = current_time

        # Check if the global request limit has been reached
        if self.global_request_count >= self.rate_limit_requests:
            raise HTTPException(status_code=429, detail="Global rate limit exceeded")

        # Increment the global request count
        self.global_request_count += 1

        # Proceed to process the request
        response = await call_next(request)

        return response
