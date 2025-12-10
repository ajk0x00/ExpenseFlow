from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base


class StatementFormat(Base):
    """Model for storing bank statement XLSX format configuration"""
    
    id = Column(Integer, primary_key=True, index=True)
    format_name = Column(String, nullable=False, index=True)
    bank_name = Column(String, nullable=True, index=True)
    
    # Row configuration
    data_start_row = Column(Integer, nullable=False, comment="Row number where transaction data begins (1-indexed)")
    
    # Column configuration (supports column letters like 'A', 'B' or names like 'Date', 'Amount')
    date_column = Column(String, nullable=False, comment="Column identifier for transaction date")
    narration_column = Column(String, nullable=False, comment="Column identifier for narration/description")
    withdrawal_column = Column(String, nullable=False, comment="Column identifier for withdrawal/debit amount")
    deposit_column = Column(String, nullable=False, comment="Column identifier for deposit/credit amount")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
