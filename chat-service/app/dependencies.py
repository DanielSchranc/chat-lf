from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_session
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.chat_service import ChatService
from app.services.llm_service import LLMService


def get_chat_service(db: AsyncSession = Depends(get_session)) -> ChatService:
    return ChatService(
        ConversationRepository(db),
        MessageRepository(db),
        LLMService(),
    )


ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
