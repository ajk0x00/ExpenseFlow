from sqlalchemy import Column, Integer, String, Enum, JSON
from app.db.base_class import Base
import enum

class AccountType(str, enum.Enum):
    credit = "credit"
    debit = "debit"

class BankAccount(Base):
    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, index=True)
    bank_name = Column(String, index=True)
    description = Column(String, nullable=True)
    account_type = Column(Enum(AccountType), nullable=False)
    metadata_ = Column("metadata", JSON, nullable=True)
