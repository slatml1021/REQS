"""Database configuration and SQLAlchemy session management."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DEFAULT_DATABASE_URL = "mysql+pymysql://reqs:reqs@localhost:3307/reqs"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


class Base(DeclarativeBase):
    """Base class shared by all persistent domain models."""


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    """Provide one transactional database session per API request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
