from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_settings
from app.database import create_db_and_tables
from app.routers import conversations, chat_messages


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


if app_settings.sentry_dsn:
    sentry_sdk.init(dsn=app_settings.sentry_dsn)

app = FastAPI(title="Chat Service", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    conversations.router, prefix="/api/v1/conversations", tags=["conversations"]
)
app.include_router(
    chat_messages.router, prefix="/api/v1/conversations", tags=["messages"]
)


@app.get("/healthz", tags=["health"])
async def health():
    return {"status": "ok"}
