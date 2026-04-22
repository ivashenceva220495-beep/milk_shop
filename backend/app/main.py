from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine  # ← добавить app.
from app import models
from app import routes

#Создаем таблицы

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = 'Молочный магазин API',
    description= 'API для интернет - магазина молочных продуктов',
    version = '1.0.0'
)

#Настройка CORS для фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

#Подключаем роуты
app.include_router(routes.router, prefix="/api/v1",tags=["Shop"])
@app.get("/")
def read_root():
    return {
        "message":"Добро пожаловать в API молочного магазина!",
        "docs": "/docs",
        "endpoints": {
            "products": "api/v1/products",
            "create_order": "api/v1/orders (POST)",
            "order_status": "api/v1/orders/{order_id}"
        }
    }