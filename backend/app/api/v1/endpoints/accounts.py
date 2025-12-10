from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.account import BankAccount, BankAccountCreate, BankAccountUpdate
from app.crud import crud_account

router = APIRouter()

@router.get("/", response_model=List[BankAccount])
async def read_accounts(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Retrieve accounts.
    """
    accounts = await crud_account.get_multi(db, skip=skip, limit=limit)
    return accounts

@router.post("/", response_model=BankAccount)
async def create_account(
    *,
    db: AsyncSession = Depends(get_db),
    account_in: BankAccountCreate,
) -> Any:
    """
    Create new account.
    """
    account = await crud_account.create(db=db, obj_in=account_in)
    return account

@router.get("/{id}", response_model=BankAccount)
async def read_account(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Get account by ID.
    """
    account = await crud_account.get(db=db, id=id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{id}", response_model=BankAccount)
async def update_account(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    account_in: BankAccountUpdate,
) -> Any:
    """
    Update an account.
    """
    account = await crud_account.get(db=db, id=id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account = await crud_account.update(db=db, db_obj=account, obj_in=account_in)
    return account

@router.delete("/{id}", response_model=BankAccount)
async def delete_account(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Delete an account.
    """
    account = await crud_account.get(db=db, id=id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account = await crud_account.remove(db=db, id=id)
    return account
