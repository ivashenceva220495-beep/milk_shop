from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from unicodedata import category

from app.database import get_db
from app import models
from app import schemas

router = APIRouter()

#GET - view products
@router.get("/products", response_model=List[schemas.ProductResponse])
def get_products(
    category: schemas.ProductCategory = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    products = query.offset(skip).limit(limit).all()
    return products

# GET /products/product_id - получение конкретного продукта по id

@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product
# POST /orders - create order

@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = models.Order(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_email=order.customer_email,
        address=order.address,
        status= models.OrderStatus.CONFIRMED
    )

    db.add(db_order)
    db.flush() #должны получить id заказа без коммита

    total_price = 0
    order_items = []

    #Обработка заказа и товаров
    for item in order.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            db.rollback()
            raise HTTPException(status_code=404, detail="Товар не найден на складе")
        if product.stock < item.quantity:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=f"На складе не хватает товара {product.name}"
            )
        product.stock -= item.quantity

        order_item = models.OrderItem(
            order_id = db_order.id,
            product_id = product.id,
            quantity = item.quantity,
            price= product.price
        )
        #обновление суммы заказа
        db.add(order_item)
        total_price += product.price * item.quantity
        order_items.append(order_item)

        db_order.total_price = total_price

        db.commit()
        db.refresh(db_order)

        #формирование ответа с названиями продуктов

        response_items =[]
        for item in order_items:
            response_items.append(schemas.OrderItemsResponse(
                id = item.id,
                product_id = item.product_id,
                product_name = item.product.name,
                quantity = item.quantity,
                price = item.price
            ))
        return schemas.OrderResponse(
            id = db_order.id,
            customer_name = db_order.customer_name,
            customer_phone = db_order.customer_phone,
            address = db_order.address,
            status = db_order.status,
            total_price = total_price,
            created_at = db_order.created_at,
            items = response_items
        )
# GET /orders/{order_id} - получение статуса заказа
@router.get("/orders/{order_id}", response_model=schemas.OrderStatusResponse)
def get_order_status(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    customer_phone = getattr(order,"customer_phone", None)

    return schemas.OrderStatusResponse(
        order_id = order.id,
        status = order.status,
        customer_name = order.customer_name,
        updated_at= order.updated_at,
        customer_phone = customer_phone
    )

#GET - полная информация о заказе
@router.get("/orders/{order_id}/full", response_model=schemas.OrderResponse)
def get_order_full(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail= "Заказ не найден")
    response_items = []
    for item in order.items:
        response_items.append(schemas.OrderItemsResponse(
            id = item.id,
            product_id = item.product_id,
            product_name = item.product.name,
            quantity = item.quantity,
            price = item.price
        ))

    return schemas.OrderResponse(
        id = order.id,
        customer_name = order.customer_name,
        customer_phone = order.customer_phone,
        address = order.address,
        status = order.status,
        total_price = order.total_price,
        created_at = order.created_at,
        items = response_items
    )