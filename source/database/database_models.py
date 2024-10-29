from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Users(SQLModel, table=True):
    __tablename__ = "users"

    user_id: int = Field(primary_key=True)
    firstname: Optional[str] = Field(default=None, max_length=64)
    surname: Optional[str] = Field(default=None, max_length=64)
    username: Optional[str] = Field(default=None, max_length=64)
    created_at: datetime = Field(default_factory=lambda: datetime.now().replace(tzinfo=None))