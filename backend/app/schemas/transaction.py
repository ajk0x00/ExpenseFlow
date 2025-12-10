from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

class TransactionBase(BaseModel):
    account_id: int
    date: datetime
    narration: str
    withdrawal_amount: Optional[Decimal] = Decimal('0.00')
    deposit_amount: Optional[Decimal] = Decimal('0.00')
    metadata_: Optional[Dict[str, Any]] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(TransactionBase):
    account_id: Optional[int] = None
    date: Optional[datetime] = None
    narration: Optional[str] = None
    withdrawal_amount: Optional[Decimal] = None
    deposit_amount: Optional[Decimal] = None

class TransactionInDBBase(TransactionBase):
    id: int

    class Config:
        from_attributes = True

class Transaction(TransactionInDBBase):
    pass
