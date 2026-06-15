import uuid

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, conversation_id: uuid.UUID, role: str, content: str) -> Message:
        msg = Message(conversation_id=conversation_id, role=role, content=content)
        self._db.add(msg)
        await self._db.commit()
        await self._db.refresh(msg)
        return msg

    async def list_by_conversation(
        self, conversation_id: uuid.UUID, limit: int = 200
    ) -> list[Message]:
        result = await self._db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        return list(result.all())
