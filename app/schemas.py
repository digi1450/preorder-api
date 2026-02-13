from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CategoryOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    price: float = Field(gt=0)
    category_id: Optional[int] = None


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    price: Optional[float] = Field(default=None, gt=0)
    category_id: Optional[int] = None


class MenuItemOut(BaseModel):
    id: int
    name: str
    price: float
    category_id: Optional[int] = None

    class Config:
        from_attributes = True