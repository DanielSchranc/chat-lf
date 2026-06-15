from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import app_settings

engine = create_async_engine(app_settings.database_url, echo=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def create_db_and_tables() -> None:
    """Dev convenience — Alembic handles production migrations."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
