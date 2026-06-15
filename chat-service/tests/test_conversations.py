import uuid

import pytest


@pytest.mark.unit
async def test_create_conversation_returns_201(client):
    r = await client.post("/api/v1/conversations", json={})
    assert r.status_code == 201
    assert "id" in r.json()


@pytest.mark.unit
async def test_list_conversations_empty(client):
    r = await client.get("/api/v1/conversations")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.unit
async def test_get_unknown_conversation_returns_404(client):
    r = await client.get(f"/api/v1/conversations/{uuid.uuid4()}")
    assert r.status_code == 404


@pytest.mark.unit
async def test_delete_conversation_returns_204(client):
    conv = (await client.post("/api/v1/conversations", json={})).json()
    r = await client.delete(f"/api/v1/conversations/{conv['id']}")
    assert r.status_code == 204


@pytest.mark.unit
async def test_delete_unknown_conversation_returns_404(client):
    r = await client.delete(f"/api/v1/conversations/{uuid.uuid4()}")
    assert r.status_code == 404
