import pytest
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_category(client: AsyncClient, token_headers):
    logger.info("Starting test_create_category")
    payload = {"name": "Groceries", "description": "Daily needs"}
    logger.info(f"Creating category with payload: {payload}")
    response = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json=payload
    )
    logger.info(f"Response status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Groceries"
    assert data["description"] == "Daily needs"
    assert "id" in data
    logger.info(f"Category created with ID: {data['id']}")

@pytest.mark.asyncio
async def test_read_categories(client: AsyncClient, token_headers):
    logger.info("Starting test_read_categories")
    # Create one first
    await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={"name": "Utilities", "description": "Bills"}
    )
    
    logger.info("Fetching categories")
    response = await client.get("/api/v1/categories/", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    logger.info(f"Fetched {len(data)} categories")
    assert any(c["name"] == "Utilities" for c in data)

@pytest.mark.asyncio
async def test_update_category(client: AsyncClient, token_headers):
    logger.info("Starting test_update_category")
    create_res = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={"name": "Old Name", "description": "Old Desc"}
    )
    cat_id = create_res.json()["id"]
    logger.info(f"Created category to update, ID: {cat_id}")
    
    update_payload = {"name": "New Name", "description": "New Desc"}
    logger.info(f"Updating category {cat_id} with: {update_payload}")
    response = await client.put(
        f"/api/v1/categories/{cat_id}",
        headers=token_headers,
        json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == "New Desc"
    logger.info("Category updated successfully")

@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient, token_headers):
    logger.info("Starting test_delete_category")
    create_res = await client.post(
        "/api/v1/categories/",
        headers=token_headers,
        json={"name": "To Delete", "description": "Desc"}
    )
    cat_id = create_res.json()["id"]
    logger.info(f"Created category to delete, ID: {cat_id}")
    
    logger.info(f"Deleting category {cat_id}")
    response = await client.delete(f"/api/v1/categories/{cat_id}", headers=token_headers)
    assert response.status_code == 200
    
    logger.info("Verifying deletion")
    list_res = await client.get("/api/v1/categories/", headers=token_headers)
    data = list_res.json()
    assert not any(c["id"] == cat_id for c in data)
    logger.info("Category verified as deleted")
