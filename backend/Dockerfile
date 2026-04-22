FROM python:3.12-slim

#Рабочая директория

WORKDIR /app

#Присваиваем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Копируем проект
COPY . .

#Open port
EXPOSE 8000

#Run app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]