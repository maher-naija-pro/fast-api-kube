"""
base.py

This module defines the base model for SQLAlchemy ORM, which is used to create
database tables and map Python objects to database records. The `Base` class
serves as the foundation for all models in the application.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata
