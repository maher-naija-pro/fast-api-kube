
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import os
from helpers.log.logger import init_log
from fastapi import  HTTPException
# Initialize loggers
logger=init_log()
# Database URL: replace with your PostgreSQL credentials
DATABASE_URL =  os.getenv("DB_URI")
# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# SessionLocal class for managing sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for creating models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection():
    try:
        db = SessionLocal()
        # Run a simple query to check the database connection

        result = engine.connect().execute(text("SELECT 1")).scalar()
 
        # If connection is successful, return status
        if result == 1 :
            logger.info(f"Database connection check successful.{str(result)}")
            return {"status": "Database is connected"}
        else:
            raise HTTPException(status_code=500, detail="Unexpected result from DB check")
    except Exception as e:
        # Log the exception and return an error response
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")