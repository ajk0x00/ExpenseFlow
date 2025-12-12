from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from datetime import datetime

class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("bankaccount.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    narration = Column(String, nullable=False)
    withdrawal_amount = Column(Numeric(10, 2), default=0.0)
    deposit_amount = Column(Numeric(10, 2), default=0.0)
    metadata_ = Column("metadata", JSON, nullable=True)

    account = relationship("BankAccount", backref="transactions")
    
    # Many-to-many relationship with Category
    # The association table is defined in category.py module
    categories = relationship(
        "Category",
        secondary="transaction_category",
        back_populates="transactions"
    )
