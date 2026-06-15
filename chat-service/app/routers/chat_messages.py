import json
import uuid

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.database import SessionDep
from app.dependencies import ChatServiceDep
from app.models.message import MessageCreate, MessageRead
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository

router = APIRouter()


@router.get("/{conversation_id}/messages", response_model=list[MessageRead])
async def list_messages(
    conversation_id: uuid.UUID,
    db: SessionDep,
    limit: int = Query(200, ge=1, le=500),
):
    if not await ConversationRepository(db).get(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return await MessageRepository(db).list_by_conversation(conversation_id, limit)


@router.post("/{conversation_id}/messages")
async def send_message(
    conversation_id: uuid.UUID,
    body: MessageCreate,
    service: ChatServiceDep,
):
    async def sse_generator():
        try:
            async for chunk in service.send_message(conversation_id, body.content):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
