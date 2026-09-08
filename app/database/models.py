from sqlmodel import Field, Relationship, SQLModel
from typing import List
from datetime import datetime
import uuid

# User Model
class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user")


class RefreshToken(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    token: str = Field(unique=True, index=True)

    user_id: uuid.UUID = Field(foreign_key="user.id")

    createdAt: datetime = Field(default_factory=datetime.utcnow)
    expiresAt: datetime
    isRevoked: bool = Field(default=False)

    user: User = Relationship(back_populates="refresh_tokens")
