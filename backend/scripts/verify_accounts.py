import httpx
import json

BASE_URL = "http://localhost:8000/api/v1/accounts"

def test_create_account():
    print("Testing Create Account...")
    data = {
        "account_name": "My Savings",
        "bank_name": "Chase",
        "description": "Emergency fund",
        "account_type": "debit",
        "metadata_": {"interest_rate": 0.01}
    }
    with httpx.Client(timeout=30.0) as client:
        response = client.post(BASE_URL + "/", json=data)
        if response.status_code == 200:
            print("Create Success:", response.json())
            return response.json()["id"]
        else:
            print("Create Failed:", response.text)
            return None

def test_get_accounts():
    print("\nTesting Get Accounts...")
    with httpx.Client(timeout=30.0) as client:
        response = client.get(BASE_URL + "/")
        if response.status_code == 200:
            print("Get All Success:", len(response.json()), "accounts found")
        else:
            print("Get All Failed:", response.text)

def test_get_account(id):
    print(f"\nTesting Get Account {id}...")
    with httpx.Client(timeout=30.0) as client:
        response = client.get(f"{BASE_URL}/{id}")
        if response.status_code == 200:
            print("Get One Success:", response.json())
        else:
            print("Get One Failed:", response.text)

def test_update_account(id):
    print(f"\nTesting Update Account {id}...")
    data = {
        "account_name": "My Updated Savings",
        "account_type": "credit"
    }
    with httpx.Client(timeout=30.0) as client:
        response = client.put(f"{BASE_URL}/{id}", json=data)
        if response.status_code == 200:
            print("Update Success:", response.json())
        else:
            print("Update Failed:", response.text)

def test_delete_account(id):
    print(f"\nTesting Delete Account {id}...")
    with httpx.Client(timeout=30.0) as client:
        response = client.delete(f"{BASE_URL}/{id}")
        if response.status_code == 200:
            print("Delete Success:", response.json())
        else:
            print("Delete Failed:", response.text)

if __name__ == "__main__":
    account_id = test_create_account()
    if account_id:
        test_get_accounts()
        test_get_account(account_id)
        test_update_account(account_id)
        test_delete_account(account_id)
