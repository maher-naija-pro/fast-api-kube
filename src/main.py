#!/usr/bin/python
import os 
import sys
import asyncio

# Security Middleware 
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware


# Adding necessary paths
sys.path.append("routers")
sys.path.append("helpers")
sys.path.append("middleware")

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from helpers.log.logger import init_log
from db.database import get_db,check_db_connection

from routers import health
from routers import metric
from routers import tools
from routers import history
from routers import root

from middleware.rate_limit import GlobalRateLimitMiddleware  # Import custom middleware


# Initialize the database
db=get_db()

# Initialize loggers
logger=init_log()
logger.info('Hello start APP !!')
# Graceful shutdown logic with retries for DB connection

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    logger.info("Application lifespan started")
    # Retry logic for DB connection if necessary
    retries = 3
    for _ in range(retries):
        try:
            check_db_connection()
            logger.info("Database connected")
            break
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            await asyncio.sleep(5)  # Delay before retry
    else:
        logger.critical("Failed to connect to database after retries")
        sys.exit(1)
    yield  # The app runs here
    logger.info("Shutting down gracefully...")
    db.close()

app = FastAPI(lifespan=app_lifespan)

# Add global rate-limiting middleware
app.add_middleware(GlobalRateLimitMiddleware)

# Add middleware for security and observability
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict origins for better security
    allow_credentials=True,
    allow_methods=["*"],  # Controls which methods are allowed (GET, POST, etc.)
    allow_headers=["*"]   # Specifies which headers are allowed
    
)

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*", "localhost"] # Replace "*" with trusted domains for security
)

# Redirect all HTTP to HTTPS for production environments
if os.getenv("ENV") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(health.router, prefix="")
app.include_router(metric.router, prefix="")
app.include_router(tools.router, prefix="/v1")
app.include_router(history.router, prefix="/v1")
app.include_router(root.router, prefix="")

