import pytest
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_account(client: AsyncClient, token_headers):
    logger.info("Starting test_create_account")
    payload = {
        "account_name": "Savings",
        "bank_name": "Chase",
        "account_type": "debit",
        "description": "My Savings"
    }
    logger.info(f"Creating account with payload: {payload}")
    response = await client.post(
        "/api/v1/accounts/",
        headers=token_headers,
        json=payload
    )
    logger.info(f"Create response code: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["account_name"] == "Savings"
    assert data["bank_name"] == "Chase"
    assert data["account_type"] == "debit"
    assert "id" in data
    logger.info(f"Account created successfully with ID: {data['id']}")

@pytest.mark.asyncio
async def test_read_accounts(client: AsyncClient, token_headers):
    logger.info("Starting test_read_accounts")
    # Ensure at least one exists
    await client.post(
        "/api/v1/accounts/",
        headers=token_headers,
        json={"account_name": "Checking", "bank_name": "BoA", "account_type": "debit"}
    )
    
    logger.info("Fetching all accounts")
    response = await client.get("/api/v1/accounts/", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    logger.info(f"Retrieved {len(data)} accounts")

@pytest.mark.asyncio
async def test_update_account(client: AsyncClient, token_headers):
    logger.info("Starting test_update_account")
    create_res = await client.post(
        "/api/v1/accounts/",
        headers=token_headers,
        json={"account_name": "ToUpdate", "bank_name": "Bank", "account_type": "credit"}
    )
    acc_id = create_res.json()["id"]
    logger.info(f"Created account to update, ID: {acc_id}")
    
    update_payload = {"account_name": "Updated", "bank_name": "Bank", "account_type": "credit"}
    logger.info(f"Updating account {acc_id} with: {update_payload}")
    response = await client.put(
        f"/api/v1/accounts/{acc_id}",
        headers=token_headers,
        json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["account_name"] == "Updated"
    logger.info("Account updated successfully")

@pytest.mark.asyncio
async def test_delete_account(client: AsyncClient, token_headers):
    logger.info("Starting test_delete_account")
    create_res = await client.post(
        "/api/v1/accounts/",
        headers=token_headers,
        json={"account_name": "ToDelete", "bank_name": "Bank", "account_type": "debit"}
    )
    acc_id = create_res.json()["id"]
    logger.info(f"Created account to delete, ID: {acc_id}")
    
    logger.info(f"Deleting account {acc_id}")
    response = await client.delete(f"/api/v1/accounts/{acc_id}", headers=token_headers)
    assert response.status_code == 200
    
    # Verify
    logger.info("Verifying deletion")
    list_res = await client.get("/api/v1/accounts/", headers=token_headers)
    data = list_res.json()
    assert not any(a["id"] == acc_id for a in data)
    logger.info("Account verified as deleted")
