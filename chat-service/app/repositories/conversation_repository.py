import uuid
from datetime import datetime

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.conversation import Conversation


class ConversationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, title: str | None = None) -> Conversation:
        conv = Conversation(title=title)
        self._db.add(conv)
        await self._db.commit()
        await self._db.refresh(conv)
        return conv

    async def get(self, id: uuid.UUID) -> Conversation | None:
        return await self._db.get(Conversation, id)

    async def list_all(self, limit: int = 50, offset: int = 0) -> list[Conversation]:
        result = await self._db.exec(
            select(Conversation)
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())

    async def touch(self, id: uuid.UUID) -> None:
        """Bump updated_at so conversation sorts correctly after a new message."""
        conv = await self._db.get(Conversation, id)
        if conv:
            conv.updated_at = datetime.utcnow()
            self._db.add(conv)
            await self._db.commit()
