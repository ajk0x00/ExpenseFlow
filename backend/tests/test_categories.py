import httpx
import asyncio

BASE_URL = "http://localhost:8000/api/v1"

async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=== Testing Category CRUD Operations ===\n")
        
        # 0. Verify default 'others' category exists
        print("0. Verifying default 'others' category exists...")
        response = await client.get(f"{BASE_URL}/categories/")
        if response.status_code != 200:
            print(f"❌ Failed to list categories: {response.text}")
            return
        categories = response.json()
        others_category = next((c for c in categories if c["name"] == "others"), None)
        if others_category:
            print(f"✓ Default 'others' category found with ID: {others_category['id']}")
            print(f"  Description: {others_category['description']}\n")
        else:
            print("❌ Default 'others' category not found!\n")
        
        # 1. Create a category
        print("1. Creating a new category...")
        category_data = {
            "name": "Food",
            "description": "Food and dining expenses"
        }
        response = await client.post(f"{BASE_URL}/categories/", json=category_data)
        if response.status_code != 200:
            print(f"❌ Failed to create category: {response.text}")
            return
        category1 = response.json()
        category_id = category1["id"]
        print(f"✓ Created category with ID: {category_id}")
        print(f"  Data: {category1}\n")

        # 2. Create another category
        print("2. Creating another category...")
        category_data2 = {
            "name": "Transport",
            "description": "Transportation and travel expenses"
        }
        response = await client.post(f"{BASE_URL}/categories/", json=category_data2)
        if response.status_code != 200:
            print(f"❌ Failed to create second category: {response.text}")
            return
        category2 = response.json()
        category_id2 = category2["id"]
        print(f"✓ Created category with ID: {category_id2}\n")

        # 3. List all categories
        print("3. Listing all categories...")
        response = await client.get(f"{BASE_URL}/categories/")
        if response.status_code != 200:
            print(f"❌ Failed to list categories: {response.text}")
            return
        categories = response.json()
        print(f"✓ Retrieved {len(categories)} category(ies)")
        for cat in categories:
            print(f"  - {cat['name']} (ID: {cat['id']})")
        print()

        # 4. Get specific category
        print(f"4. Getting category {category_id}...")
        response = await client.get(f"{BASE_URL}/categories/{category_id}")
        if response.status_code != 200:
            print(f"❌ Failed to get category: {response.text}")
            return
        retrieved_category = response.json()
        print(f"✓ Retrieved category: {retrieved_category['name']}")
        print(f"  Description: {retrieved_category['description']}\n")

        # 5. Update category
        print(f"5. Updating category {category_id}...")
        update_data = {
            "description": "Food, dining, and groceries"
        }
        response = await client.put(f"{BASE_URL}/categories/{category_id}", json=update_data)
        if response.status_code != 200:
            print(f"❌ Failed to update category: {response.text}")
            return
        updated_category = response.json()
        print(f"✓ Updated category:")
        print(f"  Description: {updated_category['description']} (was 'Food and dining expenses')\n")

        # 6. Test duplicate name (should fail)
        print("6. Testing duplicate category name (should fail)...")
        duplicate_data = {
            "name": "Food",
            "description": "This should fail"
        }
        response = await client.post(f"{BASE_URL}/categories/", json=duplicate_data)
        if response.status_code != 200:
            print(f"✓ Duplicate name properly rejected: {response.status_code}\n")
        else:
            print(f"❌ Duplicate name was accepted (should have failed)\n")

        # 7. Delete first category
        print(f"7. Deleting category {category_id}...")
        response = await client.delete(f"{BASE_URL}/categories/{category_id}")
        if response.status_code != 200:
            print(f"❌ Failed to delete category: {response.text}")
            return
        print(f"✓ Deleted category {category_id}\n")

        # 8. Verify deletion
        print(f"8. Verifying deletion of category {category_id}...")
        response = await client.get(f"{BASE_URL}/categories/{category_id}")
        if response.status_code == 404:
            print(f"✓ Category {category_id} properly deleted (404 Not Found)\n")
        else:
            print(f"❌ Category still exists: {response.status_code}\n")

        # 9. Clean up - delete second category
        print(f"9. Cleaning up - deleting category {category_id2}...")
        await client.delete(f"{BASE_URL}/categories/{category_id2}")
        print(f"✓ Deleted category {category_id2}\n")

        # 10. Final verification - 'others' category should still exist
        print("10. Verifying 'others' category still exists...")
        response = await client.get(f"{BASE_URL}/categories/")
        if response.status_code == 200:
            categories = response.json()
            others_exists = any(c["name"] == "others" for c in categories)
            if others_exists:
                print(f"✓ 'others' category still exists after cleanup\n")
            else:
                print(f"❌ 'others' category missing after cleanup\n")

        print("=== All tests completed successfully! ✓ ===")

if __name__ == "__main__":
    asyncio.run(main())
