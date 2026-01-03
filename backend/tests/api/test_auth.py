import pytest
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    logger.info("Starting test_register_user")
    logger.info("Attempting to register new user: newuser@example.com")
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "newpassword123",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False 
        }
    )
    logger.info(f"Register response status: {response.status_code}")
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    logger.info(f"User registered successfully with ID: {data['id']}")

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, test_user):
    logger.info("Starting test_login_user")
    logger.info(f"Attempting to login with user: {test_user['email']}")
    response = await client.post(
        "/api/v1/auth/jwt/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    logger.info(f"Login response status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    logger.info("Login successful, token received")
