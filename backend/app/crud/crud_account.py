from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.account import BankAccount
from app.schemas.account import BankAccountCreate, BankAccountUpdate

async def get(db: AsyncSession, id: int) -> Optional[BankAccount]:
    result = await db.execute(select(BankAccount).filter(BankAccount.id == id))
    return result.scalars().first()

async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[BankAccount]:
    result = await db.execute(select(BankAccount).offset(skip).limit(limit))
    return result.scalars().all()

async def create(db: AsyncSession, obj_in: BankAccountCreate) -> BankAccount:
    db_obj = BankAccount(
        account_name=obj_in.account_name,
        bank_name=obj_in.bank_name,
        description=obj_in.description,
        account_type=obj_in.account_type,
        metadata_=obj_in.metadata_,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, *, db_obj: BankAccount, obj_in: BankAccountUpdate) -> BankAccount:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove(db: AsyncSession, *, id: int) -> BankAccount:
    result = await db.execute(select(BankAccount).filter(BankAccount.id == id))
    obj = result.scalars().first()
    await db.delete(obj)
    await db.commit()
    return obj
