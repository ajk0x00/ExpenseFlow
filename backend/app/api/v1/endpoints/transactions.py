from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
import tempfile
import os
from app.db.session import get_db
from app.crud import crud_transaction
from app.crud import statement_format as crud_statement_format
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate
from app.services.statement_parser import extract_transactions

router = APIRouter()

@router.get("/", response_model=List[Transaction])
async def read_transactions(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve transactions.
    """
    transactions = await crud_transaction.get_multi(db, skip=skip, limit=limit)
    return transactions

@router.post("/", response_model=Transaction)
async def create_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    transaction_in: TransactionCreate,
) -> Any:
    """
    Create new transaction.
    """
    transaction = await crud_transaction.create(db=db, obj_in=transaction_in)
    return transaction

@router.post("/upload", response_model=dict)
async def upload_transactions(
    *,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    statement_format_id: int = Form(...),
    account_id: int = Form(...),
) -> Any:
    """
    Upload and import transactions from bank statement file (XLSX/XLS).
    
    Args:
        file: Bank statement file (XLSX/XLS)
        statement_format_id: ID of the StatementFormat to use for parsing
        account_id: ID of the bank account to associate transactions with
        
    Returns:
        Dictionary with number of imported transactions and summary
    """
    # Validate statement format exists
    statement_format = await crud_statement_format.get(db=db, id=statement_format_id)
    if not statement_format:
        raise HTTPException(status_code=404, detail="Statement format not found")
    
    # Validate file type
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only .xls and .xlsx files are supported"
        )
    
    # Save uploaded file to temporary location
    temp_file = None
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Extract transactions using statement parser
        transactions = extract_transactions(
            file_path=temp_file_path,
            statement_format=statement_format,
            account_id=account_id
        )
        
        if not transactions:
            raise HTTPException(
                status_code=400,
                detail="No transactions found in the file"
            )
        
        # Bulk insert transactions
        created_transactions = await crud_transaction.create_bulk(db=db, objs_in=transactions)
        
        # Calculate summary
        total_withdrawals = sum(t.withdrawal_amount for t in created_transactions)
        total_deposits = sum(t.deposit_amount for t in created_transactions)
        
        return {
            "success": True,
            "count": len(created_transactions),
            "total_withdrawals": float(total_withdrawals),
            "total_deposits": float(total_deposits),
            "net": float(total_deposits - total_withdrawals)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@router.get("/{id}", response_model=Transaction)
async def read_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Get transaction by ID.
    """
    transaction = await crud_transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.put("/{id}", response_model=Transaction)
async def update_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    transaction_in: TransactionUpdate,
) -> Any:
    """
    Update a transaction.
    """
    transaction = await crud_transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction = await crud_transaction.update(db=db, db_obj=transaction, obj_in=transaction_in)
    return transaction

@router.delete("/{id}", response_model=Transaction)
async def delete_transaction(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Delete a transaction.
    """
    transaction = await crud_transaction.get(db=db, id=id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction = await crud_transaction.remove(db=db, id=id)
    return transaction
