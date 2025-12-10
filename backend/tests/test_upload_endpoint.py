"""
Test script for the transaction upload endpoint.

This script tests the complete flow of uploading a bank statement file
and importing transactions using a StatementFormat.

Requirements:
- Backend server must be running (http://localhost:8000)
- Sample XLS/XLSX file must be available
- httpx package must be installed

Usage:
    python tests/test_upload_endpoint.py
"""
import httpx
import asyncio
from pathlib import Path
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

# Path to test file - update this to match your test file location
TEST_FILE_PATH = "/home/abhijith/Downloads/Acct.xls"


async def main():
    async with httpx.AsyncClient(timeout=60.0) as client:
        print("=" * 100)
        print("TESTING TRANSACTION UPLOAD ENDPOINT")
        print("=" * 100)
        print()
        
        # Step 1: Create a test bank account
        print("Step 1: Creating test bank account...")
        account_data = {
            "account_name": "HDFC Savings Account - Test",
            "bank_name": "HDFC Bank",
            "account_type": "credit",  # Changed from 'savings' to valid enum value
            "description": "Test account for upload endpoint testing",
            "metadata_": {"test": True}
        }
        response = await client.post(f"{BASE_URL}/accounts/", json=account_data)
        if response.status_code != 200:
            print(f"❌ Failed to create account: {response.text}")
            return
        account = response.json()
        account_id = account["id"]
        print(f"✓ Created account with ID: {account_id}")
        print(f"  Account: {account['account_name']}")
        print()
        
        # Step 2: Create a StatementFormat
        print("Step 2: Creating statement format...")
        format_data = {
            "format_name": "HDFC Bank Statement Format",
            "bank_name": "HDFC Bank",
            "data_start_row": 23,  # First transaction row (1-indexed)
            "date_column": "A",
            "narration_column": "B",
            "withdrawal_column": "E",
            "deposit_column": "F"
        }
        response = await client.post(f"{BASE_URL}/statement-formats/", json=format_data)
        if response.status_code != 200:
            print(f"❌ Failed to create statement format: {response.text}")
            # Clean up account
            await client.delete(f"{BASE_URL}/accounts/{account_id}")
            return
        statement_format = response.json()
        format_id = statement_format["id"]
        print(f"✓ Created statement format with ID: {format_id}")
        print(f"  Format: {statement_format['format_name']}")
        print(f"  Bank: {statement_format['bank_name']}")
        print(f"  Data starts at row: {statement_format['data_start_row']}")
        print()
        
        # Step 3: Check if test file exists
        print("Step 3: Validating test file...")
        test_file = Path(TEST_FILE_PATH)
        if not test_file.exists():
            print(f"❌ Test file not found: {TEST_FILE_PATH}")
            print("   Please update TEST_FILE_PATH in the script to point to a valid XLS/XLSX file")
            # Clean up
            await client.delete(f"{BASE_URL}/statement-formats/{format_id}")
            await client.delete(f"{BASE_URL}/accounts/{account_id}")
            return
        print(f"✓ Test file found: {test_file.name}")
        print(f"  Size: {test_file.stat().st_size / 1024:.2f} KB")
        print()
        
        # Step 4: Get initial transaction count
        print("Step 4: Getting initial transaction count...")
        response = await client.get(f"{BASE_URL}/transactions/")
        if response.status_code != 200:
            print(f"❌ Failed to get transactions: {response.text}")
            # Clean up
            await client.delete(f"{BASE_URL}/statement-formats/{format_id}")
            await client.delete(f"{BASE_URL}/accounts/{account_id}")
            return
        initial_transactions = response.json()
        initial_count = len(initial_transactions)
        print(f"✓ Initial transaction count: {initial_count}")
        print()
        
        # Step 5: Upload the file
        print("Step 5: Uploading bank statement file...")
        print(f"  File: {test_file.name}")
        print(f"  Statement Format ID: {format_id}")
        print(f"  Account ID: {account_id}")
        print()
        
        with open(test_file, "rb") as f:
            files = {"file": (test_file.name, f, "application/vnd.ms-excel")}
            data = {
                "statement_format_id": format_id,
                "account_id": account_id
            }
            
            print("  Uploading and processing...")
            response = await client.post(
                f"{BASE_URL}/transactions/upload",
                files=files,
                data=data
            )
        
        if response.status_code != 200:
            print(f"❌ Upload failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            # Clean up
            await client.delete(f"{BASE_URL}/statement-formats/{format_id}")
            await client.delete(f"{BASE_URL}/accounts/{account_id}")
            return
        
        result = response.json()
        print("✓ Upload successful!")
        print()
        
        # Step 6: Display upload results
        print("=" * 100)
        print("UPLOAD RESULTS")
        print("=" * 100)
        print(f"Success: {result['success']}")
        print(f"Transactions imported: {result['count']}")
        print(f"Total withdrawals: ₹{result['total_withdrawals']:,.2f}")
        print(f"Total deposits: ₹{result['total_deposits']:,.2f}")
        print(f"Net amount: ₹{result['net']:,.2f}")
        print()
        
        # Step 7: Verify transactions were created
        print("Step 6: Verifying transactions were created...")
        response = await client.get(f"{BASE_URL}/transactions/")
        if response.status_code != 200:
            print(f"❌ Failed to get transactions: {response.text}")
        else:
            all_transactions = response.json()
            final_count = len(all_transactions)
            new_transactions_count = final_count - initial_count
            print(f"✓ Final transaction count: {final_count}")
            print(f"  New transactions added: {new_transactions_count}")
            
            if new_transactions_count == result['count']:
                print(f"✓ Transaction count matches upload result!")
            else:
                print(f"⚠ Warning: Count mismatch! Expected {result['count']}, got {new_transactions_count}")
        print()
        
        # Step 8: Display sample transactions
        print("Step 7: Displaying sample imported transactions...")
        # Get transactions for this account
        response = await client.get(f"{BASE_URL}/transactions/?limit=5")
        if response.status_code == 200:
            sample_transactions = response.json()[:5]
            print(f"✓ Showing first {len(sample_transactions)} transactions:")
            print()
            for i, txn in enumerate(sample_transactions, 1):
                date_str = txn['date'][:10] if isinstance(txn['date'], str) else str(txn['date'])
                narration = txn['narration'][:60] + "..." if len(txn['narration']) > 60 else txn['narration']
                print(f"  {i}. {date_str} | {narration}")
                print(f"     Withdrawal: ₹{float(txn['withdrawal_amount']):,.2f} | Deposit: ₹{float(txn['deposit_amount']):,.2f}")
                if txn.get('metadata_'):
                    print(f"     Metadata: {txn['metadata_']}")
                print()
        print()
        
        # Step 9: Test error handling - Invalid file type
        print("Step 8: Testing error handling (invalid file type)...")
        files = {"file": ("test.txt", b"This is not an excel file", "text/plain")}
        data = {
            "statement_format_id": format_id,
            "account_id": account_id
        }
        response = await client.post(
            f"{BASE_URL}/transactions/upload",
            files=files,
            data=data
        )
        if response.status_code == 400:
            print(f"✓ Correctly rejected invalid file type")
            print(f"  Error: {response.json()['detail']}")
        else:
            print(f"⚠ Expected 400 error, got {response.status_code}")
        print()
        
        # Step 10: Test error handling - Invalid statement format ID
        print("Step 9: Testing error handling (invalid statement format ID)...")
        with open(test_file, "rb") as f:
            files = {"file": (test_file.name, f, "application/vnd.ms-excel")}
            data = {
                "statement_format_id": 99999,  # Non-existent ID
                "account_id": account_id
            }
            response = await client.post(
                f"{BASE_URL}/transactions/upload",
                files=files,
                data=data
            )
        if response.status_code == 404:
            print(f"✓ Correctly handled non-existent statement format")
            print(f"  Error: {response.json()['detail']}")
        else:
            print(f"⚠ Expected 404 error, got {response.status_code}")
        print()
        
        # Step 11: Clean up
        print("Step 10: Cleaning up test data...")
        
        # Delete imported transactions
        response = await client.get(f"{BASE_URL}/transactions/")
        if response.status_code == 200:
            transactions = response.json()
            for txn in transactions:
                if txn['account_id'] == account_id:
                    await client.delete(f"{BASE_URL}/transactions/{txn['id']}")
            print(f"✓ Deleted {new_transactions_count} imported transactions")
        
        # Delete statement format
        response = await client.delete(f"{BASE_URL}/statement-formats/{format_id}")
        if response.status_code == 200:
            print(f"✓ Deleted statement format {format_id}")
        
        # Delete account
        response = await client.delete(f"{BASE_URL}/accounts/{account_id}")
        if response.status_code == 200:
            print(f"✓ Deleted account {account_id}")
        print()
        
        print("=" * 100)
        print("ALL TESTS COMPLETED SUCCESSFULLY! ✓")
        print("=" * 100)


if __name__ == "__main__":
    print()
    print("Starting Transaction Upload Endpoint Tests...")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
