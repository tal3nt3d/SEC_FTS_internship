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

```bash
docker compose up --build -d # сборка контейнеров
docker compose down # разборка контейнера
docker compose --profile test run --rm test # запуск тестов 
```