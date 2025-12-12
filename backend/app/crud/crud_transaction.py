from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

async def get(db: AsyncSession, id: int) -> Optional[Transaction]:
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.categories))
        .filter(Transaction.id == id)
    )
    return result.scalars().first()

async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Transaction]:
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.categories))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def create(db: AsyncSession, obj_in: TransactionCreate) -> Transaction:
    """Create a new transaction with category assignment."""
    from app.models.category import Category
    
    db_obj = Transaction(
        account_id=obj_in.account_id,
        date=obj_in.date,
        narration=obj_in.narration,
        withdrawal_amount=obj_in.withdrawal_amount,
        deposit_amount=obj_in.deposit_amount,
        metadata_=obj_in.metadata_,
    )
    
    # Handle category assignment
    if obj_in.category_ids:
        # Assign specified categories
        result = await db.execute(select(Category).filter(Category.id.in_(obj_in.category_ids)))
        categories = result.scalars().all()
        db_obj.categories = list(categories)
    else:
        # Default to 'others' category
        result = await db.execute(select(Category).filter(Category.name == "others"))
        others_category = result.scalars().first()
        if others_category:
            db_obj.categories = [others_category]
    
    db.add(db_obj)
    await db.commit()
    return await get(db, db_obj.id)

async def create_bulk(db: AsyncSession, objs_in: List[TransactionCreate]) -> List[Transaction]:
    """Create multiple transactions in bulk with default 'others' category."""
    from app.models.category import Category
    
    # Get 'others' category
    result = await db.execute(select(Category).filter(Category.name == "others"))
    others_category = result.scalars().first()
    
    db_objs = [
        Transaction(
            account_id=obj_in.account_id,
            date=obj_in.date,
            narration=obj_in.narration,
            withdrawal_amount=obj_in.withdrawal_amount,
            deposit_amount=obj_in.deposit_amount,
            metadata_=obj_in.metadata_,
        )
        for obj_in in objs_in
    ]
    
    # Assign 'others' category to all transactions
    if others_category:
        for db_obj in db_objs:
            db_obj.categories = [others_category]
            
    db.add_all(db_objs)
    await db.commit()
    
    # Re-fetch all objects with eager loading
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.categories))
        .filter(Transaction.id.in_([obj.id for obj in db_objs]))
    )
    return result.scalars().all()

async def update(db: AsyncSession, *, db_obj: Transaction, obj_in: TransactionUpdate) -> Transaction:
    """Update an existing transaction including categories."""
    from app.models.category import Category
    
    update_data = obj_in.dict(exclude_unset=True)
    
    # Handle category updates separately
    category_ids = update_data.pop('category_ids', None)
    
    # Update regular fields
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    
    # Update categories if provided
    if category_ids is not None:
        if category_ids:
            result = await db.execute(select(Category).filter(Category.id.in_(category_ids)))
            categories = result.scalars().all()
            db_obj.categories = list(categories)
        else:
            # If empty list provided, clear categories (or could default to 'others')
            db_obj.categories = []
    
    db.add(db_obj)
    await db.commit()
    return await get(db, db_obj.id)

async def remove(db: AsyncSession, *, id: int) -> Transaction:
    result = await db.execute(select(Transaction).filter(Transaction.id == id))
    obj = result.scalars().first()
    await db.delete(obj)
    await db.commit()
    return obj
