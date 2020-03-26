from typing import Generator

from dynaconf import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

DB_SETTINGS = settings.DATABASE

engine = create_engine(DB_SETTINGS.URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Retrieve a Thread-local Session."""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def create_models() -> None:
    """Create sqlalchemy models."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
