from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from logging_config import logger 


SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

# Needed for SQLite to work with multiple threads in FastAPI
logger.info("Creating database engine with URL: %s", SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

logger.info("Configuring SessionLocal with autocommit=False and autoflush=False")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
logger.info("Declarative base class created for ORM models")

def get_db():
    """Dependency that provides a database session per request."""
    db = SessionLocal()
    logger.debug("Database session started")
    try:
        yield db
    finally:
        db.close()
        logger.debug("Database session closed")
