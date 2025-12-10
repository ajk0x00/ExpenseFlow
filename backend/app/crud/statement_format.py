from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.statement_format import StatementFormat
from app.schemas.statement_format import StatementFormatCreate, StatementFormatUpdate


async def get(db: AsyncSession, id: int) -> Optional[StatementFormat]:
    """Get a statement format by ID"""
    result = await db.execute(select(StatementFormat).filter(StatementFormat.id == id))
    return result.scalars().first()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[StatementFormat]:
    """Get all statement formats with pagination"""
    result = await db.execute(select(StatementFormat).offset(skip).limit(limit))
    return result.scalars().all()


async def create(db: AsyncSession, obj_in: StatementFormatCreate) -> StatementFormat:
    """Create a new statement format"""
    db_obj = StatementFormat(
        format_name=obj_in.format_name,
        bank_name=obj_in.bank_name,
        data_start_row=obj_in.data_start_row,
        date_column=obj_in.date_column,
        narration_column=obj_in.narration_column,
        withdrawal_column=obj_in.withdrawal_column,
        deposit_column=obj_in.deposit_column,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, *, db_obj: StatementFormat, obj_in: StatementFormatUpdate) -> StatementFormat:
    """Update an existing statement format"""
    update_data = obj_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, *, id: int) -> StatementFormat:
    """Delete a statement format"""
    result = await db.execute(select(StatementFormat).filter(StatementFormat.id == id))
    obj = result.scalars().first()
    await db.delete(obj)
    await db.commit()
    return obj

