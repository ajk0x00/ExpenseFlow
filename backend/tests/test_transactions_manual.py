import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Create an account
        account_data = {
            "account_name": "Test Account for Transactions",
            "bank_name": "Test Bank",
            "account_type": "credit",
            "description": "Created by test script"
        }
        response = await client.post(f"{BASE_URL}/accounts/", json=account_data)
        if response.status_code != 200:
            print(f"Failed to create account: {response.text}")
            return
        account = response.json()
        account_id = account["id"]
        print(f"Created account with ID: {account_id}")

        # 2. Create a transaction
        transaction_data = {
            "account_id": account_id,
            "date": datetime.utcnow().isoformat(),
            "narration": "Test Transaction",
            "withdrawal_amount": 100.50,
            "deposit_amount": 0.0,
            "metadata_": {"category": "test"}
        }
        response = await client.post(f"{BASE_URL}/transactions/", json=transaction_data)
        if response.status_code != 200:
            print(f"Failed to create transaction: {response.text}")
            return
        transaction = response.json()
        transaction_id = transaction["id"]
        print(f"Created transaction with ID: {transaction_id}")
        print(f"Transaction data: {transaction}")

        # 3. Get transaction
        response = await client.get(f"{BASE_URL}/transactions/{transaction_id}")
        if response.status_code != 200:
            print(f"Failed to get transaction: {response.text}")
            return
        print(f"Retrieved transaction: {response.json()}")

        # 4. Update transaction
        update_data = {
            "narration": "Updated Transaction"
        }
        response = await client.put(f"{BASE_URL}/transactions/{transaction_id}", json=update_data)
        if response.status_code != 200:
            print(f"Failed to update transaction: {response.text}")
            return
        print(f"Updated transaction: {response.json()}")

        # 5. Delete transaction
        response = await client.delete(f"{BASE_URL}/transactions/{transaction_id}")
        if response.status_code != 200:
            print(f"Failed to delete transaction: {response.text}")
            return
        print("Deleted transaction")

        # 6. Clean up account
        await client.delete(f"{BASE_URL}/accounts/{account_id}")
        print("Deleted account")

if __name__ == "__main__":
    asyncio.run(main())
