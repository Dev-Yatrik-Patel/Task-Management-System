import pytest
import pytest_asyncio

@pytest_asyncio.fixture
async def auth_headers(async_client):
    # register
    await async_client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "strongpassword123",
        },
    )

    # login
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "strongpassword123",
        },
    )

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_crud_and_list_tasks_endpoints(async_client, auth_headers):
    # create task
    create_response = await async_client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "Testing task creation",
        },
        headers=auth_headers,
    )

    assert create_response.status_code == 200
    body = create_response.json()

    assert body["success"] is True
    assert body["message"] == "Success"
    assert body["data"]["id"] == 1
    assert body["data"]["title"] == "Test Task"
    assert body["data"]["description"] == "Testing task creation"
    assert body["data"]["status"] == "pending"


    # update task
    update_response = await async_client.put(
        f"/tasks/{1}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "completed"
        },
        headers=auth_headers,
    )

    assert update_response.status_code == 200
    body = update_response.json()

    assert body["success"] is True
    assert body["message"] == "Success"
    assert body["data"]["id"] == 1
    assert body["data"]["title"] == "Updated Task"
    assert body["data"]["description"] == "Updated Description"
    assert body["data"]["status"] == "completed"

    # list tasks
    list_response = await async_client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert list_response.status_code == 200
    body = list_response.json()

    assert body["success"] is True
    assert len(body["data"]["tasks"]) >= 1
    
    # list specific task
    specific_list_response = await async_client.get(
        f"/tasks/{1}",
        headers=auth_headers,
    )

    assert specific_list_response.status_code == 200
    body = specific_list_response.json()

    assert body["success"] is True
    assert body["message"] == "Success"
    assert body["data"]["id"] == 1
    assert body["data"]["title"] == "Updated Task"
    assert body["data"]["description"] == "Updated Description"
    assert body["data"]["status"] == "completed"
    
    # delete task
    delete_response = await async_client.delete(
        f"/tasks/{1}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 200
    body = delete_response.json()
    assert body["success"] is True
    assert body["message"] == "Task has been deleted successfully!"