"""Database setup and utility functions.

This module initializes the database connection using SQLAlchemy, sets up the
engine, session maker, and declarative base. It provides helper functions to
obtain a database session and to check the database connection.

Attributes:
    logger (Logger): The logger instance for logging information.
    DATABASE_URL (str): The database URL fetched from environment variables.
    engine (Engine): The SQLAlchemy engine connected to the database.
    SessionLocal (sessionmaker): The session maker for creating database sessions.
    Base (declarative_base): The declarative base class for ORM models.
"""

import os

from fastapi import HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

from helpers.log.logger import init_log

# Initialize loggers
logger = init_log()

# Database URL: replace with your PostgreSQL credentials or use the default

POSTGRES_USER = os.getenv("POSTGRES_USER", "default_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "default_pass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "default_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"  # noqa: E501  # pylint: disable=C0301
# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal class for managing sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    """Provide a database session.

    This function yields a database session

    Yields:
        SessionLocal: A database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection():
    """Check the database connection by executing a simple query.

    Attempts to connect to the database and execute a "SELECT 1"
    Raises an HTTPException if the connection fails

    Returns:
        dict: A dictionary if the connection is successful.

    Raises:
        HTTPException: If the database connection fails
    """
    try:
        # Run a simple query to check the database connection
        result = engine.connect().execute(text("SELECT 1")).scalar()
        # If connection is successful, return status
        if result == 1:
            logger.info(f"Database connection check successful.{str(result)}")
            return {"status": "Database is connected"}

        raise HTTPException(status_code=500, detail="Unexpected result from DB check")
    except Exception as e:
        # Log the exception and return an error response
        logger.error(f"Database connection failed: {str(e)}")
    # raise HTTPException(status_code=500, detail="Database connection failed") from e
    return None
