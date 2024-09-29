# rate_limit_middleware.py
import os
import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware



# Load rate-limiting settings from environment variables
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", 10))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", 60))


# Middleware for global rate-limiting
class GlobalRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Time window in seconds
        self.global_request_count = 0                            # Global request count (in-memory)
        self.window_start_time = time.time()                     # When the current window started
        self.rate_limit_requests = RATE_LIMIT_REQUESTS
        self.rate_limit_window = RATE_LIMIT_WINDOW
    async def dispatch(self, request: Request, call_next):
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
