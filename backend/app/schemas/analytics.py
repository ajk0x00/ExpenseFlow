from pydantic import BaseModel
from datetime import date
from typing import List

class ExpenseByCategory(BaseModel):
    category_name: str
    amount: float
    percentage: float | None = None

class ExpenseOverTime(BaseModel):
    date: date
    amount: float

class AnalyticsResponse(BaseModel):
    by_category: List[ExpenseByCategory]
    over_time: List[ExpenseOverTime]

class ExpensesByCategoryResponse(BaseModel):
    items: List[ExpenseByCategory]
    total_amount: float
