import pytest
import pytest_asyncio
from httpx import AsyncClient
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@pytest_asyncio.fixture
async def analytics_data(client, token_headers):
    logger.info("Setting up analytics data")
    # Setup: Create Account, Categories, Transactions
    # 1. Categories
    logger.info("Creating categories for analytics")
    cat_food_res = await client.post(
        "/api/v1/categories/", headers=token_headers, 
        json={"name": "Food", "description": "Food"}
    )
    cat_food_id = cat_food_res.json().get("id")
    
    cat_bills_res = await client.post(
        "/api/v1/categories/", headers=token_headers, 
        json={"name": "Bills", "description": "Bills"}
    )
    cat_bills_id = cat_bills_res.json().get("id")
    
    # 2. Account
    logger.info("Creating account for analytics")
    acc_res = await client.post(
        "/api/v1/accounts/", headers=token_headers,
        json={"account_name": "AnalyticsAcc", "bank_name": "Test", "account_type": "debit"}
    )
    acc_id = acc_res.json()["id"]
    
    # 3. Transactions
    logger.info("Creating transactions for analytics")
    # Food: $100 today
    await client.post(
        "/api/v1/transactions/", headers=token_headers,
        json={
            "account_id": acc_id,
            "date": datetime.now().isoformat(),
            "narration": "Grocery",
            "withdrawal_amount": 100.00,
            "category_ids": [cat_food_id]
        }
    )
    
    # Bills: $200 yesterday
    await client.post(
        "/api/v1/transactions/", headers=token_headers,
        json={
            "account_id": acc_id,
            "date": (datetime.now() - timedelta(days=1)).isoformat(),
            "narration": "Electric",
            "withdrawal_amount": 200.00,
            "category_ids": [cat_bills_id]
        }
    )
    
    logger.info("Analytics data setup complete")
    return {"food_id": cat_food_id, "bills_id": cat_bills_id}

@pytest.mark.asyncio
async def test_expenses_by_category(client: AsyncClient, token_headers, analytics_data):
    logger.info("Starting test_expenses_by_category")
    response = await client.get("/api/v1/analytics/expenses-by-category", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Expenses by category data: {data}")
    items = data["items"]
    
    food_item = next((i for i in items if i["category_name"] == "Food"), None)
    bills_item = next((i for i in items if i["category_name"] == "Bills"), None)
    
    assert food_item is not None
    assert float(food_item["amount"]) == 100.0
    
    assert bills_item is not None
    assert float(bills_item["amount"]) == 200.0
    
    # Total should be sum of all positive withdrawals
    assert float(data["total_amount"]) >= 300.0 
    logger.info("Expenses by category verified")

@pytest.mark.asyncio
@pytest.mark.xfail(reason="SQLite cast compatibility issue")
async def test_expenses_over_time(client: AsyncClient, token_headers, analytics_data):
    logger.info("Starting test_expenses_over_time")
    response = await client.get("/api/v1/analytics/expenses-over-time", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    logger.info(f"Expenses over time data length: {len(data)}")
    assert len(data) >= 2 # At least two days
    logger.info("Expenses over time verified")
