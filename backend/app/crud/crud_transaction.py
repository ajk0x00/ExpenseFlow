from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

async def get(db: AsyncSession, id: int) -> Optional[Transaction]:
    result = await db.execute(select(Transaction).filter(Transaction.id == id))
    return result.scalars().first()

async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Transaction]:
    result = await db.execute(select(Transaction).offset(skip).limit(limit))
    return result.scalars().all()

async def create(db: AsyncSession, obj_in: TransactionCreate) -> Transaction:
    db_obj = Transaction(
        account_id=obj_in.account_id,
        date=obj_in.date,
        narration=obj_in.narration,
        withdrawal_amount=obj_in.withdrawal_amount,
        deposit_amount=obj_in.deposit_amount,
        metadata_=obj_in.metadata_,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def update(db: AsyncSession, *, db_obj: Transaction, obj_in: TransactionUpdate) -> Transaction:
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj

async def remove(db: AsyncSession, *, id: int) -> Transaction:
    result = await db.execute(select(Transaction).filter(Transaction.id == id))
    obj = result.scalars().first()
    await db.delete(obj)
    await db.commit()
    return obj
