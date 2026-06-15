from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool, create_engine
from sqlmodel import SQLModel

import app.models.conversation  # noqa: F401
import app.models.message  # noqa: F401

from app.config import app_settings

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def _sync_url() -> str:
    """Alembic runs sync — strip the _async suffix from the async driver name."""
    return app_settings.database_url.replace("+psycopg_async", "+psycopg")


def run_migrations_offline() -> None:
    context.configure(
        url=_sync_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(_sync_url(), poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
