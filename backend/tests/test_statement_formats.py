import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=== Testing Statement Format CRUD Operations ===\n")
        
        # 1. Create a statement format
        print("1. Creating a new statement format...")
        format_data = {
            "format_name": "HDFC Bank Standard Format",
            "bank_name": "HDFC Bank",
            "data_start_row": 15,
            "date_column": "A",
            "narration_column": "C",
            "withdrawal_column": "D",
            "deposit_column": "E"
        }
        response = await client.post(f"{BASE_URL}/statement-formats/", json=format_data)
        if response.status_code != 200:
            print(f"❌ Failed to create statement format: {response.text}")
            return
        format1 = response.json()
        format_id = format1["id"]
        print(f"✓ Created statement format with ID: {format_id}")
        print(f"  Data: {format1}\n")

        # 2. Create another statement format
        print("2. Creating another statement format...")
        format_data2 = {
            "format_name": "ICICI Bank Standard Format",
            "bank_name": "ICICI Bank",
            "data_start_row": 12,
            "date_column": "Date",
            "narration_column": "Description",
            "withdrawal_column": "Withdrawal",
            "deposit_column": "Deposit"
        }
        response = await client.post(f"{BASE_URL}/statement-formats/", json=format_data2)
        if response.status_code != 200:
            print(f"❌ Failed to create second statement format: {response.text}")
            return
        format2 = response.json()
        format_id2 = format2["id"]
        print(f"✓ Created statement format with ID: {format_id2}\n")

        # 3. List all statement formats
        print("3. Listing all statement formats...")
        response = await client.get(f"{BASE_URL}/statement-formats/")
        if response.status_code != 200:
            print(f"❌ Failed to list statement formats: {response.text}")
            return
        formats = response.json()
        print(f"✓ Retrieved {len(formats)} statement format(s)")
        for fmt in formats:
            print(f"  - {fmt['format_name']} (ID: {fmt['id']})")
        print()

        # 4. Get specific statement format
        print(f"4. Getting statement format {format_id}...")
        response = await client.get(f"{BASE_URL}/statement-formats/{format_id}")
        if response.status_code != 200:
            print(f"❌ Failed to get statement format: {response.text}")
            return
        retrieved_format = response.json()
        print(f"✓ Retrieved statement format: {retrieved_format['format_name']}")
        print(f"  Data start row: {retrieved_format['data_start_row']}")
        print(f"  Date column: {retrieved_format['date_column']}")
        print(f"  Narration column: {retrieved_format['narration_column']}\n")

        # 5. Update statement format
        print(f"5. Updating statement format {format_id}...")
        update_data = {
            "data_start_row": 20,
            "date_column": "Transaction Date"
        }
        response = await client.put(f"{BASE_URL}/statement-formats/{format_id}", json=update_data)
        if response.status_code != 200:
            print(f"❌ Failed to update statement format: {response.text}")
            return
        updated_format = response.json()
        print(f"✓ Updated statement format:")
        print(f"  Data start row: {updated_format['data_start_row']} (was 15)")
        print(f"  Date column: {updated_format['date_column']} (was A)\n")

        # 6. Delete first statement format
        print(f"6. Deleting statement format {format_id}...")
        response = await client.delete(f"{BASE_URL}/statement-formats/{format_id}")
        if response.status_code != 200:
            print(f"❌ Failed to delete statement format: {response.text}")
            return
        print(f"✓ Deleted statement format {format_id}\n")

        # 7. Verify deletion
        print(f"7. Verifying deletion of format {format_id}...")
        response = await client.get(f"{BASE_URL}/statement-formats/{format_id}")
        if response.status_code == 404:
            print(f"✓ Statement format {format_id} properly deleted (404 Not Found)\n")
        else:
            print(f"❌ Statement format still exists: {response.status_code}\n")

        # 8. Clean up - delete second format
        print(f"8. Cleaning up - deleting format {format_id2}...")
        await client.delete(f"{BASE_URL}/statement-formats/{format_id2}")
        print(f"✓ Deleted statement format {format_id2}\n")

        print("=== All tests completed successfully! ✓ ===")

if __name__ == "__main__":
    asyncio.run(main())

