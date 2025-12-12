from typing import Optional
from pydantic import BaseModel


class CategoryBase(BaseModel):
    """Base schema for Category."""
    name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a Category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a Category. All fields are optional."""
    name: Optional[str] = None
    description: Optional[str] = None


class CategoryInDBBase(CategoryBase):
    """Base schema for Category in database."""
    id: int

    class Config:
        from_attributes = True


class Category(CategoryInDBBase):
    """Schema for Category response."""
    pass
