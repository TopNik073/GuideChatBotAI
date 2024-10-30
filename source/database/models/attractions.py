from email.policy import default

from source.database.models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime


class Attractions(Base):
    __tablename__ = "attractions"

    repr_cols = ("name",)

    attraction_id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)

    working_hour: Mapped[str] = mapped_column(nullable=True)

    location: Mapped[str] = mapped_column(nullable=True)

    category: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
