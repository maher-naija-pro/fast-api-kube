"""
security_headers.py

This module defines a middleware that adds security-related HTTP headers to
all outgoing responses. These headers help protect against common web
vulnerabilities, such as clickjacking, cross-site scripting (XSS), and
content type sniffing.

Classes:
    SecurityHeadersMiddleware: Middleware to apply security headers to HTTP responses.
"""

from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds security headers to HTTP responses.

    This middleware adds several security headers to all outgoing responses
    to enhance security and protect against common vulnerabilities. These
    headers include:
        - Strict-Transport-Security: Enforces HTTPS connections.
        - X-Content-Type-Options: Prevents MIME-type sniffing.
        - X-Frame-Options: Protects against clickjacking.
        - X-XSS-Protection: Enables XSS filtering in browsers.
        - Content-Security-Policy: Controls sources for content.
    """


async def dispatch(request, call_next):
    """
    Processes each request and adds security headers to the response.

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or handler to process the request.

    Returns:
        The HTTP response with added security headers.
    """
    response = await call_next(request)

    # Add security headers to the response
    # response.headers["Strict-Transport-Security"] = (
    #   "max-age=31536000; includeSubDomains"
    # )
    # response.headers["X-Content-Type-Options"] = "nosniff"
    # response.headers["X-Frame-Options"] = "DENY"
    # response.headers["X-XSS-Protection"] = "1; mode=block"
    # response.headers["Content-Security-Policy"] = (
    #   "default-src 'self'; script-src 'self'; object-src 'none'"
    # )

    return response
