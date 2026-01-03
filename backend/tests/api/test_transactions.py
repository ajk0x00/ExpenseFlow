import pytest
import pytest_asyncio
from httpx import AsyncClient
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@pytest_asyncio.fixture
async def test_account(client: AsyncClient, token_headers):
    logger.info("Creating test account for transactions")
    response = await client.post(
        "/api/v1/accounts/",
        headers=token_headers,
        json={
            "account_name": "Transaction Account",
            "bank_name": "Test Bank",
            "account_type": "debit"
        }
    )
    logger.info(f"Test account created: {response.json().get('id')}")
    return response.json()

@pytest.mark.asyncio
async def test_create_transaction(client: AsyncClient, token_headers, test_account):
    logger.info("Starting test_create_transaction")
    payload = {
        "account_id": test_account["id"],
        "date": datetime.now().isoformat(),
        "narration": "Grocery Store",
        "withdrawal_amount": 50.00,
        "deposit_amount": 0.00
    }
    logger.info(f"Creating transaction with payload: {payload}")
    response = await client.post(
        "/api/v1/transactions/",
        headers=token_headers,
        json=payload
    )
    logger.info(f"Response status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["narration"] == "Grocery Store"
    assert float(data["withdrawal_amount"]) == 50.0
    assert data["account_id"] == test_account["id"]
    logger.info(f"Transaction created successfully with ID: {data['id']}")

@pytest.mark.asyncio
async def test_read_transactions(client: AsyncClient, token_headers, test_account):
    logger.info("Starting test_read_transactions")
    # Create a transaction
    await client.post(
        "/api/v1/transactions/",
        headers=token_headers,
        json={
            "account_id": test_account["id"],
            "date": datetime.now().isoformat(),
            "narration": "Rent",
            "withdrawal_amount": 1000.00,
            "deposit_amount": 0.00
        }
    )
    
    logger.info("Fetching transactions")
    response = await client.get("/api/v1/transactions/", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    logger.info(f"Fetched {len(data)} transactions")

@pytest.mark.asyncio
async def test_update_transaction(client: AsyncClient, token_headers, test_account):
    logger.info("Starting test_update_transaction")
    create_res = await client.post(
        "/api/v1/transactions/",
        headers=token_headers,
        json={
            "account_id": test_account["id"],
            "date": datetime.now().isoformat(),
            "narration": "Old Narration",
            "withdrawal_amount": 10.00,
            "deposit_amount": 0.00
        }
    )
    tx_id = create_res.json()["id"]
    logger.info(f"Created transaction to update, ID: {tx_id}")
    
    update_payload = {
        "account_id": test_account["id"],
        "date": datetime.now().isoformat(),
        "narration": "New Narration",
        "withdrawal_amount": 10.00,
        "deposit_amount": 0.00
    }
    logger.info(f"Updating transaction {tx_id} with: {update_payload}")
    response = await client.put(
        f"/api/v1/transactions/{tx_id}",
        headers=token_headers,
        json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["narration"] == "New Narration"
    logger.info("Transaction updated successfully")

@pytest.mark.asyncio
async def test_delete_transaction(client: AsyncClient, token_headers, test_account):
    logger.info("Starting test_delete_transaction")
    create_res = await client.post(
        "/api/v1/transactions/",
        headers=token_headers,
        json={
            "account_id": test_account["id"],
            "date": datetime.now().isoformat(),
            "narration": "To Delete",
            "withdrawal_amount": 5.00,
            "deposit_amount": 0.00
        }
    )
    tx_id = create_res.json()["id"]
    logger.info(f"Created transaction to delete, ID: {tx_id}")
    
    logger.info(f"Deleting transaction {tx_id}")
    response = await client.delete(f"/api/v1/transactions/{tx_id}", headers=token_headers)
    assert response.status_code == 200
    
    # Verify
    logger.info("Verifying deletion")
    get_res = await client.get(f"/api/v1/transactions/{tx_id}", headers=token_headers)
    assert get_res.status_code == 404
    logger.info("Transaction verified as deleted")
