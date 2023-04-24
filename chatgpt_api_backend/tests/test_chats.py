import pytest
from app.schemas.chat import ChatCreate, ChatUpdate


@pytest.fixture
def created_chat(test_client):
    chat = ChatCreate(summary="This is a test chat.")
    response = test_client.post("/chats/", data=chat.json())
    data = response.json()
    chat_id = data["id"]
    return chat_id


def test_create_chat(test_client):
    chat = ChatCreate(summary="This is a test chat.")
    response = test_client.post("/chats/", data=chat.json())
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["summary"] == "This is a test chat."
    assert "id" in data


def test_get_chat(test_client, created_chat):
    response = test_client.get(f"/chats/{created_chat}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["summary"] == "This is a test chat."
    assert data["id"] == created_chat


def test_get_chats_with_pagination(test_client):
    response = test_client.get("/chats/", params={"skip": 0, "limit": 10})
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) > 0


def test_update_chat(test_client, created_chat):
    chat_update = ChatUpdate(summary="This is an updated test chat.")
    response = test_client.put(f"/chats/{created_chat}", data=chat_update.json())
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["summary"] == "This is an updated test chat."
    assert data["id"] == created_chat


def test_delete_chat(test_client, created_chat):
    response = test_client.delete(f"/chats/{created_chat}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["summary"] == "This is a test chat."
    assert data["id"] == created_chat


def test_get_non_existent_chat(test_client, created_chat):
    test_client.delete(f"/chats/{created_chat}")
    response = test_client.get(f"/chats/{created_chat}")
    assert response.status_code == 404, response.text
