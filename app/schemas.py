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

class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1, max_length=120)
    phone: str = Field(min_length=3, max_length=30)
    pickup_time: datetime
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    item_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    customer_name: str
    phone: str
    pickup_time: datetime
    send_time: datetime
    prep_minutes: int
    status: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut]

    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    # อนุญาตแก้ pickup_time ได้ (แล้วระบบจะคำนวณ send_time ใหม่)
    pickup_time: Optional[datetime] = None
    # อนุญาตเปลี่ยน status
    status: Optional[str] = None