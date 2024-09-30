"""
main.py

This module initializes and configures a FastAPI application with custom
middleware, routers, and a graceful shutdown mechanism. It includes:
    - HTTPS redirection middleware for production environments.
    - Global rate-limiting middleware.
    - Security middleware for security headers and access restrictions.
    - Custom routes for health, metrics, tools, history, and root endpoints.
    - Graceful shutdown logic to manage database connections.

Environment Variables:
    ENV (str): Environment setting. Use "prod" for production.

Middleware:
    GlobalRateLimitMiddleware: Enforces global rate limits.
    SecurityHeadersMiddleware: Adds security-related headers to responses.
    SecurityMiddleware: Applies CORS and trusted host validation.
    HTTPSRedirectMiddleware: Redirects HTTP traffic to HTTPS in production.

Routers:
    health: Health check endpoint.
    metric: Metric endpoints.
    tools: Tool-related endpoints.
    history: History-related endpoints.
    root: Root-level endpoints.
"""

import asyncio
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

# Https redirect Middleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

from db.database import check_db_connection, get_db
from helpers.log.logger import init_log

# Rate limit Middleware
from middleware.rate_limit import GlobalRateLimitMiddleware  # Import custom middleware

# Security Middleware
from middleware.security import SecurityMiddleware  # Import security middleware
from routers import health, history, metric, root, tools


# Adding necessary paths
sys.path.append("routers")
sys.path.append("helpers")
sys.path.append("middleware")

# Initialize the database
db = get_db()

# Initialize loggers
logger = init_log()
logger.info("Hello start APP !!")
# Graceful shutdown logic with retries for DB connection
RETRY_LIMIT = int(os.getenv("RETRY_LIMIT", "10"))


@asynccontextmanager
async def app_lifespan(status):
    """
    Context manager for managing app lifespan.

    Handles application startup and graceful shutdown, including retry
    logic for database connection and closing the DB connection during shutdown.
    """
    logger.info("Application lifespan started")
    # Retry logic for DB connection if necessary
    retries = RETRY_LIMIT
    for _ in range(retries):
        try:
            check_db_connection()
            logger.info("Database connected")
            break
        except ConnectionError as e:
            logger.error(f"Database connection error: {e}")
            await asyncio.sleep(5)

        logger.critical("Failed to connect to database after retries")
        sys.exit(1)
    yield  # The app runs here
    logger.info("Shutting down gracefully...")
    db.close()


app = FastAPI(lifespan=app_lifespan)

# Add global rate-limiting middleware
app.add_middleware(GlobalRateLimitMiddleware)
# Add the security middlewares
app.add_middleware(SecurityMiddleware)
# Redirect all HTTP to HTTPS for production environments
if os.getenv("ENV") == "prod":
    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(health.router, prefix="")
app.include_router(metric.router, prefix="")
app.include_router(tools.router, prefix="/v1")
app.include_router(history.router, prefix="/v1")
app.include_router(root.router, prefix="")
