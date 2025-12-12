import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=== Testing Transaction-Category Relationship ===\n")
        
        # 1. Create transaction without categories (should default to 'others')
        print("1. Creating transaction without categories...")
        tx_data = {
            "account_id": 1,
            "date": datetime.now().isoformat(),
            "narration": "Test default category",
            "withdrawal_amount": 100.00,
            "deposit_amount": 0.00
        }
        response = await client.post(f"{BASE_URL}/transactions/", json=tx_data)
        if response.status_code != 200:
            print(f"❌ Failed to create transaction: {response.text}")
            return
        
        tx1 = response.json()
        print(f"✓ Created transaction ID: {tx1['id']}")
        
        # Verify categories
        categories = tx1.get("categories", [])
        others_cat = next((c for c in categories if c["name"] == "others"), None)
        
        if others_cat:
            print(f"✓ Transaction correctly assigned to 'others' category")
            print(f"  Categories: {[c['name'] for c in categories]}\n")
        else:
            print(f"❌ Transaction NOT assigned to 'others' category")
            print(f"  Categories: {[c['name'] for c in categories]}\n")

        # 2. Create transaction with specific categories
        # First get some categories
        print("2. Getting available categories...")
        response = await client.get(f"{BASE_URL}/categories/")
        all_cats = response.json()
        
        # Create a new category if needed
        food_cat = next((c for c in all_cats if c["name"] == "Food"), None)
        if not food_cat:
            print("  Creating 'Food' category...")
            response = await client.post(f"{BASE_URL}/categories/", json={"name": "Food", "description": "Food items"})
            food_cat = response.json()
            
        print(f"  Using category: {food_cat['name']} (ID: {food_cat['id']})")
        
        print("3. Creating transaction with specific category...")
        tx_data2 = {
            "account_id": 1,
            "date": datetime.now().isoformat(),
            "narration": "Test specific category",
            "withdrawal_amount": 50.00,
            "deposit_amount": 0.00,
            "category_ids": [food_cat["id"]]
        }
        response = await client.post(f"{BASE_URL}/transactions/", json=tx_data2)
        if response.status_code != 200:
            print(f"❌ Failed to create transaction: {response.text}")
            return
            
        tx2 = response.json()
        print(f"✓ Created transaction ID: {tx2['id']}")
        
        # Verify categories
        categories = tx2.get("categories", [])
        has_food = any(c["id"] == food_cat["id"] for c in categories)
        
        if has_food:
            print(f"✓ Transaction correctly assigned to '{food_cat['name']}' category")
            print(f"  Categories: {[c['name'] for c in categories]}\n")
        else:
            print(f"❌ Transaction NOT assigned to '{food_cat['name']}' category")
            print(f"  Categories: {[c['name'] for c in categories]}\n")

        # 3. Verify existing transactions
        print("4. Verifying existing transactions...")
        response = await client.get(f"{BASE_URL}/transactions/")
        transactions = response.json()
        
        # Check a few transactions
        count_others = 0
        for tx in transactions[:5]:
            cats = tx.get("categories", [])
            if any(c["name"] == "others" for c in cats):
                count_others += 1
                
        print(f"✓ Checked first {min(5, len(transactions))} transactions")
        print(f"  Found 'others' category in {count_others} of them")
        
        print("\n=== All tests completed! ===")

if __name__ == "__main__":
    asyncio.run(main())
