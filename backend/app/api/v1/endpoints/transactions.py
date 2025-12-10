from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import crud_transaction
from app.schemas.transaction import Transaction, TransactionCreate, TransactionUpdate

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
