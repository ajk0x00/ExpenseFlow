from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, cast, Date
from app.db.session import get_db
from app.models.transaction import Transaction
from app.models.category import Category, transaction_category
from app.schemas.analytics import ExpenseByCategory, ExpenseOverTime, ExpensesByCategoryResponse

router = APIRouter()

@router.get("/expenses-by-category", response_model=ExpensesByCategoryResponse)
async def get_expenses_by_category(
    db: AsyncSession = Depends(get_db),
    start_date: str | None = None,
    end_date: str | None = None,
):
    """
    Get total expenses grouped by category.
    """
    query = (
        select(Category.name, func.sum(Transaction.withdrawal_amount).label("total"))
        .join(transaction_category, Category.id == transaction_category.c.category_id)
        .join(Transaction, transaction_category.c.transaction_id == Transaction.id)
        .filter(Transaction.withdrawal_amount > 0)
    )

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    query = query.group_by(Category.name)

    result = await db.execute(query)
    rows = result.all()

    total_expense = sum(r.total for r in rows) if rows else 0

    items = []
    for name, amount in rows:
        percentage = (amount / total_expense * 100) if total_expense > 0 else 0
        items.append(ExpenseByCategory(
            category_name=name,
            amount=float(amount),
            percentage=round(percentage, 2)
        ))
    
    return ExpensesByCategoryResponse(
        items=items,
        total_amount=float(total_expense)
    )

@router.get("/expenses-over-time", response_model=List[ExpenseOverTime])
async def get_expenses_over_time(
    db: AsyncSession = Depends(get_db),
    start_date: str | None = None,
    end_date: str | None = None,
):
    """
    Get total expenses grouped by date.
    """
    # Cast datetime to date for grouping
    date_cast = cast(Transaction.date, Date)
    
    query = (
        select(date_cast.label("date"), func.sum(Transaction.withdrawal_amount).label("total"))
        .filter(Transaction.withdrawal_amount > 0)
    )

    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)

    query = query.group_by(date_cast).order_by(date_cast)

    result = await db.execute(query)
    rows = result.all()

    return [
        ExpenseOverTime(date=r.date, amount=float(r.total))
        for r in rows
    ]
