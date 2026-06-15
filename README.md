# Chat Service

Minimal AI chat microservice — Python / FastAPI / PostgreSQL / OpenAI.

## Architecture

```
[Browser]
   ↓  /api/backend/...  (BFF proxy)
[Next.js — thin proxy layer]
   ↓  http://localhost:8000/api/v1/...
[chat-service FastAPI — LLM + persistence]
   └── PostgreSQL
```

The Next.js app is a BFF: it forwards browser requests to the Python service, hides the
internal URL, and is the single browser-facing origin. No CORS complexity in prod.

## Quick start

Prerequisites: Docker + Docker Compose, an OpenAI API key.

```bash
git clone <repo>
cd chat-service
cp .env.example .env          # add your OPENAI_API_KEY
docker compose up --build
```

API docs: http://localhost:8000/docs

## API

| Method | Path | Description |
|--------|------|-------------|
| GET    | `/healthz` | Health check |
| POST   | `/api/v1/conversations` | Create conversation |
| GET    | `/api/v1/conversations` | List conversations |
| GET    | `/api/v1/conversations/{id}` | Get conversation |
| DELETE | `/api/v1/conversations/{id}` | Delete conversation + messages |
| GET    | `/api/v1/conversations/{id}/messages` | Fetch message history |
| POST   | `/api/v1/conversations/{id}/messages` | Send message (SSE stream) |

## Running tests

```bash
cd chat-service
poetry install
poetry run pytest -m unit -v
```

## Tech choices

| Choice | Rationale |
|--------|-----------|
| **FastAPI** | Async-native Python, Pydantic built-in, auto OpenAPI docs |
| **SQLModel** | Unified ORM + Pydantic schema — one class per entity |
| **psycopg3** | Modern async-capable driver; sync URL for Alembic, async URL for FastAPI |
| **AsyncOpenAI** | Full control of message list format, native async streaming |
| **PostgreSQL** | ACID, relational model fits conversation/message hierarchy, scales |
| **Repository pattern** | Decouples business logic from storage; swap DB without touching service code |
| **Docker Compose** | One-command reproducible local dev mirroring microservice prod topology |
| **Alembic** | Schema migrations tracked in git; runs automatically on container startup |
