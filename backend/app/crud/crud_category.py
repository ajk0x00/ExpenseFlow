from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


async def get(db: AsyncSession, id: int) -> Optional[Category]:
    """Get a category by ID."""
    result = await db.execute(select(Category).filter(Category.id == id))
    return result.scalars().first()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Category]:
    """Get multiple categories with pagination."""
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()


async def create(db: AsyncSession, obj_in: CategoryCreate) -> Category:
    """Create a new category."""
    db_obj = Category(
        name=obj_in.name,
        description=obj_in.description,
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def update(db: AsyncSession, *, db_obj: Category, obj_in: CategoryUpdate) -> Category:
    """Update an existing category."""
    update_data = obj_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(db_obj, field, update_data[field])
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


async def remove(db: AsyncSession, *, id: int) -> Category:
    """Delete a category."""
    result = await db.execute(select(Category).filter(Category.id == id))
    obj = result.scalars().first()
    await db.delete(obj)
    await db.commit()
    return obj
