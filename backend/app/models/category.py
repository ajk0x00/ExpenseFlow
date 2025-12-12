from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# Association table for many-to-many relationship between Transaction and Category
transaction_category = Table(
    'transaction_category',
    Base.metadata,
    Column('transaction_id', Integer, ForeignKey('transaction.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)


class Category(Base):
    """Category model for organizing transactions into groups."""
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    
    # Many-to-many relationship with Transaction
    transactions = relationship(
        "Transaction",
        secondary=transaction_category,
        back_populates="categories"
    )
