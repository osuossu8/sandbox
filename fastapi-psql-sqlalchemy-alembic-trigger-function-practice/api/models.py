from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

UTC_NOW = func.now()


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=UTC_NOW, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=UTC_NOW, server_onupdate=UTC_NOW, nullable=False
    )
