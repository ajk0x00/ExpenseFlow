"""
Test script to extract transactions from Acct_tr.xls

This script:
1. Identifies the StatementFormat values from the file
2. Creates a StatementFormat object
3. Extracts transactions using the parser service
"""
import sys
sys.path.insert(0, '/home/abhijith/work/expense-tracker/backend')

from app.services.statement_parser import extract_transactions
from app.models.statement_format import StatementFormat

def main():
    print("="*100)
    print("STEP 1: Identify StatementFormat Values from Acct_tr.xls")
    print("="*100)
    
    # Based on analysis of the file:
    # Row 21: Headers - Date | Narration | Chq./Ref.No. | Value Dt | Withdrawal Amt. | Deposit Amt. | Closing Balance
    # Row 22: Separator
    # Row 23: First transaction data
    
    format_config = {
        "format_name": "HDFC Bank Statement Format",
        "bank_name": "HDFC Bank",
        "data_start_row": 23,  # First transaction row (1-indexed)
        "date_column": "A",    # Column A contains Date
        "narration_column": "B",  # Column B contains Narration
        "withdrawal_column": "E",  # Column E contains Withdrawal Amt.
        "deposit_column": "F"   # Column F contains Deposit Amt.
    }
    
    print("\nIdentified StatementFormat values:")
    print(f"  format_name: {format_config['format_name']}")
    print(f"  bank_name: {format_config['bank_name']}")
    print(f"  data_start_row: {format_config['data_start_row']}")
    print(f"  date_column: {format_config['date_column']}")
    print(f"  narration_column: {format_config['narration_column']}")
    print(f"  withdrawal_column: {format_config['withdrawal_column']}")
    print(f"  deposit_column: {format_config['deposit_column']}")
    
    print("\n" + "="*100)
    print("STEP 2: Create StatementFormat Object")
    print("="*100)
    
    # Create StatementFormat object (simulating the model)
    class MockStatementFormat:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    statement_format = MockStatementFormat(**format_config)
    print("\n✓ StatementFormat object created")
    
    print("\n" + "="*100)
    print("STEP 3: Extract Transactions")
    print("="*100)
    
    file_path = "/home/abhijith/work/expense-tracker/Acct.xls"
    account_id = 1  # Test account ID
    
    try:
        transactions = extract_transactions(file_path, statement_format, account_id)
        
        print(f"\n✓ Successfully extracted {len(transactions)} transactions")
        
        print("\n" + "="*100)
        print("EXTRACTED TRANSACTIONS:")
        print("="*100)
        
        for i, txn in enumerate(transactions, 1):
            print(f"\nTransaction {i}:")
            print(f"  Date: {txn.date}")
            print(f"  Narration: {txn.narration[:80]}")
            print(f"  Withdrawal: {txn.withdrawal_amount}")
            print(f"  Deposit: {txn.deposit_amount}")
            print(f"  Metadata: {txn.metadata_}")
        
        print("\n" + "="*100)
        print("SUMMARY:")
        print("="*100)
        total_withdrawals = sum(txn.withdrawal_amount for txn in transactions)
        total_deposits = sum(txn.deposit_amount for txn in transactions)
        print(f"Total Withdrawals: {total_withdrawals}")
        print(f"Total Deposits: {total_deposits}")
        print(f"Net: {total_deposits - total_withdrawals}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
