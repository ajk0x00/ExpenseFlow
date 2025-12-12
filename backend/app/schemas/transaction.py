from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal
from app.schemas.category import Category

class TransactionBase(BaseModel):
    account_id: int
    date: datetime
    narration: str
    withdrawal_amount: Optional[Decimal] = Decimal('0.00')
    deposit_amount: Optional[Decimal] = Decimal('0.00')
    metadata_: Optional[Dict[str, Any]] = None

class TransactionCreate(TransactionBase):
    category_ids: Optional[List[int]] = None  # If not provided, defaults to 'others' category

class TransactionUpdate(TransactionBase):
    account_id: Optional[int] = None
    date: Optional[datetime] = None
    narration: Optional[str] = None
    withdrawal_amount: Optional[Decimal] = None
    deposit_amount: Optional[Decimal] = None
    category_ids: Optional[List[int]] = None

class TransactionInDBBase(TransactionBase):
    id: int

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    categories: List["Category"] = []
