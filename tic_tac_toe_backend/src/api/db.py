"""
SQLAlchemy database setup for FastAPI Tic Tac Toe backend.
Establishes engine, session, and init utility for SQLite persistence.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

import os

# SQLite DB path (file-based, persistent)
DB_FILENAME = os.getenv("TICTACTOE_DB_FILENAME", "tic_tac_toe.sqlite3")
DATABASE_URL = f"sqlite:///./{DB_FILENAME}"

# Create SQLAlchemy engine and session
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# PUBLIC_INTERFACE
def get_db():
    """
    PUBLIC_INTERFACE: Dependency-yielding database session for FastAPI routes.
    Usage:
        db = next(get_db())
    Yields:
        SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUBLIC_INTERFACE
def init_db():
    """
    PUBLIC_INTERFACE: Initializes database and creates tables if not present.
    """
    Base.metadata.create_all(bind=engine)
