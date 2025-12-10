from typing import Optional, Dict, Any
from pydantic import BaseModel
from app.models.account import AccountType

class BankAccountBase(BaseModel):
    account_name: str
    bank_name: str
    description: Optional[str] = None
    account_type: AccountType
    metadata_: Optional[Dict[str, Any]] = None

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BankAccountBase):
    account_name: Optional[str] = None
    bank_name: Optional[str] = None
    account_type: Optional[AccountType] = None

class BankAccountInDBBase(BankAccountBase):
    id: int

    class Config:
        from_attributes = True

class BankAccount(BankAccountInDBBase):
    pass
