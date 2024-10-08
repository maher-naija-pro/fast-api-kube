"""
security_middleware.py

This module defines security-related middleware for FastAPI applications.

The SecurityMiddleware class adds two layers of security:
    - CORS validation to manage cross-origin requests.
    - Trusted host validation to limit accepted hosts.

Classes:
    SecurityMiddleware: Middleware to apply CORS and host validation.
"""

from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add CORS and Trusted Host validation.

    This middleware applies CORS policies, allowing cross-origin requests
    from any origin. Additionally, it restricts the hosts that can access
    the FastAPI application based on predefined rules.
    """

    def __init__(self, app: Callable):
        """
        Initializes the SecurityMiddleware.

        Args:
            app (Callable): The ASGI application instance to wrap.
        """
        super().__init__(app)

        # Add CORS middleware
        app = CORSMiddleware(
            app=app,
            allow_origins=[
                "http://localhost",
                "http://localhost:3000",
            ],  # Allow all origins (can be restricted in production)
            allow_credentials=True,
            allow_methods=["*"],  # Allow all HTTP methods
            allow_headers=["*"],  # Allow all headers
        )

        # Add Trusted Host middleware for host validation
        app = TrustedHostMiddleware(
            app=app,
            allowed_hosts=[
                "*",
                "localhost",
            ],  # "*" allows any host, restrict in production
        )

        # Pass the modified app back to the middleware
        self.app = app

    async def dispatch(self, request: Request, call_next: Callable):
        """
        Handles incoming requests and applies security rules.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or handler to call.

        Returns:
            Response: The HTTP response after applying security rules.
        """
        # Process the request and get response from the next middleware or endpoint
        response = await call_next(request)

        # Set security headers to protect against common attacks
        response.headers["Sec-Fetch-Dest"] = "document"
        response.headers["Sec-Fetch-Mode"] = "navigate"
        response.headers["Sec-Fetch-Site"] = "same-origin"
        response.headers["Sec-Fetch-User"] = "?1"

        # Prevent caching to ensure data privacy
        response.headers["Cache-Control"] = "no-store"

        # Prevent clickjacking by disallowing iframes
        response.headers["X-Frame-Options"] = "DENY"

        # Hide server software information
        response.headers["server"] = "none"

        # Suppress date and last-modified headers for timestamp privacy
        response.headers["date"] = "none"
        response.headers["last-modified"] = "none"

        # Enforce HTTPS with Strict-Transport-Security
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

        # Prevent MIME sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Basic XSS protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Limit scripts and objects to trusted sources
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; object-src 'none'"
        )

        # Return the response with security and privacy headers
        return response
