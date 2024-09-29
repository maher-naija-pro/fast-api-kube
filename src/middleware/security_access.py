from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI, Request
from typing import Callable

class SecurityMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Callable):
        """
        Middleware to add CORS and Trusted Host validation.
        """
        super().__init__(app)

        # Add CORS middleware
        app = CORSMiddleware(
            app=app,
            allow_origins=["*"],  # Allow all origins (can be restricted in production)
            allow_credentials=True,
            allow_methods=["*"],  # Allow all HTTP methods
            allow_headers=["*"],  # Allow all headers
        )

        # Add Trusted Host middleware for host validation
        app = TrustedHostMiddleware(
            app=app,
            allowed_hosts=["*", "localhost"],  # "*" allows any host, restrict in production
        )
        
        # Pass the modified app back to the middleware
        self.app = app

    async def dispatch(self, request: Request, call_next: Callable):
        # Here, you can add custom logic if needed
        response = await call_next(request)
        return response
