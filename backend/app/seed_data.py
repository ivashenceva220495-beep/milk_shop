# app/seed_data.py
import sys
import os

# Добавляем папку /app в путь (нужно для Docker)
sys.path.insert(0, '/app')

from app.database import SessionLocal, engine
from app import models

def init_db():
    models.Base.metadata.create_all(bind=engine) #create table

    db = SessionLocal()

    if db.query(models.Order).count() > 0:
        print('В базе данных есть товары.')
        db.close()
        return

    #Молочные продукты
    products = [
        {
            "name": "Молоко",
            "category": models.ProductCategory.MILK,
            "price": 89.90,
            "unit": "л",
            "stock": 10,
            "description": "Пастеризованное молоко Простаквашино 3.2% жирности"
        },
        {
            "name": "Молоко «Фермерское» 2.5%",
            "category": models.ProductCategory.MILK,
            "price": 79.90,
            "unit": "л",
            "stock": 45,
            "description": "Свежее молоко от местных фермеров"
        },
        {
            "name": "Молоко топленое 4%",
            "category": models.ProductCategory.MILK,
            "price": 99.90,
            "unit": "л",
            "stock": 30,
            "description": "С натуральным вкусом топленого молока"
        },
        {
            "name": "Сыр «Российский» 50%",
            "category": models.ProductCategory.CHEESE,
            "price": 399.90,
            "unit": "кг",
            "stock": 20,
            "description": "Полутвердый сыр с насыщенным вкусом"
        },
        {
            "name": "Сыр «Моцарелла»",
            "category": models.ProductCategory.CHEESE,
            "price": 349.90,
            "unit": "кг",
            "stock": 23,
            "description": "Нежный итальянский сыр"
        },
        {
            "name": "Сыр плавленый «Дружба»",
            "category": models.ProductCategory.CHEESE,
            "price": 58.90,
            "unit": "шт",
            "stock": 100,
            "description": "Классический плавленый сырок"
        },
        {
            "name": "Йогурт питьевой «Клубника»",
            "category": models.ProductCategory.YOGURT,
            "price": 58.90,
            "unit": "шт",
            "stock": 100,
            "description": "Натуральный йогурт с клубникой"
        },
        {
            "name": "Йогурт греческий 2%",
            "category": models.ProductCategory.YOGURT,
            "price": 128.90,
            "unit": "шт",
            "stock": 190,
            "description": "Густой йогурт без добавок"
        },
        {
            "name": "Масло сливочное 82.5%%",
            "category": models.ProductCategory.BUTTER,
            "price": 128.90,
            "unit": "шт",
            "stock": 190,
            "description": "Традиционное сливочное масло"
        },
        {
            "name": "Сметана 20%",
            "category": models.ProductCategory.SOUR_CREAM,
            "price": 128.90,
            "unit": "шт",
            "stock": 190,
            "description": "Домашняя сметана"
        }
    ]


    try:
        for product_data in products:
            product = models.Product(**product_data)
            db.add(product)
        db.commit()

        print(f"Продукты в кол-ве {len(products)} добавлены в базу данных")
    except Exception as e:
        db.rollback()
        print("fОшибка при добавлении продуктов в базу данных")
    finally:
        db.close()

if __name__ == '__main__':
    init_db()