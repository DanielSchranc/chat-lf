import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class MessageBase(SQLModel):
    content: str
    role: str = Field(default="user", max_length=16)


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    conversation: "Conversation | None" = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    content: str = Field(min_length=1, max_length=32_000)


class MessageRead(MessageBase):
    id: uuid.UUID
    conversation_id: uuid.UUID
    created_at: datetime
