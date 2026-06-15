import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class ConversationBase(SQLModel):
    title: str | None = Field(default=None, max_length=255)


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
