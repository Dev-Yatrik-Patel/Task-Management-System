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
async def test_create_and_list_tasks(async_client, auth_headers):
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

    # list tasks
    list_response = await async_client.get(
        "/tasks",
        headers=auth_headers,
    )

    assert list_response.status_code == 200
    body = list_response.json()

    assert body["success"] is True
    assert len(body["data"]["tasks"]) >= 1