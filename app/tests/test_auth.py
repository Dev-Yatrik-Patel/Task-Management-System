import pytest

@pytest.mark.asyncio
async def test_user_registration(async_client):
    payload = {
        "email": "testuser@example.com",
        "password": "strongpassword123"
    }

    response = await async_client.post("/auth/register", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert body["success"] is True
    assert body["data"]["email"] == payload["email"]
    assert "password" not in body["data"]
    
@pytest.mark.asyncio
async def test_user_login(async_client):
    response = await async_client.post(
        "/auth/login",
        data={
            "username": "testuser@example.com",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 200
    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"
