from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI

def add_security_middleware(app: FastAPI):
    """
    Adds CORS and Trusted Host middleware to the FastAPI application.
    """
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins (can be restricted as needed)
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    # Add Trusted Host middleware for host validation
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*", "localhost"],  # "*" allows any host, restrict in production
    )
