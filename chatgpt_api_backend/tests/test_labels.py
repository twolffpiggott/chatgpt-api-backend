def test_create_label(test_client):
    chat_data = {"summary": "Test chat for label creation"}
    chat_response = test_client.post("/chats/", json=chat_data)
    chat = chat_response.json()

    label_data = {"name": "Test Label"}
    response = test_client.post(f"/chats/{chat['id']}/labels/", json=label_data)

    assert response.status_code == 200
    label = response.json()
    assert label["name"] == "Test Label"
    assert "id" in label
    assert label["chat_id"] == chat["id"]


def test_delete_label(test_client):
    chat_data = {"summary": "Test chat for label deletion"}
    chat_response = test_client.post("/chats/", json=chat_data)
    chat = chat_response.json()

    label_data = {"name": "Label to delete"}
    create_response = test_client.post(f"/chats/{chat['id']}/labels/", json=label_data)
    label_to_delete = create_response.json()

    response = test_client.delete(f"/chats/{chat['id']}/labels/{label_to_delete['id']}")

    assert response.status_code == 200
    deleted_label = response.json()
    assert deleted_label["id"] == label_to_delete["id"]

    # Verify the label no longer exists in the database
    response = test_client.delete(f"/chats/{chat['id']}/labels/{deleted_label['id']}")
    assert response.status_code == 404
