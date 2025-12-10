"""
Bank Statement Parser Service

This service extracts transaction data from XLSX/XLS bank statement files
using StatementFormat configuration.
"""
import xlrd
from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from dateutil import parser as date_parser

from app.models.statement_format import StatementFormat
from app.schemas.transaction import TransactionCreate


def column_letter_to_index(letter: str) -> int:
    """
    Convert Excel column letter to 0-based index.
    
    Examples:
        A -> 0
        B -> 1
        Z -> 25
        AA -> 26
    """
    result = 0
    for char in letter.upper():
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1


def get_column_index(sheet: xlrd.sheet.Sheet, column_ref: str, workbook) -> int:
    """
    Resolve column reference to 0-based index.
    
    Supports:
    - Column letters: "A", "B", "C"
    - Column names: "Date", "Narration" (searches header row)
    - Numeric strings: "0", "1" (direct index)
    
    Args:
        sheet: The worksheet
        column_ref: Column reference (letter, name, or index)
        workbook: The workbook (for date handling)
        
    Returns:
        0-based column index
    """
    # Check if it's a column letter (A, B, C, etc.)
    if column_ref.upper().isalpha():
        return column_letter_to_index(column_ref)
    
    # Check if it's a numeric index
    if column_ref.isdigit():
        return int(column_ref)
    
    # Otherwise, search for column name in header rows (first 10 rows)
    for row_idx in range(min(10, sheet.nrows)):
        for col_idx in range(sheet.ncols):
            cell_value = str(sheet.cell(row_idx, col_idx).value).strip()
            if cell_value.lower() == column_ref.lower():
                return col_idx
    
    raise ValueError(f"Could not resolve column reference: {column_ref}")


def parse_date(value, workbook) -> Optional[datetime]:
    """
    Parse date value from Excel cell.
    
    Args:
        value: Cell value (can be Excel date number or string)
        workbook: Workbook for date mode
        
    Returns:
        datetime object or None if empty
    """
    if not value:
        return None
    
    # If it's an Excel date number
    if isinstance(value, float):
        try:
            date_tuple = xlrd.xldate_as_tuple(value, workbook.datemode)
            return datetime(*date_tuple)
        except:
            pass
    
    # If it's a string, try to parse it
    if isinstance(value, str):
        try:
            # Try common date formats
            return date_parser.parse(value, dayfirst=True)  # DD/MM/YYYY format common in India
        except:
            pass
    
    return None


def parse_amount(value) -> Decimal:
    """
    Parse amount value from Excel cell.
    
    Args:
        value: Cell value (number or string)
        
    Returns:
        Decimal amount (0.00 if empty or invalid)
    """
    if not value:
        return Decimal('0.00')
    
    try:
        if isinstance(value, (int, float)):
            return Decimal(str(value))
        
        # Remove common formatting characters
        cleaned = str(value).replace(',', '').replace(' ', '').strip()
        if cleaned:
            return Decimal(cleaned)
    except:
        pass
    
    return Decimal('0.00')


def is_separator_row(sheet: xlrd.sheet.Sheet, row_idx: int) -> bool:
    """
    Check if a row is a separator row (contains only asterisks or dashes).
    
    Args:
        sheet: The worksheet
        row_idx: Row index
        
    Returns:
        True if row is a separator
    """
    for col_idx in range(sheet.ncols):
        value = str(sheet.cell(row_idx, col_idx).value).strip()
        if value and not all(c in '*-=' for c in value):
            return False
    return True


def extract_transactions(
    file_path: str, 
    statement_format: StatementFormat,
    account_id: int
) -> List[TransactionCreate]:
    """
    Extract transactions from XLS/XLSX file using StatementFormat configuration.
    
    Args:
        file_path: Path to the XLS/XLSX file
        statement_format: StatementFormat object with parsing configuration
        account_id: Account ID to associate transactions with
        
    Returns:
        List of TransactionCreate objects
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If column references are invalid
    """
    transactions = []
    
    try:
        # Open workbook
        workbook = xlrd.open_workbook(file_path)
        sheet = workbook.sheet_by_index(0)
        
        # Resolve column indices
        date_col = get_column_index(sheet, statement_format.date_column, workbook)
        narration_col = get_column_index(sheet, statement_format.narration_column, workbook)
        withdrawal_col = get_column_index(sheet, statement_format.withdrawal_column, workbook)
        deposit_col = get_column_index(sheet, statement_format.deposit_column, workbook)
        
        # Start from configured row (1-indexed in config, 0-indexed in code)
        start_row = statement_format.data_start_row - 1
        
        print(f"Extracting from row {statement_format.data_start_row} (0-based: {start_row})")
        print(f"Column indices - Date: {date_col}, Narration: {narration_col}, "
              f"Withdrawal: {withdrawal_col}, Deposit: {deposit_col}")
        
        # Process each row
        for row_idx in range(start_row, sheet.nrows):
            # Skip separator rows
            if is_separator_row(sheet, row_idx):
                continue
            
            # Get cell values
            date_value = sheet.cell(row_idx, date_col).value
            narration_value = sheet.cell(row_idx, narration_col).value
            withdrawal_value = sheet.cell(row_idx, withdrawal_col).value
            deposit_value = sheet.cell(row_idx, deposit_col).value
            
            # Parse values
            transaction_date = parse_date(date_value, workbook)
            narration = str(narration_value).strip() if narration_value else ""
            withdrawal_amount = parse_amount(withdrawal_value)
            deposit_amount = parse_amount(deposit_value)
            
            # Skip if no valid date or narration (likely end of data)
            if not transaction_date or not narration:
                continue
            
            # Skip summary rows or non-transaction rows
            if any(keyword in narration.lower() for keyword in ['statement', 'summary', 'opening', 'closing', 'balance', 'generated']):
                continue
            
            # Create transaction object
            transaction = TransactionCreate(
                account_id=account_id,
                date=transaction_date,
                narration=narration,
                withdrawal_amount=withdrawal_amount,
                deposit_amount=deposit_amount,
                metadata_={
                    'source': 'imported',
                    'file': file_path.split('/')[-1]
                }
            )
            
            transactions.append(transaction)
            print(f"Row {row_idx + 1}: {transaction_date:%Y-%m-%d} | {narration[:50]} | "
                  f"W: {withdrawal_amount} | D: {deposit_amount}")
        
        print(f"\nExtracted {len(transactions)} transactions")
        return transactions
        
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error extracting transactions: {str(e)}")
