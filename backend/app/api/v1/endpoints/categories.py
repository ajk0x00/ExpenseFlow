from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.crud import crud_category
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.get("/", response_model=List[Category])
async def read_categories(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.
    """
    categories = await crud_category.get_multi(db, skip=skip, limit=limit)
    return categories


@router.post("/", response_model=Category)
async def create_category(
    *,
    db: AsyncSession = Depends(get_db),
    category_in: CategoryCreate,
) -> Any:
    """
    Create new category.
    """
    category = await crud_category.create(db=db, obj_in=category_in)
    return category


@router.get("/{id}", response_model=Category)
async def read_category(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Get category by ID.
    """
    category = await crud_category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{id}", response_model=Category)
async def update_category(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    category_in: CategoryUpdate,
) -> Any:
    """
    Update a category.
    """
    category = await crud_category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = await crud_category.update(db=db, db_obj=category, obj_in=category_in)
    return category


@router.delete("/{id}", response_model=Category)
async def delete_category(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Delete a category.
    """
    category = await crud_category.get(db=db, id=id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category = await crud_category.remove(db=db, id=id)
    return category
