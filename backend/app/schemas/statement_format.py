from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class StatementFormatBase(BaseModel):
    """Base schema for StatementFormat"""
    format_name: str = Field(..., description="User-friendly name for this format")
    bank_name: Optional[str] = Field(None, description="Associated bank name")
    data_start_row: int = Field(..., gt=0, description="Row number where transaction data begins (1-indexed)")
    date_column: str = Field(..., description="Column identifier for transaction date (e.g., 'A', 'Date')")
    narration_column: str = Field(..., description="Column identifier for narration/description")
    withdrawal_column: str = Field(..., description="Column identifier for withdrawal/debit amount")
    deposit_column: str = Field(..., description="Column identifier for deposit/credit amount")


class StatementFormatCreate(StatementFormatBase):
    """Schema for creating a new StatementFormat"""
    pass


class StatementFormatUpdate(BaseModel):
    """Schema for updating a StatementFormat"""
    format_name: Optional[str] = None
    bank_name: Optional[str] = None
    data_start_row: Optional[int] = Field(None, gt=0)
    date_column: Optional[str] = None
    narration_column: Optional[str] = None
    withdrawal_column: Optional[str] = None
    deposit_column: Optional[str] = None


class StatementFormat(StatementFormatBase):
    """Schema for StatementFormat response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
