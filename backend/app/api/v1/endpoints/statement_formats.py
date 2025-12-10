from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.statement_format import StatementFormat, StatementFormatCreate, StatementFormatUpdate
from app.crud import crud_statement_format

router = APIRouter()

@router.get("/", response_model=List[StatementFormat])
async def read_statement_formats(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Retrieve statement formats.
    """
    statement_formats = await crud_statement_format.get_multi(db, skip=skip, limit=limit)
    return statement_formats

@router.post("/", response_model=StatementFormat)
async def create_statement_format(
    *,
    db: AsyncSession = Depends(get_db),
    statement_format_in: StatementFormatCreate,
) -> Any:
    """
    Create new statement format.
    """
    statement_format = await crud_statement_format.create(db=db, obj_in=statement_format_in)
    return statement_format

@router.get("/{id}", response_model=StatementFormat)
async def read_statement_format(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Get statement format by ID.
    """
    statement_format = await crud_statement_format.get(db=db, id=id)
    if not statement_format:
        raise HTTPException(status_code=404, detail="Statement format not found")
    return statement_format

@router.put("/{id}", response_model=StatementFormat)
async def update_statement_format(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
    statement_format_in: StatementFormatUpdate,
) -> Any:
    """
    Update a statement format.
    """
    statement_format = await crud_statement_format.get(db=db, id=id)
    if not statement_format:
        raise HTTPException(status_code=404, detail="Statement format not found")
    statement_format = await crud_statement_format.update(db=db, db_obj=statement_format, obj_in=statement_format_in)
    return statement_format

@router.delete("/{id}", response_model=StatementFormat)
async def delete_statement_format(
    *,
    db: AsyncSession = Depends(get_db),
    id: int,
) -> Any:
    """
    Delete a statement format.
    """
    statement_format = await crud_statement_format.get(db=db, id=id)
    if not statement_format:
        raise HTTPException(status_code=404, detail="Statement format not found")
    statement_format = await crud_statement_format.remove(db=db, id=id)
    return statement_format
