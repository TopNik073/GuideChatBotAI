from source.database.models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime


class Users(Base):
    __tablename__ = "users"

    repr_cols = ("name",)

    user_id: Mapped[int] = mapped_column(primary_key=True)

    firstname: Mapped[str] = mapped_column(unique=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)

    context: Mapped[list[dict]] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
