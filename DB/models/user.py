from DB.models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import BIGINT

from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    repr_cols = ("name",)

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)

    context: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)
    available_trips: Mapped[int] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
