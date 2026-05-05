# SEC_FTS_internship

## Локальный запуск

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# или
venv\Scripts\activate  # Windows
# Установка зависимостей
pip install -r requirements.txt
# Настройка переменных окружения
cp .env.dev .env
# Запуск сервиса
python main.py
```

## Запуск через Docker

```bash
# Сборка контейнеров
docker compose up --build -d
# Автоматическая генерация миграции
alembic revision --autogenerate -m "описание изменений"
# Применение миграций Alembic
alembic upgrade head
# Разборка контейнеров
docker compose down 
# Запуск тестов 
docker compose --profile test run --rm test 
```
