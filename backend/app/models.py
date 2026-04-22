from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey,Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base
from sqlalchemy import func

class ProductCategory(enum.Enum):
    MILK ='milk'
    CHEESE ='cheese'
    YOGURT ='yogurt'
    BUTTER ='butter'
    SOUR_CREAM ='sour_cream'

class OrderStatus(enum.Enum):
    CONFIRMED = 'confirmed'
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,nullable=False)
    category = Column(Enum(ProductCategory),nullable=False)
    price = Column(Float,nullable=False)
    unit =Column(Enum('шт', 'кг', 'л', name='unit_types'), default='шт')
    stock = Column(Integer,default = 0)
    description = Column(String)

    order_items = relationship("OrderItem",back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True,index=True)
    customer_name = Column(String,nullable=False)
    customer_phone = Column(String,nullable=False)
    customer_email = Column(String)
    address = Column(String,nullable=False)
    status = Column(Enum(OrderStatus),default = OrderStatus.CONFIRMED)
    total_price =Column(Float,default = 0.0)
    created_at = Column(DateTime,default=func.now())
    updated_at = Column(DateTime,default=func.now(),onupdate=func.now())

    items = relationship("OrderItem",back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True,index=True)
    product_id = Column(Integer,ForeignKey('products.id'),nullable=False)
    order_id = Column(Integer,ForeignKey('orders.id'),nullable=False)
    quantity = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)

    order = relationship("Order",back_populates="items")
    product = relationship("Product",back_populates="order_items")