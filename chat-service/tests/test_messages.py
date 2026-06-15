import uuid

import pytest


@pytest.mark.unit
async def test_send_message_streams_response(client, mock_llm):
    conv = (await client.post("/api/v1/conversations", json={})).json()
    r = await client.post(
        f"/api/v1/conversations/{conv['id']}/messages",
        json={"content": "Hello"},
    )
    assert r.status_code == 200
    assert "data:" in r.text


@pytest.mark.unit
async def test_messages_persisted_after_send(client, mock_llm):
    conv = (await client.post("/api/v1/conversations", json={})).json()
    await client.post(
        f"/api/v1/conversations/{conv['id']}/messages",
        json={"content": "Hello"},
    )
    msgs = (await client.get(f"/api/v1/conversations/{conv['id']}/messages")).json()
    assert len(msgs) == 2
    assert msgs[0]["role"] == "user"
    assert msgs[1]["role"] == "assistant"


@pytest.mark.unit
async def test_list_messages_unknown_conversation_returns_404(client):
    r = await client.get(f"/api/v1/conversations/{uuid.uuid4()}/messages")
    assert r.status_code == 404


@pytest.mark.unit
async def test_send_message_unknown_conversation_returns_error(client, mock_llm):
    r = await client.post(
        f"/api/v1/conversations/{uuid.uuid4()}/messages",
        json={"content": "Hello"},
    )
    assert "error" in r.text
