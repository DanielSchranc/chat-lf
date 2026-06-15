import uuid

from fastapi import APIRouter, HTTPException, Query

from app.database import SessionDep
from app.models.conversation import ConversationCreate, ConversationRead
from app.repositories.conversation_repository import ConversationRepository

router = APIRouter()


@router.post("/", response_model=ConversationRead, status_code=201)
async def create_conversation(body: ConversationCreate, db: SessionDep):
    return await ConversationRepository(db).create(body.title)


@router.get("/", response_model=list[ConversationRead])
async def list_conversations(
    db: SessionDep,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    return await ConversationRepository(db).list_all(limit, offset)


@router.get("/{id}", response_model=ConversationRead)
async def get_conversation(id: uuid.UUID, db: SessionDep):
    conv = await ConversationRepository(db).get(id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.delete("/{id}", status_code=204)
async def delete_conversation(id: uuid.UUID, db: SessionDep):
    conv = await ConversationRepository(db).get(id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await db.delete(conv)
    await db.commit()
