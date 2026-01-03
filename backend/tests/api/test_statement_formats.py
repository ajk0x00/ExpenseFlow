import pytest
from httpx import AsyncClient
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_create_format(client: AsyncClient, token_headers):
    logger.info("Starting test_create_format")
    payload = {
        "format_name": "Chase CSV",
        "bank_name": "Chase",
        "data_start_row": 2,
        "date_column": "Date",
        "narration_column": "Description",
        "withdrawal_column": "Debit",
        "deposit_column": "Credit"
    }
    logger.info(f"Creating statement format with payload: {payload}")
    response = await client.post(
        "/api/v1/statement-formats/",
        headers=token_headers,
        json=payload
    )
    logger.info(f"Response status: {response.status_code}")
    assert response.status_code == 200
    data = response.json()
    assert data["format_name"] == "Chase CSV"
    assert "id" in data
    logger.info(f"Statement format created with ID: {data['id']}")

@pytest.mark.asyncio
async def test_read_formats(client: AsyncClient, token_headers):
    logger.info("Starting test_read_formats")
    # Ensure one exists
    await client.post(
        "/api/v1/statement-formats/",
        headers=token_headers,
        json={
            "format_name": "Amex",
            "data_start_row": 1,
            "date_column": "A",
            "narration_column": "B",
            "withdrawal_column": "C",
            "deposit_column": "D"
        }
    )
    
    logger.info("Fetching formats")
    response = await client.get("/api/v1/statement-formats/", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    logger.info(f"Fetched {len(data)} formats")

@pytest.mark.asyncio
async def test_update_format(client: AsyncClient, token_headers):
    logger.info("Starting test_update_format")
    create_res = await client.post(
        "/api/v1/statement-formats/",
        headers=token_headers,
        json={
            "format_name": "UpdateMe",
            "data_start_row": 1,
            "date_column": "A",
            "narration_column": "B",
            "withdrawal_column": "C",
            "deposit_column": "D"
        }
    )
    obj_id = create_res.json()["id"]
    logger.info(f"Created format to update, ID: {obj_id}")
    
    update_payload = {
        "format_name": "Updated",
        "data_start_row": 1,
        "date_column": "A",
        "narration_column": "B",
        "withdrawal_column": "C",
        "deposit_column": "D"
    }
    logger.info(f"Updating format {obj_id} with: {update_payload}")
    response = await client.put(
        f"/api/v1/statement-formats/{obj_id}",
        headers=token_headers,
        json=update_payload
    )
    assert response.status_code == 200
    assert response.json()["format_name"] == "Updated"
    logger.info("Format updated successfully")

@pytest.mark.asyncio
async def test_delete_format(client: AsyncClient, token_headers):
    logger.info("Starting test_delete_format")
    create_res = await client.post(
        "/api/v1/statement-formats/",
        headers=token_headers,
        json={
            "format_name": "DeleteMe",
            "data_start_row": 1,
            "date_column": "A",
            "narration_column": "B",
            "withdrawal_column": "C",
            "deposit_column": "D"
        }
    )
    obj_id = create_res.json()["id"]
    logger.info(f"Created format to delete, ID: {obj_id}")
    
    logger.info(f"Deleting format {obj_id}")
    response = await client.delete(f"/api/v1/statement-formats/{obj_id}", headers=token_headers)
    assert response.status_code == 200
    
    logger.info("Verifying deletion")
    list_res = await client.get("/api/v1/statement-formats/", headers=token_headers)
    assert not any(f["id"] == obj_id for f in list_res.json())
    logger.info("Format verified as deleted")
