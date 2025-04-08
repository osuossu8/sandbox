from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .settings import DatabaseSettings

database_settings = DatabaseSettings()

DB_USER = database_settings.DB_USER
DB_PASSWORD = database_settings.DB_PASSWORD
DB_HOST = database_settings.DB_HOST
DB_PORT = database_settings.DB_PORT
DB_NAME = database_settings.DB_NAME

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
