from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ProductCategory(str, Enum):
    MILK = "milk"
    CHEESE = "cheese"
    YOGURT = "yogurt"
    BUTTER = "butter"
    SOUR_CREAM = "sour_cream"


class OrderStatus(str, Enum):
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


#Product - схемы
class ProductBase(BaseModel):
    name: str
    category: ProductCategory
    price: float
    unit: str = 'шт'
    stock: int
    description: Optional[str] = None


class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


#OrderItems schemas

class OrderItemsCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemsResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product_name: Optional[str] = None
    price: float

    class Config:
        from_attributes = True


#order schemas

class OrderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    customer_email: str
    address: str
    items: List[OrderItemsCreate]

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    address: str
    customer_email: Optional[str] = None
    status: OrderStatus
    total_price: float
    created_at: datetime
    items: List[OrderItemsResponse]

    class Config:
        from_attributes = True

class OrderStatusResponse(BaseModel):
    order_id: int
    status: OrderStatus
    customer_name: str
    customer_phone: Optional[str] = None
    updated_at: datetime
