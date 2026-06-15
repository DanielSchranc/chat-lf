import uuid
from collections.abc import AsyncIterator

from fastapi import HTTPException

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.llm_service import LLMService


class ChatService:
    def __init__(
        self,
        conv_repo: ConversationRepository,
        msg_repo: MessageRepository,
        llm: LLMService,
    ) -> None:
        self._conv_repo = conv_repo
        self._msg_repo = msg_repo
        self._llm = llm

    async def send_message(
        self, conversation_id: uuid.UUID, user_content: str
    ) -> AsyncIterator[str]:
        if not await self._conv_repo.get(conversation_id):
            raise HTTPException(status_code=404, detail="Conversation not found")

        await self._msg_repo.create(conversation_id, "user", user_content)

        history = await self._msg_repo.list_by_conversation(conversation_id)

        accumulated: list[str] = []
        async for chunk in self._llm.stream(history):
            accumulated.append(chunk)
            yield chunk

        assistant_text = "".join(accumulated)
        await self._msg_repo.create(conversation_id, "assistant", assistant_text)
        await self._conv_repo.touch(conversation_id)
