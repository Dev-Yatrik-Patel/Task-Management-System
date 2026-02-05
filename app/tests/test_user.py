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
async def test_user_details_fetcher(async_client, auth_headers):
    # create task
    user_details_response = await async_client.get(
        "users/me",
        headers=auth_headers,
    )

    assert user_details_response.status_code == 200
    body = user_details_response.json()

    assert body["success"] is True
    assert body["data"]["id"] == 1
    assert body["data"]["email"] == "testuser@example.com"
    assert body["data"]["is_active"] is True
    
@pytest.mark.asyncio
async def test_delete_user_profile(async_client, auth_headers):
    # create task
    user_details_response = await async_client.post(
        "users/deleteprofile",
        headers=auth_headers,
    )

    assert user_details_response.status_code == 200
    body = user_details_response.json()

    assert body["success"] is True
    assert body["message"]== "Profile has been deleted successfully!"