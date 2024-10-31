from DB.models.Base import Base
from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR

from datetime import datetime


class Attractions(Base):
    __tablename__ = "attractions"

    repr_cols = ("name",)

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=True)
    image: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)

    tsv_description: Mapped[str] = mapped_column(TSVECTOR, nullable=False)

    __table_args__ = (
        Index("ix_attractions_tsv_description", "tsv_description", postgresql_using="gin"),
    )
