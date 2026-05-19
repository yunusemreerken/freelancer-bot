"""
app/database.py

Database connection and session management.
This module provides the SQLAlchemy equivalent of a DbContext.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

# SQLite file path written to the Docker volume.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:////data/freelancer.db")

# Engine object used for database connections.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for FastAPI request handling.
)

# Session factory used to create per-request database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class inherited by all SQLAlchemy ORM models.
class Base(DeclarativeBase):
    pass


def get_db():
    """
    Provide a database session through FastAPI dependency injection.
    Each request gets its own session, which is closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create database tables during application startup."""
    from app import models  # noqa: F401 - importing models registers metadata.
    Base.metadata.create_all(bind=engine)
